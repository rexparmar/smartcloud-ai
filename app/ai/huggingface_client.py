import os
import logging
import requests
from typing import Dict, List, Optional
import json

logger = logging.getLogger(__name__)

# Lazy imports to avoid circular import issues
def _import_transformers():
    """Lazy import of transformers to avoid circular import issues"""
    try:
        from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
        import torch
        return pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, torch
    except ImportError as e:
        logger.warning(f"Transformers not available: {e}")
        return None, None, None, None
    except Exception as e:
        logger.warning(f"Error importing transformers: {e}")
        return None, None, None, None

class HuggingFaceClient:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Hugging Face client"""
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.base_url = "https://api-inference.huggingface.co"
        
        # Local models for offline use
        self.local_summarizer = None
        self.local_qa_model = None
        
        if not self.api_key:
            logger.warning("Hugging Face API key not found. Will use local models only.")
    
    def is_available(self) -> bool:
        """Check if Hugging Face API is available"""
        return bool(self.api_key)
    
    def _get_local_summarizer(self):
        """Get or create local summarization model"""
        if self.local_summarizer is None:
            try:
                # Lazy import to avoid circular import issues
                pipeline, _, _, torch = _import_transformers()
                if pipeline is None:
                    logger.warning("Transformers not available, skipping local summarizer")
                    return None
                
                logger.info("Loading local summarization model...")
                self.local_summarizer = pipeline(
                    "summarization",
                    model="facebook/bart-large-cnn",
                    device=0 if torch.cuda.is_available() else -1
                )
                logger.info("Local summarization model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load local summarization model: {e}")
                return None
        return self.local_summarizer
    
    def _get_local_qa_model(self):
        """Get or create local question-answering model"""
        if self.local_qa_model is None:
            try:
                # Lazy import to avoid circular import issues
                pipeline, _, _, torch = _import_transformers()
                if pipeline is None:
                    logger.warning("Transformers not available, skipping local QA model")
                    return None
                
                logger.info("Loading local QA model...")
                self.local_qa_model = pipeline(
                    "question-answering",
                    model="deepset/roberta-base-squad2",
                    device=0 if torch.cuda.is_available() else -1
                )
                logger.info("Local QA model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load local QA model: {e}")
                return None
        return self.local_qa_model
    
    def query_file_content(self, file_content: str, user_prompt: str) -> Dict[str, any]:
        """Query file content using Hugging Face models"""
        try:
            # Try local QA model first
            qa_model = self._get_local_qa_model()
            if qa_model:
                try:
                    # For QA models, we need to provide context and question
                    result = qa_model(
                        question=user_prompt,
                        context=file_content[:1000]  # Limit context for performance
                    )
                    
                    if result and result.get('answer'):
                        return {
                            "status": "success",
                            "answer": result['answer'],
                            "confidence": result.get('score', 0),
                            "model": "local-roberta-qa"
                        }
                except Exception as e:
                    logger.warning(f"Local QA model failed: {e}")
            
            # Fallback to API if available
            if self.is_available():
                return self._query_with_api(file_content, user_prompt)
            
            # Final fallback to rule-based approach
            return self._fallback_query(file_content, user_prompt)
            
        except Exception as e:
            logger.error(f"Error querying with Hugging Face: {e}")
            return {
                "status": "error",
                "message": f"Hugging Face error: {str(e)}",
                "answer": "Sorry, I encountered an error while processing your question."
            }
    
    def generate_summary(self, file_content: str) -> Dict[str, any]:
        """Generate a summary using Hugging Face models"""
        try:
            # Try local summarizer first
            summarizer = self._get_local_summarizer()
            if summarizer:
                try:
                    # Split content if too long
                    max_length = 1024
                    if len(file_content) > max_length:
                        # Take first and last parts
                        first_part = file_content[:max_length//2]
                        last_part = file_content[-max_length//2:]
                        content_for_summary = first_part + "\n\n" + last_part
                    else:
                        content_for_summary = file_content
                    
                    result = summarizer(
                        content_for_summary,
                        max_length=150,
                        min_length=50,
                        do_sample=False
                    )
                    
                    if result and result[0].get('summary_text'):
                        return {
                            "status": "success",
                            "summary": result[0]['summary_text'],
                            "model": "local-bart-summarizer"
                        }
                except Exception as e:
                    logger.warning(f"Local summarizer failed: {e}")
            
            # Fallback to API if available
            if self.is_available():
                return self._summarize_with_api(file_content)
            
            # Final fallback to rule-based approach
            return self._fallback_summary(file_content)
            
        except Exception as e:
            logger.error(f"Error generating summary with Hugging Face: {e}")
            return {
                "status": "error",
                "message": f"Hugging Face error: {str(e)}",
                "summary": "Unable to generate summary due to AI service error."
            }
    
    def generate_tags(self, file_content: str) -> Dict[str, any]:
        """Generate tags using Hugging Face models"""
        try:
            # For tags, we'll use a simple approach with the summarizer
            summary_result = self.generate_summary(file_content)
            
            if summary_result["status"] == "success":
                # Extract key terms from summary for tags
                summary = summary_result["summary"]
                words = summary.lower().split()
                
                # Common tag categories
                tag_categories = {
                    "Technology": ["software", "system", "development", "technical", "code", "programming"],
                    "Business": ["project", "company", "business", "management", "strategy"],
                    "Finance": ["budget", "cost", "financial", "money", "expense", "revenue"],
                    "Education": ["learning", "training", "education", "course", "study"],
                    "Health": ["medical", "health", "treatment", "patient", "doctor"],
                    "Legal": ["legal", "law", "contract", "agreement", "document"],
                    "Marketing": ["marketing", "advertising", "campaign", "promotion"],
                    "Research": ["research", "analysis", "study", "data", "investigation"]
                }
                
                tags = []
                for category, keywords in tag_categories.items():
                    if any(keyword in words for keyword in keywords):
                        tags.append(category)
                
                # Add some content-based tags
                if any(word in file_content.lower() for word in ["report", "document", "file"]):
                    tags.append("Documentation")
                
                if any(word in file_content.lower() for word in ["meeting", "agenda", "minutes"]):
                    tags.append("Meeting")
                
                return {
                    "status": "success",
                    "tags": tags[:5],  # Limit to 5 tags
                    "model": summary_result.get("model", "local")
                }
            else:
                return {
                    "status": "error",
                    "message": "Failed to generate summary for tags",
                    "tags": []
                }
                
        except Exception as e:
            logger.error(f"Error generating tags with Hugging Face: {e}")
            return {
                "status": "error",
                "message": f"Hugging Face error: {str(e)}",
                "tags": []
            }
    
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
    
    def _fallback_query(self, file_content: str, user_prompt: str) -> Dict[str, any]:
        """Fallback query method using simple text analysis"""
        try:
            # Simple keyword-based response
            prompt_lower = user_prompt.lower()
            content_lower = file_content.lower()
            
            if "summary" in prompt_lower or "summarize" in prompt_lower:
                sentences = file_content.split('. ')
                summary = '. '.join(sentences[:3]) + '.'
                return {
                    "status": "success",
                    "answer": f"Here's a summary: {summary}",
                    "model": "fallback-rule-based"
                }
            
            elif "what" in prompt_lower:
                # Find sentences that might answer "what" questions
                sentences = file_content.split('. ')
                key_sentences = sentences[:2]
                return {
                    "status": "success",
                    "answer": f"Based on the document: {' '.join(key_sentences)}",
                    "model": "fallback-rule-based"
                }
            
            else:
                return {
                    "status": "success",
                    "answer": "I found information in the document that might be relevant to your question. Please ask a more specific question about the content.",
                    "model": "fallback-rule-based"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Fallback query failed: {str(e)}",
                "answer": "Sorry, I cannot process your question at this time."
            }
    
    def _fallback_summary(self, file_content: str) -> Dict[str, any]:
        """Fallback summary method"""
        try:
            sentences = file_content.split('. ')
            if len(sentences) >= 3:
                summary = '. '.join(sentences[:3]) + '.'
            else:
                summary = file_content[:200] + "..." if len(file_content) > 200 else file_content
            
            return {
                "status": "success",
                "summary": summary,
                "model": "fallback-rule-based"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Fallback summary failed: {str(e)}",
                "summary": "Unable to generate summary."
            }

# Global instance
huggingface_client = None

def get_huggingface_client() -> HuggingFaceClient:
    """Get or create Hugging Face client instance"""
    global huggingface_client
    if huggingface_client is None:
        huggingface_client = HuggingFaceClient()
    return huggingface_client 