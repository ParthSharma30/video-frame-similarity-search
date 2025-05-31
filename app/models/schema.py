# app/models/schema.py
from pydantic import BaseModel, Field, validator
from typing import List


class VideoUploadResponse(BaseModel):
    message: str
    total_frames: int
    processed_frames: int


class FrameMetadata(BaseModel):
    image_path: str
    frame_timestamp: float
    video_filename: str
    upload_timestamp: str


class SimilarFrameResult(BaseModel):
    score: float
    metadata: FrameMetadata


class SimilarityQuery(BaseModel):
    vector: List[float] = Field(..., description="Feature vector to query against")
    top_k: int = Field(5, ge=1, le=100, description="Number of similar frames to return")

    @validator("vector")
    def validate_vector(cls, v):
        if len(v) != 512:
            raise ValueError("Feature vector must be of the correct dimension (512)")
        return v
