from ultralytics import YOLO
import os

def main():

    print("=" * 60)
    print("ROAD SIGN DETECTION MODEL TRAINING")
    print("=" * 60)

    DATASET = "dataset/data.yaml"

    if not os.path.exists(DATASET):
        print("Dataset not found!")
        print("Expected:", DATASET)
        return

    # Load pretrained model
    model = YOLO("yolov8n.pt")

    # Train model
    model.train(
        data=DATASET,
        epochs=50,
        imgsz=640,
        batch=16,
        workers=2,
        project="RoadSign_Project",
        name="RoadSign_Model",
        exist_ok=True
    )

    print("\nTraining Completed Successfully!")

    print("\nBest Model:")

    print("runs/detect/RoadSign_Project/RoadSign_Model/weights/best.pt")

    print("\nLast Model:")

    print("runs/detect/RoadSign_Project/RoadSign_Model/weights/last.pt")


if __name__ == "__main__":
    main()