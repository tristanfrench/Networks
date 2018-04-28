import matplotlib.pyplot as plt
import numpy as np






def draw_grid(data,wait_for=False):
#    plt.close("all")
#    data=data*10000
    X,Y=np.shape(data)    
    # make a figure + axes
    for col in range(0,X):
        for row in range(0,Y):
            if data[row,col]==0:
                data[row,col]=None
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    for x in range(X + 1):
        ax.axhline(x, lw=2, color='k')
    for y in range(Y+1):
        ax.axvline(y, lw=2, color='k')  
   
#     draw the boxes
    ax.imshow(data, interpolation='none', cmap='brg', extent=[0, Y, 0, X])    
#     turn off the axis labels
    ax.axis('off')
    if wait_for==True:
        plt.waitforbuttonpress()
    return data
    
