# Image Feature Matching System

## What are Image Features?

Image features are distinctive points or patterns in an image that help identify and compare objects. Common image features include corners, edges, blobs, and textured regions. These features are used in computer vision tasks such as object recognition, image stitching, image alignment, augmented reality, and visual localization.

---

## Difference Between Harris Corner Detection and ORB

| Harris Corner Detection | ORB (Oriented FAST and Rotated BRIEF) |
|--------------------------|----------------------------------------|
| Detects only corners. | Detects keypoints and computes descriptors. |
| Fast and simple. | Fast and suitable for real-time applications. |
| Does not support feature matching. | Supports feature matching. |
| Not scale or rotation invariant. | Rotation invariant and partially scale invariant. |
| Used mainly for corner detection. | Used for object recognition, image matching, and panorama stitching. |

---

## How Feature Matching Works

Feature matching is the process of finding corresponding keypoints between two images. First, ORB detects keypoints and computes descriptors for each image. Then, a Brute Force Matcher compares the descriptors from both images and finds the best matching pairs based on their similarity. Finally, the matched keypoints are drawn to visualize the correspondence between the two images.

---

## Best Matching Results

Among the 10 image pairs tested, the **Burj Khalifa image pair** produced the best matching results. The building contains many unique edges, corners, and repetitive window patterns, allowing ORB to detect a large number of stable keypoints. Since both images were captured from similar viewpoints with sufficient overlap, the Brute Force Matcher found a high number of accurate matches, resulting in reliable feature matching.

## Overview

This application compares two images using ORB Feature Detection and Brute Force Matcher.

## Features

- Upload two images
- Detect ORB keypoints
- Match image features
- Display matched keypoints
- Show number of detected keypoints
- Show number of good matches

## Technologies

- Python
- OpenCV
- Streamlit
- NumPy

## Dataset

10 image pairs including:

- Buildings
- Landmarks
- Logos
- Product Images
- Book Covers

## Run

```bash
streamlit run app.py
```