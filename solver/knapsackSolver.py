# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Given items to collect, finds the shortest path to collect these
# items and leave the maze
#
# __author__ = 'Edward Small'
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------------------------


from maze.util import Coordinates
from maze.maze import Maze

from knapsack.knapsack import Knapsack
from itertools import permutations

from typing import List, Dict, Optional


class KnapsackSolver:
    def __init__(self, knapsack: Knapsack):
        self.m_solverPath: List[Coordinates] = []
        self.m_cellsExplored = 0
        self.m_entranceUsed = None
        self.m_exitUsed = None
        self.m_knapsack = knapsack
        self.m_value = self.m_knapsack.optimalValue
        self.m_reward = 0

    def reward(self):
        return self.m_knapsack.optimalValue - self.m_cellsExplored

    def bfs(self, maze: Maze, start: Coordinates, goal: Coordinates) -> List[Coordinates]:
        """
        Finds the shortest path between start and goal coordinate using breadth first search

        @param maze: the maze we are working on.
        @param start: the starting coordinate.
        @param goal: the goal coordinate.

        @return A list containing coordinates to go from the start to the goal.
        """

        if start == goal:
            return [start]

        visited = set()
        queue = [start]
        predecessors: Dict[Coordinates, Optional[Coordinates]] = {start: None}

        while queue:
            curr = queue.pop(0)

            if curr == goal:
                # Reconstruct path from goal to start
                path = []
                while curr is not None:
                    path.append(curr)
                    curr = predecessors[curr]
                return list(reversed(path))

            visited.add(curr)

            for neighbor in maze.neighbours(curr):
                if neighbor not in visited and neighbor not in predecessors:
                    if not maze.hasWall(curr, neighbor):
                        queue.append(neighbor)
                        predecessors[neighbor] = curr

        # If goal is unreachable (shouldn’t happen in a fully connected maze)
        return []

    def solveMaze(self, maze: Maze, entrance: Coordinates, exit: Coordinates):
        """
        Finds the shortest path that goes from entrance, through knapsack cells, and to the exit.

        @param maze: the maze we are working on.
        @param entrance: the starting coordinate.
        @param exit: the end coordinate.
        """

        # get all points of interest:
        points = [entrance] + list(self.m_knapsack.optimalCells) + [exit]
        # make sure everything is a coordinate type

        for i in range(1, len(points) - 1):
            points[i] = Coordinates(points[i][0], points[i][1])

        # find minimum paths between all points
        distances = {}  # distances between each pair of points
        paths = {}  # To store the actual paths between points

        for i in range(len(points)):
            for j in range(len(points)):
                if j != i:
                    path = self.bfs(maze, points[i], points[j])
                    distances[(points[i], points[j])] = len(path) - 1  # Store the distance (edge count)
                    paths[(points[i], points[j])] = path  # Store the actual path

        knapsack_cells = points[1:-1]

        # Try all permutations of the knapsack cells to find the shortest route
        # where multiple solutions exist, choose the one that minimises unique cell visits
        min_path = None
        min_distance = float('inf')
        min_explored = float('inf')

        for perm in permutations(knapsack_cells):
            # Create the path visiting entrance, then knapsack cells in perm order, then exit
            full_path = [entrance] + list(perm) + [exit]
            total_distance = 0
            full_route = []  # This will hold the full path

            # For each pair of consecutive points, get the path
            for i in range(len(full_path) - 1):
                total_distance += distances[(full_path[i], full_path[i + 1])]
                full_route.extend(
                    paths[(full_path[i], full_path[i + 1])][1:])  # Exclude first point to avoid duplicates

            # get unique cells in the path and check how many there are
            explored = len(set(full_route))
            # Check if this is the shortest route and minimises unique cell visits
            if total_distance <= min_distance:
                if explored < min_explored:
                    min_distance = total_distance
                    min_explored = explored
                    min_path = full_route

        self.m_solverPath = [entrance] + min_path
        self.m_entranceUsed = entrance
        self.m_exitUsed = exit
        self.m_cellsExplored = len(set(self.m_solverPath))
        self.m_reward = self.reward()
