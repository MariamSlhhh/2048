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
rect_width= width // cols

outlinecol = (187, 173, 160)
outlinethick = 10
backgroundcol = (205, 192, 180)
fontcol = (200, 191, 181)

WINDOW = pygame.display.set_mode((width, height))
pygame.display.set_caption("2048")

font = pygame.font.SysFont("impact", 60)
move_vel = 20


#Game structure

#class for functions necessary for game-usage, and continuety
class Tile:
    colors = [
        (72, 139, 73),
        (193, 131, 159),
        (214, 58, 249),
        (46, 41, 78),
        (105, 88, 95),
        (151, 216, 178),
        (147, 22, 33),
        (44, 140, 153),
        (255, 153, 20)
    ]

    def __init__(self, value, row, col):
        self._value = value
        self._row = row
        self._col = col
        self._x = col *rect_width
        self._y = row*rect_height

    def getcol (self):
        colorIndex = int (math.log2(self._value) -1)
        color = self.colors[colorIndex]
        return color

    def draw (self, window):
        color = self.getcol()
        pygame.draw.rect(window, color, (self._x, self._y, rect_width, rect_height))

        text = font.render (str(self._value), 1, fontcol)
        window.blit(
            text,
            (self._x + (rect_width/2- text.get_width() /2),
             self._y + (rect_height /2 -text.get_height() /2),
             ),
            )

    def setpos (self):
        pass

    def move (self, delta):
        pass

def draw_grid (window):
    for row in range (1, rows):
        y = row * rect_height
        pygame.draw.line(window, outlinecol, (0,y), (width, y), outlinethick)

    for col in range (1, cols):
        x = col * rect_width
        pygame.draw.line(window, outlinecol, (x, 0), (x, height), outlinethick)

    pygame.draw.rect(window, outlinecol, (0, 0, width, height), outlinethick)

def draw(window, tiles):
    window.fill(backgroundcol)

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)
    pygame.display.update()


def getRandomPos (tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)

        if f"{row}{col}" not in tiles:
            break

    return row, col


def generateTiles():
    tiles = {}
    for _ in range (2):
        row, col = getRandomPos (tiles)
        tiles [f"{row}{col}"] = Tile(2, row, col)

    return tiles


def main (window):
    clock = pygame.time.Clock()
    run = True

    tiles = generateTiles()

    while run:
        clock.tick (fps)

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run = False
                break

        draw(window, tiles)
    pygame.quit()

if __name__=="__main__":
    main(WINDOW)
