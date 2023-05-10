import pygame


class Player:

    def __init__(self, grid):
        self.grid = grid
        self.position = (0, 0)
        self.color = (0, 255, 0)
        self.size = (grid.CELL_SIZE, grid.CELL_SIZE)

    def __getitem__(self, item):
        return self.position[item]

    def draw(self, screen):
        rect = pygame.Rect(
            self.grid.GRID_POSITION[0] + (self.position[0] * self.grid.CELL_SIZE),
            self.grid.GRID_POSITION[1] + (self.position[1] * self.grid.CELL_SIZE),
            self.size[0],
            self.size[1]
        )
        pygame.draw.rect(
            surface=screen,
            color=self.color,
            rect=rect,
            width=0,
            border_radius=0
        )