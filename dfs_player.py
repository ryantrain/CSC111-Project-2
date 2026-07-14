"""DFS Player.

A player that solves the maze using Depth-First Search.

Copyright (c) 2026 [Ryan Tran, Jenny Bian, Raymond Wu, Soltan Isgandar]. All rights reserved.
"""

from typing import Any
from graph import Graph
from player import Player


class DFSPlayer(Player):
    """A player that solves the maze using Depth-First Search.

    Instance Attributes:
        - _graph: the graph representation of the maze

    Representation Invariants:
        - self._graph is not None
    >>> g = Graph()
    >>> g.add_vertex(1)
    >>> g.add_vertex(2)
    >>> g.add_vertex(3)
    >>> g.add_edge(1, 2)
    >>> g.add_edge(2, 3)

    >>> player = DFSPlayer(g)
    >>> player.get_path_dfs(1, 3)
    [1, 2, 3]

    >>> player.get_path_dfs(1, 1)
    [1]

    >>> player.get_path_dfs(1, 99)
    []
    """

    def solve(self, start: int, end: int) -> list[int]:
        """Solve the maze from start to end using DFS.
        Return the path taken, or an empty list if no path exists.
        Preconditions:
            - start and end are valid vertex IDs in the graph.
        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_edge(1, 2)
        >>> player = DFSPlayer(g)
        >>> player.solve(1, 2)
        [1, 2]
        """
        path = self.get_path_dfs(start, end)
        for position in path:
            self.move(int(position))
        return self._path

    def get_path_dfs(self, start: Any, end: Any) -> list[int]:
        """Return the shortest path from start to end using DFS, or an empty list if none exists.
        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_vertex(3)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 3)
        >>> player = DFSPlayer(g)
        >>> player.get_path_dfs(1, 3)
        [1, 2, 3]

        >>> player.get_path_dfs(2, 2)
        [2]

        >>> player.get_path_dfs(3, 1)
        [3, 2, 1]

        >>> player.get_path_dfs(1, 99)
        []
        """
        if start not in self._graph.get_all_vertices() or end not in self._graph.get_all_vertices():
            return []
        return self._graph.get_all_vertices()[start].get_path(end, set())

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
