# Document Image Enhancement Tool

## Project Overview

The Document Image Enhancement Tool is a Python application built using OpenCV and NumPy. It improves the quality of document images by applying various image processing techniques. The application processes multiple document images automatically and saves the enhanced results for better readability and OCR (Optical Character Recognition).

---

## Objectives

- Load document images.
- Correct the perspective of tilted documents.
- Convert images to grayscale.
- Reduce image noise.
- Enhance brightness and contrast.
- Sharpen the image.
- Save the enhanced output images.

---

## Technologies Used

- Python 3
- OpenCV
- NumPy

---

## Project Structure

```
Document_Image_Enhancement_Tool/
│
├── input/
│   ├── doc1.jpg
│   ├── doc2.jpg
│   ├── ...
│   └── doc10.jpg
│
├── Output/
│
├── Enhancement_Tool.py
│
└── README.md
```

---

## Processing Pipeline

1. Load the document image.
2. Resize the image.
3. Apply Perspective Transformation.
4. Convert the image to Grayscale.
5. Reduce noise using Gaussian Blur.
6. Enhance Brightness and Contrast.
7. Sharpen the image.
8. Save the perspective-corrected image.
9. Save the final enhanced image.

---

## OpenCV Functions Used

| Function | Purpose |
|----------|---------|
| `cv2.imread()` | Load image |
| `cv2.resize()` | Resize image |
| `cv2.getPerspectiveTransform()` | Calculate perspective transformation matrix |
| `cv2.warpPerspective()` | Apply perspective correction |
| `cv2.cvtColor()` | Convert image to grayscale |
| `cv2.GaussianBlur()` | Reduce image noise |
| `cv2.convertScaleAbs()` | Adjust brightness and contrast |
| `cv2.filter2D()` | Sharpen the image |
| `cv2.imwrite()` | Save processed images |

---

## Dataset

- Total Images Used: **10 Document Images**
- Image Types:
  - Forms
  - Printed Documents
  - Application Pages
  - Receipts
  - Notes

---

## Challenge Task

Five tilted document images were processed.

For each document, the following images were generated:

- Original Image
- Perspective Corrected Image
- Final Enhanced Image

---

## Results

The application successfully:

- Corrected document perspective.
- Improved image readability.
- Reduced image noise.
- Enhanced brightness and contrast.
- Sharpened document text.
- Saved processed images automatically.

---

## Challenges Faced

- Selecting suitable points for perspective transformation.
- Handling different document angles.
- Balancing brightness and contrast without affecting text clarity.
- Choosing suitable sharpening values to avoid over-enhancement.

---

## Learning Outcomes

After completing this project, I learned:

- Image Transformation using OpenCV.
- Perspective Transformation.
- Image Enhancement techniques.
- Noise Reduction methods.
- Brightness and Contrast Adjustment.
- Image Sharpening.
- Batch processing multiple images using Python.

---

## Future Improvements

- Automatic document edge detection.
- Automatic perspective correction using contours.
- Adaptive thresholding for better document scanning.
- Graphical User Interface (GUI).
- OCR integration using Tesseract.



