    
def non_overlap(memory,coord):
    #coord here is position of drone
    sensed=grid.sense(coord,3)
    non_overlap=[x for x in sensed if x not in memory]
    return non_overlap
    
def radar_iteration(grid,possible_squares):
    memory=[]
    
    #1st phase
 
        #loop through all possible squares and extract the number of non overlapping squares
    for square in possible_squares:
        memory+=non_overlap(memory,square)

    return len(memory)
        
        
    #2nd phase
    
    #first need to get to the goal point found
    #set objective square as goal?
    #once you've reached goal
    #continue in direction, find change in heuristics, if positive
#    past_H=get_heuristic([_,_])
#    future_H=get_heuristic([_,_])
#    if future_H-past_H<0:
#        #do stuff, heuristic decreased
#    else:
        #pick different direction
        
    