# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 19:55:32 2018

@author: matth
"""

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
<<<<<<< HEAD

sizeA = (3,3)
startA = [0,0]
endA = [2,2]
obs=[0,2]
##print(obs)
test1 = grid_object.grid(sizeA,[obs],startA,endA)
#print(test1.get_state([1,1]))
test1.update_risk()
#print(test1.get_risk())
test1.update_heuristic(endA)
#print(test1.get_heuristic())
result1 = search.find_path(test1,startA,endA)
print(result1)

##test2 = grid_object.grid(sizeA,startA,endA,[[1,1]])
##result2 = search.find_path(test2,startA,endA)



#sizeB = (10,10)
#ob1 = [[3,4],[4,4],[3,3],[4,5]]
#ob2 = [[6,8],[7,8],[8,8],[9,8]]
#obstacles = ob1+ob2
#startB = [0,0]
#endB = [9,9]
#
#inf = grid_object.grid(sizeB,[],startB,endB)
#inf.update_risk()
#inf.update_heuristic(endB)
#
#env = grid_object.grid(sizeB,obstacles,startB,endB)
##print(env.get_state())
#env.show_me()
#env.update_risk()
#env.update_heuristic(endB)
#
#results3 = journey.simulation(inf,env,[0,0],[9,9])
=======
##test2 = grid_object.grid(sizeA,startA,endA,[[1,1]])
##result2 = search.find_path(test2,startA,endA)

sizeB = (10,10)
ob1 = [[3,4],[4,4],[3,3],[4,5]]
ob2 = [[6,8],[7,8],[8,8],[9,8]]
ob3 = [[2,5],[3,4],[4,3],[5,2]]
obstacles = ob1+ob2+ob3
startB = [0,0]
endB = [9,9]
#
inf = grid_object.grid(sizeB,[],startB,endB)
inf.update_risk()
inf.update_heuristic(endB)
>>>>>>> 47a64b6712358be09cab82d06e479af7b8910a84

#sizeB = (10,10)
#ob1 = [[3,4],[4,4],[3,3],[4,5]]
#ob2 = [[6,8],[7,8],[8,8],[9,8]]
#obstacles = ob1+ob2
#startB = [0,0]
#endB = [9,9]
##
#inf = grid_object.grid(sizeB,[],startB,endB)
#inf.update_risk()
#inf.update_heuristic(endB)
#
#env = grid_object.grid(sizeB,obstacles,startB,endB)
##print(env.get_state())
##env.show_me()
#env.update_risk()
#env.update_heuristic(endB)
##
#
#move_prob1 = [1,0,0,0,0,0,0,0]
#move_prob2 = [0.9,0.1,0,0,0,0,0,0]
#
#results4 = journey.simulation(inf,env,[0,0],[9,9],move_prob2)
#env.update_path_colour(results4[2])
#env.show_me()
#print('BWANANA!!!!!x2')

<<<<<<< HEAD
=======
move_prob1 = [1,0,0,0,0,0,0,0]
move_prob2 = [0.9,0.1,0,0,0,0,0,0]
move_prob3 = [0.8,0.1,0,0,0,0,0,0.1]

results3 = journey.simulation(inf,env,[0,0],[9,9],move_prob1)
env.update_path_colour(results3[2])
env.show_me()
>>>>>>> 47a64b6712358be09cab82d06e479af7b8910a84
#env.update_path_colour (results3[1])
#env.show_me()
##print(results3)
##real_cost = results3[0]
#perfect_path = search.find_path(env,startB,endB)
#best_cost = perfect_path[0]
#print(best_cost)