# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 22:52:22 2018

@author: matth
"""

import numpy as np

labels = {'empty':0,'obstacle':1}

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
        # int is used because states will contain discrete classifications.
        self.__states = self.__states.astype(int)
        for ob in obstacles:
            self.__states[ob[0]][ob[1]] = labels['obstacle']
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
    
    def get_state(self,coord):
        '''
        Returns the matrix of state indices. Empty grid spaces are represented
        by zeros and obstacles with ones. 
        '''
        return self.__states[coord[0]][coord[1]]
    
    def is_in_grid(self,coord):
        '''
        Checks whether an input coordinate is within the boundaries of the
        grid.
        '''
        if 0<=coord[0]<self.__width and 0<=coord[1]<self.__height:
            return True
        return False
    
    def vision_field(self,coord):
        '''
        Calculates a list of grid spaces that are visible from a given input
        coordinate.
        '''
        visible = []
        for d in self.__directions:
            # first deal with horizontal and vertical lines of sight.
            if d[0]*d[1]==0:
                # iterate through a maximum of three steps.
                for inc in range(1,self.__vision_range+1):
                    squ = [coord[0]+inc*d[0],coord[1]+inc*d[1]]
                    visible.append(squ)
                    if (not self.is_in_grid(self,squ) or
                        self.__states[squ[0]][squ[1]]!=labels['empty']):
                        break
            else :
                blocked_x = False
                blocked_y = False
                # with diagonal lines of sight, iterate once fewer.
                for inc in range(1,self.__vision_range):
                    squ = [coord[0]+inc*d[0],coord[1]+inc*d[1]]
                    # check if off-diagonals are obstructed.
                    blocked_x = (self.__states[squ[0]-d[0]][squ[1]]==
                                 labels['obstacle'] or blocked_x)
                    blocked_y = (self.__states[squ[0]][squ[1]-d[1]]==
                                 labels['obstacle'] or blocked_y)
                    if (self.is_in_grid(self,squ) and
                        (not blocked_x or not blocked_y) and
                        self.__states[squ[0]][squ[1]]==labels['empty']):
                        visible.append(squ)
                    else :
                        break
        # vectors to check the grid squares missed by above directions.
        knight_moves = [[1,2],[-1,2],[1,-2],[-1,-2],
                        [2,1],[-2,1],[2,-1],[-2,-1]]
        for d in knight_moves:
            squ = [coord[0]+d[0],coord[1]+d[1]]
            # define intermidiate moves between 'coord' and 'squ'.
            s1 = [d[0]/abs(d[0]),d[1]/abs(d[1])]
            s2 = [d[0]-s1[0],d[1]-s1[1]]
            if (self.is_in_grid(self,squ) and 
                self.__states[squ[0]-s1[0]][squ[1]-s1[1]]==labels['empty'] and
                self.__states[squ[0]-s2[0]][squ[1]-s2[1]]==labels['empty']):
                visible.append(squ)
            else :
                continue
        return visible
    
    def update_risk(self,squares=[]):
        '''
        Updates the risk values of an optional selection of grid squares; by
        default, all values are updated.
        '''
        if len(squares)==0:
            for x in range(0,self.__width):
                for y in range(1,self.__height):
                    surrounding_obstacles = 0
                    for d in self.__directions:
                        squ = [x+d[0],y+d[1]]
                        if (self.is_in_grid(squ) and
                            self.__states[squ[0]][squ[1]]==labels['obstacle']):
                            surrounding_obstacles+=1
                    self.__risk[x][y] = surrounding_obstacles
        else :
            for i in range(0,len(squares)):
                coord = squares[i]
                surrounding_obstacles = 0
                for d in self.__directions:
                    squ = [coord[0]+d[0],coord[1]+d[1]]
                    if (self.is_in_grid(squ) and
                        self.__states[squ[0]][squ[1]]==labels['obstacle']):
                        surrounding_obstacles+=1
                self.__risk[coord[0]][coord[1]] = surrounding_obstacles
    
    def get_risk(self,coord=[]):
        '''
        Return the risk value for a given grid square or, by default, the
        entire array.
        '''
        if len(coord)==0:
            return self.__risk
        else :
            return self.__risk[coord[0]][coord[1]]
    
    def update_heuristic(self,goal):
        '''
        Stores the values of the heuristic for each grid square, calculated
        as the euclidean distance between grid squares and a goal square.
        '''
        for x in range(0,self.__width):
            for y in range(0,self.___height):
                self.__heuristic[x][y] = p2_dist([x,y],goal)
    
    def get_heuristic(self,coord=[]):
        '''
        Return the heuristic value for a given grid square or, by default, the
        entire array.
        '''
        if len(coord)==0:
            return self.__heuristic
        else :
            return self.__heuristic[coord[0]][coord[1]]
    
    def neighbours(self,coord,desc):
        '''
        Return a list of grid squares neighbouring a given coordinate with a
        specified state.
        '''
        neighbs = []
        for d in self.__directions:
            squ = [coord[0]+d[0],coord[1]+d[1]]
            if self.is_in_grid(squ) and self.__states[squ[0]][squ[1]]==desc:
                neighbs.append(squ)
        return neighbs