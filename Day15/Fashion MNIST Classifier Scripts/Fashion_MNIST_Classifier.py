# This Program shows how to load and build CNN Project

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


# Load Dataset
(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()

# Class Names

class_names = [
    "T-shirt/Top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle Boot"
]

# Display Sample Images


plt.figure(figsize=(12,6))

for i in range(10):
    plt.subplot(2,5,i+1)
    plt.imshow(X_train[i], cmap="gray")
    plt.title(class_names[y_train[i]])
    plt.axis("off")

plt.tight_layout()
plt.show()


# Normalize Dataset

X_train = X_train.astype("float32") / 255.0
X_test = X_test.astype("float32") / 255.0

# Reshape Dataset


X_train = X_train.reshape(-1,28,28,1)
X_test = X_test.reshape(-1,28,28,1)

# Build CNN Model

model = Sequential()

model.add(Conv2D(32, (3,3), activation="relu", input_shape=(28,28,1)))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dense(10, activation="softmax"))


# Compile Model

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Train Model

history = model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2
)

# Evaluate Model

train_loss, train_accuracy = model.evaluate(X_train, y_train, verbose=0)
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)

print("\nTraining Accuracy :", train_accuracy)
print("Training Loss :", train_loss)

print("\nTest Accuracy :", test_accuracy)
print("Test Loss :", test_loss)

# Accuracy Graph

plt.figure(figsize=(8,5))

plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")

plt.title("Training vs Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

plt.show()

# Loss Graph

plt.figure(figsize=(8,5))

plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")

plt.title("Training vs Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.show()

# Predict Images

predictions = model.predict(X_test)

predicted_labels = np.argmax(predictions, axis=1)

# Show 10 Sample Predictions

plt.figure(figsize=(12,6))

for i in range(10):

    plt.subplot(2,5,i+1)

    plt.imshow(X_test[i].reshape(28,28), cmap="gray")

    plt.title(
        f"Actual: {class_names[y_test[i]]}\nPred: {class_names[predicted_labels[i]]}",
        fontsize=8
    )

    plt.axis("off")

plt.tight_layout()
plt.show()

# Confusion Matrix

cm = confusion_matrix(y_test, predicted_labels)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=class_names
)

fig, ax = plt.subplots(figsize=(10,10))
disp.plot(ax=ax, cmap="Blues", xticks_rotation=45)
plt.title("Confusion Matrix")
plt.show()

# Show 10 Correct Predictions

correct = np.where(predicted_labels == y_test)[0]

plt.figure(figsize=(12,8))

for i, index in enumerate(correct[:10]):

    plt.subplot(2,5,i+1)

    plt.imshow(X_test[index].reshape(28,28), cmap="gray")

    plt.title(
        f"Actual:\n{class_names[y_test[index]]}\n\nPred:\n{class_names[predicted_labels[index]]}",
        fontsize=8
    )

    plt.axis("off")

plt.suptitle("10 Correctly Classified Images")
plt.tight_layout()
plt.show()

# Show 10 Incorrect Predictions

incorrect = np.where(predicted_labels != y_test)[0]

plt.figure(figsize=(12,8))

for i, index in enumerate(incorrect[:10]):

    plt.subplot(2,5,i+1)

    plt.imshow(X_test[index].reshape(28,28), cmap="gray")

    plt.title(
        f"Actual:\n{class_names[y_test[index]]}\n\nPred:\n{class_names[predicted_labels[index]]}",
        fontsize=8
    )

    plt.axis("off")

plt.suptitle("10 Incorrectly Classified Images")
plt.tight_layout()
plt.show()