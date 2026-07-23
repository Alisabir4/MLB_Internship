# Mini Project: Object Detection using YOLOv8
# Dataset: Face Mask Detection (Roboflow)


from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import os

# Load Pre-trained YOLOv8 Model

print("=" * 60)
print("Loading YOLOv8 Model...")
print("=" * 60)

model = YOLO("yolov8n.pt")

print("Model Loaded Successfully!\n")

# Dataset Path


dataset_path = r"D:\python\MLB_Internship\Day17\FaceMask Detection Scripts\FaceMask\test\images"

# Check dataset exists
if not os.path.exists(dataset_path):
    print("Dataset folder not found!")
    exit()

# Run Inference

print("Running Object Detection...\n")

results = model.predict(
    source=dataset_path,
    conf=0.25,
    save=True,
    show=False
)

print("Inference Completed Successfully!\n")

print("Results Saved In:")
print(results[0].save_dir)

# Detection Details


print("\n")
print("=" * 60)
print("Prediction Results")
print("=" * 60)

for result in results:

    print(f"\nImage: {os.path.basename(result.path)}")

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
        print(f"BoundingBox : ({int(x1)}, {int(y1)}) -> ({int(x2)}, {int(y2)})")
        print("-" * 40)

# Display First Three Output Images

output_folder = results[0].save_dir

print("\nDisplaying Prediction Results...\n")

images = [img for img in os.listdir(output_folder)
          if img.endswith((".jpg", ".png", ".jpeg"))]

for image in images[:3]:

    image_path = os.path.join(output_folder, image)

    img = cv2.imread(image_path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(8,6))

    plt.imshow(img)

    plt.title(image)

    plt.axis("off")

    plt.show()

print("\nMini Project Completed Successfully!")