import numpy as np

import grid_object
import journey
import performance
import matplotlib.pyplot as plt
#import gridStore


def get_results(knowledge,movement,results_nb,goals_nb,repeat_nb):
    #create an environment...
    sizeB = (10,10)
    ob1 = [[3,4],[4,4],[3,3],[4,5]]
    ob2 = [[6,8],[7,8],[8,8],[9,8]]
    ob3 = [[2,5],[3,4],[4,3],[5,2]]
    ob4 = [[5,6],[5,7]]
    obstacles=ob1+ob2+ob3+ob4
#    obstacles = gridStore.obs
#    sizeB=(30,30)
    env = grid_object.grid(sizeB,obstacles,len(obstacles))
    env.show_me()
                
                #create parameter vectors...
    
    num_goals = [0,1,2,3,4,5,6,7,8,9,10]
    min_dist = [0,1,2,3,4,5,6,7,8,9,10]
    alphas = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5]
    betas = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5]
    repeat = [0,1,2,3,4,5,6,7,8,9,10]
    results=[]

    for i in range(0,results_nb):
        results.append(performance.analyse(env,knowledge,movement,
                                   num_goals[goals_nb],min_dist[2],
                                   [alphas[10]],[betas[10]],repeat[repeat_nb],[1,0]))
    return results



k = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
m = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5]


results_nb=1
goals_nb=1
repeat_nb=5
'''
CHOOSE PARA TO STUDY
'''
PARA='k'

print('COLLECTING RESULTS')
if PARA=='m':
    result_list=get_results([k[-1]],m,results_nb,goals_nb,repeat_nb)
elif PARA=='k':
    result_list=get_results(k,[m[0]],results_nb,goals_nb,repeat_nb)
rl=len(results)

print('PLOTTING RESULTS')
testing_para=np.zeros(rl)
efficiency=[[],[],[]]
testing_para=[[],[],[]]

i=-1

for result in result_list:
    y=len(result)
    i+=1
    if PARA=='m':
        for row in range(0,y):        
            efficiency[i].append(result[row][4]-3*result[row][5])
            testing_para[i].append(result[row][1])
    elif PARA== 'k':
        for row in range(0,y):        
            efficiency[i].append(result[row][4])
            testing_para[i].append(result[row][0])


'''
OUTPUT:[knowledge,movement,alpha,beta,cost,collisions,start,goals]
'''
for i in range(0,rl):
    plt.figure()
    plt.plot(testing_para[i],efficiency[i])
    
#if PARA=='m'

