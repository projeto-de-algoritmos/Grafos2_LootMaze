import os
import random

import pygame

from src.config import (
    MAP_ASSETS_DIR,
    SPRITES_DIR,
    CELL_SIZE,
    GRID_X_OFFSET,
    GRID_Y_OFFSET,
    TILE_WIDTH,
    TILE_HEIGHT,
    CONVERSION_FACTOR_X,
    CONVERSION_FACTOR_Y
)


class Grid:

    CELL_SIZE = CELL_SIZE

    CELL_TYPE = {
        0: {
            'name': 'floor',
            'color': (255, 255, 255, 255),
            'walkable': True,
            'cost': 1,
            'image_filename': 'ground_tile.png'
        },
        1: {
            'name': 'wall',
            'color': (0, 0, 0, 255),
            'walkable': False,
            'cost': 0,
            'image_filename': 'wall_tile.png'
        },
        2: {
            'name': 'lava',
            'color': (255, 255, 0, 255),
            'walkable': True,
            'cost': 10,
            'image_filename': 'lava_tile.png'
        },
        3: {
            'name': 'spawn',
            'color': (0, 255, 0, 255),
            'walkable': True,
            'cost': 1,
            'image_filename': 'lava_tile.png'
        },
        4: {
            'name': 'goal',
            'color': (0, 0, 255, 255),
            'walkable': True,
            'cost': 1,
            'image_filename': 'lava_tile.png'
        },

    }

    # Map color to cell type
    COLOR_TO_CELL_TYPE = {v['color']: k for k, v in CELL_TYPE.items()}

    GRID_POSITION = (CELL_SIZE * 2, CELL_SIZE * 2)

    spawn = ()

    path = []

    goal = ()

    explored = []

    def __init__(self, filename):
        self.grid = self.load_from_file(filename)
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        
        # load tile images
        self.tile_images = {
            cell_type: self.load_tile(
                self.CELL_TYPE[cell_type]['image_filename']
            ) for cell_type in self.CELL_TYPE.keys()
        }

    @staticmethod
    def load_tile(image_file):
        tile_image = pygame.image.load(os.path.join(SPRITES_DIR, image_file)).convert()
        tile_image.set_colorkey((0, 0, 0))
        return tile_image

    def pixel_to_cell(self, pixel):
        return (
            (pixel[0] - self.GRID_POSITION[0]) // self.CELL_SIZE,
            (pixel[1] - self.GRID_POSITION[1]) // self.CELL_SIZE
        )
        
    def pixel_to_cell_type(self, color):
        return self.COLOR_TO_CELL_TYPE.get(tuple(color), 0)  # Convert color to tuple

    def load_from_file(self, filename):
        image = pygame.image.load(os.path.join(MAP_ASSETS_DIR, filename))
        maze_array = []

        for y in range(image.get_height()):
            row = []
            for x in range(image.get_width()):
                pixel_color = image.get_at((x, y))
                r, g, b, a = pixel_color

                if (r, g, b) == (0, 255, 0):  # green pixel for spawn
                    self.spawn = (x, y)
                    row.append(self.pixel_to_cell_type(pixel_color))
                elif (r, g, b) == (0, 0, 255):  # red pixel for goal
                    self.goal = (x, y)
                    row.append(self.pixel_to_cell_type(pixel_color))
                else:
                    row.append(self.pixel_to_cell_type(pixel_color))

            maze_array.append(row)

        # Make sure both spawn and goal were found
        if self.spawn is None:
            raise ValueError("Spawn point not found in image.")
        if self.goal is None:
            raise ValueError("Goal point not found in image.")

        print(f"Spawn point: {self.spawn} ")
        print(f"Goal point: {self.goal} ")

        return maze_array

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
                    cell_color = (255, 128, 128, 255)  # Pink
                elif (x, y) in self.explored:
                    cell_color = (0, 0, 255, 255)  # Blue
                elif (x, y) == self.goal:
                    cell_color = (255, 128, 0, 255)  # Orange
                else:
                    cell_color = self.CELL_TYPE[self.grid[y][x]]['color']

                pygame.draw.rect(
                    surface=screen,
                    color=cell_color,
                    rect=rect,
                    width=0,
                    border_radius=0                    
                )

                # Calculate tile position
                tile_x = GRID_X_OFFSET + (
                            x - y
                ) * TILE_WIDTH * CONVERSION_FACTOR_Y
                tile_y = GRID_Y_OFFSET + (
                    x + y
                ) * TILE_HEIGHT * CONVERSION_FACTOR_X
                tile_position = (tile_x, tile_y)


                # Scale tile image
                self.tile_images[self.grid[y][x]] = pygame.transform.scale(
                    self.tile_images[self.grid[y][x]],
                    (self.CELL_SIZE * CONVERSION_FACTOR_Y * 6, self.CELL_SIZE * CONVERSION_FACTOR_X * 10)
                )

                screen.blit(
                    self.tile_images[self.grid[y][x]],
                    tile_position
                )
