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


def handle_mouse_click():
    global goal, grid
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        goal = grid.pixel_to_cell(pos)
        grid.path = []
        grid.explored = []
        grid.goal = goal
        solver.goal = goal
        print(f"Goal: {goal}")


if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Set up the game window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Limit the frame rate
    clock = pygame.time.Clock()

    # Create the grid
    grid = Grid("map_2.png")
    from pprint import pprint

    # pprint(grid.grid)

    # Create the player
    player = Player(grid)

    solver = AStar(grid)
    # solver = Dijkstra(grid)
    # solver = DFS(grid)

    pprint(f"Empty path: {grid.path}")

    # Game loop
    while True:
        clock.tick(30)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player has no goal
        # if not solver.goal and not grid.path:
        # Player clicks on goal pixel
        # handle_mouse_click()

        # Player has a goal
        if solver.goal:
            # Perform a step of the pathfinder algorithm
            path, explored = solver.algorithm_tick()

            # If a path was found, store it
            if path is not None:
                grid.path = path
                explored = explored - set(path)
                player.acknoledge_path(path)

            # Store the explored cells
            grid.explored = explored

        player.execute_action()

        # Fill the window with black
        window.fill((0, 0, 0))

        # Draw the grid
        grid.draw_grid(window)

        # Draw the player
        player.draw(window)

        # Update the display
        pygame.display.flip()
