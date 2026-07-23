# Shape Detection System

## What are Contours?

Contours are curves or boundaries that connect continuous points having the same color or intensity in an image. In image processing, contours are used to detect the outline and shape of objects.

Contours help identify objects by finding their boundaries, which allows us to calculate properties like area, perimeter, and shape type.


## How Contour Detection Works

The contour detection process works as follows:

1. The input image is loaded using OpenCV.
2. The image is converted into grayscale.
3. Thresholding is applied to separate objects from the background.
4. OpenCV's `findContours()` function detects the boundaries of objects.
5. Detected contours are drawn on the image.
6. The contour points are analyzed to identify the shape.
7. Area and perimeter of each detected shape are calculated.


## Shapes Detected by This Program

The program can detect the following shapes:

- Triangle
- Rectangle
- Circle

It also displays:
- Shape name
- Area of the shape
- Perimeter of the shape


## Challenges Faced

Some challenges faced during development were:

- Selecting the correct threshold value for different images.
- Removing noise and avoiding detection of unwanted small contours.
- Correctly identifying shapes with different sizes and orientations.
- Improving accuracy when distinguishing between different shapes.

These challenges were solved by adjusting image preprocessing steps and filtering unnecessary contours.