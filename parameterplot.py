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



for i in range(1,4): 
    file = 'wall_fitness/0' + str(i) + 'a_fitness.csv'
    with open(file,'r') as csvfile:

        fitness = csv.reader(csvfile, delimiter = ',')
        y = []
        for row in fitness:
            row = [float(i) for i in row]
            y.append(np.average(row))
        
        d = {'Generation': x, 'Fitness': y}
        df = pd.DataFrame(d)

        sns.regplot(x='Generation', y='Fitness', data=df,
                    order=2, scatter = False, label =('w = ' + str(i))).set(title='No crossover')           
        plt.legend()
plt.show()

        
#ci=None