# app/ai/tagging.py
import os
import logging
from typing import Dict, List, Tuple, Optional
import re

logger = logging.getLogger(__name__)

class AITaggingSystem:
    def __init__(self):
        """Initialize AI tagging system with rule-based approach for now"""
        self.tag_categories = [
            "Finance", "Work", "Personal", "Legal", "Medical", 
            "Education", "Technology", "Business", "Creative", 
            "Travel", "Health", "Real Estate", "Marketing",
            "Research", "Project Management", "HR", "Sales"
        ]
        
        # Define keyword patterns for each category
        self.category_keywords = {
            "Finance": ["invoice", "bill", "payment", "financial", "budget", "money", "cost", "expense", "revenue"],
            "Work": ["project", "meeting", "deadline", "report", "work", "business", "professional", "team", "task"],
            "Personal": ["family", "personal", "private", "home", "love", "relationship", "friend"],
            "Technology": ["software", "code", "programming", "development", "technical", "system", "computer", "digital"],
            "Business": ["company", "corporate", "enterprise", "strategy", "management", "organization"],
            "Education": ["learning", "study", "course", "education", "training", "academic", "school", "university"],
            "Health": ["medical", "health", "doctor", "patient", "treatment", "medicine", "hospital", "wellness"],
            "Legal": ["legal", "law", "contract", "agreement", "legal", "attorney", "court", "document"],
            "Marketing": ["marketing", "advertising", "campaign", "promotion", "brand", "customer", "market"],
            "Research": ["research", "study", "analysis", "data", "investigation", "survey", "findings"],
            "Project Management": ["project", "management", "planning", "schedule", "milestone", "deliverable", "timeline"],
            "HR": ["human resources", "hr", "employee", "staff", "recruitment", "hiring", "personnel"],
            "Sales": ["sales", "revenue", "customer", "deal", "purchase", "transaction", "client"],
            "Creative": ["design", "creative", "art", "content", "media", "visual", "creative"],
            "Travel": ["travel", "trip", "vacation", "destination", "hotel", "flight", "tourism"],
            "Real Estate": ["property", "real estate", "house", "apartment", "rental", "mortgage", "property"],
            "Medical": ["medical", "health", "doctor", "patient", "treatment", "medicine", "hospital", "diagnosis"]
        }
        
        logger.info("AI tagging system initialized with rule-based approach")
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text content from various file types"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.txt':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            
            elif file_extension == '.docx':
                try:
                    from docx import Document
                    doc = Document(file_path)
                    return ' '.join([paragraph.text for paragraph in doc.paragraphs])
                except ImportError:
                    logger.warning("python-docx not available, treating as text file")
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        return f.read()
            
            elif file_extension == '.pdf':
                try:
                    import PyPDF2
                    text = ""
                    with open(file_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        for page in pdf_reader.pages:
                            text += page.extract_text() + " "
                    return text
                except ImportError:
                    logger.warning("PyPDF2 not available, cannot read PDF")
                    return ""
            
            elif file_extension in ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            
            else:
                # Try to read as text file
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        return f.read()
                except:
                    return ""
                    
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            return ""
    
    def generate_tags(self, text: str) -> List[str]:
        """Generate intelligent tags based on text content using rule-based approach"""
        if not text.strip():
            return []
        
        try:
            text_lower = text.lower()
            tags = []
            
            # Check each category for keywords
            for category, keywords in self.category_keywords.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        if category not in tags:
                            tags.append(category)
                        break  # Found one keyword for this category, move to next
            
            # Add some basic content-based tags
            if any(word in text_lower for word in ['invoice', 'bill', 'payment', 'financial']):
                if 'Finance' not in tags:
                    tags.append('Finance')
            
            if any(word in text_lower for word in ['report', 'meeting', 'project', 'deadline']):
                if 'Work' not in tags:
                    tags.append('Work')
            
            if any(word in text_lower for word in ['family', 'personal', 'private']):
                if 'Personal' not in tags:
                    tags.append('Personal')
            
            # Limit to top 5 tags
            return tags[:5]
            
        except Exception as e:
            logger.error(f"Error generating tags: {e}")
            return []
    
    def generate_summary(self, text: str) -> str:
        """Generate a concise summary of the text content"""
        if not text.strip():
            return ""
        
        try:
            # Simple rule-based summarization
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) <= 2:
                return text[:200] + "..." if len(text) > 200 else text
            
            # Take first and last sentence, plus any sentence with key terms
            key_terms = ['project', 'report', 'summary', 'conclusion', 'important', 'key']
            important_sentences = []
            
            for sentence in sentences:
                if any(term in sentence.lower() for term in key_terms):
                    important_sentences.append(sentence)
            
            summary_sentences = []
            if sentences:
                summary_sentences.append(sentences[0])  # First sentence
            
            # Add important sentences
            for sentence in important_sentences[:2]:
                if sentence not in summary_sentences:
                    summary_sentences.append(sentence)
            
            if sentences and sentences[-1] not in summary_sentences:
                summary_sentences.append(sentences[-1])  # Last sentence
            
            summary = ". ".join(summary_sentences)
            return summary[:300] + "..." if len(summary) > 300 else summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return text[:200] + "..." if len(text) > 200 else text
    
    def process_file(self, file_path: str) -> Tuple[List[str], str]:
        """Process a file and return tags and summary"""
        try:
            # Extract text from file
            text = self.extract_text_from_file(file_path)
            
            if not text.strip():
                logger.warning(f"No text content extracted from {file_path}")
                return [], ""
            
            # Generate tags and summary
            tags = self.generate_tags(text)
            summary = self.generate_summary(text)
            
            logger.info(f"Processed {file_path}: {len(tags)} tags, summary length: {len(summary)}")
            return tags, summary
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return [], ""

# Global instance
ai_tagger = None

def get_ai_tagger() -> AITaggingSystem:
    """Get or create AI tagging system instance"""
    global ai_tagger
    if ai_tagger is None:
        ai_tagger = AITaggingSystem()
    return ai_tagger

def tag_file_content(file_path: str) -> List[str]:
    """Legacy function for backward compatibility"""
    tagger = get_ai_tagger()
    tags, _ = tagger.process_file(file_path)
    return tags

def process_file_with_ai(file_path: str) -> Dict[str, any]:
    """Process file with AI and return tags and summary"""
    tagger = get_ai_tagger()
    tags, summary = tagger.process_file(file_path)
    
    return {
        "tags": tags,
        "summary": summary,
        "status": "success"
    }
