# Day 41 – FastAPI YOLO Prediction API

A **FastAPI-based Computer Vision API** that integrates a trained **YOLO model** to detect cups in uploaded images.

The project demonstrates how to connect a trained YOLO object-detection model with a REST API, handle image uploads, return prediction results, and deploy the application using Render.

## 🚀 Live API

**Swagger API Documentation:**

https://fastapi-day41.onrender.com/docs

**Render API:**

https://fastapi-day41.onrender.com

---

## 📌 Project Overview

This project converts a trained YOLO cup-detection model into an API using FastAPI.

The API accepts an image, sends it to the YOLO model for inference, and returns information about the detected objects.

### Main Features

* FastAPI REST API
* YOLO object detection
* Cup detection
* Image upload handling
* Prediction confidence scores
* JSON prediction response
* Swagger/OpenAPI documentation
* Render deployment
* Modular FastAPI project structure

---

## 🛠️ Technologies Used

* Python
* FastAPI
* Uvicorn
* Ultralytics YOLO
* PyTorch
* Pydantic
* Swagger/OpenAPI
* Render
* Thunder Client

---

## 📁 Project Structure

```text
Day41/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   └── prediction.py
│   │
│   ├── schemas/
│   │   └── response.py
│   │
│   └── services/
│       └── detector.py
│
├── models/
│   └── best.pt
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🧠 YOLO Model

The project uses a trained YOLO model stored at:

```text
models/best.pt
```

The model is used for cup detection.

Example local test result:

```text
11.jpg → 3 cups detected

Confidence:
0.9366
0.3329
0.3050
```

The model successfully detected multiple cups from the test image.

---

## 🔌 API Endpoints

### 1. Predict

**POST**

```text
/api/predict
```

This endpoint accepts an uploaded image and performs YOLO prediction.

### 2. Predict Image

**POST**

```text
/api/predict/image
```

This endpoint accepts an image file and returns image prediction information.

---

## 📖 Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
https://fastapi-day41.onrender.com/docs
```

From Swagger, you can:

1. Select an endpoint.
2. Click **Try it out**.
3. Upload an image.
4. Execute the request.
5. View the prediction response.

---

## ▶️ Run Locally

### 1. Open the project

```powershell
cd D:\python\MLB_Internship\Day41
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Start FastAPI

```powershell
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🧪 Testing the YOLO Model

The trained model can be tested directly using Python:

```python
from ultralytics import YOLO

model = YOLO("models/best.pt")

results = model("test_image.jpg", conf=0.10)

print("Detections:", len(results[0].boxes))
```

The model returns the detected objects and their confidence scores.

---

## ☁️ Deployment

The FastAPI application was deployed using **Render**.

Live application:

```text
https://fastapi-day41.onrender.com
```

Swagger:

```text
https://fastapi-day41.onrender.com/docs
```

---

## 🧪 API Testing

The API was tested using FastAPI Swagger/OpenAPI.

Thunder Client was also considered for testing.

### Blocker

File sending in **Thunder Client is available only in the paid version**, so image file-upload testing through Thunder Client could not be completed.

The API itself was successfully tested through Swagger and the YOLO model was verified locally.

---

## 📚 What I Learned

During Day 41, I learned:

* How to integrate YOLO with FastAPI.
* How to create REST API endpoints for computer-vision models.
* How to handle uploaded image files using FastAPI.
* How to organize a FastAPI project into routes, schemas, and services.
* How to load a trained YOLO `.pt` model.
* How to return prediction results through an API.
* How to test FastAPI endpoints using Swagger.
* How to deploy a FastAPI application on Render.

---

## 🎯 Day 41 Outcome

The final result is a deployed **FastAPI YOLO Prediction API** capable of receiving images and using the trained YOLO model for cup detection.

The API is available online through Render and its interactive Swagger documentation can be used for testing.



