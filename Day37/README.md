# Day 37 - YOLO Model Improvement

## Objective

Improve the YOLO model using data analysis and image augmentation.

## V1 → Error Analysis → Data Improvement → V2

### 1. Class Distribution

The original dataset contained:

| Class | Samples |
|---|---:|
| bicycle | 1014 |
| bus | 44 |
| car | 1785 |
| motorcycle | 672 |
| person | 0 |
| truck | 17 |

The least represented class was truck with 17 samples.
Bus was also significantly underrepresented.

## 2. Data Augmentation

Image augmentation was applied to increase training variation.

Augmented data was added to the training dataset.

The augmentation process generated additional training images and labels.

## 3. Model V2

YOLOv8 Nano was retrained using the improved training dataset.

Training settings:

- Model: YOLOv8 Nano
- Image size: 640
- Epochs: 20
- Batch size: 4

## 4. V1 vs V2

| Metric | V1 | V2 |
|---|---:|---:|
| Precision | 0.3595 | 0.8041 |
| Recall | 0.1244 | 0.4077 |
| mAP@50 | 0.0883 | 0.4275 |
| mAP@50-95 | 0.0513 | 0.2724 |

## 5. Improvement

V2 achieved higher Precision, Recall, mAP@50 and mAP@50-95
under the available evaluation setup.

## 6. Model

The trained V2 model is:

`runs/detect/runs/v2-2/weights/best.pt`

## 7. Prediction Examples

Five qualitative examples where V2 detected more objects than V1
are included in:

`comparison_examples/`

## 8. Conclusion

The experiment shows that improving a YOLO model is not simply about
training for more epochs. Improving the training data and using
appropriate augmentation can improve model performance.

## 9. Note

The original Day36 validation split was not available in the local
dataset. Therefore, V2 evaluation used the available training dataset
for validation. The V1 and V2 numbers should therefore be interpreted
as an available evaluation comparison rather than a perfectly
controlled benchmark.