import os, json, asyncio
from fastapi import FastAPI, UploadFile, File as UploadFileType, HTTPException, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import Form
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from . import models, schemas
from .config import STORAGE_DIR, APP_NAME
from .security import authenticate_user, create_access_token, get_current_user
from .utils import save_stream_to_disk
from .tasks import parse_file_task
from .redis_client import get_progress

os.makedirs(STORAGE_DIR, exist_ok=True)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME, version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/auth/token", response_model=schemas.Token)
def login(username: str = Form(...), password: str = Form(...)):
    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/files", response_model=schemas.FileProgress, status_code=201)
async def upload_file(file: UploadFile = UploadFileType(...), db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    f = models.File(filename=file.filename, path="", status="uploading", progress=0)
    db.add(f); db.commit(); db.refresh(f)

    src = file.file
    try:
        src.seek(0, os.SEEK_END); total_size = src.tell(); src.seek(0)
    except Exception:
        total_size = 0

    dst_path = os.path.join(STORAGE_DIR, f"{f.id}_{file.filename}")
    f.path = dst_path; db.add(f); db.commit()

    save_stream_to_disk(src, dst_path, total_size, db, f.id)
    parse_file_task.delay(f.id)

    return {"file_id": f.id, "status": f.status, "progress": f.progress}

@app.get("/files/{file_id}/progress", response_model=schemas.FileProgress)
def get_progress_api(file_id: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    f = db.query(models.File).filter(models.File.id == file_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="File not found")
    red = get_progress(file_id) or {"status": f.status, "progress": f.progress}
    return {"file_id": f.id, "status": red["status"], "progress": red["progress"]}

@app.get("/files/{file_id}", response_model=schemas.FileContent)
def get_file_content(file_id: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    f = db.query(models.File).filter(models.File.id == file_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="File not found")
    if f.status != "ready":
        return JSONResponse(status_code=202, content={"message": "File upload or processing in progress. Please try again later."})
    rows = db.query(models.FileRow).filter(models.FileRow.file_id == file_id).limit(10000).all()
    data = [json.loads(r.data) for r in rows]
    return {"file_id": f.id, "filename": f.filename, "status": f.status, "rows": data}

@app.get("/files", response_model=schemas.ListFilesResponse)
def list_files(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    files = db.query(models.File).order_by(models.File.created_at.desc()).all()
    return {"files": [{
        "id": f.id, "filename": f.filename, "status": f.status,
        "progress": f.progress, "created_at": f.created_at.isoformat() + "Z"
    } for f in files]}

@app.delete("/files/{file_id}", status_code=204)
def delete_file(file_id: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    f = db.query(models.File).filter(models.File.id == file_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="File not found")
    db.query(models.FileRow).filter(models.FileRow.file_id == file_id).delete()
    try:
        if os.path.exists(f.path): os.remove(f.path)
    except Exception: pass
    db.delete(f); db.commit()
    return JSONResponse(status_code=204, content=None)

@app.websocket("/ws/files/{file_id}/progress")
async def ws_progress(websocket, file_id: str):
    await websocket.accept()
    try:
        while True:
            pr = get_progress(file_id) or {"status": "unknown", "progress": 0}
            await websocket.send_json({"file_id": file_id, **pr})
            if pr["status"] in ("ready", "failed"):
                break
            await asyncio.sleep(1)
    finally:
        await websocket.close()

@app.get("/sse/files/{file_id}/progress")
async def sse_progress(file_id: str):
    async def event_gen():
        while True:
            pr = get_progress(file_id) or {"status": "unknown", "progress": 0}
            yield f"data: {json.dumps({'file_id': file_id, **pr})}\n\n"
            if pr["status"] in ("ready", "failed"):
                break
            await asyncio.sleep(1)
    return StreamingResponse(event_gen(), media_type="text/event-stream")