from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
import pygame
import sys
import random


class Grid:

    cell_size = 20

    CELL_TYPE = {
        0: {
            'name': 'floor',
            'color': (255, 255, 255),
            'walkable': True
        },
        1: {
            'name': 'wall',
            'color': (255, 0, 0),
            'walkable': False
        }
    }
    

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.create_walls()
        
    def create_walls(self):
        # create random walls assigning 1 to random cells on the grid
        for y in range(self.height):
            for x in range(self.width):
                if random.randint(0, 100) < 20:
                    self.grid[y][x] = 1

    def draw_grid(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size, 
                    self.cell_size
                )
                cell_color = self.CELL_TYPE[self.grid[y][x]]['color']
                pygame.draw.rect(
                    surface=screen,
                    color=cell_color,
                    rect=rect,
                    width=0,
                    border_radius=0                    
                )


if __name__ == '__main__':
    # Initialize Pygame
    pygame.init()

    # Set up the game window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    grid = Grid(24, 32)
    from pprint import pprint; pprint(grid.grid)


    # Game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill the window with red
        window.fill((0, 0, 0))

        # Draw the grid
        grid.draw_grid(window)

        # Update the display
        pygame.display.flip()
