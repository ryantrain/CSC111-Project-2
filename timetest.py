from timeit import timeit

from typing import Type

import player
from maze_generation import generate_mazes, number_maze
from graph import Graph
from player import Player
from random_player import RandomPlayer
from compass_algorithm_player import CompassPlayer
from dfs_player import DFSPlayer
from bfs_player import BFSPlayer
from handonwall_player import HandOnWallPlayer
from deadend_filling_player import DeadEndFillingPlayer


import sys
sys.setrecursionlimit(50000)

def run_game(player: Type[Player], start: int, end: int, graph: Graph) -> list:
    """
    Run one instance of the game of the given Player.
    Returns a list of vertex IDs representing the path taken by the player.
    """
    return player(graph).run_game(start, end)


dataset = generate_mazes()

ALGORITHMS = {
    HandOnWallPlayer: 0.0,
    CompassPlayer: 0.0,
    RandomPlayer: 0.0,
    BFSPlayer: 0.0,
    DFSPlayer: 0.0,
    DeadEndFillingPlayer: 0.0
}

steps = [0] * 6

for i in range(5):
    for j in range(20):
        maze = dataset[i*20 + j]
        numbered_maze = number_maze(maze)
        start = int(maze.start_pos[0] * 10 + maze.start_pos[1] + 1)
        end = int(maze.end_pos[0] * 10 + maze.end_pos[1] + 1)

        for x, algo in enumerate(ALGORITHMS.keys()):
            path = run_game(algo, start, end, numbered_maze)
            elapsed_time = timeit(
                lambda algo=algo: run_game(algo, start, end, numbered_maze),
                number=100
            ) * 10

            ALGORITHMS[algo] += elapsed_time
            steps[x] += len(path)

    for x, algo in enumerate(ALGORITHMS.keys()):
        print("Time taken (ms): ", algo, ALGORITHMS[algo]/20.0)
        print("Steps: " + str(steps[x]/20.0))
        ALGORITHMS[algo] = 0
        steps[x] = 0
    print("-"*50)
