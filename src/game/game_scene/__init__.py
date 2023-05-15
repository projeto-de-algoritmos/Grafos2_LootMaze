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

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.back_button = pygame.Rect(0, WINDOW_HEIGHT - 100, 200, 80) 

    def draw_back_button(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.back_button)
        # You should replace this with your actual drawing code, especially if you want a more styled button

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self.running = False

    def run(self):
        # Limit the frame rate
        clock = pygame.time.Clock()

        # Create the grid
        grid = Grid("map_3.png")
        from pprint import pprint

        # Create the player
        player = Player(grid)

        solver = AStar(grid)
        # solver = Dijkstra(grid)
        # solver = DFS(grid)

        pprint(f"Empty path: {grid.path}")


        # Game loop
        while self.running:

            for event in pygame.event.get():
                self.handle_event(event)
            
            clock.tick(360/((len(grid.path)/2) + 1))
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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
            self.screen.fill((0, 0, 0))

            # Draw the grid
            grid.draw_grid(self.screen)

            # Draw the player
            player.draw(self.screen)

            self.draw_back_button()

            # Update the display
            pygame.display.flip()


        return self.running