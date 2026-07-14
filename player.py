"""Player Class.

Parent class for all algorithms that solve the maze.
This class should not be instantiated directly, but rather inherited by specific algorithm implementations.

Copyright (c) 2026 [Ryan Tran, Jenny Bian, Raymond Wu, Soltan Isgandar]. All rights reserved.
"""

from graph import Graph


class Player:
    """Parent class for the player character and bot algorithms.

    Instance Attributes:
    - _num_moves: the number of moves this player has made
    - _path: the paths this player has taken in chronological order

    Representation Invariants:
    - self.num_moves >= 0
    - self._path == [] or self._path[-1] is the current position

    """
    _num_moves: int
    _path: list[int]
    _graph: Graph

    def __init__(self, graph: Graph) -> None:
        """Initialize the player with a graph, 0 moves, and empty path."""
        self._num_moves = 0
        self._path = []
        self._graph = graph

    def get_num_moves(self) -> int:
        """
        Return the number of moves this player has made.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> p = Player(g)
        >>> p.get_num_moves()
        0
        >>> p.move(1)
        >>> p.get_num_moves()
        1
        """
        return self._num_moves

    def get_path(self) -> list[int]:
        """
        Return the path this player has traversed in chronological order.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> p = Player(g)
        >>> p.get_path()
        []
        >>> p.move(1)
        >>> p.get_path()
        [1]
        >>> p.move(2)
        >>> p.get_path()
        [1, 2]
        """
        return self._path

    def move(self, position: int) -> None:
        """
        Move the player to the given position and update the path and move count.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> p = Player(g)
        >>> p.move(1)
        >>> p.get_path()
        [1]
        >>> p.get_num_moves()
        1
        >>> p.move(2)
        >>> p.get_path()
        [1, 2]
        >>> p.get_num_moves()
        2
        """
        self._path.append(position)
        self._num_moves += 1

    def get_current_position(self) -> int:
        """
        Return the current position of the player, or -1 if the player has not moved yet.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> p = Player(g)
        >>> p.get_current_position()
        -1
        >>> p.move(1)
        >>> p.get_current_position()
        1
        >>> p.move(2)
        >>> p.get_current_position()
        2
        """
        if not self._path:
            return -1
        return self._path[-1]

    def reset(self) -> None:
        """
        Reset the player to their initial state.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> p = Player(g)
        >>> p.move(1)
        >>> p.move(2)
        >>> p.get_path()
        [1, 2]
        >>> p.get_num_moves()
        2
        >>> p.reset()
        >>> p.get_path()
        []
        >>> p.get_num_moves()
        0
        """
        self._num_moves = 0
        self._path = []

    def is_solved(self, end: int) -> bool:
        """
        Return whether the maze has been completed.
        """
        return self._path[-1] == end

    def run_game(self, start: int, end: int) -> list[int]:
        """
        Run the maze from start to end and return the path taken.
        This method should be overridden by subclasses to implement specific algorithms.
        """
        raise NotImplementedError

    def solve(self, start: int, end: int) -> list:
        """
        Return a list of the path taken to reach the end of the maze.
        This function should be overwritten by child classes.
        """
        raise NotImplementedError


if __name__ == '__main__':
    import python_ta
    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
