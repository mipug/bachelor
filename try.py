import random
import numpy as np
X1 = np.loadtxt("X_samples.csv", delimiter = ',', dtype=float)

Y1 = np.loadtxt("Y_samples.csv", delimiter = ',', dtype=float)


Y1 = Y1.reshape(2, Y1.shape[0])


print(np.amax(X1))
sensors = np.array([3,5,6,2,5]) 
print(sensors.shape[0])

np.random.seed(42)

