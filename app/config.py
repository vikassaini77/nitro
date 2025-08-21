import os
from datetime import timedelta
APP_NAME = os.getenv("APP_NAME", "File Parser API Pro (PG)")
STORAGE_DIR = os.getenv("STORAGE_DIR", "/app/storage")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
ALGORITHM = "HS256"
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "fileparser")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_URL = os.getenv("REDIS_URL", f"redis://{REDIS_HOST}:6379/0")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", f"redis://{REDIS_HOST}:6379/1")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", f"redis://{REDIS_HOST}:6379/2")

DEMO_USERNAME = os.getenv("DEMO_USERNAME", "admin")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "admin123")

def access_token_expires():
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)