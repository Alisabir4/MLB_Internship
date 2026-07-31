import os
from ultralytics import YOLO


def main():
    print("=" * 60)
    print("ROAD SIGN DETECTION USING YOLOv8")
    print("=" * 60)

    # Check dataset
    if not os.path.exists("dataset/data.yaml"):
        print("Error: dataset/data.yaml not found!")
        print("Place your Roboflow dataset inside a folder named 'dataset'.")
        return

    # Load pretrained YOLOv8 Nano model
    model = YOLO("yolov8n.pt")

   
    # TRAIN MODEL
    
    print("\nStarting Training...\n")

    model.train(
        data="dataset/data.yaml",
        epochs=20,
        imgsz=640,
        batch=16,
        workers=2,
        device="cpu",      # Change to 0 if you have an NVIDIA GPU
        project="RoadSign_Project",
        name="RoadSign_Model",
        exist_ok=True
    )

    print("\nTraining Completed!")

    
    # LOAD BEST MODEL
    
    best_model = YOLO("RoadSign_Project/RoadSign_Model/weights/best.pt")

    
    # EVALUATE MODEL
    
    print("\nEvaluating Model...\n")

    metrics = best_model.val()

    print("\nEvaluation Completed!")
    print(metrics)

   
    # RUN INFERENCE
 
    test_folder = "dataset/test/images"

    if not os.path.exists(test_folder):
        print("\nTest folder not found!")
        return

    images = [
        img for img in os.listdir(test_folder)
        if img.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    print(f"\nFound {len(images)} test images.")

    for i, image in enumerate(images, start=1):
        image_path = os.path.join(test_folder, image)

        print(f"Processing {i}/{len(images)} : {image}")

        best_model.predict(
            source=image_path,
            conf=0.5,
            save=True,
            show=False
        )

    print("\nInference Completed!")
    print("Predicted images are saved in:")
    print("runs/detect/predict/")


if __name__ == "__main__":
    main()