# 🛡️ Intelligent Security Monitoring System

## Overview

The Intelligent Security Monitoring System is a computer vision application developed using **YOLOv8**, **OpenCV**, and **Streamlit**. It monitors surveillance videos by detecting and tracking people, identifies when they enter or leave a predefined monitoring region, records security events, captures entry snapshots, and generates a detailed summary after processing.

---

## Features

* Upload surveillance videos
* Detect and track people using YOLOv8
* Monitor a predefined Region of Interest (ROI)
* Detect entry and exit events
* Display current people inside the region
* Count total entries and exits
* Calculate maximum occupancy
* Measure how long each person stays inside the region
* Capture a snapshot whenever a new person enters
* Save all events in a CSV file
* Save the processed output video with overlays
* Download the processed video and event log

---

## Technologies Used

* Python
* Streamlit
* YOLOv8 (Ultralytics)
* OpenCV
* NumPy
* Pandas

---

## Project Structure

```text
Day33/
│── app.py
│── requirements.txt
│── README.md
│── input_videos/
│── outputs/
│   ├── processed_video.mp4
│   ├── events.csv
│   └── snapshots/
```

---

## Problem Statement

Traditional security monitoring requires continuous human observation, making it difficult to accurately monitor entry and exit activities. This application automates surveillance by detecting and tracking people, monitoring a defined region, recording events, and generating useful security statistics.

---

## How Entry and Exit Detection Works

The application uses YOLOv8 to detect people in every video frame. Each detected person is assigned a unique tracking ID through object tracking. A predefined Region of Interest (ROI) is used for monitoring. When the center point of a tracked person enters the ROI, an **Entry** event is recorded. When the person leaves the ROI, an **Exit** event is logged. The application also measures how long each tracked person stays inside the monitored region.

---

## Event Logging

Every detected event is stored in an **events.csv** file containing:

* Tracking ID
* Event Type (Entry/Exit)
* Timestamp

The system also saves a snapshot whenever a person enters the ROI for the first time.

---

## Output Summary

After processing the video, the application displays:

* Total Entries
* Total Exits
* Current Occupancy
* Maximum Occupancy
* Average Time Spent Inside the Region

---

## Biggest Challenge

The biggest challenge was preventing duplicate entry and exit events while tracking the same person across multiple frames. This was solved by maintaining a unique tracking ID and tracking each person's state (inside or outside the ROI). This ensured accurate counting and reliable event logging.

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run app.py
```

---

## Deployment

The application can be deployed on:

* Streamlit Community Cloud
* Hugging Face Spaces

---

## Deliverables

* Complete Source Code
* Streamlit Application
* requirements.txt
* README.md
* Sample Input Videos
* Processed Output Videos
* Event Log (events.csv)
* GitHub Repository
* Streamlit Deployment URL
* Demo Video


