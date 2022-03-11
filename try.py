import numpy as np
X1 = np.loadtxt("X_samples.csv", delimiter = ',', dtype=float)

print(X1.shape[0])
Y1 = np.loadtxt("Y_samples.csv", delimiter = ',', dtype=float)
print(Y1.shape[0])
X = np.array([1.5, 1.5, 1.2, 0.1, 0.2])
print(X)
print(X1.shape[0])
X1 = X1.T
print(X1.shape[0])
Y1 = Y1.reshape(2, Y1.shape[0])
print(Y1.shape[0])