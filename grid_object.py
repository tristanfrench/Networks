# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 22:52:22 2018

@author: matth
"""

import numpy as np

def p2_dist(a,b):
    '''
    Calculates the euclidean distance between two points 'a' and 'b'. This is
    used as the distance measure when calculating the heuristics of states.
    '''
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

class grid:
    '''
    'grid' objects will have a set value for 'vision_range', which will be used
    to define the maximum boundaries of a drones field of vision. 'directions'
    simply stores vectors for horizontal, vertical and diagonal movements.
    '''
    __vision_range = 3
    __directions = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]
    
    def __init__(self,size,obstacles):
        '''
        'size' is a vector that defines the dimensions of the grid. 'obstacles'
        is a list of coordinate locations for permanent obstacles in the grid.
        '''
        self.__width = size[0]
        self.__height = size[1]
        self.__states = np.zeros((self.__width,self.__height))
        self.__states = self.__states.astype(int)                               # int is used because states will contain discrete classifications.
        for ob in obstacles:
            self.__states[ob[0]][ob[1]] = 1
        self.__risk = np.zeros((self.__width,self.__height))
        self.__heuristic = np.zeros((self.__width,self.__height))
    
    def get_width(self):
        '''
        Returns the number of columns in the grid.
        '''
        return self.__width
    
    def get_height(self):
        '''
        Returns the number of rows in the grid.
        '''
        return self.__height
    
    def get_state(self):
        '''
        Returns the matrix of state indices. Empty grid spaces are represented
        by zeros and obstacles with ones. 
        '''
        return self.__states
    
    def is_in_grid(self,coord):
        '''
        Checks whether an input coordinate is within the boundaries of the
        grid.
        '''
        if 1<=coord[0]<=self.__width and 1<=coord[1]<=self.__height:
            return True
        return False
    
    def vision_field(self,coord):
        '''
        Calculates a list of grid spaces that are visible from a given input
        coordinate.
        '''
        visible = []
        for d in self.__directions:
            if d[0]*d[1]==0:                                                    # deal with horizontal and vertical sight lines.
                for inc in range(1,self.__vision_range+1):                      # iterate through a maximum of three steps.
                    squ = [coord[0]+inc*d[0],coord[1]+inc*d[1]]                 # define new grid square.
                    visible.append(squ)                                         # add new square to list of visible coordinates.
                    if (self.__states[squ[0]][squ[1]]!=0 or
                        not self.is_in_grid(self,squ)):                         # if the square contains an obstacle or is not in the grid...
                        break                                                   # move on to next direction.
            else :                                                              # deal with diagonal sight lines separately.
                blocked_x = False
                blocked_y = False
                for inc in range(1,self.__vision_range):                        # iterate one less step than for vetical / horizontal directions.
                    squ = [coord[0]+inc*d[0],coord[1]+inc*d[1]]
                    blocked_x = (self.__states[squ[0]-d[0]][squ[1]]==1 or       # check if off-diagonals are obstructed.
                                 blocked_x)
                    blocked_y = (self.__states[squ[0]][squ[1]-d[1]]==1 or
                                 blocked_y)
                    if ((not blocked_x or not blocked_y) and
                        self.__states[squ[0]][squ[1]]==0 and
                        self.is_in_grid(self,squ)):                             # if at least one off-diagonal is un-obstructed...
                        visible.append(squ)                                     # add new square to list of visible coordinates.
                    else :
                        break
        knight_moves = [[1,2],[-1,2],[1,-2],[-1,-2],
                        [2,1],[-2,1],[2,-1],[-2,-1]]                            # vectors to check the grid squares missed by above directions.
        for d in knight_moves:
            squ = [coord[0]+d[0],coord[1]+d[1]]
            step1 = [d[0]/abs(d[0]),d[1]/abs(d[1])]                             # define intermidiate grid squares.
            step2 = [d[0]-step1[0],d[1]-step1[1]]
            if (self.__states[step1[0]][step1[1]]==0 and
                self.__states[step2[0]][step2[1]]==0 and
                self.is_in_grid(self,squ)):                                     # if no intermideiate grid squares are blocked by obstacles...
                visible.append(squ)                                             # add new square to list of visible coordinates.
            else :
                continue
        return visible
    
    def update_risk(self,squares=[]):
        '''
        Updates the risk values of an optional selection of grid squares; by
        default, all values are updated.
        '''
        if len(squares)==0:                                                     # if no coordinates are specified, update all values
            for x in range(0,self.__width):
                for y in range(1,self.__height):
                    surrounding_obstacles = 0
                    for d in self.__directions:
                        if self.__states[x+d[0]][y+d[1]]==1:                    # counts the nummber of obstacles in neighbouring grid squares.
                            surrounding_obstacles+=1
                    self.__risk[x][y] = surrounding_obstacles
        else :                                                                  # if a list of coordinates are given...
            for i in range(0,len(squares)):                                     # update only the risk values for those grid squares.
                coord = squares[i]
                surrounding_obstacles = 0
                for d in self.__directions:
                    if self.__states[coord[0]+d[0]][coord[1]+d[1]]==1:
                        surrounding_obstacles+=1
                self.__risk[coord[0]][coord[1]] = surrounding_obstacles
    
    def get_risk(self,coord):
        '''
        Return the risk value for a given grid square.
        '''
        return self.__risk[coord[0]][coord[1]]
    
    def set_heuristic(self,goal):
        '''
        Stores the values of the heuristic for each grid square, calculated
        as the euclidean distance between grid squares and a goal square.
        '''
        for x in range(0,self.__width):
            for y in range(0,self.___height):
                self.__heuristic[x][y] = p2_dist([x,y],goal)
    
    def get_heuristic(self,coord):
        '''
        Return the heuristic value for a given grid square.
        '''
        return self.__heuristic[coord[0]][coord[1]]
    
'''random test commands'''
size = (10,10)
ob1 = [[3,4],[4,4],[3,3],[4,5]]
ob2 = [[6,8],[7,8],[8,8],[9,8]]
obstacles = ob1+ob2
drone_map = grid(size,obstacles)
environment = grid(size,[])