from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from app.database import Base, engine
from app.auth import auth_routes
from app.auth.dependencies import get_current_user
from app.model.user import User
from fastapi.responses import JSONResponse, FileResponse
from app.model.file import FileMeta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.model.share import SharedLink
from datetime import datetime, timedelta
import uuid
from app.tasks.file_tasks import process_file_task, process_file_sync
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure upload folder exists
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  
        "http://localhost:3001",  
        "https://*.vercel.app", 
        "https://*.vercel.com",   
        "https://v0-frontend-for-api-endpoints-rosy.vercel.app",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_folder = os.path.join(UPLOAD_DIR, str(user.id))
    os.makedirs(user_folder, exist_ok=True)

    file_path = os.path.join(user_folder, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    metadata = FileMeta(
        file_name=file.filename,
        file_path=file_path,
        mime_type=file.content_type,
        file_size=os.path.getsize(file_path),
        owner_id=user.id
    )

    db.add(metadata)
    db.commit()
    
    # Handle Celery task with error handling
    try:
        process_file_task.delay(file_path)
        logger.info(f"File processing task queued for {file_path}")
    except Exception as e:
        logger.error(f"Failed to queue file processing task: {e}")
        # Fallback to synchronous processing
        logger.info("Falling back to synchronous processing")
        result = process_file_sync(file_path)
        logger.info(f"Synchronous processing result: {result}")

    return {
        "message": f"File uploaded for user {user.email}",
        "path": file_path,
        "id": metadata.id
    }



@app.get("/files")
async def list_user_files(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    files = db.query(FileMeta).filter(FileMeta.owner_id == user.id).all()

    return [
        {
            "id": f.id,
            "filename": f.file_name,
            "size": f.file_size,
            "path": f.file_path,
            "mime_type": f.mime_type,
            "uploaded_at": f.upload_date.isoformat(),
            "ai_tags": f.ai_tags.split(", ") if f.ai_tags else [],
            "summary": f.summary
        }
        for f in files
    ]

@app.get("/download/{file_id}")
def download_file(
    file_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file = db.query(FileMeta).filter(FileMeta.id == file_id).first()
    if not file or file.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return FileResponse(
        path=file.file_path,
        filename=file.file_name,
        media_type=file.mime_type
    )

@app.post("/share/{file_id}")
def create_share_link(
    file_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file = db.query(FileMeta).filter(FileMeta.id == file_id).first()
    if not file or file.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=1)  # 1 day link

    link = SharedLink(file_id=file_id, token=token, expires_at=expires_at)
    db.add(link)
    db.commit()

    return {"shareable_link": f"http://localhost:8000/share/{token}"}

@app.get("/share/{token}")
def access_shared_file(token: str, db: Session = Depends(get_db)):
    link = db.query(SharedLink).filter(SharedLink.token == token).first()
    if not link or link.expires_at < datetime.utcnow():
        raise HTTPException(status_code=404, detail="Link expired or invalid")

    file = db.query(FileMeta).filter(FileMeta.id == link.file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file.file_path,
        filename=file.file_name,
        media_type=file.mime_type
    )


@app.get("/files/{file_id}")
async def get_file_details(
    file_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific file including AI results"""
    file = db.query(FileMeta).filter(FileMeta.id == file_id, FileMeta.owner_id == user.id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {
        "id": file.id,
        "filename": file.file_name,
        "size": file.file_size,
        "path": file.file_path,
        "mime_type": file.mime_type,
        "uploaded_at": file.upload_date.isoformat(),
        "ai_tags": file.ai_tags.split(", ") if file.ai_tags else [],
        "summary": file.summary
    }

@app.post("/files/{file_id}/process-ai")
async def process_file_with_ai_endpoint(
    file_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Manually trigger AI processing for a specific file"""
    file = db.query(FileMeta).filter(FileMeta.id == file_id, FileMeta.owner_id == user.id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Import here to avoid circular imports
    from app.tasks.file_tasks import update_file_metadata_with_ai
    
    try:
        result = update_file_metadata_with_ai(file_id, file.file_path)
        
        if result["status"] == "success":
            return {
                "message": "AI processing completed successfully",
                "tags": result["tags"],
                "summary": result["summary"]
            }
        else:
            raise HTTPException(status_code=500, detail=f"AI processing failed: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"Error processing file with AI: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during AI processing")

@app.get("/files/search")
async def search_files(
    query: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search files by AI tags, summary, or filename"""
    files = db.query(FileMeta).filter(FileMeta.owner_id == user.id).all()
    
    results = []
    query_lower = query.lower()
    
    for file in files:
        # Search in filename
        if query_lower in file.file_name.lower():
            results.append(file)
            continue
            
        # Search in AI tags
        if file.ai_tags and query_lower in file.ai_tags.lower():
            results.append(file)
            continue
            
        # Search in summary
        if file.summary and query_lower in file.summary.lower():
            results.append(file)
            continue
    
    return [
        {
            "id": f.id,
            "filename": f.file_name,
            "size": f.file_size,
            "path": f.file_path,
            "mime_type": f.mime_type,
            "uploaded_at": f.upload_date.isoformat(),
            "ai_tags": f.ai_tags.split(", ") if f.ai_tags else [],
            "summary": f.summary
        }
        for f in results
    ]

@app.delete("/files/{file_id}")
async def delete_file(
    file_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a file and its metadata"""
    try:
        # Find the file in database
        file_metadata = db.query(FileMeta).filter(
            FileMeta.id == file_id, 
            FileMeta.owner_id == user.id
        ).first()
        
        if not file_metadata:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Get file path for physical deletion
        file_path = file_metadata.file_path
        
        # First, delete any shared links for this file (to avoid foreign key constraint)
        shared_links = db.query(SharedLink).filter(SharedLink.file_id == file_id).all()
        for link in shared_links:
            db.delete(link)
        db.commit()
        
        # Now delete the file metadata
        db.delete(file_metadata)
        db.commit()
        
        # Delete physical file if it exists
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Physical file deleted: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to delete physical file {file_path}: {e}")
                # Don't fail the request if physical deletion fails
        
        logger.info(f"File {file_id} deleted for user {user.email}")
        
        return {
            "message": "File deleted successfully",
            "file_id": file_id,
            "filename": file_metadata.file_name
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting file {file_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/files/{file_id}/query")
async def query_file(
    file_id: int,
    prompt: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Query a specific file with AI - ask questions about the file content"""
    file = db.query(FileMeta).filter(FileMeta.id == file_id, FileMeta.owner_id == user.id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Import the query system
        from app.ai.query import query_file_with_ai
        
        # Query the file with AI
        result = query_file_with_ai(file.file_path, prompt)
        
        if result["status"] == "success":
            return {
                "file_id": file_id,
                "filename": file.file_name,
                "user_prompt": prompt,
                "ai_answer": result["answer"],
                "status": "success"
            }
        else:
            raise HTTPException(status_code=500, detail=f"AI query failed: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"Error querying file with AI: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during AI query")

# Create tables (users table etc.)
Base.metadata.create_all(bind=engine)

# Mount the auth routes (including /login and /signup)
app.include_router(auth_routes.router)
