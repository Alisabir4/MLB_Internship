# Document & Object Segmentation Tool

## What is Image Segmentation?

Image Segmentation is a computer vision technique that divides an image into meaningful regions by grouping pixels with similar characteristics. Unlike object detection, which only locates an object using a bounding box, image segmentation identifies the exact pixels belonging to the object, making it useful for applications such as document scanning, medical imaging, autonomous vehicles, agriculture, and image editing.

---

## Difference Between Binary, Adaptive, and Otsu Thresholding

### Binary Thresholding

Binary Thresholding uses a fixed threshold value to separate the foreground from the background. Pixels with intensity greater than the threshold become white, while the remaining pixels become black. It works well when the image has uniform lighting but performs poorly under shadows or uneven illumination.

### Adaptive Thresholding

Adaptive Thresholding calculates a different threshold for each small region of the image instead of using a single global value. This makes it much more effective for images with varying lighting conditions, shadows, or non-uniform backgrounds.

### Otsu Thresholding

Otsu Thresholding automatically determines the optimal threshold value by analysing the image histogram. It is useful when the image contains two distinct intensity groups and removes the need to manually choose a threshold value.

---

## Best Method for My Dataset

For my dataset, **Adaptive Thresholding** produced the best overall results. Since the dataset included documents, simple objects, images with uneven lighting, and shadows, Adaptive Thresholding handled local brightness variations much better than Binary Thresholding. Otsu Thresholding also performed well on clear images with good contrast, but Adaptive Thresholding provided more consistent segmentation across different image conditions.

---

## Challenges Faced During Implementation

* Selecting threshold values that worked well for different types of images.
* Handling images with shadows and uneven lighting.
* Ensuring foreground objects were clearly separated from the background.
* Saving and downloading processed images correctly in the Streamlit application.
* Comparing the results of different segmentation techniques to identify the most suitable method for each image.

---

## Technologies Used

* Python
* OpenCV
* Streamlit
* NumPy
* Pillow


## Overview
A Streamlit application that performs image segmentation using OpenCV thresholding techniques.

## Features
- Upload image
- Binary Thresholding
- Adaptive Thresholding
- Otsu Thresholding
- Foreground Segmentation
- Download processed image

## Technologies
- Python
- OpenCV
- Streamlit
- NumPy
- Pillow

## Dataset
15 sample images including:
- Documents
- Objects
- Uneven lighting
- Shadow images

## Installation

pip install -r requirements.txt

streamlit run app.py