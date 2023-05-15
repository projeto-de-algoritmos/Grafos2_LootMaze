import os

import pygame

from src.config import (
    SPRITES_DIR,
    CELL_SIZE,
    GRID_X_OFFSET,
    GRID_Y_OFFSET,
    TILE_WIDTH,
    TILE_HEIGHT,
    CONVERSION_FACTOR_X,
    CONVERSION_FACTOR_Y,
)


class Player:
    def __init__(self, grid):
        self.grid = grid
        self.path = []
        self.position = self.grid.spawn
        self.color = (0, 255, 0)
        self.size = (grid.CELL_SIZE, grid.CELL_SIZE)
        self.player_image = self.load_tile("mage.png")

    def __getitem__(self, item):
        return self.position[item]
    
    def reset(self):
        self.position = self.grid.spawn

    def draw(self, screen):
        rect = pygame.Rect(
            self.grid.GRID_POSITION[0] + (self.position[0] * self.grid.CELL_SIZE),
            self.grid.GRID_POSITION[1] + (self.position[1] * self.grid.CELL_SIZE),
            self.size[0],
            self.size[1],
        )
        pygame.draw.rect(
            surface=screen, color=self.color, rect=rect, width=0, border_radius=0
        )

        player_x, player_y = self.position[0], self.position[1]

        # Calculate tile position
        tile_x = (
            GRID_X_OFFSET + (player_x - player_y) * TILE_WIDTH * CONVERSION_FACTOR_Y
        )
        tile_y = (
            GRID_Y_OFFSET + (player_x + player_y) * TILE_HEIGHT * CONVERSION_FACTOR_X
        )
        tile_position = (tile_x, tile_y)

        # Scale tile image
        self.player_image = pygame.transform.scale(
            self.player_image,
            (CELL_SIZE * CONVERSION_FACTOR_Y * 5, CELL_SIZE * CONVERSION_FACTOR_X * 10),
        )

        # Adjust player's position to account for depth
        tile_position = (tile_position[0], tile_position[1] - CELL_SIZE * 4)

        screen.blit(self.player_image, tile_position)

    def acknoledge_path(self, path):
        if not self.path:
            self.path = path

    def execute_action(self):
        try:
            self.position = self.path.pop(0)

        except IndexError:
            pass

    @staticmethod
    def load_tile(image_file):
        tile_image = pygame.image.load(os.path.join(SPRITES_DIR, image_file)).convert()
        tile_image.set_colorkey((0, 0, 0))
        return tile_image
