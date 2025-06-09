from flask import request, jsonify
from .model import PestDetectionModel
from .helpers import get_pest_recommendation
import os

# Initialize the model
model_instance = PestDetectionModel()

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'bn': 'Bengali',
    'pa': 'Punjabi',
    'or': 'Odia',
    'as': 'Assamese'
}

def init_routes(app):
    @app.route('/', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "success",
            "message": "HarvestHub Pest Detection API is running",
            "version": "2.0.0",
            "features": [
                "Multi-language pest detection",
                "AI-powered recommendations",
                "Firebase caching",
                "12 Indian languages supported"
            ]
        })

    @app.route('/languages', methods=['GET'])
    def get_supported_languages():
        """Get list of supported languages"""
        return jsonify({
            "status": "success",
            "supported_languages": SUPPORTED_LANGUAGES,
            "total_languages": len(SUPPORTED_LANGUAGES)
        })

    @app.route('/predict/<lang>', methods=['POST'])
    def predict_with_language(lang):
        """Main prediction endpoint with language-specific recommendations"""
        try:
            # Validate language code
            if lang not in SUPPORTED_LANGUAGES:
                return jsonify({
                    "status": "error",
                    "message": f"Unsupported language code: {lang}. Supported languages: {list(SUPPORTED_LANGUAGES.keys())}"
                }), 400            # Check if image file is present
            if 'file' not in request.files:
                return jsonify({
                    "status": "error",
                    "message": "No image file provided. Use 'file' as the form field name."
                }), 400

            file = request.files['file']
            
            if file.filename == '':
                return jsonify({
                    "status": "error",
                    "message": "No image file selected"
                }), 400

            # Validate file type
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
            if not ('.' in file.filename and 
                    file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
                return jsonify({
                    "status": "error",
                    "message": "Invalid file type. Supported: PNG, JPG, JPEG, GIF, BMP"
                }), 400

            # Get prediction from model
            prediction_result = model_instance.predict(file)
            
            if prediction_result is None:
                return jsonify({
                    "status": "error",
                    "message": "Failed to process image"
                }), 500

            # Get language-specific pest recommendation
            recommendation = get_pest_recommendation(prediction_result['label'], lang)
            
            # Combine prediction and recommendation with enhanced response format
            response = {
                "status": "success",
                "prediction": prediction_result,
                "recommendation": recommendation['data'],
                "language": {
                    "code": lang,
                    "name": SUPPORTED_LANGUAGES[lang]
                },
                "source": recommendation['source'],
                "timestamp": prediction_result.get('timestamp')
            }
            
            return jsonify(response)

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Internal server error: {str(e)}"
            }), 500

    @app.route('/predict', methods=['POST'])
    def predict_default():
        """Default prediction endpoint (English)"""
        return predict_with_language('en')

    @app.route('/health', methods=['GET'])
    def detailed_health():
        """Detailed health check endpoint"""
        try:
            model_loaded = model_instance.model is not None
            labels_loaded = len(model_instance.labels) > 0
            
            return jsonify({
                "status": "success",
                "health": {
                    "model_loaded": model_loaded,
                    "labels_loaded": labels_loaded,
                    "total_classes": len(model_instance.labels)
                }
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Health check failed: {str(e)}"
            }), 500
