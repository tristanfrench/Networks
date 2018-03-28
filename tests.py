# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 19:55:32 2018

@author: matth
"""

import numpy as np

import grid_object
import search

test1 = grid_object.grid((3,3),[])
result1 = search.find_path(test1,[0,0],[2,2])
test2 = grid_object.grid((3,3),[[1,1]])
result2 = search.find_path(test1,[0,0],[2,2])




'''
size = (10,10)
ob1 = [[3,4],[4,4],[3,3],[4,5]]
ob2 = [[6,8],[7,8],[8,8],[9,8]]
obstacles = ob1+ob2
drone_map = grid_object.grid(size,obstacles)
environment = grid_object.grid(size,[])
'''