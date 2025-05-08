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
        (46, 41, 78),  # 2
        (193, 131, 159),   # 4
        (112, 103, 207),   
         (200, 100, 150),   # 8
         (44, 140, 153),    # 16
        (105, 88, 95),     # 32
        (7, 190, 184),   # 64
        (147, 22, 33),     # 128
        (101, 104, 57),      # 256
        (255, 153, 20),    # 512
        (214, 58, 249),   # 1024
        (200, 100, 150),   # 2048
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col *rect_width
        self.y = row*rect_height

    def getcol(self):
        exponent = math.log2(self.value)
        colorIndex = int(exponent) - 1
        colorIndex = min(colorIndex, len(self.colors) - 1)

        return self.colors[colorIndex]

    def draw (self, window):
        color = self.getcol()
        pygame.draw.rect(window, color, (self.x, self.y, rect_width, rect_height))

        text = font.render (str(self.value), 1, fontcol)
        window.blit(
            text,
            (self.x + (rect_width/2- text.get_width() /2),
             self.y + (rect_height /2 -text.get_height() /2),
             ),
            )

    def setPos (self, ceil = False):
        if ceil: 
            self.row = math.ceil (self.y / rect_height)
            self.col = math.ceil(self.x / rect_width)

        else:
            self.row = math.floor(self.y /rect_height)
            self.col = math.floor(self.x / rect_width)

    def move (self, delta):
        self.x += delta[0]
        self.y += delta[1]

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


def moveTiles (window, tiles, clock, direction):
    updated = True
    blocks = set()

    if direction == "left":
        sortFunc = lambda x: x.col 
        reverse = False
        delta = (-move_vel, 0)
        boundaryCheck = lambda tile: tile.col == 0 
        getNextTile = lambda tile: tiles.get (f"{tile.row}{tile.col-1}")
        mergeCheck = lambda tile, nextTile: tile.x > nextTile.x + move_vel
        move_check = (
            lambda tile, nextTile: tile.x > nextTile.x + rect_width + move_vel)
        ceil = True

    elif direction == "right":
        sortFunc = lambda x: x.col 
        reverse = True
        delta = (move_vel, 0)
        boundaryCheck = lambda tile: tile.col == cols -1
        getNextTile = lambda tile: tiles.get (f"{tile.row}{tile.col+1}")
        mergeCheck = lambda tile, nextTile: tile.x < nextTile.x - move_vel
        move_check = (
            lambda tile, nextTile: tile.x> nextTile.x + rect_width+ move_vel < nextTile.x)
        ceil = False

    elif direction=="up":
        sortFunc = lambda y: y.row 
        reverse = False
        delta = (0, -move_vel)
        boundaryCheck = lambda tile: tile.row == 0 
        getNextTile = lambda tile: tiles.get (f"{tile.row -1}{tile.col}")
        mergeCheck = lambda tile, nextTile: tile.y> nextTile.y + move_vel
        move_check = (
            lambda tile, nextTile: tile.y> nextTile.y + rect_height+ move_vel)
        ceil = True

    elif direction =="down":
        sortFunc = lambda y: y.row 
        reverse = True
        delta = (0, move_vel)
        boundaryCheck = lambda tile: tile.row == rows -1 
        getNextTile = lambda tile: tiles.get (f"{tile.row +1}{tile.col}")
        mergeCheck = lambda tile, nextTile: tile.y < nextTile.y - move_vel
        move_check = (
            lambda tile, nextTile: tile.y + rect_height + move_vel < nextTile.y)
        ceil = False

    while updated:
        clock.tick (fps)
        updated = False
        sortedTiles= sorted(tiles.values(), key = sortFunc, reverse=reverse)

        for i, tile in enumerate(sortedTiles):
            if boundaryCheck(tile):
                continue

            nextTile = getNextTile(tile)
            if not nextTile:
                tile.move(delta)

            elif (tile.value == nextTile.value 
                  and tile not in blocks 
                  and nextTile not in blocks
            ):
                if mergeCheck(tile, nextTile):
                    tile.move(delta)

                else:
                    nextTile.value *= 2
                    sortedTiles.pop(i)
                    blocks.add(nextTile)

            elif move_check (tile, nextTile):
                tile.move(delta)

            else:
                continue

            tile.setPos(ceil)
            updated = True

        updateTiles (window, tiles, sortedTiles)
    endTiles(tiles)

def endTiles(tiles):
    if len(tiles)==16:
        return "lost"
    
    row, col = getRandomPos(tiles)
    tiles [f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"

def updateTiles (window, tiles, sortedTiles):
    tiles.clear()
    for tile in sortedTiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)


def generateTiles():
    tiles = {}
    for _ in range (2):
        row, col = getRandomPos (tiles)
        tiles [f"{row}{col}"] = Tile(2, row, col)

    return tiles


#implements methods used on screen
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moveTiles(window, tiles, clock, "left")

                elif event.key == pygame.K_RIGHT:
                    moveTiles(window, tiles, clock, "right")

                elif event.key == pygame.K_UP:
                    moveTiles(window, tiles, clock, "up") 

                elif event.key == pygame.K_DOWN:
                    moveTiles(window, tiles, clock, "down")

        draw(window, tiles) 
    pygame.quit()

if __name__=="__main__":
    main(WINDOW)
