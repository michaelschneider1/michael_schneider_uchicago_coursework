#
# Base Tree class
#
# DO NOT MODIFY THIS FILE
#

from abc import ABC, abstractmethod


class BST(ABC):

    @abstractmethod
    def is_empty(self) -> bool:
        """Check whether the tree is empty"""
        raise NotImplementedError

    @abstractmethod
    def is_leaf(self) -> bool:
        """Check whether the tree is a single node (with no children)"""
        raise NotImplementedError

    @abstractmethod
    def value(self) -> int:
        """
        Return the value at the root of this tree (if any)

        Raises: TypeError, if called on an empty tree
        """
        raise NotImplementedError

    @abstractmethod
    def left(self) -> "BST":
        """
        Get the left child of the given tree.

        Returns (BST): the left child

        Raises: TypeError, if called on an empty tree
        """
        raise NotImplementedError

    @abstractmethod
    def right(self) -> "BST":
        """
        Get the right child of the given tree.

        Returns (BST): the right child

        Raises: TypeError, if called on an empty tree
        """
        raise NotImplementedError

    @abstractmethod
    def elements(self) -> list[int]:
        """
        Return a list of all values stored in the tree,
        according to an in-order traversal. Because this is
        a binary search tree, this in-order traversal will
        return a sorted list.
        """
        raise NotImplementedError

    ### MAIN BST OPERATIONS ###

    @abstractmethod
    def contains(self, n: int) -> bool:
        """
        Determine if a value is in the tree.

        Inputs:
            n (int): the sought-for value

        Returns (bool): True if the value is present, otherwise False
        """
        raise NotImplementedError

    @abstractmethod
    def insert(self, n: int) -> "BST":
        """
        Add a value to the tree and return the new tree.
        The original tree is returned if the value is already present.

        Inputs:
            n (int): the value to add

        Returns (BST): the tree with the value added
        """
        raise NotImplementedError

    ### BASIC STATS ###

    @abstractmethod
    def num_nodes(self) -> int:
        """
        Get the number of nodes in the given tree.

        Returns (int): the number of nodes
        """
        raise NotImplementedError

    @abstractmethod
    def height(self) -> int:
        """
        Get the height of the given tree.

        Returns (int): the height
        """
        raise NotImplementedError

    @abstractmethod
    def min(self) -> int:
        """Get the minimum value in the tree"""
        raise NotImplementedError

    @abstractmethod
    def max(self) -> int:
        """Get the maximum value in the tree"""
        raise NotImplementedError

    @abstractmethod
    def mean(self) -> float:
        """Get the average (mean) of all values in the tree"""
        raise NotImplementedError

    @abstractmethod
    def median(self) -> float:
        """
        Get the median of all values in the tree. If there is
        an even number of values, return the average of the
        two middle elements.
        """
        raise NotImplementedError
