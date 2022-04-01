import matplotlib.pyplot as plt
import csv
from shapely.geometry import MultiLineString
import numpy as np
import pylab
import seaborn as sns
import pandas as pd
import filenames

W = 10.0  # width of arena
H = 10.0  # height of arena
walls = [
        ((W/2,H/2),(-W/2,H/2),(-W/2,-H/2),(W/2,-H/2),(W/2,H/2)),
        ((3,-5),(-3,-1)),
        ((-1, 5), (-3, 2)), 
        ((-1, -2.3), (1 , 0)),
        ((5, 0), (3, -2)),
        ((-2.0, 3.5), (1, 2))]
world = MultiLineString(walls)

x = []
y = []
  
with open(filenames.fitness_file,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
    for row, gen in zip(plots, range(100)):
        x.append(gen)
        row = [float(i) for i in row]
        y.append(np.average(row))

d = {'Generation': x, 'Fitness': y}
df = pd.DataFrame(d)



sns.set_theme()
sns.regplot(x='Generation', y='Fitness', data=df,
           order=2, ci=None).set(title='Avg Fitness Top 3 ')           
plt.show()

"""
plt.xlim([0,100])
plt.ylim([0.2,0.7])  
plt.scatter(x, y)
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
pylab.plot(x,p(x),"r--")
plt.title('Fitness')
plt.legend()
plt.show()"""