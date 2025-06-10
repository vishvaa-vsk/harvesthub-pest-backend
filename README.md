# HarvestHub Pest Detection API

A high-performance FastAPI-based intelligent crop pest detection system using TensorFlow/Keras image classification with **multi-language AI-powered recommendations**. Built with modern async architecture and supporting 12 Indian languages for comprehensive agricultural support.

## 🌟 Key Features

- 🔬 **AI-Powered Detection**: TensorFlow/Keras model for 66 pest/disease classes
- 🌐 **Multi-Language Support**: 12 Indian languages with native script support
- 🤖 **Dynamic AI Recommendations**: Google Gemini AI integration for expert-level agricultural advice
- 📸 **Smart Image Processing**: Automatic preprocessing and normalization
- ⚡ **High-Performance Async**: FastAPI with async/await for superior performance
- 🛡️ **Production Ready**: Comprehensive error handling and middleware
- 📚 **Interactive Documentation**: Automatic Swagger UI and ReDoc generation
- 🚀 **Modern Architecture**: Type-safe APIs with Pydantic validation

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

## 🏗️ Modern FastAPI Architecture

Built with industry best practices and modern Python standards:

- **Async/Await**: Non-blocking I/O for maximum performance
- **Type Safety**: Comprehensive type hints with Pydantic models
- **Dependency Injection**: Clean, testable code architecture
- **Layered Design**: Separation of concerns across API, service, and core layers
- **Automatic Documentation**: Interactive Swagger UI and ReDoc
- **Request Validation**: Automatic request/response validation
- **Error Handling**: Structured error responses with proper HTTP status codes

## 📁 Project Structure

```
harvesthub-pest-backend/
├── main.py                        # FastAPI application entry point
├── start_fastapi.py               # Production server startup script
├── deploy.py                      # Deployment management utilities
├── requirements.txt               # Python dependencies
├── performance_test.py            # Performance testing suite
├── .env                           # Environment variables
├── README.md                      # Project documentation
│
├── app/                           # Main application package
│   ├── __init__.py               # Package initialization
│   ├── helpers_async.py          # Async helper functions
│   ├── model.py                  # Legacy model wrapper
│   │
│   ├── core/                     # Core application modules
│   │   ├── __init__.py
│   │   ├── config.py             # Pydantic settings configuration
│   │   ├── constants.py          # Application constants
│   │   ├── exceptions.py         # Custom exceptions and handlers
│   │   ├── middleware.py         # Custom middleware
│   │   └── security.py           # Security utilities
│   │
│   ├── api/                      # API layer
│   │   ├── __init__.py
│   │   ├── dependencies.py       # Dependency injection
│   │   └── routes/               # API route modules
│   │       ├── __init__.py
│   │       ├── health.py         # Health check endpoints
│   │       ├── prediction.py     # Prediction endpoints
│   │       ├── languages.py      # Language endpoints
│   │       └── docs.py           # Documentation endpoints
│   │
│   ├── schemas/                  # Pydantic models
│   │   ├── __init__.py
│   │   ├── prediction.py         # Prediction-related schemas
│   │   ├── responses.py          # API response schemas
│   │   └── requests.py           # API request schemas
│   │
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── model_service.py      # ML model service
│   │   └── recommendation_service.py  # Recommendation service
│   │
│   ├── data/                     # Model and data files
│   │   ├── model.h5              # TensorFlow model file (66 classes)
│   │   └── labels.txt            # Class labels
│   │
│   └── firebase-key.json         # Firebase service account key
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

Create a `.env` file in the root directory:

```bash
# Required: Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Server Configuration
PORT=8000
WORKERS=4
LOG_LEVEL=info
RELOAD=false

# Application Settings
ENVIRONMENT=production
DEBUG=false
```

### 3. Firebase Setup (Optional but Recommended)

1. Create a Firebase project at https://console.firebase.google.com
2. Enable Firestore Database
3. Generate a service account key
4. Save it as `app/firebase-key.json`

### 4. Add Your Model

- Place your trained TensorFlow model as `app/data/model.h5`
- Update `app/data/labels.txt` with your class labels (one per line)
- Ensure your model expects 224x224x3 input images

### 5. Run the Application

```bash
# Development mode with auto-reload
python main.py

# Production mode using the startup script
python start_fastapi.py

# Using deployment script for different environments
python deploy.py dev    # Development with reload
python deploy.py prod   # Production with optimizations
python deploy.py test   # Testing mode

