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


df = [1,2,3,4]

ax.scatter(df, [-0.04]*len(df), s=100, c='r')
ax.set_ylim(0.0,0.0)

plt.show()