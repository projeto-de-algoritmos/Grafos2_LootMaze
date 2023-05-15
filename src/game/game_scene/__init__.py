import os
import pygame
import sys
import random
from time import sleep

from src.game.grid.grid import Grid
from src.game.player.player import Player
from src.game.path_algorithm.a_star import AStar
from src.game.path_algorithm.dijkstra import Dijkstra
from src.game.path_algorithm.DFS import DFS
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, SPRITES_DIR


class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.back_button = pygame.Rect(0, WINDOW_HEIGHT - 100, 200, 80) 
        self.button_tile = pygame.transform.scale(
            self.load_tile("button.png"), (200, 80)
        )

    @staticmethod
    def load_tile(image_file):
        tile_image = pygame.image.load(os.path.join(SPRITES_DIR, image_file)).convert()
        tile_image.set_colorkey((0, 0, 0))
        return tile_image

    def draw_back_button(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.back_button)
        self.screen.blit(self.button_tile, (0, WINDOW_HEIGHT - 100))
        # Write back text
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render("Back", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (100, WINDOW_HEIGHT - 60)
        self.screen.blit(text, textRect)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self.running = False

    def vertical_gradient(self, screen, top_color, bottom_color):
        for y in range(screen.get_height()):
            ratio = y / screen.get_height()
            color = (
                top_color[0] * (1 - ratio) + bottom_color[0] * ratio,
                top_color[1] * (1 - ratio) + bottom_color[1] * ratio,
                top_color[2] * (1 - ratio) + bottom_color[2] * ratio
            )
            pygame.draw.line(screen, color, (0, y), (screen.get_width(), y))

    def run(self, map_file):
        # Limit the frame rate
        clock = pygame.time.Clock()

        # Create the grid
        grid = Grid(map_file)

        # Create the player
        player = Player(grid)

        #solver = AStar(grid)
        solver = Dijkstra(grid)
        #solver = DFS(grid)

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
            self.vertical_gradient(self.screen, (50, 0, 50), (20, 0, 20))

            # Draw the grid
            grid.draw_grid(self.screen)

            # Draw the player
            player.draw(self.screen)

            self.draw_back_button()

            # Update the display
            pygame.display.flip()

        return self.running
