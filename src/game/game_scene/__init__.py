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
        self.font = pygame.font.Font(None, 36)
        self.steps_counter_text = "passos: "
        self.lesser_path = "menor caminho: "
        # table -> [solver_name, steps, lesser_path]
        self.table_data = [
            ["A*", 0, 0],
            ["Dijkstra", 0, 0],
            ["DFS", 0, 0]
        ]
        self.button_tile = pygame.transform.scale(
            self.load_tile("button.png"), (200, 80)
        )

    def draw_table(self, table_data):
        # Títulos das colunas
        column_titles = ["", "Steps", "Path"]
        
        # Desenhar os contadores de etapas no canto superior direito
        for i in range(len(table_data)):
            for j in range(len(table_data[i])):
                # Desenhar os dados da tabela
                text = self.font.render(str(table_data[i][j]), True, (255, 0, 0))
                text_rect = text.get_rect(center=(WINDOW_WIDTH - 100 + (j * 100) - 300, 150 + (i * 30) - 100))
                self.screen.blit(text, text_rect)
                
                # Desenhar os títulos das colunas
                if i == 0:
                    title_text = self.font.render(column_titles[j], True, (255, 0, 0))
                    title_rect = title_text.get_rect(center=(WINDOW_WIDTH - 100 + (j * 100) - 300, 120 - 100))
                    self.screen.blit(title_text, title_rect)

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

    def run(self):
        # Limit the frame rate
        clock = pygame.time.Clock()

        # Create the grid
        grid = Grid("map_2.png")

        # Create the player
        player = Player(grid)

        solvers = [
            AStar(grid),
            Dijkstra(grid),
            DFS(grid)
        ]
        current_solver_index = 0
        current_solver = solvers[current_solver_index]

        # Game loop
        while self.running:
            # Event handling
            for event in pygame.event.get():
                self.handle_event(event)
            
            clock.tick(360/((len(grid.path)/2) + 1))
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Player has a goal
            if current_solver.goal:

                if player.position == grid.spawn and self.table_data[current_solver_index][2] != 0:
                    self.table_data[current_solver_index][1] = 0
                    self.table_data[current_solver_index][2] = 0

                # Perform a step of the pathfinder algorithm
                path, explored = current_solver.algorithm_tick()

                # If a path was found, store it
                if path is not None:
                    grid.path = path
                    explored = explored - set(path)
                    player.acknoledge_path(path)
                    self.table_data[current_solver_index][2] = len(path)
                else:
                    self.table_data[current_solver_index][1] += 1

                # Store the explored cells
                grid.explored = explored

            player.execute_action()

            # Check if the player has reached the goal
            if player.position == grid.goal:
                # Move to the next solver
                current_solver_index = (current_solver_index + 1) % len(solvers)
                current_solver = solvers[current_solver_index]
                player.reset()
                grid.reset()
                current_solver.reset()

            # Fill the window with black
            self.vertical_gradient(self.screen, (50, 0, 50), (20, 0, 20))

            # Draw the grid
            grid.draw_grid(self.screen)

            # Draw the player
            player.draw(self.screen)

            # Draw the counters
            self.draw_table(self.table_data)

            self.draw_back_button()

            # Update the display
            pygame.display.flip()

        return self.running
