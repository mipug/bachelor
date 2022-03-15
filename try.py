import random
import numpy as np
X1 = np.loadtxt("X_samples.csv", delimiter = ',', dtype=float)

Y1 = np.loadtxt("Y_samples.csv", delimiter = ',', dtype=float)
print(Y1.shape[0])

print(X1.shape[0])
X1 = X1.T

Y1 = Y1.reshape(2, Y1.shape[0])
print(Y1.shape[0])



X = np.array([1.5, 1.5, 1.2, 0.1, 0.2])
print(X)

np.random.seed(42)
W1 = np.random.random(size = (2, 5))
print(W1)
b1 = 0
Z1 = np.dot(W1, X) + b1

print(Z1)
A1 = np.tanh(Z1) 
print("A1", A1)

W2 = np.random.random(size = (2, 2))
Z2 = np.dot(W2, A1)
print("Z2: ", Z2)

y = np.tanh(Z2)

print("y: ", y)