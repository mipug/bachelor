import matplotlib.pyplot as plt
import csv
from shapely.geometry import MultiLineString
import numpy as np
import pylab
import seaborn as sns
import pandas as pd

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
  
with open('fitness_g60_p21_s40000_w5_wheels0.5.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
    for row, gen in zip(plots, range(100)):
        x.append(gen)
        #y.append((float(row[0]) + float(row[1]) + float(row[2]))/3)
        row = [float(i) for i in row]
        y.append(max(row))
      #  for i in row:
       #     y.append(int(i))
    #print(x, y)

d = {'gen': x, 'fitness': y}
df = pd.DataFrame(d)

sns.regplot(x='gen', y='fitness', data=df,
           order=2, ci=None)
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