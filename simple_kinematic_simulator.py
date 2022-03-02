import shapely
from shapely.geometry import LinearRing, LineString, Point, MultiLineString
from numpy import sin, cos, pi, sqrt
from random import random
import matplotlib.pyplot as plt

# A prototype simulation of a differential-drive robot with one sensor

# Constants
###########
R = 0.02  # radius of wheels in meters
L = 0.10  # distance between wheels in meters

W = 2.0  # width of arena
H = 2.0  # height of arena

robot_timestep = 0.1        # 1/robot_timestep equals update frequency of robot
simulation_timestep = 0.01  # timestep in kinematics sim (probably don't touch..)

# the world is a rectangular arena with width W and height H
walls = [
        ((W/2,H/2),(-W/2,H/2),(-W/2,-H/2),(W/2,-H/2),(W/2,H/2)),
        ((-0.75,-1),(-0.5,-0.25)),
        ((0.26, -0.25), (0.26, 0.25))
        ]
world = MultiLineString(walls)
print(world)


# Variables 
###########

x = 0.0   # robot position in meters - x direction - positive to the right 
y = 0.0   # robot position in meters - y direction - positive up
q = 0.0   # robot heading with respect to x-axis in radians 

left_wheel_velocity =  random()   # robot left wheel velocity in radians/s
right_wheel_velocity =  random()  # robot right wheel velocity in radians/s

# Kinematic model
#################
# updates robot position and heading based on velocity of wheels and the elapsed time
# the equations are a forward kinematic model of a two-wheeled robot - don't worry just use it
def simulationstep():
    global x, y, q

    for step in range(int(robot_timestep/simulation_timestep)):     #step model time/timestep times
        v_x = cos(q)*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2) 
        v_y = sin(q)*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2)
        omega = (R*right_wheel_velocity - R*left_wheel_velocity)/(2*L)    
    
        x += v_x * simulation_timestep
        y += v_y * simulation_timestep
        q += omega * simulation_timestep

# Simulation loop
#################
file = open("trajectory.dat", "w")

path = []

for cnt in range(5000):
    #simple single-ray sensor
    robot = LineString([(x-0.05,y-0.05), (x+0.05,y-0.05), (x+0.05,y+0.05), (x-0.05,y+0.05),(x-0.05,y-0.05)])
    ray = LineString([(x, y), ((x+cos(q))/4,(y+sin(q))/4) ])  # a line from robot to a point outside arena in direction of q
    #ray = LineString([(x, y), ((x+cos(q))*2*(H+W),(y+sin(q))*2*(H+W)) ])  # a line from robot to a point outside arena in direction of q
    s = world.intersects(ray)


    #distance = sqrt((s.x-x)**2+(s.y-y)**2)                    # distance to wall
    
    #path.append(Point(x,y).xy)
    #plt.plot(*world.xy)
    for line in world:
        plt.plot(*line.xy)
    plt.plot(*robot.xy)
    plt.plot(*ray.xy)
    plt.show()

    
    #simple controller - change direction of wheels every 10 seconds (100*robot_timestep) unless close to wall then turn on spot
    if (s == True):
        left_wheel_velocity = -0.4
        right_wheel_velocity = 0.4
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
        
    if cnt%50==0:
        file.write( str(x) + ", " + str(y) + ", " + str(cos(q)*0.2) + ", " + str(sin(q)*0.2) + "\n")

#print(path)
#pathAll = LineString([path])



file.close()
    
