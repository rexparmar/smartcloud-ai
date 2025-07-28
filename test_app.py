#!/usr/bin/env python3
"""
Simple test script to verify the application works
"""
import requests
import json
import os

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_FILE_PATH = "test_file.txt"

def create_test_file():
    """Create a test file for upload"""
    with open(TEST_FILE_PATH, "w") as f:
        f.write("This is a test invoice report for work purposes.")
    print(f"✅ Created test file: {TEST_FILE_PATH}")

def test_health_check():
    """Test if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Server is running and accessible")
            return True
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 8000")
        return False

def test_upload_without_auth():
    """Test upload without authentication (should fail)"""
    try:
        with open(TEST_FILE_PATH, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        if response.status_code == 401:
            print("✅ Upload correctly requires authentication")
            return True
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing upload: {e}")
        return False

def cleanup():
    """Clean up test files"""
    if os.path.exists(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)
        print(f"✅ Cleaned up test file: {TEST_FILE_PATH}")

def main():
    print("🧪 Testing SmartCloud AI Application")
    print("=" * 40)
    
    # Test 1: Health check
    if not test_health_check():
        print("❌ Health check failed. Please start the server first.")
        return
    
    # Test 2: Upload without auth
    test_upload_without_auth()
    
    # Cleanup
    cleanup()
    
    print("\n✅ Basic tests completed!")
    print("📝 To test with authentication, you'll need to:")
    print("   1. Create a user account via /signup")
    print("   2. Login via /login to get a token")
    print("   3. Use the token in the Authorization header")

if __name__ == "__main__":
    create_test_file()
    main() 