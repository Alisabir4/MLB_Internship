import os
import shutil
import random

SOURCE_IMAGES = "dataset/train/images"
SOURCE_LABELS = "dataset/train/labels"

OUTPUT_IMAGES = "test100/images"
OUTPUT_LABELS = "test100/labels"

MAX_IMAGES = 100

os.makedirs(OUTPUT_IMAGES, exist_ok=True)
os.makedirs(OUTPUT_LABELS, exist_ok=True)

images = [
    f for f in os.listdir(SOURCE_IMAGES)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

random.seed(42)
random.shuffle(images)

selected_count = 0

for image in images:

    if selected_count >= MAX_IMAGES:
        break

    image_name = os.path.splitext(image)[0]
    label = image_name + ".txt"

    image_path = os.path.join(SOURCE_IMAGES, image)
    label_path = os.path.join(SOURCE_LABELS, label)

    # Only select images that have annotations
    if not os.path.exists(label_path):
        continue

    shutil.copy2(
        image_path,
        os.path.join(OUTPUT_IMAGES, image)
    )

    shutil.copy2(
        label_path,
        os.path.join(OUTPUT_LABELS, label)
    )

    selected_count += 1

print("=" * 40)
print("Dataset preparation completed")
print("=" * 40)
print(f"Images selected : {selected_count}")
print(f"Images folder   : {OUTPUT_IMAGES}")
print(f"Labels folder   : {OUTPUT_LABELS}")