"""
CMSC 14200, Spring 2025
Homework #4, Task #3

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
   1) https://docs.python.org/3/library/heapq.html to learn more about hepaq
"""

import heapq
from typing import TypeAlias
from graph import GridGraph, Vertex


DijkstraTable: TypeAlias = dict[Vertex, tuple[int, Vertex | None]]

def shortest_paths(graph: GridGraph, origin: Vertex) -> DijkstraTable:
    """
    Find the shortest path from the origin to every other reachable destination
    in the graph

    Inputs:
       graph (GridGraph): the grid graph
       origin (Vertex): the starting node

    Returns:
      DijkstraTable: Shortest distances from origin to every other vertex,
      along with the previous vertex along the shortest path.
    """
    heap: list[tuple[int, Vertex, Vertex | None]] = [(0, origin, None)]
    visited = set()
    d_table: DijkstraTable = {}

    while heap:
        distance, current_vertex, previous = heapq.heappop(heap)
        if current_vertex in visited:
            continue
        visited.add(current_vertex)
        d_table[current_vertex] = (distance, previous)

        for neighbor in graph.neighbors(current_vertex):
            if neighbor not in visited:
                weight = graph.get_weight(current_vertex, neighbor)
                if weight is not None:
                    heapq.heappush(heap, (distance + weight, neighbor,
                    current_vertex))
    return d_table
def trace_path(
    table: DijkstraTable, destination: Vertex
) -> tuple[list[Vertex], int]:
    """
    Given a dictionary of single-source shortest path distances and previous
    nodes, reconstruct the shortest path from origin to destination, as well
    as its distance.
    """
    if destination not in table:
        return ([], 0)
    path = []
    current_vertex = destination
    while current_vertex is not None:
        path.append(current_vertex)
        _, previous = table[current_vertex]
        if previous is None:
            break
        current_vertex = previous
    path.reverse()
    total = table[destination][0]

    return (path, total)
