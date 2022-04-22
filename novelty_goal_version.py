from locale import normalize
from locale import normalize
import shapely
from shapely.geometry import LinearRing, LineString, Point, MultiLineString
from numpy import sin, cos, pi, sqrt, genfromtxt
import random #import random
import matplotlib.pyplot as plt
import math
import numpy as np
import filenames
import sys
from scipy.spatial import distance

#np.random.seed(42)

# CONSTANTS

R = 0.02  # radius of wheels in meters
L = 0.10  # distance between wheels in meters

W = 10.0  # width of arena
H = 10.0  # height of arena

robot_timestep =  0.1       # 1/robot_timestep (10) equals update frequency of robot
simulation_timestep = 0.1  # timestep in kinematics simulation (probably don't touch..)

walls = [ # the world is a quadratic arena with width W and height H
        ((W/2,H/2),(-W/2,H/2),(-W/2,-H/2),(W/2,-H/2),(W/2,H/2)),
        ((3,-5),(-3,-1)),
        ((-1, 5), (-3, 2)), 
        ((-1, -2.3), (1 , 0)),
        ((5, 0), (3, -2)),
        ((-2.0, 3.5), (1, 2))]
world = MultiLineString(walls)
goal = Point(-4,-4)


# VARIABLES

q_mid = 0.0 
q_mid_left = 0.5
q_mid_right = -0.5  # robot heading with respect to x-axis in radians 
q_left = 1
q_right = -1
q_all = [q_mid, q_mid_left, q_mid_right, q_left, q_right]


input = 5 # 5 sensor + 1 bias
hidden_size = 2
popsize = 21
old_robots = []

# FUNCTIONS

def startPoint(): 
    global x, y, left_wheel_velocity, right_wheel_velocity
    
    x = -4   # robot position in meters - x direction - positive to the right 
    y = 4  # robot position in meters - y direction - positive up
    
    left_wheel_velocity =  np.random.uniform(-0.25, 0.25)   # robot left wheel velocity in radians/s
    right_wheel_velocity =  np.random.uniform(-0.25, 0.25)  # robot right wheel velocity in radians/s

def makeray(q, x, y):
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
    if s > 5:
        s = 5
    #s = Normalize(s, 0, 10)
    return s

def simulationstep(left_wheel_velocity, right_wheel_velocity): # updates robot position and heading based on velocity of wheels and the elapsed time
    global x, y, q_all

    for step in range(int(robot_timestep/simulation_timestep)):    #step model time/timestep times (0.1/0.1)
        v_x = cos(q_all[0])*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2) 
        v_y = sin(q_all[0])*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2)
        omega = (R*right_wheel_velocity - R*left_wheel_velocity)/(2*L)  
        
        x += v_x * simulation_timestep
        y += v_y * simulation_timestep
        for i in range(len(q_all)): 
            q_all[i] += omega * simulation_timestep
    
def forwardPropagation(X, W1, W2): 
    Z1 = np.dot(W1, X) #+ b1
    A1 = sigmoid(Z1) 

    Z2 = np.dot(W2, A1) #+ b2
    Y = sigmoid(Z2) 
    return Y 

def Normalize(x, min, max):
    i = (x - min) / (max - min)
    return i

def sigmoid(x):
    return 1/(1 + np.exp(-x))



# FIRST GENERATION

def GenerateGenom(hidden_layer, W):
    if W == 1:
        Weight = np.random.uniform(low = -5, high = 5, size = (hidden_layer, 5)) #(hidden_neurons, input_size)
    if W == 2:
        Weight = np.random.uniform(low = -5, high = 5, size = (2, hidden_layer)) #(Output_neurons, hidden_neurons)
    return Weight

def InitializeGeneration(popsize, hidden_layer):
    population_W1 = [GenerateGenom(hidden_layer,1) for i in range(popsize)]
    population_W2 = [GenerateGenom(hidden_layer,2) for i in range(popsize)]
    #print(population_W1)
    #print(population_W1)
    return population_W1, population_W2


# FITNESS

def Fitness(x,y): # evaluates the robot at each step between 0 and 1
    fitness = 1 - Normalize(Point(x,y).distance(goal), 0, 10)

    return fitness


def noveltyMetric(new_population, k):
    global old_robots 
    old_robots.extend(new_population) #End position of robots appended to history 
    pop_score = []

    for new_robot in new_population: 
        distances = []
        for old_robot in old_robots: 
            dist = distance.euclidean(new_robot, old_robot) #calcuate distances to all robots in history
            distances.append(dist)
    
        distances.sort()
        neighbours = distances[1:k+1] #Take n-nearest neighbours 

        score = sum(neighbours)/k #sum of distances divided by number of nearest neighbours
        pop_score.append(score)
    print("score: ", pop_score)
    return pop_score



def SelectTop(n, fitness, current_genW1, current_genW2):
    best_robots = np.argsort(fitness)[-n:]
    print('best fitness ',  fitness[best_robots])
    print("Fitness all: ", fitness)
    
    s.write(str(fitness[best_robots[0]]) + ',' + str(fitness[best_robots[1]]) + ',' + str(fitness[best_robots[2]]) + '\n')
    
    best_current_generation_W1 = [current_genW1[idx] for idx in best_robots]
    print("Selected best: ", best_current_generation_W1)
    best_current_generation_W2 = [current_genW2[idx] for idx in best_robots]
    return best_current_generation_W1, best_current_generation_W2



# NEW GENERATION

