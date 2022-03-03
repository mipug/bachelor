
from tkinter import FALSE
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

left_wheel_velocity =  random()   # robot left wheel velocity in radians/s
right_wheel_velocity =  random()  # robot right wheel velocity in radians/s





# KINEMATIC MODEL
# updates robot position and heading based on velocity of wheels and the elapsed time
# the equations are a forward kinematic model of a two-wheeled robot - don't worry just use it
def simulationstep():
    global x, y, q_mid, q_mid_left, q_mid_right, q_left, q_right

    for step in range(int(robot_timestep/simulation_timestep)):    #step model time/timestep times (0.1/0.1)
        v_x = cos(q_mid)*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2) 
        v_y = sin(q_mid)*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2)
        omega = (R*right_wheel_velocity - R*left_wheel_velocity)/(2*L)  
        

        x += v_x * simulation_timestep
        y += v_y * simulation_timestep
        q_mid += omega * simulation_timestep
        q_mid_left += omega * simulation_timestep
        q_mid_right += omega * simulation_timestep
        q_left += omega * simulation_timestep
        q_right += omega * simulation_timestep

# SIMULATION LOOP
# SENERE PROJEKT: lave 'log' over koordinater så vi kan gemme og se/plotte en specific robot iteration's rute senere
plot = False
f = open("coordinates.csv", "w")
for cnt in range(20000):
    robot = LineString([(x-0.20,y-0.20), (x+0.20,y-0.20), (x+0.20,y+0.20), (x-0.20,y+0.20),(x-0.20,y-0.20)])
    ray_mid = LineString([(x, y), ((x+cos(q_mid)),(y+sin(q_mid)))])  # a line from robot to a point outside arena in direction of q
    ray_mid_left = LineString([(x, y), ((x+cos(q_mid_left)),(y+sin(q_mid_left)))])  
    ray_mid_right = LineString([(x, y), ((x+cos(q_mid_right)),(y+sin(q_mid_right)))])  
    ray_left = LineString([(x, y), ((x+cos(q_left)),(y+sin(q_left)))])
    ray_right = LineString([(x, y), ((x+cos(q_right)),(y+sin(q_right)))])
    s_mid = world.intersects(ray_mid)
    s_mid_left = world.intersects(ray_mid_left)
    s_mid_right = world.intersects(ray_mid_right)
    s_left = world.intersects(ray_left)
    s_right = world.intersects(ray_right)
    #print(ray1.length)
    f.write(str(x) + ',' + str(y) + '\n')

    # PLOT THE ROBOT
    if plot == True:
        if cnt%100==0:
            plt.figure(figsize =(5,5))
            plt.xticks(range(-5,5))
            plt.yticks(range(-5,5))
            for line in world:
                plt.plot(*line.xy, color='black')
            plt.plot(*robot.xy, color='blue')
            plt.plot(*ray_mid.xy, color='red', linestyle='dashed')
            plt.plot(*ray_mid_left.xy, color='red', linestyle='dashed')
            plt.plot(*ray_mid_right.xy, color='red', linestyle='dashed')
            plt.plot(*ray_left.xy, color='red', linestyle='dashed')
            plt.plot(*ray_right.xy, color='red', linestyle='dashed')
            print(cnt)
            plt.pause(0.1)
        
    #simple controller - change direction of wheels every 10 seconds (100*robot_timestep) unless close to wall then turn on spot
    if (s_left == True): 
        if ((s_mid == False) and (s_mid_left == False)): # Hvis væg på venstre side drej til højre of følg væggen
            # FORWARD
            left_wheel_velocity = 0.5
            right_wheel_velocity = 0.5
            print("ligeud")
        
        # Hvis robot er ved at ramme venstre væg drej til højre
        if s_mid_left == True:
            left_wheel_velocity = 0.5
            right_wheel_velocity = -0.5
            print("højre")

    elif (s_mid == True): # Hvis væg lige foran robot, drej til højre
        # RIGHT
        left_wheel_velocity = 0.5
        right_wheel_velocity = -0.5
        print("højre")
    
    elif (s_mid == s_mid_left == s_mid_right == s_left == s_right == False): # hvis ingen vægge, drej til venstre
        left_wheel_velocity = 0.5
        right_wheel_velocity = 0.65
        print("alt False")

    else:   
        left_wheel_velocity = 0.5
        right_wheel_velocity = 0.5
        print("hej")
        
    
        """if cnt%100==0:
            left_wheel_velocity = random()
            right_wheel_velocity = random()"""
    
    """VORES ROBOT: Skal følge venstre væg/sensor
    If distance_forward>0.5 AND distance_left < 0.5:
    kør ligud. """
        
    #step simulation
    simulationstep()

    #check collision with arena walls 
    if (world.distance(Point(x,y))<L/2):
        break
    if ((goal.distance(Point(x,y))<L/2)):
        print('WINNER')
        break
f.close()
if plot == True:
    plt.show()




    
