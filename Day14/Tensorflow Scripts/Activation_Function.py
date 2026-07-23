# This program show how to experiment with different functions

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


# Function to create model
def create_model(activation_name):

    model = Sequential([
        Dense(16,
              activation=activation_name,
              input_shape=(4,),
              name="Hidden_Layer"),

        Dense(1,
              activation="sigmoid",
              name="Output_Layer")
    ])

    return model


activation_functions = [
    "relu",
    "sigmoid",
    "tanh"
]

for activation in activation_functions:

    print(f"Activation Function : {activation.upper()}")
    

    model = create_model(activation)

    model.summary()

    print("\nHidden Layer Activation:",
          model.layers[0].activation.__name__)

    print("Output Layer Activation:",
          model.layers[1].activation.__name__)