import pygame
import numpy as np

# Initialize Pygame
pygame.init()

import sys
from os import path

def newPath(relPath: str):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, relPath)  # type: ignore -> pyinstaller temp folder
    else:
        return path.join(path.abspath('.'), relPath)

screen_width, screen_height = 640, 480  # adjust this to your desired screen size
screen = pygame.display.set_mode((screen_width, screen_height))

image = pygame.image.load(newPath("assets/img/bg/ocean.png"))

# Get the image dimensions
image_width, image_height = image.get_size()

# Set the tile size
tile_size = (50, 50)  # adjust this to your desired tile size

# Create a 2D array to store the tile pattern
pattern = np.zeros((tile_size[1], tile_size[0], 3), dtype=np.uint8)

# Fill the pattern array with the image data
for y in range(tile_size[1]):
    for x in range(tile_size[0]):
        pattern[x, y] = image.get_at((x % image_width, y % image_height))[:3]

# Create a surface from the pattern array
surface = pygame.surfarray.make_surface(pattern)

# Multiply the surface to fill the screen
for y in range(0, screen_height, tile_size[1]):
    for x in range(0, screen_width, tile_size[0]):
        screen.blit(surface, (x, y))

# Update the screen
pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
