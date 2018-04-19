# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 22:37:24 2018

@author: matth
"""

import numpy as np

import grid_object
import search

def dev(prob):
    '''
    Randomly selects a deviation index based on the probabilities specified.
    'prob' is a 1x8 vector whose sum must be equal to 1. Element 0 represents
    the probability of a drone completing it's intended movement; element n
    represents the probability of the drone being deflected nx45 degrees
    clockwise from its intended movement.
    '''
    value = np.random.uniform()
    cum_prob = np.cumsum(prob)
    for p in range(0,len(cum_prob)):
        if value < cum_prob[p]:
            return p
    return []

def simulation(information,environment,start,end,move_prob,alpha=1,beta=1):
    '''
    Runs a theoretical simulation of a drone travelling through a grid trying
    to get from 'start' to 'end'. 'information' represents the drones knowledge
    of its surroundings and 'environment' represents the drones actual
    surrounds.'alpha' and 'beta' represent the weightings of the heuristic and
    risk to be used when finding paths.
    '''
    # Calculate initial plan and store the path found as the first strategy.
    plan = search.find_path(information,start,end,alpha=1,beta=1)
    strategies = [plan[1]]
    # update 'route' to be the most recently devised path.
    route = strategies[-1]
    # initialise record of squares that are visited.
    record = []
    cost = 0
    step = 0
    collisions = 0
    journey_complete = False
    while not journey_complete:
        # compute deviation index.
        deviated = dev(move_prob)
        if step==0:
            deviated = 0
        reroute_required = False
        if not deviated:
            # move to the next square listed in the current route.
            record.append(route[step])
        else :
            reroute_required = True
            # if the drone has deviated, find it's new position - 'trajectory'.
            move_intent = [route[step][0]-record[step-1][0],
                           route[step][1]-record[step-1][1]]
            total_moves = len(grid_object.directions)
            for d_num in range(0,total_moves):
                if grid_object.directions[d_num]==move_intent:
                    break
            move_actual = grid_object.directions[(d_num+deviated)%total_moves]
            trajectory = [record[step-1][0]+move_actual[0],
                          record[step-1][1]+move_actual[1]]
            if (environment.is_in_grid(trajectory) and
                environment.get_state(trajectory)!=
                grid_object.labels['obstacle']):
                # if the deviation is a valid move, add to record.
                record.append(trajectory)
            else :
                # if the deviation is not a valid move, remain stationary.
                record.append(record[step-1])
                collisions+=1
        # calculate cost of most recent move.
        cost+=grid_object.p2_dist(record[step],record[step-1])
        # stop simulation if drone has remained stationary for three 'moves'.
        if (step>=3 and 
            record[step]==record[step-1]==record[step-2]==record[step-3]):
            break
        # terminate if the current square is the destination.
        if record[step]==end:
            journey_complete = True
            break
        # identify squares in the current field of vision.
        sight = environment.vision_field(record[step])
        changes = []
        # find and correct any visible errors in the drones knowledge.
        for square in sight:
            state = environment.get_state(square)
            if state!=information.get_state(square):
                changes.append(square)
                information.update_state(square,state)
        update_list = []
        # check if any of the corrections affect the current route.
        for square in changes:
            proximity = information.neighbours(square)
            for coord in proximity:
                if not coord in update_list:
                    update_list.append(coord)
            # (an unexpected empty square may lead to a better path)
            if (information.get_state(square)==grid_object.labels['empty'] or
                square in route):
                reroute_required = True
        information.update_risk(update_list)
        
        next_sight = information.vision_field(route[step+1])
        if ((step+1<len(route) and not route[step+1] in sight) or 
            (step+2<len(route) and not route[step+2] in next_sight)):
            reroute_required = True
        
        
        
        if reroute_required:
            plan = search.find_path(information,record[step],end,alpha,beta)
            # define new strategy as "journey so far" plus path to destination.
            strategies.append(record[0:step]+plan[1])
            # update 'route' to be the most recently devised path.
            route = strategies[-1]
        # if next square in 'route' is viable, continue journey.
        if step+1<len(route) and route[step+1] in sight:
            step+=1
        else :
            break
    return [cost,collisions,record,strategies,journey_complete]