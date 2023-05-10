class DFS:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal

        self.stack = [start]  # Use a stack instead of a set for DFS
        self.came_from = {start: None}
        self.explored = set()

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
        if not self.stack:
            return None, self.explored  # No path found

        current = self.stack.pop()  # Take the last cell from the stack
        self.explored.add(current)  # Add current cell to explored set

        if current == self.goal:
            path = []
            while current is not None:
                path.append(current)
                current = self.came_from[current]
            path.reverse()
            return path, self.explored

        for neighbor in self.get_neighbors(current):
            if neighbor not in self.explored and neighbor not in self.stack:
                self.stack.append(neighbor)  # Add neighbors to the stack
                self.came_from[neighbor] = current

        return None, self.explored  # Path not yet found
