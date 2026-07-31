import os
from ultralytics import YOLO

MODEL = r"D:\python\MLB_Internship\Day29\best.pt"

TEST_IMAGES = "dataset/test/images"

if not os.path.exists(MODEL):
    print("best.pt not found!")
    exit()

if not os.path.exists(TEST_IMAGES):
    print("Test folder not found!")
    exit()

model = YOLO(MODEL)

images = []

for file in os.listdir(TEST_IMAGES):

    if file.endswith((".jpg", ".jpeg", ".png")):
        images.append(file)

print("=" * 60)
print("ROAD SIGN DETECTION")
print("=" * 60)

print(f"Found {len(images)} Images\n")

for i, image in enumerate(images, start=1):

    image_path = os.path.join(TEST_IMAGES, image)

    print(f"[{i}/{len(images)}] Processing {image}")

    results = model.predict(
        source=image_path,
        conf=0.5,
        save=True,
        save_txt=True,
        save_conf=True
    )

    boxes = results[0].boxes

    if len(boxes) == 0:
        print("No Road Sign Detected\n")
        continue

    print("Detected Objects:")

    for box in boxes:

        cls = int(box.cls[0])

        confidence = float(box.conf[0])

        label = model.names[cls]

        print(f"{label} : {confidence:.2f}")

    print()

print("=" * 60)

print("Inference Completed")

print("Results Saved In")

print("runs/detect/predict/")