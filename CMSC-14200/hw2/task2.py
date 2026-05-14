"""
CMSC 14200, Spring 2025
Homework #2, Task #2

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from abc import abstractmethod
from bst import BST

import task1


class BSTEmpty(BST):
    """
    Class to represent an empty BST.
    """

    # No constructor needed

    def is_empty(self) -> bool:
        """See BST"""
        return True

    def is_leaf(self) -> bool:
        """See BST"""
        return False

    def value(self) -> int:
        """See BST"""
        raise TypeError

    def left(self) -> BST:
        """See BST"""
        raise TypeError

    def right(self) -> BST:
        """See BST"""
        raise TypeError

    def elements(self) -> list[int]:
        """See BST"""
        return []

    def contains(self, n: int) -> bool:
        """See BST"""
        return False

    def insert(self, n: int) -> "BSTNode":
        """See BST"""
        return BSTNode(n, BSTEmpty(), BSTEmpty())

    def num_nodes(self) -> int:
        """See BST"""
        return 0

    def height(self) -> int:
        """See BST"""
        return 0

    def min(self) -> int:
        """See BST"""
        raise TypeError

    def max(self) -> int:
        """See BST"""
        raise TypeError

    def mean(self) -> float:
        """See BST"""
        raise TypeError

    def median(self) -> float:
        """See BST"""
        raise TypeError

class BSTNode(BST):
    """
    Class to represent a node in a BST.
    """

    _value: int
    _left: BST
    _right: BST

    def __init__(self, n: int, left: BST, right: BST):
        """
        Constructor

        Inputs:
            n (int): the value at this node
            left (BST): the left child
            right (BST): the right child
        """
        self._value = n
        self._left = left
        self._right = right

    def is_empty(self) -> bool:
        """See BST"""
        return False

    def is_leaf(self) -> bool:
        """See BST"""
        return self._left.is_empty() and self._right.is_empty()

    def value(self) -> int:
        """See BST"""
        return self._value

    def left(self) -> BST:
        """See BST"""
        return self._left

    def right(self) -> BST:
        """See BST"""
        return self._right

    def num_nodes(self) -> int:
        """See BST"""
        return 1 + self._left.num_nodes() + self._right.num_nodes()

    def height(self) -> int:
        """See BST"""
        return 1 + max(self._left.height(), self._right.height())

    def elements(self) -> list[int]:
        """See BST"""
        return self._left.elements() + [self._value] + self._right.elements()

    def contains(self, n: int) -> bool:
        """See BST"""
        if n < self._value:
            return self._left.contains(n)
        elif n > self._value:
            return self._right.contains(n)
        else:
            return True

    def insert(self, n: int) -> "BSTNode":
        """See BST"""
        if n < self._value:
            return BSTNode(self._value, self._left.insert(n), self._right)
        elif n > self._value:
            return BSTNode(self._value, self._left, self._right.insert(n))
        else:
            return self

    def min(self) -> int:
        """
        Implements BST.min, exploiting BST ordering property for efficiency.
        """
        if self._left.is_empty():
            return self._value
        else:
            return self._left.min()

    def max(self) -> int:
        """
        Implements BST.max, exploiting BST ordering property for efficiency.
        """
        if self._right.is_empty():
            return self._value
        else:
            return self._right.max()

    def mean(self) -> float:
        """See BST"""
        return task1.mean(self.elements())

    def median(self) -> float:
        """See BST"""
        return task1.median(self.elements())
