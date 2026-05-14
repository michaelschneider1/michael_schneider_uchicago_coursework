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

from image import Image, Color, Loc
from typing import TypedDict

Region = TypedDict(
    "Region",
    {"color": Color, "pixels": set[Loc], "outline": set[Loc]},
)


class ImageGraph:
    """
    Class for a graph over an image where adjacent pixels are neighbors
    """

    def __init__(self, image: Image):
        """
        Constructor

        Inputs:
            image (Image): the image over which to build the graph
        """
        self.image = image

    def neighbors(self, location: Loc) -> set[Loc]:
        """
        Determines the pixels adjacent to a given pixel in the graph.
        Adjacency is defined by being immediately above, below, to the
        left, or to the right.

        Inputs:
            location (Loc): the pixel whose immediate neighbors to find

        Returns (set[Loc]): the set of immediate neighbors
        """
        x, y = location
        neighbors_set: set[Loc] = set()
        if y > 0:
            neighbors_set.add((x, y - 1))
        if y < self.image.height - 1:
            neighbors_set.add((x, y + 1))
        if x > 0:
            neighbors_set.add((x - 1, y))
        if x < self.image.width - 1:
            neighbors_set.add((x + 1, y))
        return neighbors_set

    def compute_region(self, start: Loc) -> Region:
        """
        Determines the region of contiguous pixels surrounding the given
        starting pixel with the same color, then returns (i) its color,
        (ii) the set of pixels in the region, and (iii) the set of pixels
        on the border between this region and other-colored regions or the
        edge of the image. Contiguity is defined by being directly above,
        below, to the left, or to the right.

        Inputs:
            start (Loc): a pixel in the region to outline

        Returns (Region): the color, interior, and outline of the region
        """
        start_x, start_y = start
        visited: set[Loc] = set()
        will_visit: set[Loc] = {start}
        border: set[Loc] = set()
        start_color = self.image.pixels[start_y][start_x]


        while len(will_visit) > 0:
            current_pixel = will_visit.pop()
            current_x, current_y = current_pixel
            if current_pixel in visited:
                continue
            visited.add(current_pixel)

            border_pixel = False
            for neighbor in self.neighbors(current_pixel):
                neighbor_x, neighbor_y = neighbor
                neighbor_color = self.image.pixels[neighbor_y][neighbor_x]
                if neighbor_color != start_color:
                    border_pixel = True
                else:
                    will_visit.add(neighbor)
            if border_pixel or current_x == 0 or current_y == 0 or current_x ==\
            (self.image.width - 1) or current_y == (self.image.height - 1):
                border.add(current_pixel)
        final_region: Region = {
            "color": start_color,
        "pixels": visited,
        "outline": border}
        return final_region


    def compute_all_regions(self) -> list[Region]:
        """
        Determine a list of all regions in the image. Each of the
        regions should be as large as possible, as prescribed and
        implemented by `compute_region`.

        Returns (list[Region]): the order of regions does not matter
        """
        visited_pixels: set[Loc] = set()
        all_regions: list[Region] = []

        for y in range(self.image.height):
            for x in range(self.image.width):
                current_pixel = (x, y)
                if current_pixel not in visited_pixels:
                    current_region = self.compute_region(current_pixel)
                    all_regions.append(current_region)

                    for pixel in current_region["pixels"]:
                        visited_pixels.add(pixel)

        return all_regions
