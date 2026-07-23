# Practice 1 - Object Detection using YOLOv8


from ultralytics import YOLO
import os

# Load Pre-trained YOLOv8 Model


print("Loading YOLOv8 Model...")

model = YOLO("yolov8n.pt")

print("Model Loaded Successfully!\n")

# Image Folder

image_folder = r"D:\python\MLB_Internship\Day17\YOLO Scripts\Images"

# Check if folder exists

if not os.path.exists(image_folder):
    print("Image folder not found!")
    exit()

# Run Object Detection


print("Running Object Detection...\n")

results = model.predict(
    source=image_folder,
    conf=0.25,
    save=True,
    show=True
)

print("\nDetection Completed Successfully!")

print("\nResults Saved In:")
print(results[0].save_dir)