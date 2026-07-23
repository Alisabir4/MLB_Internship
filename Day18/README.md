# Day 18 - OpenCV Image Processing Toolkit

## Objective

The objective of this project is to learn the basics of OpenCV by building a menu-driven image processing application. The program allows users to perform different image operations such as loading, resizing, rotating, flipping, cropping, drawing shapes, adding text, and saving the processed image.

---

## Features

- Load an image
- Convert image to grayscale
- Resize image
- Rotate image (90°, 180°, 270°)
- Flip image (Horizontal & Vertical)
- Crop image
- Draw rectangle, circle, line, and polygon
- Add custom text
- Save the processed image

---

## Technologies Used

- Python 3.x
- OpenCV (cv2)
- NumPy

---

## Project Structure

```
Day18/
│── Image_Processing_Toolkit.py
│
├── input/
│   ├── landscape.jpg
│   ├── person.jpg
│   ├── vehicle.jpg
│   ├── document.jpg
│   └── object.jpg
│
└── output/
```

---

## BGR vs RGB

OpenCV reads images in **BGR (Blue, Green, Red)** format, while most image processing libraries use **RGB (Red, Green, Blue)** format.

- **BGR:** Default color format used by OpenCV.
- **RGB:** Standard color format used for displaying images.

When displaying OpenCV images using libraries like Matplotlib, converting BGR to RGB ensures the colors appear correctly.

---

## What is a Grayscale Image?

A grayscale image contains only one color channel, representing different shades of gray from black to white.

### Why Grayscale is Used

- Reduces image complexity.
- Uses less memory.
- Speeds up image processing.
- Commonly used in computer vision tasks such as edge detection, face detection, and object recognition.

---

## OpenCV Functions Used

| Function | Purpose |
|----------|---------|
| `cv2.imread()` | Load an image |
| `cv2.imshow()` | Display an image |
| `cv2.imwrite()` | Save an image |
| `cv2.cvtColor()` | Convert color image to grayscale |
| `cv2.resize()` | Resize image |
| `cv2.rotate()` | Rotate image |
| `cv2.flip()` | Flip image |
| `cv2.rectangle()` | Draw rectangle |
| `cv2.circle()` | Draw circle |
| `cv2.line()` | Draw line |
| `cv2.polylines()` | Draw polygon |
| `cv2.putText()` | Add text to image |
| `cv2.waitKey()` | Wait for key press |
| `cv2.destroyAllWindows()` | Close all OpenCV windows |

---

## Challenge Task

The toolkit was tested on five different image categories:

- Landscape
- Person
- Vehicle
- Document
- Object

The same image processing operations were applied to each image.

---

## Challenges Faced

- Encountered the error **`AttributeError: 'NoneType' object has no attribute 'shape'`** because the image path was incorrect.
- Solved the issue by placing images inside the **input** folder and loading them using the correct relative path.
- Learned that OpenCV uses the **BGR** color format instead of RGB.

---

## Learning Outcomes

After completing this project, I learned how to:

- Load and save images using OpenCV.
- Read image properties such as height, width, and channels.
- Convert images to grayscale.
- Resize, rotate, flip, and crop images.
- Draw shapes and add text to images.
- Build a menu-driven image processing application.
- Apply the same processing operations to multiple images.

---

## Conclusion

This project strengthened my understanding of OpenCV fundamentals and basic image processing techniques. It provided practical experience in manipulating images and built a strong foundation for advanced computer vision topics such as image filtering, feature detection, object detection, and deep learning.