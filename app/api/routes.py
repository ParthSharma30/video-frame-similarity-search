# app/api/routes.py
import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import List
from datetime import datetime
from pathlib import Path

from app.core import video_processor, feature_extractor, database
from app.models import schema
from app.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    try:
        database.init_collection()
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")


@router.post("/upload", response_model=schema.VideoUploadResponse)
async def upload_video(
    file: UploadFile = File(...),
    interval: float = Form(default=1.0)
):
    # Validate file format
    if not video_processor.is_supported_format(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file format. Only MP4, AVI, MOV are allowed.")

    # Generate unique video ID
    video_id = Path(file.filename).stem + "_" + datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Ensure video directory exists
    save_dir = Path(settings.VIDEO_DIR)
    save_dir.mkdir(parents=True, exist_ok=True)
    
    save_path = save_dir / f"{video_id}.mp4"

    try:
        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.")

    # Validate size
    if video_processor.get_file_size_mb(str(save_path)) > settings.MAX_FILE_SIZE_MB:
        os.remove(save_path)
        raise HTTPException(status_code=400, detail="File too large. Limit is 500MB.")

    try:
        frames = video_processor.extract_frames(str(save_path), interval)
    except Exception as e:
        os.remove(save_path)
        raise HTTPException(status_code=422, detail=f"Frame extraction failed: {str(e)}")

    # Process frames and compute vectors
    frame_vectors = []
    for image_path, timestamp in frames:
        try:
            vector = feature_extractor.compute_color_histogram(image_path)
            payload = {
                "image_path": image_path,
                "frame_timestamp": timestamp,
                "video_filename": file.filename,
                "upload_timestamp": datetime.utcnow().isoformat()
            }
            frame_vectors.append({
                "vector": vector,
                "payload": payload
            })
        except Exception as e:
            continue  # skip bad frame

    if not frame_vectors:
        raise HTTPException(status_code=500, detail="No valid frames could be processed.")

    try:
        database.insert_frame_vectors(frame_vectors)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database insertion error: {str(e)}")

    return schema.VideoUploadResponse(
        message="Video uploaded and processed successfully",
        total_frames=len(frames),
        processed_frames=len(frame_vectors)
    )


@router.post("/search", response_model=List[schema.SimilarFrameResult])
async def search_similar_frames(query: schema.SimilarityQuery):
    # Validate input vector length
    if len(query.vector) != settings.VECTOR_DIM:
        raise HTTPException(
            status_code=400,
            detail=f"Feature vector must be of length {settings.VECTOR_DIM}, got {len(query.vector)}"
        )

    try:
        results = database.search_similar_frames(query_vector=query.vector, top_k=query.top_k)
        response = []
        for hit in results:
            metadata = hit.get("payload", {})
            response.append(schema.SimilarFrameResult(
                score=hit["score"],
                metadata=schema.FrameMetadata(**metadata)
            ))
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Similarity search failed: {str(e)}")
