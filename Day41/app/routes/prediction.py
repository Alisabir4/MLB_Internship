from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import Response
from app.schemas.response import PredictionResponse
from pathlib import Path
import tempfile
import os
import cv2

from app.services.detector import detector


router = APIRouter(prefix="/api", tags=["Prediction"])


ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/jpg"
}


@router.post(
    "/predict",
    response_model=PredictionResponse
)
async def predict(
    file: UploadFile = File(...),
    confidence: float = Query(0.5, ge=0.0, le=1.0)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload JPG, JPEG, or PNG."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    temp_path = None

    try:
        suffix = Path(file.filename or "").suffix.lower()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name

        detections = detector.predict(
            temp_path,
            confidence
        )

        return {
            "detections": detections,
            "total": len(detections)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@router.post("/predict/image")
async def predict_image(
    file: UploadFile = File(...),
    confidence: float = Query(0.5, ge=0.0, le=1.0)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload JPG, JPEG, or PNG."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    temp_path = None

    try:
        suffix = Path(file.filename or "").suffix.lower()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name

        annotated_image = detector.predict_image(
            temp_path,
            confidence
        )

        success, encoded_image = cv2.imencode(
            ".jpg",
            annotated_image
        )

        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to encode processed image."
            )

        return Response(
            content=encoded_image.tobytes(),
            media_type="image/jpeg"
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Image processing failed: {str(e)}"
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)