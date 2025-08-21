import time
import json
import os
from celery import Celery
from .database import SessionLocal
from . import models

celery = Celery(
    __name__,
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/1"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/2")
)
@celery.task(name="parse_file_task")
def parse_file_task(file_id: str):
    """
    This background task simulates parsing a file by updating its progress
    from 0 to 100 and storing dummy data in the database.
    """
    db = SessionLocal()
    try:
        file_record = db.query(models.File).filter(models.File.id == file_id).first()
        if not file_record:
            print(f"File with ID {file_record} not found.")
            return
        file_record.status = "processing"
        db.commit()
        for i in range(1, 101):
            file_record.progress = i
            db.commit()
            time.sleep(0.05) 
        for i in range(5):
            dummy_data = {"row": i + 1, "content": f"This is parsed line {i+1}."}
            file_row = models.FileRow(file_id=file_id, data=json.dumps(dummy_data))
            db.add(file_row)
        db.commit()
        file_record.status = "ready"
        file_record.progress = 100
        db.commit()

    except Exception as e:
        
        print(f"An error occurred: {e}")
        file_record.status = "failed"
        file_record.progress = 0
        db.commit()
    finally:
        
        db.close()