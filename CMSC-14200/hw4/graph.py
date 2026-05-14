"""
CMSC 14200, Spring 2025
Homework #4

Grid Graph implementation

DO NOT MODIFY THIS FILE
"""

from typing import TypeAlias

Vertex: TypeAlias = tuple[int, int]


class GridGraph:
    """
    A Class to represent a graph, which maintains an adjacency list
    as an edge dictionary. Also contains a start and target position.
    """

    n: int
    m: int
    edges: dict[Vertex, dict[Vertex, int]]
    start_pos: Vertex | None
    target_pos: Vertex | None

    def __init__(self, n: int, m: int):
        """
        Initialize a Grid Graph with a given shape
        Inputs:
            n (int): number of rows
            m (int): number of columns
        """
        self.n = n
        self.m = m
        self.edges = {}
        self.start_pos = None
        self.target_pos = None

    def add_vertex(self, vertex: Vertex) -> None:
        """
        Initialize a vertex (grid position)
        """
        self.edges[vertex] = {}

    def add_edge(
        self, src_vertex: Vertex, dest_vertex: Vertex, weight: int
    ) -> None:
        """
        Store an edge between two vertex positions with integer weight
        """
        self.edges[src_vertex][dest_vertex] = weight

    def neighbors(self, v: Vertex) -> set[Vertex]:
        """
        Return the positions that are neighboring to a vertex
        """
        if v in self.edges:
            return set(self.edges[v].keys())
        else:
            return set()

    def get_weight(self, src: Vertex, dest: Vertex) -> int | None:
        """
        Return the weight between two vertices, if there is a direct edge
        between them
        """
        n = self.neighbors(src)
        if dest in n:
            return self.edges[src][dest]
        else:
            return None
