import numpy as np
from T_grid import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import grid_object
import journey


np.set_printoptions(threshold=np.inf)

def path_animation2(grid,square,start,goals,obs):
#    path_len=len(path)
#    grid_list= [[] for x in range(path_len)]
    grid_seen=np.zeros((grid.get_height(),grid.get_width()))
    obstacle=[]
        
    for i in grid.vision_field(square):
        grid_seen[i[0]][i[1]]=grid.get_colour([i[0],i[1]])+1
        if grid.get_colour([i[0],i[1]])==1:
            obstacle.append(i[:])
            
    grid_seen[square[0]][square[1]]=4.5
    for i in goals:
        grid_seen[i[0]][i[1]]=7          
    grid_seen[0][0]=7
    for sq in obs:
        if sq!=[]:
            grid_seen[sq[0]][sq[1]]=2   
    return grid_seen,obstacle


def path_animation(grid,path,start,goals):
    grid_seen=np.zeros((grid.get_height(),grid.get_width()))
    for square in path:
        for i in grid.vision_field(square):
            grid_seen[i[0]][i[1]]=grid.get_colour([i[0],i[1]])+1
            
        grid_seen[square[0]][square[1]]=4.5
        for i in goals:
            grid_seen[i[0]][i[1]]=7          
        grid_seen[0][0]=7






