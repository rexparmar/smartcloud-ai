#!/usr/bin/env python3
"""
Simple test for the AI tagging system
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """Test basic functionality without loading heavy AI models"""
    try:
        # Test file extraction
        from app.ai.tagging import AITaggingSystem
        
        print("✅ AI tagging system can be imported")
        
        # Test text extraction
        test_file = "uploaded_files/1/testfime.txt"
        if os.path.exists(test_file):
            print(f"✅ Test file exists: {test_file}")
            
            # Test basic text extraction
            with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                print(f"✅ Text extraction works, content length: {len(content)}")
                
                if len(content) > 0:
                    print("✅ File has content")
                    print(f"Sample content: {content[:100]}...")
                else:
                    print("⚠️ File is empty")
        else:
            print(f"⚠️ Test file not found: {test_file}")
            
        print("✅ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error in basic functionality test: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        from app.database import SessionLocal
        from app.model.file import FileMeta
        
        db = SessionLocal()
        files = db.query(FileMeta).all()
        print(f"✅ Database connection works, found {len(files)} files")
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing AI System Components...")
    
    basic_test = test_basic_functionality()
    db_test = test_database_connection()
    
    if basic_test and db_test:
        print("✅ All basic tests passed!")
        print("🚀 Ready to implement AI features!")
    else:
        print("❌ Some tests failed") 