"""Maze Generation and Graph Conversion.

Main module for generating mazes using the maze-datasets GitHub repository
and converting them into graph objects for use in maze-solving algorithms.

Copyright (c) 2026 [Ryan Tran, Jenny Bian, Raymond Wu, Soltan Isgandar]. All rights reserved.
"""

import muutils.json_serialize.util as u

from graph import Graph

u._FORMAT_KEY = "__format__"
import sys

sys.modules['muutils.json_serialize.util']._FORMAT_KEY = "__format__"

from maze_dataset import MazeDataset, MazeDatasetConfig
from maze_dataset.generation import LatticeMazeGenerators
from maze_dataset.maze import SolvedMaze

_cfg: MazeDatasetConfig = MazeDatasetConfig(
    name="Maze Analysis",
    grid_n=10,  # number of rows/columns in the lattice
    n_mazes=100,  # number of mazes to generate
    maze_ctor=LatticeMazeGenerators.gen_dfs,  # algorithm to generate the maze
    maze_ctor_kwargs=dict(do_forks=True),  # additional parameters to pass to the maze generation algorithm
)
_DATASET = MazeDataset.from_config(_cfg)


def generate_mazes() -> MazeDataset:
    """
    Return the generated dataset, using the maze-datasets GitHub repository.
    """
    return _DATASET


def number_maze(maze: SolvedMaze) -> Graph:
    """
    Convert a MazeDataset instance into a graph object where the vertices
    contain numbers from 1 to n^2, where n is the number of rows/columns in the maze.
    """

    graph = Graph()
    adj_list = maze.as_adj_list()

    for connection in adj_list:
        coord1 = connection[0]
        coord2 = connection[1]

        v1 = coord1[0] * 10 + coord1[1] + 1
        v2 = coord2[0] * 10 + coord2[1] + 1

        graph.add_vertex(v1)
        graph.add_vertex(v2)

        graph.add_edge(v1, v2)

    return graph


if __name__ == '__main__':
    import python_ta
    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
