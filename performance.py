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

def analyse(environment,knowledge,movement,num_goals,min_dist,alphas,betas):
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
    size = (environment.get_width(),environment.get_height())
    results = []
    for k in knowledge:
        num_obs = int(np.floor(k*max_obs))
        initial_obs = []
        for n in range(0,num_obs):
            index = np.random.randint(0,len(obstacles))
            initial_obs.append(obstacles[index])
            obstacles.remove(initial_obs[-1])
        information = grid_object.grid(size,initial_obs,max_obs)
        for m in movement:
            move_prob = [1-2*m,m,0,0,0,0,0,m]
            for a in alphas:
                for b in betas:
                    run = journey.simulation(information,environment,start,
                                             goals,move_prob,a,b)
                    if run[journey.outputs['complete']]==True:
                        results.append([k,m,a,b,run[journey.outputs['cost']],
                                   run[journey.outputs['collisions']]])
    return results

def display(results):
    # TODO: plot some graphs...
    return 0