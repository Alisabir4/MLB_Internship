# 🛡️ Intelligent Security Monitoring System

A real-time AI-based security monitoring application built using **YOLOv8, ByteTrack, OpenCV, and Streamlit**.  
The system detects and tracks people in images and videos, monitors a selected region of interest (ROI), counts entries/exits, calculates occupancy, analyzes stay time, and generates reports.

---

# 📌 Project Overview

The Intelligent Security Monitoring System uses computer vision and deep learning techniques to provide automated surveillance analytics.

The application can:

- Detect people using YOLOv8
- Track individuals using ByteTrack
- Monitor a specific Region of Interest (ROI)
- Count entries and exits
- Calculate current and maximum occupancy
- Analyze person stay duration
- Generate CSV reports
- Save person snapshots
- Process images and videos
- Download processed results

---

# 🚀 Features

## Object Detection

✅ YOLOv8 Nano model  
✅ Real-time person detection  
✅ Confidence threshold tuning  


## Object Tracking

✅ ByteTrack multi-object tracking  
✅ Unique tracking IDs  
✅ Consistent person tracking  


## Security Monitoring

✅ ROI-based monitoring  
✅ Entry detection  
✅ Exit detection  
✅ Occupancy monitoring  
✅ Maximum occupancy calculation  


## Analytics

✅ Stay time analysis  
✅ Event logging  
✅ CSV report generation  
✅ Snapshot saving  


## Application Features

✅ Image support  
✅ Video support  
✅ Live processing preview  
✅ Progress bar  
✅ Adjustable confidence threshold  
✅ Adjustable IoU threshold  
✅ Download processed results  

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| YOLOv8 | Object Detection |
| ByteTrack | Object Tracking |
| OpenCV | Image/Video Processing |
| Streamlit | Web Application |
| Pandas | Data Analysis |
| NumPy | Numerical Processing |
| Ultralytics | YOLO Framework |

---

# 📂 Project Structure


Day35/
│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
│ └── yolov8n.pt
│
├── sample_inputs/
│ ├── test_image.jpg
│ └── test_video.mp4
│
├── sample_outputs/
│ ├── processed_image.jpg
│ ├── processed_video.mp4
│ └── events.csv
│
└── outputs/
└── snapshots/


---

# ⚙ Installation

## 1. Clone Repository

```bash
git clone https://github.com/your_username/your_repository.git

Move into project folder:

cd Day35
2. Create Virtual Environment (Optional)

Create environment:

python -m venv venv

Activate environment:

Windows
venv\Scripts\activate
Linux/Mac
source venv/bin/activate
3. Install Dependencies

Install required packages:

pip install -r requirements.txt
▶️ Running the Application

Start Streamlit application:

streamlit run app.py

The application will open in your browser.

Example:

http://localhost:8501
📖 Usage Guide
Step 1: Upload Input

Upload:

Image (jpg, png, bmp)
Video (mp4, avi, mov, mkv)
Step 2: Adjust Settings

Use sidebar controls:

Confidence Threshold

Controls detection confidence.

Recommended:

0.4 - 0.6
IoU Threshold

Controls overlapping detection removal.

Recommended:

0.4 - 0.5
ROI Monitoring

Enable/disable monitored area.

Snapshot Saving

Enable saving detected person images.

Step 3: Run Detection

The system will:

Detect people
Assign tracking IDs
Monitor ROI
Count entries/exits
Calculate occupancy
Generate analytics
Step 4: Download Results

Available downloads:

Processed image
Processed video
CSV event report
📊 Output Examples

Generated outputs:

outputs/

├── processed_video.mp4

├── processed_image.jpg

├── events.csv

└── snapshots/
      ├── person_1.jpg
      ├── person_2.jpg
⚡ Optimization Techniques Implemented
Model Optimization
Used YOLOv8 Nano model for faster inference
Tunable confidence threshold
Tunable IoU threshold
Application Optimization
Cached YOLO model loading
Optimized OpenCV processing
Modular code structure
Progress monitoring
Error Handling

The application handles:

Invalid files
Missing videos
Unsupported formats
Model loading errors
📈 Future Improvements

Possible enhancements:

Custom ROI selection using mouse
Face recognition integration
Database storage
Real-time CCTV camera support
Cloud deployment
Email/SMS alerts
Multiple camera monitoring
🌐 Deployment
Streamlit Cloud

Deployment steps:

Upload project to GitHub
Connect repository with Streamlit Cloud
Select app.py
Deploy application


📜 License

This project is created for educational and internship purposes.


---

## Also create `requirements.txt`
file:

requirements.txt
streamlit
ultralytics
opencv-python
numpy
pandas
torch
torchvision