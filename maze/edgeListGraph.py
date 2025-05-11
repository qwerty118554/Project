# ------------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Adjacent list implementation.
#
# __author__ = 'Elham Naghizade'
# __copyright__ = 'Copyright 2025, RMIT University'
# ------------------------------------------------------------------------


from typing import List

from maze.util import Coordinates
from maze.graph import Graph


class EdgeListGraph(Graph):
    

    def __init__(self):
        self.vertices = []
        self.edges = []  # List of tuples (vert1, vert2, wallStatus)
        

  
    def addVertex(self, label:Coordinates):
        if label not in self.vertices:
            self.vertices.append(label)

    def addVertices(self, vertLabels:List[Coordinates]):
        for label in vertLabels:
            self.addVertex(label)


    def addEdge(self, vert1:Coordinates, vert2:Coordinates, addWall:bool = False)->bool:
        
        # Check if both vertices exist in the graph and they are not the same vertex
        if self.hasVertex(vert1) and self.hasVertex(vert2) and vert1 != vert2:
            if vert1.isAdjacent(vert2): # this is not necessarily needed given our maze initialisation
                self.edges.append((vert1, vert2, addWall))
                return True
        return False
      

    def updateWall(self, vert1:Coordinates, vert2:Coordinates, wallStatus:bool)->bool:
        
        if self.hasVertex(vert1) and self.hasVertex(vert2):
            if vert1.isAdjacent(vert2):
                # Iterate through the edge list to find the corresponding edge
                for index, (v1, v2, _) in enumerate(self.edges):
                    # the edge can be in either direction (this is an undirected graph)
                    if (v1 == vert1 and v2 == vert2) or (v1 == vert2 and v2 == vert1):
                        self.edges[index] = (vert1, vert2, wallStatus)
                        return True
        return False


    def removeEdge(self, vert1:Coordinates, vert2:Coordinates)->bool:
        
        if self.hasVertex(vert1) and self.hasVertex(vert2):
            # Iterate through the edge list to find the corresponding edge
            for index, (v1, v2, _) in enumerate(self.edges):
                # the edge can be in either direction
                if (v1 == vert1 and v2 == vert2) or (v1 == vert2 and v2 == vert1):
                    self.edges.pop(index)
                    return True
        return False
        

    def hasVertex(self, label:Coordinates)->bool:
        return label in self.vertices



    def hasEdge(self, vert1:Coordinates, vert2:Coordinates)->bool:
        
        if self.hasVertex(vert1) and self.hasVertex(vert2):
            # Iterate through the edge list to check if the edge exists
            for v1, v2, _ in self.edges:
                if (v1 == vert1 and v2 == vert2) or (v1 == vert2 and v2 == vert1):
                    return True
        return False

    def getWallStatus(self, vert1:Coordinates, vert2:Coordinates)->bool:
        
        if self.hasVertex(vert1) and self.hasVertex(vert2):
            if self.hasEdge(vert1, vert2):
                # Iterate through the edge list to find the edge and return its wall status
                for v1, v2, wall in self.edges:
                    if (v1 == vert1 and v2 == vert2) or (v1 == vert2 and v2 == vert1):
                        return wall
        return False
    

    def neighbours(self, label:Coordinates)->List[Coordinates]:
        
        neighbors = []
        # Iterate through the edge list to find all neighbors of the given vertex
        for v1, v2, _ in self.edges:
            if v1 == label:
                neighbors.append(v2)
            elif v2 == label:
                neighbors.append(v1)
        return neighbors
        