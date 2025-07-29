import os
import logging
from typing import Dict, List, Optional
from app.ai.openai_client import get_openai_client
from app.ai.simple_ai_client import get_simple_ai_client
from app.ai.tagging import get_ai_tagger

logger = logging.getLogger(__name__)

class EnhancedAIProcessor:
    def __init__(self):
        """Initialize enhanced AI processor with multiple providers"""
        self.openai_client = get_openai_client()
        self.simple_ai_client = get_simple_ai_client()
        self.fallback_tagger = get_ai_tagger()
        
        # Priority order for AI providers
        self.provider_priority = ["openai", "simple_ai", "fallback"]
        
        logger.info("Enhanced AI processor initialized")
    
    def query_file_content(self, file_content: str, user_prompt: str) -> Dict[str, any]:
        """Query file content using the best available AI provider"""
        if not file_content.strip():
            return {
                "status": "error",
                "message": "No content to query",
                "answer": "The file contains no readable text content."
            }
        
        # Try providers in priority order
        for provider in self.provider_priority:
            try:
                if provider == "openai" and self.openai_client.is_available():
                    logger.info("Using OpenAI for query")
                    result = self.openai_client.query_file_content(file_content, user_prompt)
                    if result["status"] == "success":
                        return result
                
                elif provider == "simple_ai":
                    logger.info("Using Simple AI for query")
                    result = self.simple_ai_client.query_file_content(file_content, user_prompt)
                    if result["status"] == "success":
                        return result
                
                elif provider == "fallback":
                    logger.info("Using fallback rule-based approach for query")
                    return self._fallback_query(file_content, user_prompt)
                    
            except Exception as e:
                logger.warning(f"Provider {provider} failed: {e}")
                continue
        
        # If all providers failed
        return {
            "status": "error",
            "message": "All AI providers failed",
            "answer": "Sorry, I'm unable to process your question at this time."
        }
    
    def generate_summary(self, file_content: str) -> Dict[str, any]:
        """Generate summary using the best available AI provider"""
        if not file_content.strip():
            return {
                "status": "error",
                "message": "No content to summarize",
                "summary": "The file contains no readable text content."
            }
        
        # Try providers in priority order
        for provider in self.provider_priority:
            try:
                if provider == "openai" and self.openai_client.is_available():
                    logger.info("Using OpenAI for summary")
                    result = self.openai_client.generate_summary(file_content)
                    if result["status"] == "success":
                        return result
                
                elif provider == "simple_ai":
                    logger.info("Using Simple AI for summary")
                    result = self.simple_ai_client.generate_summary(file_content)
                    if result["status"] == "success":
                        return result
                
                elif provider == "fallback":
                    logger.info("Using fallback rule-based approach for summary")
                    return self._fallback_summary(file_content)
                    
            except Exception as e:
                logger.warning(f"Provider {provider} failed: {e}")
                continue
        
        # If all providers failed
        return {
            "status": "error",
            "message": "All AI providers failed",
            "summary": "Unable to generate summary due to AI service errors."
        }
    
    def generate_tags(self, file_content: str) -> Dict[str, any]:
        """Generate tags using the best available AI provider"""
        if not file_content.strip():
            return {
                "status": "error",
                "message": "No content to tag",
                "tags": []
            }
        
        # Try providers in priority order
        for provider in self.provider_priority:
            try:
                if provider == "openai" and self.openai_client.is_available():
                    logger.info("Using OpenAI for tags")
                    result = self.openai_client.generate_tags(file_content)
                    if result["status"] == "success":
                        return result
                
                elif provider == "simple_ai":
                    logger.info("Using Simple AI for tags")
                    result = self.simple_ai_client.generate_tags(file_content)
                    if result["status"] == "success":
                        return result
                
                elif provider == "fallback":
                    logger.info("Using fallback rule-based approach for tags")
                    return self._fallback_tags(file_content)
                    
            except Exception as e:
                logger.warning(f"Provider {provider} failed: {e}")
                continue
        
        # If all providers failed
        return {
            "status": "error",
            "message": "All AI providers failed",
            "tags": []
        }
    
    def process_file_complete(self, file_content: str) -> Dict[str, any]:
        """Process file with all AI operations (summary, tags, and basic analysis)"""
        if not file_content.strip():
            return {
                "status": "error",
                "message": "No content to process",
                "summary": "",
                "tags": [],
                "analysis": {}
            }
        
        try:
            # Generate summary
            summary_result = self.generate_summary(file_content)
            summary = summary_result.get("summary", "") if summary_result["status"] == "success" else ""
            
            # Generate tags
            tags_result = self.generate_tags(file_content)
            tags = tags_result.get("tags", []) if tags_result["status"] == "success" else []
            
            # Basic analysis
            analysis = self._basic_analysis(file_content)
            
            return {
                "status": "success",
                "summary": summary,
                "tags": tags,
                "analysis": analysis,
                "summary_model": summary_result.get("model", "unknown"),
                "tags_model": tags_result.get("model", "unknown")
            }
            
        except Exception as e:
            logger.error(f"Error in complete file processing: {e}")
            return {
                "status": "error",
                "message": f"Processing failed: {str(e)}",
                "summary": "",
                "tags": [],
                "analysis": {}
            }
    
    def _fallback_query(self, file_content: str, user_prompt: str) -> Dict[str, any]:
        """Fallback query using rule-based approach"""
        try:
            # Use the existing tagging system's text extraction
            text = file_content
            
            # Simple keyword-based responses
            prompt_lower = user_prompt.lower()
            
            if "summary" in prompt_lower or "summarize" in prompt_lower:
                sentences = text.split('. ')
                summary = '. '.join(sentences[:3]) + '.'
                return {
                    "status": "success",
                    "answer": f"Here's a summary: {summary}",
                    "model": "fallback-rule-based"
                }
            
            elif "what" in prompt_lower:
                sentences = text.split('. ')
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
        """Fallback summary using rule-based approach"""
        try:
            # Use the existing tagging system's summary generation
            summary = self.fallback_tagger.generate_summary(file_content)
            
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
    
    def _fallback_tags(self, file_content: str) -> Dict[str, any]:
        """Fallback tags using rule-based approach"""
        try:
            # Use the existing tagging system's tag generation
            tags = self.fallback_tagger.generate_tags(file_content)
            
            return {
                "status": "success",
                "tags": tags,
                "model": "fallback-rule-based"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Fallback tags failed: {str(e)}",
                "tags": []
            }
    
    def _basic_analysis(self, file_content: str) -> Dict[str, any]:
        """Perform basic content analysis"""
        try:
            analysis = {
                "word_count": len(file_content.split()),
                "character_count": len(file_content),
                "sentence_count": len([s for s in file_content.split('.') if s.strip()]),
                "paragraph_count": len([p for p in file_content.split('\n\n') if p.strip()]),
                "estimated_reading_time": len(file_content.split()) // 200,  # Average reading speed
                "content_type": self._detect_content_type(file_content),
                "key_topics": self._extract_key_topics(file_content)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in basic analysis: {e}")
            return {}
    
    def _detect_content_type(self, content: str) -> str:
        """Detect the type of content"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['invoice', 'bill', 'payment', 'financial']):
            return "Financial Document"
        elif any(word in content_lower for word in ['report', 'analysis', 'study']):
            return "Report"
        elif any(word in content_lower for word in ['meeting', 'agenda', 'minutes']):
            return "Meeting Document"
        elif any(word in content_lower for word in ['contract', 'agreement', 'legal']):
            return "Legal Document"
        elif any(word in content_lower for word in ['code', 'programming', 'software']):
            return "Technical Document"
        elif any(word in content_lower for word in ['email', 'message', 'correspondence']):
            return "Communication"
        else:
            return "General Document"
    
    def _extract_key_topics(self, content: str) -> List[str]:
        """Extract key topics from content"""
        try:
            # Simple keyword extraction
            words = content.lower().split()
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
            return [word for word, freq in top_words]
            
        except Exception as e:
            logger.error(f"Error extracting key topics: {e}")
            return []

# Global instance
enhanced_processor = None

def get_enhanced_processor() -> EnhancedAIProcessor:
    """Get or create enhanced AI processor instance"""
    global enhanced_processor
    if enhanced_processor is None:
        enhanced_processor = EnhancedAIProcessor()
    return enhanced_processor 