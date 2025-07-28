#!/usr/bin/env python3
"""
Test the full AI tagging system
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_full_ai_system():
    """Test the complete AI tagging system"""
    
    # Test with a sample text file
    test_file_path = "uploaded_files/1/test_document.txt"
    
    if os.path.exists(test_file_path):
        print(f"🧪 Testing full AI system with file: {test_file_path}")
        
        try:
            from app.ai.tagging import process_file_with_ai
            
            print("📥 Processing file with AI...")
            result = process_file_with_ai(test_file_path)
            
            if result["status"] == "success":
                print("✅ AI processing successful!")
                print(f"🏷️ Tags: {result['tags']}")
                print(f"📝 Summary: {result['summary']}")
                
                # Test database integration
                from app.tasks.file_tasks import update_file_metadata_with_ai
                from app.database import SessionLocal
                from app.model.file import FileMeta
                
                db = SessionLocal()
                file_metadata = db.query(FileMeta).filter(FileMeta.file_path == test_file_path).first()
                
                if file_metadata:
                    print(f"📊 Found file in database: {file_metadata.file_name}")
                    print(f"🔄 Updating database with AI results...")
                    
                    db_result = update_file_metadata_with_ai(file_metadata.id, test_file_path)
                    
                    if db_result["status"] == "success":
                        print("✅ Database update successful!")
                        print(f"🏷️ Database tags: {db_result['tags']}")
                        print(f"📝 Database summary: {db_result['summary']}")
                    else:
                        print(f"❌ Database update failed: {db_result}")
                else:
                    print("⚠️ File not found in database")
                
                db.close()
                
            else:
                print(f"❌ AI processing failed: {result}")
                
        except Exception as e:
            print(f"❌ Error testing AI system: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"Test file not found: {test_file_path}")
        print("Please upload a file first to test the AI system")

if __name__ == "__main__":
    test_full_ai_system() 