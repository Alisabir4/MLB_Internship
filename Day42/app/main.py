from fastapi import FastAPI

from app.routes.video import router as video_router


app = FastAPI(
    title="AI Video Processing API",
    description="FastAPI backend for YOLO-based video processing with background jobs.",
    version="1.0.0",
)


app.include_router(video_router)


@app.get("/")
async def root():
    return {
        "message": "AI Video Processing API is running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }