import itertools
import pygame as pg


pg.init()

BLACK = pg.Color('black')
WHITE = pg.Color('white')
RED = pg.Color('red')
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

colors = itertools.cycle((WHITE, BLACK))
tile_size = 5
width, height = 8*tile_size, 8*tile_size
background = pg.Surface((width, height))
#background.fill(WHITE)

#for y in range(height):
#    for x in range(width):
#        rect = (x, y, 1, tile_size)
#        pg.draw.rect(background, BLACK, rect)

rect = (10,1, 1, tile_size)
pg.draw.rect(background, BLACK, rect)
rect = (20,10, 10, tile_size)
pg.draw.rect(background, WHITE, rect)
game_exit = False
while not game_exit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    screen.fill((60, 70, 90))
    screen.blit(background, (400, 300))

    pg.display.flip()
    clock.tick(30)

pg.quit()