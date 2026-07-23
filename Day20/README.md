## Edge Detection Techniques

### Difference Between Sobel, Laplacian, and Canny

### Sobel Edge Detection
Sobel detects edges by calculating the gradient intensity of an image in horizontal and vertical directions.

- Detects edges based on changes in brightness.
- Provides information about edge direction.
- More sensitive to noise compared to Canny.

### Laplacian Edge Detection
Laplacian detects edges by calculating the second derivative of an image.

- Detects edges in all directions.
- Produces sharp edge responses.
- More sensitive to noise because it does not perform smoothing automatically.

### Canny Edge Detection
Canny is an advanced multi-stage edge detection algorithm.

Steps:
- Noise reduction using Gaussian Blur.
- Gradient calculation.
- Non-maximum suppression.
- Edge tracking using thresholds.

Canny produced better results for document detection because it provides cleaner and more accurate document boundaries.


## Morphological Operations

Morphological operations are used to remove noise and improve edge connectivity.

### Morphological Closing
Closing combines dilation followed by erosion.

Purpose:
- Fills small gaps in detected edges.
- Connects broken document boundaries.
- Improves contour detection.

### Dilation
Dilation expands white regions in an image.

Purpose:
- Strengthens weak edges.
- Connects nearby edge pixels.

### Erosion
Erosion removes small unwanted regions.

Purpose:
- Removes noise.
- Reduces unnecessary white regions.


## Best Combination of Techniques

The best results were achieved using:

1. Grayscale Conversion
2. Gaussian Blur
3. Canny Edge Detection
4. Morphological Closing
5. Largest Contour Detection

This combination provided accurate document boundary detection by reducing noise, connecting broken edges, and identifying the largest document contour.


## Challenges Faced

During document boundary detection, several challenges occurred:

- Uneven lighting and shadows affected edge detection.
- Tilted documents created irregular contours.
- Blurred images produced weak edges.
- Background objects generated extra contours.

## Solutions

To improve results:

- Applied Gaussian Blur before edge detection to reduce noise.
- Used morphological operations to connect broken edges.
- Selected the largest contour to identify the document.
- Adjusted Canny threshold values for better edge detection.
