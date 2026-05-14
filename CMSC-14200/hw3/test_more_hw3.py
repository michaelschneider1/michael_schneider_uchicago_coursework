"""
CMSC 14200, Spring 2025
Homework #3

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

import pytest

from image import Image, Loc, Color
from graph import ImageGraph


### TASK 2 TESTS ###


def test_task2_neighbors_corners() -> None:
    """
    Load the image represented by assets/grid.ppm, and
    check that `neighbors` returns the correct answer
    for each of the four corner pixels (top-left, top-right,
    bottom-right, and bottom-left).
    """
    image = ImageGraph(Image("assets/grid.ppm"))
    assert image.neighbors((0,0)) == {(0, 1), (1, 0)}
    assert image.neighbors((319, 0)) == {(318, 0), (319, 1)}
    assert image.neighbors((0, 191)) == {(1, 191), (0, 190)}
    assert image.neighbors((319, 191)) == {(319, 190), (318, 191)}

def test_task2_neighbors_edges() -> None:
    """
    Load the image represented by assets/grid.ppm, and
    check that `neighbors` returns the correct answer
    for one non-corner pixel on each of the four edges
    of the image (left, top, right, bottom).
    """
    image = ImageGraph(Image("assets/grid.ppm"))
    assert image.neighbors((0, 1)) == {(0, 0), (0, 2), (1, 1)}
    assert image.neighbors((1, 0)) == {(0, 0), (2, 0), (1, 1)}
    assert image.neighbors((319, 190)) == {(319, 191), (319, 189), (318, 190)}
    assert image.neighbors((318, 191)) == {(317, 191), (319, 191), (318, 190)}

def test_task2_neighbors_interior() -> None:
    """
    Load the image represented by assets/grid.ppm, and
    check that `neighbors` returns the correct answer
    for three distinct interior pixels (i.e, excluding
    corner and edge pixels).
    """
    image = ImageGraph(Image("assets/grid.ppm"))
    assert image.neighbors((1, 1)) == {(0, 1), (1, 0), (1, 2), (2, 1)}
    assert image.neighbors((2, 2)) == {(2, 3), (3, 2), (1, 2), (2, 1)}
    assert image.neighbors((3, 3)) == {(2, 3), (4, 3), (3, 2), (3, 4)}

### TASK 4 TESTS ###


def test_task4_compute_all_regions_count() -> None:
    """
    For each of the three sample images
    (assets/{example, grid, shapes.ppm}), call
    compute_all_regions and check that the number
    of regions and total number of pixels inside
    the regions are correct.
    """
    example_img = ImageGraph(Image("assets/example.ppm"))
    grid_img = ImageGraph(Image("assets/grid.ppm"))
    shapes_img = ImageGraph(Image("assets/shapes.ppm"))

    example_regions = example_img.compute_all_regions()
    grid_regions = grid_img.compute_all_regions()
    shapes_regions = shapes_img.compute_all_regions()

    total_example_pixels = 0
    for region in example_regions:
        total_example_pixels += len(region["pixels"])
    total_grid_pixels = 0
    for region in grid_regions:
        total_grid_pixels += len(region["pixels"])
    total_shapes_pixels = 0
    for region in shapes_regions:
        total_shapes_pixels += len(region["pixels"])
    assert len(example_regions) == 4
    assert total_example_pixels == (2 * 4)

    assert len(grid_regions) == 15
    assert total_grid_pixels == (320 * 192)

    assert len(shapes_regions) == 10
    assert total_shapes_pixels == (800 * 300)
def test_task4_compute_all_regions_count_blue() -> None:
    """
    For each of the three sample images
    (assets/{example, grid, shapes.ppm}), call
    compute_all_regions and check that the number
    of blue regions are correct.
    """
    example_img = ImageGraph(Image("assets/example.ppm"))
    grid_img = ImageGraph(Image("assets/grid.ppm"))
    shapes_img = ImageGraph(Image("assets/shapes.ppm"))

    example_regions = example_img.compute_all_regions()
    grid_regions = grid_img.compute_all_regions()
    shapes_regions = shapes_img.compute_all_regions()

    example_blue_regions = 0
    for region in example_regions:
        if region["color"] == (0, 0, 255):
            example_blue_regions += 1
    grid_blue_regions = 0
    for region in grid_regions:
        if region["color"] == (0, 0, 255):
            grid_blue_regions += 1

    shapes_blue_regions = 0
    for region in shapes_regions:
        if region["color"] == (0, 0, 255):
            shapes_blue_regions += 1

    assert example_blue_regions == 1
    assert grid_blue_regions == 8
    assert shapes_blue_regions == 1

def test_task4_compute_all_regions_count_colors() -> None:
    """
    For each of the three sample images
    (assets/{example, grid, shapes.ppm}), call
    compute_all_regions and check that the number
    of regions for each color in the image is
    correct.
    """
    example_img = ImageGraph(Image("assets/example.ppm"))
    grid_img = ImageGraph(Image("assets/grid.ppm"))
    shapes_img = ImageGraph(Image("assets/shapes.ppm"))

    example_regions = example_img.compute_all_regions()
    grid_regions = grid_img.compute_all_regions()
    shapes_regions = shapes_img.compute_all_regions()

    example_regions_colors = set()
    for region in example_regions:
        if region["color"] not in example_regions_colors:
            example_regions_colors.add(region["color"])

    grid_regions_colors = set()
    for region in grid_regions:
        if region["color"] not in grid_regions_colors:
            grid_regions_colors.add(region["color"])

    shapes_regions_colors = set()
    for region in shapes_regions:
        if region["color"] not in shapes_regions_colors:
            shapes_regions_colors.add(region["color"])

    assert len(example_regions_colors) == 4
    assert len(grid_regions_colors) == 2
    assert len(shapes_regions_colors) == 5
