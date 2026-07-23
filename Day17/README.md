# Mini Project: Object Detection using YOLOv8 (Face Mask Detection)

## Overview

This mini project demonstrates how to perform **object detection** using a **pre-trained YOLOv8 model** on a public **Face Mask Detection** dataset downloaded from **Roboflow Universe**. The objective was to understand how YOLO performs inference, visualizes detections, and interprets prediction results without training a custom model.

---

## Dataset

* **Dataset Name:** Face Mask Detection
* **Source:** Roboflow Universe
* **Format:** YOLO Format
* **Classes:**

  * With Mask
  * Without Mask
  * Mask Worn Incorrectly (depending on the dataset version)

---

## Model Used

* **Model:** YOLOv8 Nano (`yolov8n.pt`)
* **Framework:** Ultralytics YOLO
* **Purpose:** Object Detection (Inference Only)

---

## Steps Performed

1. Downloaded the Face Mask Detection dataset in YOLO format from Roboflow.
2. Installed the Ultralytics YOLO package.
3. Loaded the pre-trained YOLOv8 Nano model.
4. Performed inference on the test images.
5. Visualized the detection results.
6. Saved the output images with bounding boxes.
7. Examined the detected objects, confidence scores, and bounding boxes.

---

## Results

* Successfully loaded the pre-trained YOLOv8 model.
* Performed inference on the Face Mask dataset.
* Generated prediction images with bounding boxes.
* Displayed detected object names and confidence scores.
* Saved the annotated images automatically in the output folder.

---

## Model Prediction Analysis

The pre-trained **YOLOv8 Nano** model is trained on the **COCO dataset**, which contains 80 common object categories such as **person**, **car**, **dog**, and **bicycle**.

Since the Face Mask Detection dataset contains custom classes (**With Mask**, **Without Mask**, etc.), the pre-trained model does **not** recognize these classes directly. Instead, it mainly detects **persons** in the images.

This demonstrates an important concept of object detection:

* A pre-trained model can only detect the classes it has learned during training.
* To detect face masks specifically, the YOLO model must be fine-tuned using the Face Mask Detection dataset.

---

## Key Observations

* The model successfully detected people in most images.
* Bounding boxes were accurately drawn around detected persons.
* Confidence scores indicated the reliability of each prediction.
* Output images were automatically saved with annotations.
* The model could not classify "With Mask" or "Without Mask" because these classes are not part of the COCO dataset.

---

## Challenges Faced

* Correctly configuring dataset paths.
* Understanding the folder structure of the YOLO dataset.
* Resolving file path errors during inference.
* Learning that a pre-trained model cannot detect custom classes without additional training.

---

## Conclusion

This project provided practical experience with YOLOv8 object detection using a pre-trained model. It demonstrated the complete inference workflow, including loading the model, processing images, visualizing detections, and interpreting prediction results. The project also highlighted the importance of model training when working with custom object classes such as face masks.

---

## Technologies Used

* Python
* Ultralytics YOLOv8
* OpenCV
* Matplotlib
* Roboflow Universe
