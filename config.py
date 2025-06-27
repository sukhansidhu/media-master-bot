import os
from dotenv import load_dotenv

load_dotenv(".env")

class Config:
    # Telegram API credentials
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    
    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/database.db")
    
    # Other configurations
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 2000000000))  # 2GB
    WORKERS = int(os.getenv("WORKERS", 4))
    ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]
    
    # FFmpeg configuration
    FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")
    
    # Temporary directory for processing
    TEMP_DIR = os.getenv("TEMP_DIR", "data/temp")
