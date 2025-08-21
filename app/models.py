import uuid
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from .database import Base

def gen_uuid():
    return str(uuid.uuid4())

class File(Base):
    __tablename__ = "files"
    
    id = Column(String, primary_key=True, default=gen_uuid)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)
    status = Column(String, default="uploading", nullable=False)
    progress = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    rows = relationship("FileRow", back_populates="file", cascade="all, delete-orphan")

class FileRow(Base):
    __tablename__ = "file_rows"
    
    id = Column(String, primary_key=True, default=gen_uuid)
    file_id = Column(String, ForeignKey("files.id"), nullable=False)
    data = Column(Text, nullable=False) 
    
    file = relationship("File", back_populates="rows")