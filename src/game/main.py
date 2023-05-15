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

from src.game.game_scene import GameScene


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
    
    game_scene = GameScene(window)

    game_scene.run()
