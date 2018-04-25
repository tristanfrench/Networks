# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 23:34:52 2018

@author: matth
"""

import numpy as np

import grid_object

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

def find_path(grid,start,end,move_prob,alpha=1,beta=1):
    '''
    Calculates an optimal path through 'grid' from 'start' to 'end'. 'alpha'
    represents the relative weighting of the heuristic and 'beta' represents
    the relative weighting of the risk factors.
    '''
    # initialise flags for explored and frontier sets.
    num_squares = grid.get_width()*grid.get_height()
    explored = np.zeros((num_squares,1))
    explored = explored.astype(int)
    frontier = np.zeros((num_squares,1))
    frontier = frontier.astype(int)
    # initialise cost values.
    inf_cost = 2*num_squares
    cost = inf_cost*np.ones((num_squares,1))
    total_cost = 0
    # initialise estimate values (based on knowledge risk and heuristic) and 
    # movement risk - chance of drone colliding at least one along a path.
    informed = np.zeros((num_squares,1))
    collides = np.zeros((num_squares,1))
    estimate = np.zeros((num_squares,1))
    # initialise paths to grid squares.
    paths = []
    for index in range(0,num_squares):
        square = index2coord(index,grid.get_width())
        estimate[index] = (alpha*grid.get_heuristic(square)+
                           beta*grid.get_risk(square))
        paths.append([start])
    optimal_path = []
    # add the start point to the frontier with a cost of zero.
    start_index = coord2index(start,grid.get_width())
    frontier[start_index] = 1
    cost[start_index] = 0
    goal_reached = False
    while sum(frontier)>0:
        # find a grid square index in the frontier set with minimal cost.
        index = np.argmin((3-alpha-beta)*cost+estimate+beta*collides,axis=0)
        index = index[0]
        explored[index] = 1
        frontier[index] = 0
        # if the destination / goal is reached record cost and path, then exit.
        if index==coord2index(end,grid.get_width()):
            total_cost = cost[index]
            optimal_path = paths[index]
            goal_reached = True
            break
        parent = index2coord(index,grid.get_width())
        children = grid.neighbours(parent,grid_object.labels['empty'])
        # explore each grid square that can be moved to from current position.
        for child in children:
            if child in grid.vision_field(parent):
                # cost formula.
                new_cost = cost[index]+grid_object.p2_dist(child,parent)
                child_index = coord2index(child,grid.get_width())
                # if a less expensive path is found to an unexplored square
                # update cost, estimate, frontier, path and collision risk.
                if (explored[child_index]==0 and new_cost<cost[child_index]):
                    cost[child_index] = new_cost
                    frontier[child_index] = 1
                    paths[child_index] = paths[index]+[child]
                    coll_prob = collision_chance(grid,[paths[child_index]],
                                                 move_prob)
                    collides[child_index] = sum(coll_prob[0])
                    informed[child_index] = informativeness(paths[child_index])
        # reset cost of explored grid square.
        cost[index] = inf_cost
    if not goal_reached:
        return [inf_cost,paths]
    else :
        return [total_cost[0],optimal_path]

def schedule_paths(grid,start,ordered_goals,move_prob,alpha=1,beta=1):
    '''
    Calculates an optimal path through 'grid' from 'start' which visits each
    square in 'ordered_goals' in turn. 'alpha' represents the relative 
    weighting of the heuristic and 'beta' represents the relative weighting
    of the risk factors.
    '''
    checkpoints = [start]+ordered_goals
    combined_cost = 0
    combined_route = [start]
    for n in range(0,len(ordered_goals)):
        grid.update_heuristic(ordered_goals(n))
        plan = find_path(grid,checkpoints[n],checkpoints[n+1],move_prob,
                         alpha,beta)
        combined_cost+=plan[0]
        combined_route = combined_route+plan[1][1:]
    return [combined_cost,combined_route]

def adjacency(grid,start,goal_list,move_prob,alpha=1,beta=1):
    '''
    Constructs the adjacency matrix for 'grid' squares in the union of 'start'
    and 'goal_list'. Each entry of the matrix is the cost of the optimal path
    found between each pair of grid squares.
    '''
    node_list = [start]+goal_list
    matrix = np.zeros((len(node_list),len(node_list)))
    for n1 in range(0,len(node_list)):
        for n2 in range(0,len(node_list)):
            plan = find_path(grid,node_list[n1],node_list[n2],move_prob,
                             alpha,beta)
            matrix[n1][n2] = plan[0]
    return matrix

def collision_chance(grid,path_list,move_prob):
    '''
    Calculates the probability that a drone will collide with an obstacle at
    each point on a set of routes.
    '''
    coll_mat = []
    for path in path_list:
        chance_list = []
        for s in range(0,len(path)-1):
            chance = 0
            obstacles = grid.neighbours(path[s],grid_object.labels['obstacle'])
            if len(obstacles)!=0:
                action = [path[s+1][0]-path[s][0],path[s+1][1]-path[s][1]]
                action_ind = grid_object.directions.index(action)
                for ob in obstacles:
                    bad_move = [ob[0]-path[s][0],ob[1]-path[s][1]]
                    bad_ind = grid_object.directions.index(bad_move)
                    chance+=move_prob[(bad_ind+action_ind)%len(move_prob)]
            chance*=move_prob[0]**s
            chance_list.append(chance)
        coll_mat.append(chance_list)
    return coll_mat

def informativeness(grid,path):
    return 0