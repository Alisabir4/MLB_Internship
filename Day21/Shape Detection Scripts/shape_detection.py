import cv2
import os

# Input and Output Paths

input_folder = r"D:\python\MLB_Internship\Day21\Input Images"
output_folder = r"D:\python\MLB_Internship\Day21\Output Images"

os.makedirs(output_folder, exist_ok=True)

# Supported image formats

extensions = (".jpg", ".jpeg", ".png", ".bmp")

# Process all images

for filename in os.listdir(input_folder):

    if filename.lower().endswith(extensions):

        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Could not read {filename}")
            continue

        output = image.copy()

# Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply threshold
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

# Detect contours
        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        print(f"\nProcessing: {filename}")
        print("-" * 40)

        for contour in contours:

            area = cv2.contourArea(contour)

# Ignore tiny contours (noise)
            if area < 100:
                continue

            perimeter = cv2.arcLength(contour, True)

# Approximate contour
            approx = cv2.approxPolyDP(
                contour,
                0.04 * perimeter,
                True
            )

            vertices = len(approx)

# Bounding Rectangle
            x, y, w, h = cv2.boundingRect(approx)

# Shape Detection
            if vertices == 3:
                shape = "Triangle"

            elif vertices == 4:

                aspect_ratio = w / float(h)

                if 0.95 <= aspect_ratio <= 1.05:
                    shape = "Square"
                else:
                    shape = "Rectangle"

            elif vertices == 5:
                shape = "Pentagon"

            elif vertices == 6:
                shape = "Hexagon"

            elif vertices > 6:
                shape = "Circle"

            else:
                shape = "Polygon"

# Draw contour
            cv2.drawContours(output, [approx], -1, (0, 255, 0), 2)

# Draw bounding rectangle
            cv2.rectangle(
                output,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

# Label shape
            cv2.putText(
                output,
                shape,
                (x, y - 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

# Display area
            cv2.putText(
                output,
                f"Area: {int(area)}",
                (x, y - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 255),
                2
            )

# Display perimeter
            cv2.putText(
                output,
                f"Peri: {int(perimeter)}",
                (x, y + h + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 255),
                2
            )

# Print details
            print(f"Shape     : {shape}")
            print(f"Area      : {area:.2f}")
            print(f"Perimeter : {perimeter:.2f}")
            print("-" * 40)

# Save final image
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, output)

print("\nAll images processed successfully!")