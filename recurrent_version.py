import shapely
from shapely.geometry import LinearRing, LineString, Point, MultiLineString
from numpy import sin, cos, pi, sqrt, genfromtxt
from random import random
import matplotlib.pyplot as plt
import math
import numpy as np


# A simulation of a differential-drive robot with x sensors

# CONSTANTS

R = 0.02  # radius of wheels in meters
L = 0.10  # distance between wheels in meters

W = 10.0  # width of arena
H = 10.0  # height of arena

robot_timestep = 0.1        # 1/robot_timestep (10) equals update frequency of robot
simulation_timestep = 0.1  # timestep in kinematics simulation (probably don't touch..)

# the world is a quadratic arena with width W and height H
# it contains walls of various sizes and directions to create a maze environment
walls = [
        ((W/2,H/2),(-W/2,H/2),(-W/2,-H/2),(W/2,-H/2),(W/2,H/2)),
        ((3,-5),(-3,-1)),
        ((-1, 5), (-3, 2)), 
        ((-1, -2.3), (1 , 0)),
        ((5, 0), (3, -2)),
        ((-2.0, 3.5), (1, 2))]
world = MultiLineString(walls)
goal = Point(4,4)


# VARIABLES

x = -4.0   # robot position in meters - x direction - positive to the right 
y = 4.0   # robot position in meters - y direction - positive up
q_mid = 0.0 
q_mid_left = 0.5
q_mid_right = -0.5  # robot heading with respect to x-axis in radians 
q_left = 1
q_right = -1
q_all = [q_mid, q_mid_left, q_mid_right, q_left, q_right]

left_wheel_velocity =  random()   # robot left wheel velocity in radians/s
right_wheel_velocity =  random()  # robot right wheel velocity in radians/s

def makeray(q):
    ray = LineString([(x, y), (x+cos(q)*10,y+sin(q)*10)])
    #s = world.distance(ray)
    s = 1000
    for line in world:
        intersect = ray.intersection(line)
        try:
            distance = sqrt((intersect.x-x)**2+(intersect.y-y)**2) 
            if distance < s:
                s = distance
        except:
            pass
    return ray, s



# KINEMATIC MODEL
# updates robot position and heading based on velocity of wheels and the elapsed time
# the equations are a forward kinematic model of a two-wheeled robot - don't worry just use it
def simulationstep():
    global x, y, q_all#, q_mid, q_mid_left, q_mid_right, q_left, q_right

    for step in range(int(robot_timestep/simulation_timestep)):    #step model time/timestep times (0.1/0.1)
        v_x = cos(q_all[0])*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2) 
        v_y = sin(q_all[0])*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2)
        omega = (R*right_wheel_velocity - R*left_wheel_velocity)/(2*L)  
        

        x += v_x * simulation_timestep
        y += v_y * simulation_timestep
        for i in range(len(q_all)): 
            q_all[i] += omega * simulation_timestep



input = 6 # 5 sensor + 1 bias
hidden_size = 2


def setParameters(X1, Y1, hidden_size):
    np.random.seed(42)
    input_size = X1.shape[0] # number of neurons in input layer
    output_size = 1 #Y1.shape[0] # number of neurons in output layer.
    W1 = np.random.random(size = (hidden_size, input_size))
    b1 = np.zeros((hidden_size, 1))
    W2 = np.random.random(size = (output_size, hidden_size))
    b2 = np.zeros((output_size, 1))
    return W1, b1, W2, b2


def softmax(x):
    return np.exp(x)/np.sum(np.exp(x))

def forwardPropagation(X1, W1, b1, W2, b2): 
    Z1 = np.dot(W1, X1) + b1
    print("Z1: ", Z1)
    A1 = np.tanh(Z1) 
    Z2 = np.dot(W2, A1) + b2
    print("Z2: ", Z2)
    y1 = np.tanh(Z2) 
    #skaler ouptut til at ligge mellem .25 og -.25
    return y1, A1

X1 = np.array([1.5, 1.5, 1.2, 0.1, 0.2])
Y1 = np.array([0.5, -0.5])
W1, b1, W2, b2 = setParameters(X1, Y1, hidden_size)

# SIMULATION LOOP
plot = True
f = open("coordinates.csv", "w")
for cnt in range(10000):
    robot = LineString([(x-0.20,y-0.20), (x+0.20,y-0.20), (x+0.20,y+0.20), (x-0.20,y+0.20),(x-0.20,y-0.20)])


    ray_mid, s_mid = makeray(q_all[0]) # a line from robot to a point outside arena in direction of q
    ray_mid_left, s_mid_left = makeray(q_all[1]) 
    ray_mid_right, s_mid_right = makeray(q_all[2]) 
    ray_left, s_left = makeray(q_all[3]) 
    ray_right, s_right = makeray(q_all[4]) 
    f.write(str(x) + ',' + str(y) + '\n')

    
    sensors = np.array([s_left, s_mid_left, s_mid, s_mid_right, s_right])
    #sensors = sensors.T

    y1, _ = forwardPropagation(sensors, W1, b1, W2, b2)
    print('y1:', y1)
    left_wheel_velocity, right_wheel_velocity = y1[0], y1[1]
    print("left: ", cnt)

    # PLOT THE ROBOT
    if plot == True:
        if cnt%100==0:
            plt.figure(figsize =(5,5))
            plt.xticks(range(-5,5))
            plt.yticks(range(-5,5))
            for line in world:
                plt.plot(*line.xy, color='black')
            plt.plot(*robot.xy, color='blue')
            for r in [ray_mid, ray_mid_left, ray_mid_right, ray_left, ray_right]:
                plt.plot(*r.xy, color='red', linestyle='dashed')
            print(cnt)
            plt.pause(0.1)

    simulationstep()
    print(x,y)
    if (world.distance(Point(x,y))<L/2):
        break
    if ((goal.distance(Point(x,y))<L/2)):
        print('WINNER')
        break
f.close()
if plot == True:
    plt.show()