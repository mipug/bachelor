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
    s = 10
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


##NEURAL NET #################
#X = np.array([1.5, 1.5, 1.2, 0.1, 0.2]) #sensor input
#Y = # wheels

input = 5 # 5 sensor + 1 bias
hidden_size = 2
popsize = 18



def GenerateGenom(hidden_layer, W):
    if W == 1:
        Weight = np.random.random(size = (hidden_layer, 5)) #(hidden_neurons, input_size)
    if W == 2:
        Weight = np.random.random(size = (2, hidden_layer)) #(Output_neurons, hidden_neurons)
    return Weight

def InitializeGeneration(popsize, hidden_layer):
    population_W1 = [GenerateGenom(hidden_layer,1) for i in range(popsize)]
    population_W2 = [GenerateGenom(hidden_layer,2) for i in range(popsize)]
    #print(population_W1)
    #print(population_W1)
    return population_W1, population_W2

def SelectTop(n, fitness, current_genW1, current_genW2):
    best_robots = np.argsort(fitness)[-n:]
    print('best fitness ',  fitness[best_robots])
    
    best_current_generation_W1 = [current_genW1[idx] for idx in best_robots]
    best_current_generation_W2 = [current_genW2[idx] for idx in best_robots]
    #print("best: ", best_current_generation_W1, best_current_generation_W2)
    return best_current_generation_W1, best_current_generation_W2
    

def Mutate(robot_W1, robot_W2, n):
    # rand,om int 0 or 1
    # for each input robot, mutate it n times
    # return the arrays of new weights
    #print('OG robot: ', robot_W1, robot_W2)
    new_robots_W1 = []
    new_robots_W2 = []
    
    for i in range(n):
        xxx = np.copy(robot_W1)
        mat_pick = np.random.randint(2) #choose randomly if W1 or W2 should be mutated
        #print("mat_pick: ", mat_pick)
        if mat_pick == 0: 
            for weight in range(xxx.shape[1]):
                random = np.random.uniform(0,1)
                #print("Weight: ", weight, "Random: ", random)
                if random <= 0.3:
                    #print("MUTATE!!!!")
                    #print("OLD!: ", xxx[0, weight])
                    xxx[0, weight] = np.random.uniform(0,1)
                    xxx[1, weight] = np.random.uniform(0,1)
                    #print("NEW!: ", xxx[0, weight])
                
            

        xxx2 = np.copy(robot_W2)
        if mat_pick == 1:
            for weight in range(xxx2.shape[1]):
                random = np.random.uniform(0,1)
                
                if random <= 0.4:
                    #print("OLD!: ", xxx2[0, weight])
                    xxx2[0, weight] = np.random.uniform(0,1)
                    xxx2[1, weight] = np.random.uniform(0,1)
                    #print("NEW: ", xxx2[0, weight])
        new_robots_W1.append(xxx)
        new_robots_W2.append(xxx2)
    #print("new_robots: ", new_robots_W1, new_robots_W2)   
    return new_robots_W1, new_robots_W2

def NewGeneration(best_current_gen_W1, best_current_gen_W2, n):
    print(best_current_gen_W1)
    new_gen_W1 = []
    new_gen_W2 = []
    for W1, W2 in zip(best_current_gen_W1, best_current_gen_W2): #Generates a batch of n mutated robots for every 'best robot' selected in selectTop
        print('hello')
        n_new_W1, n_new_W2 = Mutate(W1, W2, n)
        for W1, W2 in zip(n_new_W1, n_new_W2): # for every robot weigts in returned batch, append them to the list of the new generation
            #print('Success??: ')
            new_gen_W1.append(W1)
            new_gen_W2.append(W2)
    return new_gen_W1, new_gen_W2


def Fitness(V, diff, i): # evaluates the robot at each step between 0 and 1
    # V             -> average rotation speed -> (left_velocity + right_velocity) / 2
    # 1-sqrt(v)     -> square root of the absolute value of the difference speed values -> sqrt of |(left_velocity-right_velocity)|
    # i             -> i is the normalized value (0-1) of the closest distance to a wall -> if high distance then high value
    fitness = V*(1-np.sqrt(diff))*i
    return fitness


