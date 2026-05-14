"""
CMSC 14200, Spring 2025
Homework #4, Task #2

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from graph import GridGraph, Vertex


def get_path_distance(graph: GridGraph, path: list[Vertex]) -> int | None:
    """
    Determine the total distance of the given path in the grid graph.
    If invalid, returns None.
    """
    if path == []:
        return None
    if len(path) == 1:
        return 0
    total = 0
    for step, _ in enumerate(path[:-1]):
        current_location = path[step]
        next_location = path[step + 1]

        weight = graph.get_weight(current_location, next_location)

        if weight is None:
            return None
        else:
            total += weight
    return total
