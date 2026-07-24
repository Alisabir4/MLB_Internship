import easyocr
import cv2
import os

# Input and Output Paths

input_folder = r"D:\python\MLB_Internship\Day24\Coding Practice\Input Images"

original_output = r"D:\python\MLB_Internship\Day24\Coding Practice\Output\Original OCR"
enhanced_output = r"D:\python\MLB_Internship\Day24\Coding Practice\Output\Enhanced OCR"
comparison_output = r"D:\python\MLB_Internship\Day24\Coding Practice\Output\Comparison"

os.makedirs(original_output, exist_ok=True)
os.makedirs(enhanced_output, exist_ok=True)
os.makedirs(comparison_output, exist_ok=True)

# Initialize EasyOCR

reader = easyocr.Reader(['en'])

extensions = ('.jpg', '.jpeg', '.png', '.bmp')

# Process Images

for filename in os.listdir(input_folder):

    if filename.lower().endswith(extensions):

        image_path = os.path.join(input_folder, filename)

        image = cv2.imread(image_path)

        if image is None:
            print(f"Cannot read {filename}")
            continue

        print(f"\nProcessing: {filename}")

        
        # OCR on Original Image
        

        original_result = reader.readtext(image_path, detail=0)

        original_text = "\n".join(original_result)

        with open(os.path.join(original_output,
                 os.path.splitext(filename)[0] + ".txt"),
                 "w",
                 encoding="utf-8") as f:
            f.write(original_text)

        
        # Image Enhancement
       

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (3,3), 0)

        enhanced = cv2.equalizeHist(gray)

        enhanced_path = os.path.join(comparison_output, filename)

        cv2.imwrite(enhanced_path, enhanced)

        
        # OCR on Enhanced Image
        

        enhanced_result = reader.readtext(enhanced_path, detail=0)

        enhanced_text = "\n".join(enhanced_result)

        with open(os.path.join(enhanced_output,
                 os.path.splitext(filename)[0] + ".txt"),
                 "w",
                 encoding="utf-8") as f:
            f.write(enhanced_text)

        print("Original OCR:")
        print(original_text)

        print("\nEnhanced OCR:")
        print(enhanced_text)

print("\nCompleted OCR for all images.")