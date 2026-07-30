## Brief Explanation

### What is Object Detection?

Object Detection is a computer vision technique that identifies and locates one or more objects within an image or video. It predicts the object class, draws a bounding box around each detected object, and provides a confidence score indicating the accuracy of the prediction.

---

### How YOLO is Different from Image Classification

Image Classification only predicts the category of an image without identifying the location of the object. In contrast, YOLO (You Only Look Once) performs both object classification and localization in a single step by detecting multiple objects, drawing bounding boxes around them, and assigning confidence scores in real time.

---

### Which YOLO Model You Used

This project uses the **YOLO11n (Nano)** pre-trained model provided by Ultralytics. It is lightweight, fast, and suitable for real-time object detection while maintaining good accuracy.

---

### What Objects Your Application Detected

The application successfully detected various objects from the COCO dataset, including:

- Person
- Car
- Bus
- Truck
- Motorcycle
- Bicycle
- Dog
- Cat
- Bird
- Chair
- Laptop
- Bottle
- Cell Phone
- Backpack
- Traffic Light

The detected objects are displayed with bounding boxes, class labels, and confidence scores.

---

### Challenges Faced During Implementation

- Processing large video files required more time and system resources.
- Managing temporary files for uploaded images and videos in Streamlit.
- Ensuring compatibility between OpenCV and Streamlit for displaying processed outputs.
- Selecting an appropriate confidence threshold to balance detection accuracy and false positives.