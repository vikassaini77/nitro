import json, os, time
from sqlalchemy.orm import Session
from . import models
from .redis_client import set_progress

CHUNK_SIZE = 1024 * 1024  # 1MB

def db_update_progress(db: Session, file_id: str, progress: int | None = None, status: str | None = None):
    f = db.query(models.File).filter(models.File.id == file_id).first()
    if not f:
        return
    if progress is not None:
        f.progress = max(0, min(progress, 100))
    if status is not None:
        f.status = status
    db.add(f)
    db.commit()
    set_progress(file_id, f.status, f.progress)

def save_stream_to_disk(src_file, dst_path: str, total_size: int, db: Session, file_id: str) -> int:
    written = 0
    with open(dst_path, "wb") as out:
        while True:
            chunk = src_file.read(CHUNK_SIZE)
            if not chunk:
                break
            out.write(chunk)
            written += len(chunk)
            if total_size > 0:
                pct = int((written / total_size) * 60)
                db_update_progress(db, file_id, progress=pct, status="uploading")
    return written

def parse_file_to_rows(path: str):
    import pandas as pd
    name = os.path.basename(path).lower()
    if name.endswith(".csv"):
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            yield json.dumps(row.to_dict(), ensure_ascii=False)
    elif name.endswith(".xlsx") or name.endswith(".xls"):
        df = pd.read_excel(path)
        for _, row in df.iterrows():
            yield json.dumps(row.to_dict(), ensure_ascii=False)
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                yield json.dumps({"line": line.rstrip("\n")}, ensure_ascii=False)

def simulate_processing_delay():
    time.sleep(0.02)