import cv2
import matplotlib.pyplot as plt

# Load Image


image = cv2.imread("sample.jpg")

if image is None:
    print("Image not found!")
    exit()


image_rgb = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2RGB
)

# Convert to Grayscale

gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)


# Gaussian Blur


blur = cv2.GaussianBlur(
    gray,
    (5,5),
    0
)

# Sobel Edge Detection


sobel_x = cv2.Sobel(
    blur,
    cv2.CV_64F,
    1,
    0,
    ksize=3
)

sobel_y = cv2.Sobel(
    blur,
    cv2.CV_64F,
    0,
    1,
    ksize=3
)


sobel = cv2.magnitude(
    sobel_x,
    sobel_y
)

# Laplacian Edge Detection


laplacian = cv2.Laplacian(
    blur,
    cv2.CV_64F
)

# Canny Edge Detection

canny = cv2.Canny(
    blur,
    100,
    200
)

# Display Results
titles = [
    "Original Image",
    "Grayscale",
    "Sobel Edge",
    "Laplacian Edge",
    "Canny Edge"
]


images = [
    image_rgb,
    gray,
    sobel,
    laplacian,
    canny
]


plt.figure(figsize=(12,8))


for i in range(len(images)):

    plt.subplot(2,3,i+1)

    if i == 0:
        plt.imshow(images[i])
    else:
        plt.imshow(
            images[i],
            cmap="gray"
        )

    plt.title(titles[i])
    plt.axis("off")


plt.tight_layout()
plt.show()