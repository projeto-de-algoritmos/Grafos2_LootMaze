from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
import pygame
import sys
import random



class Player:

    def __init__(self, grid):
        self.grid = grid
        self.position = (0, 0)
        self.color = (0, 255, 0)
        self.size = (grid.CELL_SIZE, grid.CELL_SIZE)

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
            'color': (255, 0, 0),
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

    def get_neighbors(self, cell):
        neighbors = []
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # 4-connectivity
            x, y = cell[0] + dx, cell[1] + dy
            if 0 <= x < self.width and 0 <= y < self.height and self.CELL_TYPE[self.grid[y][x]]['walkable']:
                neighbors.append((x, y))
        return neighbors

    def heuristic(self, cell1, cell2):
        return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])  # Manhattan distance


    def a_star(self, start, goal):
        open_set = {start}
        came_from = {start: None}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current = min(open_set, key=lambda cell: f_score[cell])

            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                self.path = path
                return

            open_set.remove(current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + self.CELL_TYPE[self.grid[neighbor[1]][neighbor[0]]]['cost']
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    if neighbor not in open_set:
                        open_set.add(neighbor)

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
                    cell_color = (128, 128, 128)
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

    player = Player(grid)

    grid.a_star(player.position, (10, 20))

    pprint(grid.path)

    # Game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill the window with red
        window.fill((0, 0, 0))

        # Draw the grid
        grid.draw_grid(window)

        # Draw the player
        player.draw(window)

        # Update the display
        pygame.display.flip()
