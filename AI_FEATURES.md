# AI-Powered File Tagging and Summarization

## Overview

The SmartCloud system now includes AI-powered automatic tagging and summarization of uploaded files. The system uses state-of-the-art language models to analyze file content and generate intelligent tags and summaries.

## Features

### 🏷️ Automatic Tagging
- **Intelligent Classification**: Uses zero-shot classification to automatically categorize files
- **Multi-label Support**: Files can have multiple relevant tags
- **Predefined Categories**: 17 predefined categories including Finance, Work, Personal, Legal, Medical, Education, Technology, Business, Creative, Travel, Health, Real Estate, Marketing, Research, Project Management, HR, and Sales

### 📝 Automatic Summarization
- **Content Summarization**: Generates concise summaries of file content
- **Smart Truncation**: Handles large files by intelligently truncating content
- **Multiple Formats**: Supports various file types including .txt, .docx, .pdf, and code files

### 🔍 Smart Search
- **Multi-field Search**: Search across filenames, AI tags, and summaries
- **Real-time Results**: Instant search results with AI-enhanced metadata

### 🤖 File Querying (NEW!)
- **Interactive File Q&A**: Ask questions about specific files
- **Natural Language Queries**: Use natural language to ask about file content
- **Intelligent Responses**: Get contextual answers based on file content
- **Multiple Query Types**: Ask about achievements, features, status, next steps, team info, budget, etc.

## Supported File Types

- **Text Files**: .txt files
- **Documents**: .docx files (Microsoft Word)
- **PDFs**: .pdf files
- **Code Files**: .py, .js, .html, .css, .java, .cpp, .c files
- **Other**: Any text-based file format

## API Endpoints

### File Listing with AI Results
```http
GET /files
```
Returns file list including AI tags and summaries.

### File Details
```http
GET /files/{file_id}
```
Returns detailed information about a specific file including AI results.

### Manual AI Processing
```http
POST /files/{file_id}/process-ai
```
Manually trigger AI processing for a specific file.

### AI-Enhanced Search
```http
GET /files/search?query={search_term}
```
Search files by AI tags, summary, or filename.

### File Querying (NEW!)
```http
POST /files/{file_id}/query
Content-Type: application/x-www-form-urlencoded

prompt=What are the main achievements in this document?
```
Query a specific file with natural language questions.

**Example Queries:**
- "What is this document about?"
- "What are the main achievements mentioned?"
- "What features or capabilities are described?"
- "What is the current status of the project?"
- "What are the next steps?"
- "What team information is available?"
- "What budget information is mentioned?"
- "Summarize this document for me"

**Response:**
```json
{
  "file_id": 1,
  "filename": "project_report.txt",
  "user_prompt": "What are the main achievements?",
  "ai_answer": "Key achievements mentioned in the document: Successfully implemented secure user authentication with JWT tokens. Created robust file upload and storage system. Developed AI-powered content analysis and tagging.",
  "status": "success"
}
```

## Database Schema

The `file_metadata` table includes two new columns:
- `ai_tags`: Comma-separated list of AI-generated tags
- `summary`: AI-generated summary of file content

## Technical Implementation

### AI Models Used
- **Tagging**: Facebook BART-large-mnli for zero-shot classification
- **Summarization**: Facebook BART-large-cnn for text summarization
- **Querying**: Rule-based approach with keyword analysis (expandable to LLM)

### Processing Pipeline
1. **Text Extraction**: Extract text content from various file formats
2. **Content Analysis**: Analyze text using AI models
3. **Tag Generation**: Generate relevant tags using zero-shot classification
4. **Summary Generation**: Create concise summaries
5. **Query Processing**: Handle natural language queries about file content
6. **Database Storage**: Save results to database

### Error Handling
- Graceful fallback for unsupported file types
- Comprehensive logging for debugging
- Error recovery mechanisms

## Installation

1. Install the new dependencies:
```bash
pip install -r requirements.txt
```

2. The AI models will be downloaded automatically on first use.

## Usage Examples

### Upload a File
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf"
```

### List Files with AI Results
```bash
curl -X GET "http://localhost:8000/files" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Search Files
```bash
curl -X GET "http://localhost:8000/files/search?query=finance" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Query a File (NEW!)
```bash
curl -X POST "http://localhost:8000/files/1/query" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "prompt=What are the main achievements in this document?"
```

### Manual AI Processing
```bash
curl -X POST "http://localhost:8000/files/1/process-ai" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Performance Considerations

- **Model Loading**: Models are loaded once and cached in memory
- **GPU Support**: Automatically uses GPU if available
- **Async Processing**: File processing happens asynchronously via Celery
- **Batch Processing**: Multiple files can be processed simultaneously

## Future Enhancements

- Custom tag categories based on user preferences
- Advanced content analysis (sentiment, key entities)
- Multi-language support
- Document structure analysis
- Image content analysis for image files
- Integration with external LLM APIs (OpenAI, Anthropic, etc.)
- Advanced query processing with semantic understanding
- Conversation history for file queries
- Multi-file querying across related documents 