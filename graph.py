"""Main graph & vertex classes.

The main graph class and vertex class for representing and manipulating graphs.

Copyright (c) 2026 [Ryan Tran, Jenny Bian, Raymond Wu, Soltan Isgandar]. All rights reserved.
"""

from __future__ import annotations

from typing import Any


class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The item stored in this vertex
        - neighbours: A set of the vertices adjacent to this vertex

    Representation Invariants:
        - item is not None
        - self not in self.neighbours
        - all(v not in self.neighbours for v in self.neighbours)
    """

    _item: Any
    _neighbours: set[_Vertex]

    def __init__(self, item: Any, neighbours: set) -> None:
        self._item = item
        self._neighbours = neighbours

    def adjacent_vertices(self) -> set[_Vertex]:
        """Return the set of adjacent vertices.
        >>> v1 = _Vertex(1, set())
        >>> v2 = _Vertex(2, set())
        >>> v1.add_neighbour(v2)
        >>> v1.adjacent_vertices() == {v2}
        True"""
        return self._neighbours

    def get_item(self) -> Any:
        """
        Return the item stored in this vertex.
        >>> v = _Vertex(5, set())
        >>> v.get_item()
        5
        """
        return self._item

    def check_connected(self, target_item: Any, visited: set[_Vertex]) -> bool:
        """Return whether connected to target_item."""
        visited.add(self)
        return self._check_connected_helper(target_item, visited)

    def _check_connected_helper(self, target_item: Any, visited: set[_Vertex]) -> bool:
        if self._item == target_item:
            return True
        for neighbor in self._neighbours:
            if neighbor not in visited and neighbor._check_connected_helper(target_item, visited):
                return True
        return False

    def add_neighbour(self, vertex: _Vertex) -> None:
        """
        Add the given vertex to self._neighbours.
        Preconditions:
            - vertex != self

        >>> v1 = _Vertex(1, set())
        >>> v2 = _Vertex(2, set())
        >>> v1.add_neighbour(v2)
        >>> v2 in v1.adjacent_vertices()
        True
        """
        self._neighbours.add(vertex)

    def degree(self) -> int:
        """
        Returns the number of neighbours that this vertex has.

        >>> v1 = _Vertex(1, set())
        >>> v1.degree()
        0
        >>> v2 = _Vertex(2, set())
        >>> v1.add_neighbour(v2)
        >>>
        """
        return len(self._neighbours)

    def get_path(self, target_item: Any, visited: set[_Vertex]) -> list[Any]:
        """ Return a path between item1 and item2, or an empty list if none exists.
        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_edge(1, 2)
        >>> g.get_path(1, 2)
        [1, 2]
        >>> g.get_path(1, 3)
        []
        """
        visited.add(self)
        return self._get_path_helper(target_item, visited)

    def _get_path_helper(self, target_item: Any, visited: set[_Vertex]) -> list[Any]:
        stack = [(self, [self._item])]
        while stack:
            current, path = stack.pop()
            if current._item == target_item:
                return path
            for neighbor in current._neighbours:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor._item]))
        return []

    def get_neighbours(self) -> set:
        """
        Return the set of items adjacent to this vertex.

        >>> v1 = _Vertex(1, set())
        >>> v2 = _Vertex(2, set())
        >>> v1.add_neighbour(v2)
        >>> v1.get_neighbours()
        {2}
        """
        return {v._item for v in self._neighbours}

    def get_neighbours_vertex(self) -> set[_Vertex]:
        """
        Return the set of vertices adjacent to this vertex.
        """

        return self._neighbours


class Graph:
    """A graph data structure.

    Instance Attributes:
        - vertices: A set of the vertices in this graph.
        - edges: A set of the edges in this graph. Each edge is represented as a
            tuple of two vertices (u, v) where u and v are in vertices.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)

    """

    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        If a vertex with the given item already exists in this graph, raise ValueError.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.is_vertex(1)
        True
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, set())

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_edge(1, 2)
        >>> g.get_neighbours(1)
        {2}
        >>> g.get_neighbours(2)
        {1}
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            v1.add_neighbour(v2)
            v2.add_neighbour(v1)
        else:
            raise ValueError

    def connected(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are connected vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_edge(1, 2)
        >>> g.connected(1, 2)
        True
        >>> g.connected(1, 3)
        False
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            if v1.check_connected(v2.get_item(), set()):
                return True
        return False

    def get_path(self, item1: Any, item2: Any) -> list:
        """
        Return a path between item1 and item2, or an empty list if none exists.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_edge(1, 2)
        >>> g.get_path(1, 2)
        [1, 2]
        >>> g.get_path(1, 3)
        []
        """
        if item1 in self._vertices and item2 in self._vertices:
            return self._vertices[item1].get_path(item2, set())
        return []

    def is_vertex(self, item: Any) -> bool:
        """Return whether the given item exists as a vertex in this graph.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.is_vertex(1)
        True
        >>> g.is_vertex(2)
        False
        """
        return item in self._vertices

    def get_neighbours(self, item: Any) -> set:
        """Return the set of items adjacent to the given item in this graph.

        Raise a ValueError if item does not appear as a vertex in this graph.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_edge(1, 2)
        >>> g.get_neighbours(1)
        {2}
        """
        if item not in self._vertices:
            raise ValueError
        return set(self._vertices[item].get_neighbours())

    def get_all_vertices(self) -> dict[Any, _Vertex]:
        """
        Returns all vertices in the graph.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> sorted(g.get_all_vertices().keys())
        [1]
        """
        return self._vertices

    def remove_vertex(self, item: Any) -> None:
        """
        Remove the specified vertex if item is in self._graph._vertices.
        If item is not in the graph, raise ValueError.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_edge(1, 2)
        >>> g.remove_vertex(2)
        >>> g.is_vertex(2)
        False
        >>> g.get_neighbours(1)
        set()
        """
        if item not in self._vertices:
            raise ValueError
        vertex = self._vertices[item]
        for neighbour in vertex.get_neighbours_vertex():
            neighbour.get_neighbours_vertex().remove(vertex)
        self._vertices.pop(item)


if __name__ == '__main__':
    import python_ta
    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
