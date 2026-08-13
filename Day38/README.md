# Day 38 - Custom Object Detection Dataset & Model

## 1. Dataset

Object: Cups

Classes:
- Black
- White

The dataset was sourced from Roboflow and contained existing YOLO annotations.

## 2. Dataset Split

| Split | Images |
|---|---:|
| Original Training | 201 |
| Validation | 30 |
| Test | 10 |
| Total Original | 241 |

Validation and test images were kept untouched.

## 3. Data Augmentation

The training dataset was augmented to approximately 650 images.

Augmentations used:
- Horizontal flip
- Rotation
- Brightness adjustment
- Scaling

Only training images were augmented.

## 4. Dataset Analysis

- Training images: 201
- Training labels: 201
- Validation images: 30
- Validation labels: 30
- Test images: 10
- Missing annotations: 0
- Classes: Black and White
- Class distribution was approximately balanced.

## 5. Model Training

- Model: YOLOv8n
- Epochs: 10
- Image size: 640
- Batch size: 8
- Device: CPU

## 6. Evaluation Results

| Metric | Result |
|---|---:|
| Precision | 99.77% |
| Recall | 100% |
| mAP@50 | 99.50% |
| mAP@50-95 | 93.99% |

Evaluation was performed on 30 validation images containing 60 objects.

## 7. Unseen Image Testing

The trained model was tested on 10 completely new images collected separately from the original dataset.

The model correctly detected most cups, but at least one cup was missed.

This shows that the model can still be improved with more diverse training examples.

## 8. Problems Found

- Some cups were missed in unseen images.
- The model may need more examples with different backgrounds, angles, lighting, and object sizes.

## 9. Future Improvements

- Collect more original cup images.
- Include more challenging viewpoints and lighting conditions.
- Improve annotation quality.
- Add more diverse training examples.
- Retrain and evaluate the improved model.

## 10. Workflow

Collect → Clean → Annotate → Split → Augment → Train → Evaluate → Test