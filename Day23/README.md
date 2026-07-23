# Computer Vision Image Processing Studio

## Project Overview

Computer Vision Image Processing Studio is a web-based application developed using **Python**, **OpenCV**, and **Gradio**. The application allows users to upload an image, apply various image processing techniques, preview the processed result, and download the output image.

This project combines multiple computer vision concepts learned throughout the OpenCV module into a single, interactive application.

---

## Features

* Upload an image
* Select an image processing operation from a dropdown menu
* Process the uploaded image
* Display the processed image
* Download the processed image
* Simple and user-friendly Gradio interface

---

## Image Processing Operations

The application supports the following operations:

* Grayscale Conversion
* Gaussian Blur
* Edge Detection (Canny)
* Image Rotation
* Image Enhancement
* Contour Detection
* Shape Detection
* Image Flip (Custom Feature)

---

## Technologies Used

* Python
* OpenCV
* Gradio
* NumPy

---

## Project Structure

```text
Day23/
│
├── app.py
├── requirements.txt
├── README.md
├── Sample Input Images/
└── Sample Output Images/
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Alisabir4/MLB_Internship.git
```

2. Navigate to the project folder:

```bash
cd Day23
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

5. Open the Gradio URL displayed in the terminal (usually `http://127.0.0.1:7860`).

---

## How to Use

1. Launch the application.
2. Upload an image.
3. Choose an image processing operation from the dropdown menu.
4. View the processed image.
5. Download the processed image using the download button.

---

## Challenge Feature

In addition to the required operations, the application includes **Image Flip**, allowing users to horizontally flip the uploaded image. This custom feature extends the functionality beyond the classroom requirements.

---

## Learning Outcomes

Through this project, I learned how to:

* Build a complete Computer Vision application.
* Combine multiple OpenCV image processing techniques.
* Create an interactive web interface using Gradio.
* Organize code into a clean and reusable structure.
* Prepare an application for deployment on Hugging Face Spaces.

---

## Future Improvements

* Add webcam support.
* Add video processing features.
* Allow users to apply multiple filters in sequence.
* Add brightness and contrast adjustment sliders.
* Improve the interface with additional customization options.

---

## Requirements

```
gradio
opencv-python-headless
numpy
```

