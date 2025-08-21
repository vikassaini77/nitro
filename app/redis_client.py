import redis
from .config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def set_progress(file_id: str, status: str, progress: int):
    r.hset(f"file:{file_id}:progress", mapping={"status": status, "progress": progress})

def get_progress(file_id: str):
    data = r.hgetall(f"file:{file_id}:progress")
    if not data:
        return None
    return {"status": data.get("status", "uploading"), "progress": int(data.get("progress", 0))}