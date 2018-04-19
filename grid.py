# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 12:19:13 2018

@author: YAYA
"""
import numpy as np
import random

#make output of this a grid object class
empty =[]
obs = []
startB = []
endB = []
grid =[[2,1,1,0,1,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,1,1,0,1,0,0,1,1,1],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,3]]
for d1 in range(10):
    for d2 in range(10):
        if grid[d1][d2] == 0:
            empty.append([d1+1,d2+1])
for d1 in range(10):
    for d2 in range(10):
        if grid[d1][d2] == 1:
            obs.append([d1+1,d2+1])
for d1 in range(10):
    for d2 in range(10):
        if grid[d1][d2] == 2:
            startB.append([d1+1,d2+1])
for d1 in range(10):
    for d2 in range(10):
        if grid[d1][d2] == 3:
            endB.append([d1+1,d2+1])
print ('empty at ',empty)
print ('obs at' ,obs)
print ('start point at' ,startB)
print ('end point at' ,endB)
