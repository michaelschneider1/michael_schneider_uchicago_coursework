"""
CMSC 14200, Spring 2025
Homework #2, Task #4

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from enum import Enum
from typing import TypeAlias
from bst import BST
from task2 import BSTEmpty, BSTNode


Step = Enum("Step", ["LEFT", "RIGHT"])
Path: TypeAlias = list[Step]


def full_tree(h: int) -> BST:
    """
    Return a full binary tree of height h,
    where each node carries the value 0.

    Raises: ValueError, if h is negative
    """
    if h < 0:
        raise ValueError("full_tree: negative height")
    if h == 0:
        return BSTEmpty()
    else:
        return BSTNode(0, full_tree(h - 1), full_tree(h - 1))


def int_to_path(i: int) -> Path:
    """
    Convert a tree index to a path, denoted as a list of
    left or write steps.

    Raises: ValueError, if i is negative
    """
    if i < 0:
        raise ValueError
    backwards_path = []

    if i == 0:
        return []
    while i > 0:
        if i % 2 == 0:
            backwards_path.append(Step.RIGHT)
        else:
            backwards_path.append(Step.LEFT)
        i = (i - 1) // 2
    return backwards_path[::-1]
def trim_tree(t: BST, i: int) -> BST:
    """
    Return a tree like the given tree but where the subtree
    identified by tree index i is been removed.

    Implemented as a function rather than a method inside base BST class.
    Assumes t is BSTEmpty | BSTNode. If not, raises TypeError.

    Raises: TypeError, if t neither a BSTEmpty nor a BSTNode.

    Raises: ValueError, if i is negative
    """
    return trim_tree_path(t, int_to_path(i))


def trim_tree_path(t: BST, path: Path) -> BST:
    """
    Return a tree like the given tree but where the subtree
    identified by the given path is been removed.

    Raises: TypeError, if t neither a BSTEmpty nor a BSTNode.

    Raises: ValueError, the path is invalid (i.e., it does not
      correspond to a subtree in t)
    """
    if isinstance(t, BSTEmpty):
        raise ValueError
    if isinstance(t, BSTNode):
        if path == []:
            return BSTEmpty()
        first, *rest = path
        if first == Step.LEFT:
            new_left = trim_tree_path(t.left(), rest)
            return BSTNode(t.value(), new_left, t.right())
        elif first == Step.RIGHT:
            new_right = trim_tree_path(t.right(), rest)
            return BSTNode(t.value(), t.left(), new_right)
        else:
            raise ValueError
    else:
        raise TypeError
