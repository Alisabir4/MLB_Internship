# This Program shows how to build Neural Network
import tensorflow as tf
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
import matplotlib.pyplot as plt
import numpy as np


# Class Labels


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


# Load Dataset


print("Loading Fashion MNIST Dataset")


(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()


# Explore Dataset

print("\nTraining Images Shape :", X_train.shape)
print("Training Labels Shape :", y_train.shape)

print("\nTesting Images Shape :", X_test.shape)
print("Testing Labels Shape :", y_test.shape)

print("\nUnique Labels :", np.unique(y_train))


# Display Sample Images

plt.figure(figsize=(10, 5))

for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(X_train[i], cmap="gray")
    plt.title(class_names[y_train[i]])
    plt.axis("off")

plt.tight_layout()
plt.show()

# Normalize Images


X_train = X_train / 255.0
X_test = X_test / 255.0

print("\nImages Normalized Successfully!")

# Build ANN Model


model = Sequential([
    Flatten(input_shape=(28, 28)),

    Dense(128, activation="relu"),

    Dense(64, activation="relu"),

    Dense(10, activation="softmax")
])

# Compile Model


model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# Model Summary


print("\n")
model.summary()


# Train Model

print("\nTraining Model...\n")

history = model.fit(
    X_train,
    y_train,
    epochs=10,
    validation_split=0.2,
    verbose=1
)

# Evaluate Model


print("\nEvaluating Model...\n")

test_loss, test_accuracy = model.evaluate(
    X_test,
    y_test,
    verbose=0
)

print(f"Test Accuracy : {test_accuracy:.4f}")
print(f"Test Loss     : {test_loss:.4f}")


# Training & Validation Accuracy


print("\nFinal Training Accuracy :",
      history.history["accuracy"][-1])

print("Final Validation Accuracy :",
      history.history["val_accuracy"][-1])


# Make Predictions

predictions = model.predict(X_test)

print("\nSample Predictions\n")

for i in range(5):

    predicted = np.argmax(predictions[i])

    actual = y_test[i]

    print(f"Image {i+1}")

    print("Predicted :", class_names[predicted])

    print("Actual    :", class_names[actual])

    

# Bonus Accuracy Curve

plt.figure(figsize=(8, 5))

plt.plot(history.history["accuracy"], label="Training Accuracy")

plt.plot(history.history["val_accuracy"],
         label="Validation Accuracy")

plt.title("Training vs Validation Accuracy")

plt.xlabel("Epoch")

plt.ylabel("Accuracy")

plt.legend()

plt.grid(True)

plt.savefig("accuracy_curve.png")

plt.show()


# Display Predictions


plt.figure(figsize=(12, 8))

for i in range(9):

    plt.subplot(3, 3, i + 1)

    plt.imshow(X_test[i], cmap="gray")

    predicted = np.argmax(predictions[i])

    actual = y_test[i]

    plt.title(
        f"P:{class_names[predicted]}\nA:{class_names[actual]}"
    )

    plt.axis("off")

plt.tight_layout()

plt.savefig("sample_predictions.png")

plt.show()

print("\nProject Completed Successfully!")