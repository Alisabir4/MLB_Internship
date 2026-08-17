# 🥤 Day 39 - Custom Cup Detection

## Project Overview

This project is a complete Computer Vision application for detecting cups using a custom-trained YOLOv8 model.

The original dataset contained black and white cup classes. For this project, both classes were converted into a single class:

- `0 = cup`

This allows the model to detect cups regardless of their color.

---

## 🎯 Objective

The goal of Day 39 was to build an end-to-end Computer Vision pipeline:

Dataset → Training → Model → Inference → Error Analysis → Application

The final application allows users to upload images and run cup detection using the trained YOLO model.

---

## 📊 Dataset

A custom cup dataset was used for training.

### Classes

| Class ID | Class |
|---|---|
| 0 | cup |

The original black and white labels were converted into the single `cup` class.

### Image Size

Training image size:

**640 × 640**

---

## 🤖 Model

The model used was:

**YOLOv8n**

Training configuration:

- Epochs: 20
- Batch size: 16
- Image size: 640
- GPU: NVIDIA Tesla T4
- Number of classes: 1

The trained model is saved as:

```text
best.pt

🧪 Model Testing

The model was tested on 20 unseen images.

Testing was performed separately from the training dataset.

Observed Results
Metric	Result
Unseen images tested	20
Images with at least one detection	14
Images with no detection	6
Image-level detection success	70%

At a lower confidence threshold, the model detected cups in 14 of the 20 unseen images.

In one difficult image containing three cups:

2 cups were detected
1 cup was missed

Note: The 70% figure is the percentage of test images containing at least one detection. It is not Precision or Recall.

🔍 Error Analysis

The main error observed during testing was missed detection.

The model sometimes failed to detect cups when the image was difficult.

Possible difficult conditions include:

Small or distant cups
Partially visible cups
Different viewing angles
Complex backgrounds
Different lighting conditions
Example Error

One test image contained three cups. The model detected two cups but missed one.

This indicates that the model can detect cups but may struggle with some objects depending on their position, appearance, or visibility.

🖥️ Application

A Streamlit application was created for easy model testing.

The application provides:

Image upload
Cup detection
Bounding boxes
Class names
Confidence scores
Confidence threshold control
Number of detected cups
Detection statistics
Downloadable prediction results

The application uses the trained:

best.pt

model.

📁 Project Structure
Day39/
│
├── app.py
├── best.pt
├── requirements.txt
├── README.md
│
└── test_images/
    ├── image01.jpg
    ├── image02.jpg
    └── ...
⚙️ Installation

Install the required packages:

pip install -r requirements.txt
▶️ Run the Application

Run:

streamlit run app.py

The application will open in your browser.

Upload an image and adjust the confidence threshold to test the model.

🚀 Future Improvements

With more time, the model could be improved by:

Adding more cup images.
Adding more variety in backgrounds and lighting.
Adding difficult examples to the training dataset.
Increasing the number of training examples.
Improving missed detections through additional training.
Performing a more detailed evaluation using ground-truth labels.
📌 Conclusion

This project demonstrates a complete Computer Vision workflow using a custom YOLOv8 model.

The pipeline covers:

Dataset → Model Training → Testing → Error Analysis → Streamlit Application

The model successfully detects cups in many unseen images while the error analysis identifies missed detections and areas for future improvement.