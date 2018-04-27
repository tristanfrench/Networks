import numpy as np

import grid_object
import journey
import performance
import matplotlib.pyplot as plt

def results_plotting():
    print(a)

#create an environment...
sizeB = (10,10)
ob1 = [[3,4],[4,4],[3,3],[4,5]]
ob2 = [[6,8],[7,8],[8,8],[9,8]]
ob3 = [[2,5],[3,4],[4,3],[5,2]]
obstacles = ob1+ob2+ob3
env = grid_object.grid(sizeB,obstacles,len(obstacles))
            
            #create parameter vectors...
knowledge = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
movement = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
num_goals = [0,1,2,3,4,5,6,7,8,9,10]
min_dist = [0,1,2,3,4,5,6,7,8,9,10]
alphas = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5]
betas = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5]
repeat = [0,1,2,3,4,5]
            
            #to test various proportions of initial knowledge with
            #deterministic movement, a single goal placed at least 2 units 
            #(measured by euclidean distance) away from the start point,
            #standard alpha and beta values (both equal to 1), and to have
            #each set of results averaged over 5 simulations*...
results1 = performance.analyse(env,[knowledge[-1]],movement,
                               num_goals[1],min_dist[2],
                               [alphas[10]],[betas[10]],repeat[5],[1,0])


y=len(results1)
testing_para=[]
efficiency=[]
for row in range(0,y):
    efficiency.append(results1[row][4])
    testing_para.append(results1[row][1])
        
print(efficiency)

'''
OUTPUT:[knowledge,movement,alpha,beta,cost,collisions,start,goals]

'''


plt.plot(testing_para,efficiency)
