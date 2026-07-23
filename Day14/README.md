# Deep Learning Project README

## What is Deep Learning?

Deep Learning is a branch of Machine Learning that uses Artificial Neural Networks (ANNs) with multiple hidden layers to automatically learn patterns and features from large amounts of data. It is widely used in image recognition, speech recognition, natural language processing, and recommendation systems.

## Difference Between Machine Learning and Deep Learning

| Machine Learning                                                   | Deep Learning                                                       |
| ------------------------------------------------------------------ | ------------------------------------------------------------------- |
| Requires manual feature engineering.                               | Automatically learns features from raw data.                        |
| Works well with small to medium-sized datasets.                    | Performs best with large datasets.                                  |
| Training is generally faster.                                      | Training is more computationally intensive and often requires GPUs. |
| Simpler models such as Linear Regression, Decision Trees, and SVM. | Uses multi-layer Artificial Neural Networks (ANNs).                 |
| Easier to interpret.                                               | More complex and often considered a "black box."                    |

## What is a Perceptron?

A Perceptron is the simplest type of artificial neural network and serves as the basic building block of deep learning models. It receives input values, applies weights and a bias, computes a weighted sum, passes it through an activation function, and produces an output for binary classification.

## Activation Functions Explored

* **ReLU (Rectified Linear Unit):** Most commonly used in hidden layers because it is computationally efficient and helps reduce the vanishing gradient problem.
* **Sigmoid:** Produces output values between 0 and 1. Commonly used for binary classification output layers.
* **Softmax:** Converts outputs into probability distributions across multiple classes. Commonly used in the output layer for multi-class classification problems, such as Fashion MNIST.

## Model Performance

* **Final Training Accuracy:** 0.9111875295639038
* **Final Testing Accuracy:** 0.8818333148956299
