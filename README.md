# Video Frame Similarity Search API

A FastAPI backend service that allows uploading videos, extracting frame-level color histogram features, storing these vectors in a Qdrant vector database, and performing similarity searches to find visually similar frames.

## Features

- Upload videos in MP4, AVI, or MOV format
- Extract frames at configurable intervals
- Compute 3D HSV color histogram vectors for frames
- Store frame vectors with metadata in Qdrant
- Perform similarity search with cosine distance
- Interactive Swagger UI for API testing
- Health check endpoint

## Tech Stack

- **Python 3.13+**
- **FastAPI** - Modern web framework for building APIs
- **OpenCV (cv2)** - Computer vision library for video processing
- **NumPy** - Numerical computing for array operations
- **Qdrant** - Vector search engine for similarity matching
- **Pydantic** - Data validation and serialization
- **Docker** - For running Qdrant vector database

## Getting Started

### Prerequisites

- Python 3.13 or higher
- Docker and Docker Compose
- `pip` package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ParthSharma30/video-frame-similarity-search.git
   cd video-frame-similarity-search
   ```

2. **Start Qdrant with Docker:**
   
   Using Docker Desktop or Docker CLI, run:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

   Verify Qdrant is running:
   ```bash
   curl http://localhost:6333/health
   ```

3. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate     # On Linux/macOS
   venv\Scripts\activate        # On Windows
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables or edit `config.py`:**
   ```env
   QDRANT_HOST=http://localhost:6333
   QDRANT_COLLECTION=video_frames
   VECTOR_DIM=512
   VIDEO_DIR=./storage/videos
   MAX_FILE_SIZE_MB=500
   ```

6. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

7. **Open your browser at:**
   ```
   http://localhost:8000/docs
   ```

## Docker Setup for Qdrant

### Quick Start with Docker

For running Qdrant, simply use Docker Desktop or Docker CLI:

```bash
# Start Qdrant database
docker run -p 6333:6333 qdrant/qdrant

# In a new terminal, check if Qdrant is healthy
curl http://localhost:6333/health

# To run Qdrant in the background (detached mode)
docker run -d -p 6333:6333 qdrant/qdrant

# To stop the container later, find the container ID and stop it
docker ps
docker stop <container_id>
```

### Qdrant Web UI

Once Qdrant is running, you can access the web interface at:
```
http://localhost:6333/dashboard
```

## API Endpoints

### POST /upload

Upload a video file and extract frame features.

**Form Data:**
- `file`: Video file (mp4, avi, mov)
- `interval` (optional): Frame extraction interval in seconds (default: 1.0)

**Response:**
Message, total frames extracted, and frames processed

### POST /search

Search for visually similar frames by feature vector.

**JSON Body:**
```json
{
  "vector": [/* list of floats, length 512 */],
  "top_k": 5
}
```

**Response:**
List of similar frames with similarity scores and metadata

### GET /health

Check the health status of the service and database connectivity.

## Project Structure

```
VIDEO-FRAME-SIMILE/
├── api/
│   └── routes.py            # FastAPI route definitions
├── core/
│   ├── database.py          # Qdrant client integration
│   ├── feature_extractor.py # Frame feature extraction logic
│   └── video_processor.py   # Video frame extraction utilities
├── models/
│   └── schema.py            # Pydantic request/response schemas
├── storage/
│   ├── frames/              # Extracted frame images
│   └── videos/              # Uploaded video files
├── config.py                # App configuration and constants
├── main.py                  # Application entrypoint
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## How It Works

1. **Video Upload**: Users upload video files through the `/upload` endpoint
2. **Frame Extraction**: The system extracts frames at specified intervals using OpenCV
3. **Feature Extraction**: Each frame is converted to HSV color space and a 3D histogram is computed
4. **Vector Storage**: Frame features are stored as vectors in Qdrant with metadata
5. **Similarity Search**: Users can search for similar frames using vector similarity with cosine distance

## Configuration

The application can be configured through environment variables or by modifying `config.py`:

- `QDRANT_HOST`: Qdrant server URL (default: http://localhost:6333)
- `QDRANT_COLLECTION`: Collection name for storing frame vectors
- `VECTOR_DIM`: Dimension of feature vectors (default: 512)
- `VIDEO_DIR`: Directory for storing uploaded videos (default: ./storage/videos)
- `MAX_FILE_SIZE_MB`: Maximum allowed file size for uploads

## Usage Example

**Prerequisites:** Make sure Qdrant is running with Docker before testing the API.

1. **Start Qdrant:**
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

2. **Upload a video:**
   ```bash
   curl -X POST "http://localhost:8000/upload" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@your_video.mp4" \
        -F "interval=1.0"
   ```

3. **Search for similar frames:**
   ```bash
   curl -X POST "http://localhost:8000/search" \
        -H "accept: application/json" \
        -H "Content-Type: application/json" \
        -d '{
          "vector": [0.1, 0.2, ..., 0.9],
          "top_k": 5
        }'
   ```

## Troubleshooting

### Common Issues

1. **Qdrant Connection Error:**
   - Ensure Docker is running and Qdrant container is active: `docker ps`
   - Check if Qdrant is healthy: `curl http://localhost:6333/health`
   - Restart Qdrant: `docker stop <container_id>` then `docker run -p 6333:6333 qdrant/qdrant`

2. **Port Already in Use:**
   - Check what's using port 6333: `lsof -i :6333` (Linux/macOS) or `netstat -ano | findstr :6333` (Windows)
   - Stop conflicting services or use a different port: `docker run -p 6334:6333 qdrant/qdrant`

3. **Video Upload Issues:**
   - Verify supported formats (MP4, AVI, MOV)
   - Check file size limits in configuration
   - Ensure `storage/videos` directory exists and is writable

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Quality

```bash
# Format code
black app/

# Lint code
flake8 app/
```

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

**Parth Sharma**
- GitHub: [@ParthSharma30](https://github.com/ParthSharma30)
- Email: parth.sharma2022a@vitstudent.ac.in

## Acknowledgments

- Built using FastAPI for high-performance API development
- Powered by Qdrant for efficient vector similarity search
- OpenCV for robust video processing capabilities
- Docker for easy deployment and development setup