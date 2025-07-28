from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database import Base
from datetime import datetime, timedelta
import uuid

class SharedLink(Base):
    __tablename__ = "shared_links"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("file_metadata.id"))
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
