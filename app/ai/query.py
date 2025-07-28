# app/ai/query.py
import logging
from typing import Dict, Optional
from app.ai.tagging import get_ai_tagger

logger = logging.getLogger(__name__)

class FileQuerySystem:
    def __init__(self):
        """Initialize file query system"""
        self.ai_tagger = get_ai_tagger()
        logger.info("File query system initialized")
    
    def query_file(self, file_path: str, user_prompt: str) -> Dict[str, any]:
        """Query a specific file with a user prompt"""
        try:
            # Extract text from file
            text = self.ai_tagger.extract_text_from_file(file_path)
            
            if not text.strip():
                return {
                    "status": "error",
                    "message": "No text content found in file",
                    "answer": "I cannot answer questions about this file as it contains no readable text content."
                }
            
            # Create a context-aware prompt for the LLM
            enhanced_prompt = self._create_enhanced_prompt(text, user_prompt)
            
            # Generate answer using rule-based approach (for now)
            # In the future, this can be replaced with actual LLM calls
            answer = self._generate_answer(enhanced_prompt, text)
            
            return {
                "status": "success",
                "file_path": file_path,
                "user_prompt": user_prompt,
                "answer": answer
            }
            
        except Exception as e:
            logger.error(f"Error querying file {file_path}: {e}")
            return {
                "status": "error",
                "message": f"Error processing file query: {str(e)}",
                "answer": "Sorry, I encountered an error while processing your question about this file."
            }
    
    def _create_enhanced_prompt(self, file_content: str, user_prompt: str) -> str:
        """Create an enhanced prompt for better AI responses"""
        # Truncate file content if too long
        max_content_length = 2000
        if len(file_content) > max_content_length:
            file_content = file_content[:max_content_length] + "..."
        
        enhanced_prompt = f"""
Based on the following file content, please answer the user's question.

File Content:
{file_content}

User Question: {user_prompt}

Please provide a clear, accurate answer based only on the information in the file content above.
"""
        return enhanced_prompt
    
    def _generate_answer(self, prompt: str, file_content: str) -> str:
        """Generate answer using rule-based approach (placeholder for LLM)"""
        # This is a simple rule-based approach
        # In production, you would call an actual LLM here
        
        prompt_lower = prompt.lower()
        user_question = prompt.split("User Question: ")[-1].strip().lower()
        
        # Simple keyword-based responses
        if "summary" in user_question or "summarize" in user_question:
            return self._generate_summary_response(file_content)
        
        elif "achievement" in user_question or "accomplish" in user_question or "complete" in user_question:
            return self._find_achievements(file_content)
        
        elif "feature" in user_question or "capability" in user_question or "function" in user_question:
            return self._find_features(file_content)
        
        elif "status" in user_question or "progress" in user_question or "current" in user_question:
            return self._find_status(file_content)
        
        elif "next" in user_question or "future" in user_question or "plan" in user_question:
            return self._find_next_steps(file_content)
        
        elif "team" in user_question or "member" in user_question:
            return self._find_team_info(file_content)
        
        elif "budget" in user_question or "cost" in user_question or "financial" in user_question:
            return self._find_budget_info(file_content)
        
        else:
            # Generic response based on content analysis
            return self._generate_generic_response(file_content, user_question)
    
    def _generate_summary_response(self, content: str) -> str:
        """Generate a summary response"""
        sentences = content.split('. ')
        if len(sentences) >= 3:
            summary = '. '.join(sentences[:3]) + '.'
            return f"Here's a summary of the document: {summary}"
        else:
            return f"Here's the document content: {content}"
    
    def _find_achievements(self, content: str) -> str:
        """Find achievements in the content"""
        achievement_keywords = ['achieved', 'completed', 'implemented', 'successfully', 'delivered', 'finished', 'accomplished', 'developed', 'created', 'built']
        sentences = content.split('. ')
        achievements = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in achievement_keywords):
                achievements.append(sentence.strip())
        
        if achievements:
            return f"Key achievements mentioned in the document: {' '.join(achievements[:3])}"
        else:
            return "No specific achievements are mentioned in this document."
    
    def _find_features(self, content: str) -> str:
        """Find features/capabilities in the content"""
        feature_keywords = ['feature', 'system', 'technology', 'capability', 'functionality', 'tool', 'platform', 'solution', 'service']
        sentences = content.split('. ')
        features = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in feature_keywords):
                features.append(sentence.strip())
        
        if features:
            return f"Key features and capabilities mentioned: {' '.join(features[:3])}"
        else:
            return "No specific features or capabilities are mentioned in this document."
    
    def _find_status(self, content: str) -> str:
        """Find current status information"""
        status_keywords = ['currently', 'status', 'progress', 'schedule', 'budget', 'ready', 'deployment', 'production']
        sentences = content.split('. ')
        status_info = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in status_keywords):
                status_info.append(sentence.strip())
        
        if status_info:
            return f"Current status information: {' '.join(status_info[:2])}"
        else:
            return "No specific status information is mentioned in this document."
    
    def _find_next_steps(self, content: str) -> str:
        """Find next steps or future plans"""
        next_keywords = ['next', 'future', 'plan', 'upcoming', 'will', 'going to', 'intend to']
        sentences = content.split('. ')
        next_steps = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in next_keywords):
                next_steps.append(sentence.strip())
        
        if next_steps:
            return f"Next steps and future plans: {' '.join(next_steps[:2])}"
        else:
            return "No specific next steps or future plans are mentioned in this document."
    
    def _find_team_info(self, content: str) -> str:
        """Find team-related information"""
        team_keywords = ['team', 'member', 'developer', 'staff', 'personnel', 'collaborator']
        sentences = content.split('. ')
        team_info = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in team_keywords):
                team_info.append(sentence.strip())
        
        if team_info:
            return f"Team information: {' '.join(team_info[:2])}"
        else:
            return "No specific team information is mentioned in this document."
    
    def _find_budget_info(self, content: str) -> str:
        """Find budget or financial information"""
        budget_keywords = ['budget', 'cost', 'financial', 'money', 'expense', 'revenue', 'funding']
        sentences = content.split('. ')
        budget_info = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in budget_keywords):
                budget_info.append(sentence.strip())
        
        if budget_info:
            return f"Budget and financial information: {' '.join(budget_info[:2])}"
        else:
            return "No specific budget or financial information is mentioned in this document."
    
    def _generate_generic_response(self, content: str, question: str) -> str:
        """Generate a generic response based on content analysis"""
        # Simple keyword matching for common questions
        if "what" in question:
            # Extract key sentences that might answer "what" questions
            sentences = content.split('. ')
            key_sentences = sentences[:2]  # Take first two sentences
            return f"Based on the document content: {' '.join(key_sentences)}"
        
        elif "how" in question:
            return "The document describes various processes and implementations. For specific details, please ask a more specific question about what aspect you're interested in."
        
        elif "when" in question:
            return "The document doesn't contain specific timeline information. Please ask about specific aspects of the project or content."
        
        elif "where" in question:
            return "This appears to be a project document. For location-specific information, please ask about specific aspects of the project."
        
        else:
            return f"I found information in the document that might be relevant to your question. Here are the key points: {content[:300]}..."

# Global instance
file_query_system = None

def get_file_query_system() -> FileQuerySystem:
    """Get or create file query system instance"""
    global file_query_system
    if file_query_system is None:
        file_query_system = FileQuerySystem()
    return file_query_system

def query_file_with_ai(file_path: str, user_prompt: str) -> Dict[str, any]:
    """Query a file with AI and return the answer"""
    query_system = get_file_query_system()
    return query_system.query_file(file_path, user_prompt) 