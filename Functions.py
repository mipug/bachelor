from locale import normalize
import shapely
from shapely.geometry import LinearRing, LineString, Point, MultiLineString
from numpy import sin, cos, pi, sqrt, genfromtxt
from random import random
import matplotlib.pyplot as plt
import math
import numpy as np
from variables import *

q_mid = 0.0 
q_mid_left = 0.5
q_mid_right = -0.5  # robot heading with respect to x-axis in radians 
q_left = 1
q_right = -1 
q_all= [q_mid, q_mid_left, q_mid_right, q_left, q_right]

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
    #s = Normalize(s, 0, 10)
    return ray, s

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
    print("Fitness all: ", fitness)
    s.write(str(fitness[best_robots]) + '\n')
    
    best_current_generation_W1 = [current_genW1[idx] for idx in best_robots]
    print("Selected best: ", best_current_generation_W1)
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
                random = np.random.uniform(-3,3)
                #print("Weight: ", weight, "Random: ", random)
                if random <= 0.3:
                    #print("MUTATE!!!!")
                    #print("OLD!: ", xxx[0, weight])
                    xxx[0, weight] = np.random.uniform(-3,3)
                    xxx[1, weight] = np.random.uniform(-3,3)
                    #print("NEW!: ", xxx[0, weight])
                
        xxx2 = np.copy(robot_W2)
        if mat_pick == 1:
            for weight in range(xxx2.shape[1]):
                random = np.random.uniform(-3,3)
                
                if random <= 0.4:
                    #print("OLD!: ", xxx2[0, weight])
                    xxx2[0, weight] = np.random.uniform(-3,3)
                    xxx2[1, weight] = np.random.uniform(-3,3)
                    #print("NEW: ", xxx2[0, weight])
        new_robots_W1.append(xxx)
        new_robots_W2.append(xxx2)
    #print("new_robots: ", new_robots_W1, new_robots_W2)   
    return new_robots_W1, new_robots_W2

def NewGeneration(best_current_gen_W1, best_current_gen_W2, n):
    print("same?", best_current_gen_W1)
    new_gen_W1 = []
    new_gen_W2 = []
    for W1, W2 in zip(best_current_gen_W1, best_current_gen_W2): #Generates a batch of n mutated robots for every 'best robot' selected in selectTop
        print('hello')
        new_gen_W1.append(W1)
        new_gen_W2.append(W2)
        n_new_W1, n_new_W2 = Mutate(W1, W2, n)
        
        for W1, W2 in zip(n_new_W1, n_new_W2): # for every robot weigts in returned batch, append them to the list of the new generation
            #print('Success??: ')
            new_gen_W1.append(W1)
            new_gen_W2.append(W2)
    return new_gen_W1, new_gen_W2

def Fitness(left_wheel_velocity, right_wheel_velocity, closest): # evaluates the robot at each step between 0 and 1
    # V             -> average rotation speed -> (left_velocity + right_velocity) / 2
    # 1-sqrt(v)     -> square root of the absolute value of the difference speed values -> sqrt of |(left_velocity-right_velocity)|
    # i             -> i is the normalized value (0-1) of the closest distance to a wall -> if high distance then high value
    V = Normalize(((left_wheel_velocity+right_wheel_velocity)/2), -1, 1)
    diff = Normalize((np.absolute(left_wheel_velocity - right_wheel_velocity)), -0.5, 0.5)
    i = Normalize(closest, 0, 5)

    fitness = V*(1-np.sqrt(diff))*i

    return fitness

def forwardPropagation(X, W1, W2): 

    Z1 = np.dot(W1, X) #+ b1
    A1 = np.tanh(Z1) 

    Z2 = np.dot(W2, A1) #+ b2
    Y = np.tanh(Z2) 
    
    return Y 

def StartingPosition():
    return -4, 4

def Normalize(x, min, max):
    # min = 0, max = 5 (sensor distance)
    i = (x - min) / (max - min)
    return i

def RunExperiment(depth, popsize, hidden_size):
    #simulate the first initialized generation
    first_generation_W1, first_generation_W2 = InitializeGeneration(popsize, hidden_size) 
    fitness_generation = np.copy(Simulate(first_generation_W1, first_generation_W2))
    #print(fitness_generation)

    cw1, cw2 = SelectTop(3, fitness_generation, first_generation_W1, first_generation_W2)
    nw1, nw2 = NewGeneration(cw1, cw2, 5)
    
    # make new generations 'depth' number of times and run simulation on them
    gen_depth = 1
    for i in range(depth):
        print('depth: ', gen_depth)
        fitness_generation = np.copy(Simulate(nw1, nw2))

        cw1, cw2 = SelectTop(3, fitness_generation, nw1, nw2)
        gen_depth += 1
        nw1, nw2 = NewGeneration(cw1, cw2, 5)

def Simulate(current_generation_W1, current_generation_W2):
    robot_depth = 0
    fitness_generation = np.array([]) # collection of each robot's fitness
    
    for W1, W2 in zip(current_generation_W1, current_generation_W2): # for every robot in the generation
        #print(W1, '\n', W2)
        fitness_robot = np.array([]) # current robot's collection of fitness for each timestep
        print('robot depth: ', robot_depth)
        robot_depth += 1
        x, y = StartingPosition()

        for cnt in range(5000):
            
            robot = LineString([(x-0.20,y-0.20), (x+0.20,y-0.20), (x+0.20,y+0.20), (x-0.20,y+0.20),(x-0.20,y-0.20)])

            ray_mid, s_mid = makeray(q_all[0], x, y) # a line from robot to a point outside arena in direction of q
            ray_mid_left, s_mid_left = makeray(q_all[1], x, y) 
            ray_mid_right, s_mid_right = makeray(q_all[2], x, y) 
            ray_left, s_left = makeray(q_all[3], x, y) 
            ray_right, s_right = makeray(q_all[4], x, y) 
            f.write(str(x) + ',' + str(y) + '\n')

            
            
            # X value and smallest sensor distance
            sensors = np.array([s_left, s_mid_left, s_mid, s_mid_right, s_right]) # X value
            #print("non-norm: ", sensors)
            closest = np.amin(sensors) # sensor closest to wall
            #if closest > 5: # define max value so that we can normalize and use in fitness function (maybe a better solution later)
            #    closest = 5
            for i in range(sensors.shape[0]): 
                sensors[i] = Normalize(sensors[i], 0, 10)
            #print("norm: ", sensors)
            # new wheel velocity values
            Y = forwardPropagation(sensors, W1, W2)
            y_norm_left = (0.25-(-0.25))*(Y[0]-0)+(-0.25)
            y_norm_right = (0.25-(-0.25))*(Y[1]-0)+(-0.25)
            left_wheel_velocity, right_wheel_velocity = y_norm_left, y_norm_right

            #print("left + right: ", left_wheel_velocity, right_wheel_velocity)

            # evaluation step

            fitness_timestep = Fitness(left_wheel_velocity, right_wheel_velocity, closest)
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
        fitness_avg = np.average(fitness_robot)
        fitness_generation = np.append(fitness_generation, fitness_avg) 
        if plot == True:
            plt.show()
    return fitness_generation
    












