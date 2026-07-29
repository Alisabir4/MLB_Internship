import cv2
import numpy as np


def segment_image(image, method):

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    if method == "Binary Threshold":

        _, output = cv2.threshold(
            gray,
            127,
            255,
            cv2.THRESH_BINARY
        )

    elif method == "Adaptive Threshold":

        output = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

    elif method == "Otsu Threshold":

        _, output = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

    elif method == "Foreground Segmentation":

        _, mask = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        output = cv2.bitwise_and(
            image,
            image,
            mask=mask
        )

    else:

        output = gray

    return output