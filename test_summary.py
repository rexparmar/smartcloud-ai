#!/usr/bin/env python3
"""
Test the improved summarization
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_summarization():
    """Test the improved summarization"""
    
    # Test with our document
    test_file_path = "uploaded_files/1/test_document.txt"
    
    if os.path.exists(test_file_path):
        print("📄 Testing improved summarization...")
        
        # Read the file content
        with open(test_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📝 Original content length: {len(content)} characters")
        print("📄 Original content:")
        print("-" * 50)
        print(content[:500] + "..." if len(content) > 500 else content)
        print("-" * 50)
        
        # Test the summarization
        from app.ai.tagging import get_ai_tagger
        
        tagger = get_ai_tagger()
        tags, summary = tagger.process_file(test_file_path)
        
        print(f"\n🏷️ Generated tags: {tags}")
        print(f"\n📝 Generated summary:")
        print("-" * 50)
        print(summary)
        print("-" * 50)
        print(f"📊 Summary length: {len(summary)} characters")
        
        # Show improvement
        original_length = len(content)
        summary_length = len(summary)
        compression_ratio = (1 - summary_length / original_length) * 100
        
        print(f"\n📈 Summary compression: {compression_ratio:.1f}% reduction")
        
    else:
        print(f"Test file not found: {test_file_path}")

if __name__ == "__main__":
    test_summarization() 