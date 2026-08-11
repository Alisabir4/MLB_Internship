# Day 36 - YOLO Model Performance Audit

## Model and Dataset

- Model: YOLOv8 Nano (`yolov8n.pt`)
- Dataset: traffic-200
- Evaluation images: 100
- Classes: bicycle, bus, car, motorcycle, person, truck

## Evaluation Metrics

| Metric | Result |
|---|---:|
| Precision | 35.95% |
| Recall | 12.44% |
| mAP@50 | 8.83% |
| mAP@50-95 | 5.13% |

## Best-Performing Class

Car was the best-performing class.

- mAP@50: 38.6%
- mAP@50-95: 24.58%

## Worst-Performing Classes

- Bicycle: mAP@50 = 0%
- Truck: mAP@50 = 0.13%

## Error Analysis

30 prediction results were manually reviewed.

The main error categories were:

- Missed Object
- Wrong Class
- False Detection
- Low Confidence
- Small Object
- Occlusion

10 difficult or incorrect predictions were selected for detailed analysis.

## Improvements

- Add more difficult training examples.
- Add small-object examples.
- Add occluded-object examples.
- Improve class balance.
- Train a custom model on the traffic dataset.

## Results

The evaluation generated:

- Precision
- Recall
- mAP@50
- mAP@50-95
- Confusion Matrix
- Prediction examples
- Error analysis report

## Application

A Streamlit application was created to:

- Run model evaluation
- Display evaluation metrics
- Display confusion matrix
- Test challenging images