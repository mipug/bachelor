from Functions import *

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


input = 5 # 5 sensor + 1 bias
hidden_size = 2
popsize = 18

first_generation_W1, first_generation_W2 = InitializeGeneration(popsize, hidden_size) 

plot = False
f = open("coordinates.csv", "w")
s = open('fitness.csv', 'w')


RunExperiment(depth = 10, popsize = popsize, hidden_size = hidden_size)
s.close()
f.close()