import cv2
import numpy as np
import os

# Folder Paths

input_folder = "Document5"
output_folder = "Output"

os.makedirs(output_folder, exist_ok=True)


# Process Images


for filename in os.listdir(input_folder):

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):

        image_path = os.path.join(input_folder, filename)

        image = cv2.imread(image_path)

        if image is None:
            print("Could not read:", filename)
            continue

        print(f"Processing {filename}")

       
# Resize Image
       

        image = cv2.resize(image, (800, 600))

        
# Perspective Transformation
       

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

        perspective = cv2.warpPerspective(
            image,
            matrix,
            (800, 600)
        )

# Save Perspective Image

        cv2.imwrite(
            os.path.join(
                output_folder,
                "perspective_" + filename
            ),
            perspective
        )

        
# Convert to Grayscale
        

        gray = cv2.cvtColor(
            perspective,
            cv2.COLOR_BGR2GRAY
        )

        
# Noise Reduction
        

        blur = cv2.GaussianBlur(
            gray,
            (5, 5),
            0
        )

# Brightness & Contrast
        
        enhanced = cv2.convertScaleAbs(
            blur,
            alpha=1.5,
            beta=20
        )

        
# Sharpen Image

        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])

        sharpen = cv2.filter2D(
            enhanced,
            -1,
            kernel
        )

       
# Save Final Image
      

        cv2.imwrite(
            os.path.join(
                output_folder,
                "enhanced_" + filename
            ),
            sharpen
        )

print("\nAll Images Processed Successfully!")