# The API will be available at http://localhost:8000
# Interactive documentation at http://localhost:8000/docs
```

## 🌐 API Endpoints

### Interactive Documentation
```http
GET /docs           # Swagger UI - Interactive API documentation
GET /redoc          # ReDoc - Alternative documentation view
GET /openapi.json   # OpenAPI specification
```

### Health & Status
```http
GET /               # Main health check
GET /health         # Detailed health information  
GET /status         # Quick status check
```

### Core Functionality
```http
GET /languages      # Get supported languages
POST /predict/{lang} # Language-specific prediction
POST /predict       # Default prediction (English)
```

### Health Check Response
```json
{
  "status": "success",
  "message": "HarvestHub Pest Detection API is running",
  "version": "3.0.0",
  "features": [
    "Multi-language pest detection",
    "AI-powered recommendations",
    "Firebase caching",
    "12 Indian languages supported",
    "Async FastAPI architecture"
  ]
}
```

### Detailed Health Check Response
```json
{
  "status": "success", 
  "health": {
    "model_loaded": true,
    "labels_loaded": true,
    "total_classes": 66,
    "framework": "FastAPI",
    "version": "3.0.0",
    "environment": "development",
    "supported_languages": 12
  }
}
```

### Get Supported Languages Response
```json
{
  "status": "success",
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
  "total_languages": 12
}
```

### Multi-Language Prediction
```http
POST /predict/{lang}
```
Upload an image for pest detection with recommendations in the specified language.

**Parameters:**
- `{lang}`: Language code (en, hi, ta, te, kn, ml, mr, gu, bn, pa, or, as)

**Request:**
- `Content-Type: multipart/form-data`
- `file`: Image file (PNG, JPG, JPEG, GIF, BMP)

**Response Schema:**
```json
{
  "status": "success",
  "prediction": {
    "label": "string",
    "confidence": 0.95,
    "index": 42,
    "timestamp": "2025-06-10T19:30:00"
  },
  "recommendation": {
    "diagnosis": "string",
    "causal_agent": "string", 
    "treatments": ["string"]
  },
  "language": {
    "code": "ta",
    "name": "Tamil"
  },
  "source": "firebase|gemini|fallback",
  "timestamp": "2025-06-10T19:30:00"
}
```

**Example Response (Tamil):**
```json
{
  "status": "success",
  "prediction": {
    "label": "Tomato___Early_blight",
    "confidence": 0.95,
    "index": 42,
    "timestamp": "2025-06-10T19:30:00"
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
  "language": {
    "code": "ta", 
    "name": "Tamil"
  },
  "source": "firebase",
  "timestamp": "2025-06-10T19:30:00"
}
```

## 💡 Usage Examples

### Test API with cURL
```bash
# Check API health
curl http://localhost:8000/health

# Get supported languages
curl http://localhost:8000/languages

# Upload image for English prediction
curl -X POST -F "file=@test_image.jpg" http://localhost:8000/predict/en

# Upload image for Tamil prediction  
curl -X POST -F "file=@test_image.jpg" http://localhost:8000/predict/ta
```

### Python Example
```python
import requests

# Health check
response = requests.get('http://localhost:8000/health')
print(response.json())

# Multi-language prediction
with open('plant_image.jpg', 'rb') as img:
    files = {'file': img}
    response = requests.post('http://localhost:8000/predict/ta', files=files)
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
# Server runs at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Production Mode (Recommended)
```bash
# Use the provided production script
python start_fastapi.py

# Or use uvicorn directly
pip install uvicorn[standard]
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Or use gunicorn with uvicorn workers
pip install gunicorn uvicorn[standard]
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
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

### Response Times (FastAPI Async)
- **Health Check**: ~5-10ms
- **Cached Predictions**: ~50-100ms (Firebase retrieval with async)
- **New Predictions**: ~1-2 seconds (first-time Gemini generation)
- **Model Inference**: ~30-50ms (TensorFlow processing with async)
- **Concurrent Requests**: 150+ requests/second

### Optimization Features
- **Async Architecture**: Non-blocking I/O operations
- **Smart Caching**: Reduces repeated API calls
- **Concurrent Processing**: Multiple requests handled simultaneously
- **Error Recovery**: Graceful fallback mechanisms
- **Memory Efficient**: Model loaded once at startup
- **Auto Documentation**: Built-in Swagger UI and ReDoc

## 🧪 Testing

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
curl -X POST -F "file=@sample_plant.jpg" http://localhost:8000/predict/en

# Test error handling
curl -X POST http://localhost:8000/predict/invalid_lang

# Test health checks
curl http://localhost:8000/health
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
## 🌐 Deployment
### Cloud Deployment Options

**Google Cloud Platform:**
```bash
# Deploy to Google Cloud Run
gcloud run deploy harvesthub-api --source . --platform managed
```

**AWS Elastic Beanstalk:**
```bash
# Create application.py for EB (FastAPI)
echo "from main import app as application" > application.py
```

**Heroku:**
```bash
# Create Procfile for FastAPI
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile
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
4. Ensure all tests pass (`python test_fastapi.py`)
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

- **FastAPI Team** - For the modern, high-performance web framework
- **TensorFlow Team** - For the machine learning framework
- **Google Gemini** - For AI-powered recommendation generation
- **Firebase** - For reliable cloud database services
- **Uvicorn & Starlette** - For the excellent ASGI server and foundation
- **Pydantic** - For data validation and settings management
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
