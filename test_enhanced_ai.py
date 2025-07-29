#!/usr/bin/env python3
"""
Test script for enhanced AI capabilities
This script demonstrates the multi-provider AI system with OpenAI, Hugging Face, and fallback options.
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

def test_ai_providers():
    """Test different AI providers"""
    print("🤖 Testing Enhanced AI System")
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
        from app.ai.enhanced_processor import get_enhanced_processor
        from app.ai.config import get_ai_config
        
        # Get configuration
        config = get_ai_config()
        print(f"📋 Available AI Providers: {', '.join(config.get_available_providers())}")
        print(f"🎯 Provider Priority: {' -> '.join(config.provider_priority)}")
        print()
        
        # Get enhanced processor
        processor = get_enhanced_processor()
        
        # Test 1: Generate Summary
        print("📝 Testing Document Summarization")
        print("-" * 30)
        summary_result = processor.generate_summary(sample_content)
        
        if summary_result["status"] == "success":
            print(f"✅ Summary generated successfully using {summary_result.get('model', 'unknown')}")
            print(f"📄 Summary: {summary_result['summary']}")
        else:
            print(f"❌ Summary generation failed: {summary_result.get('message', 'Unknown error')}")
        print()
        
        # Test 2: Generate Tags
        print("🏷️ Testing Document Tagging")
        print("-" * 30)
        tags_result = processor.generate_tags(sample_content)
        
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
            query_result = processor.query_file_content(sample_content, question)
            
            if query_result["status"] == "success":
                print(f"✅ Answer (using {query_result.get('model', 'unknown')}): {query_result['answer']}")
            else:
                print(f"❌ Query failed: {query_result.get('message', 'Unknown error')}")
            print()
        
        # Test 4: Complete Processing
        print("🔄 Testing Complete File Processing")
        print("-" * 30)
        complete_result = processor.process_file_complete(sample_content)
        
        if complete_result["status"] == "success":
            print(f"✅ Complete processing successful")
            print(f"📄 Summary: {complete_result['summary'][:100]}...")
            print(f"🏷️ Tags: {', '.join(complete_result['tags'])}")
            print(f"📊 Analysis: {complete_result.get('analysis', {})}")
        else:
            print(f"❌ Complete processing failed: {complete_result.get('message', 'Unknown error')}")
        print()
        
        # Test 5: Configuration Info
        print("⚙️ AI Configuration Information")
        print("-" * 30)
        model_info = config.get_model_info()
        
        print("OpenAI Settings:")
        openai_info = model_info["openai"]
        print(f"  - Enabled: {openai_info['enabled']}")
        if openai_info['enabled']:
            print(f"  - Model: {openai_info['model']}")
            print(f"  - Max Tokens: {openai_info['max_tokens']}")
            print(f"  - Temperature: {openai_info['temperature']}")
        
        print("\nHugging Face Settings:")
        hf_info = model_info["huggingface"]
        print(f"  - Enabled: {hf_info['enabled']}")
        print(f"  - API Enabled: {hf_info['api_enabled']}")
        print(f"  - Local Models: {hf_info['local_models_enabled']}")
        print(f"  - Summarization Model: {hf_info['summarization_model']}")
        print(f"  - QA Model: {hf_info['qa_model']}")
        print(f"  - Device: {hf_info['device']}")
        
        print("\nProcessing Settings:")
        proc_info = model_info["processing"]
        print(f"  - Max Content Length: {proc_info['max_content_length']}")
        print(f"  - Max Summary Length: {proc_info['max_summary_length']}")
        print(f"  - Max Tags Count: {proc_info['max_tags_count']}")
        
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
        "USE_LOCAL_MODELS": os.getenv("USE_LOCAL_MODELS", "true")
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
    
    print("  - Local models will be used by default (free)")
    print("  - Rule-based fallback is always available")

if __name__ == "__main__":
    print("🚀 SmartCloud AI Enhanced System Test")
    print("=" * 60)
    print()
    
    # Test environment setup
    test_environment_setup()
    print()
    
    # Test AI providers
    test_ai_providers()
    
    print("✅ Testing completed!")
    print("\n💡 Tips:")
    print("- Set OPENAI_API_KEY for best AI performance")
    print("- Set HUGGINGFACE_API_KEY for free AI alternatives")
    print("- Local models work offline but require more memory")
    print("- The system automatically falls back to rule-based processing") 