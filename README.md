# HarvestHub Pest Detection Backend

A modern Flask-based API for intelligent crop pest detection using TensorFlow/Keras image classification with **multi-language AI-powered recommendations**. Transformed from a static CSV system to a dynamic, AI-driven platform supporting 12 Indian languages.

## 🌟 Key Features

- 🔬 **AI-Powered Detection**: TensorFlow/Keras model for 66 pest/disease classes
- 🌐 **Multi-Language Support**: 12 Indian languages with native script support
- 🤖 **Dynamic Recommendations**: Google Gemini AI integration for expert-level agricultural advice
- 📸 **Smart Image Processing**: Automatic preprocessing and normalization
- ⚡ **Firebase Caching**: Intelligent caching system for performance optimization
- 🛡️ **Production Ready**: Comprehensive error handling and security
- 🚀 **RESTful API**: Clean, structured JSON responses

## 📋 Supported Languages

| Code | Language  | Native Script |
| ---- | --------- | ------------- |
| `en` | English   | English       |
| `hi` | Hindi     | हिन्दी           |
| `ta` | Tamil     | தமிழ்           |
| `te` | Telugu    | తెలుగు           |
| `kn` | Kannada   | ಕನ್ನಡ          |
| `ml` | Malayalam | മലയാളം          |
| `mr` | Marathi   | मराठी           |
| `gu` | Gujarati  | ગુજરાતી          |
| `bn` | Bengali   | বাংলা            |
| `pa` | Punjabi   | ਪੰਜਾਬੀ           |
| `or` | Odia      | ଓଡ଼ିଆ           |
| `as` | Assamese  | অসমীয়া          |

## 🔄 Major Transformation (June 2025)

### Before vs After

| Aspect               | Before (CSV System)    | After (AI System)             |
| -------------------- | ---------------------- | ----------------------------- |
| **Recommendations**  | Static CSV lookup      | AI-generated, contextual      |
| **Languages**        | English only           | 12 Indian languages           |
| **Response Quality** | Basic, fixed responses | Expert-level, detailed advice |
| **Performance**      | Instant (static)       | Smart caching (100ms-2s)      |
| **Scalability**      | Limited by CSV size    | Unlimited with AI             |
| **Maintenance**      | Manual CSV updates     | Self-updating AI responses    |
| **Localization**     | None                   | Native language support       |

### Key Changes Made

#### 1. **API Architecture Overhaul**
- **Old**: `/predict` endpoint with static responses
- **New**: `/predict/<lang>` with language-specific AI recommendations

#### 2. **Backend Intelligence Enhancement**
- **Removed**: `app/data/pests.csv` (static data)
- **Added**: Google Gemini 1.5 Flash integration
- **Enhanced**: Dynamic recommendation generation

#### 3. **Caching System Implementation**
- **Collection**: Firebase Firestore `remedies` collection
- **Structure**: `<pest_label>::<language_code>` document IDs
- **Fallback**: Firebase → Gemini API → Static fallback

#### 4. **Multi-Language Infrastructure**
- **Language validation** for all endpoints
- **Native script responses** in requested languages
- **Culturally appropriate** agricultural advice

#### 5. **Code Architecture Improvements**
- **helpers.py**: Complete rewrite with AI integration
- **routes.py**: Enhanced with language support
- **Error handling**: Comprehensive validation system

## 📁 Project Structure

```
harvesthub-pest-backend/
├── .env                           # Environment variables
├── .gitignore                     # Git ignore patterns
├── main.py                        # Flask application entry point
├── requirements.txt               # Python dependencies
├── test_multilang_api.py          # Comprehensive test suite
├── app/                           # Main application package
│   ├── __init__.py               # Package initialization
│   ├── routes.py                 # Flask API endpoints (multi-language)
│   ├── model.py                  # TensorFlow model loading
│   ├── helpers.py                # Gemini AI & Firebase integration
│   ├── firebase-key.json         # Firebase service account key
│   └── data/
│       ├── model.h5              # TensorFlow model file (66 classes)
│       └── labels.txt            # Class labels
└── README.md                     # This documentation
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo>
cd harvesthub-pest-backend

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
# Create environment file
cp .env.example .env

# Add your API keys to .env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Firebase Setup (Optional but Recommended)

1. Create a Firebase project at https://console.firebase.google.com
2. Enable Firestore Database
3. Generate a service account key
4. Save it as `app/firebase-key.json` in the app directory

### 4. Add Your Model

- Place your trained TensorFlow model as `app/data/model.h5`
- Update `app/data/labels.txt` with your class labels (one per line)
- Ensure your model expects 224x224x3 input images

### 5. Run the Application

```bash
# Development mode
python main.py

