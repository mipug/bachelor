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

sns.set_theme(color_codes=True)
x = [i for i in range(101)]

weight = ['5', '0.5', '1', '2', '3', '4']
ver = ['a', 'b', 'c', 'd', 'e']
w = 0

y = [0 for i in range(101)]

for i in range(5): 
    file_a = 'wall_fitness/' + str('13') + ver[i] + '_fitness.csv' #crossover
    print(file_a)


    with open(file_a,'r') as csvfile:

        fitness = csv.reader(csvfile, delimiter = ',')
        
        for row, i in zip(fitness, range(101)):
            row = [float(i) for i in row]
            y[i] += np.average(row)
        
for i in range(101):
    y[i] = y[i]/5

d = {'Generation': x, 'Fitness': y}
df = pd.DataFrame(d)

sns.regplot(x='Generation', y='Fitness', data=df,
    lowess=True, scatter = True, label =('w = 3 : Crossover')).set(title='Parameter Search')          


y = [0 for i in range(101)]

for i in range(5):     
    file_a = 'wall_fitness/' + str('14') + ver[i] + '_fitness.csv' #crossover   
    with open(file_a, 'r') as csvfile:

        fitness = csv.reader(csvfile, delimiter = ',')
        for i, row in zip(range(len(y)), fitness):
            row = [float(i) for i in row]
            y[i] += np.average(row)

for i in range(101):
    y[i] = y[i]/5

d = {'Generation': x, 'Fitness': y}
df = pd.DataFrame(d)




sns.regplot(x='Generation', y='Fitness', data=df,
    lowess= True, scatter = True, label =('w = 3 : No crossover')).set(title='Parameter Search')    


plt.ylim(0.15,0.55)           


plt.legend()

plt.show()

        
#ci=None