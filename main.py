from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.config import settings
from app.core import database
import logging

app = FastAPI(
    title="Video Frame Similarity Search API",
    version="1.0.0",
    description="Upload videos, extract frames, compute visual features, and search similar frames"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    try:
        database.init_collection()
        logging.info("Qdrant collection initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize Qdrant collection: {e}")
