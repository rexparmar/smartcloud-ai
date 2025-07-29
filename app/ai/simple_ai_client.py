import os
import logging
import requests
from typing import Dict, List, Optional
import json
import re

logger = logging.getLogger(__name__)

class SimpleAIClient:
    """Simple AI client that works without heavy dependencies"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize simple AI client"""
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.base_url = "https://api-inference.huggingface.co"
        
        if not self.api_key:
            logger.warning("Hugging Face API key not found. Will use rule-based fallback only.")
    
    def is_available(self) -> bool:
        """Check if Hugging Face API is available"""
        return bool(self.api_key)
    
    def query_file_content(self, file_content: str, user_prompt: str) -> Dict[str, any]:
        """Query file content using simple rule-based approach or API"""
        try:
            # Try API if available
            if self.is_available():
                result = self._query_with_api(file_content, user_prompt)
                if result["status"] == "success":
                    return result
            
            # Fallback to rule-based approach
            return self._rule_based_query(file_content, user_prompt)
            
        except Exception as e:
            logger.error(f"Error querying with simple AI: {e}")
            return {
                "status": "error",
                "message": f"Simple AI error: {str(e)}",
                "answer": "Sorry, I encountered an error while processing your question."
            }
    
    def generate_summary(self, file_content: str) -> Dict[str, any]:
        """Generate a summary using simple rule-based approach or API"""
        try:
            # Try API if available
            if self.is_available():
                result = self._summarize_with_api(file_content)
                if result["status"] == "success":
                    return result
            
            # Fallback to rule-based approach
            return self._rule_based_summary(file_content)
            
        except Exception as e:
            logger.error(f"Error generating summary with simple AI: {e}")
            return {
                "status": "error",
                "message": f"Simple AI error: {str(e)}",
                "summary": "Unable to generate summary due to AI service error."
            }
    
    def generate_tags(self, file_content: str) -> Dict[str, any]:
        """Generate tags using simple rule-based approach"""
        try:
            # Extract key terms from content
            words = file_content.lower().split()
            word_freq = {}
            
            # Common stop words to ignore
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
            
            for word in words:
                # Clean word
                word = ''.join(c for c in word if c.isalnum())
                if len(word) > 3 and word not in stop_words:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top 5 most frequent words
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Map words to categories
            tags = self._categorize_content(file_content)
            
            return {
                "status": "success",
                "tags": tags,
                "model": "simple-rule-based"
            }
            
        except Exception as e:
            logger.error(f"Error generating tags with simple AI: {e}")
            return {
                "status": "error",
                "message": f"Simple AI error: {str(e)}",
                "tags": []
            }
    
    def _categorize_content(self, content: str) -> List[str]:
        """Categorize content based on keywords"""
        content_lower = content.lower()
        categories = []
        
        # Define category keywords
        category_keywords = {
            "Technology": ["software", "system", "development", "technical", "code", "programming", "api", "database"],
            "Business": ["project", "company", "business", "management", "strategy", "organization", "team"],
            "Finance": ["budget", "cost", "financial", "money", "expense", "revenue", "payment", "invoice"],
            "Education": ["learning", "study", "course", "education", "training", "academic", "school"],
            "Health": ["medical", "health", "doctor", "patient", "treatment", "medicine", "hospital"],
            "Legal": ["legal", "law", "contract", "agreement", "legal", "attorney", "court"],
            "Marketing": ["marketing", "advertising", "campaign", "promotion", "brand", "customer"],
            "Research": ["research", "study", "analysis", "data", "investigation", "survey"],
            "Project Management": ["project", "management", "planning", "schedule", "milestone", "deliverable"],
            "Documentation": ["document", "report", "file", "record", "documentation", "manual"]
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                categories.append(category)
        
        return categories[:5]  # Limit to 5 categories
    
    def _query_with_api(self, file_content: str, user_prompt: str) -> Dict[str, any]:
        """Query using Hugging Face API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Use a question-answering model
            data = {
                "inputs": {
                    "question": user_prompt,
                    "context": file_content[:1000]  # Limit context
                }
            }
            
            response = requests.post(
                f"{self.base_url}/models/deepset/roberta-base-squad2",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "answer": result.get("answer", "No answer found"),
                    "confidence": result.get("score", 0),
                    "model": "api-roberta-qa"
                }
            else:
                return {
                    "status": "error",
                    "message": f"API error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"API call failed: {str(e)}"
            }
    
    def _summarize_with_api(self, file_content: str) -> Dict[str, any]:
        """Summarize using Hugging Face API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "inputs": file_content[:1000],  # Limit input
                "parameters": {
                    "max_length": 150,
                    "min_length": 50
                }
            }
            
            response = requests.post(
                f"{self.base_url}/models/facebook/bart-large-cnn",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "summary": result[0].get("summary_text", "No summary generated"),
                    "model": "api-bart-summarizer"
                }
            else:
                return {
                    "status": "error",
                    "message": f"API error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"API call failed: {str(e)}"
            }
    
    def _rule_based_query(self, file_content: str, user_prompt: str) -> Dict[str, any]:
        """Rule-based query using simple text analysis"""
        try:
            prompt_lower = user_prompt.lower()
            content_lower = file_content.lower()
            
            # Simple keyword-based responses
            if "summary" in prompt_lower or "summarize" in prompt_lower:
                sentences = file_content.split('. ')
                summary = '. '.join(sentences[:3]) + '.'
                return {
                    "status": "success",
                    "answer": f"Here's a summary: {summary}",
                    "model": "simple-rule-based"
                }
            
            elif "what" in prompt_lower:
                # Find sentences that might answer "what" questions
                sentences = file_content.split('. ')
                key_sentences = sentences[:2]
                return {
                    "status": "success",
                    "answer": f"Based on the document: {' '.join(key_sentences)}",
                    "model": "simple-rule-based"
                }
            
            elif "how" in prompt_lower:
                return {
                    "status": "success",
                    "answer": "The document describes various processes and implementations. For specific details, please ask a more specific question about what aspect you're interested in.",
                    "model": "simple-rule-based"
                }
            
            else:
                return {
                    "status": "success",
                    "answer": "I found information in the document that might be relevant to your question. Please ask a more specific question about the content.",
                    "model": "simple-rule-based"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Rule-based query failed: {str(e)}",
                "answer": "Sorry, I cannot process your question at this time."
            }
    
    def _rule_based_summary(self, file_content: str) -> Dict[str, any]:
        """Rule-based summary generation"""
        try:
            sentences = file_content.split('. ')
            if len(sentences) >= 3:
                summary = '. '.join(sentences[:3]) + '.'
            else:
                summary = file_content[:200] + "..." if len(file_content) > 200 else file_content
            
            return {
                "status": "success",
                "summary": summary,
                "model": "simple-rule-based"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Rule-based summary failed: {str(e)}",
                "summary": "Unable to generate summary."
            }

# Global instance
simple_ai_client = None

def get_simple_ai_client() -> SimpleAIClient:
    """Get or create simple AI client instance"""
    global simple_ai_client
    if simple_ai_client is None:
        simple_ai_client = SimpleAIClient()
    return simple_ai_client 