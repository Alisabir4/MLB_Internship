# This Program shows how to build CNN

import tensorflow as tf
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import matplotlib.pyplot as plt
import numpy as np


# Load Fashion MNIST Dataset


(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()

# Normalize the images
X_train = X_train.astype("float32") / 255.0
X_test = X_test.astype("float32") / 255.0

# Reshape for CNN (Height, Width, Channels)
X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)

# Build CNN Model


model = Sequential([
    Conv2D(
        filters=32,
        kernel_size=(3, 3),
        activation="relu",
        input_shape=(28, 28, 1)
    ),

    MaxPooling2D(pool_size=(2, 2)),

    Flatten(),

    Dense(128, activation="relu"),

    Dense(10, activation="softmax")
])


# Display Model Summary


model.summary()


# Compile the Model

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Train the Model

history = model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2
)

print("\nCNN model training completed successfully!")


# Evaluate on Training Data

train_loss, train_accuracy = model.evaluate(X_train, y_train, verbose=0)

print("Training Accuracy :", train_accuracy)
print("Training Loss     :", train_loss)


# Evaluate on Test Data


test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)

print("Test Accuracy :", test_accuracy)
print("Test Loss     :", test_loss)

# Plot Accuracy Graph

plt.figure(figsize=(8,5))

plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")

plt.title("Model Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

plt.show()

# Plot Loss Graph

plt.figure(figsize=(8,5))

plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")

plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.show()

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

# Make Predictions

predictions = model.predict(X_test)

predicted_labels = np.argmax(predictions, axis=1)

# Display 10 Sample Predictions


plt.figure(figsize=(12,6))

for i in range(10):

    plt.subplot(2,5,i+1)

    plt.imshow(X_test[i].reshape(28,28), cmap="gray")

    plt.title(
        f"Actual: {class_names[y_test[i]]}\n"
        f"Pred: {class_names[predicted_labels[i]]}",
        fontsize=9
    )

    plt.axis("off")

plt.tight_layout()
plt.show()