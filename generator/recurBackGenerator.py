# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Recursive backtracking maze generator with random wall removal.
#
# __author__ = 'Jeffrey Chan' & 'Elham Naghizade' & 'Edward Small'
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------------------------

from random import choice
from collections import deque

from maze.maze import Maze
from maze.util import Coordinates



class RecurBackMazeGenerator():
	"""
	Recursive backtracking maze generator.
	Overrides genrateMaze of parent class.
	"""

	def generateMaze(self, maze: Maze, randWall: int):

		# Select a random starting cell from the initialized maze cells
		
		startCoord: Coordinates = choice(maze.getCoords())
		while startCoord.getWeight() == 0: # the random cell is a boundary cell
			startCoord = choice(maze.getCoords())


		# run recursive backtracking/DFS from starting cell
		stack : deque = deque()
		stack.append(startCoord)
		currCell : Coordinates = startCoord 
		visited : set[Coordinates] = set([startCoord])

		totalCells = maze.rowNum() * maze.colNum()
		

		while len(visited) < totalCells:
			# find all neighbours of current cell
			neighbours : list[Coordinates] = maze.neighbours(currCell)

			# filter to ones that haven't been visited and within boundary
			nonVisitedNeighs : list[Coordinates] = [neigh for neigh in neighbours if neigh not in visited and neigh.getRow() >= 0 and neigh.getRow() < maze.rowNum() and neigh.getCol() >= 0 and neigh.getCol() < maze.colNum()]
			
			# see if any unvisited neighbours
			if len(nonVisitedNeighs) > 0:

				neigh = choice(nonVisitedNeighs)

				# we move there and knock down wall
				maze.removeWall(currCell, neigh)

				# add to stack
				stack.append(neigh)

				# updated visited
				visited.add(neigh)

				# update currCell
				currCell = neigh
			else:
				# backtrack
				currCell = stack.pop()

		num_cells = len(maze.m_cells)
		cells = list(maze.m_cells)
		numWallsToRemove = int((randWall / 100.0) * num_cells) * 4
		cell_counter = {}

		while numWallsToRemove > 0 and len(cells) > 0:
			cell = choice(cells)
			if cell not in cell_counter:
				cell_counter[cell] = 1
			else:
				cell_counter[cell] = cell_counter[cell] + 1

			if cell_counter[cell] == 4:
				cells.remove(cell)

			cell = maze.m_cells[cell]
			neighbours = maze.neighbours(cell)

			if not neighbours:
				continue  # skip if no neighbors

			neigh = choice(neighbours)


			if (0 <= cell.getRow() < maze.rowNum() and 0 <= cell.getCol() < maze.colNum()):
				if (0 <= neigh.getRow() < maze.rowNum() and 0 <= neigh.getCol() < maze.colNum()):
					if maze.hasWall(cell, neigh):
						maze.removeWall(cell, neigh)

			numWallsToRemove = numWallsToRemove - 1

		
