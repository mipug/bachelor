
from tkinter import FALSE
import shapely
from shapely.geometry import LinearRing, LineString, Point, MultiLineString
from numpy import sin, cos, pi, sqrt
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
print(world)

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
    #print(s)
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


# SIMULATION LOOP
# SENERE PROJEKT: lave 'log' over koordinater s?? vi kan gemme og se/plotte en specific robot iteration's rute senere
plot = False
f = open("coordinates.csv", "w")
f_X = open("X_samples.csv", "w")
f_Y = open("Y_samples.csv", "w")
for cnt in range(50000):
    robot = LineString([(x-0.20,y-0.20), (x+0.20,y-0.20), (x+0.20,y+0.20), (x-0.20,y+0.20),(x-0.20,y-0.20)])


    ray_mid, s_mid = makeray(q_all[0]) # a line from robot to a point outside arena in direction of q
    ray_mid_left, s_mid_left = makeray(q_all[1]) 
    ray_mid_right, s_mid_right = makeray(q_all[2]) 
    ray_left, s_left = makeray(q_all[3]) 
    ray_right, s_right = makeray(q_all[4]) 
    print(cnt, s_mid, s_mid_left, s_mid_right, s_left, s_right)

    f.write(str(x) + ',' + str(y) + '\n')
    f_X.write(str(s_mid)+ ',' + str(s_mid_left) + ',' + str(s_mid_right) + ',' + str(s_left) + ',' + str(s_right)+ '\n')

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
            #print(cnt)
            plt.pause(0.1)
        
    #simple controller - change direction of wheels every 10 seconds (100*robot_timestep) unless close to wall then turn on spot
    if (s_left <= 1): 
        if ((s_mid >= 1) and (s_mid_left >= 1)): # Hvis v??g p?? venstre side drej til h??jre of f??lg v??ggen
            # FORWARD
            left_wheel_velocity = 0.5
            right_wheel_velocity = 0.5
            print("ligeud", left_wheel_velocity, right_wheel_velocity)
        
        # Hvis robot er ved at ramme venstre v??g drej til h??jre
        if s_mid_left <= 1:
            left_wheel_velocity = 0.5
            right_wheel_velocity = -0.5
            print("h??jre", left_wheel_velocity, right_wheel_velocity)

    elif (s_mid <= 1): # Hvis v??g lige foran robot, drej til h??jre
        # RIGHT
        left_wheel_velocity = 0.5
        right_wheel_velocity = -0.5
        print("h??jre", left_wheel_velocity, right_wheel_velocity)
    
    elif ((s_mid >=1) and (s_mid_left>=1) and (s_mid_right>=1)  and (s_left >=1) and (s_right >= 1)): # hvis ingen v??gge, drej til venstre
        left_wheel_velocity = 0.5
        right_wheel_velocity = 0.65
        print("alt False", left_wheel_velocity, right_wheel_velocity)

    else:   
        left_wheel_velocity = 0.5
        right_wheel_velocity = 0.65
        print("hej", left_wheel_velocity, right_wheel_velocity)
        
    
        """if cnt%100==0:
            left_wheel_velocity = random()
            right_wheel_velocity = random()"""
    
    """VORES ROBOT: Skal f??lge venstre v??g/sensor
    If distance_forward>0.5 AND distance_left < 0.5:
    k??r ligud. """
        
    f_Y.write(str(left_wheel_velocity) + ',' + str(right_wheel_velocity)+ '\n')
    #step simulation
    simulationstep()

    #check collision with arena walls 
    if (world.distance(Point(x,y))<L/2):
        break
    if ((goal.distance(Point(x,y))<L/2)):
        print('WINNER')
        break

### Neural net
lr = 1
bias = 1
weights = [random() for i in range(6)] # 5 sensors and bias
sensors = [s_mid, s_mid_left, s_left, s_mid_right, s_right] #distances
#print("w", weights)

f.close()
f_X.close()
f_Y.close()
if plot == True:
    plt.show()