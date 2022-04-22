from turtle import color
import matplotlib.pyplot as plt
import csv
from shapely.geometry import MultiLineString
import numpy as np
import pylab
import seaborn as sns
import pandas as pd
import filenames
import numpy


x = [i for i in range(101)]

weight = ['5', '0.5', '1', '2', '3', '4']
w = 0

for i in range(2,13,2): 
    file_a = 'wall_fitness/0' + str(i) + 'a_fitness.csv'
    file_b = 'wall_fitness/0' + str(i) + 'b_fitness.csv'
    print(file_a)
    with open(file_a,'r') as csvfile:

        fitness = csv.reader(csvfile, delimiter = ',')
        y = []
        for row in fitness:
            row = [float(i) for i in row]
            y.append(np.average(row))
        
    with open(file_b, 'r') as csvfile:

        fitness = csv.reader(csvfile, delimiter = ',')
        for i, row in zip(range(len(y)), fitness):
            row = [float(i) for i in row]
            y[i] = (y[i] + np.average(row))/2

            
        d = {'Generation': x, 'Fitness': y}
        df = pd.DataFrame(d)

        sns.regplot(x='Generation', y='Fitness', data=df,
                    order=2, scatter = True, label =('w = ' + weight[w])).set(title='No Crossover')           
        plt.legend()
        w += 1
plt.show()

        
#ci=None