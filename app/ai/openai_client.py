import os
import logging
import requests
from typing import Dict, List, Optional
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
        self.model = "gpt-3.5-turbo"  # Default model, can be overridden
        
        if not self.api_key:
            logger.warning("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
    
    def is_available(self) -> bool:
        """Check if OpenAI API is available"""
        return bool(self.api_key)
    
    def query_file_content(self, file_content: str, user_prompt: str) -> Dict[str, any]:
        """Query file content using OpenAI"""
        if not self.is_available():
            return {
                "status": "error",
                "message": "OpenAI API not configured",
                "answer": "AI service not available. Please configure OpenAI API key."
            }
        
        try:
            # Prepare the prompt
            system_prompt = """You are a helpful AI assistant that answers questions about documents. 
            Provide accurate, concise answers based only on the information in the document content provided.
            If the document doesn't contain information to answer the question, say so clearly."""
            
            user_message = f"""Document Content:
{file_content}

User Question: {user_prompt}

Please answer the question based on the document content above."""

            response = self._make_api_call(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            
            if response["status"] == "success":
                return {
                    "status": "success",
                    "answer": response["content"],
                    "model": self.model
                }
            else:
                return {
                    "status": "error",
                    "message": response.get("message", "Unknown error"),
                    "answer": "Sorry, I encountered an error while processing your question."
                }
                
        except Exception as e:
            logger.error(f"Error querying with OpenAI: {e}")
            return {
                "status": "error",
                "message": f"OpenAI API error: {str(e)}",
                "answer": "Sorry, I encountered an error while processing your question."
            }
    
    def generate_summary(self, file_content: str) -> Dict[str, any]:
        """Generate a summary using OpenAI"""
        if not self.is_available():
            return {
                "status": "error",
                "message": "OpenAI API not configured",
                "summary": "AI service not available for summarization."
            }
        
        try:
            system_prompt = """You are an expert at summarizing documents. 
            Create a concise, informative summary that captures the key points, 
            main objectives, achievements, and important details from the document.
            Keep the summary under 200 words and focus on the most important information."""
            
            user_message = f"""Please provide a comprehensive summary of the following document:

{file_content}

Focus on:
- Main topic/purpose
- Key achievements or results
- Important features or capabilities
- Current status or progress
- Next steps or future plans (if mentioned)"""

            response = self._make_api_call(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            
            if response["status"] == "success":
                return {
                    "status": "success",
                    "summary": response["content"],
                    "model": self.model
                }
            else:
                return {
                    "status": "error",
                    "message": response.get("message", "Unknown error"),
                    "summary": "Unable to generate summary due to AI service error."
                }
                
        except Exception as e:
            logger.error(f"Error generating summary with OpenAI: {e}")
            return {
                "status": "error",
                "message": f"OpenAI API error: {str(e)}",
                "summary": "Unable to generate summary due to AI service error."
            }
    
    def generate_tags(self, file_content: str) -> Dict[str, any]:
        """Generate intelligent tags using OpenAI"""
        if not self.is_available():
            return {
                "status": "error",
                "message": "OpenAI API not configured",
                "tags": []
            }
        
        try:
            system_prompt = """You are an expert at categorizing and tagging documents. 
            Analyze the document content and generate 3-5 relevant tags that best describe the document.
            Return only the tags as a comma-separated list, no additional text."""
            
            user_message = f"""Analyze this document and provide 3-5 relevant tags:

{file_content}

Return only the tags as a comma-separated list."""

            response = self._make_api_call(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            
            if response["status"] == "success":
                # Parse tags from response
                tags_text = response["content"].strip()
                tags = [tag.strip() for tag in tags_text.split(",") if tag.strip()]
                
                return {
                    "status": "success",
                    "tags": tags,
                    "model": self.model
                }
            else:
                return {
                    "status": "error",
                    "message": response.get("message", "Unknown error"),
                    "tags": []
                }
                
        except Exception as e:
            logger.error(f"Error generating tags with OpenAI: {e}")
            return {
                "status": "error",
                "message": f"OpenAI API error: {str(e)}",
                "tags": []
            }
    
    def _make_api_call(self, messages: List[Dict[str, str]]) -> Dict[str, any]:
        """Make API call to OpenAI"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.3
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                return {
                    "status": "success",
                    "content": content
                }
            else:
                error_msg = f"OpenAI API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return {
                    "status": "error",
                    "message": error_msg
                }
                
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "message": "Request timeout - OpenAI API took too long to respond"
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Network error: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }

# Global instance
openai_client = None

def get_openai_client() -> OpenAIClient:
    """Get or create OpenAI client instance"""
    global openai_client
    if openai_client is None:
        openai_client = OpenAIClient()
    return openai_client 