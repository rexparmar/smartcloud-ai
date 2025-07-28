#!/usr/bin/env python3
"""
Test script for the AI tagging system
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ai.tagging import process_file_with_ai

def test_ai_system():
    """Test the AI tagging system with sample files"""
    
    # Test with a sample text file
    test_file_path = "uploaded_files/1/testfime.txt"
    
    if os.path.exists(test_file_path):
        print(f"Testing AI system with file: {test_file_path}")
        
        try:
            result = process_file_with_ai(test_file_path)
            
            if result["status"] == "success":
                print("✅ AI processing successful!")
                print(f"Tags: {result['tags']}")
                print(f"Summary: {result['summary']}")
            else:
                print(f"❌ AI processing failed: {result}")
                
        except Exception as e:
            print(f"❌ Error testing AI system: {e}")
    else:
        print(f"Test file not found: {test_file_path}")
        print("Please upload a file first to test the AI system")

if __name__ == "__main__":
    test_ai_system() 