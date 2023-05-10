import random

import pygame


class Grid:

    CELL_SIZE = 10

    CELL_TYPE = {
        0: {
            'name': 'floor',
            'color': (255, 255, 255),
            'walkable': True,
            'cost': 1
        },
        1: {
            'name': 'wall',
            'color': (10, 0, 0),
            'walkable': False,
            'cost': 0
        },
        2: {
            'name': 'lava',
            'color': (255, 255, 0),
            'walkable': True,
            'cost': 10
        }

    }

    GRID_POSITION = (CELL_SIZE  * 2, CELL_SIZE * 2)

    path = []

    explored = []

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
                    self.GRID_POSITION[0] + (x * self.CELL_SIZE),
                    self.GRID_POSITION[1] + (y * self.CELL_SIZE),
                    self.CELL_SIZE,
                    self.CELL_SIZE
                )

                if (x, y) in self.path:
                    cell_color = (255, 128, 128)
                elif (x, y) in self.explored:
                    cell_color = (0, 0, 255)
                else:
                    cell_color = self.CELL_TYPE[self.grid[y][x]]['color']

                pygame.draw.rect(
                    surface=screen,
                    color=cell_color,
                    rect=rect,
                    width=0,
                    border_radius=0                    
                )
