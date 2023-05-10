from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
import pygame
import sys
import random
from time import sleep

from src.game.grid.grid import Grid
from src.game.player.player import Player
from src.game.path_algorithm.a_star import AStar
from src.game.path_algorithm.dijkstra import Dijkstra
from src.game.path_algorithm.DFS import DFS


if __name__ == '__main__':
    # Initialize Pygame
    pygame.init()

    # Set up the game window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Limit the frame rate
    clock = pygame.time.Clock()
    clock.tick(24)

    # Create the grid
    grid = Grid(24, 32)
    from pprint import pprint
    # pprint(grid.grid)


    # Create the player
    player = Player(grid)


    goal = (10,20)
    # solver = AStar(grid, player, goal)
    # solver = Dijkstra(grid, player, goal)
    solver = DFS(grid, player, goal)

    pprint(f'Empty path: {grid.path}')

    # Game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Perform a step of the pathfinder algorithm
        path, explored = solver.algorithm_tick()
        sleep(0.1)

        # If a path was found, store it
        if path is not None:
            print(f'Path: {path}')
            grid.path = path
            explored = explored - set(path)

        # Store the explored cells
        grid.explored = explored

        # Fill the window with red
        window.fill((0, 0, 0))

        # Draw the grid
        grid.draw_grid(window)

        # Draw the player
        player.draw(window)

        # Update the display
        pygame.display.flip()
