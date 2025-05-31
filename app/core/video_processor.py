import cv2
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from app.config import settings


def is_supported_format(filename: str) -> bool:
    ext = filename.lower().split(".")[-1]
    return ext in settings.SUPPORTED_FORMATS


def get_file_size_mb(file_path: str) -> float:
    return os.path.getsize(file_path) / (1024 * 1024)


def extract_frames(video_path: str, interval: float) -> List[Tuple[str, float]]:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Cannot open video file.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    frame_interval = max(1, int(interval * fps))

    extracted_frames = []
    frame_count = 0

    output_dir = Path(settings.FRAME_DIR) / Path(video_path).stem
    output_dir.mkdir(parents=True, exist_ok=True)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            timestamp = frame_count / fps
            frame_filename = output_dir / f"frame_{frame_count}.jpg"
            cv2.imwrite(str(frame_filename), frame)
            extracted_frames.append((str(frame_filename), timestamp))

        frame_count += 1

    cap.release()
    return extracted_frames
