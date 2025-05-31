import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MAX_FILE_SIZE_MB: int = 500
    SUPPORTED_FORMATS: tuple = ("mp4", "avi", "mov")
    FRAME_INTERVAL: float = 1.0  # default: every 1 second
    FRAME_DIR: str = "./storage/frames"
    VIDEO_DIR: str = "./storage/videos"
    TEMP_DIR: str = "./storage/temp"
    QDRANT_HOST: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "video_frames"
    VECTOR_DIM: int = 512  # set to 512 to match your feature vector dimension

    class Config:
        env_file = ".env"

settings = Settings()
