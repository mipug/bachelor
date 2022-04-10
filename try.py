import numpy as np
from scipy.spatial import distance

#old_robots = [(1.5 ,2), (2,3), (3,4), (2,1)]
old_robots = [(19,19)]
new = [(1.8,1), (18,15), (3,5), (1,1)]

#def score(neighbours):


def noveltyMetric(new_population, k):
    global old_robots 
    old_robots.extend(new_population)
    cnt =0
    pop_score = []
    for new_robot in new_population: 
        cnt+=1
        distances = []
        for old_robot in old_robots: 
            #print(new_robot, old_robot)
            dist = distance.euclidean(new_robot, old_robot)
            
            distances.append(dist)
    
        distances.sort()

        #print(distances)
        neighbours = distances[1:k+1]
        print(neighbours)

        score = sum(neighbours)/k
        pop_score.append(score)
        #print(cnt, score)
    print(pop_score)
noveltyMetric(new, 2)


