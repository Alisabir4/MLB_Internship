import cv2
import os
import time


def save_image(image):

    os.makedirs("outputs", exist_ok=True)

    filename = f"outputs/output_{int(time.time())}.png"

    cv2.imwrite(filename, image)

    return filename