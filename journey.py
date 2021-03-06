# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 22:37:24 2018

@author: matth
"""

import numpy as np
import itertools as it

import grid_object
import search

outputs = {'cost':0,'collisions':1,'record':2,'strategies':3,'complete':4}

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

def simulation(information,environment,start,goals,move_prob,alpha=1,beta=1):
    '''
    Runs a theoretical simulation of a drone travelling through a grid trying
    to get from 'start' to 'end'. 'information' represents the drones knowledge
    of its surroundings and 'environment' represents the drones actual
    surrounds.'alpha' and 'beta' represent the weightings of the heuristic and
    risk to be used when finding paths.
    '''
    #environment.set_goals(goals)
    remaining_goals = []
    for g1 in environment.get_goals():
        remaining_goals.append(g1)
    known_goals = []
    for g2 in information.get_goals():
        known_goals.append(g2)
    Adj = search.adjacency(information,start,known_goals,move_prob,alpha,beta)
    order = travelling_salesman(Adj)
    ordered_goals = []
    for i in order:
        ordered_goals.append(known_goals[i-1])
    # Calculate initial plan and store the path found as the first strategy.
    #print(['ordered_goals',ordered_goals])
    information.set_goals(ordered_goals)
    plan = search.schedule_paths(information,start,ordered_goals,
                                 move_prob,alpha,beta)
    #print(plan)
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
        #print(step)
        #print(record)
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
            d_num = grid_object.directions.index(move_intent)
            ##for d_num in range(0,total_moves):
            ##    if grid_object.directions[d_num]==move_intent:
            ##        break
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
        if record[step] in remaining_goals and record[step] in known_goals:
            remaining_goals.remove(record[step])
            known_goals.remove(record[step])
            if len(remaining_goals)==0:
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
            if square in remaining_goals and not square in known_goals:
                known_goals.append(square)
                reroute_required = True
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
        information.have_seen(sight)        
        information.have_scanned(information.radar_field(record[step]))
        information.update_risk(update_list)
        if len(remaining_goals)!=len(known_goals):
            for goal in remaining_goals:
                if (goal in information.radar_field(record[step]) and
                    not goal in known_goals):
                    information.construct_heuristic(record[step],
                                                    record[step-1],goal)
                    known_goals.append(goal)###################################
                    reroute_required = True
        # Potentially a redundant check??? - Answer: no it's definitely not!
        if step+1<len(route):
            next_sight = information.vision_field(route[step+1])
            if (not route[step+1] in sight or 
                (step+2<len(route) and not route[step+2] in next_sight)):
                reroute_required = True
        if step+1==len(route):
            reroute_required = True
        if reroute_required:
            information.set_goals(known_goals)
            Adj = search.adjacency(information,record[step],known_goals,
                                   move_prob,alpha,beta)
            order = travelling_salesman(Adj)
            ordered_goals = []
            for i in order:
                ordered_goals.append(known_goals[i-1])
            information.set_goals(ordered_goals)
            plan = search.schedule_paths(information,record[step],
                                         ordered_goals,move_prob,alpha,beta)
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

def travelling_salesman(Adj):
    #inf = float('inf')
    d = Adj
    
    points = range(0,d.shape[0])
    
    combinations = list(it.permutations(points,len(points)))
    
    total_distances=[]
    
    for i in range(len(combinations)):
        summation=0
        if combinations[i][0] == 0:
            for j in range(len(combinations[i])-1):
                #if j==3:
                #    continue
                #else:
                summation += d[combinations[i][j]][combinations[i][j+1]]
            total_distances.append(summation)
        
    #min_dist=min(total_distances)
    
    for i in total_distances:
        if i==min(total_distances):
            index=total_distances.index(i)
            x=list(combinations[index])
        else:
            continue
        del x[0]
            
    return x