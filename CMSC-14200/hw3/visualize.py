"""
CMSC 14200, Spring 2025
Homework #3
"""

import os
import sys
import math


os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from image import Image, Loc
from graph import ImageGraph


def augment(locs: set[Loc], expand: int) -> set[Loc]:
    """
    Augment a border to make it more visible.

    Inputs:
        locs (set[Loc]): the points in the border
        expand (int): amount by which to expand

    Returns (set[Loc]): augmented border
    """
    rv = set()
    for x, y in locs:
        for dx in range(-expand, expand + 1):
            for dy in range(-expand, expand + 1):
                rv.add((x + dx, y + dy))
    return rv


class Visualize:
    """
    Class for a GUI-based image viewer that allows regions of the
    same color to be identified and outlined.
    """

    _image: Image
    _graph: ImageGraph | None
    _zoom: int
    _expand: int
    _duration: int
    _highlighted: set[Loc]
    _counter: int

    _surface: pygame.surface.Surface
    _clock: pygame.time.Clock

    def __init__(
        self, image: Image, zoom: int = 1, expand: int = 0, duration: int = 12
    ):
        """
        Constructor

        Inputs:
            image (Image): the image to display and analyze
            zoom (int): how many pixels to use on screen per image pixel
            expand (int): by how many pixels to expand the highlight
            duration (int): number of frames per animation cycle
        """
        self._image = image
        self._graph = None
        self._zoom = zoom
        self._expand = expand
        self._duration = duration
        self._highlighted = set()
        self._counter = 0

        # Initialize Pygame surface, clock, and event loop
        pygame.init()
        pygame.display.set_caption("Visualize")
        self._surface = pygame.display.set_mode(
            (self._zoom * self._image.width, self._zoom * self._image.height)
        )
        self._clock = pygame.time.Clock()
        self._event_loop()

    def _draw_window(self) -> None:
        """Draw window"""
        for y, row in enumerate(self._image.pixels):
            for x, color in enumerate(row):
                rect = (x * self._zoom, y * self._zoom, self._zoom, self._zoom)
                if (x, y) in self._highlighted:
                    if self._counter < self._duration / 2:
                        color = (255, 255, 255)
                    else:
                        color = (0, 0, 0)
                pygame.draw.rect(self._surface, color, rect)

        self._counter = (self._counter + 1) % self._duration

    def _event_loop(self) -> None:
        """Handle user interactions"""
        while True:
            # Process Pygame events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    px, py = x // self._zoom, y // self._zoom
                    if self._graph is None:
                        self._graph = ImageGraph(self._image)
                    region = self._graph.compute_region((px, py))
                    self._highlighted = augment(region["outline"], self._expand)

            # Update the display
            self._draw_window()
            pygame.display.update()
            self._clock.tick(24)


if __name__ == "__main__":
    image = Image(sys.argv[1])
    zoom = int(sys.argv[2])
    expand = int(sys.argv[3])
    Visualize(image, zoom, expand)
