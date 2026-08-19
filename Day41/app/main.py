from fastapi import FastAPI

from app.routes.prediction import router
from app.services.detector import detector


app = FastAPI(
    title="Custom YOLO Prediction API",
    description="FastAPI REST API for custom YOLO cup detection",
    version="1.0.0"
)


app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": detector.model is not None,
        "model": "best.pt",
        "classes": detector.model.names
    }