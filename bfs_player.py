"""BFS Player.

A player that solves the maze using Breadth-First Search.

Copyright (c) 2026 [Ryan Tran, Jenny Bian, Raymond Wu, Soltan Isgandar]. All rights reserved.
"""

from typing import Any
from player import Player
from graph import Graph


class BFSPlayer(Player):
    """A player that solves the maze using Breadth-First Search.

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

    >>> player = BFSPlayer(g)
    >>> player.get_path_bfs(1, 3)
    [1, 2, 3]

    >>> player.get_path_bfs(1, 1)
    [1]

    >>> player.get_path_bfs(1, 4)
    []
    """

    def solve(self, start: int, end: int) -> list[int]:
        """Solve the maze from start to end using BFS.
        Return the path taken, or an empty list if no path exists.
        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_edge(1, 2)

        >>> player = BFSPlayer(g)
        >>> player.solve(1, 2)
        [1, 2]
        """
        path = self.get_path_bfs(start, end)
        for position in path:
            self.move(int(position))
        return self._path

    def get_path_bfs(self, start: Any, end: Any) -> list[int]:
        """Return the shortest path from start to end using BFS, or an empty list if none exists.

            Preconditions:
                - start and end are integers representing vertex IDs.
        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_vertex(3)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 3)

        >>> player = BFSPlayer(g)
        >>> player.get_path_bfs(1, 3)
        [1, 2, 3]

        >>> player.get_path_bfs(2, 2)
        [2]

        >>> player.get_path_bfs(3, 1)
        [3, 2, 1]

        >>> player.get_path_bfs(1, 99)
        []
        """
        if start not in self._graph.get_all_vertices() or end not in self._graph.get_all_vertices():
            return []

        queue = [[start]]
        visited = {start}

        while queue:
            path = queue.pop(0)
            current = int(path[-1])
            self._num_moves += 1

            if current == end:
                return path

            for neighbour in self._graph.get_neighbours(current):
                if neighbour not in visited:
                    visited.add(int(neighbour))
                    queue.append(path + [neighbour])

        return []

    def run_game(self, start: int, end: int) -> list:
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
