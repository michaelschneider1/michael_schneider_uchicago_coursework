"""
CMSC 14200, Spring 2025
Homework #4

Test file for HW4

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

import pytest
import json
import os
import ast

from graph import GridGraph, Vertex
from task1 import load_maze_grid, construct_grid_graph
from task2 import get_path_distance
from task3 import shortest_paths
from typing import TypedDict, Any


DATA_DIR = "data/"
EXPECTED_DIR = "data/output/"

INPUT_GRAPHS = [
    name.removesuffix(".txt")
    for name in os.listdir(DATA_DIR)
    if name.endswith(".txt")
]

GraphDict = TypedDict(
    "GraphDict",
    {
        "n": int,
        "m": int,
        "edges": dict[tuple[int, int], dict[tuple[int, int], int]],
    },
)


def jsonify_dict(d: Any) -> Any:
    """
    Given a dictionary d that has tuples as keys, convert them to string
    for JSON
    """
    if isinstance(d, dict):
        return {
            str(k) if isinstance(k, tuple) else k: jsonify_dict(v)
            for k, v in d.items()
        }
    elif isinstance(d, list):
        return [jsonify_dict(i) for i in d]
    else:
        return d


def jsonify_graph(graph: GridGraph) -> dict:
    """
    Create a JSON-compliant graph spec from GridGraph graph
    """

    output_dict: GraphDict = {"n": graph.n, "m": graph.m, "edges": graph.edges}

    return jsonify_dict(output_dict)


@pytest.mark.parametrize(
    "file_prefix, edges",
    [
        (
            "tiny_1_3",
            {
                (0, 0): {(0, 1): 1},
                (0, 1): {(0, 0): 1, (0, 2): 1},
                (0, 2): {(0, 1): 1},
            },
        ),
        (
            "tiny_2_2",
            {
                (0, 0): {(0, 1): 2, (1, 0): 1},
                (0, 1): {(0, 0): 1, (1, 1): 1},
                (1, 0): {(0, 0): 1, (1, 1): 1},
                (1, 1): {(1, 0): 1, (0, 1): 2},
            },
        ),
        (
            "tiny_2_3",
            {
                (0, 0): {(0, 1): 3, (1, 0): 1},
                (0, 1): {(0, 0): 1, (1, 1): 2},
                (1, 0): {(0, 0): 1, (1, 1): 2},
                (1, 1): {(1, 0): 1, (0, 1): 3, (1, 2): 1},
                (1, 2): {(1, 1): 2},
            },
        ),
    ],
)
def test_task1_construct_grid_graph_edges(
    file_prefix: str, edges: dict[Vertex, dict[Vertex, int]]
) -> None:
    grid = load_maze_grid(f"{DATA_DIR}/tiny/{file_prefix}.txt")
    actual_graph = construct_grid_graph(grid)
    actual_edges = jsonify_dict(actual_graph.edges)
    expected_edges = jsonify_dict(edges)
    assert actual_edges == expected_edges


@pytest.mark.parametrize("file_prefix", INPUT_GRAPHS)
def test_task1_construct_grid_graph(file_prefix: str) -> None:
    """
    Run a single test for each graph file to see if the construction
    is correct
    """
    grid = load_maze_grid(f"{DATA_DIR}/{file_prefix}.txt")
    actual_graph = construct_grid_graph(grid)
    with open(f"{EXPECTED_DIR}/{file_prefix}_grid.json") as fp:
        expected_graph = json.load(fp)
    assert jsonify_graph(actual_graph) == expected_graph


@pytest.mark.parametrize(
    "file_prefix, path, distance",
    [
        ("tiny_1_3", [], None),
        ("tiny_1_3", [(0, 0)], 0),
        ("tiny_1_3", [(0, 1)], 0),
        ("tiny_1_3", [(0, 2)], 0),
    ],
)
def test_task2_get_path_distance_0_or_1_steps(
    file_prefix: str, path: list[Vertex], distance: int | None
) -> None:
    grid = load_maze_grid(f"{DATA_DIR}/tiny/{file_prefix}.txt")
    graph = construct_grid_graph(grid)

    actual_path_distance = get_path_distance(graph, path)
    assert actual_path_distance == distance


@pytest.mark.parametrize(
    "file_prefix, path, distance",
    [
        ("tiny_1_3", [(0, 0), (0, 1), (0, 2)], 2),
        ("tiny_1_3", [(0, 0), (0, 1)], 1),
        ("tiny_1_3", [(0, 1), (0, 2)], 1),
        ("tiny_2_2", [(0, 0), (0, 1), (1, 1)], 3),
        ("tiny_2_2", [(0, 0), (1, 0), (1, 1)], 2),
        ("tiny_2_2", [(1, 0), (0, 0), (0, 1)], 3),
        ("tiny_2_3", [(1, 2), (1, 1), (0, 1), (0, 0), (1, 0)], 7),
        ("tiny_2_3", [(1, 0), (0, 0), (0, 1), (1, 1), (1, 2)], 7),
        ("tiny_2_3", [(0, 1), (1, 1)], 2),
    ],
)
def test_task2_get_path_distance_valid(
    file_prefix: str, path: list[Vertex], distance: int
) -> None:
    grid = load_maze_grid(f"{DATA_DIR}/tiny/{file_prefix}.txt")
    graph = construct_grid_graph(grid)

    actual_path_distance = get_path_distance(graph, path)
    assert actual_path_distance == distance


@pytest.mark.parametrize(
    "file_prefix, path, distance",
    [
        ("tiny_1_3", [(0, 0), (0, 1), (0, 0)], 2),
        ("tiny_1_3", [(0, 0), (0, 1), (0, 2), (0, 1), (0, 0)], 4),
        ("tiny_2_2", [(0, 0), (0, 1), (1, 1), (1, 0)] * 3, 14),
        ("tiny_2_3", [(0, 0), (0, 1), (1, 1), (0, 1), (1, 1), (1, 2)], 11),
    ],
)
def test_task2_get_path_distance_multiple_visits(
    file_prefix: str, path: list[Vertex], distance: int
) -> None:
    grid = load_maze_grid(f"{DATA_DIR}/tiny/{file_prefix}.txt")
    graph = construct_grid_graph(grid)

    actual_path_distance = get_path_distance(graph, path)
    assert actual_path_distance == distance


@pytest.mark.parametrize(
    "file_prefix, path",
    [
        ("tiny_1_3", [(0, 0), (0, 2)]),
        ("tiny_1_3", [(0, 2), (0, 0)]),
        ("tiny_1_3", [(0, 0), (0, 1), (0, 2), (0, 3)]),
        ("tiny_2_2", [(0, 0), (-1, 0), (0, 0)]),
        ("tiny_2_2", [(0, 0), (1, 0), (2, 0), (2, 1), (1, 1)]),
        ("tiny_2_2", [(0, 0), (1, 1)]),
        ("tiny_2_2", [(0, 0), (0, 1), (1, 0), (1, 1)]),
        ("tiny_2_3", [(0, 2), (1, 2)]),
        ("tiny_2_3", [(1, 2), (0, 2)]),
        ("tiny_2_3", [(0, 0), (0, 1), (0, 2), (1, 2)]),
    ],
)
def test_task2_get_path_distance_invalid(
    file_prefix: str, path: list[Vertex]
) -> None:
    grid = load_maze_grid(f"{DATA_DIR}/tiny/{file_prefix}.txt")
    graph = construct_grid_graph(grid)

    actual_path_distance = get_path_distance(graph, path)
    assert actual_path_distance == None


@pytest.mark.parametrize("file_prefix", INPUT_GRAPHS)
def test_task2_get_path_distance(file_prefix: str) -> None:
    """Run tests for each graph file to see if the path distance calculation is
    correct"""
    grid = load_maze_grid(f"{DATA_DIR}/{file_prefix}.txt")
    actual_graph = construct_grid_graph(grid)

    with open(f"{EXPECTED_DIR}/{file_prefix}_path_dist.json") as fp:
        path_cases = json.load(fp)

    for case in path_cases:
        path = [tuple(x) for x in case["path"]]
        expected_distance = case["distance"]
        actual_distance = get_path_distance(actual_graph, path)
        assert actual_distance == expected_distance


@pytest.mark.parametrize("file_prefix", INPUT_GRAPHS)
def test_task3_shortest_paths(file_prefix: str) -> None:
    """
    Run a single test for each graph file to check if S to E
    shortest-path distances are correct
    """
    grid = load_maze_grid(f"{DATA_DIR}/{file_prefix}.txt")
    actual_graph = construct_grid_graph(grid)
    assert actual_graph.start_pos is not None
    actual_distances = shortest_paths(actual_graph, actual_graph.start_pos)
    actual_abbr_distances = {k: v[0] for k,v in actual_distances.items()}

    with open(f"{EXPECTED_DIR}/{file_prefix}_distances.json") as fp:
        expected_distances = json.load(fp)
    assert (
        jsonify_dict(actual_abbr_distances) == expected_distances
    )
