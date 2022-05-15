import matplotlib.pyplot as plt
import csv
from shapely.geometry import MultiLineString
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
c = []
i = 0
#with open(filenames.coordinate_file,'r') as csvfile:
with open("goal_endpoints/010d_endpoints.csv",'r') as csvfile:
#with open("009_coordinates.csv",'r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
      
    for row in plots:
        if row[0] == 'new':
            i += 1 
            continue
        x.append(float(row[0]))
        y.append(float(row[1]))
        c.append(i) #colors
  
size = [1 for i in range(len(x))]
plt.xlim([-5,5])
plt.ylim([-5,5])
for line in world:
    plt.plot(*line.xy, color='black')     
plt.scatter(x, y, s=size, c=c, cmap='viridis')
#plt.title('40000 simulated steps')
plt.legend()
plt.show()