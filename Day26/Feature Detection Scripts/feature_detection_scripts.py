import cv2
import numpy as np
import os

# Create Output folder
os.makedirs("Output", exist_ok=True)

# Read Images
img1 = cv2.imread("D:\python\MLB_Internship\Day26\Sample Input Images/image1.png")
img2 = cv2.imread("D:\python\MLB_Internship\Day26\Sample Input Images/image2.png")

if img1 is None or img2 is None:
    print("Error: Check image paths.")
    exit()

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Task 1: Harris Corner Detection


gray_float = np.float32(gray1)

corners = cv2.cornerHarris(gray_float, 2, 3, 0.04)
corners = cv2.dilate(corners, None)

harris_img = img1.copy()
harris_img[corners > 0.01 * corners.max()] = [0, 0, 255]

cv2.imwrite("Output/harris_output.jpg", harris_img)

cv2.imshow("Task 1 - Harris Corner Detection", harris_img)
cv2.waitKey(0)

# Task 2: ORB Detection

orb = cv2.ORB_create(1000)

kp1, des1 = orb.detectAndCompute(gray1, None)
kp2, des2 = orb.detectAndCompute(gray2, None)

print("ORB Keypoints in Image 1 :", len(kp1))
print("ORB Keypoints in Image 2 :", len(kp2))

# Task 3: Visualize ORB Keypoints


orb_img = cv2.drawKeypoints(
    img1,
    kp1,
    None,
    color=(0, 255, 0),
    flags=cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS
)

cv2.imwrite("Output/orb_keypoints.jpg", orb_img)

cv2.imshow("Task 3 - ORB Keypoints", orb_img)
cv2.waitKey(0)

# Task 4: Feature Matching

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

matches = bf.match(des1, des2)

matches = sorted(matches, key=lambda x: x.distance)

print("Total Matches :", len(matches))

# Task 5: Display Matched Keypoints

matched_img = cv2.drawMatches(
    img1,
    kp1,
    img2,
    kp2,
    matches[:50],
    None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)

cv2.imwrite("Output/matched_features.jpg", matched_img)

cv2.imshow("Task 5 - ORB Feature Matching", matched_img)
cv2.waitKey(0)

# Task 6: Comparison

harris_count = np.sum(corners > 0.01 * corners.max())

print("\n========== Comparison ==========")
print("Harris Corners :", harris_count)
print("ORB Keypoints  :", len(kp1))

print("\nHarris Corner Detection")
print("- Detects only corners.")
print("- Fast.")
print("- Cannot match features.")
print("- Not scale invariant.")

print("\nORB")
print("- Detects keypoints and descriptors.")
print("- Supports feature matching.")
print("- Rotation invariant.")
print("- Suitable for real-time applications.")

cv2.destroyAllWindows()

print("\nAll Tasks Completed Successfully!")