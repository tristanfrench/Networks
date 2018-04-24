    
def non_overlap(memory,coord):
    #coord here is position of drone
    sensed=grid.sense(coord,3)
    non_overlap=[x for x in sensed if x not in memory]
    
def radar_iteration(grid):
    memory=[]
    
    #1st phase
    while goal_found!=True:
        new_sensed=[]
        #loop through all possible squares and extract the number of non overlapping squares
        for square in possible_squares:
            new_sensed.append(non_overlap(memory,square))
        #this key=len means the max is calculated using the length of each item  i.e  [1,1,3,1] is "bigger" than [100,200]
        #least overlapp occurs when the length of the non overlappingg squares is largest
        least_overlap=max(new_sensed,key=len)
        #update memory
        memory+=least_overlap
        #update path
        #this gives the index of the max item
        my_index=new_sensed.index(least_overlap)
        path.append(possible_squares[my_index])
        
        
    #2nd phase