# Practice 2 - Test YOLO on Your Own Image


from ultralytics import YOLO
import os


# Load Pre-trained YOLOv8 Model

print("Loading YOLOv8 Model...")

model = YOLO("yolov8n.pt")

print("Model Loaded Successfully!\n")


# Image Path


image_path = r"D:\python\MLB_Internship\Day17\YOLO Scripts\Images"

# Check image exists
if not os.path.exists(image_path):
    print("Image not found!")
    exit()

# Perform Object Detection


print("Running Detection...\n")

results = model.predict(
    source=image_path,
    conf=0.25,
    save=True,
    show=True
)

print("\nDetection Completed!")


# Display Detection Results

print("\nDetected Objects")
print("=" * 50)

for result in results:

    if len(result.boxes) == 0:
        print("No objects detected.")
        continue

    for box in result.boxes:

        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        confidence = float(box.conf[0])

        x1, y1, x2, y2 = box.xyxy[0]

        print(f"Object      : {class_name}")
        print(f"Confidence  : {confidence:.2f}")
        print(f"Bounding Box: ({int(x1)}, {int(y1)}) -> ({int(x2)}, {int(y2)})")
        print("-" * 50)

print("\nPrediction image saved in:")
print(results[0].save_dir)