# The API will be available at http://localhost:5000
```

## 🌐 API Endpoints

### Health Check
```http
GET /
```
Returns basic API status.

**Response:**
```json
{
  "message": "HarvestHub Pest Detection API",
  "status": "running"
}
```

### Detailed Health Check
```http
GET /health
```
Returns detailed system status including model and configuration.

**Response:**
```json
{
  "model_loaded": true,
  "labels_loaded": true,
  "labels_count": 66,
  "firebase_configured": true,
  "gemini_configured": true,
  "status": "healthy"
}
```

### Get Supported Languages
```http
GET /languages
```
Returns all supported languages for multi-language predictions.

**Response:**
```json
{
  "supported_languages": {
    "en": "English",
    "hi": "Hindi", 
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "gu": "Gujarati",
    "bn": "Bengali",
    "pa": "Punjabi",
    "or": "Odia",
    "as": "Assamese"
  },
  "count": 12
}
```

### Multi-Language Prediction
```http
POST /predict/<lang>
```
Upload an image for pest detection with recommendations in the specified language.

**Parameters:**
- `<lang>`: Language code (en, hi, ta, te, kn, ml, mr, gu, bn, pa, or, as)

**Request:**
- `Content-Type: multipart/form-data`
- `image`: Image file (PNG, JPG, JPEG, GIF, BMP)

**Response:**
```json
{
  "status": "success",
  "language": {
    "code": "ta",
    "name": "Tamil"
  },
  "prediction": {
    "label": "Tomato___Early_blight",
    "confidence": 0.95,
    "index": 42
  },
  "recommendation": {
    "diagnosis": "தக்காளி இலைகளில் பழுப்பு நிற புள்ளிகள் தோன்றி உள்ளன...",
    "causal_agent": "அல்டர்னேரியா சோலானி (Alternaria solani)",
    "treatments": [
      "காப்பர் அடிப்படையிலான பூஞ்சாணக் கொல்லி தெளிக்கவும்",
      "பாதிக்கப்பட்ட இலைகளை அகற்றி அழிக்கவும்",
      "சரியான காற்று சுழற்சியை உறுதி செய்யவும்"
    ]
  },
  "source": "firebase"
}
```

## 💡 Usage Examples

### Test API with cURL
```bash
# Check API health
curl http://localhost:5000/health

# Get supported languages
curl http://localhost:5000/languages

# Upload image for English prediction
curl -X POST -F "image=@test_image.jpg" http://localhost:5000/predict/en

# Upload image for Tamil prediction  
curl -X POST -F "image=@test_image.jpg" http://localhost:5000/predict/ta
```

### Python Example
```python
import requests

# Health check
response = requests.get('http://localhost:5000/health')
print(response.json())

# Multi-language prediction
with open('plant_image.jpg', 'rb') as img:
    files = {'image': img}
    response = requests.post('http://localhost:5000/predict/ta', files=files)
    result = response.json()
    print(f"Prediction: {result['prediction']['label']}")
    print(f"Diagnosis: {result['recommendation']['diagnosis']}")
