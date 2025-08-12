#!/usr/bin/env python3

import requests
import time
import sys

def test_url(url, description):
    """URL 테스트"""
    print(f"Testing {description}...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✓ {description}: OK ({response.status_code})")
            return True
        else:
            print(f"✗ {description}: Failed ({response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ {description}: Connection failed ({str(e)[:50]}...)")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_deployment.py <backend-url> [frontend-url]")
        print("Example: python test_deployment.py https://erpnext-ai-backend.railway.app")
        return
    
    backend_url = sys.argv[1]
    frontend_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("=" * 60)
    print("ERPNext AI System - Deployment Test")
    print("=" * 60)
    
    # Backend tests
    print("\n[BACKEND TESTS]")
    backend_tests = [
        (f"{backend_url}/api/health", "Health Check"),
        (f"{backend_url}/docs", "API Documentation"),
        (f"{backend_url}/api/system/info", "System Info"),
    ]
    
    backend_ok = 0
    for url, desc in backend_tests:
        if test_url(url, desc):
            backend_ok += 1
        time.sleep(1)
    
    # Frontend tests
    if frontend_url:
        print("\n[FRONTEND TESTS]")
        frontend_tests = [
            (frontend_url, "Main Page"),
            (f"{frontend_url}/favicon.ico", "Favicon"),
        ]
        
        frontend_ok = 0
        for url, desc in frontend_tests:
            if test_url(url, desc):
                frontend_ok += 1
            time.sleep(1)
        
        print(f"\nFrontend: {frontend_ok}/{len(frontend_tests)} tests passed")
    
    print(f"\nBackend: {backend_ok}/{len(backend_tests)} tests passed")
    
    if backend_ok == len(backend_tests):
        print("🎉 Backend deployment successful!")
    else:
        print("❌ Backend deployment has issues")
    
    print("=" * 60)

if __name__ == "__main__":
    main()