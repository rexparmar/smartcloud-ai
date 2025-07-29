#!/usr/bin/env python3
"""
Simple test script for AI capabilities without heavy dependencies
This script tests the basic AI functionality without requiring transformers/torch.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_simple_ai():
    """Test simple AI functionality"""
    print("🤖 Testing Simple AI System")
    print("=" * 50)
    
    # Sample document content
    sample_content = """
    SmartCloud AI Platform - Technical Documentation
    
    The SmartCloud AI Platform is a comprehensive document management and AI analysis system designed to help users organize, analyze, and extract insights from their files. The platform combines advanced AI capabilities with intuitive user interfaces to provide powerful document processing features.
    
    Key Features:
    - Intelligent file tagging and categorization
    - AI-powered document summarization
    - Natural language querying of document content
    - Multi-format file support (PDF, DOCX, TXT, etc.)
    - Secure file storage and sharing capabilities
    - Real-time AI processing with background tasks
    
    Technical Architecture:
    The system is built using FastAPI for the backend API, SQLAlchemy for database management, and Celery for background task processing. The AI components utilize multiple providers including OpenAI GPT models, Hugging Face transformers, and local rule-based fallbacks for maximum reliability.
    
    Current Status:
    The platform is currently in active development with core features implemented and tested. The AI processing pipeline supports multiple providers with automatic fallback mechanisms to ensure consistent service availability.
    
    Future Plans:
    Planned enhancements include advanced document comparison, collaborative editing features, and expanded AI model support. The team is also working on performance optimizations and additional file format support.
    """
    
    try:
        # Import AI components
        from app.ai.simple_ai_client import get_simple_ai_client
        from app.ai.openai_client import get_openai_client
        
        # Test Simple AI Client
        print("📝 Testing Simple AI Client")
        print("-" * 30)
        
        simple_client = get_simple_ai_client()
        
        # Test 1: Generate Summary
        print("📄 Testing Document Summarization")
        summary_result = simple_client.generate_summary(sample_content)
        
        if summary_result["status"] == "success":
            print(f"✅ Summary generated successfully using {summary_result.get('model', 'unknown')}")
            print(f"📄 Summary: {summary_result['summary']}")
        else:
            print(f"❌ Summary generation failed: {summary_result.get('message', 'Unknown error')}")
        print()
        
        # Test 2: Generate Tags
        print("🏷️ Testing Document Tagging")
        tags_result = simple_client.generate_tags(sample_content)
        
        if tags_result["status"] == "success":
            print(f"✅ Tags generated successfully using {tags_result.get('model', 'unknown')}")
            print(f"🏷️ Tags: {', '.join(tags_result['tags'])}")
        else:
            print(f"❌ Tag generation failed: {tags_result.get('message', 'Unknown error')}")
        print()
        
        # Test 3: Query Document
        print("❓ Testing Document Querying")
        print("-" * 30)
        
        test_questions = [
            "What are the key features of this platform?",
            "What is the current status of the project?",
            "What are the future plans mentioned?",
            "What technologies are used in this system?"
        ]
        
        for question in test_questions:
            print(f"🤔 Question: {question}")
            query_result = simple_client.query_file_content(sample_content, question)
            
            if query_result["status"] == "success":
                print(f"✅ Answer (using {query_result.get('model', 'unknown')}): {query_result['answer']}")
            else:
                print(f"❌ Query failed: {query_result.get('message', 'Unknown error')}")
            print()
        
        # Test OpenAI Client (if available)
        print("🔍 Testing OpenAI Client")
        print("-" * 30)
        
        openai_client = get_openai_client()
        if openai_client.is_available():
            print("✅ OpenAI API is configured")
            
            # Test OpenAI summary
            openai_summary = openai_client.generate_summary(sample_content)
            if openai_summary["status"] == "success":
                print(f"✅ OpenAI summary: {openai_summary['summary'][:100]}...")
            else:
                print(f"❌ OpenAI summary failed: {openai_summary.get('message', 'Unknown error')}")
        else:
            print("⚠️ OpenAI API not configured (set OPENAI_API_KEY environment variable)")
        
        print()
        
        # Test 4: Enhanced Processor
        print("🔄 Testing Enhanced Processor")
        print("-" * 30)
        
        try:
            from app.ai.enhanced_processor import get_enhanced_processor
            
            processor = get_enhanced_processor()
            
            # Test complete processing
            complete_result = processor.process_file_complete(sample_content)
            
            if complete_result["status"] == "success":
                print(f"✅ Complete processing successful")
                print(f"📄 Summary: {complete_result['summary'][:100]}...")
                print(f"🏷️ Tags: {', '.join(complete_result['tags'])}")
                print(f"📊 Analysis: {complete_result.get('analysis', {})}")
            else:
                print(f"❌ Complete processing failed: {complete_result.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Enhanced processor test failed: {e}")
        
        print()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the project root directory")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        logger.error(f"Test error: {e}")

def test_environment_setup():
    """Test environment setup and API keys"""
    print("🔧 Environment Setup Check")
    print("=" * 50)
    
    # Check environment variables
    env_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "HUGGINGFACE_API_KEY": os.getenv("HUGGINGFACE_API_KEY"),
    }
    
    print("Environment Variables:")
    for var, value in env_vars.items():
        if value:
            print(f"  ✅ {var}: {'*' * 10} (set)")
        else:
            print(f"  ❌ {var}: Not set")
    
    print("\nRecommendations:")
    if not env_vars["OPENAI_API_KEY"]:
        print("  - Set OPENAI_API_KEY for GPT-3.5/4 access (paid)")
    
    if not env_vars["HUGGINGFACE_API_KEY"]:
        print("  - Set HUGGINGFACE_API_KEY for free API access")
    
    print("  - Simple AI client works without any API keys")
    print("  - Rule-based fallback is always available")

if __name__ == "__main__":
    print("🚀 SmartCloud Simple AI System Test")
    print("=" * 60)
    print()
    
    # Test environment setup
    test_environment_setup()
    print()
    
    # Test AI functionality
    test_simple_ai()
    
    print("✅ Testing completed!")
    print("\n💡 Tips:")
    print("- Simple AI client works without heavy dependencies")
    print("- Set OPENAI_API_KEY for best AI performance")
    print("- Set HUGGINGFACE_API_KEY for free AI alternatives")
    print("- The system automatically falls back to rule-based processing") 