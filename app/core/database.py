# app/core/database.py
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from app.config import settings
from typing import List, Dict, Union
import uuid
import numpy as np


client = QdrantClient(url=settings.QDRANT_HOST)


def init_collection():
    if not client.collection_exists(settings.QDRANT_COLLECTION):
        client.recreate_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(size=settings.VECTOR_DIM, distance=Distance.COSINE)
        )


def insert_frame_vectors(frame_data: List[Dict]):
    """
    Insert frame feature vectors into Qdrant.
    Each dict in frame_data must contain:
    - vector: np.ndarray or List[float]
    - payload: Dict with metadata (image path, timestamps etc.)
    """
    points = []
    for item in frame_data:
        vector = item["vector"]
        # Ensure vector is a list before inserting
        if hasattr(vector, "tolist"):
            vector_list = vector.tolist()
        else:
            vector_list = vector

        payload = item["payload"]
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector_list,
                payload=payload
            )
        )

    client.upsert(collection_name=settings.QDRANT_COLLECTION, points=points)


def search_similar_frames(query_vector: Union[np.ndarray, List[float]], top_k: int = 5) -> List[Dict]:
    """
    Search for similar frames in Qdrant using the given feature vector.
    """
    if hasattr(query_vector, "tolist"):
        vector = query_vector.tolist()
    else:
        vector = query_vector

    results = client.search(
        collection_name=settings.QDRANT_COLLECTION,
        query_vector=vector,
        limit=top_k
    )

    return [
        {
            "score": hit.score,
            "payload": hit.payload
        }
        for hit in results
    ]
