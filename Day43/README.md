# Day 43 — Production-Ready AI Video Processing API

## Overview

Day 43 focused on improving the existing FastAPI + YOLO video processing API by adding API validation, error handling, structured logging, request/job tracking, and health monitoring.

The goal was to make the AI API more reliable and easier to debug when users provide invalid or unexpected input.

The API now follows this workflow:

```text
Request
   ↓
Validation
   ↓
Job Creation
   ↓
YOLO Processing
   ↓
Logging
   ↓
Response
```

---

## Technologies Used

* Python
* FastAPI
* Uvicorn
* Pydantic / FastAPI validation
* OpenCV
* Ultralytics YOLO
* Python Logging
* Swagger UI
* Background Tasks

---

## Project Structure

```text
Day-43/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   └── video.py
│   │
│   ├── services/
│   │   ├── detector.py
│   │   └── video_processor.py
│   │
│   └── utils/
│       └── file_utils.py
│
├── models/
│   └── best.pt
│
├── uploads/
│
├── outputs/
│
├── logs/
│   └── app.log
│
├── screenshots/
│
├── requirements.txt
│
└── README.md
```

---

# Features

The Day-43 API includes:

* Video upload validation
* Supported video format validation
* Maximum file-size validation
* Empty-file validation
* Confidence threshold validation
* Job ID validation
* Unique request IDs
* Unique job IDs
* Background video processing
* YOLO inference
* Processing progress tracking
* Processing start/end time
* Processing statistics
* Global exception handling
* Request validation error handling
* Structured application logging
* `/health` endpoint
* Processed video download endpoint

---

# API Validation

## 1. Supported File Formats

The API accepts the following video formats:

```text
.mp4
.avi
.mov
.mkv
```

Unsupported formats are rejected.

Example:

```text
test.txt
```

Response:

```json
{
  "success": false,
  "error": "Unsupported video format. Allowed formats: MP4, AVI, MOV, MKV.",
  "request_id": "req_..."
}
```

HTTP status:

```text
415 Unsupported Media Type
```

---

## 2. Maximum File Size

The maximum allowed video size is:

```text
100 MB
```

Files larger than this limit are rejected before processing.

HTTP status:

```text
413 Payload Too Large
```

Example response:

```json
{
  "success": false,
  "error": "Video file is too large. Maximum allowed size is 100 MB.",
  "request_id": "req_..."
}
```

---

## 3. Empty File Validation

The API checks whether an uploaded video contains any data.

If an empty file is submitted:

```json
{
  "success": false,
  "error": "Uploaded video is empty.",
  "request_id": "req_..."
}
```

HTTP status:

```text
400 Bad Request
```

---

## 4. Confidence Threshold Validation

The YOLO confidence threshold must be between:

```text
0.0 and 1.0
```

Example of an invalid value:

```text
1.5
```

The API rejects the request using FastAPI request validation.

HTTP status:

```text
422 Unprocessable Entity
```

Example response:

```json
{
  "success": false,
  "error": "Invalid request data.",
  "request_id": "req_..."
}
```

---

# Request IDs

Every HTTP request receives a unique request ID.

Example:

```text
req_7f82ab91c123
```

The request ID is:

* Added to the API response
* Added to the response header
* Stored with the video job
* Included in application logs

Example:

```json
{
  "success": true,
  "request_id": "req_7f82ab91c123",
  "job_id": "job_a82f91c3d7e1",
  "status": "processing",
  "confidence": 0.4
}
```

This makes it easier to trace a request through the application.

---

# Job IDs

Each uploaded video receives a unique job ID.

Example:

```text
job_a82f91c3d7e1
```

The job can then be monitored using:

```text
GET /video/status/{job_id}
```

---

# Error Handling

The API handles expected and unexpected errors without crashing.

Handled errors include:

* Missing video file
* Missing filename
* Unsupported file format
* Empty file
* File too large
* Invalid confidence value
* Invalid job ID
* Job ID not found
* Corrupted/unsupported video
* Output video not found
* Unexpected application errors

---

# HTTP Status Codes

| Status Code | Purpose                   |
| ----------- | ------------------------- |
| `200`       | Successful request        |
| `400`       | Bad request               |
| `413`       | File is too large         |
| `415`       | Unsupported video format  |
| `422`       | Request validation failed |
| `404`       | Job/result not found      |
| `202`       | Video is still processing |
| `500`       | Internal server error     |

---

# Logging

The API uses Python's logging system.

Logs are stored in:

```text
logs/app.log
```

The application records important events such as:

```text
INFO  - Request started
INFO  - Video upload received
INFO  - Job queued
INFO  - Job started
INFO  - Video processing started
INFO  - Processing completed
WARNING - Unsupported file format
WARNING - Video file too large
WARNING - Request validation failed
ERROR - Video processing failed
ERROR - Unhandled application error
```

