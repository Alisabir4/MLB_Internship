# Smart Object Tracking System

## Overview

This project is a Smart Object Tracking System built using YOLOv8 and ByteTrack. It allows users to upload a video, detect multiple objects, assign a unique tracking ID to each object, display confidence scores, count unique objects, and save the processed output video.

---

## Features

- Upload a video
- Detect multiple objects using YOLOv8
- Track objects using ByteTrack
- Display object class
- Display confidence score
- Assign a unique tracking ID
- Count total unique objects
- Save processed video
- Download processed video

---

## Technologies Used

- Python
- Streamlit
- OpenCV
- Ultralytics YOLOv8
- ByteTrack

---

## What is Object Tracking?

Object Tracking is the process of detecting an object and continuously following it across multiple video frames while maintaining the same identity using a unique tracking ID.

---

## Difference Between Detection and Tracking

| Object Detection | Object Tracking |
|------------------|-----------------|
| Detects objects in individual frames | Detects and follows objects across frames |
| No unique identity | Assigns a unique ID |
| Works frame-by-frame | Maintains object history |

---

## Tracking Algorithm Used

This project uses **ByteTrack**, one of the tracking algorithms supported by Ultralytics YOLO.

ByteTrack matches detections between consecutive frames and keeps IDs consistent even when objects move through the scene.

---

## Challenges Faced

- Maintaining consistent IDs when objects overlap
- Fast-moving objects
- Occlusion (objects temporarily disappear)
- Motion blur
- Different lighting conditions

---

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## Project Structure

```
Mini_Project/
│
├── app.py
├── requirements.txt
├── README.md
├── sample_videos/
└── output_videos/
```

---

## Output

The application displays:

- Object Class
- Confidence Score
- Tracking ID
- Total Unique Objects
- Processed Video