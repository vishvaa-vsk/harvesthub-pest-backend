import os
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    # Initialize Firebase app
    firebase_key_path = os.path.join(os.path.dirname(__file__), 'firebase-key.json')
    if os.path.exists(firebase_key_path):
        cred = credentials.Certificate(firebase_key_path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase initialized successfully")
    else:
        print("Warning: Firebase key file not found. Caching disabled.")
        db = None
except Exception as e:
    print(f"Warning: Firebase initialization failed: {e}")
    db = None

# Initialize Gemini API
try:
    import google.generativeai as genai
    
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if gemini_api_key:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("Gemini API initialized successfully")
    else:
        print("Warning: GEMINI_API_KEY not found in environment variables")
        model = None
except Exception as e:
    print(f"Warning: Gemini API initialization failed: {e}")
    model = None

# Language mappings for Gemini prompts
LANGUAGE_NAMES = {
    'en': 'English',
    'hi': 'Hindi (हिन्दी)',
    'ta': 'Tamil (தமிழ்)',
    'te': 'Telugu (తెలుగు)',
    'kn': 'Kannada (ಕನ್ನಡ)',
    'ml': 'Malayalam (മലയാളം)',
    'mr': 'Marathi (मराठी)',
    'gu': 'Gujarati (ગુજરાતી)',
    'bn': 'Bengali (বাংলা)',
    'pa': 'Punjabi (ਪੰਜਾਬੀ)',
    'or': 'Odia (ଓଡ଼ିଆ)',
    'as': 'Assamese (অসমীয়া)'
}

def get_pest_recommendation(label, lang='en'):
    """
    Get localized pest recommendation using Firebase cache or Gemini API
    
    Args:
        label (str): Predicted pest/disease label
        lang (str): Language code (e.g., 'en', 'hi', 'ta')
    
    Returns:
        dict: Recommendation data with source information
    """
    try:
        # Create cache key
        cache_key = f"{label}::{lang}"
        
        # Try to get from Firebase cache first
        cached_result = get_from_firestore_cache(cache_key)
        if cached_result:
            return {
                "source": "firebase",
                "data": cached_result
            }
        
        # If not in cache, generate using Gemini API
        if model:
            gemini_result = generate_gemini_recommendation(label, lang)
            if gemini_result:
                # Cache the result in Firestore
                cache_to_firestore(cache_key, gemini_result)
                return {
                    "source": "gemini",
                    "data": gemini_result
                }
        
        # Fallback to default response
        return get_fallback_recommendation(label, lang)
        
    except Exception as e:
        print(f"Error getting pest recommendation: {e}")
        return get_fallback_recommendation(label, lang)

def generate_gemini_recommendation(label, lang):
    """
    Generate pest recommendation using Gemini API
    
    Args:
        label (str): Pest/disease label
        lang (str): Language code
    
    Returns:
        dict: Generated recommendation
    """
    try:
        language_name = LANGUAGE_NAMES.get(lang, 'English')
        
        # Create detailed prompt for Gemini
        prompt = f"""
You are an expert agricultural pathologist specializing in Indian farming practices. 

Analyze this plant disease/pest: "{label}"

Provide a comprehensive response in {language_name} language with the following structure:

1. DIAGNOSIS: Detailed description of the disease/pest condition, symptoms, and impact on the crop
2. CAUSAL_AGENT: Scientific name and type of pathogen/pest (fungus, bacteria, virus, insect, etc.)
3. TREATMENTS: List of 3-4 practical treatment recommendations suitable for Indian farmers, including:
   - Local/organic remedies using common household items
   - Chemical pesticides/fungicides available in Indian markets
   - Preventive agricultural practices
   - Cultural management techniques

Format your response as a valid JSON object with these exact keys:
{{
    "diagnosis": "detailed diagnosis in {language_name}",
    "causal_agent": "scientific name and type of pathogen/pest in {language_name}",
    "treatments": [
        "treatment 1 in {language_name}",
        "treatment 2 in {language_name}",
        "treatment 3 in {language_name}",
        "treatment 4 in {language_name}"
    ]
}}

Important notes:
- Use simple, farmer-friendly language
- Include local Indian pesticide/fungicide brand names when relevant
- Consider cost-effective solutions for small-scale farmers
- Mention organic/natural alternatives when possible
- Ensure all text is in {language_name} language
"""

        # Generate response
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up the response text to extract JSON
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        # Parse JSON response
        recommendation_data = json.loads(response_text.strip())
        
        # Validate required fields
        required_fields = ['diagnosis', 'causal_agent', 'treatments']
        if all(field in recommendation_data for field in required_fields):
            return recommendation_data
        else:
            print(f"Invalid Gemini response format: missing required fields")
            return None
            
    except json.JSONDecodeError as e:
        print(f"Error parsing Gemini JSON response: {e}")
        print(f"Raw response: {response_text}")
        return None
    except Exception as e:
        print(f"Error generating Gemini recommendation: {e}")
        return None

def get_from_firestore_cache(cache_key):
    """
    Retrieve recommendation from Firestore cache
    
    Args:
        cache_key (str): Cache key in format "label::lang"
    
    Returns:
        dict or None: Cached recommendation data
    """
    try:
        if not db:
            return None
            
        doc_ref = db.collection('remedies').document(cache_key)
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            print(f"Retrieved from Firestore cache: {cache_key}")
            return {
                'diagnosis': data.get('diagnosis', ''),
                'causal_agent': data.get('causal_agent', ''),
                'treatments': data.get('treatments', [])
            }
        
        return None
        
    except Exception as e:
        print(f"Error retrieving from Firestore cache: {e}")
        return None

def cache_to_firestore(cache_key, recommendation_data):
    """
    Cache recommendation to Firestore
    
    Args:
        cache_key (str): Cache key in format "label::lang"
        recommendation_data (dict): Recommendation data to cache
    """
    try:
        if not db:
            return
            
        doc_ref = db.collection('remedies').document(cache_key)
        
        # Add metadata
        cache_data = {
            'diagnosis': recommendation_data.get('diagnosis', ''),
            'causal_agent': recommendation_data.get('causal_agent', ''),
            'treatments': recommendation_data.get('treatments', []),
            'cached_at': firestore.SERVER_TIMESTAMP,
            'source': 'gemini'
        }
        
        doc_ref.set(cache_data)
        print(f"Cached to Firestore: {cache_key}")
        
    except Exception as e:
        print(f"Error caching to Firestore: {e}")

def get_fallback_recommendation(label, lang):
    """
    Generate fallback recommendation when Gemini API fails
    
    Args:
        label (str): Pest/disease label
        lang (str): Language code
    
    Returns:
        dict: Fallback recommendation
    """
    language_name = LANGUAGE_NAMES.get(lang, 'English')
    
    # Basic fallback responses in different languages
    fallback_responses = {
        'en': {
            'diagnosis': f'Plant condition identified as {label}. Please consult with local agricultural extension officer for detailed diagnosis.',
            'causal_agent': 'Requires professional diagnosis',
            'treatments': [
                'Consult local agricultural extension officer',
                'Take sample to nearest Krishi Vigyan Kendra (KVK)',
                'Contact helpline: 1800-180-1551 (Kisan Call Centre)',
                'Maintain proper field hygiene and crop rotation'
            ]
        },
        'hi': {
            'diagnosis': f'पौधे की स्थिति {label} के रूप में पहचानी गई। विस्तृत निदान के लिए स्थानीय कृषि विस्तार अधिकारी से सलाह लें।',
            'causal_agent': 'व्यावसायिक निदान की आवश्यकता',
            'treatments': [
                'स्थानीय कृषि विस्तार अधिकारी से सलाह लें',
                'निकटतम कृषि विज्ञान केन्द्र (KVK) में नमूना ले जाएं',
                'हेल्पलाइन संपर्क करें: 1800-180-1551 (किसान कॉल सेंटर)',
                'उचित खेत स्वच्छता और फसल चक्र बनाए रखें'
            ]
        },
        'ta': {
            'diagnosis': f'தாவர நிலை {label} என அடையாளம் காணப்பட்டுள்ளது. விரிவான நோயறிதலுக்கு உள்ளூர் விவசாய விரிவாக்க அதிகாரியுடன் கலந்தாலோசிக்கவும்.',
            'causal_agent': 'தொழில்முறை நோயறிதல் தேவை',
            'treatments': [
                'உள்ளூர் விவசாய விரிவாக்க அதிகாரியுடன் கலந்தாலோசிக்கவும்',
                'அருகிலுள்ள கிருஷி விஞ்ஞான் கேந்திராவிற்கு (KVK) மாதிரி எடுத்துச் செல்லுங்கள்',
                'உதவி எண்ணை தொடர்பு கொள்ளுங்கள்: 1800-180-1551 (கிசான் கால் சென்டர்)',
                'சரியான வயல் சுகாதாரம் மற்றும் பயிர் சுழற்சியை பராமரிக்கவும்'
            ]
        }
    }
    
    # Get appropriate fallback response
    fallback = fallback_responses.get(lang, fallback_responses['en'])
    
    return {
        "source": "fallback",
        "data": fallback
    }
