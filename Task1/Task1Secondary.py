import pygame
import random
from math import *
import os as  foldersave

# Define a folder to save the images
foldername = "genimg"
if not foldersave.path.exists(foldername):
    foldersave.makedirs(foldername)

pygame.init()

black = (0, 0, 0)
grey = (128, 128, 128)
yellow = (255, 255, 0)

width, height = 800, 800
tilesize = 20
gridwidth = width // tilesize
gridheight = height // tilesize
FPS = 60

screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

def hex_corner(center, size, i):
    deg = 60 * i
    rad = pi / 180 * deg
    return center[0] + size * cos(rad), center[1] + size * sin(rad)

def generate(num):
    return set([(random.randrange(0, gridheight), random.randrange(0, gridwidth)) for _ in range(num)])

def draw_hexagon(center, size):
    corners = [hex_corner(center, size, i) for i in range(6)]
    pygame.draw.polygon(screen, yellow, corners, 0)

def draw_grid(positions):
    live_positions = set()  # Set to store live positions
    for position in positions:
        col, row = position
        live_positions.add((col, row))  # Add live positions to the set

    for position in positions:
        col, row = position
        x = col * 1.5 * tilesize
        y = row * sqrt(3) * tilesize
        if col % 2 == 1:
            y += sqrt(3) * tilesize / 2

        draw_hexagon((x, y), tilesize)
    # Draw grid outlines
    for row in range(gridheight):
        for col in range(gridwidth):
            x = col * 1.5 * tilesize
            y = row * sqrt(3) * tilesize
            if col % 2 == 1:
                y += sqrt(3) * tilesize / 2
            corners = [hex_corner((x, y), tilesize, i) for i in range(6)]
            pygame.draw.polygon(screen, black, corners, 1)


def adjust_grid(positions):
    new_positions = set()

    for position in positions:
        live_neighbors = sum(1 for neighbor in get_neighbors(position) if neighbor in positions)

        if live_neighbors == 2 or live_neighbors == 3:
            new_positions.add(position)

        for neighbor in get_neighbors(position):
            if neighbor not in positions:
                live_neighbors = sum(1 for n in get_neighbors(neighbor) if n in positions)
                if live_neighbors == 3:
                    new_positions.add(neighbor)

    return new_positions


def get_neighbors(pos):
    x, y = pos
    offsets = [(1, 0), (-1, 0), (0, -1), (0, 1), (-1, -1), (1, -1)] if x % 2 == 0 else [(1, 0), (-1, 0), (0, -1), (0, 1), (-1, 1), (1, 1)]
    neighbors = [(x + dx, y + dy) for dx, dy in offsets]
    return neighbors


def main():
    running = True
    playing = False
    count = 0
    gencounter = 0
    update_freq = 120

    positions = set()
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
        
        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)
            gencounter += 1
            
            # Save an image of the current gen
            filename = foldersave.path.join(foldername, f"gen{gencounter-1}.png")
            pygame.image.save(screen, filename)

        pygame.display.set_caption("Playing" if playing else "Paused")
        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = int(x / (1.5 * tilesize))
                row = int(y / (sqrt(3) * tilesize))
                if col % 2 == 1:
                    y -= sqrt(3) * tilesize / 2
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                    gencounter = 0
                
                if event.key == pygame.K_r:
                    positions = generate(random.randrange(8,16)*gridwidth)
                    gencounter = 0
    
        screen.fill(grey)
        draw_grid(positions)
        
        # Render gen counter text
        font = pygame.font.SysFont(None, 30)
        gen_text = font.render(f"Generation: {gencounter}", True, black)
        screen.blit(gen_text, (10, 10))
        pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    main()