import numpy as np

import grid_object
import journey
import performance
import matplotlib.pyplot as plt
import gridStore


def get_results(knowledge,movement,results_nb,goals_nb,repeat_nb):
    #create an environment...
    sizeB = (10,10)
    ob1 = [[3,4],[4,4],[3,3],[4,5]]
    ob2 = [[6,8],[7,8],[8,8],[9,8]]
    ob3 = [[2,5],[3,4],[4,3],[5,2]]
    ob4 = [[5,6],[5,7]]
    obstacles=ob1+ob2+ob3#+ob4
#    
#    ob1=[[3,4],[3,6],[4,4],[4,6],[5,4],[5,6],[6,4],[6,6],[7,4],[7,6]]
#    obstacles=ob1
    obstacles = gridStore.obs
    sizeB=(30,30)
    env = grid_object.grid(sizeB,obstacles,len(obstacles))
  
    
                
                #create parameter vectors...
    
    num_goals = [0,1,2,3,4,5,6,7,8,9,10]
    min_dist = [0,1,2,3,4,5,6,7,8,9,10,15]
    '''
    alpha is heuristic
    beta is risk
    '''
    
    #test for cost
    alphas_c = [1.5,1.4,1.3,1.2,1.1,1.0,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0]
    betas__c = [1.5,1.4,1.3,1.2,1.1,1.0,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0]
    
    #test for heuristic
    alphas_h = [0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0]
    betas__h = [1.5,1.4,1.3,1.2,1.1,1.0,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0]
    
    #test fot risk
    alphas_r = [1.5,1.4,1.3,1.2,1.1,1.0,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0]
    betas__r = [0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0]
    
    repeat = [0,1,2,3,4,5,6,7,8,9,10]
    results=[]
    
    alphas = [alphas_r[-2]]
    betas = [betas__r[-2]]
    alphas = [1]
    betas = [1]

    for i in range(0,results_nb):
        results.append(performance.analyse(env,knowledge,movement,
                                   num_goals[goals_nb],min_dist[5],
                                   alphas,betas,repeat[repeat_nb],[2,4]))

    env.update_path_colour(results[0][0][-1],results[0][0][-3],results[0][0][-2])
    env.show_me()
    return results



k = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
m = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5]



results_nb=1
goals_nb=1
repeat_nb=1
'''
CHOOSE PARA TO STUDY
'''
PARA='k'

print('COLLECTING RESULTS')
if PARA=='m':
    result_list=get_results([k[-1]],m,results_nb,goals_nb,repeat_nb)
elif PARA=='k':
    result_list=get_results(k,[m[0]],results_nb,goals_nb,repeat_nb)
elif PARA=='c':
    result_list=get_results([k[-1]],[m[0]],results_nb,goals_nb,repeat_nb)
elif PARA=='h':
    result_list=get_results([k[-1]],[m[0]],results_nb,goals_nb,repeat_nb)
elif PARA=='r':
    result_list=get_results([k[-1]],[m[1]],results_nb,goals_nb,repeat_nb)

rl=len(result_list)

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
    elif PARA== 'c':
        for row in range(0,y):        
            efficiency[i].append(result[row][4])
            testing_para[i].append(3-result[row][2]-result[row][3])#alpha
    elif PARA== 'h':
        for row in range(0,y):        
            efficiency[i].append(result[row][4])
            testing_para[i].append(result[row][2])#alpha
    elif PARA== 'r':
        for row in range(0,y):        
            efficiency[i].append(result[row][4])
            testing_para[i].append(result[row][3])#alpha

            



'''
OUTPUT:[knowledge,movement,alpha,beta,cost,collisions,start,goals]
'''
print('x axis',testing_para)
print('y axis',efficiency)
for i in range(0,rl):
    plt.figure()
    plt.plot(testing_para[i],efficiency[i])
    plt.xlabel('Knowledge')
    plt.ylabel('Efficiency')
    plt.title('Efficiency against knowledge with deterministic movement ')
    


plt.xlabel('Probability of deviating')
plt.ylabel('Efficiency')
plt.title('Efficiency against Probability of deviating ')

