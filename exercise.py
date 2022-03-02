import shapely
from shapely.geometry import LinearRing, LineString, Point, Polygon
from numpy import sin, cos, pi, sqrt
from random import random
import matplotlib.pyplot as plt

# A prototype simulation of a differential-drive robot with one sensor

# Constants
###########
R = 0.02  # radius of wheels in meters
L = 0.10  # distance between wheels in meters

W = 4.0   # width of arena
H = 4.0   # height of arena

robot_timestep = 0.1        # 1/robot_timestep equals update frequency of robot
simulation_timestep = 0.01  # timestep in kinematics sim (probably don't touch..)

# the world is a rectangular arena with width W and height H
world = Polygon([(W/2,H/2),(-W/2,H/2),(-W/2,-H/2),(W/2,-H/2)]) 
wall = LineString([(-1, -2), (0, -1)])
wall2 = LineString([(-1, 2), (0, 1)])


print(world)

#coor = wall.coords
for x, y in wall.coords:
    print("x={}, y={}".format(x, y))
#print(list(coor))

x, y = world.exterior.xy
plt.plot(x,y)
plt.plot(*wall.xy)
plt.plot(*wall2.xy)
plt.show()