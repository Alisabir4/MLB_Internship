# README

## What is Transfer Learning?

Transfer Learning is a deep learning technique in which a model that has already been trained on a large dataset is reused for a different but related task. Instead of training a neural network from scratch, a pre-trained model is used as a feature extractor, and only the final classification layers are trained on the new dataset. This approach reduces training time, requires less data, and often produces higher accuracy.

---

## Why did you choose MobileNetV2?

MobileNetV2 was selected because it is a lightweight and highly efficient convolutional neural network designed for image classification. It provides excellent accuracy while requiring fewer computational resources than many larger models. Since it is pre-trained on the ImageNet dataset, it has already learned useful image features that can be transferred to the Cats vs Dogs classification task.

---

## What experiments did you perform to improve accuracy?

To improve the model's performance, the following experiments were performed:

- Applied data augmentation (random flip, rotation, and zoom) to reduce overfitting.
- Used MobileNetV2 with ImageNet pre-trained weights.
- Initially froze the base model to train only the custom classification layers.
- Fine-tuned the last layers of MobileNetV2 after the initial training phase.
- Used the Adam optimizer with a lower learning rate during fine-tuning.
- Trained the model for multiple epochs and monitored validation accuracy and loss.

---

## Final Validation Accuracy

**Final Validation Accuracy:** **_________%**

> Replace the blank with the final validation accuracy displayed after training (for example, **93.4%**).

---

## Key Challenges and Lessons Learned

### Challenges

- Setting up TensorFlow and required libraries.
- Loading the Cats vs Dogs dataset.
- Handling corrupted images in the dataset.
- Selecting suitable hyperparameters such as learning rate and number of epochs.
- Preventing overfitting while maintaining good validation accuracy.

### Lessons Learned

- Transfer Learning significantly reduces training time compared to training a model from scratch.
- MobileNetV2 provides strong performance even with limited training time.
- Data augmentation improves model generalization.
- Fine-tuning pre-trained layers can further improve validation accuracy.
- Proper preprocessing and dataset organization are essential for successful image classification.