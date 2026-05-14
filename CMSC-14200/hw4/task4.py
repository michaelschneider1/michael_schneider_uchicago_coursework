"""
CMSC 14200, Spring 2025
Homework #4, Task #4

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from graph import GridGraph, Vertex
from task1 import load_maze_grid, construct_grid_graph
from task2 import get_path_distance
from task3 import shortest_paths, trace_path
import sys

DIRECTIONS = {"up": (-1, 0),
"down": (1, 0),
"left": (0, -1),
"right": (0, 1)}

BLUE = "\033[34m"
RED =  "\033[31m"
DEFAULT = "\033[0m"

def make_grid(grid: list[list[str]], current_vertex: Vertex, visited:
    set[Vertex]) -> list[list[str]]:
    final_grid = []
    for row_index, row in enumerate(grid):
        this_row = []
        for col_index, value in enumerate(row):
            position = (row_index, col_index)
            if position == current_vertex:
                spot = f"{BLUE}{value}{DEFAULT}"
            elif position in visited and position != current_vertex:
                spot = f"{RED}{value}{DEFAULT}"
            else:
                spot = value
            this_row.append(spot)
        final_grid.append(this_row)
    return final_grid

def display_grid(grid: list[list[str]]) -> None:
    for row in grid:
        print(" ".join(row))

def gameplay() -> None:
    print("Shall we play a game?")
    file = sys.argv[1]
    grid = load_maze_grid(file)
    graph = construct_grid_graph(grid)
    print(f"Loading File: {file}")

    assert graph.start_pos is not None
    assert graph.target_pos is not None

    start: Vertex = graph.start_pos
    target: Vertex = graph.target_pos

    d_table = shortest_paths(graph, start)
    shortest_path, shortest_distance = trace_path(d_table, target)

    current_vertex = start
    visited = {start}
    path: list[Vertex] = [start]

    while True:
        constructed_grid = make_grid(grid, current_vertex, visited)
        display_grid(constructed_grid)

        get_distance = get_path_distance(graph, path)
        if get_distance is None:
            distance = 0
        else:
            distance = get_distance
        print(f"Current distance: {distance}")

        move = input("Enter a direction (u)p, (d)own, (l)eft, (r)ight, or (q)uit: ")
        if move == "u":
            move = "up"
        elif move == "d":
            move = "down"
        elif move == "l":
            move = "left"
        elif move == "r":
            move = "right"
        elif move == "q":
            print("Quitter!")
            break
        else:
            print("Invalid move! Please use a valid input!")
            continue
        
        change_r, change_c = DIRECTIONS[move]
        next_step = (current_vertex[0] + change_r, current_vertex[1] + change_c)

        if next_step not in graph.neighbors(current_vertex):
            print("Invalid move! Move is undoable!")
            continue
        
        path.append(next_step)
        visited.add(next_step)
        current_vertex = next_step

        if current_vertex == target:
            final_distance = get_path_distance(graph,path)
            if final_distance == shortest_distance:
                print("Your path is equivelent to the shortest path to the end!")
            else:
                print(f"Sorry! Your path with distance {final_distance} is longer than the shortest path ({shortest_distance})")
            break

if __name__ == "__main__":
    gameplay()
