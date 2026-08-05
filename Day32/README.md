# 👥 Smart People Counting System

A Computer Vision application built using YOLOv8 and Streamlit that detects, tracks, and counts people in images and videos.

## Features

- Upload Image
- Upload Video
- People Detection using YOLOv8
- Person Tracking using ByteTrack
- Live People Counting
- Peak Occupancy Detection
- Bounding Boxes
- Confidence Scores
- Download Processed Image
- Download Processed Video
- Streamlit Web Interface

## Technologies

- Python
- OpenCV
- Ultralytics YOLOv8
- Streamlit
- ByteTrack

## Installation

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

## Project Structure

```
Day32/
│
├── app.py
├── people_counter.py
├── requirements.txt
├── README.md
├── yolov8n.pt
│
├── uploads/
└── outputs/
```

## Dataset

Use videos containing people from:

- Pexels
- Pixabay
- Shopping Mall
- Classroom
- Office
- Public Street

## Output

- Live People Detection
- Current People Count
- Peak Occupancy
- Processed Image
- Processed Video

