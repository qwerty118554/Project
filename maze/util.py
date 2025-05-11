# -------------------------------------------------
# DON'T CHANGE THIS FILE.
# Utility classes and methods.
#
# __author__ = 'Jeffrey Chan' & 'Elham Naghizade'
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------



class Coordinates:
    """
    Forward declaration.
    """
    def getRow(self)->int:
        pass

    def getCol(self)->int:
        pass


class Coordinates:
    """
    Represent coordinates for maze cells.
    """

    def __init__(self, row:int, col:int, weight:str = None):
        """
        Constructor.
        
        @param row: Row of coordinates.
        @param col: Column of coordinates.
        @param weight: Weight of the coordinates
        """

        self.m_r = row
        self.m_c = col
        
        if weight is not None:
            self.m_weight = self.setWeight(weight)
        else:
            # For boundary cells, no weight is assigned
            self.m_weight = 0  # or some sentinel value



    def getRow(self)->int:
        """
        @returns Row of coordinate.
        """
        return self.m_r
    


    def getCol(self)->int:
        """
        @returns Column of coordinate.
        """
        return self.m_c
    


    def isAdjacent(self, other:Coordinates)->bool:
        """
        Determine if two coordinates are adjacent to each other.
        """
        if (abs(self.m_r - other.getRow()) == 1 and self.m_c == other.getCol()) or\
                (self.m_r == other.getRow() and abs(self.m_c - other.getCol()) == 1): 
            return True
        else:
            return False
        
    def setWeight(self, approach):
        """
        Returns the weight of the cell in the maze based on the specified approach.

        @param approach: The approach for weight calculation (e.g., "random", "checkered").
        @param rng: Range for calculating weight. This can become part of the configuration
        @return: The calculated weight.
        """    
        import random

        rng = 4
        if approach == "random":
            wt = random.randint(1, rng)
            
        elif approach == "checkered":
            wt = ((self.m_c + self.m_r) % rng) +1
        else: 
            wt = 1
        return wt

    def getWeight(self) -> int:
        """
        @returns Weight of the cell.
        """
        return self.m_weight


    def __eq__(self, other:Coordinates):
        """
        Define == operator.

        @param other: Other coordinates that we are comparing with.
        """
        if other != None:
            return self.m_r == other.getRow() and self.m_c == other.getCol()
        else:
            return False



    def __hash__(self):
        """
        Returns hash value of Coordinates.  Needed for being a key in dictionaries.
        """
        return hash(str(self.m_r)+'|'+str(self.m_c))
    
    
    
        
        
    


