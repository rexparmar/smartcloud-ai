#!/usr/bin/env python3
"""
Test the file querying feature
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_file_query():
    """Test the file querying feature"""
    
    # Test with our document
    test_file_path = "uploaded_files/1/test_document.txt"
    
    if os.path.exists(test_file_path):
        print("🤖 Testing File Query Feature...")
        
        # Test different types of queries
        test_queries = [
            "What is this document about?",
            "What are the main achievements mentioned?",
            "What features or capabilities are described?",
            "What is the current status of the project?",
            "What are the next steps?",
            "What team information is available?",
            "What budget information is mentioned?",
            "Summarize this document for me"
        ]
        
        from app.ai.query import query_file_with_ai
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Query {i}: {query}")
            print("-" * 60)
            
            result = query_file_with_ai(test_file_path, query)
            
            if result["status"] == "success":
                print(f"✅ AI Answer: {result['answer']}")
            else:
                print(f"❌ Error: {result['message']}")
            
            print("-" * 60)
        
        print("\n🎉 File querying test completed!")
        
    else:
        print(f"Test file not found: {test_file_path}")

if __name__ == "__main__":
    test_file_query() 