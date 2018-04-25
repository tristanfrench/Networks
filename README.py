# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 20:53:30 2018

@author: matth
"""

'''
IMPORTANT FILES

-----performance.py-----
this file contains functions that allow you to analyse the performance of a
drone with a variety of parameter values.

CONTENTS:
    analyse(environment,knowledge,movement,num_goals,
            min_dist,alphas,betas,repeat):
        
        - description:
            a function that runs many simulations of a drone and outputs
            parameter values and results.
            
        - inputs:
            environment = a grid object with the complete set of obstacles.
            
            knowledge = a vector of values between 0 and 1 representing the
            proportion of obstacles in 'environment' the drone will be aware of
            at the start of each simulation
            
            movement = a vector of values between 0 and 1 representing the
            probability that the drone deviates from it's intended path at each
            step.
            
            num_goals = a scalar value indicating how many goals should be
            randomly placed for the simulation
            
            min_dist = a scalar value indicating the minimum distance between 
            the start point and the goals and between each pair of the goals.
            
            alphas = a vector of values* representing the relative weighting of
            heuristics to be used for route finding.
            
            betas = a vector of values* representing the relative weighting of
            risk factors to be used for route finding.
            
                *NOTE: each pairwise sum of alpha and beta values must be
                between 0 and 3. So 0<=alphas[n]+betas[n]<=3 must be true for
                all n. 
            
            repeat = a scalar value that determines the number of times a
            simulation should be repeated (and averaged over) for a given set
            of parameter values (described above).
            
        - examples:
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
            results1 = performance.analyse(env,knowledge,movement[0],
                                           num_goals[1],min_dist[2],
                                           alphas[10],betas[10],repeat[5])
            
                *NOTE: since in this case the movement is deterministic,
                averaging over multiple simulations is not necessary as the
                results will be identical for the same parameter values.
            
            #to instead test various likelihoods of deviation for zero initial
            #knowledge and the same conditions as above...
            results2 = performance.analyse(env,knowledge[0],movement,
                                           num_goals[1],min_dist[2],
                                           alphas[10],betas[10],repeat[5])
            
            #to instead test pairs of alpha and beta values when there is no
            #initial knowledge and a 10% chance that the drone will deviate at
            #each step...
            results3 = performance.analyse(env,knowledge[0],movement[1],
                                           num_goals[1],min_dist[2],
                                           alphas,betas,repeat[5])
            
        - outputs:
            results = a list of vectors containing the results of each set of
            simulations. Each vector in 'results' contains the parameter values
            that were used in that simulation, the difference between the
            actual cost of the drones journey and the cost of the optimal path,
            the average number of collisions that occured, as well as the start
            and end points. For example...
                results[n] = [k,m,a,b,av_cost,av_colls,start,goals]
            where the knowledge was 'k', the likelihood of deviation was 'm',
            alpha was 'a', beta was 'b', the average differrence in cost 
            between the simulations and the optimals is 'av_cost', the average
            number of collisions is 'av_colls, the random start point was
            'start' and the randomly placed goals were 'goals'.

