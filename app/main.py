from fastapi import FastAPI, UploadFile, File, Depends
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
from app.tasks.file_tasks import process_file_task
# Ensure upload folder exists
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()
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
    
    process_file_task.delay(file_path)

    return {
        "message": f"File uploaded for user {user.email}",
        "path": file_path
    }



@app.get("/files")
async def list_user_files(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    files = db.query(FileMeta).filter(FileMeta.owner_id == user.id).all()

    return [
        {
            "filename": f.file_name,
            "size": f.file_size,
            "path": f.file_path,
            "mime_type": f.mime_type,
            "uploaded_at": f.upload_date.isoformat()
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


# Create tables (users table etc.)
Base.metadata.create_all(bind=engine)

# Mount the auth routes (including /login and /signup)
app.include_router(auth_routes.router)
