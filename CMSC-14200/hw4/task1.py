"""
CMSC 14200, Spring 2025
Homework #4, Task #1

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from graph import GridGraph


def load_maze_grid(filename: str) -> list[list[str]]:
    """
    Read a file that contains a maze specification and
    return a 2D-list representation of the maze.

    Input:
       filename (str): The file to load, assumed to
       represent a valid maze

    Returns:
       list[list[str]]: 2D-list matrix of the maze
    """
    maze_representation = []
    with open(filename, "r") as file:
        current_line = file.readline()
        while current_line != "":
            current_row = current_line.split()
            maze_representation.append(current_row)
            current_line = file.readline()
    return maze_representation

def construct_grid_graph(grid: list[list[str]]) -> GridGraph:
    """
    Given a 2D representation of a maze, induce the grid graph object

    Input:
        grid (list[list[str]]): The input maze

    Returns:
        GridGraph: The induced grid graph object
    """
    n = len(grid)
    m = len(grid[0])
    graph = GridGraph(n, m)

    for row_index in range(n):
        for col_index in range(m):
            if grid[row_index][col_index] != "#":
                current_coord = (row_index, col_index)
                graph.add_vertex(current_coord)
                if grid[row_index][col_index] == "S":
                    graph.start_pos = current_coord
                elif grid[row_index][col_index] == "E":
                    graph.target_pos = current_coord
                if row_index != 0:
                    up_coord = (row_index - 1, col_index)
                    up_value = grid[row_index - 1][col_index]
                    if up_value != "#":
                        if up_value in ["S", "E"]:
                            graph.add_edge(current_coord, up_coord, 1)
                        else:
                            graph.add_edge(current_coord, up_coord, \
                            int(up_value))
                if row_index != n - 1:
                    down_coord = (row_index + 1, col_index)
                    down_value = grid[row_index + 1][col_index]
                    if down_value != "#":
                        if down_value in ["S", "E"]:
                            graph.add_edge(current_coord, down_coord, 1)
                        else:
                            graph.add_edge(current_coord, down_coord, \
                            int(down_value))
                if col_index != 0:
                    left_coord = (row_index, col_index - 1)
                    left_value = grid[row_index][col_index - 1]
                    if left_value != "#":
                        if left_value in ["S", "E"]:
                            graph.add_edge(current_coord, left_coord, 1)
                        else:
                            graph.add_edge(current_coord, left_coord, \
                            int(left_value))
                if col_index != m - 1:
                    right_coord = (row_index, col_index + 1)
                    right_value = grid[row_index][col_index + 1]
                    if right_value != "#":
                        if right_value in ["S", "E"]:
                            graph.add_edge(current_coord, right_coord, 1)
                        else:
                            graph.add_edge(current_coord, right_coord, \
                            int(right_value))
    return graph
    