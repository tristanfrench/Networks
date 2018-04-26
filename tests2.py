# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 19:55:32 2018

@author: matth
"""

import grid_object
import search
import journey
import performance
import numpy as np
import animation

np.set_printoptions(threshold=np.inf)

sizeA = (5,5)
startA = [0,0]
endA = [2,2]
#obs=[0,2]
##print(obs)
test1 = grid_object.grid(sizeA,[],0)
test1.random_obs(3,[startA,endA])
#test1.update_risk()
#print(test1.get_state())
#test1.update_heuristic(endA)
##print(test1.get_heuristic())
#result1 = search.find_path(test1,startA,endA)
##print(result1)
##test2 = grid_object.grid(sizeA,startA,endA,[[1,1]])
##result2 = search.find_path(test2,startA,endA)

sizeB = (15,15)
ob1 = [[3,4],[4,4],[3,3],[4,5]]
ob2 = [[6,8],[7,8],[8,8],[9,8]]
ob3 = [[2,5],[3,4],[4,3],[5,2]]
ob4 = [[10,12],[11,12],[13,12],[12,11]]
obstacles = ob1+ob2+ob3+ob4
startB = [0,0]
endB = [9,9]
endC = [0,14]
endD = [12,1]
endE = [12,12]
#
env = grid_object.grid(sizeB,obstacles,len(obstacles))
#env.update_heuristic(endB)

inf = grid_object.grid(sizeB,[],len(obstacles))
#inf.update_heuristic(endB)

move_prob1 = [1,0,0,0,0,0,0,0]
move_prob2 = [0.9,0.1,0,0,0,0,0,0]
move_prob3 = [0.8,0.1,0,0,0,0,0,0.1]

env.update_sense_range(3)
inf.update_sense_range(3)

env.set_goals([endC,endD,endE])
#inf.set_goals([endB,endC,endD])
#env.set_goals([endD])

inf.update_heuristic([])
env.update_heuristic([])


results3 = journey.simulation(inf,env,startB,[endB,endC],move_prob1)
env.update_path_colour(results3[2],startB,[endC,endD,endE])
env.show_me()
#animation.path_animation(env,results3[2])

env2 = grid_object.grid(sizeB,obstacles,len(obstacles))
'''
knowledge = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
movement = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5]
num_goals = 1
min_dist = 0
alphas = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5]
betas = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5]

'''
#results = performance.analyse(env,knowledge,movement,num_goals,
                              #min_dist,alphas,betas)

#def analyse(environment,knowledge,movement,num_goals,min_dist,alphas,betas):

#Adj = search.adjacency(env2,[0,0],[[3,0],[9,9],[1,8]],move_prob1)

#env.update_path_colour (results3[1])
#env.show_me()
##print(results3)
##real_cost = results3[0]
#perfect_path = search.find_path(env,startB,endB)
#best_cost = perfect_path[0]
#print(best_cost)