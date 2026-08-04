# 🚗 Smart Vehicle Counting System using YOLOv8

A Computer Vision application that detects, tracks, and counts vehicles in traffic videos.

Built using YOLOv8, ByteTrack, OpenCV, and Streamlit.

---

# Features

✅ Upload traffic videos  
✅ Vehicle detection  
✅ Multi-object tracking  
✅ Unique tracking IDs  
✅ Counting line detection  
✅ Avoid duplicate counting  
✅ Live vehicle statistics  
✅ Processed video saving  
✅ Download processed output  

---

# Vehicle Classes

The system detects:

- 🚗 Cars
- 🏍 Motorcycles
- 🚌 Buses
- 🚚 Trucks

---

# Technologies Used

- Python
- YOLOv8
- Ultralytics
- OpenCV
- Streamlit
- ByteTrack

---

# Project Structure

```
Day31/

├── app.py
├── vehicle_counter.py
├── yolov8n.pt
├── requirements.txt
└── README.md
```

---

# Installation

Clone repository:

```bash
git clone <repository-url>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
streamlit run app.py
```

---

# Workflow

```
Input Video

      ↓

YOLOv8 Detection

      ↓

ByteTrack Tracking

      ↓

Vehicle ID Assignment

      ↓

Counting Line

      ↓

Vehicle Count

      ↓

Processed Video
```

---

# Output

The application displays:

- Bounding boxes
- Vehicle labels
- Tracking IDs
- Live vehicle counts
- Saved processed video


---

# Deployment

Deployed using Streamlit Community Cloud.

---
