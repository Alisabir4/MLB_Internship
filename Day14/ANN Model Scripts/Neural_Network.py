# This program shows how to build neural network

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Create the neural network
model = Sequential()

# Input Layer + Hidden Layer
model.add(Dense(
    units=16,
    activation="relu",
    input_shape=(4,),
    name="Hidden_Layer"
))

# Output Layer
model.add(Dense(
    units=1,
    activation="sigmoid",
    name="Output_Layer"
))

# Print model summary

print("Neural Network Summary")


model.summary()

print("\nLayer Explanation")


for layer in model.layers:
    print(f"Layer Name       : {layer.name}")
    print(f"Layer Type       : {layer.__class__.__name__}")
    print(f"Number of Neurons: {layer.units}")
    print(f"Activation       : {layer.activation.__name__}")
    