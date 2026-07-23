import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np

IMG_SIZE = 160
BATCH_SIZE = 32
EPOCHS = 5

# Load Dataset


dataset, info = tfds.load(
    "cats_vs_dogs",
    with_info=True,
    as_supervised=True
)

dataset = dataset["train"]

# Data Augmentation


data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.2),
    tf.keras.layers.RandomZoom(0.2)
])

# Preprocessing


def preprocess(image, label):
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

dataset = dataset.map(preprocess)

dataset = dataset.shuffle(3000)

train_size = int(0.8 * info.splits["train"].num_examples)

train_dataset = dataset.take(train_size)
val_dataset = dataset.skip(train_size)

train_dataset = train_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
val_dataset = val_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)


# Load MobileNetV2


base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

# Build Model


inputs = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))

x = data_augmentation(inputs)

x = tf.keras.applications.mobilenet_v2.preprocess_input(x * 255)

x = base_model(x, training=False)

x = tf.keras.layers.GlobalAveragePooling2D()(x)

x = tf.keras.layers.Dropout(0.2)(x)

x = tf.keras.layers.Dense(128, activation="relu")(x)

outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)

model = tf.keras.Model(inputs, outputs)


# Compile


model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()


# Train


history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=EPOCHS
)


# Evaluate


loss, accuracy = model.evaluate(val_dataset)

print("\nValidation Accuracy:", accuracy)

# Fine Tuning


base_model.trainable = True

for layer in base_model.layers[:-30]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-5),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

fine_history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=5
)


# Plot Accuracy


acc = history.history["accuracy"] + fine_history.history["accuracy"]
val_acc = history.history["val_accuracy"] + fine_history.history["val_accuracy"]

loss = history.history["loss"] + fine_history.history["loss"]
val_loss = history.history["val_loss"] + fine_history.history["val_loss"]

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(acc, label="Training")
plt.plot(val_acc, label="Validation")
plt.title("Accuracy")
plt.legend()

plt.subplot(1,2,2)
plt.plot(loss, label="Training")
plt.plot(val_loss, label="Validation")
plt.title("Loss")
plt.legend()

plt.show()


# Sample Predictions


class_names = ["Cat", "Dog"]

images, labels = next(iter(val_dataset))

predictions = model.predict(images)

plt.figure(figsize=(12,12))

for i in range(9):

    plt.subplot(3,3,i+1)

    plt.imshow(images[i])

    pred = 1 if predictions[i] > 0.5 else 0

    plt.title(f"Pred: {class_names[pred]}\nTrue: {class_names[labels[i]]}")

    plt.axis("off")

plt.show()