# This program show how to install tensorflow
import tensorflow as tf
from tensorflow import keras


print("TensorFlow Installation Verification")


print("TensorFlow Version :", tf.__version__)
print("Keras Version      :", keras.__version__)

print("\nTensorFlow imported successfully!")
print("Keras imported successfully!")

print("\nChecking available devices...")
print(tf.config.list_physical_devices())

print("\nGPU Available:", len(tf.config.list_physical_devices('GPU')) > 0)

print("\nInstallation Verified Successfully!")