# 🚦 Road Sign Detection System using YOLOv8

## 📌 Project Overview

This project is a Custom Object Detection System developed using **YOLOv8** and **Streamlit**. The model is trained on the **Road Sign Detection** dataset from Roboflow Universe. It can detect road signs in both images and videos, display confidence scores, and allow users to download the processed results.

---

## 🎯 Features

- Custom YOLOv8 model training
- Model evaluation
- Road sign detection on images
- Road sign detection on videos
- Confidence score display
- Save prediction results
- Download processed image
- Download processed video
- Streamlit Web Interface

---

## 📂 Dataset

- **Dataset:** Road Sign Detection
- **Source:** Roboflow Universe
- **Format:** YOLOv8

Dataset Structure:

```
dataset/
│
├── train/
│   ├── images/
│   └── labels/
│
├── valid/
│   ├── images/
│   └── labels/
│
├── test/
│   ├── images/
│   └── labels/
│
└── data.yaml
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone <your_repository_link>
cd Day29
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Training

```bash
python train.py
```

The trained model will be saved in:

```
RoadSign_Project/
└── RoadSign_Model/
    └── weights/
        ├── best.pt
        └── last.pt
```

---

## 📊 Model Evaluation

```bash
python evaluate.py
```

Metrics:

- Precision
- Recall
- mAP@50
- mAP@50-95

---

## 🔍 Run Inference

```bash
python predict.py
```

Prediction results are saved in:

```
runs/detect/predict/
```

---

## 🌐 Streamlit Application

Run:

```bash
streamlit run app.py
```

---

## 📈 Training Parameters

| Parameter | Value |
|-----------|--------|
| Model | YOLOv8 Nano |
| Epochs | 50 |
| Batch Size | 16 |
| Image Size | 640 |

---

## 📊 Results

Fill these after training.

| Metric | Value |
|---------|-------|
| Precision |0.9346755307930424|
| Recall |0.8928571428571428|
| mAP@50 |0.8947154866332497|
| mAP@50-95 |0.7555143908616849|

---

## 🔬 Observations


- The YOLOv8 Nano model was trained on the Road Sign Detection dataset from Roboflow Universe.
- Training for 50 epochs produced a strong performance with an mAP@50 of 89.47%, exceeding the target of 80%.
- Precision (93.47%) indicates that most predicted road signs were correct.
- Recall (89.29%) shows that the model successfully detected the majority of road signs in the dataset.
- The model generalized well and produced accurate detections on the test images.
---

## 🛠 Technologies Used

- Python
- YOLOv8
- OpenCV
- Streamlit
- Roboflow
- PyTorch

---

## 📁 Project Structure

```
Day29/
│
├── app.py
├── train.py
├── evaluate.py
├── predict.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── dataset/
│
├── RoadSign_Project/
│
└── runs/
```