Sensitive information is not intentionally stored in the logs.

---

# Processing Information

For each completed video job, the API records processing information including:

* Total frames
* Processed frames
* Total detections
* Average FPS
* Processing time
* Confidence threshold
* Processing start time
* Processing end time

Example:

```json
{
  "statistics": {
    "total_frames": 500,
    "processed_frames": 500,
    "total_detections": 127,
    "average_fps": 3.21,
    "processing_time": 155.9,
    "confidence": 0.4
  }
}
```

---

# API Endpoints

## Root

```text
GET /
```

Returns basic API information.

---

## Health Check

```text
GET /health
```

Example:

```json
{
  "success": true,
  "api_status": "healthy",
  "model_status": "loaded",
  "version": "1.0.0"
}
```

The health endpoint checks:

* API status
* YOLO model status
* Application version

---

## Process Video

```text
POST /video/process
```

Uploads a video and starts YOLO processing in the background.

Parameters:

```text
file
confidence
```

Example confidence:

```text
0.40
```

Example successful response:

```json
{
  "success": true,
  "request_id": "req_123456789abc",
  "job_id": "job_abcdef123456",
  "status": "processing",
  "confidence": 0.4
}
```

---

## Check Video Status

```text
GET /video/status/{job_id}
```

Returns the current processing status.

Possible states:

```text
queued
processing
completed
failed
```

---

## Download Result

```text
GET /video/result/{job_id}
```

Returns the processed video after successful completion.

If processing is still running:

```text
202
```

If the job does not exist:

```text
404
```

---

# Failed Request Examples

## Example 1 — Unsupported File

Request:

```text
POST /video/process
file = test.txt
```

Response:

```json
{
  "success": false,
  "error": "Unsupported video format. Allowed formats: MP4, AVI, MOV, MKV.",
  "request_id": "req_123456789abc"
}
```

Status:

```text
415 Unsupported Media Type
```

---

## Example 2 — Invalid Confidence

Request:

```text
POST /video/process
confidence = 1.5
```

Response:

```json
{
  "success": false,
  "error": "Invalid request data.",
  "request_id": "req_123456789abc"
}
```

Status:

```text
422 Unprocessable Entity
```

---

## Example 3 — Invalid Job ID

Request:

```text
GET /video/status/invalid@job
```

Response:

```json
{
  "success": false,
  "error": "Invalid job ID format.",
  "request_id": "req_123456789abc"
}
```

Status:

```text
400 Bad Request
```

---

# Corrupted Video Handling

A video with a valid extension may still be corrupted or unreadable.

The video processor checks whether OpenCV can open the video.

If the video cannot be opened, processing fails safely and the job status becomes:

```text
failed
```

The API does not expose internal exception details to the user.

The technical error is recorded in:

```text
logs/app.log
```

---

# Testing

The API was tested against multiple invalid-input scenarios.

Testing included:

* Valid video upload
* Unsupported file format
* Empty file
* Large file
* Invalid confidence
* Invalid job ID
* Non-existent job ID
* Corrupted video
* Missing request parameters
* Health endpoint

Swagger UI was used for API testing through:

```text
http://127.0.0.1:8000/docs
```

---

# Thunder Client Testing Note

Thunder Client file-upload testing was limited because file sending in Thunder Client is available only in the paid version.

Therefore, file-upload API testing was performed using FastAPI Swagger UI/browser-based testing.

---

# Running the Project

## 1. Create Virtual Environment

```bash
python -m venv venv
```

## 2. Activate Virtual Environment

Windows:

```powershell
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Start FastAPI

```bash
uvicorn app.main:app --reload
```

## 5. Open Swagger

```text
http://127.0.0.1:8000/docs
```

## 6. Health Check

```text
http://127.0.0.1:8000/health
```

---

# Expected Outcome

The Day-43 project transforms the basic YOLO video API into a more reliable backend service.

The API now follows:

```text
Request
   ↓
Validation
   ↓
Error Handling
   ↓
Job Creation
   ↓
Background Processing
   ↓
YOLO Inference
   ↓
Logging
   ↓
Status / Result
```

The application can handle incorrect input and unexpected situations without crashing.


# Demo Video

A 3–5 minute demonstration video should show:

1. Project structure
2. FastAPI Swagger documentation
3. `/health` endpoint
4. Valid video upload
5. Job ID and request ID
6. Processing status
7. YOLO processed result
8. Invalid confidence test
9. Unsupported file test
10. Application log file

---

# Day-43 Summary

Today I improved the FastAPI + YOLO video processing API by adding validation, error handling, logging, request tracking, job tracking, and health monitoring.

The API is now designed to handle both successful requests and invalid input more reliably instead of assuming that every request will be correct.