def Mutate(robot_W1, robot_W2, n):
    # rand,om int 0 or 1
    # for each input robot, mutate it n times
    # return the arrays of new weights
    new_robots_W1 = []
    new_robots_W2 = []
    
    for i in range(n):
        xxx = np.copy(robot_W1)
        mat_pick = np.random.randint(2) #choose randomly if W1 or W2 should be mutated
        if mat_pick == 0: 
            for weight in range(xxx.shape[1]):
                random0 = np.random.uniform(0,1)
                random1 = np.random.uniform(0,1)
                if random0 <= 0.4:      
                    xxx[0, weight] = np.random.uniform(-5,5)
                if random1 <= 0.4:
                    xxx[1, weight] = np.random.uniform(-5,5)
                
        xxx2 = np.copy(robot_W2)
        if mat_pick == 1:
            for weight in range(xxx2.shape[1]):
                random0 = np.random.uniform(0,1)
                random1 = np.random.uniform(0,1)
                if random0 <= 0.4:
                    xxx2[0, weight] = np.random.uniform(-5,5)
                if random1 <= 0.4:
                    xxx2[1, weight] = np.random.uniform(-5,5)
                    
        new_robots_W1.append(xxx)
        new_robots_W2.append(xxx2) 
    return new_robots_W1, new_robots_W2

def NewGeneration(best_current_gen_W1, best_current_gen_W2, n):
    print("same?", best_current_gen_W1)
    new_gen_W1 = []
    new_gen_W2 = []
    for W1, W2 in zip(best_current_gen_W1, best_current_gen_W2): #Generates a batch of n mutated robots for every 'best robot' selected in selectTop
        new_gen_W1.append(W1)
        new_gen_W2.append(W2)
        n_new_W1, n_new_W2 = Mutate(W1, W2, n)
        
        for W1, W2 in zip(n_new_W1, n_new_W2): # for every robot weigts in returned batch, append them to the list of the new generation
            #print('Success??: ')
            new_gen_W1.append(W1)
            new_gen_W2.append(W2)
    return new_gen_W1, new_gen_W2


# RUN EXPERIMENT
h = open('endpoints.csv', 'w')
def RunExperiment(depth, popsize, hidden_size):
    # Initialize and run the first initialized generation
    first_generation_W1, first_generation_W2 = InitializeGeneration(popsize, hidden_size) 
    fitness_generation = np.copy(Simulate(first_generation_W1, first_generation_W2))

    cw1, cw2 = SelectTop(3, fitness_generation, first_generation_W1, first_generation_W2)
    nw1, nw2 = NewGeneration(cw1, cw2, 6)
    
    # make new generations 'depth' number of times and run simulation on them
    gen_depth = 1
    for i in range(depth):
        print('depth: ', gen_depth)
        fitness_generation = np.copy(Simulate(nw1, nw2))

        cw1, cw2 = SelectTop(3, fitness_generation, nw1, nw2)
        gen_depth += 1
        nw1, nw2 = NewGeneration(cw1, cw2, 6)




# SIMULATION LOOP
s = open(filenames.goal_fitness, 'w')

def Simulate(current_generation_W1, current_generation_W2):
    robot_depth = 0
    #fitness_generation = np.array([]) # collection of each robot's fitness
    coordinates = []
    
    f = open(filenames.goal_coordinates, "w")
    for W1, W2 in zip(current_generation_W1, current_generation_W2): # for every robot in the generation
        
        startPoint()
        fitness_robot = np.array([]) # current robot's collection of fitness for each timestep
        print('robot depth: ', robot_depth)
        robot_depth += 1
        
        for cnt in range(40000):
            s_mid = makeray(q_all[0], x, y) # a line from robot to a point outside arena in direction of q
            s_mid_left = makeray(q_all[1], x, y) 
            s_mid_right = makeray(q_all[2], x, y) 
            s_left = makeray(q_all[3], x, y) 
            s_right = makeray(q_all[4], x, y) 
            f.write(str(x) + ',' + str(y) + '\n')
            
            # X value and smallest sensor distance
            sensors = np.array([s_left, s_mid_left, s_mid, s_mid_right, s_right]) # X value
            closest = np.amin(sensors) # sensor closest to wall
            for i in range(sensors.shape[0]): 
                sensors[i] = Normalize(sensors[i], 0, 5) 
            
            # new wheel velocity values
            Y = forwardPropagation(sensors, W1, W2)
            
            y_norm_left = ((Y[0])/(1))*(0.25-(-0.25))+(-0.25) #range -0.25, 0.25
            y_norm_right =((Y[1])/(1))*(0.25-(-0.25))+(-0.25)
            left_wheel_velocity, right_wheel_velocity = y_norm_left, y_norm_right

            simulationstep(left_wheel_velocity, right_wheel_velocity)
            

            if (world.distance(Point(x,y))<L/2):
                print("dead")
                break
                
            if ((goal.distance(Point(x,y))<L/2)):
                print('WINNER! ', 'robot: ', robot_depth)
                sys.exit()
        coordinates.append((x,y))
        h.write(str(x) + ',' + str(y) + '\n')
        print("Coordinates: ", coordinates)
    fitness_generation = noveltyMetric(coordinates, 5)
    print("fitness: ", fitness_generation)
        # evaluation step

        #fitness_robot = Fitness(x,y)
        #fitness_generation = np.append(fitness_generation, fitness_robot) 
        
        
    f.close()
    return fitness_generation


RunExperiment(depth = 50, popsize = popsize, hidden_size = hidden_size)
s.close()