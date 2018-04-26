# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 11:11:55 2018

@author: matth
"""

import numpy as np

import grid_object
import journey

parameters = {'knowledge':0,'movement':1,'alpha':2,
              'beta':3,'cost':4,'collisions':5}

def analyse(environment,knowledge,movement,num_goals,
            min_dist,alphas,betas,repeat,scenario):
    max_obs = environment.get_capacity()
    obstacles = environment.get_coords(grid_object.labels['obstacle'])
    spaces = environment.get_coords(grid_object.labels['empty'])
    start = spaces[np.random.randint(0,len(spaces))]
    goals = [start]
    too_close = []
    for g in range(0,num_goals):
        for square in spaces:
            if grid_object.p2_dist(goals[-1],square)<=min_dist:
                too_close.append(square)
        for square in too_close:
            if square in spaces:
                spaces.remove(square)
        goals.append(spaces[np.random.randint(0,len(spaces))])
    goals.remove(start)
    environment.set_goals(goals)
    size = (environment.get_width(),environment.get_height())
    results = []
    for k in knowledge:
        num_obs = int(np.floor(k*max_obs))
        initial_obs = []
        for n in range(0,num_obs):
            index = np.random.randint(0,len(obstacles))
            initial_obs.append(obstacles[index])
            obstacles.remove(initial_obs[-1])
        for m in movement:
            move_prob = [1-m,m/2,0,0,0,0,0,m/2]
            for p in range(0,len(alphas)):
                a = alphas[p]
                b = betas[p]
                costs = []
                colls = []
                perfect = journey.simulation(environment,environment,start,
                                             goals,[1,0,0,0,0,0,0,0],a,b)
                for r in range(0,repeat):
                    information = grid_object.grid(size,initial_obs,max_obs)
                    if scenario[0]==1:
                        information.set_goals(goals)
                    elif scenario[0]==2:
                        information.update_sense_range(scenario[1])
                    actual = journey.simulation(information,environment,start,
                                                goals,move_prob,a,b)
                    if (actual[journey.outputs['complete']] and 
                        perfect[journey.outputs['complete']]):
                        costs.append(perfect[journey.outputs['cost']]-
                                     actual[journey.outputs['cost']])
                        colls.append(actual[journey.outputs['collisions']])
                av_cost = sum(costs)/len(costs)
                av_coll = sum(colls)/len(colls)
                results.append([k,m,a,b,av_cost,av_coll,start,goals])
    return results

def display(results,parameter):
    x = []
    for i in results:
        x.append(i)
    # TODO: plot some graphs...
    x.remove(x[0])
    return 0

def display_3D(results):
    return 0