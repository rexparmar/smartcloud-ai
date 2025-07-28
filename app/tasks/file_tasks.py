from celery import shared_task
from app.ai.tagging import process_file_with_ai
from app.database import SessionLocal
from app.model.file import FileMeta
from sqlalchemy.orm import Session
import logging
import os

logger = logging.getLogger(__name__)

def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        logger.error(f"Error creating database session: {e}")
        raise

@shared_task
def process_file_task(file_path: str):
    """Celery task for processing files with AI"""
    return process_file_sync(file_path)

def process_file_sync(file_path: str):
    """Synchronous function for processing files with AI and saving to database"""
    db = None
    try:
        print(f"🚀 Processing file with AI at {file_path}")
        
        # Process file with AI
        result = process_file_with_ai(file_path)
        
        if result["status"] == "success":
            tags = result["tags"]
            summary = result["summary"]
            
            print(f"🏷️ AI Tags: {', '.join(tags)}")
            print(f"📝 AI Summary: {summary[:100]}...")
            
            # Save to database
            db = get_db()
            
            # Find the file in database by path
            file_metadata = db.query(FileMeta).filter(FileMeta.file_path == file_path).first()
            
            if file_metadata:
                # Update with AI results
                file_metadata.ai_tags = ", ".join(tags) if tags else None
                file_metadata.summary = summary if summary else None
                db.commit()
                
                logger.info(f"File processed and saved to database: {file_path}")
                print(f"✅ AI results saved to database")
                
                return {
                    "status": "success", 
                    "tags": tags, 
                    "summary": summary,
                    "file_id": file_metadata.id
                }
            else:
                logger.warning(f"File metadata not found in database: {file_path}")
                return {
                    "status": "warning", 
                    "message": "File metadata not found in database",
                    "tags": tags, 
                    "summary": summary
                }
        else:
            logger.error(f"AI processing failed for {file_path}")
            return {"status": "error", "message": "AI processing failed"}
            
    except Exception as e:
        error_msg = f"Error processing file {file_path}: {str(e)}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        return {"status": "error", "error": str(e)}
    finally:
        if db:
            db.close()

def update_file_metadata_with_ai(file_id: int, file_path: str):
    """Update specific file metadata with AI results"""
    db = None
    try:
        print(f"🔄 Updating file metadata with AI for file ID: {file_id}")
        
        # Process file with AI
        result = process_file_with_ai(file_path)
        
        if result["status"] == "success":
            tags = result["tags"]
            summary = result["summary"]
            
            # Update database
            db = get_db()
            file_metadata = db.query(FileMeta).filter(FileMeta.id == file_id).first()
            
            if file_metadata:
                file_metadata.ai_tags = ", ".join(tags) if tags else None
                file_metadata.summary = summary if summary else None
                db.commit()
                
                logger.info(f"Updated file metadata with AI results: {file_id}")
                return {
                    "status": "success",
                    "tags": tags,
                    "summary": summary
                }
            else:
                logger.error(f"File metadata not found: {file_id}")
                return {"status": "error", "message": "File not found"}
        else:
            return {"status": "error", "message": "AI processing failed"}
            
    except Exception as e:
        logger.error(f"Error updating file metadata: {e}")
        return {"status": "error", "error": str(e)}
    finally:
        if db:
            db.close()
