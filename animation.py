import numpy as np
from T_grid import draw_grid

def path_animation(grid,path):
    grid_seen=np.zeros((grid.get_height(),grid.get_width()))
    for square in path:
        for i in grid.vision_field(square):
            grid_seen[i[0]][i[1]]=grid.get_colour([i[0],i[1]])+1
        grid_seen[square[0]][square[1]]=4.5
        draw_grid(grid_seen,True)

    return grid_seen