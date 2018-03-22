# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 22:52:22 2018

@author: matth
"""

import numpy as np

def p2_dist(a,b):
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

class grid:
    __vision_range = 3
    __directions = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]   
    
    def __init__(self,size,obstacles):
        self.__width = size[0]
        self.__height = size[1]
        self.__obstacles = np.zeros((self.__width,self.__height))
        self.__obstacles = self.__obstacles.astype(int)
        for ob in obstacles:
            self.__obstacles[ob[0]][ob[1]] = 1
    
    def get_width(self):
        return self.__width
    
    def get_height(self):
        return self.__height
    
    #def is_obstacle(self,coord):
    #    for ob in self.__obstacles:
    #       if ob[0]==coord[0] and ob[1]==coord[1]:
    #           return True
    #    return False
    
    def is_in_grid(self,coord):
        if 1<=coord[0]<=self.__width and 1<=coord[1]<=self.__height:
            return True
        return False
    
    def vision_field(self,coord):
        visible = []
        for d in self.__directions:
            if d[0]*d[1]==0:
                for inc in range(1,self.__vision_range+1):
                    squ = [coord[0]+inc*d[0],coord[1]+inc*d[1]]
                    if (self.__obstacles[squ[0]][squ[1]]==0 and
                        self.is_in_grid(self,squ)):
                        visible.append(squ)
                    else :
                        break
            else :
                blocked_x = False
                blocked_y = False
                for inc in range(1,self.__vision_range):
                    squ = [coord[0]+inc*d[0],coord[1]+inc*d[1]]
                    blocked_x = (self.__obstacles[squ[0]-d[0]][squ[1]]==1 or
                                 blocked_x)
                    blocked_y = (self.__obstacles[squ[0]][squ[1]-d[1]]==1 or
                                 blocked_y)
                    if ((not blocked_x or not blocked_y) and
                        self.__obstacles[squ[0]][squ[1]]==0 and
                        self.is_in_grid(self,squ)):
                        visible.append(squ)
                    else :
                        break
        knight_moves = [[1,2],[-1,2],[1,-2],[-1,-2],
                        [2,1],[-2,1],[2,-1],[-2,-1]]
        for d in knight_moves:
            squ = [coord[0]+d[0],coord[1]+d[1]]
            step1 = [d[0]/abs(d[0]),d[1]/abs(d[1])]
            step2 = [d[0]-step1[0],d[1]-step1[1]]
            if (self.__obstacles[step1[0]][step1[1]]==0 and
                self.__obstacles[step2[0]][step2[1]]==0 and
                self.is_in_grid(self,squ)):
                visible.append(squ)
            else :
                continue
        return visible
    
    def set_risk(self):
        self.__risk = np.zeros((self.__width,self.__height))
        for x in range(0,self.__width):
            for y in range(1,self.__height):
                surrounding_obstacles = 0
                for d in self.__directions:
                    if self.__obstacles[x+d[0]][y+d[1]]==1:
                        surrounding_obstacles+=1
                self.__risk[x][y] = surrounding_obstacles
    
    def set_heuristic(self,goal):
        self.__heuristic = np.zeros((self.__width,self.__height))
        for x in range(0,self.__width):
            for y in range(0,self.___height):
                self.__heuristic[x][y] = p2_dist([x,y],goal)
                
                

size = (10,10)
ob1 = [[3,4],[4,4],[3,3],[4,5]]
ob2 = [[6,8],[7,8],[8,8],[9,8]]
obstacles = ob1+ob2
drone_map = grid(size,obstacles)
environment = grid(size,[])