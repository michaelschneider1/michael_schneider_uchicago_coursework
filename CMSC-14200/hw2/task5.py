"""
CMSC 14200, Spring 2025
Homework #2, Task #5

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

import math
import sys
import pygame

from task2 import BST
import task4
from task4 import Step


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

MAX_TREE_HEIGHT = 5

NODE_RADIUS = 10
LEAF_IMG_SIZE = 30

LINE_COLOR = (255, 255, 255)
NODE_COLOR = (255, 255, 0)
ERROR = 15

class TreeTrimmer:
    """
    A GUI application for drawing and trimming full trees.

    The application starts by drawing a full binary tree of height
    `MAX_TREE_HEIGHT` (i.e. `5`). Only the structure of the tree is
    displayed, not the values.

    When the user clicks on a tree node, it is "trimmed": the visual
    effect is that the subtree rooted at that node disappears.

    When the tree becomes completely empty, the application displays
    a message urging the user to conserve trees.

    Pressing the "q" key at any time quits the application.
    """

    cell_centers: list[tuple[int, tuple[int, int]]]
    tree: BST

    surface: pygame.Surface
    clock: pygame.time.Clock

    def __init__(self) -> None:
        """Initialize the GUI application"""
        self.reset_model()
        pygame.init()
        pygame.display.set_caption("Tree Trimmer")
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.run_event_loop()

    def reset_model(self) -> None:
        """Initialize the application state"""
        self.compute_tree_paper_cell_centers()
        self.tree = task4.full_tree(MAX_TREE_HEIGHT)

    def compute_tree_paper_cell_centers(self) -> None:
        """
        Compute the center position for every cell in
        the tree paper of height `MAX_TREE_HEIGHT`. Each
        cell is identified by its integer tree index. These
        are all saved in the `self.cell_centers` attribute.
        """
        self.cell_centers = []

        total_nodes = (2 ** MAX_TREE_HEIGHT) - 1
        for index in range(total_nodes):
            path = task4.int_to_path(index)
            row = len(path)

            col = 0
            for step in path:
                col = col * 2
                if step == Step.RIGHT:
                    col += 1
            x = (col + 0.5) * self.col_width(row)
            y = (row + 0.5) * self.row_height()

            self.cell_centers.append((index, (int(x), int(y))))

    def run_event_loop(self) -> None:
        """
        Begins run_event_looop (pulint said add docstring)
        """
        while True:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONUP:
                    click_x, click_y = event.pos
                    for i, (cx, cy) in self.cell_centers:
                        if abs(click_x - cx) <= NODE_RADIUS and \
                        abs(click_y - cy) <= NODE_RADIUS:
                            try:
                                self.tree = task4.trim_tree(self.tree, i)
                            except (ValueError, TypeError):
                                pass
            self.surface.fill((0, 0, 0))
            self.draw_window()
            self.clock.tick(24)

    def draw_window(self) -> None:
        """
        Draws the window (pylint said add docstring)
        """
        self.draw_tree_paper()
        self.draw_tree_at_index(self.tree, 0)
        self.display_empty_tree_warning()
        pygame.display.update()

    def draw_tree_paper(self) -> None:
        """
        Draws blank "tree paper"" for a binary tree of height
        `MAX_TREE_HEIGHT` (i.e. 5). Visually, each row should be
        equally tall. The first row should have a single cell
        that spans the entire width of the window. The second
        row should have two equally sized cells that span the
        window. The third row should have four such cells, and
        so on.

        To achieve this visual effect, you can choose to draw
        either rectangles or line segments.

        Refer to the helper methods `row_height` and `col_width`.
        """
        for row in range(MAX_TREE_HEIGHT):
            row_height = self.row_height()
            col_width = self.col_width(row)
            lines_per_row = 2 ** row
            y_above = row * row_height
            y_under = y_above + row_height
            for col in range(lines_per_row):
                x_start = col * col_width
                x_end = x_start + col_width

                pygame.draw.line(self.surface, LINE_COLOR, (x_start, y_above), \
                (x_end, y_above))
                pygame.draw.line(self.surface, LINE_COLOR, (x_start, y_under), \
                (x_end, y_under))

                pygame.draw.line(self.surface, LINE_COLOR, (x_start, y_above), \
                (x_start, y_under))
                pygame.draw.line(self.surface, LINE_COLOR, (x_end, y_above), \
                (x_end, y_under))
    def row_height(self) -> float:
        """
        Return the size of all rows in the tree paper.
        """
        return WINDOW_HEIGHT / MAX_TREE_HEIGHT

    def col_width(self, row: int) -> float:
        """
        Return the width of each cell in the given row.
        """
        return WINDOW_HEIGHT / (2 ** row)

    def draw_tree_at_index(self, t: BST, i: int) -> None:
        """
        Draw a tree at a given tree index in the tree paper.

        If the tree is empty, nothing is drawn.
        If the tree is non-empty, a node is drawn,
        as well as branches to any non-empty children.

        Use the helper methods `draw_node_at`, `draw_line_between`,
        and `location_of_tree_index`.
        """
        if t.is_empty():
            return
        self.draw_node_at(i)

        index_left = 2 * i + 1
        index_right = 2 * i + 2

        if not t.left().is_empty():
            self.draw_line_between(i, index_left)
            self.draw_tree_at_index(t.left(), index_left)
        if not t.right().is_empty():
            self.draw_line_between(i, index_right)
            self.draw_tree_at_index(t.right(), index_right)

    def location_of_tree_index(self, i: int) -> tuple[int, int]:
        """
        Given a tree index `i`, compute the center `(cx, cy)`
        of the corresponding cell in the tree paper.
        """
        path = task4.int_to_path(i)
        row = len(path)
        col = 0

        for step in path:
            col = col * 2
            if step == Step.RIGHT:
                col += 1
        cx = (col + 0.5) * self.col_width(row)
        cy = (row + 0.5) * self.row_height()
        return (int(cx), int(cy))

    def draw_node_at(self, i: int) -> None:
        """
        Given a tree index `i`, draw a node at the center
        of the corresponding cell in the tree paper.

        Use the helper method `location_of_tree_index`.
        """
        x, y = self.location_of_tree_index(i)
        path = task4.int_to_path(i)
        t = self.tree

        for step in path:
            if step == Step.LEFT:
                t = t.left()
            else:
                t = t.right()

        if t.is_leaf():
            leaf = pygame.image.load("assets/maple-leaf.png")
            leaf_x = x - LEAF_IMG_SIZE // 2
            leaf_y = y - LEAF_IMG_SIZE // 2
            self.surface.blit(leaf, (leaf_x, leaf_y))
        else:
            pygame.draw.circle(self.surface, NODE_COLOR, (x, y), NODE_RADIUS)

    def draw_line_between(self, i: int, j: int) -> None:
        """
        Given two tree indices `i` and `j`, draw a line between
        the centers of the corresponding cells in the tree paper.

        Use the helper method `location_of_tree_index`.
        """
        xi, yi = self.location_of_tree_index(i)
        xj, yj = self.location_of_tree_index(j)

        pygame.draw.line(self.surface, LINE_COLOR, (xi, yi), (xj, yj), 2)

    def display_empty_tree_warning(self) -> None:
        """
        Display a string message somewhere in the window,
        urging the user not to trim so much next time.
        """
        msg = "Hey, be careful! That's too much trimming!"
        font = pygame.font.Font("assets/initial.ttf", 24)
        text_image = font.render(msg, True, (255, 255, 255))
        if self.tree.is_empty():
            x = 30
            y = self.row_height() // 2
            self.surface.blit(text_image, (x, y))

if __name__ == "__main__":
    TreeTrimmer()
