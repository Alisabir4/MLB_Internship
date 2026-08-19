# Day 41 - FastAPI YOLO Prediction API

## Project Overview
Built an AI-powered REST API using FastAPI and a trained YOLO cup detection model.

## Features
- FastAPI REST API
- YOLO cup detection
- Image upload and prediction
- Confidence scores
- Swagger/OpenAPI documentation
- Render deployment

## API Endpoints

POST /api/predict
- Upload an image and receive cup detection results.

POST /api/predict/image
- Upload an image and receive prediction output.

## Technologies
- Python
- FastAPI
- YOLO / Ultralytics
- Pydantic
- Uvicorn
- Render

## Live API
https://fastapi-day41.onrender.com/docs

## GitHub
https://github.com/Alisabir4/MLB_Internship
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