Day 42 — AI Video Processing API with FastAPI + YOLO
Overview

Day 42 focused on extending the previous FastAPI + YOLO image API to support video processing and background tasks.

The API accepts a video, creates a unique job_id, processes the video frame-by-frame using YOLO, tracks progress, saves the processed video, and provides the result for download.

Workflow
Client
  ↓
Upload Video
  ↓
Job ID Created
  ↓
Background Processing
  ↓
YOLO Detection
  ↓
Processed Video
  ↓
Completed
  ↓
Download Result
Features
Video upload and validation
Frame-by-frame YOLO detection
Bounding boxes, class names, and confidence
Frame/progress tracking
Background processing
Unique job IDs
Processed video generation
Processing statistics
Error handling
Swagger API documentation
Technologies
Python
FastAPI
Uvicorn
Ultralytics YOLO
OpenCV
PyTorch
Project Structure
Day42/
├── app/
│   ├── main.py
│   ├── routes/
│   │   └── video.py
│   ├── services/
│   │   ├── detector.py
│   │   └── video_processor.py
│   └── utils/
│       └── file_utils.py
├── models/
│   └── best.pt
├── uploads/
├── outputs/
├── requirements.txt
├── README.md
└── .gitignore
API Endpoints
Process Video
POST /video/process

Example response:

{
  "job_id": "21372020661b",
  "status": "processing"
}
Check Status
GET /video/status/{job_id}

Example:

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
Download Result
GET /video/result/{job_id}

Returns the processed video when processing is complete.

If processing is still running:

{
  "detail": "Video is still being processed."
}
Video Processing

Each frame is processed using YOLO:

Read Frame
   ↓
YOLO Detection
   ↓
Draw Bounding Box
   ↓
Class + Confidence
   ↓
Write Frame
Background Processing

Background processing prevents the API request from waiting for the entire video inference task.

Upload → Job ID → Processing → Status → Completed → Result
Testing

The API was tested using Swagger UI.

Test 1 — Short Cup Video
Status: Completed
Total Frames: 269
Processed Frames: 269
Total Detections: 0
Average FPS: 5.44
Processing Time: 49.44 sec
Test 2 — Longer Video
Status: Completed
Total Frames: [Add Result]
Total Detections: [Add Result]
Average FPS: [Add Result]
Processing Time: [Add Result]
Test 3 — Multiple Object Video
Status: Completed
Total Frames: [Add Result]
Total Detections: [Add Result]
Average FPS: [Add Result]
Processing Time: [Add Result]
Error Handling

The API handles:

Invalid file type
Missing file
Empty video
Corrupted video
Unsupported format
Unknown job ID
Processing failure
Result requested before completion
Problems Faced
Long Processing Time

Video processing takes longer because YOLO processes every frame.

Solution: Implemented background processing and job IDs.

Progress Tracking

The user needs to know the current processing state.

Solution: Added progress tracking based on processed frames.

Result Before Completion

The output video is unavailable while processing.

Solution: The result endpoint returns HTTP 202 until processing completes.

Run Locally

Create and activate the virtual environment:

python -m venv venv
.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Run the API:

uvicorn app.main:app --reload

Swagger:

http://127.0.0.1:8000/docs
Learning Outcomes
FastAPI video uploads
OpenCV video processing
YOLO video inference
Background tasks
Job ID management
Progress tracking
Processed video generation
API error handling
Video-processing performance statistics
