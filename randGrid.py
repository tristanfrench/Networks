# -*- coding: utf-8 -*-
"""
Created on Thurs April 26 15:26 2018

@author: JamesL
"""

import grid_object
import search
import journey
import numpy as np
import random as rng
import obstacles_store as os
np.set_printoptions(threshold=np.inf)


i = 0
sizeB = (30,30)

"""obsMax is set to grid size / 2 * the size of a single obstacle, 9
Ensure that at least half the grid is empty in any generation"""
obsMax = (sizeB[0] * sizeB[1])/(18) 

obstacles = []
for i in range(0,obsMax):
    #max obs size is 3x3, so max rng val must be < 3 away from edge. Avoids overflow error.
    X = rng.randint(1, 27)
    Y = rng.randint(1, 27)
    
    #coin toss for obs shape
    switch = rng.randint(0,1)
    if switch == 0:
        obstacles = obstacles+ os.crcol(X,Y)    
    elif switch == 1:
        obstacles = obstacles+ os.sqcol(X,Y)

startB = [0,0]
endB = [29,29]
#endC = [1,7]
#
env = grid_object.grid(sizeB,obstacles,len(obstacles))
env.update_heuristic(endB)

inf = grid_object.grid(sizeB,[],len(obstacles))
inf.update_heuristic(endB)

move_prob1 = [1,0,0,0,0,0,0,0]
move_prob2 = [0.9,0.1,0,0,0,0,0,0]
move_prob3 = [0.8,0.1,0,0,0,0,0,0.1]
env.set_goals([endB])
inf.set_goals([endB])


results3 = journey.simulation(inf,env,startB,[endB],move_prob1)
env.update_path_colour(results3[2],startB,[endB])
env.show_me()
#env.update_path_colour (results3[1])
#env.show_me()
##print(results3)
##real_cost = results3[0]
#perfect_path = search.find_path(env,startB,endB)
#best_cost = perfect_path[0]
#print(best_cost)