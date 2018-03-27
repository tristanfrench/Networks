# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 23:34:52 2018

@author: matth
"""

import grid_object.py as go

size = (10,10)
ob1 = [[3,4],[4,4],[3,3],[4,5]]
ob2 = [[6,8],[7,8],[8,8],[9,8]]
obstacles = ob1+ob2
drone_map = go.grid(size,obstacles)
environment = go.grid(size,[])