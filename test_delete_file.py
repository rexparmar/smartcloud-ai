#!/usr/bin/env python3
"""
Test script for delete file functionality
This script tests the DELETE /files/{file_id} endpoint.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}"

def test_delete_file():
    """Test the delete file functionality"""
    print("🗑️ Testing Delete File Functionality")
    print("=" * 50)
    
    # First, let's get a list of files to see what's available
    print("📋 Getting list of files...")
    
    try:
        # Note: This would require authentication in a real scenario
        # For testing, we'll assume the API is running and accessible
        response = requests.get(f"{API_BASE}/files")
        
        if response.status_code == 200:
            files = response.json()
            print(f"✅ Found {len(files)} files")
            
            if files:
                # Show available files
                print("\n📁 Available files:")
                for file in files:
                    print(f"  - ID: {file['id']}, Name: {file['filename']}, Size: {file['size']} bytes")
                
                # Test delete with the first file
                test_file = files[0]
                file_id = test_file['id']
                filename = test_file['filename']
                
                print(f"\n🗑️ Testing delete for file ID: {file_id} ({filename})")
                
                # Delete the file
                delete_response = requests.delete(f"{API_BASE}/files/{file_id}")
                
                if delete_response.status_code == 200:
                    result = delete_response.json()
                    print(f"✅ File deleted successfully!")
                    print(f"   Message: {result['message']}")
                    print(f"   File ID: {result['file_id']}")
                    print(f"   Filename: {result['filename']}")
                    
                    # Verify the file is gone
                    verify_response = requests.get(f"{API_BASE}/files")
                    if verify_response.status_code == 200:
                        remaining_files = verify_response.json()
                        remaining_ids = [f['id'] for f in remaining_files]
                        
                        if file_id not in remaining_ids:
                            print(f"✅ Verification successful: File {file_id} is no longer in the list")
                        else:
                            print(f"⚠️ Warning: File {file_id} still appears in the list")
                    else:
                        print(f"⚠️ Could not verify deletion: {verify_response.status_code}")
                        
                elif delete_response.status_code == 404:
                    print(f"❌ File not found (ID: {file_id})")
                elif delete_response.status_code == 403:
                    print(f"❌ Access denied - authentication required")
                else:
                    print(f"❌ Delete failed with status {delete_response.status_code}")
                    print(f"   Response: {delete_response.text}")
            else:
                print("ℹ️ No files available for testing")
                
        elif response.status_code == 401:
            print("❌ Authentication required to access files")
            print("   Please log in first or provide authentication token")
        else:
            print(f"❌ Failed to get files: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server")
        print("   Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

def test_delete_nonexistent_file():
    """Test deleting a file that doesn't exist"""
    print("\n🧪 Testing Delete Non-existent File")
    print("-" * 30)
    
    try:
        # Try to delete a file with a very high ID that shouldn't exist
        fake_file_id = 99999
        response = requests.delete(f"{API_BASE}/files/{fake_file_id}")
        
        if response.status_code == 404:
            print(f"✅ Correctly returned 404 for non-existent file ID: {fake_file_id}")
        else:
            print(f"⚠️ Unexpected response for non-existent file: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing non-existent file: {e}")

def test_delete_without_auth():
    """Test delete without authentication"""
    print("\n🔐 Testing Delete Without Authentication")
    print("-" * 30)
    
    try:
        # Try to delete without authentication
        response = requests.delete(f"{API_BASE}/files/1")
        
        if response.status_code == 401:
            print("✅ Correctly requires authentication")
        else:
            print(f"⚠️ Unexpected response without auth: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing without auth: {e}")

def show_api_endpoints():
    """Show available API endpoints"""
    print("\n📚 Available API Endpoints")
    print("=" * 30)
    
    endpoints = [
        ("GET", "/files", "List user files"),
        ("GET", "/files/{file_id}", "Get file details"),
        ("DELETE", "/files/{file_id}", "Delete file"),
        ("GET", "/download/{file_id}", "Download file"),
        ("POST", "/share/{file_id}", "Create share link"),
        ("GET", "/share/{token}", "Access shared file"),
        ("POST", "/files/{file_id}/process-ai", "Process file with AI"),
        ("POST", "/files/{file_id}/query", "Query file with AI"),
        ("GET", "/files/search", "Search files"),
        ("POST", "/upload", "Upload file"),
    ]
    
    for method, path, description in endpoints:
        print(f"{method:6} {path:<25} - {description}")

if __name__ == "__main__":
    print("🚀 SmartCloud Delete File Test")
    print("=" * 60)
    print()
    
    # Show available endpoints
    show_api_endpoints()
    print()
    
    # Test delete functionality
    test_delete_file()
    
    # Test edge cases
    test_delete_nonexistent_file()
    test_delete_without_auth()
    
    print("\n✅ Testing completed!")
    print("\n💡 Tips:")
    print("- Make sure the server is running: uvicorn app.main:app --reload")
    print("- Authentication is required for most operations")
    print("- Files are permanently deleted (both database and physical file)")
    print("- Shared links are automatically cleaned up when files are deleted") 