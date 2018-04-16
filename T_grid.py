import matplotlib.pyplot as plt
import numpy as np


def draw_grid(data):
    plt.close("all")
#    data=data*10000
    X,Y=np.shape(data)    
    # make a figure + axes
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    for x in range(X + 1):
        ax.axhline(x, lw=2, color='k')
    for y in range(Y+1):
        ax.axvline(y, lw=2, color='k')         
    # draw the boxes
    ax.imshow(data, interpolation='none', cmap='brg', extent=[0, Y, 0, X])    
    # turn off the axis labels
    ax.axis('off')
    



# Example:
#data = np.zeros((15,20))*100
#data[0,:]=1
#data[1,:]=1
#data[2,:]=1
#draw_grid(data)