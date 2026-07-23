import cv2
import numpy as np
import matplotlib.pyplot as plt


# Load Image

image = cv2.imread("Image.jpg")


if image is None:
    print("Image not found!")
    exit()

# Convert to Grayscale

gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)

# Convert to Binary Image


_, binary = cv2.threshold(
    gray,
    127,
    255,
    cv2.THRESH_BINARY
)

# Create Kernel

kernel = np.ones(
    (3,3),
    np.uint8
)

# Erosion

erosion = cv2.erode(
    binary,
    kernel,
    iterations=1
)

# Dilation

dilation = cv2.dilate(
    binary,
    kernel,
    iterations=1
)

# Opening

opening = cv2.morphologyEx(
    binary,
    cv2.MORPH_OPEN,
    kernel
)

# Closing

closing = cv2.morphologyEx(
    binary,
    cv2.MORPH_CLOSE,
    kernel
)

# Morphological Gradient

gradient = cv2.morphologyEx(
    binary,
    cv2.MORPH_GRADIENT,
    kernel
)

# Top Hat

top_hat = cv2.morphologyEx(
    binary,
    cv2.MORPH_TOPHAT,
    kernel
)


# Black Hat

black_hat = cv2.morphologyEx(
    binary,
    cv2.MORPH_BLACKHAT,
    kernel
)

# Display Results

titles = [
    "Original Binary",
    "Erosion",
    "Dilation",
    "Opening",
    "Closing",
    "Gradient",
    "Top Hat",
    "Black Hat"
]


images = [
    binary,
    erosion,
    dilation,
    opening,
    closing,
    gradient,
    top_hat,
    black_hat
]


plt.figure(figsize=(12,10))


for i in range(len(images)):

    plt.subplot(3,3,i+1)

    plt.imshow(
        images[i],
        cmap="gray"
    )

    plt.title(titles[i])
    plt.axis("off")


plt.tight_layout()
plt.show()