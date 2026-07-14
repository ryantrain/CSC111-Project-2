"""Compass Player.

A player that solves the maze using the compass algorithm, which always tries to move in a specific order of directions
(e.g., north, east, south, west) and backtracks when it hits a dead end.

Copyright (c) 2026 [Ryan Tran, Jenny Bian, Raymond Wu, Soltan Isgandar]. All rights reserved.
"""

from graph import Graph
from player import Player


class CompassPlayer(Player):
    """
    A player solving the maze using the compass algorithm.


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
        Solve the maze from start to finish using the hand on the compass algorithm.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_vertex(3)
        >>> g.add_vertex(4)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 3)
        >>> g.add_edge(3, 4)
        >>> player = CompassPlayer(g)
        >>> path = player.solve(1, 4)
        >>> isinstance(path, list)
        True
        >>> isinstance(path, list)
        True
        >>> player.solve(1, 1)
        [1]
        """
        directions = [1, 10, -1, -10]
        vertices = self._graph.get_all_vertices()

        self._path = []
        self._num_moves = 0

        if start not in vertices or end not in vertices:
            return []

        self._path = [start]
        if start == end:
            self._num_moves = len(self._path)
            return self._path

        visited_locations = {start}
        stack = [start]

        while stack:
            current_location = stack[-1]
            if current_location == end:
                self._num_moves = len(self._path)
                return self._path

            moved_forward = False
            neighbours = vertices[current_location].get_neighbours()

            for d in directions:
                next_location = current_location + d
                if next_location in neighbours and next_location not in visited_locations:
                    visited_locations.add(next_location)
                    stack.append(next_location)
                    self.move(next_location)
                    moved_forward = True
                    break

            if not moved_forward:
                stack.pop()
                if not stack:
                    return []

                # Record the step back so the returned route reflects traversal.
                self.move(stack[-1])

        return []

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
