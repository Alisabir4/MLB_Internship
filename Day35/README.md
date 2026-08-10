# 🎥 Smart Video Analytics System

An AI-powered video analytics application built with **Python, YOLO, OpenCV, and Streamlit**. The system detects and tracks moving objects in recorded videos and provides real-time analytics such as object count, unique objects, FPS, ROI occupancy, entry/exit events, and performance metrics.

## 🚀 Features

* 📤 Upload traffic or people videos
* 🤖 YOLO object detection
* 🎯 Object tracking using ByteTrack
* 🆔 Display tracking IDs
* 🔢 Current object count
* 👥 Unique object count
* ⚡ Real-time FPS calculation
* 📍 Customizable Region of Interest (ROI)
* ➡️ Entry detection
* ⬅️ Exit detection
* 📊 Maximum objects inside ROI
* 📄 Generate `events.csv`
* 🎥 Generate processed output video
* 📥 Download processed video
* 📥 Download event CSV
* ⚙️ 640px and 480px processing resolution
* ⏭️ Frame skipping option
* 📈 Performance testing and analytics summary

## 🛠️ Technologies Used

* Python
* Streamlit
* Ultralytics YOLO
* OpenCV
* ByteTrack
* NumPy
* Pandas

## 📁 Project Structure

```text
Day35/
│
├── app.py
├── requirements.txt
├── README.md
│
├── videos/
│   ├── people.mp4
│   ├── traffic.mp4
│   └── video3.mp4
│
└── outputs/
    ├── events.csv
    └── processed_video.mp4
```

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/Alisabir4/MLB_Internship.git
```

Go to the Day35 directory:

```bash
cd MLB_Internship/Day35
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## 🎬 How to Use

1. Upload a short traffic or people video.
2. Select the processing resolution.
3. Set the confidence threshold.
4. Configure the ROI using the sidebar.
5. Select whether frame skipping should be enabled.
6. Click **Start Video Analytics**.
7. Watch the live detection and tracking.
8. Monitor FPS, current objects, unique objects, entries, and exits.
9. After processing, view the final analytics summary.
10. Download the processed video and `events.csv`.

## 📍 ROI Analytics

The system uses a Region of Interest to determine whether tracked objects enter or leave a specific area.

The application records:

* Current objects inside ROI
* Total entries
* Total exits
* Maximum objects inside ROI

## 📊 Final Analytics

At the end of processing, the application displays:

```text
Total Objects
Total Entries
Total Exits
Maximum Objects in ROI
Average FPS
Processing Time
```

Example:

```text
Total Objects: 18
Total Entries: 12
Total Exits: 9
Maximum Objects in ROI: 7
Average FPS: 24.5
```

*Example values only; actual results depend on the video and processing configuration.*

## ⚡ Performance Testing

The system supports different processing configurations.

Recommended tests:

| Test | Resolution | Frame Skipping |
| ---- | ---------- | -------------- |
| 1    | 640px      | Disabled       |
| 2    | 480px      | Disabled       |
| 3    | 640px      | Every 2 frames |
| 4    | 480px      | Every 2 frames |

For each test, compare:

* Average FPS
* Processing time
* Processed frames
* Skipped frames
* Average inference time

The best configuration can then be selected based on processing speed and detection quality.

## 📄 Events CSV

The application automatically generates:

```text
outputs/events.csv
```

The file contains:

| Field        | Description                |
| ------------ | -------------------------- |
| Frame        | Frame where event occurred |
| Time_Seconds | Event timestamp            |
| Track_ID     | Object tracking ID         |
| Object       | Detected object class      |
| Event        | Entry or Exit              |
| X            | Object center X coordinate |
| Y            | Object center Y coordinate |

## 🎥 Processed Video

The processed video is saved as:

```text
outputs/processed_video.mp4
```

It contains:

* Bounding boxes
* Object classes
* Tracking IDs
* ROI
* FPS
* Object statistics
* Entry/exit information

## 🌐 Deployment

The application can be deployed using **Streamlit Community Cloud**.

Deployment steps:

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Select the GitHub repository.
4. Select `Day35/app.py`.
5. Deploy the application.
6. Test the public URL.

## 📌 Dataset / Videos

The project uses short traffic or people videos of approximately **15–30 seconds**.

Videos can be obtained from:

* Pexels
* Pixabay
* Self-recorded videos

The videos should contain moving objects that pass through the selected ROI so entry and exit events can be detected.

## 🎯 Project Objective

The main objective of this project is to understand and implement:

* Real-time video processing
* Frame-by-frame processing
* FPS measurement
* Inference time
* Frame skipping
* Object detection
* Object tracking
* Tracking IDs
* Object counting
* ROI monitoring
* Entry and exit detection
* Video analytics
* Performance optimization

