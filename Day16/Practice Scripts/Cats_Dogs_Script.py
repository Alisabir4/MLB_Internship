import tensorflow as tf
import tensorflow_datasets as tfds

IMG_SIZE = 160
BATCH_SIZE = 32

# Load dataset
dataset, info = tfds.load(
    "cats_vs_dogs",
    with_info=True,
    as_supervised=True
)

dataset = dataset["train"]

# Preprocessing function
def preprocess(image, label):
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

dataset = dataset.map(preprocess)

# Shuffle
dataset = dataset.shuffle(2000)

# Split dataset
train_size = int(0.8 * info.splits["train"].num_examples)

train_dataset = dataset.take(train_size)
val_dataset = dataset.skip(train_size)

train_dataset = train_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
val_dataset = val_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

print("Training batches:", len(train_dataset))
print("Validation batches:", len(val_dataset))