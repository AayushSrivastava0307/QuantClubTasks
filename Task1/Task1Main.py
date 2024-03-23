import pygame
import random
from math import pi,cos,sin,sqrt
import os as foldersave

#code reffered from this JS code https://codepen.io/SunPatch/pen/MKvYEa
# folder to save the images
foldername = "genimg"
if not foldersave.path.exists(foldername):
    foldersave.makedirs(foldername)

cols = 30
rows = 60
hexsize = 10
width = 3*hexsize # not width but the distance between centres of two adjacent hexagons of same column parity (odd col or even col)
#=3 times the radius(here hexsize)
height = hexsize * sqrt(3)/2 # simple height of hex based on its radius (use concept of equilateral triangle)
#defining my colors i like, you may change it as per need
charcoal=(54,69,79)
black=(0,0,0)
grey=(128,128,128)
yellow=(255,255,0)
#Yellow means alive and Grey is dead
# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((cols * width, rows * height)) #sets the grid according to the no of hexes correctly 
clock = pygame.time.Clock()

# our matrix function here i is just placeholder to iterate through loop
def creatematrix(rows, cols):
    matrix = []
    for i in range(rows):
        row = []
        for i in range(cols):
            row.append(0) #when board creation all cells are dead at that time
        matrix.append(row)
    return matrix

# board randomizer you may change the range of x and y to get random cells in that particular area of the board
currentboard = creatematrix(cols, rows)
for x in range(5, 25):
    for y in range(15, 45):
        currentboard[x][y] = random.randint(0, 1) # 0 is dead 1 is alive so in our random fxn 50-50 chance of dead or alive

# Function to count neighbours
def countneighbours(board, x, y):
    neighbours = 0 # gives me the live neighbours of the cell
    for dx, dy in [(0, -2), (0, -1), (0, 1), (0, 2), (1, -1), (1, 1)] if y % 2 == 0 else [(0, -2), (0, -1), (0, 1), (0, 2), (-1, -1), (-1, 1)]:
        nx, ny = x + dx, y + dy #uses the standard offset for hexagons checks if current row is odd or not and checks accordingly
        #note my dx dy has a (0,2) and (0,-2) because of the way i have generated and numbered my hexagons
        if 0 <= nx < cols and 0 <= ny < rows: # checks if my posn nx and ny is within the board bounds
            neighbours += board[nx][ny]
    return neighbours

# Function to draw the board with gridlines
def drawboard(board):
    # Draw hexagons
    for x in range(1, cols - 1):
        for y in range(1, rows - 1):
            color = yellow if board[x][y] == 1 else grey # if live then  yellow if dead then grey
            if y % 2 == 0:
                drawpoly((x * width) + width / 2, (y * height), hexsize, 6, color) # move by +width/2 extra because of the staggered nature of hexagon
            else:
                drawpoly((x * width), (y * height), hexsize, 6, color)

# standard code to draw a polygon
def drawpoly(x, y, radius, num_sides, color):
    angle = 2 * pi / num_sides #here it will be 60 for my hexagon 
    vertices = []
    for i in range(num_sides):
        px = x + radius * cos(i * angle)
        py = y + radius * sin(i * angle)
        vertices.append((px, py))
    pygame.draw.polygon(screen, color, vertices)
    pygame.draw.polygon(screen,charcoal, vertices, 1) #draws the grid lines in a greyish black color ie charcoal

# my main loop flag denotes if my code is running
# to keep track of generation number
generation = 0
flag=True
while flag:
    screen.fill(black)
    # counting  neighbours and update board
    nextboard = creatematrix(cols, rows)
    for x in range(1, cols - 1):
        for y in range(1, rows - 1):
            neighbours = countneighbours(currentboard, x, y)
            if currentboard[x][y] == 1 and neighbours < 2:
                nextboard[x][y] = 0  # logic for death by solitude
            elif currentboard[x][y] == 1 and neighbours > 3:
                nextboard[x][y] = 0  # logic for death by overpopulation
            elif currentboard[x][y] == 0 and neighbours == 3:
                nextboard[x][y] = 1  # logic for reproduction
            else:
                nextboard[x][y] = currentboard[x][y]  # otherwise move onto next genstasis ie at 2/3
                
    # Logic for  every 4 generations a random dead cell comes to life irrespective of the number of live neighbours
    if generation % 4 == 0:
        deadcells = [(x, y) for x in range(1,cols-1) for y in range(1,rows-1) if currentboard[x][y] == 0]
        if deadcells:
            xrand, yrand = random.choice(deadcells) #chooses one of the dead cells
            nextboard[xrand][yrand] = 1
    #couldnt think of a properly working code for resurrection of dead cells, and saving their state in which they previously died 
                
    currentboard = nextboard
    pygame.display.set_caption("Hexagonal Game Of Life - Generation: " + str(generation)) # a generation counted on the caption side
    drawboard(currentboard)
    pygame.display.flip()
    clock.tick(10)  # adjust the framerate accordingly 

    # saving the img
    pygame.image.save(screen, f"{foldername}/gen{generation}.png")
    generation += 1
 
    for event in pygame.event.get(): # for quiting hit the X 
        if event.type == pygame.QUIT:
            flag = False

pygame.quit()
