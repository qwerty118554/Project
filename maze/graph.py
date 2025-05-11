# -------------------------------------------------
# DON'T CHANGE THIS FILE.
# Base class for graph implementations. 
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------


from typing import List

from maze.util import Coordinates



class Graph:
    """
    Base class for a graph.  Defines the interface.
    """
    
    def addVertex(self, label:Coordinates):
        """
        Adds a vertex to the graph.

        @param label Label of the added vertex (which is a Coordinate),
        """
        pass



    def addVertices(self, vertLabels:List[Coordinates]):
        """
        Adds a list of vertices to the graph.

        @param vertLabels List of labels of the added vertices,
        """
        pass



    def addEdge(self, vert1:Coordinates, vert2:Coordinates, addWall:bool = False)->bool:
        """
        Adds an edge to the graph.  An edge is defined by the two vertex labels, which are Coordinates.

        @param vert1: Label of source vertex of added edge.
        @param vert2: Label of target vertex of added edge.
        @param addWall: Whether to add wall as well.  Default is False.

        @returns True if edge is successfully added, otherwise False.
        """
        pass



    def updateWall(self, vert1:Coordinates, vert2:Coordinates, wallStatus:bool)->bool:
        """
        Sets edge weight/bool.  Edge must exist for the operation to succeed.

        @param vert1: Label of source vertex of edge.
        @param vert2: Label of target vertex of edge.
        @param wallStatus: Whether to set wall or not.  True to set/add wall.

        @returns True if edge weight/bool is successfully set, otherwise False.
        """
        pass  



    def removeEdge(self, vert1:Coordinates, vert2:Coordinates)->bool:
        """
        Removes edge.  Edge must exist for the operation to succeed.

        @param vert1: Label of source vertex of removed edge.
        @param vert2: Label of target vertex of removed edge.

        @returns True if edge is successfully removed, otherwise False.
        """
        pass



    def hasVertex(self, label:Coordinates)->bool:
        """
        Checks if label is a vertex in the graph.  

        @param label: Label/Coordinate to check.

        @returns True if vertex exists in graph, otherwise False.
        """
        pass



    def hasEdge(self, vert1:Coordinates, vert2:Coordinates)->bool:
        """
        Checks if label is a vertex in the graph.  

        @param vert1: Label of source vertex to check.
        @param vert2: Label of target vertex to check.

        @returns True if edge exists in graph, otherwise False.
        """
        pass



    def getWallStatus(self, vert1:Coordinates, vert2:Coordinates)->bool:
        """
        Gets the edge bool/weight.  

        @param vert1: Label of source vertex of edge to retrieve.
        @param vert2: Label of target vertex of edge to retrieve.

        @returns True if edge weight was retrieved, otherwise False.
        """
        pass



    def neighbours(self, label:Coordinates)->List[Coordinates]:
        """
        Retrieves all the neighbours of vertex/label.

        @param label: Label of vertex to obtain neighbours.
        
        @returns List of neighbouring vertices.  Returns empty list if no neighbours.
        """
        pass






