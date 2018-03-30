import matplotlib.pyplot as plt
import numpy as np


def draw_grid(data):
    
    X,Y=np.shape(data)    
    # make a figure + axes
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    for x in range(X + 1):
        ax.axhline(x, lw=2, color='k')
    for y in range(Y+1):
        ax.axvline(y, lw=2, color='k')         
    # draw the boxes
    ax.imshow(data, interpolation='none', cmap='hsv', extent=[0, Y, 0, X])    
    # turn off the axis labels
    ax.axis('off')
    

# Example:
# data = np.ones((15,20))*100
# data[0,:]=50
# data[1,:]=40
# data[2,:]=70
# draw_grid(data)