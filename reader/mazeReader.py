# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Base class for maze reader.
#
# __author__ = 'Elham Naghizade'
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------------------------


from maze.maze import Maze
from maze.util import Coordinates



class MazeReader():
    """
    Base class for reading and updating a maze from a file.
    """

    def __init__(self, mazeFname):
        # Flag to indicate whether the maze has been read and updated successfully.
        self.m_mazeGenerated: bool = False
        self.mazeFname = mazeFname


    def isMazeGenerated(self) -> bool:
        """
        Returns whether the maze has been successfully generated and updated from the file.
        """
        return self.m_mazeGenerated

    def readMaze(self, maze):
        """
        Reads the maze file, updates the cell weights and walls, and sets the m_mazeGenerated flag.
        """
        try:
            weights = self.loadWeights(self.mazeFname)
            self.update_cell_weights(maze, weights)
            self.update_cell_walls(maze, self.mazeFname)
            self.m_mazeGenerated = True
        except Exception as e:
            print(f"Error reading maze file: {e}")
            self.m_mazeGenerated = False

    def loadWeights(self, fname) -> dict:
        """
        Reads the weights from a file and returns a dictionary where keys are (row, column) tuples
        and values are the corresponding cell weights.
        """
        m_weights = {}
        with open(fname, 'r') as file:
            for i, line in enumerate(file):
                lineInfo = list(map(int, line.strip().split()))

                # Odd lines are maze rows, where odd values are cell weights
                if i % 2 == 0:
                    row = i // 2
                    for col in range(0, len(lineInfo), 2):
                        m_weights[(row, col // 2)] = lineInfo[col]                      
        return m_weights

    def update_cell_weights(self, maze, weights: dict):
        """
        Updates the weights of all cells in the maze using the provided weights dictionary.
        
        :param weights: A dictionary containing the weights keyed by (row, column) tuples.
        """
        for vertex in maze.getVetrices():  
            row = vertex.getRow()
            col = vertex.getCol()
            if (row, col) in weights:
                vertex.m_weight = weights[(row, col)]  # Directly setting the weight of the Coordinate object
        
        print("Cell weights updated.")

    def update_cell_walls(self, maze, fname):
        """
        Updates the walls of the maze based on the file input. 
        """
        with open(fname, 'r') as file:
            for i, line in enumerate(file):
                lineInfo = list(map(int, line.strip().split()))
                
                row = i // 2
                # Odd lines represent wall statuses for vertical walls
                if i % 2 == 0:
                    walls = [lineInfo[w] for w in range(1, len(lineInfo), 2)]
                    # Update the walls between cells
                    for col in range(len(walls)):
                        if walls[col] == 0:
                            maze.removeWall(Coordinates(row, col), Coordinates(row, col + 1))

                # Even lines represent horizontal walls
                else:
                    walls = lineInfo
                    for col in range(len(walls)):
                        if walls[col] == 0:
                            maze.removeWall(Coordinates(row, col), Coordinates(row + 1, col))
        
        print("Cell walls updated.")



	