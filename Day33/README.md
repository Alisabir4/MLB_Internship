# Intelligent Security Monitoring System

## Problem Statement

Traditional security monitoring requires continuous human attention, making it difficult to accurately monitor people entering and leaving restricted areas. This application automates the monitoring process by detecting, tracking, and recording people's movements within a defined region of interest (ROI). It provides real-time occupancy information, logs security events, and generates a summary after processing the video.

## How Entry and Exit Detection Works

The application uses the YOLOv8 model to detect people in each video frame and assigns a unique tracking ID using object tracking. A fixed Region of Interest (ROI) is defined in the video. When the center point of a tracked person moves inside the ROI, the system records an **Entry** event. When the tracked person leaves the ROI, an **Exit** event is recorded. The application also calculates how long each person remains inside the monitored region.

## How Event Logging is Implemented

Every entry and exit event is stored in an `events.csv` file. Each record contains:

* Tracking ID
* Event Type (Entry/Exit)
* Timestamp

The system also saves a snapshot whenever a new person enters the ROI and generates a processed video with all detections, tracking IDs, and live statistics.

## Biggest Challenge and Solution

The biggest challenge was accurately identifying entry and exit events without counting the same person multiple times. This was solved by using persistent object tracking IDs and maintaining each person's current state (inside or outside the ROI). This approach prevents duplicate event logging and improves counting accuracy.
