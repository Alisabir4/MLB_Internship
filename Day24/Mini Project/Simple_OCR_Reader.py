import cv2
import easyocr
import os


# Input and Output Paths


image_path = r"D:\python\MLB_Internship\Day24\Mini Project\Input Images\image9.jpg"

output_folder = r"D:\python\MLB_Internship\Day24\Mini Project\Output Images"
os.makedirs(output_folder, exist_ok=True)

text_file = os.path.join(output_folder, "extracted_text.txt")

# Initialize EasyOCR


reader = easyocr.Reader(['en'])


# Read Image


image = cv2.imread(image_path)

if image is None:
    print("Image not found!")
    exit()

# Extract Text


result = reader.readtext(image_path, detail=0)

extracted_text = "\n".join(result)

# Display Extracted Text

print("========== Extracted Text ==========\n")
print(extracted_text)


# Save Text File


with open(text_file, "w", encoding="utf-8") as file:
    file.write(extracted_text)

print("\nText saved successfully!")


# Show Original Image


cv2.imshow("Original Image", image)

print("\nPress any key to close the image window...")

cv2.waitKey(0)
cv2.destroyAllWindows()