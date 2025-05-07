import pygame
import random
import math

pygame.init()

#frames per second
fps = 60


#Game-structure, and initial values
width, height = 800, 800
rows = 4
cols = 4 

rect_height= height // rows
rect_width= width = width // cols

outlinecol = (187, 173, 160)
outlinethick = 10
backgroundcol = (205, 192, 180)
fontcol = (119, 110, 101)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("2048")

font = pygame.font.SysFont("impact", 60, bold= True)
move_vel = 20

window = pygame.display.set_mode ((width, height))
pygame.display.set_caption("2048")




#Game developement
def draw(window):
    window.fill(backgroundcol)

    pygame.display.update()


def main (window):
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick (fps)

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run = False
                break

        draw(window)
    pygame.quit()

if __name__=="__main__":
    main(window)