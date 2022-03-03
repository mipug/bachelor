
import shapely
from shapely.geometry import LinearRing, LineString, Point, MultiLineString
from numpy import sin, cos, pi, sqrt
from random import random
import matplotlib.pyplot as plt
import math

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
        ((1,-1),(1,2)),
        ]
world = MultiLineString(walls)
print(world)




# VARIABLES

x = 0.0   # robot position in meters - x direction - positive to the right 
y = 0.0   # robot position in meters - y direction - positive up
q1 = 0.0   # robot heading with respect to x-axis in radians 
q2 = 0.75
q3 = -0.75

left_wheel_velocity =  random()   # robot left wheel velocity in radians/s
right_wheel_velocity =  random()  # robot right wheel velocity in radians/s





# KINEMATIC MODEL
# updates robot position and heading based on velocity of wheels and the elapsed time
# the equations are a forward kinematic model of a two-wheeled robot - don't worry just use it
def simulationstep():
    global x, y, q1, q2, q3

    for step in range(int(robot_timestep/simulation_timestep)):    #step model time/timestep times (0.1/0.1)
        v_x = cos(q1)*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2) 
        v_y = sin(q1)*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2)
        omega1 = (R*right_wheel_velocity - R*left_wheel_velocity)/(2*L)  
        omega2 = (R*right_wheel_velocity - R*left_wheel_velocity)/(2*L)    
        omega3 = (R*right_wheel_velocity - R*left_wheel_velocity)/(2*L) 
        

        x += v_x * simulation_timestep
        y += v_y * simulation_timestep
        q1 += omega1 * simulation_timestep
        q2 += omega2 * simulation_timestep
        q3 += omega3 * simulation_timestep

# SIMULATION LOOP
# SENERE PROJEKT: lave 'log' over koordinater så vi kan gemme og se/plotte en specific robot iteration's rute senere

for cnt in range(10000):
    robot = LineString([(x-0.20,y-0.20), (x+0.20,y-0.20), (x+0.20,y+0.20), (x-0.20,y+0.20),(x-0.20,y-0.20)])
    ray1 = LineString([(x, y), ((x+cos(q1)),(y+sin(q1)))])  # a line from robot to a point outside arena in direction of q
    ray2 = LineString([(x, y), ((x+cos(q2)),(y+sin(q2)))])
    ray3 = LineString([(x, y), ((x+cos(q3)),(y+sin(q3)))])
    s = world.intersects(ray1)
    #print(ray1.length)
    
    # PLOT THE ROBOT
    if cnt%100==0:
        plt.figure(figsize =(10,10))
        plt.xticks(range(-5,5))
        plt.yticks(range(-5,5))
        for line in world:
            plt.plot(*line.xy, color='black')
        plt.plot(*robot.xy, color='blue')
        plt.plot(*ray1.xy, color='red', linestyle='dashed')
        plt.plot(*ray2.xy, color='red', linestyle='dashed')
        plt.plot(*ray3.xy, color='red', linestyle='dashed')
        print(cnt)
        plt.pause(0.1)
        
    #simple controller - change direction of wheels every 10 seconds (100*robot_timestep) unless close to wall then turn on spot
    if (s == True): # TURN RIGHT
        left_wheel_velocity = 0.5
        right_wheel_velocity = -0.5
    else:                
        if cnt%100==0:
            left_wheel_velocity = random()
            right_wheel_velocity = random()
    
    """VORES ROBOT: Skal følge venstre væg/sensor
    If distance_forward>0.5 AND distance_left < 0.5:
    kør ligud. """
        
    #step simulation
    simulationstep()

    #check collision with arena walls 
    if (world.distance(Point(x,y))<L/2):
       break

plt.show()




    
