"""
CMSC 14200, Spring 2025
Homework #2, Task 4B

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

import pytest
import task4
from task2 import BSTNode, BSTEmpty
from task4 import Step

def test_task4_int_to_path() -> None:
    """
    Check that int_to_path computes the correct paths for
    the first ten indices, 0 through 9.
    """
    print(task4.int_to_path(0))
    assert not task4.int_to_path(0)
    assert task4.int_to_path(1) == [Step.LEFT]
    assert task4.int_to_path(2) == [Step.RIGHT]
    assert task4.int_to_path(3) == [Step.LEFT, Step.LEFT]
    assert task4.int_to_path(4) == [Step.LEFT, Step.RIGHT]
    assert task4.int_to_path(5) == [Step.RIGHT, Step.LEFT]
    assert task4.int_to_path(6) == [Step.RIGHT, Step.RIGHT]
    assert task4.int_to_path(7) == [Step.LEFT, Step.LEFT, Step.LEFT]
    assert task4.int_to_path(8) == [Step.LEFT, Step.LEFT, Step.RIGHT]
    assert task4.int_to_path(9) == [Step.LEFT, Step.RIGHT, Step.LEFT]

def test_task4_trim_tree_at_index_0() -> None:
    """
    Create a full tree of height 3, and then trim at index 0.
    Check that the resulting tree is empty.
    """
    tree = task4.full_tree(3)
    new_tree = task4.trim_tree(tree, 0)
    assert isinstance(new_tree, BSTEmpty)


def test_task4_trim_tree_at_index_2() -> None:
    """
    Create a full tree of height 3, and then trim at index 2.
    Check that the resulting tree has four nodes, that it has
    two leaf nodes (that is, with zero children) in the expected
    places, and that it has no right subtree.
    """
    tree = task4.full_tree(3)
    new_tree = task4.trim_tree(tree, 2)
    assert new_tree.num_nodes() == 4
    assert new_tree.right().is_empty()
    assert not new_tree.left().is_empty()
    assert new_tree.left().left().is_leaf()
    assert new_tree.left().right().is_leaf()

def test_task4_trim_tree_at_index_4() -> None:
    """
    Create a full tree of height 3, and then trim at index 4.
    Check that the resulting tree has six nodes, that it has
    three leaf nodes (that is, with zero children) in the expected
    places, and that it has one node with exactly one child
    (a left child) in the expected place.
    """
    tree = task4.full_tree(3)
    new_tree = task4.trim_tree(tree, 4)
    assert new_tree.num_nodes() == 6
    assert not new_tree.left().is_empty()
    assert not new_tree.right().is_empty()
    assert not new_tree.left().left().is_empty()
    assert new_tree.left().right().is_empty()
    assert new_tree.right().left().is_leaf()
    assert new_tree.right().right().is_leaf()

def test_task4_trim_tree_at_index_6() -> None:
    """
    Create a full tree of height 3, and then trim at index 6.
    Check that the resulting tree has six nodes, that it has
    three leaf nodes (that is, with zero children) in the expected
    places, and that it has one node with exactly one child
    (a left child) in the expected place.
    """
    tree = task4.full_tree(3)
    new_tree = task4.trim_tree(tree, 6)
    assert new_tree.num_nodes() == 6
    assert not new_tree.left().is_empty()
    assert not new_tree.right().is_empty()
    assert new_tree.left().left().is_leaf()
    assert new_tree.left().right().is_leaf()
    assert new_tree.right().left().is_leaf()
    assert new_tree.right().right().is_empty()

def test_task4_trim_tree_at_index_7() -> None:
    """
    Create a full tree of height 3, and then trim at index 7.
    Check that this operation raises a ValueError.
    """
    tree = task4.full_tree(3)
    with pytest.raises(ValueError):
        task4.trim_tree(tree, 7)
