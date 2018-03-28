# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 23:34:52 2018

@author: matth
"""

import numpy as np

import grid_object.py as go

def coord2index(coord,width):
    '''
    Converts a grid coordinate to a unique scalar index. 'width' is the number
    of columns in the grid.
    '''
    return coord[0]+coord[1]*width

def index2coord(index,width):
    '''
    Converts a scalar index to a unique grid coordinate. 'width' is the number
    of columns in the grid.
    '''
    return [index%width,index//width]

def find_path(grid,start,end,alpha=1,beta=1):
    '''
    Calculates an optimal path through 'grid' from 'start' to 'end'. 'alpha'
    repreents the relative weighting of the heuristic and 'beta' represents the
    relative weighting of the risk.
    '''
    # initialise flags for explored and frontier sets.
    num_states = grid.get_width()*grid.get_height()
    explored = np.zeros((num_states,1))
    explored = explored.astype(int)
    frontier = np.zeros((num_states,1))
    frontier = frontier.astype(int)
    # initialise cost values.
    max_cost = 2*num_states
    cost = max_cost*np.ones((num_states,1))
    total_cost = 0
    # initialise paths.
    paths = []
    for s in range(0,num_states):
        paths.append([start])
    optimal_path = []
    # add the start point to the frontier with a cost of zero.
    start_index = coord2index(start,grid.get_width())
    frontier[start_index] = 1
    cost[start_index] = 0
    while sum(frontier)>0:
        # find a grid square index in the frontier set with minimal cost.
        index = np.argmin(cost,axis=0)
        explored[index] = 1
        frontier[index] = 0
        current_cost = cost[index]
        # reset cost of explored grid square.
        cost[index] = max_cost
        # if the destination / goal is reached record cost and path, then exit.
        if index==coord2index(end,grid.get_width()):
            total_cost = current_cost
            optimal_path = paths[index]
            break
        parent = index2coord(index,grid.get_width())
        children = grid.neighbours(parent,'empty')
        # explore each grid square that can be moved to from current position.
        for child in children:
            # cost formula.
            new_cost = (alpha*grid.get_heuristic(child)+
                        beta*grid.get_risk(child)+
                        (3-alpha-beta)*go.p2_dist(child,parent))
            child_index = coord2index(child,grid.get_width())
            parent_index = coord2index(parent,grid.get_width())
            # if a less expense path is found to an unexplored grid square,
            # update the cost, frontier flag and path.
            if (explored[child_index]==0 and new_cost<cost[child_index]):
                cost[child_index] = new_cost
                frontier[child_index] = 1
                paths[child_index] = paths[parent_index]+[child]
    return [total_cost,optimal_path]
