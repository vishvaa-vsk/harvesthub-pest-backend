#!/usr/bin/env python3
"""
FastAPI Test script for the HarvestHub Pest Detection API
Tests all endpoints and compares performance with Flask version
"""

import requests
import json
import os
import time
import asyncio
import aiohttp
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# API base URLs
FASTAPI_URL = "http://127.0.0.1:8000"
FLASK_URL = "http://127.0.0.1:5000"

def test_health_endpoints():
    """Test health endpoints"""
    print("🔍 Testing FastAPI health endpoints...")
    
    # Test main health endpoint
    try:
        start_time = time.time()
        response = requests.get(f"{FASTAPI_URL}/")
        response_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Main endpoint: {data['message']} ({response_time:.1f}ms)")
            print(f"   Version: {data['version']}")
            print(f"   Features: {', '.join(data['features'])}")
        else:
            print(f"❌ Main endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Main endpoint error: {e}")
    
    # Test detailed health endpoint
    try:
        start_time = time.time()
        response = requests.get(f"{FASTAPI_URL}/health")
        response_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            data = response.json()
            health = data['health']
            print(f"✅ Health endpoint: Model loaded: {health['model_loaded']}, Classes: {health['total_classes']} ({response_time:.1f}ms)")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")

def test_languages_endpoint():
    """Test supported languages endpoint"""
    print("\n🌐 Testing languages endpoint...")
    
    try:
        start_time = time.time()
        response = requests.get(f"{FASTAPI_URL}/languages")
        response_time = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            data = response.json()
            languages = data['supported_languages']
            print(f"✅ Languages endpoint: {data['total_languages']} languages supported ({response_time:.1f}ms)")
            print("   Supported languages:")
            for code, name in list(languages.items())[:5]:  # Show first 5
                print(f"     {code}: {name}")
            if len(languages) > 5:
                print(f"     ... and {len(languages) - 5} more")
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
            start_time = time.time()
            with open(test_image_path, 'rb') as img_file:
                files = {'file': img_file}
                response = requests.post(f"{FASTAPI_URL}/predict/{lang}", files=files)
            response_time = (time.time() - start_time) * 1000
                
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Prediction successful for {lang} ({response_time:.1f}ms)")
                print(f"   Predicted: {data['prediction']['label']} (confidence: {data['prediction']['confidence']:.3f})")
                print(f"   Language: {data['language']['name']}")
                print(f"   Source: {data['source']}")
                print(f"   Diagnosis: {data['recommendation']['diagnosis'][:100]}...")
                print(f"   Treatments: {len(data['recommendation']['treatments'])} recommendations")
            else:
                print(f"❌ Prediction failed for {lang}: {response.status_code}")
                if response.text:
                    try:
                        error_data = response.json()
                        print(f"   Error: {error_data.get('message', 'Unknown error')}")
                    except:
                        print(f"   Error: {response.text}")
                    
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
        response = requests.post(f"{FASTAPI_URL}/predict/xx", files=files)
        if response.status_code == 400:
            print("✅ Unsupported language correctly rejected")
        else:
            print(f"❌ Expected 400 for unsupported language, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing unsupported language: {e}")
    
    # Test missing file
    try:
        response = requests.post(f"{FASTAPI_URL}/predict/en")
        if response.status_code == 422:  # FastAPI returns 422 for validation errors
            print("✅ Missing file correctly rejected")
        else:
            print(f"❌ Expected 422 for missing file, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing missing file: {e}")

async def test_concurrent_requests():
    """Test concurrent request handling"""
    print("\n⚡ Testing concurrent request performance...")
    
    test_image_path = create_test_image()
    if not test_image_path:
        print("❌ Could not create test image, skipping concurrent tests")
        return
    
    async def make_request(session, url, lang):
        """Make a single async request"""
        try:
            with open(test_image_path, 'rb') as img_file:
                data = aiohttp.FormData()
                data.add_field('file', img_file, filename='test.jpg', content_type='image/jpeg')
                
                start_time = time.time()
                async with session.post(f"{url}/predict/{lang}", data=data) as response:
                    response_time = (time.time() - start_time) * 1000
                    if response.status == 200:
                        return response_time, True, lang
                    else:
                        return response_time, False, lang
        except Exception as e:
            return None, False, f"Error: {e}"
    
    # Test FastAPI concurrent performance
    try:
        async with aiohttp.ClientSession() as session:
            tasks = [
                make_request(session, FASTAPI_URL, 'en') for _ in range(5)
            ]
            
            start_time = time.time()
            results = await asyncio.gather(*tasks)
            total_time = (time.time() - start_time) * 1000
            
            successful = [r for r in results if r[1]]
            print(f"✅ FastAPI Concurrent: {len(successful)}/5 requests successful")
            print(f"   Total time: {total_time:.1f}ms")
            print(f"   Average per request: {sum(r[0] for r in successful) / len(successful):.1f}ms")
            
    except Exception as e:
        print(f"❌ Concurrent test error: {e}")
    
    # Clean up
    if os.path.exists(test_image_path):
        os.remove(test_image_path)

