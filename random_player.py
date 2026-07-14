"""Random Player.

A player that solves the maze by randomly choosing a direction to move in.

Copyright (c) 2026 [Ryan Tran, Jenny Bian, Raymond Wu, Soltan Isgandar]. All rights reserved.
"""
import random
from player import Player
from graph import Graph


class RandomPlayer(Player):
    """A player that solves the maze by randomly choosing a direction to move in.

    This player does not use any strategy and may take a long time to solve the maze.

    Instance attributes:
        - _graph: the graph representation of the maze
    """

    def solve(self, start: int, end: int) -> list[int]:
        """Solve the maze from start to end by randomly choosing a direction to move in.
        Return the path taken.

        Preconditions:
        - start in self._graph._vertices
        - end in self._graph._vertices

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_vertex(3)
        >>> g.add_vertex(4)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 3)
        >>> g.add_edge(3, 4)
        >>> player = RandomPlayer(g)
        >>> result = player.solve(1, 4)
        >>> isinstance(result, list)
        True
        >>> all(isinstance(x, int) for x in result)
        True
        >>> player.get_current_position() == 4
        True
        """
        self._path.append(start)
        while self.get_current_position() != end:
            current = int(self.get_current_position())
            neighbours = self._graph.get_neighbours(current)
            valid_choices = list(neighbours)
            choice = int(random.choice(valid_choices))
            self.move(choice)
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
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
