# Day 42 — AI Video Processing API with FastAPI + YOLO

## Overview

Day 42 focuses on extending the FastAPI + YOLO image prediction API into an AI-powered video processing backend.

The API accepts video files, creates a unique job ID, processes the video in the background using YOLO, tracks processing progress, saves the processed video, and provides the final result for download.

## Project Workflow

```text
Client
   │
   ▼
Upload Video
   │
   ▼
Job Created
   │
   ▼
Job ID Returned
   │
   ▼
Background Processing
   │
   ▼
YOLO Frame-by-Frame Detection
   │
   ▼
Draw Bounding Boxes
   │
   ▼
Save Processed Video
   │
   ▼
Processing Completed
   │
   ▼
Download Result

Features
Video file upload
Video format validation
Unique job ID generation
Background video processing
Frame-by-frame YOLO detection
Bounding boxes
Class names
Confidence scores
Frame number display
Processing progress tracking
Processed video generation
Video result download
Processing statistics
Error handling
Swagger/OpenAPI documentation
Technologies Used
Python
FastAPI
Uvicorn
Ultralytics YOLO
OpenCV
Pydantic
Python Multipart
Project Structure
Day-42/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── video.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── detector.py
│   │   └── video_processor.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── file_utils.py
│
├── models/
│   └── best.pt
│
├── uploads/
├── outputs/
├── requirements.txt
├── README.md
└── .gitignore
API Endpoints
1. Process Video
POST /video/process

Uploads a video and starts background processing.

Example response:

{
  "job_id": "21372020661b",
  "status": "processing"
}
2. Check Processing Status
GET /video/status/{job_id}

Returns the current processing status and progress.

Example:

{
  "job_id": "21372020661b",
  "status": "processing",
  "progress": 62
}

When processing is completed:

{
  "job_id": "21372020661b",
  "status": "completed",
  "progress": 100,
  "statistics": {
    "total_frames": 269,
    "processed_frames": 269,
    "total_detections": 0,
    "average_fps": 5.44,
    "processing_time": 49.44
  }
}

Update the detection value above with the final successful detection result if it changes during testing.

3. Download Processed Video
GET /video/result/{job_id}

Returns the processed video after YOLO processing is complete.

If processing is still running:

{
  "detail": "Video is still being processed."
}

HTTP status:

202
Video Processing

The uploaded video is opened using OpenCV.

Each frame is processed individually:

Video
  ↓
Read Frame
  ↓
YOLO Detection
  ↓
Draw Bounding Boxes
  ↓
Add Class + Confidence
  ↓
Add Frame Information
  ↓
Write Frame
  ↓
Next Frame

The final frames are written into a new processed video file.

Background Processing

Video inference can take significantly longer than a normal API request, especially when processing hundreds or thousands of frames.

The API therefore uses FastAPI background tasks.

Instead of waiting for the entire video to finish, the API immediately returns a job ID.