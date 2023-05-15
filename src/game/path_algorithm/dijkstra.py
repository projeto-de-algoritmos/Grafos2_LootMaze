class Dijkstra:
    def __init__(self, grid):
        self.grid = grid
        self.spawn = self.grid.spawn
        self.goal = self.grid.goal

        self.open_set = {self.spawn}
        self.came_from = {self.spawn: None}
        self.g_score = {self.spawn: 0}
        self.explored = set()

    def get_neighbors(self, cell):
        # Returns walkable neighbors
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cell[0] + dx, cell[1] + dy
            if (
                0 <= nx < self.grid.width
                and 0 <= ny < self.grid.height
                and self.grid.CELL_TYPE[self.grid.grid[ny][nx]]["walkable"]
            ):
                neighbors.append((nx, ny))
        return neighbors

    def algorithm_tick(self):
        if not self.open_set:
            return None, self.explored  # No path found

        current = min(
            self.open_set, key=lambda cell: self.g_score[cell]
        )  # Here we only consider g_score
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
            tentative_g_score = (
                self.g_score[current]
                + self.grid.CELL_TYPE[self.grid.grid[neighbor[1]][neighbor[0]]]["cost"]
            )
            if (
                neighbor not in self.g_score
                or tentative_g_score < self.g_score[neighbor]
            ):
                self.came_from[neighbor] = current
                self.g_score[neighbor] = tentative_g_score
                if neighbor not in self.open_set:
                    self.open_set.add(neighbor)

        return None, self.explored  # Path not yet found
