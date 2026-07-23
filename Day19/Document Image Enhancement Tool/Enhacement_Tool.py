import cv2
import numpy as np
import os

# Folder Paths
input_folder = r"D:\python\MLB_Internship\Day19\Document Image Enhancement Tool\input"
output_folder = "output"

os.makedirs(output_folder, exist_ok=True)

# Process Every Image

for filename in os.listdir(input_folder):

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):

        image_path = os.path.join(input_folder, filename)

        image = cv2.imread(image_path)

        if image is None:
            continue

        print(f"Processing {filename}")

        
# Step 1: Resize for Display (Optional)
        
        image = cv2.resize(image, (800, 600))

# Step 2: Perspective Correction
       
        h, w = image.shape[:2]

        pts1 = np.float32([
            [50, 40],
            [750, 40],
            [40, 560],
            [760, 560]
        ])

        pts2 = np.float32([
            [0, 0],
            [800, 0],
            [0, 600],
            [800, 600]
        ])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)

        corrected = cv2.warpPerspective(image, matrix, (800, 600))

# Step 3: Convert to Grayscale
        
        gray = cv2.cvtColor(corrected, cv2.COLOR_BGR2GRAY)

# Step 4: Noise Reduction
      
        denoise = cv2.GaussianBlur(gray, (5, 5), 0)

# Step 5: Brightness & Contrast
     
        enhanced = cv2.convertScaleAbs(
            denoise,
            alpha=1.2,
            beta=20
        )


# Step 6: Sharpen Image
        
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])

        sharpen = cv2.filter2D(enhanced, -1, kernel)

# Step 7: Save Output
        
        output_path = os.path.join(
            output_folder,
            "enhanced_" + filename
        )

        cv2.imwrite(output_path, sharpen)

        print("Saved:", output_path)

print("\nProcessing Complete!")