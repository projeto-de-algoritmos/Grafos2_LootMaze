import os
import random

import pygame

from src.config import ASSETS_DIR


class Grid:

    CELL_SIZE = 10

    CELL_TYPE = {
        0: {
            'name': 'floor',
            'color': (255, 255, 255, 255),
            'walkable': True,
            'cost': 1
        },
        1: {
            'name': 'wall',
            'color': (0, 0, 0, 255),
            'walkable': False,
            'cost': 0
        },
        2: {
            'name': 'lava',
            'color': (255, 255, 0, 255),
            'walkable': True,
            'cost': 10
        }

    }

    # Map color to cell type
    COLOR_TO_CELL_TYPE = {v['color']: k for k, v in CELL_TYPE.items()}

    GRID_POSITION = (CELL_SIZE  * 2, CELL_SIZE * 2)

    path = []

    explored = []

    def __init__(self, filename):
        self.grid = self.load_from_file(filename)
        # self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def pixel_to_cell_type(self, color):
        print(color)
        return self.COLOR_TO_CELL_TYPE.get(tuple(color), 0)  # Convert color to tuple

    def load_from_file(self, filename):
        image = pygame.image.load(os.path.join(ASSETS_DIR, filename))
        print(self.COLOR_TO_CELL_TYPE)
        return [
            [
                self.pixel_to_cell_type(image.get_at((x, y))) for x in range(image.get_width())
            ] for y in range(image.get_height())
        ]

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
                    cell_color = (255, 128, 128) # Pink
                elif (x, y) in self.explored:
                    cell_color = (0, 0, 255) # Blue
                else:
                    cell_color = self.CELL_TYPE[self.grid[y][x]]['color']

                pygame.draw.rect(
                    surface=screen,
                    color=cell_color,
                    rect=rect,
                    width=0,
                    border_radius=0                    
                )