def forwardPropagation(X, W1, W2): 

    Z1 = np.dot(W1, X) #+ b1
    A1 = np.tanh(Z1) 

    Z2 = np.dot(W2, A1) #+ b2
    Y = np.tanh(Z2) 
    
    """print("x1 :", X1 ,"dot W1: ", W1)
    print("Z1: ", Z1)
    print("Z2: ", Z2)
    print("A1", A1)
    #skaler ouptut til at ligge mellem .25 og -.25"""
    return Y 


def Normalize(x, min, max):
    # min = 0, max = 5 (sensor distance)
    i = (x - min) / (max - min)
    return i


# SIMULATION LOOP
plot = False
f = open("coordinates.csv", "w")


### FIRST GENERATION
first_generation_W1, first_generation_W2 = InitializeGeneration(popsize, hidden_size) 
#print('W1: ', first_generation_W1, '\n W2: ', first_generation_W2)



def RunExperiment(depth, popsize, hidden_size):
    #simulate the first initialized generation
    first_generation_W1, first_generation_W2 = InitializeGeneration(popsize, hidden_size) 
    fitness_generation = Simulate(first_generation_W1, first_generation_W2)
    #print(fitness_generation)

    cw1, cw2 = SelectTop(3, fitness_generation, first_generation_W1, first_generation_W2)
    nw1, nw2 = NewGeneration(cw1, cw2, 5)
    
    # make new generations 'depth' number of times and run simulation on them
    gen_depth = 1
    for i in range(depth):
        print('depth: ', gen_depth)
        fitness_generation = Simulate(nw1, nw2)

        cw1, cw2 = SelectTop(3, fitness_generation, first_generation_W1, first_generation_W2)
        gen_depth += 1
        nw1, nw2 = NewGeneration(cw1, cw2, 5)
    #print(nw1, nw2)


def Simulate(current_generation_W1, current_generation_W2):
    robot_depth = 0
    fitness_generation = np.array([]) # collection of each robot's fitness
    for W1, W2 in zip(current_generation_W1, current_generation_W2): # for every robot in the generation
        #print(W1, '\n', W2)
        fitness_robot = np.array([]) # current robot's collection of fitness for each timestep
        print('robot depth: ', robot_depth)
        robot_depth += 1

        for cnt in range(1000):
            robot = LineString([(x-0.20,y-0.20), (x+0.20,y-0.20), (x+0.20,y+0.20), (x-0.20,y+0.20),(x-0.20,y-0.20)])

            ray_mid, s_mid = makeray(q_all[0]) # a line from robot to a point outside arena in direction of q
            ray_mid_left, s_mid_left = makeray(q_all[1]) 
            ray_mid_right, s_mid_right = makeray(q_all[2]) 
            ray_left, s_left = makeray(q_all[3]) 
            ray_right, s_right = makeray(q_all[4]) 
            f.write(str(x) + ',' + str(y) + '\n')

            
            
            # X value and smallest sensor distance
            sensors = np.array([s_left, s_mid_left, s_mid, s_mid_right, s_right]) # X value
            closest = np.amin(sensors) # sensor closest to wall
            if closest > 5: # define max value so that we can normalize and use in fitness function (maybe a better solution later)
                closest = 5
            
            # new wheel velocity values
            Y = forwardPropagation(sensors, W1, W2)
            left_wheel_velocity, right_wheel_velocity = Y[0], Y[1]

            # evaluation step
            V = (left_wheel_velocity+right_wheel_velocity)/2
            diff = np.absolute(left_wheel_velocity - right_wheel_velocity)
            i = Normalize(closest, 0, 5)
            fitness_timestep = Fitness(V, diff, i)
            fitness_robot = np.append(fitness_robot, fitness_timestep)


            #print("left: ", cnt)
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
            #print(x,y)
            if (world.distance(Point(x,y))<L/2):
                break
            if ((goal.distance(Point(x,y))<L/2)):
                print('WINNER')
                break
        fitness_robot = np.average(fitness_robot)
        fitness_generation = np.append(fitness_generation, fitness_robot) 
        if plot == True:
            plt.show()
    return fitness_generation

RunExperiment(10, 15, 2)

f.close()