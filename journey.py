# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 22:37:24 2018

@author: matth
"""

import numpy as np

import grid_object
import search

def simulation(information,environment,start,end,alpha=1,beta=1):
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
    journey_complete = False
    while not journey_complete:
        # move to the next square listed in the current route and update cost.
        record.append(route[step])
        cost+=grid_object.p2_dist(record[step],record[step-1])
        # terminate if the current square is the destination.
        if record[step][0]==end[0] and record[step][1]==end[1]:
            journey_complete = True
            break
        # identify squares ni the current field of vision.
        sight = environment.vision_field(record[step])
        changes = []
        # find and correct any visible errors in the drones knowledge.
        for square in sight:
            state = environment.get_state(square)
            if state!=information.get_state(square):
                changes.append(square)
                information.update_state(square,state)
        reroute_required = False
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
    return [cost,record,strategies,journey_complete]