def test_documentation():
    """Test automatic documentation endpoints"""
    print("\n📚 Testing documentation endpoints...")
    
    endpoints = ["/docs", "/redoc", "/openapi.json"]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{FASTAPI_URL}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {endpoint}: Available")
            else:
                print(f"❌ {endpoint}: Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")

def create_test_image():
    """Create a small test image for API testing"""
    try:
        from PIL import Image
        import numpy as np
        
        # Create a simple test image
        image_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        image = Image.fromarray(image_array)
        
        test_image_path = "test_image_fastapi.jpg"
        image.save(test_image_path, "JPEG")
        
        print(f"✅ Created test image: {test_image_path}")
        return test_image_path
        
    except Exception as e:
        print(f"❌ Could not create test image: {e}")
        return None

def performance_comparison():
    """Compare FastAPI vs Flask performance"""
    print("\n🏁 Performance Comparison (FastAPI vs Flask)")
    print("="*60)
    
    test_image_path = create_test_image()
    if not test_image_path:
        print("❌ Could not create test image for comparison")
        return
    
    def test_endpoint(url, name):
        """Test an endpoint and return response time"""
        try:
            with open(test_image_path, 'rb') as img_file:
                files = {'file': img_file}
                start_time = time.time()
                response = requests.post(f"{url}/predict/en", files=files)
                response_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    return response_time, True
                else:
                    return response_time, False
        except Exception as e:
            print(f"❌ {name} test failed: {e}")
            return None, False
    
    # Test both endpoints
    fastapi_time, fastapi_success = test_endpoint(FASTAPI_URL, "FastAPI")
    flask_time, flask_success = test_endpoint(FLASK_URL, "Flask")
    
    if fastapi_success and flask_success:
        improvement = ((flask_time - fastapi_time) / flask_time) * 100
        print(f"FastAPI: {fastapi_time:.1f}ms")
        print(f"Flask:   {flask_time:.1f}ms")
        print(f"Improvement: {improvement:.1f}% faster" if improvement > 0 else f"Slower by: {abs(improvement):.1f}%")
    elif fastapi_success:
        print(f"FastAPI: {fastapi_time:.1f}ms ✅")
        print("Flask: Not available ❌")
    elif flask_success:
        print("FastAPI: Not available ❌")
        print(f"Flask: {flask_time:.1f}ms ✅")
    else:
        print("Both endpoints failed ❌")
    
    # Clean up
    if os.path.exists(test_image_path):
        os.remove(test_image_path)

async def main():
    """Run all tests"""
    print("🚀 Testing HarvestHub FastAPI Migration\n")
    print(f"FastAPI URL: {FASTAPI_URL}")
    print(f"Flask URL: {FLASK_URL}")
    print("="*60)
    
    # Sequential tests
    test_health_endpoints()
    test_languages_endpoint() 
    test_prediction_api()
    test_error_handling()
    test_documentation()
    
    # Async tests
    await test_concurrent_requests()
    
    # Performance comparison
    performance_comparison()
    
    print("\n" + "="*60)
    print("✅ FastAPI testing completed!")
    print("\n📝 FastAPI Migration Benefits:")
    print("1. ✅ Async/await support for better concurrency")
    print("2. ✅ Automatic API documentation (/docs, /redoc)")
    print("3. ✅ Built-in request/response validation")
    print("4. ✅ Better error handling and status codes")
    print("5. ✅ Type hints and Pydantic models")
    print("6. ✅ Modern Python async architecture")
    
    print("\n🚀 To start FastAPI server:")
    print("uvicorn main_fastapi:app --host 0.0.0.0 --port 8000 --reload")

if __name__ == "__main__":
    asyncio.run(main())
