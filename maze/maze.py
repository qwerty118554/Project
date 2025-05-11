# -------------------------------------------------
# DON'T CHANGE THIS FILE.
# Base class for maze implementations. 
#
# __author__ = 'Elham Naghizade' and 'Edward Small'
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------

from typing import List
import random


from maze.util import Coordinates
from maze.edgeListGraph import EdgeListGraph


class Maze:
    """
    Base (abstract) class for mazes.
    """


    def __init__(self, rowNum:int, colNum:int, itemParams:list):
        """
        Constructor.

        @param rowNum: number of rows in the maze.
        @param colNum: number of columns in the maze
        """
        self.m_rowNum = rowNum
        self.m_colNum = colNum

        # entrances and exits
        self.m_entrance = list()
        self.m_exit = list()
        self.m_graph = EdgeListGraph() 

        # Store coordinates for reuse
        self.m_cells = {}
        self.initCells()

        # store items as {cell: [weight, value]}
        self.m_itemParams = itemParams
        self.m_items = {}
        self.initItems()



    def initCells(self,  addWallFlag:bool = True, wt: str = "unWeighted" ):
        """
        Initialises the cells in the maze. 
        Override to customise behaviour.

        @param addWallFlag: Whether we should also add the walls between cells.  Default is True.
        """
        

        # add the vertices and edges to the graph
        # Add vertices and initialize Coordinates with weights
        for r in range(self.m_rowNum):
            for c in range(self.m_colNum):
                coord = Coordinates(r, c, wt)
                self.m_cells[(r, c)] = coord  
                self.m_graph.addVertex(coord)


        # add boundary vertices and store them in cells; the weights are assigned to 0
        
        for c in range(self.m_colNum):
            # Top and bottom boundaries (row -1 and row m_rowNum)
            top_boundary = Coordinates(-1, c)  
            bottom_boundary = Coordinates(self.m_rowNum, c)  
            self.m_cells[(-1, c)] = top_boundary
            self.m_cells[(self.m_rowNum, c)] = bottom_boundary
            self.m_graph.addVertices([top_boundary, bottom_boundary])

        for r in range(self.m_rowNum):
            # Left and right boundaries (col -1 and col m_colNum)
            left_boundary = Coordinates(r, -1)  
            right_boundary = Coordinates(r, self.m_colNum)  
            self.m_cells[(r, -1)] = left_boundary
            self.m_cells[(r, self.m_colNum)] = right_boundary
            self.m_graph.addVertices([left_boundary, right_boundary])

        # add adjacenies/edges to the graph
        # Add adjacencies/edges to the graph using the stored cells
        for row in range(0, self.m_rowNum):
            for col in range(-1, self.m_colNum):
                cell1 = self.m_cells[(row, col)]
                cell2 = self.m_cells[(row, col + 1)]
                self.m_graph.addEdge(cell1, cell2, addWallFlag)
        
        # Scan columns now
        for col in range(0, self.m_colNum):
            for row in range(-1, self.m_rowNum):
                # Use pre-initialized cells with weights
                cell1 = self.m_cells[(row, col)]
                cell2 = self.m_cells[(row + 1, col)]
                self.m_graph.addEdge(cell1, cell2, addWallFlag)
        

    def initItems(self):
        """
        Adds items to the maze based on item parameter inputs
        """
        num_items = self.m_itemParams[0]
        max_weight = self.m_itemParams[1]
        max_value = self.m_itemParams[2]

        # generate a list of possible cells. Remove from this list when we choose this cell.
        remaining_cells = [(i, j) for i in range(0, self.m_rowNum) for j in range(0, self.m_colNum)]

        for i in range(num_items):
            if not remaining_cells:
                raise Exception('Number of items exceeds cells')

            weight = random.randint(1, max_weight)
            value = random.randint(1, max_value)
            loc = random.choice(remaining_cells)
            remaining_cells.remove(loc)

            self.m_items[loc] = [weight, value]




    def addWall(self, cell1:Coordinates, cell2:Coordinates)->bool:
        """
        Adds a wall between cells cell1 and cell2.
        cell1 and cell2 should be adjacent.
        Override to customise behaviour.

        @param cell1: Coordinates of cell1.
        @param cell2: Coordinates of cell2.

        @return True if successfully added a wall, otherwise False in all other cases.
        """
        # checks if coordinates are valid
        assert(self.checkCoordinates(cell1) and self.checkCoordinates(cell2))

        # only can add wall if adjacent
        if self.m_graph.hasEdge(cell1, cell2):
            self.m_graph.updateWall(cell1, cell2, True)
            return True
        
        # in all other cases, we return False
        return False
    

    def removeWall(self, cell1:Coordinates, cell2:Coordinates)->bool:
        """
        Removes a wall between cells cell1 and cell2.
        cell1 and cell2 should be adjacent.
        Override to customise behaviour.

        @param cell1: Coordinates of cell1.
        @param cell2: Coordinates of cell2.

        @return True if successfully removed a wall, otherwise False in all other cases.
        """

        # checks if coordinates are valid
        assert(self.checkCoordinates(cell1) and self.checkCoordinates(cell2))

        # only can remove wall if adjacent
        if self.m_graph.hasEdge(cell1, cell2):
            self.m_graph.updateWall(cell1, cell2, False)
            return True
        
        # in all other cases, we return False
        return False
    

    def allWalls(self):
        """
        Add walls between all cells in the maze.
        """

        # add walls to the left and bottom of a 2d traversal of cells
        for r in range(-1,self.m_rowNum):
            for c in range(-1,self.m_colNum):
                cell1 = self.m_cells[(r, c)]
                cell2 = self.m_cells[(r + 1, c)]
                cell3 = self.m_cells[(r, c+1)]

                self.addWall(cell1, cell2)
                self.addWall(cell1, cell3)
                
        # add the wall along the right maze boundary, and top maze boundary
        for r in range(0,self.m_rowNum):
            cell1 = self.m_cells[(r, self.m_colNum-1)] 
            cell2 = self.m_cells[(r, self.m_colNum)] 
            self.addWall(cell1, cell2)

        for c in range(0,self.m_colNum):
            cell1 = self.m_cells[(self.m_rowNum-1, c)] 
            cell2 = self.m_cells[(self.m_rowNum, c)] 
            self.addWall(cell1, cell2)

    def hasWall(self, cell1:Coordinates, cell2:Coordinates)->bool:
        """
        Checks if there is a wall between cell1 and cell2.
        Override if need to customise behaviour

        @returns True, if there is a wall.

        """
        return self.m_graph.getWallStatus(cell1, cell2)
    
    def hasEdge(self, cell1:Coordinates, cell2:Coordinates)->bool:
        """
        Checks if there is an edge between cell1 and cell2.

        @returns True, if there is an edge.

        """
        return self.m_graph.hasEdge(cell1, cell2)

    def neighbours(self, cell:Coordinates)->List[Coordinates]:
        """
        Return neighbours of cell.
        """
        return self.m_graph.neighbours(cell)

    def edgeWeight(self, cell1:Coordinates, cell2:Coordinates)->int:
        """
        Returns the weight of the edge between two cells in the maze, 
        calculated as the absolute difference in their weights.

        If there is no edge between the two cells, returns -1.

        @param cell1: The first cell (vertex) in the graph.
        @param cell2: The second cell (vertex) in the graph.
        @return: The absolute difference in weight between the two cells if an edge exists, or -1 otherwise.
        """
        
        if self.m_graph.hasEdge(cell1, cell2):
            return abs(cell1.getWeight()- cell2.getWeight())
        else:
            return -1
        
    def getVetrices(self)->List[Coordinates]:
        """
        Retrieves all vertices (cells) in the maze graph.

        @return: A list of all the vertex coordinates in the maze graph.
        """
        return self.m_graph.vertices  

    def getEdges(self)->List[Coordinates]:
        """
        Retrieves all edges in the maze graph.

        @return: A list of tuples representing edges.
        """
        return self.m_graph.edges  
    
    def getCoords(self)->List[Coordinates]:
        """
        Retrieves all coordinates (including their weight) from the maze.

        @return: A list of coordinates representing all cells in the maze.
        """
        return list(self.m_cells.values())

    

    def addEntrance(self, cell: Coordinates)->bool:
        """
        Adds an entrance to the maze.  A maze can have more than one entrance, so this method can be called more than once.

        @return True if successfully added an entrance, otherwise False.
        """

        # check if cell of entrance is valid
        assert(self.checkCoordinates(cell))

        # check if cell of the entrance is on the boundary of the maze, as an entrance should only be added along the boundary
        if (cell.getRow() == -1 and cell.getCol() >= 0 and cell.getCol() < self.m_colNum) \
            or (cell.getRow() == self.m_rowNum and cell.getCol() >= 0 and cell.getCol() < self.m_colNum) \
            or (cell.getCol() == -1 and cell.getRow() >= 0 and cell.getRow() < self.m_rowNum) \
            or (cell.getCol() == self.m_colNum and cell.getRow() >= 0 and cell.getRow() < self.m_rowNum):
            
            self.m_entrance.append(cell)

            # entrance is at bottom, need to remove wall in "up" direction
            if cell.getRow() == -1:
                uCell = self.m_cells[( 0, cell.getCol())]
                self.removeWall(cell, uCell)
			# entrance is at top, need to remove wall in "down" direction
            elif cell.getRow() == self.m_rowNum:
                dCell = self.m_cells[( self.m_rowNum-1, cell.getCol())]
                self.removeWall(cell, dCell)
			# entrace is to the left, need to remove wall in "right" direction
            elif cell.getCol() == -1:
                lCell = self.m_cells[(cell.getRow(), 0)]
                self.removeWall(cell, lCell)
			# entrance is to the right, need to remove wall in "left" direction
            elif cell.getCol() == self.m_colNum:
                rCell = self.m_cells[(cell.getRow(), self.m_colNum-1)]
                self.removeWall(cell,rCell)

            return True
        else:
            # not on the boundary
            return False



    def addExit(self, cell: Coordinates)->bool:
        """
        Adds an exit to the maze.  A maze can have more than one exit, so this method can be called more than once.

        @return True if successfully added an exit, otherwise False.
        """

        # check if cell of exit is valid
        assert(self.checkCoordinates(cell))

        # check if cel of exitl is on the boundary of the maze, as an exit should only be added along the boundary
        if (cell.getRow() == -1 and cell.getCol() >= 0 and cell.getCol() < self.m_colNum) \
            or (cell.getRow() == self.m_rowNum and cell.getCol() >= 0 and cell.getCol() < self.m_colNum) \
            or (cell.getCol() == -1 and cell.getRow() >= 0 and cell.getRow() < self.m_rowNum) \
            or (cell.getCol() == self.m_colNum and cell.getRow() >= 0 and cell.getRow() < self.m_rowNum):
            
            self.m_exit.append(cell)

            # entrance is at bottom, need to remove wall in "up" direction
            if cell.getRow() == -1:
                uCell = self.m_cells[( 0, cell.getCol())]
                self.removeWall(cell, uCell)
			# entrance is at top, need to remove wall in "down" direction
            elif cell.getRow() == self.m_rowNum:
                dCell = self.m_cells[( self.m_rowNum-1, cell.getCol())]
                self.removeWall(cell, dCell)
			# entrace is to the left, need to remove wall in "right" direction
            elif cell.getCol() == -1:
                lCell = self.m_cells[(cell.getRow(), 0)]
                self.removeWall(cell, lCell)
			# entrance is to the right, need to remove wall in "left" direction
            elif cell.getCol() == self.m_colNum:
                rCell = self.m_cells[(cell.getRow(), self.m_colNum-1)]
                self.removeWall(cell, rCell)

            return True
        else:
            # not on boundary
            return False
        
    
        

    def getEntrances(self)->List[Coordinates]:
        """
        @returns list of entrances that the maze has.
        """
        return self.m_entrance
    


    def getExits(self)->List[Coordinates]:
        """
        @returns list of exits that the maze has.
        """
        return self.m_exit



    def rowNum(self)->int:
        """
        @returns The number of rows the maze has.
        """

        return self.m_rowNum



    def colNum(self)->int:
        """
        @return The number of columns the maze has.
        """

        return self.m_colNum

    def checkCoordinates(self, coord:Coordinates)->bool:
        """
        Checks if the coordinates is a valid one.
        
        @param coord: Cell/coordinate to check if it is a valid one.
        
        @returns True if coord/cell is valid, otherwise False.
        """

        return coord.getRow() >= -1 and coord.getRow() <= self.m_rowNum and coord.getCol() >= -1 and coord.getCol() <= self.m_colNum

