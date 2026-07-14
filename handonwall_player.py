"""Hand on Wall Player.

Hand on wall player that uses the left hand method to solve the maze.
This player will always keep its hand on the left side.

Copyright (c) 2026 [Ryan Tran, Jenny Bian, Raymond Wu, Soltan Isgandar]. All rights reserved.
"""

from graph import Graph
from player import Player


class HandOnWallPlayer(Player):
    """
    A player solving the maze using the hand on wall approach.
    This player will always keep its hand on the left side.

    Instance attributes:
        - _graph: the graph representation of the maze
        - _num_moves: number of moves made
        - _path: list of moves made
    Representation Invariants:
        - _graph is not None
        - _num_moves >= 0

    """

    def solve(self, start: int, end: int) -> list:
        """
        Solve the maze from start to finish using the hand on the wall method (left hand).
        The path the player takes will be stored and returned at the end.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_vertex(3)
        >>> g.add_vertex(4)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 3)
        >>> g.add_edge(3, 4)
        >>> player = HandOnWallPlayer(g)
        >>> path = player.solve(1, 4)
        >>> isinstance(path, list)
        True
        >>> all(isinstance(move, int) for move in path)
        True
        >>> isinstance(path, list)
        True
        >>> player.solve(1, 1)
        [1]
        """
        self._path = []
        self._num_moves = 0
        directions = [1, 10, -1, -10]  # Right, down, left, up
        current_location = start  # Initialize current location to start

        # Check if start and end are valid vertices in the graph
        if start not in self._graph.get_all_vertices() or end not in self._graph.get_all_vertices():
            return []

        # Initialize the path with the starting location
        self._path.append(start)

        # When start and end are the same node, return the path immediately
        if start == end:
            self._num_moves = len(self._path)
            return self._path

        vertices = self._graph.get_all_vertices()
        current_direction = 0
        visited_states = {(start, current_direction)}  # Used for checking directions every node

        while current_location != end:
            assert current_location in vertices

            neighbours = vertices[current_location].get_neighbours()

            left_hand = (current_direction - 1) % 4

            turn_order = [
                left_hand,
                current_direction,
                (current_direction + 1) % 4,
                (current_direction + 2) % 4
            ]

            moved = False
            for direction_index in turn_order:
                next_location = current_location + directions[direction_index]
                if next_location in neighbours:
                    current_direction = direction_index
                    self.move(next_location)
                    current_location = next_location
                    moved = True
                    break

            if not moved:
                return []

            state = (current_location, current_direction)
            if current_location != end and state in visited_states:
                return []
            visited_states.add(state)

        self._num_moves = len(self._path)
        return self._path

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
        'allowed-io': [],     # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
