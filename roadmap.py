# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 23:16:08 2018

@author: JamesDL
"""

import obstacles_store as os
import grid_object
import journey
import numpy as np
np.set_printoptions(threshold=np.inf)

sizeB = (30,30)
startB = [0,0]
endB = [29,29]

street1 = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[8,1],[8,2],[8,3],[8,4],
[0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[5,4],[5,5],[5,6],[5,7],[5,8],[5,9],[5,10]]
obstacles = os.hroad(3,0) + os.vroad(0,3)

inf = grid_object.grid(sizeB,[],startB,endB)
inf.update_risk()
inf.update_heuristic(endB)

env = grid_object.grid(sizeB,obstacles,startB,endB)
env.update_risk()
env.update_heuristic(endB)

move_prob1 = [1,0,0,0,0,0,0,0]
move_prob2 = [0.9,0.1,0,0,0,0,0,0]

results3 = journey.simulation(inf,env,startB,endB,move_prob1)
env.update_path_colour(results3[2])
env.show_me()
