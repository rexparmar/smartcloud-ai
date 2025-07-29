# Enhanced AI System Setup Guide

This guide explains how to set up and configure the enhanced AI system for SmartCloud with multiple AI providers including OpenAI, Hugging Face, and local models.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# OpenAI Configuration (Optional - for best AI performance)
OPENAI_API_KEY=your_openai_api_key_here

# Hugging Face Configuration (Optional - for free AI alternatives)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Local Model Configuration
USE_LOCAL_MODELS=true
LOCAL_MODEL_DEVICE=auto  # auto, cpu, cuda

# Processing Configuration
MAX_CONTENT_LENGTH=4000
MAX_SUMMARY_LENGTH=200
MAX_TAGS_COUNT=5
```

### 3. Test the AI System

```bash
# Test without heavy dependencies
python test_simple_ai.py

# Test with full AI capabilities (requires transformers/torch)
python test_enhanced_ai.py
```

## 🤖 AI Providers

The system supports multiple AI providers with automatic fallback:

### 1. OpenAI (Recommended - Best Performance)
- **Cost**: Paid service
- **Performance**: Excellent
- **Setup**: Requires OpenAI API key
- **Models**: GPT-3.5-turbo, GPT-4

**Setup:**
```bash
export OPENAI_API_KEY="your_api_key_here"
```

### 2. Simple AI Client (Free Alternative)
- **Cost**: Free
- **Performance**: Good
- **Setup**: No setup required
- **Features**: Rule-based analysis + optional Hugging Face API

**Setup:**
```bash
export HUGGINGFACE_API_KEY="your_api_key_here"  # Optional
```

### 3. Rule-based Fallback (Always Available)
- **Cost**: Free
- **Performance**: Basic but reliable
- **Setup**: No setup required
- **Features**: Keyword-based analysis

## 📋 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | None | OpenAI API key for GPT models |
| `HUGGINGFACE_API_KEY` | None | Hugging Face API key (optional) |
| `USE_LOCAL_MODELS` | true | Enable local model processing |
| `LOCAL_MODEL_DEVICE` | auto | Device for local models (auto/cpu/cuda) |
| `MAX_CONTENT_LENGTH` | 4000 | Maximum content length for processing |
| `MAX_SUMMARY_LENGTH` | 200 | Maximum summary length |
| `MAX_TAGS_COUNT` | 5 | Maximum number of tags to generate |

### Model Configuration

```python
# OpenAI Models
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.3

# Hugging Face Models
HF_SUMMARIZATION_MODEL=facebook/bart-large-cnn
HF_QA_MODEL=deepset/roberta-base-squad2
```

## 🔧 API Setup

### OpenAI Setup

1. **Get API Key:**
   - Visit [OpenAI Platform](https://platform.openai.com/)
   - Create an account and get your API key
   - Add credits to your account

2. **Set Environment Variable:**
   ```bash
   export OPENAI_API_KEY="sk-your-api-key-here"
   ```

3. **Test:**
   ```python
   from app.ai.openai_client import get_openai_client
   client = get_openai_client()
   print(f"OpenAI available: {client.is_available()}")
   ```

### Hugging Face Setup

1. **Get API Key (Optional):**
   - Visit [Hugging Face](https://huggingface.co/)
   - Create an account and get your API key
   - Free tier includes 30,000 requests/month

2. **Set Environment Variable:**
   ```bash
   export HUGGINGFACE_API_KEY="hf-your-api-key-here"
   ```

3. **Test:**
   ```python
   from app.ai.huggingface_client import get_huggingface_client
   client = get_huggingface_client()
   print(f"Hugging Face available: {client.is_available()}")
   ```

## 🧪 Testing

### Run the Test Script

```bash
python test_enhanced_ai.py
```

This will test:
- ✅ Environment setup
- ✅ AI provider availability
- ✅ Document summarization
- ✅ Document tagging
- ✅ Document querying
- ✅ Complete file processing

### Manual Testing

```python
from app.ai.enhanced_processor import get_enhanced_processor

# Get processor
processor = get_enhanced_processor()

# Test with sample content
content = "Your document content here..."

# Generate summary
summary_result = processor.generate_summary(content)
print(f"Summary: {summary_result['summary']}")

# Generate tags
tags_result = processor.generate_tags(content)
print(f"Tags: {tags_result['tags']}")

# Query document
query_result = processor.query_file_content(content, "What is this document about?")
print(f"Answer: {query_result['answer']}")
```

## 📊 Performance Comparison

| Provider | Setup Difficulty | Cost | Performance | Reliability |
|----------|------------------|------|-------------|-------------|
| OpenAI | Easy | Paid | Excellent | High |
| Simple AI Client | None | Free | Good | Very High |
| Rule-based | None | Free | Basic | Very High |

## 🔄 Provider Priority

The system automatically tries providers in this order:

1. **OpenAI** (if API key available)
2. **Simple AI Client** (rule-based + optional Hugging Face API)
3. **Rule-based fallback** (always available)

## 🛠️ Troubleshooting

### Common Issues

1. **"OpenAI API not configured"**
   - Set `OPENAI_API_KEY` environment variable
   - Or use Hugging Face/local models instead

2. **"Local models failed to load"**
   - Check available memory (models require 2-4GB)
   - Set `LOCAL_MODEL_DEVICE=cpu` for lower memory usage
   - Or disable local models: `USE_LOCAL_MODELS=false`

3. **"All AI providers failed"**
   - Check internet connection for API calls
   - Verify API keys are correct
   - Check system memory for local models

### Memory Requirements

- **Local Models**: 2-4GB RAM
- **API Calls**: Minimal memory usage
- **Rule-based**: Minimal memory usage

### Performance Tips

1. **For Production:**
   - Use OpenAI for best results
   - Set up proper error handling
   - Monitor API usage and costs

2. **For Development:**
   - Use local models for free testing
   - Set `USE_LOCAL_MODELS=true`
   - Use rule-based fallback for basic testing

3. **For Offline Use:**
   - Disable API calls: `USE_LOCAL_MODELS=true`
   - Ensure sufficient memory for local models
   - Use rule-based fallback as backup

## 🔐 Security Considerations

1. **API Keys:**
   - Never commit API keys to version control
   - Use environment variables
   - Rotate keys regularly

2. **Data Privacy:**
   - OpenAI processes data on their servers
   - Hugging Face API processes data on their servers
   - Local models process data locally (most private)

3. **Rate Limiting:**
   - Monitor API usage
   - Implement rate limiting for production
   - Use fallback providers for reliability

## 📈 Monitoring and Logging

The system includes comprehensive logging:

```python
import logging
logging.basicConfig(level=logging.INFO)

# Check which provider is being used
from app.ai.enhanced_processor import get_enhanced_processor
processor = get_enhanced_processor()
```

Logs will show:
- Which provider is being used
- Success/failure of operations
- Performance metrics
- Error details

## 🎯 Best Practices

1. **Start Simple:**
   - Begin with rule-based fallback
   - Add local models for better performance
   - Add API providers for best results

2. **Monitor Usage:**
   - Track API calls and costs
   - Monitor system performance
   - Log errors and failures

3. **Plan for Scale:**
   - Use background tasks for processing
   - Implement caching for repeated queries
   - Consider multiple AI providers for redundancy

4. **User Experience:**
   - Provide clear feedback on AI processing
   - Show which AI provider is being used
   - Handle errors gracefully

## 🚀 Next Steps

1. **Set up your preferred AI providers**
2. **Test with your own documents**
3. **Monitor performance and costs**
4. **Customize prompts and models as needed**
5. **Implement additional AI features**

For more information, see the main README.md file or contact the development team. 