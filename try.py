import random
import numpy as np
X1 = np.loadtxt("X_samples.csv", delimiter = ',', dtype=float)

Y1 = np.loadtxt("Y_samples.csv", delimiter = ',', dtype=float)


Y1 = Y1.reshape(2, Y1.shape[0])


print(np.amax(X1))
sensors = np.array([3,5,6,2,5]) 
print(sensors.shape[0])

#np.random.seed(42)


start_List = [[-4.0, 4.0], [0, -4], [-2, -2.2], [4, -2]]
print(type(start_List))

new = random.choice(start_List)

print("new: ", new)

print("X: ", new[0], "y: ", new[1])

Weight = np.random.uniform(-3,3)

print(Weight)

print("what", np.absolute(0.25-(-0.25)))