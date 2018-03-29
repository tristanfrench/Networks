# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 22:37:24 2018

@author: matth
"""

import numpy as np

import grid_object
import search

def simulation(information,environment,start,end,alpha,beta):
    plan = search.find_path(information,start,end,alpha,beta)
    attempts = [plan[1]]
    route = attempts[-1]
    cost = 0
    record = []
    step = 0
    journey_complete = False
    while not journey_complete:
        record.append(route[step])
        cost+=grid_object.p2_dist(route[step],route[step-1])
        sight = environment.vision_field(route[step])
        check = information.vision_field(route[step])
        changes = []
        for square in sight:
            state = environment.get_state(square)
            if state!=information.get_state(square):
                changes.append(square)
                information.update_state(square,state)
        reroute_required = False
        for square in changes:
            if (information.get_state(square)==grid_object.labels['empty'] or
                (square in route)):
                reroute_required = True
                break
        if reroute_required:
            plan = search.find_path(information,route[step],end,alpha,beta)
            attempts.append(record[0:step]+plan[1])
            route = attempts[-1]
        if route[step+1] in sight:
            step+=1
        else :
            break
    return [cost,record,attempts]
        
        
        
        
        
        
        
        change_detected = False
        if len(sight)!=len(check):
            change_detected = True
        else :
            for i in range(0,len(sight)):
                if (sight[i][0]!=check[i][0] or sight[i][1]!=check[i][1] or
                    environment.get_state(sight[i])!=
                    information.get_state(check[i])):
                    change_detected = True
                    break
        if change_detected:
            
                
        
        
        
        
            