# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 22:52:22 2018

@author: matth
"""

import numpy as np
import T_grid
from random import randint as rnd

labels = {'empty':0,'obstacle':1,'start':2,'radar':2.5,'end':4.5,'path':3.5}
directions = [[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]]

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
    __goals = []
    ##__directions = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]
    __seen = []
    __scanned = []
    def __init__(self,size,obstacles,capacity=0):
        '''
        'size' is a vector that defines the dimensions of the grid. 'obstacles'
        is a list of coordinate locations for permanent obstacles in the grid.
        '''
        self.__width = size[0]
        self.__height = size[1]
        self.__area = self.__width*self.__height
        self.__sense_range = self.__width+self.__height
        self.__states = np.zeros((self.__width,self.__height))
        self.__colour = np.zeros((self.__width,self.__height))
        # int is used because states will contain discrete classifications.
        self.__states = self.__states.astype(int)
        ##self.__start=start
        ##self.__end=end
        ##self.__colour[start[0]][start[1]] = labels['start']
        ##self.__colour[end[0]][end[1]] = labels['end']
        for ob in obstacles:
            self.__states[ob[0]][ob[1]] = labels['obstacle']
            self.__colour[ob[0]][ob[1]] = labels['obstacle']
        self.__total_obs = len(obstacles)
        self.__capacity = max([self.__total_obs,capacity])
        self.__risk = np.zeros((self.__width,self.__height))
        self.update_risk()
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
    
    def update_state(self,coord,value):
        '''
        Updates the state of a specified grid square.
        '''
        if self.__states[coord[0]][coord[1]]!=value:
            self.__states[coord[0]][coord[1]] = value
            if value==labels['empty']:
                self.__total_obs-=1
            elif value==labels['obstacle']:
                self.__total_obs+=1
    
    def get_state(self,coord=[]):
        '''
        Returns the state of a specified grid square. 
        '''
        if len(coord)==0:
            return self.__states
        else :
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
        Calculates a list of grid squares that are visible from a given input
        coordinate.
        MATT-TODO:This function could be made neater...
        '''
        visible = []
        for d in directions:
            # first deal with horizontal and vertical lines of sight.
            if d[0]*d[1]==0:
                # iterate through a maximum of three steps.
                for inc in range(1,self.__vision_range+1):
                    square = [coord[0]+inc*d[0],coord[1]+inc*d[1]]
                    included = False
                    # if 'square' is in the grid...
                    if self.is_in_grid(square):
                        # ... flag as visible
                        visible.append(square)
                        included = True
                        # if 'square' was not included or is not empty...
                    if (not included or
                        self.__states[square[0]][square[1]]!=labels['empty']):
                        # ... do not continue in current direction.
                        break
            # secondly, deal with diagonal lines of sight.
            else :
                blocked_x = False
                blocked_y = False
                # with diagonal lines of sight, iterate once fewer.
                for inc in range(1,self.__vision_range):
                    square = [coord[0]+inc*d[0],coord[1]+inc*d[1]]
                    # if 'square' is in the grid and not blocked...
                    included = False
                    if (self.is_in_grid(square)):
                        # check if off-diagonals are obstructed.
                        blocked_x = (self.__states[square[0]-d[0]][square[1]]==
                                     labels['obstacle'] or blocked_x)
                        blocked_y = (self.__states[square[0]][square[1]-d[1]]==
                                     labels['obstacle'] or blocked_y)
                        if not blocked_x or not blocked_y:
                            # ... flag as visible
                            visible.append(square)
                            included = True
                    # if 'square' was not included or is not empty...
                    if (not included or
                        self.__states[square[0]][square[1]]!=labels['empty']):
                        # ... do not continue in current direction.
                        break
        # vectors to check the grid squares missed by above directions.
        knight_moves = [[1,2],[-1,2],[1,-2],[-1,-2],
                        [2,1],[-2,1],[2,-1],[-2,-1]]
        for d in knight_moves:
            square = [coord[0]+d[0],coord[1]+d[1]]
            # define intermidiate moves between 'coord' and 'square'.
            s1 = [int(d[0]/abs(d[0])),int(d[1]/abs(d[1]))]
            s2 = [int(d[0]-s1[0]),int(d[1]-s1[1])]
            if (self.is_in_grid(square) and 
                self.__states[square[0]-s1[0]][square[1]-s1[1]]==
                labels['empty'] and
                self.__states[square[0]-s2[0]][square[1]-s2[1]]==
                labels['empty']):
                visible.append(square)
            else :
                continue
        return visible
    
    def update_risk(self,coord_list=[]):
        '''
        Updates the knowledge risk values of an optional selection of grid
        squares; by default, all values are updated. Risk due to knowledge is
        defined as the the likelihood of finding an unexpected obstacle in a
        grid square multiplied by the number of known neighbouring obstacles.
        '''
        aware = self.get_coords(labels['obstacle'])
        for s in self.__seen:
            if not s in aware:
                aware.append(s)
        if len(coord_list)==0:
            for x in range(0,self.__width):
                for y in range(0,self.__height):
                    surrounding_obstacles = 0
                    for d in directions:
                        square = [x+d[0],y+d[1]]
                        if (self.is_in_grid(square) and
                            self.__states[square[0]][square[1]]==
                            labels['obstacle']):
                            surrounding_obstacles+=1
                    unknown = ((self.__capacity-self.__total_obs)/
                               (self.__area-len(aware)))
                    self.__risk[x][y] = unknown*surrounding_obstacles
        else :
            for i in range(0,len(coord_list)):
                coord = coord_list[i]
                surrounding_obstacles = 0
                for d in directions:
                    square = [coord[0]+d[0],coord[1]+d[1]]
                    if (self.is_in_grid(square) and
                        self.__states[square[0]][square[1]]==
                        labels['obstacle']):
                        surrounding_obstacles+=1
                unknown = ((self.__capacity-self.__total_obs)/
                               (self.__area-len(aware)))
                self.__risk[coord[0]][coord[1]] = unknown*surrounding_obstacles
    
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
            for y in range(0,self.__height):
                if len(goal)>0:
                    self.__heuristic[x][y] = p2_dist([x,y],goal)
                else :
                    self.__heuristic[x][y] = 0
    
    def get_heuristic(self,coord=[]):
        '''
        Return the heuristic value for a given grid square or, by default, the
        entire array.
        '''
        if len(coord)==0:
            return self.__heuristic
        else :
            return self.__heuristic[coord[0]][coord[1]]
    
    def neighbours(self,coord,value=-1):
        '''
        Return a list of grid squares neighbouring a given coordinate with a
        specified state value.
        '''
        neighbs = []
        for d in directions:
            square = [coord[0]+d[0],coord[1]+d[1]]
            if (self.is_in_grid(square) and
                (self.__states[square[0]][square[1]]==value or value==-1)):
                neighbs.append(square)
        return neighbs
    
    def update_path_colour(self,coord_list,start,goals):
        '''
        Updates the colour of the path taken from start to end.
        '''
        for step in coord_list:
            if step==start:
                self.__colour[step[0]][step[1]] = labels['start']
            elif step in goals:
                self.__colour[step[0]][step[1]] = labels['end']
            else :
                self.__colour[step[0]][step[1]] = labels['path']
    
    def show_me(self):
        '''
        Displays grid in command window.
        '''
        T_grid.draw_grid(self.__colour)
    
    def get_colour(self,coord=0):
        '''
        return colour of specific square
        '''
        if len(coord==0):
            return self.__colour
        else:
            return self.__colour[coord[0]][coord[1]]
    
    def random_obs(self,obs_number,occupied=[]):
        '''
        Creates obs_number of obstacles randomly, anywhere that isn't in the occupied list
        occupied should be a list of coordinates such as: [[0,0],[5,4]].
        '''
        #exit if there are too many obstacles and not enough empty spaces
        if obs_number > self.__area - len(occupied):
            print('TOO MANY OBSTACLES')
            return None
        self.__total_obs+=obs_number
        self.__capacity+=obs_number
        #if occupied isn't empty
        if occupied != []:
            for i in range(0,obs_number):  
                obs_placed=False #remains false until the obstacle is placed
                while obs_placed==False:
                    #make 2 random coordinates
                    row=rnd(0,self.__height-1)
                    col=rnd(0,self.__width-1)          
                    #check if coordinate is not empty and not in occupied list
                    if self.__states[row][col]==labels['empty'] and [row,col] not in occupied :                
                        self.__states[row][col]=labels['obstacle']
                        obs_placed=True
        #if occupied empty
        else:
            for i in range(0,obs_number):  
                obs_placed=False #remains false until the obstacle is placed
                while obs_placed==False:
                    #make 2 random coordinates
                    row=rnd(0,self.__height-1)
                    col=rnd(0,self.__width-1)          
                    if self.__states[row][col]==labels['empty']:                
                        self.__states[row][col]=labels['obstacle']
                        obs_placed=True
    
    def get_capacity(self):
        '''
        Returns the maximum number of obstacles for the grid
        '''
        return self.__capacity
    
    def increment_capacity(self,obs_number):
        '''
        Increases the maximum number of obstacles for the grid.
        '''
        self.__capacity+=obs_number
        
    def get_coords(self,value):
        coord_list = []
        for x in range(0,self.__width):
            for y in range(0,self.__height):
                if self.get_state([x,y])==value:
                    coord_list.append([x,y])
        return coord_list
                    
    def radar_field(self,coord,show=False):
        squares_list = []
        for x in range(0,self.__width):
            for y in range(0,self.__height):
                if p2_dist([x,y],coord)<=self.__sense_range:
                    squares_list.append([x,y])
                    if show==True:
                        self.__colour[x][y]=labels['radar']
        return squares_list
    
    def set_goals(self,goals):
        self.__goals = []
        for g in goals:
            self.__goals.append(g)
    
    def get_goals(self):
        return self.__goals
    
    def update_sense_range(self,dist):
        self.__sense_range = dist
        self.__heuristic = dist*np.ones((self.__width,self.__height))
    
    def get_sense_range(self):
        return self.__sense_range
    
    def have_seen(self,new_coords):
        for square in new_coords:
            if not square in self.__seen:
                self.__seen.append(square)
    
    def have_scanned(self,new_coords):
        for square in new_coords:
            if not square in self.__scanned:
                self.__scanned.append(square)
    
    def get_seen(self):
        return self.__seen
    
    def get_scanned(self):
        return self.__scanned
    
    def non_overlap(self,memory,coord):
        #coord here is position of drone
        sensed=self.radar_field(coord)
        non_overlap=[x for x in sensed if x not in memory]
        return non_overlap
    
    def radar_iteration(self,possible_squares,memory):
        new_memory = []
        #1st phase
        #loop through all possible squares and extract the number of non overlapping squares
        for square in possible_squares:
            new_memory+=self.non_overlap(memory+new_memory,square)
        return len(new_memory)
        
    def construct_heuristic(self,curr,last,goal):
        clue = 0
        if p2_dist(curr,goal)<p2_dist(last,goal):
            clue = 1
        elif p2_dist(curr,goal)>p2_dist(last,goal):
            clue = -1
        #update_list = self.radar_field(current)
        #better_square = current
        #worse_square = last
        #if clue==-1:
        #    update_list = self.radar_field(last)
        #    better_square = last
        #    worse_square = current
        for x in range(0,self.get_width()):
            for y in range(0,self.get_height()):
                if ((clue==1 and (p2_dist([x,y],curr)>p2_dist([x,y],last) or
                                  p2_dist([x,y],curr)>self.__sense_range)) or
                    (clue==-1 and (p2_dist([x,y],last)>p2_dist([x,y],curr) or
                                   p2_dist([x,y],last)>self.__sense_range)) or
                    (clue==0 and (p2_dist([x,y],curr)!=p2_dist([x,y],last) or
                                  p2_dist([x,y],curr)>self.__sense_range))):
                    self.__heuristic[x][y]+=1