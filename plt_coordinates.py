import matplotlib.pyplot as plt
import csv
from shapely.geometry import MultiLineString

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
  
with open('coordinates_g.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
      
    for row in plots:
        x.append(float(row[0]))
        y.append(float(row[1]))
  

s = [0.5 for i in range(len(x))]
plt.xlim([-5,5])
plt.ylim([-5,5])
for line in world:
    plt.plot(*line.xy, color='black')     
plt.scatter(x, y, s=s)
plt.title('Ages of different persons')
plt.legend()
plt.show()