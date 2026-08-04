# 🚗 Vehicle Counting System using YOLOv8

A Streamlit-based Computer Vision application that detects, tracks, and counts vehicles in traffic videos using YOLOv8 object tracking.

---

## 📌 Features

- Upload traffic videos
- Detect Cars and Trucks using YOLOv8
- Track vehicles with unique IDs
- Draw a virtual counting line
- Count vehicles crossing the line
- Prevent duplicate counting using tracking IDs
- Display live vehicle statistics
- Save the processed video
- Download the processed video

---

## 🛠 Technologies Used

- Python
- Streamlit
- YOLOv8 (Ultralytics)
- OpenCV
- NumPy

---

## 📂 Project Structure

```text
Day31/
│
├── app.py
├── vehicle_counter.py
├── yolov8n.pt
├── requirements.txt
├── README.md
│
├── input/
│   └── traffic.mp4
│
└── output/
    └── counted_video.mp4
```

---

## ▶ Installation

Clone the repository

```bash
git clone <repository-url>
```

Go to the project folder

```bash
cd Day31
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 🚘 Supported Vehicle Classes

- Car
- Truck

---

## 📊 Output

The application displays:

- Bounding boxes
- Tracking IDs
- Counting line
- Car count
- Truck count
- Total vehicle count
- Processed video download

---

## 🎯 Learning Outcomes

- Object Detection
- Multi-Object Tracking
- Vehicle Counting
- Tracking IDs
- Region of Interest (ROI)
- Counting Line Concept
- Streamlit Deployment

---

## 📷 Sample Workflow

```text
Upload Video
      │
      ▼
YOLO Detection
      │
      ▼
Object Tracking
      │
      ▼
Vehicle Classification
      │
      ▼
Counting Line
      │
      ▼
Vehicle Count
      │
      ▼
Processed Video
```


