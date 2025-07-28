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
            # Clean and prepare text
            text = text.strip()
            
            # For very short texts, return as is
            if len(text) < 100:
                return text
            
            # Split into sentences
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
            
            if len(sentences) <= 2:
                # For short documents, create a summary
                if len(text) > 150:
                    # Find the most important sentence or create a summary
                    important_terms = ['project', 'report', 'summary', 'overview', 'introduction']
                    for sentence in sentences:
                        if any(term in sentence.lower() for term in important_terms):
                            return sentence + "."
                    
                    # If no important sentence found, take first sentence
                    return sentences[0] + "." if sentences else text[:150] + "..."
                else:
                    return text
            
            # For longer documents, create a proper summary
            summary_sentences = []
            
            # 1. Extract title/topic (usually first sentence)
            if sentences:
                first_sentence = sentences[0]
                # Check if it looks like a title
                if len(first_sentence) < 100 and any(word in first_sentence.lower() for word in ['report', 'document', 'project', 'overview', 'summary', 'analysis']):
                    summary_sentences.append(first_sentence)
            
            # 2. Find sentences with key achievements/results (highest priority)
            achievement_keywords = ['achieved', 'completed', 'implemented', 'successfully', 'result', 'outcome', 'delivered', 'finished', 'accomplished', 'developed', 'created', 'built']
            achievement_sentences = []
            
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in achievement_keywords):
                    achievement_sentences.append(sentence)
            
            # Add up to 2 achievement sentences
            for sentence in achievement_sentences[:2]:
                if sentence not in summary_sentences:
                    summary_sentences.append(sentence)
            
            # 3. Find sentences with key features/capabilities
            feature_keywords = ['feature', 'system', 'technology', 'capability', 'functionality', 'tool', 'platform', 'solution', 'service']
            feature_sentences = []
            
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in feature_keywords):
                    feature_sentences.append(sentence)
            
            # Add up to 1 feature sentence
            for sentence in feature_sentences[:1]:
                if sentence not in summary_sentences:
                    summary_sentences.append(sentence)
            
            # 4. Find sentences with key information/objectives
            info_keywords = ['key', 'important', 'main', 'primary', 'objective', 'goal', 'purpose', 'aim', 'target', 'focus']
            info_sentences = []
            
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in info_keywords):
                    info_sentences.append(sentence)
            
            # Add up to 1 info sentence
            for sentence in info_sentences[:1]:
                if sentence not in summary_sentences:
                    summary_sentences.append(sentence)
            
            # 5. Find status/current state sentences
            status_keywords = ['currently', 'status', 'progress', 'schedule', 'budget', 'ready', 'deployment', 'production']
            status_sentences = []
            
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in status_keywords):
                    status_sentences.append(sentence)
            
            # Add up to 1 status sentence
            for sentence in status_sentences[:1]:
                if sentence not in summary_sentences:
                    summary_sentences.append(sentence)
            
            # 6. If we don't have enough sentences, add the most descriptive one
            if len(summary_sentences) < 2:
                # Find the longest sentence that's not too long and contains important content
                remaining_sentences = [s for s in sentences if s not in summary_sentences]
                if remaining_sentences:
                    # Score sentences based on content importance
                    scored_sentences = []
                    for sentence in remaining_sentences:
                        score = 0
                        # Score based on length (prefer medium length)
                        if 50 <= len(sentence) <= 120:
                            score += 2
                        # Score based on content keywords
                        content_keywords = ['project', 'system', 'development', 'team', 'work', 'implementation']
                        score += sum(1 for keyword in content_keywords if keyword in sentence.lower())
                        scored_sentences.append((sentence, score))
                    
                    # Sort by score and take the best one
                    if scored_sentences:
                        best_sentence = max(scored_sentences, key=lambda x: x[1])[0]
                        if len(best_sentence) < 150:
                            summary_sentences.append(best_sentence)
            
            # 7. Create the final summary
            if summary_sentences:
                summary = ". ".join(summary_sentences)
                
                # Ensure proper ending
                if not summary.endswith('.'):
                    summary += "."
                
                # Limit length and ensure it's meaningful
                if len(summary) > 300:
                    # Try to keep complete sentences
                    sentences_in_summary = summary.split('. ')
                    if len(sentences_in_summary) > 1:
                        # Keep as many complete sentences as possible within limit
                        truncated_summary = ""
                        for sentence in sentences_in_summary:
                            if len(truncated_summary + sentence) < 297:
                                truncated_summary += sentence + ". "
                            else:
                                break
                        summary = truncated_summary.strip()
                        if not summary.endswith('.'):
                            summary += "..."
                    else:
                        summary = summary[:297] + "..."
                
                return summary
            else:
                # Fallback: create a simple summary from first few sentences
                if len(sentences) >= 3:
                    summary = ". ".join(sentences[:3]) + "."
                    return summary[:300] + "..." if len(summary) > 300 else summary
                else:
                    return ". ".join(sentences) + "."
                    
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            # Fallback: return first 200 characters
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
