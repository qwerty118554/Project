# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# This is the entry point to run the program.
# Refer to usage() for exact format of input expected to the program.
#
# __author__ = 'Jeffrey Chan', 'Elham Naghizade', 'Edward Small' & 'Imesh Ekanayake'
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------------------------


import sys
import time
import json
import random
from typing import List

from maze.util import Coordinates
from maze.maze import Maze

from knapsack.knapsack import Knapsack

from reader.mazeReader import MazeReader
from generator.mazeGenerator import MazeGenerator
from solver.mazeSolver import MazeSolver

# this checks if Visualizer has been imported properly.
# if not, likely missing some packages, e.g., matplotlib.
# in that case, regardless of visualisation flag, we should set the canVisualise flag to False which will not call the visualisation part.
canVisualise = True
try:
    from maze.maze_viz import Visualizer
except:
    Visualizer = None
    canVisualise = False


def usage():
    """
	Print help/usage message.
	"""
    # On Teaching servers, use 'python3'
    # On Windows, you may need to use 'python' instead of 'python3' to get this to work
    print('python3 mazeRunner.py', '<configuration file>')
    sys.exit(1)


def findItemsAndCalculatePath(knapsack: Knapsack, solver: MazeSolver, maze: Maze,
                              entrance: Coordinates, exit: Coordinates, csvFilename: str):
    """
	Finds the optimal items using <knapsack strategy> and calculates the path to enter the maze,
	pick up the items, and leave the maze.
	"""
    knapsack.solveKnapsack(maze, csvFilename)
    solver.solveMaze(maze, entrance, exit)


#
# Main function, when the python script is executed, we execute this.
#
if __name__ == '__main__':
    # Fetch the command line arguments
    args = sys.argv

    if len(args) != 2:
        print('Incorrect number of arguments.')
        usage()

    # open configuration file
    fileName: str = args[1]
    with open(fileName, "r") as configFile:
        # use json parser
        configDict = json.load(configFile)

        # Assign to variables storing various parameters.

        # row, col, exit and entrance of the maze
        rowNum: int = configDict['rowNum']
        colNum: int = configDict['colNum']
        entrances: List[List[int]] = configDict['entrances']
        exits: List[List[int]] = configDict['exits']
        randWall: int = configDict['randomWallRemovalPercent']

        if randWall > 80 or randWall < 0:
            raise Exception('We cannot remove this percentage of walls.')

        # solver approach to use
        pathFinderApproach: str = configDict['pathFinder']
        solverEntIndex: int = configDict['solverEntranceIndex']
        multiPath = False

        # whether to create the maze from a text file rather than calling
        # a maze generator.

        if 'mazeFromFile' not in configDict.keys():
            print('Warning! This version of mazeTester has been updated\
		  			to support reading mazes from files. Please check your config file.')
            usage()

        fileMaze: bool = configDict['mazeFromFile']

        # whether to visualise the generated maze and solving solution or not
        bVisualise: bool = configDict['visualise']
        # Optional: Filename to store visualisation output
        outFilename: str = None
        csvFilename: str = configDict['fileOutput']
        if 'fileOutput' in configDict.keys():
            outFilename = configDict['fileOutput'] + '.png'
        # Optional: Seed to pass to random generator (used for validation)
        randSeed: int = None
        if 'randSeed' in configDict.keys():
            randSeed = configDict['randSeed']

        # initialise the random seed generator
        if randSeed != None:
            random.seed(randSeed)
        # Include item parameters
        itemParams = [None] * 3
        itemParams[0] = configDict['numItems']
        itemParams[1] = configDict['maxWeight']
        itemParams[2] = configDict['maxValue']

        # initialise knapsack config
        capacity = configDict['knapsackCapacity']
        knapsackSolver = configDict['knapsackSolver']

        # Initialise maze object
        maze: Maze = Maze(rowNum, colNum, itemParams)

        # initialise knapsack object
        knapsack: Knapsack = Knapsack(capacity, knapsackSolver)

        # add the entrances and exits
        for [r, c] in entrances:
            maze.addEntrance(Coordinates(r, c))
        for [r, c] in exits:
            maze.addExit(Coordinates(r, c))

        # reading the maze information from the file
        if fileMaze:
            mazeFileName = configDict['mazeFileName']
            reader = MazeReader(mazeFileName)
            reader.readMaze(maze)
            isMazeGenerated = reader.isMazeGenerated()

        # Generate maze
        else:
            generator = MazeGenerator(randWall)
            # timer for generation
            startGenTime: float = time.perf_counter()
            generator.generateMaze(maze)
            isMazeGenerated = generator.isMazeGenerated()
            # stop timer
            endGenTime: float = time.perf_counter()
            print(f'Generation took {endGenTime - startGenTime:0.4f} seconds')

        mazeEntrances: List[Coordinates] = maze.getEntrances()
        mazeExits: List[Coordinates] = maze.getExits()

        # check if solver entrance index is within bounds
        if solverEntIndex != None and (solverEntIndex < 0 or solverEntIndex >= len(mazeEntrances)):
            print("Specified index of entrance that solver starts is out of bounds, {}".format(solverEntIndex))
            usage()

        if isMazeGenerated:
            entrance = mazeEntrances[solverEntIndex]
            exit = mazeExits[solverEntIndex]
            solver = MazeSolver(pathFinderApproach, knapsack)
            findItemsAndCalculatePath(knapsack, solver, maze, entrance, exit, csvFilename)
        else:
            print("Maze has not been generated or read properly from the file, hence solver wasn't called.")

        print("getting to visualisation!", canVisualise)
        # Display maze.
        if bVisualise and canVisualise and isMazeGenerated:
            cellSize = 1
            visualiser = Visualizer(maze, solver, multiPath, cellSize, knapsack)
            if outFilename:
                visualiser.show_maze(outFilename)
            else:
                visualiser.show_maze()

        # --------------------------------------------------------------------
        # New code added to save the collected knapsack items into a file.
        # These items are stored in knapsack.optimalCells after findItemsAndCalculatePath() runs.
        # Both solvers now save the items in CSV format with the same structure.
        # --------------------------------------------------------------------
        if hasattr(knapsack, 'optimalCells') and knapsack.optimalCells is not None:
            import csv
            if knapsack.knapsackSolver == "recur":
                output_filename = "Knapsack_recur_items.csv"
            elif knapsack.knapsackSolver == "dynamic":
                output_filename = "Knapsack_dynamic_items.csv"
            with open(output_filename, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Item"])
                for item in knapsack.optimalCells:
                    writer.writerow([item])
                writer.writerow([knapsack.optimalValue])
            print(f"\nKnapsack items saved in {output_filename}")

