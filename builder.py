# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 14:59 2018

@author: jamesl

built from tests.py by matth
Basically just a playpen for me to work in
"""

import obstacles_store as os
import grid_object
import search
import journey
import numpy as np
np.set_printoptions(threshold=np.inf)

sizeA = (5,5) 
startA = [0,0]
endA = [2,2]
#obs=[0,2]
##print(obs)
test1 = grid_object.grid(sizeA,[],startA,endA)
test1.random_obs(3,[startA,endA])
#test1.update_risk()
print(test1.get_state())
#test1.update_heuristic(endA)
##print(test1.get_heuristic())
#result1 = search.find_path(test1,startA,endA)
##print(result1)
##test2 = grid_object.grid(sizeA,startA,endA,[[1,1]])
##result2 = search.find_path(test2,startA,endA)


sizeB = (10,10)
ob1 = [[2,5],[3,4],[4,3],[5,2]]
ob2 = [[7,9],[7,8],[8,8]]
obstacles = os.hcor(1,2)
startB = [0,0]
endB = [9,9]
#
inf = grid_object.grid(sizeB,[],startB,endB)
inf.update_risk()
inf.update_heuristic(endB)

env = grid_object.grid(sizeB,obstacles,startB,endB)
#print(env.get_state())
#env.show_me()
env.update_risk()
env.update_heuristic(endB)
#

move_prob1 = [1,0,0,0,0,0,0,0]
move_prob2 = [0.9,0.1,0,0,0,0,0,0]

results3 = journey.simulation(inf,env,[0,0],[9,9],move_prob1)
env.update_path_colour(results3[2])
env.show_me()
#env.update_path_colour (results3[1])
#env.show_me()
##print(results3)
##real_cost = results3[0]
#perfect_path = search.find_path(env,startB,endB)
#best_cost = perfect_path[0]
