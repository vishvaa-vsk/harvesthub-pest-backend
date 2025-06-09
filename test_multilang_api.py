#!/usr/bin/env python3
"""
Test script for the new multi-language pest detection API
"""

import requests
import json
import os
from pathlib import Path

# API base URL
BASE_URL = "http://127.0.0.1:5000"

def test_health_endpoints():
    """Test health endpoints"""
    print("🔍 Testing health endpoints...")
    
    # Test main health endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Main endpoint: {data['message']}")
            print(f"   Version: {data['version']}")
            print(f"   Features: {', '.join(data['features'])}")
        else:
            print(f"❌ Main endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Main endpoint error: {e}")
    
    # Test detailed health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            health = data['health']
            print(f"✅ Health endpoint: Model loaded: {health['model_loaded']}, Labels: {health['total_classes']}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")

def test_languages_endpoint():
    """Test supported languages endpoint"""
    print("\n🌐 Testing languages endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/languages")
        if response.status_code == 200:
            data = response.json()
            languages = data['supported_languages']
            print(f"✅ Languages endpoint: {data['total_languages']} languages supported")
            print("   Supported languages:")
            for code, name in languages.items():
                print(f"     {code}: {name}")
        else:
            print(f"❌ Languages endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Languages endpoint error: {e}")

def test_prediction_api():
    """Test prediction API with different languages"""
    print("\n🔮 Testing prediction API...")
    
    # Create a dummy image file for testing
    test_image_path = create_test_image()
    
    if not test_image_path:
        print("❌ Could not create test image, skipping prediction tests")
        return
    
    # Test languages to try
    test_languages = ['en', 'hi', 'ta']
    
    for lang in test_languages:
        print(f"\n🧪 Testing prediction in {lang}...")
        
        try:
            with open(test_image_path, 'rb') as img_file:
                files = {'file': img_file}
                response = requests.post(f"{BASE_URL}/predict/{lang}", files=files)
                
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Prediction successful for {lang}")
                print(f"   Predicted: {data['prediction']['label']} (confidence: {data['prediction']['confidence']:.3f})")
                print(f"   Language: {data['language']['name']}")
                print(f"   Source: {data['source']}")
                print(f"   Diagnosis: {data['recommendation']['diagnosis'][:100]}...")
                print(f"   Treatments: {len(data['recommendation']['treatments'])} recommendations")
            else:
                print(f"❌ Prediction failed for {lang}: {response.status_code}")
                if response.text:
                    print(f"   Error: {response.json().get('message', 'Unknown error')}")
                    
        except Exception as e:
            print(f"❌ Prediction error for {lang}: {e}")
    
    # Clean up test image
    if os.path.exists(test_image_path):
        os.remove(test_image_path)

def test_error_handling():
    """Test error handling for invalid inputs"""
    print("\n⚠️  Testing error handling...")
    
    # Test unsupported language
    try:
        files = {'file': ('test.txt', b'fake image data', 'text/plain')}
        response = requests.post(f"{BASE_URL}/predict/xx", files=files)
        if response.status_code == 400:
            print("✅ Unsupported language correctly rejected")
        else:
            print(f"❌ Expected 400 for unsupported language, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing unsupported language: {e}")
    
    # Test missing file
    try:
        response = requests.post(f"{BASE_URL}/predict/en")
        if response.status_code == 400:
            print("✅ Missing file correctly rejected")
        else:
            print(f"❌ Expected 400 for missing file, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing missing file: {e}")

def create_test_image():
    """Create a small test image for API testing"""
    try:
        from PIL import Image
        import numpy as np
        
        # Create a simple test image
        image_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        image = Image.fromarray(image_array)
        
        test_image_path = "test_image.jpg"
        image.save(test_image_path, "JPEG")
        
        print(f"✅ Created test image: {test_image_path}")
        return test_image_path
        
    except Exception as e:
        print(f"❌ Could not create test image: {e}")
        return None

def main():
    """Run all tests"""
    print("🚀 Testing HarvestHub Multi-Language Pest Detection API\n")
    print(f"Testing API at: {BASE_URL}")
    print("="*60)
    
    # Run all tests
    test_health_endpoints()
    test_languages_endpoint()
    test_prediction_api()
    test_error_handling()
    
    print("\n" + "="*60)
    print("✅ Testing completed!")
    print("\n📝 Next steps:")
    print("1. Add your actual GEMINI_API_KEY to .env file")
    print("2. Replace model.h5 with your trained TensorFlow model")
    print("3. Test with real plant disease images")
    print("4. Configure Firebase for production use")

if __name__ == "__main__":
    main()
