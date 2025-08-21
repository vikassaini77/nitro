from typing import List, Any
from pydantic import BaseModel

class FileProgress(BaseModel):
    file_id: str
    status: str
    progress: int

class FileMeta(BaseModel):
    id: str
    filename: str
    status: str
    progress: int
    created_at: str

class FileContent(BaseModel):
    file_id: str
    filename: str
    status: str
    rows: List[Any]

class ListFilesResponse(BaseModel):
    files: List[FileMeta]

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"