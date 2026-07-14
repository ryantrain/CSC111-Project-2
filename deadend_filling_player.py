"""Dead End Filling Player.

A player that solves the maze by filling in dead ends until only one path is left.

Copyright (c) 2026 [Ryan Tran, Jenny Bian, Raymond Wu, Soltan Isgandar]. All rights reserved.
"""

from typing import Any

from graph import Graph
from player import Player


class DeadEndFillingPlayer(Player):
    """
    A player solving the maze by filling in dead ends until only one path is left.

    Instance attributes:
        - _graph: the graph representation of the maze
        - _num_moves: number of moves made
        - _path: list of moves made
    Representation Invariants:
        - _graph is not None
        - _num_moves >= 0
    """

    def solve(self, start: int, end: int) -> list[int]:
        """
        Solve the maze using the dead end filling algorithm.
        Fill in all dead ends in the graph, then return the path from start to end.
            >>> g = Graph()
        >>> for i in [1, 2, 3, 4, 5]:
        ...     g.add_vertex(i)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 3)
        >>> g.add_edge(2, 4)
        >>> g.add_edge(4, 5)
        >>> p = DeadEndFillingPlayer(g)
        >>> p.solve(1, 5)
        [1, 2, 4, 5]
        >>> p.solve(1, 1)
        [1]
        """
        self._path = []
        self.fill_dead_ends(start, end)
        solution = self._graph.get_path(start, end)
        for position in solution:
            self.move(int(position))
        return self._path

    def fill_dead_ends(self, start: Any, end: Any) -> None:
        """Remove all dead ends from the graph, keeping start and end.
        Preconditions:
            - start and end are valid vertex IDs in the graph.
        >>> g = Graph()
        >>> for i in [1, 2, 3, 4, 5]:
        ...     g.add_vertex(i)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 3)
        >>> g.add_edge(2, 4)
        >>> g.add_edge(4, 5)
        >>> p = DeadEndFillingPlayer(g)
        >>> p.fill_dead_ends(1, 5)
        >>> g.is_vertex(3)
        False
        >>> g.is_vertex(2)
        True
        """
        changed = True
        while changed:
            changed = False
            for item in list(self._graph.get_all_vertices()):
                neighbours = self._graph.get_neighbours(item)
                if len(neighbours) == 1 and item != start and item != end:
                    self._graph.remove_vertex(item)
                    changed = True

    def run_game(self, start: int, end: int) -> list[int]:
        """
        Run one instance of the game of the given Player.
        """
        return self.solve(start, end)


if __name__ == '__main__':
    import python_ta
    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