```

## 🧠 Intelligent Recommendation System

The system uses a **multi-tier hybrid approach** for generating pest recommendations:

### 1. **Firebase Cache** (Fastest)
- Checks for previously generated recommendations
- Document ID format: `<pest_label>::<language_code>`
- Response time: ~100-200ms

### 2. **Google Gemini AI** (Dynamic)
- Generates contextual, expert-level recommendations
- Uses `gemini-1.5-flash` model for optimal performance
- Tailored for Indian agricultural practices
- Response time: ~2-3 seconds (first time)

### 3. **Automatic Caching**
- Stores Gemini responses in Firebase for future use
- Reduces API calls and improves performance
- Language-specific caching for localized responses

### 4. **Fallback System**
- Static fallback for system failures
- Ensures API reliability and uptime
- Graceful degradation with informative error messages

### Cache Structure
```
Firebase Collection: 'remedies'
Document ID: 'Tomato___Early_blight::ta'
Content: {
  "diagnosis": "தக்காளி இலைகளில் ஆரம்பகால துர்நாற்ற நோய்...",
  "causal_agent": "அல்டர்னேரியா சோலானி",
  "treatments": [...],
  "timestamp": "2024-12-09T10:30:00Z",
  "language": "ta"
}
```

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# Required: Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Custom Firebase key path (default: app/firebase-key.json)
FIREBASE_KEY_PATH=path/to/your/firebase-key.json
```

### Gemini API Setup
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create an API key
3. Add it to your `.env` file
4. The system uses `gemini-1.5-flash` model for optimal performance

### Firebase Setup (Recommended)
1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com)
2. Enable **Firestore Database** in Native mode
3. Go to **Project Settings** → **Service Accounts**
4. Generate a new private key (JSON)
5. Save it as `app/firebase-key.json` in the app directory

### Model Configuration
- **Input Shape**: 224x224x3 (RGB images)
- **Classes**: 66 pest/disease categories
- **Format**: TensorFlow/Keras H5 model
- **Labels**: One class per line in `app/data/labels.txt`

## 🌍 Supported Languages

| Language  | Code | Native Name |
| --------- | ---- | ----------- |
| English   | `en` | English     |
| Hindi     | `hi` | हिन्दी         |
| Tamil     | `ta` | தமிழ்         |
| Telugu    | `te` | తెలుగు         |
| Kannada   | `kn` | ಕನ್ನಡ        |
| Malayalam | `ml` | മലയാളം        |
| Marathi   | `mr` | मराठी         |
| Gujarati  | `gu` | ગુજરાતી        |
| Bengali   | `bn` | বাংলা          |
| Punjabi   | `pa` | ਪੰਜਾਬੀ         |
| Odia      | `or` | ଓଡ଼ିଆ         |
| Assamese  | `as` | অসমীয়া        |

## 🏃‍♂️ Running the Application

### Development Mode
```bash
python main.py
# Server runs at http://localhost:5000
```

### Production Mode (Recommended)
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn (4 workers)
gunicorn -w 4 -b 0.0.0.0:5000 main:create_app()

# Run with timeout settings
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 main:create_app()
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:create_app()"]
```

## 🛠️ Error Handling

The API includes comprehensive error handling for all scenarios:

### Image Upload Errors
```json
{
  "error": "No image file provided",
  "status": "error"
}
```

### Language Validation Errors
```json
{
  "error": "Unsupported language 'xyz'. Supported: en, hi, ta, te, kn, ml, mr, gu, bn, pa, or, as",
  "status": "error"
}
```

### Model Prediction Errors
```json
{
  "error": "Error processing image: Invalid image format",
  "status": "error"
}
```

### API Service Errors
```json
{
  "error": "Recommendation service temporarily unavailable",
  "fallback": "Static recommendation provided",
  "status": "partial"
}
```

## 📊 Performance Metrics

### Response Times
- **Health Check**: ~5-10ms
- **Cached Predictions**: ~100-200ms (Firebase retrieval)
- **New Predictions**: ~2-3 seconds (first-time Gemini generation)
- **Model Inference**: ~60-80ms (TensorFlow processing)

### Optimization Features
- **Smart Caching**: Reduces repeated API calls
- **Async Processing**: Non-blocking Firebase operations
- **Error Recovery**: Graceful fallback mechanisms
- **Memory Efficient**: Model loaded once at startup

## 🧪 Testing

### Automated Test Suite
```bash
# Run comprehensive tests
python test_multilang_api.py
```

**Test Coverage:**
- ✅ Health endpoints functionality
- ✅ Language validation and support
- ✅ Multi-language predictions
- ✅ Firebase caching operations
- ✅ Gemini AI integration
- ✅ Error handling scenarios

### Manual Testing
```bash
# Test with sample image
curl -X POST -F "image=@sample_plant.jpg" http://localhost:5000/predict/en

