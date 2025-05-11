# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Abstract class for a maze solver.  Provides common variables and method interface for maze solvers.
#
# __author__ = 'Jeffrey Chan' & 'Elham Naghizade' & 'Edward Small'
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------------------------


from maze.maze import Maze
from maze.util import Coordinates
from knapsack.knapsack import Knapsack
from typing import List

from solver.knapsackSolver import KnapsackSolver
from solver.taskDSolver import TaskDSolver



class MazeSolver:

    def __init__(self, solverName:str, knapsack:Knapsack = None):
        
        # self.m_solved: true if the solver has found the exit (maze "solved")
        self.m_solved = False
        if solverName == 'TaskC':
            self.m_solver = KnapsackSolver(knapsack)
        elif solverName == 'TaskD':
            self.m_solver = TaskDSolver(knapsack)


    def solveMaze(self, maze: Maze, entrance: Coordinates, exit: Coordinates = None):
        """
        Solves the given maze starting from the entrance using the solver object.
        Once the solver completes the solution, the maze is marked as solved.
        @param maze: The maze to be solved.
        @param entrance: The entrance coordinates where the solving process begins.
        """

        if exit == None:
            self.m_solver.solveMaze(maze, entrance)
        else:
            self.m_solver.solveMaze(maze, entrance, exit)
        self.m_solved = True
        

    def isSolved(self)->bool:
        """
        Use after solveMaze(maze), to check whether the maze is solved.
	    @return True if solved. Otherwise false.
        """
        return self.m_solved


    def cellsExplored(self)->int:
        """
        Use after solveMaze(maze), counting the number of cells explored in solving process.
	    @return The number of cells explored.
	    It is not required to be accurate and no marks are given (or lost) on it. 
        """
        return self.m_solver.cellsExplored


    
    def getEntranceUsed(self)->Coordinates:
        """
        @return Return the entrance used in the solution.  Should only be called after a solution is found.
        """
        return self.m_solver.m_entranceUsed



    def getExitUsed(self)->Coordinates:
        """
        @return Return the exit used in the solution.  Should only be called after a solution is found.
        """
        return self.m_solver.m_exitUsed 

    def getSolverPath(self)->List[Coordinates]:
        """
        Returns the list of Coordinates representing the path 
        determined by the solver from the entrance to the exit of the maze.

        @return: A list of Coordinates from entrance to exit, 
             in the order of traversal.
        """
        return self.m_solver.m_solverPath    
	
