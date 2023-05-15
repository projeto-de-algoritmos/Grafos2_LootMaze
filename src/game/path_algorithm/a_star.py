class AStar:
    def __init__(self, grid):
        self.grid = grid
        self.spawn = self.grid.spawn
        self.goal = self.grid.goal
        self.open_set = {grid.spawn}
        self.came_from = {grid.spawn: None}
        self.g_score = {grid.spawn: 0}
        self.f_score = {grid.spawn: self.heuristic(grid.spawn, grid.goal)}
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

    def algorithm_tick(self):
        if not self.open_set:
            return None, self.explored  # No path found

        current = min(self.open_set, key=lambda cell: self.f_score[cell])
        self.explored.add(current)  # add current cell to explored set

        if current == self.goal:
            path = []
            while current is not None and current != self.spawn:
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

