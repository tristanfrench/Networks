import pygame as pg


def main(tiles_per_row,tiles_per_col):
    #Initialisation stuff
    pg.init()
    
    BLACK = pg.Color('black')
    WHITE = pg.Color('white')
    RED = pg.Color('red')
    
    total_w=800
    total_h=600
    
    tile_w = int(total_w/tiles_per_row)
    tile_h = int(total_h/tiles_per_col)
    
    total_w=tiles_per_row*tile_w
    total_h=tiles_per_col*tile_h
    
    screen = pg.display.set_mode((total_w, total_h))
    clock = pg.time.Clock()
    
    background = pg.Surface((total_w, total_h))
    background.fill(WHITE)
    
    #Grid making
    for y in range(0,total_h,tile_h):
        for x in range(0,total_w,tile_w):
            rect = (x, y, tile_w, tile_h)
            pg.draw.rect(background, BLACK, rect,1)
    
    #Game loop
    game_exit = False
    while not game_exit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True
    
        screen.fill((60, 70, 90))
        screen.blit(background, (0, 0))
    
        pg.display.flip()
        clock.tick(30)
    
    pg.quit()









tiles_per_row,tiles_per_col=7,7

main(tiles_per_row,tiles_per_col)