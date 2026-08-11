import os

LABEL_DIR = "test100/labels"

# traffic-200 → COCO class IDs
CLASS_MAPPING = {
    0: 1,  # bicycle → COCO bicycle
    1: 5,  # bus → COCO bus
    2: 2,  # car → COCO car
    3: 3,  # motorcycle → COCO motorcycle
    4: 0,  # person → COCO person
    5: 7   # truck → COCO truck
}

for filename in os.listdir(LABEL_DIR):

    if not filename.endswith(".txt"):
        continue

    path = os.path.join(LABEL_DIR, filename)

    with open(path, "r") as f:
        lines = f.readlines()

    new_lines = []

    for line in lines:

        parts = line.strip().split()

        if len(parts) != 5:
            continue

        old_class = int(parts[0])

        if old_class not in CLASS_MAPPING:
            continue

        parts[0] = str(CLASS_MAPPING[old_class])

        new_lines.append(" ".join(parts))

    with open(path, "w") as f:
        f.write("\n".join(new_lines))

print("Class ID conversion completed successfully.")