# Test error handling
curl -X POST http://localhost:5000/predict/invalid_lang

# Test health checks
curl http://localhost:5000/health
```

## 📈 Monitoring & Debugging

### Logging
The application provides detailed logging for:
- Image processing steps
- Model prediction results
- Firebase cache operations
- Gemini API interactions
- Error conditions and fallbacks

### Health Monitoring
Use the `/health` endpoint to monitor:
- Model loading status
- Firebase connectivity
- Gemini API configuration
- System resource usage

## 🔧 Troubleshooting

### Common Issues

**1. Model Loading Errors**
```bash
# Check if model file exists and is valid
ls -la app/data/model.h5
# Ensure model is compatible with TensorFlow version
```

**2. Firebase Connection Issues**
```bash
# Verify firebase-key.json exists and is valid
ls -la app/firebase-key.json
# Check Firebase project permissions
```

**3. Gemini API Errors**
```bash
# Verify API key in .env file
cat .env | grep GEMINI_API_KEY
# Test API key manually
```

**4. Image Upload Problems**
```bash
# Check supported formats: PNG, JPG, JPEG, GIF, BMP
# Ensure image size is reasonable (< 10MB recommended)
```

## 🚀 Production Deployment

### Pre-Deployment Checklist
- [ ] Environment variables configured (`.env` file)
- [ ] Firebase service account key added
- [ ] Model file (`app/data/model.h5`) present and valid
- [ ] Labels file (`app/data/labels.txt`) matches model classes
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Health endpoint returns "healthy" status

### Recommended Production Setup
```bash
# Use production WSGI server
pip install gunicorn

# Run with multiple workers and proper timeout
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 --max-requests 1000 main:create_app()
```

### Cloud Deployment Options

**Google Cloud Platform:**
```bash
# Deploy to Google Cloud Run
gcloud run deploy harvesthub-api --source . --platform managed
```

**AWS Elastic Beanstalk:**
```bash
# Create application.py for EB
echo "from main import create_app; application = create_app()" > application.py
```

**Heroku:**
```bash
# Create Procfile
echo "web: gunicorn main:create_app()" > Procfile
```

### Security Considerations
- Use environment variables for all sensitive data
- Enable HTTPS in production
- Implement rate limiting for API endpoints
- Set up monitoring and alerting
- Regular security updates for dependencies

## 🤝 Contributing

### Development Setup
```bash
# Clone and setup development environment
git clone <repository-url>
cd harvesthub-pest-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Code Standards
- Follow PEP 8 for Python code style
- Add docstrings for all functions
- Include error handling for all external API calls
- Write tests for new features
- Update documentation for API changes

### Contributing Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Ensure all tests pass (`python test_multilang_api.py`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Create a Pull Request

### Reporting Issues
- Use GitHub Issues for bug reports
- Include error logs and system information
- Provide steps to reproduce the issue
- Suggest potential solutions if possible

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TensorFlow Team** - For the machine learning framework
- **Google Gemini** - For AI-powered recommendation generation
- **Firebase** - For reliable cloud database services
- **Flask Community** - For the excellent web framework
- **Contributors** - For their valuable contributions to this project

## 📞 Support

For support and questions:
- 📧 Create an issue on GitHub
- 📚 Check the documentation and examples
- 🧪 Run the test suite to verify setup
- 💬 Review error logs for troubleshooting guidance

---

**HarvestHub Pest Detection Backend** - Empowering farmers with AI-driven, multilingual pest management solutions. 🌾🤖

*Last updated: June 2025*
