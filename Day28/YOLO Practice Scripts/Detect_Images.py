import os
from ultralytics import YOLO

# Load pre-trained YOLO11 Nano model
model = YOLO("yolo11n.pt")

input_folder = r"D:\python\MLB_Internship\Day28\Sample Input Images"
output_folder = r"D:\python\MLB_Internship\Day28\Output Images & Videos"

os.makedirs(output_folder, exist_ok=True)

image_extensions = (".jpg", ".jpeg", ".png", ".bmp")

images = [
    img for img in os.listdir(input_folder)
    if img.lower().endswith(image_extensions)
]

for image_name in images:
    image_path = os.path.join(input_folder, image_name)

    results = model.predict(
        source=image_path,
        conf=0.25,
        save=False
    )

    annotated_image = results[0].plot()

    output_path = os.path.join(output_folder, image_name)

    import cv2
    cv2.imwrite(output_path, annotated_image)

    print(f"\nImage: {image_name}")

    for box in results[0].boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        print(
            f"{model.names[class_id]} : {confidence:.2f}"
        )

print("\nFinished!")