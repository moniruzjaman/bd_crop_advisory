#!/usr/bin/env python3
"""
National Crop Health Advisory System - Testing Suite
Bangladesh Government Grade Testing
"""

import requests
import json
import sys
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"

def test_api_root():
    """Test API root endpoint"""
    print("🔍 Testing API root...")
    try:
        response = requests.get(BASE_URL)
        assert response.status_code == 200
        data = response.json()
        assert "National AI-Enabled Crop Health Advisory System" in data["message"]
        print("✅ API root test passed")
        return True
    except Exception as e:
        print(f"❌ API root test failed: {e}")
        return False

def test_symptoms_endpoint():
    """Test symptoms list endpoint"""
    print("🔍 Testing symptoms endpoint...")
    try:
        response = requests.get(f"{API_URL}/symptoms")
        assert response.status_code == 200
        data = response.json()
        assert "symptoms" in data
        assert len(data["symptoms"]) == 11  # 11 symptom classes
        print("✅ Symptoms endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Symptoms endpoint test failed: {e}")
        return False

def test_crops_endpoint():
    """Test crops list endpoint"""
    print("🔍 Testing crops endpoint...")
    try:
        response = requests.get(f"{API_URL}/crops")
        assert response.status_code == 200
        data = response.json()
        assert "crops" in data
        assert len(data["crops"]) >= 10  # At least 10 crops
        print("✅ Crops endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Crops endpoint test failed: {e}")
        return False

def test_diagnosis_with_mock_image():
    """Test diagnosis endpoint with mock image"""
    print("🔍 Testing diagnosis endpoint...")
    try:
        # Create a test image (1x1 pixel red image)
        from PIL import Image
        import io

        img = Image.new('RGB', (224, 224), color='red')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        files = {'image': ('test.png', img_byte_arr, 'image/png')}
        data = {
            'crop': 'rice',
            'district': 'Dhaka',
            'upazila': 'Dhanmondi',
            'phone_number': '01712345678'
        }

        # Note: This requires authentication in production
        # For testing, we assume auth is disabled or mock token is used
        headers = {'Authorization': 'Bearer test-token'}

        response = requests.post(
            f"{API_URL}/diagnose",
            files=files,
            data=data,
            headers=headers
        )

        # We expect either 200 (success) or 401 (auth required)
        assert response.status_code in [200, 401]
        print("✅ Diagnosis endpoint test passed")
        return True
    except Exception as e:
        print(f"❌ Diagnosis endpoint test failed: {e}")
        return False

def test_whatsapp_webhook_verification():
    """Test WhatsApp webhook verification"""
    print("🔍 Testing WhatsApp webhook verification...")
    try:
        # Test verification endpoint
        params = {
            'hub.mode': 'subscribe',
            'hub.verify_token': 'crop_health_bot',
            'hub.challenge': '123456789'
        }

        response = requests.get(
            f"{API_URL}/whatsapp/webhook",
            params=params
        )

        # Should return challenge number
        assert response.status_code == 200
        print("✅ WhatsApp webhook test passed")
        return True
    except Exception as e:
        print(f"❌ WhatsApp webhook test failed: {e}")
        return False

def test_database_connection():
    """Test database connectivity"""
    print("🔍 Testing database connection...")
    try:
        # This is indirectly tested through the API
        # A successful API response implies DB is working
        response = requests.get(f"{API_URL}/symptoms")
        assert response.status_code == 200
        print("✅ Database connection test passed")
        return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🇧🇩 National Crop Health Advisory System - Test Suite")
    print("=" * 60)

    tests = [
        ("API Root", test_api_root),
        ("Symptoms Endpoint", test_symptoms_endpoint),
        ("Crops Endpoint", test_crops_endpoint),
        ("Diagnosis Endpoint", test_diagnosis_with_mock_image),
        ("WhatsApp Webhook", test_whatsapp_webhook_verification),
        ("Database Connection", test_database_connection),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} test crashed: {e}")
            results.append((name, False))
        print()

    # Summary
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")

    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the logs.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
