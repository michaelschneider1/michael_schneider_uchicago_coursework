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

from typing import TypeAlias

Loc: TypeAlias = tuple[int, int]
Color: TypeAlias = tuple[int, int, int]

class Image:
    """
    Class for a bitmap image
    """

    width: int
    height: int
    pixels: list[list[Color]]
    def __init__(self, filename: str):
        """
        Constructor

        Inputs:
            filename (str): path to a PPM file
        """
        self.filename = filename
        with open(filename, "r") as file:
            assert file.readline().strip() == "P3"

            w, h = file.readline().split()
            self.width = int(w)
            self.height = int(h)

            file.readline()

            pixels_in_order: list[Color] = []
            for _ in range(self.width * self.height):
                r, g, b = map(int, file.readline().split())
                pixels_in_order.append((r, g, b))

            self.pixels =[]
            for row in range(self.height):
                start_index = row * self.width
                end_index = start_index + self.width

                self.pixels.append(pixels_in_order[start_index: end_index])
