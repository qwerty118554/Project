# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Greedy maze solver for all entrance, exit pairs
#
# __author__ = <student name here>
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------------------------


from maze.util import Coordinates
from maze.maze import Maze

from knapsack.knapsack import Knapsack
from itertools import permutations

from typing import List, Dict, Optional


class TaskDSolver:
    def __init__(self, knapsack:Knapsack):
        self.m_solverPath: List[Coordinates] = []
        self.m_cellsExplored = 0 # count of UNIQUE cells visited. i.e. final count should equal len(set(self.m_solverPath))
        self.m_entranceUsed = None
        self.m_exitUsed = None
        self.m_knapsack = knapsack
        self.m_value = 0
        self.m_reward = float('-inf') # initial reward should be terrible

        # you may which to add more parameters here, such as probabilities, etc
        # you may update these parameters using the Maze object in SolveMaze

    def reward(self):
        return self.m_knapsack.optimalValue - self.m_cellsExplored

    def solveMaze(self, maze: Maze, entrance: Coordinates, exit: Coordinates):
        """
        Solution for Task D goes here.

        Be sure to increase self.m_cellsExplored whenever you visit a NEW cell
        Be sure to increase the knapsack_value whenever you find an item and put it in your knapsack.
        You may use the maze object to check if a cell you visit has an item
        maze.m_itemParams can be used to calculate things like predicted reward, etc. But you can only use
        maze.m_items to check if your current cell contains an item (and if so, what is its weight and value)

        Code in this function will be rigorously tested. An honest but bad solution will still gain quite a few marks.
        A cheated solution will gain 0 marks for all of Task D.
        Args:
            maze: maze object
            entrance: initial entrance coord
            exit: exit coord

        Returns: Nothing, but updates variables
        """

        self.m_solverPath = []
        self.m_entranceUsed = entrance
        self.m_exitUsed = exit
        self.m_cellsExplored = len(set(self.m_solverPath))
        self.m_reward = self.reward()