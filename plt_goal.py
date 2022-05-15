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

fig, ax = plt.subplots()
ax.yaxis.set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)


df = [28,25,25,16,13,21]
c = [1,1,1,2,2,2]

ax.scatter(df, [-0.045]*len(df), s=100, c=c)
ax.set_ylim(0.0,0.0)

plt.show()