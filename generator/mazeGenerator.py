# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Base class for maze generator.
#
# __author__ = 'Jeffrey Chan' & 'Elham Naghizade' & 'Edward Small'
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------------------------


from maze.maze import Maze


from generator.recurBackGenerator import RecurBackMazeGenerator

class MazeGenerator:
	"""
	Base class for a maze generator.
	"""
	def __init__(self, randWall:int = 0):
		# This is used to indicate to program whether a maze been generated, or nothing has been done.
		# Need to set this to true once a maze is generated!
		self.m_mazeGenerated: bool = False
		self.m_randWall = randWall
		self.m_generator = RecurBackMazeGenerator()


	def generateMaze(self, maze:Maze):
		"""
	    Generates a maze.  Will update the passed maze.

		@param maze Maze which we update on to generate a maze. 
		"""
		
		self.m_generator.generateMaze(maze, self.m_randWall)
		self.m_mazeGenerated = True


	def isMazeGenerated(self):
		return self.m_mazeGenerated			

		