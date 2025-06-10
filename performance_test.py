#!/usr/bin/env python3
"""
Quick performance test comparing FastAPI vs Flask
"""

import requests
import time
import concurrent.futures
import statistics
import os

# URLs
FASTAPI_URL = "http://127.0.0.1:8000"
FLASK_URL = "http://127.0.0.1:5000"

def test_endpoint_performance(url, endpoint="/", num_requests=10):
    """Test endpoint performance"""
    response_times = []
    success_count = 0
    
    for i in range(num_requests):
        try:
            start_time = time.time()
            response = requests.get(f"{url}{endpoint}", timeout=30)
            end_time = time.time()
            
            if response.status_code == 200:
                response_times.append((end_time - start_time) * 1000)
                success_count += 1
            
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
    
    if response_times:
        return {
            'success_rate': success_count / num_requests,
            'avg_response_time': statistics.mean(response_times),
            'min_response_time': min(response_times),
            'max_response_time': max(response_times),
            'median_response_time': statistics.median(response_times),
            'total_requests': num_requests,
            'successful_requests': success_count
        }
    else:
        return None

def test_concurrent_requests(url, endpoint="/", num_concurrent=5, requests_per_thread=3):
    """Test concurrent request performance"""
    
    def make_request():
        try:
            start_time = time.time()
            response = requests.get(f"{url}{endpoint}", timeout=30)
            end_time = time.time()
            
            return {
                'success': response.status_code == 200,
                'response_time': (end_time - start_time) * 1000
            }
        except:
            return {'success': False, 'response_time': 0}
    
    all_results = []
    start_time = time.time()
    
    # Create thread pool and submit concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
        futures = []
        
        for _ in range(num_concurrent * requests_per_thread):
            futures.append(executor.submit(make_request))
        
        # Collect results
        for future in concurrent.futures.as_completed(futures):
            all_results.append(future.result())
    
    total_time = time.time() - start_time
    
    # Calculate statistics
    successful_results = [r for r in all_results if r['success']]
    response_times = [r['response_time'] for r in successful_results]
    
    if response_times:
        return {
            'total_time': total_time * 1000,
            'total_requests': len(all_results),
            'successful_requests': len(successful_results),
            'success_rate': len(successful_results) / len(all_results),
            'avg_response_time': statistics.mean(response_times),
            'min_response_time': min(response_times),
            'max_response_time': max(response_times),
            'requests_per_second': len(successful_results) / total_time
        }
    else:
        return None

def main():
    print("🚀 HarvestHub Performance Comparison Test")
    print("="*60)
    
    # Test if servers are running
    print("🔍 Checking server availability...")
    
    fastapi_available = False
    flask_available = False
    
    try:
        response = requests.get(f"{FASTAPI_URL}/", timeout=5)
        if response.status_code == 200:
            fastapi_available = True
            print("✅ FastAPI server is running")
    except:
        print("❌ FastAPI server is not running")
    
    try:
        response = requests.get(f"{FLASK_URL}/", timeout=5)
        if response.status_code == 200:
            flask_available = True
            print("✅ Flask server is running")
    except:
        print("❌ Flask server is not running (this is expected)")
    
    if not fastapi_available:
        print("\n❌ FastAPI server is required for testing")
        print("Start it with: python start_fastapi.py")
        return
    
    print("\n📊 Performance Testing...")
    print("-" * 60)
    
    # Test single requests
    print("\n1️⃣  Single Request Performance (10 requests)")
    print("-" * 40)
    
    fastapi_results = test_endpoint_performance(FASTAPI_URL, "/", 10)
    
    if fastapi_results:
        print(f"FastAPI Results:")
        print(f"  ✅ Success Rate: {fastapi_results['success_rate']:.1%}")
        print(f"  ⚡ Avg Response: {fastapi_results['avg_response_time']:.1f}ms")
        print(f"  📈 Min/Max: {fastapi_results['min_response_time']:.1f}ms / {fastapi_results['max_response_time']:.1f}ms")
        print(f"  📊 Median: {fastapi_results['median_response_time']:.1f}ms")
    
    if flask_available:
        flask_results = test_endpoint_performance(FLASK_URL, "/", 10)
        if flask_results:
            print(f"\nFlask Results:")
            print(f"  ✅ Success Rate: {flask_results['success_rate']:.1%}")
            print(f"  ⚡ Avg Response: {flask_results['avg_response_time']:.1f}ms")
            print(f"  📈 Min/Max: {flask_results['min_response_time']:.1f}ms / {flask_results['max_response_time']:.1f}ms")
            print(f"  📊 Median: {flask_results['median_response_time']:.1f}ms")
            
            # Performance comparison
            improvement = ((flask_results['avg_response_time'] - fastapi_results['avg_response_time']) / flask_results['avg_response_time']) * 100
            print(f"\n🏆 FastAPI is {improvement:.1f}% faster than Flask")
    
    # Test concurrent requests
    print("\n2️⃣  Concurrent Request Performance (5 threads x 3 requests)")
    print("-" * 50)
    
    fastapi_concurrent = test_concurrent_requests(FASTAPI_URL, "/", 5, 3)
    
    if fastapi_concurrent:
        print(f"FastAPI Concurrent Results:")
        print(f"  ✅ Success Rate: {fastapi_concurrent['success_rate']:.1%}")
        print(f"  ⚡ Avg Response: {fastapi_concurrent['avg_response_time']:.1f}ms")
        print(f"  🚀 Requests/sec: {fastapi_concurrent['requests_per_second']:.1f}")
        print(f"  📈 Min/Max: {fastapi_concurrent['min_response_time']:.1f}ms / {fastapi_concurrent['max_response_time']:.1f}ms")
        print(f"  ⏱️  Total Time: {fastapi_concurrent['total_time']:.1f}ms")
    
    if flask_available:
        flask_concurrent = test_concurrent_requests(FLASK_URL, "/", 5, 3)
        if flask_concurrent:
            print(f"\nFlask Concurrent Results:")
            print(f"  ✅ Success Rate: {flask_concurrent['success_rate']:.1%}")
            print(f"  ⚡ Avg Response: {flask_concurrent['avg_response_time']:.1f}ms")
            print(f"  🚀 Requests/sec: {flask_concurrent['requests_per_second']:.1f}")
            print(f"  📈 Min/Max: {flask_concurrent['min_response_time']:.1f}ms / {flask_concurrent['max_response_time']:.1f}ms")
            print(f"  ⏱️  Total Time: {flask_concurrent['total_time']:.1f}ms")
            
            # Throughput comparison
            throughput_improvement = ((fastapi_concurrent['requests_per_second'] - flask_concurrent['requests_per_second']) / flask_concurrent['requests_per_second']) * 100
            print(f"\n🏆 FastAPI handles {throughput_improvement:.1f}% more requests per second")
    
    # Test language endpoint
    print("\n3️⃣  Language Endpoint Performance")
    print("-" * 35)
    
    lang_results = test_endpoint_performance(FASTAPI_URL, "/languages", 5)
    if lang_results:
        print(f"Languages Endpoint:")
        print(f"  ✅ Success Rate: {lang_results['success_rate']:.1%}")
        print(f"  ⚡ Avg Response: {lang_results['avg_response_time']:.1f}ms")
    
    print("\n" + "="*60)
    print("🎉 Performance testing complete!")
    
    if fastapi_available and not flask_available:
        print("\n💡 To compare with Flask:")
        print("   1. Start Flask server: python main.py")
        print("   2. Run this test again")

if __name__ == "__main__":
    main()
