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
        self.font = pygame.font.Font(None, 36)


        self.steps_counter_text = "passos: "
        self.lesser_path = "menor caminho: "

        # table -> [solver_name, steps, lesser_path]
        self.table_data = [
            ["A*", 0, 0],
            ["Dijkstra", 0, 0],
            ["DFS", 0, 0]
        ]

    def draw_back_button(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.back_button)
        # You should replace this with your actual drawing code, especially if you want a more styled button
    
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

        solvers = [
            AStar(grid),
            Dijkstra(grid),
            DFS(grid)
        ]
        current_solver_index = 0
        current_solver = solvers[current_solver_index]

        pprint(f"Empty path: {grid.path}")

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
            self.screen.fill((0, 0, 0))

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
