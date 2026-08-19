# Day 41 - Custom YOLO Prediction API

## Project Overview

This project integrates a custom YOLO object detection model with FastAPI.

The trained YOLO model (`best.pt`) detects cups and is exposed through REST API endpoints.

The API allows another application to upload an image and receive YOLO prediction results.

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Ultralytics YOLO
- OpenCV
- Pillow
- Pydantic

## Model

The custom YOLO model is stored at:

models/best.pt

The model contains one detection class:

- cup

## API Endpoints

### GET /health

Checks whether the API is running and whether the YOLO model is loaded.

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true,
  "model": "best.pt",
  "classes": {
    "0": "cup"
  }
}


POST /api/predict

Accepts an image and returns YOLO predictions.

Parameters:

file - Image file
confidence - Detection confidence threshold

Example response:

{
  "detections": [
    {
      "class": "cup",
      "confidence": 0.87,
      "bbox": [105.32, 72.41, 387.65, 421.18]
    }
  ],
  "total": 1
}
POST /api/predict/image

Accepts an image, performs YOLO inference, draws bounding boxes, and returns the processed image.

Request Flow

Client → FastAPI → Image Upload → YOLO Model → Inference → JSON/Image Response

Error Handling

The API handles:

Unsupported file types
Empty files
Invalid image input
Prediction errors
Image processing errors
Invalid confidence thresholds
Run Locally

Install dependencies:

pip install -r requirements.txt

Start the server:

uvicorn app.main:app --reload

Open Swagger UI:

http://127.0.0.1:8000/docs

Project Structure
Day41/
├── app/
│   ├── main.py
│   ├── routes/
│   │   └── prediction.py
│   ├── services/
│   │   └── detector.py
│   └── schemas/
│       └── response.py
├── models/
│   └── best.pt
├── sample_images/
├── outputs/
├── requirements.txt
└── README.md
Testing

The API was tested using Swagger UI with:

Valid image
Unsupported file type
Empty file
Image with no detections
Different confidence thresholds