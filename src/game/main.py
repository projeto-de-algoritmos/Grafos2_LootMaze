from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
import pygame
import sys
import random
from time import sleep


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


class AStar:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal

        self.open_set = {start}
        self.came_from = {start: None}
        self.g_score = {start: 0}
        self.f_score = {start: self.heuristic(start, goal)}
        self.explored = set()

    def heuristic(self, cell, goal):
        # Manhattan distance
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    def get_neighbors(self, cell):
        # Returns walkable neighbors
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cell[0] + dx, cell[1] + dy
            if (0 <= nx < self.grid.width and 0 <= ny < self.grid.height and
                    self.grid.CELL_TYPE[self.grid.grid[ny][nx]]['walkable']):
                neighbors.append((nx, ny))
        return neighbors

    def a_star_tick(self):
        if not self.open_set:
            return None, self.explored  # No path found

        current = min(self.open_set, key=lambda cell: self.f_score[cell])
        self.explored.add(current)  # add current cell to explored set

        if current == self.goal:
            path = []
            while current is not None:
                path.append(current)
                current = self.came_from[current]
            path.reverse()
            return path, self.explored

        self.open_set.remove(current)

        for neighbor in self.get_neighbors(current):
            tentative_g_score = self.g_score[current] + self.grid.CELL_TYPE[self.grid.grid[neighbor[1]][neighbor[0]]]['cost']
            if neighbor not in self.g_score or tentative_g_score < self.g_score[neighbor]:
                self.came_from[neighbor] = current
                self.g_score[neighbor] = tentative_g_score
                self.f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.goal)
                if neighbor not in self.open_set:
                    self.open_set.add(neighbor)

        return None, self.explored  # Path not yet found


class Grid:

    CELL_SIZE = 10

    CELL_TYPE = {
        0: {
            'name': 'floor',
            'color': (255, 255, 255),
            'walkable': True,
            'cost': 1
        },
        1: {
            'name': 'wall',
            'color': (10, 0, 0),
            'walkable': False,
            'cost': 0
        },
        2: {
            'name': 'lava',
            'color': (255, 255, 0),
            'walkable': True,
            'cost': 10
        }

    }

    GRID_POSITION = (CELL_SIZE  * 2, CELL_SIZE * 2)

    path = []

    explored = []

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.create_walls()
        
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
                    cell_color = (255, 128, 128)
                elif (x, y) in self.explored:
                    cell_color = (0, 0, 255)
                else:
                    cell_color = self.CELL_TYPE[self.grid[y][x]]['color']

                pygame.draw.rect(
                    surface=screen,
                    color=cell_color,
                    rect=rect,
                    width=0,
                    border_radius=0                    
                )


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
    solver = AStar(grid, player, goal)

    pprint(grid.path)

    # Game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Perform a step of the A* algorithm
        path, explored = solver.a_star_tick()
        sleep(0.1)

        # If a path was found, store it
        if path is not None:
            print(path)
            grid.path = path
            explored = explored - set(path)
        else:
            print('Impossible path')

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
