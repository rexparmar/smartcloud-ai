# SmartCloud AI

A document management system with AI-powered file analysis, summarization, and querying capabilities.

## Features

- 📁 **File Upload & Management**: Upload, organize, and manage your documents
- 🤖 **AI Analysis**: Automatic document summarization and intelligent tagging
- 🔍 **Smart Search**: Search files by content, tags, or AI-generated summaries
- 💬 **AI Querying**: Ask questions about your documents using natural language
- 🔗 **File Sharing**: Generate shareable links for your documents
- 🗑️ **File Deletion**: Secure file deletion with metadata cleanup

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables (Optional)
```bash
# For best AI performance (OpenAI)
export OPENAI_API_KEY="your_openai_key"

# For free AI alternatives (Hugging Face)
export HUGGINGFACE_API_KEY="your_hf_key"
```

### 3. Run the Application
```bash
# Option 1: Using the startup script (recommended)
python run.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /upload` - Upload a file
- `GET /files` - List user's files
- `GET /files/{file_id}` - Get file details
- `DELETE /files/{file_id}` - Delete a file
- `GET /download/{file_id}` - Download a file
- `POST /share/{file_id}` - Create share link
- `POST /files/{file_id}/query` - Query file with AI
- `GET /files/search` - Search files

## AI Capabilities

The system supports multiple AI providers:
- **OpenAI** (Best performance - paid)
- **Simple AI Client** (Free - rule-based + optional Hugging Face API)
- **Rule-based Fallback** (Always available)

## Testing

```bash
# Test basic functionality
python test_simple_ai.py

# Test with your own files
curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@your_document.pdf"
```

## Documentation

- API docs: `http://localhost:8000/docs`
- AI features: See `AI_FEATURES.md`
