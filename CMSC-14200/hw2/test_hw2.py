"""
CMSC 14200, Spring 2025, Tests for Homework #2
"""

import pytest
from bst import BST
import task1
import task2
import task3


### TASK 1 TESTS ###


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([1], 1),
        ([1, 2], 1.5),
        ([1, 2, 3], 2),
        ([1, 2, 141, 14200, 14300], 5728.8),
        (range(1, 101), 50.5),
    ],
)
def test_task1_mean(nums: list[int], expected: float) -> None:
    # Being careful when picking test cases,
    # because equality on floats can be brittle
    assert task1.mean(nums) == expected


def check_unmodified(list1: list[int], list2: list[int]) -> None:
    """Check that two lists are the same, one-level deep"""
    assert list1 == list2
    n = len(list1)
    assert n == len(list2)
    for i in range(n):
        assert list1[i] == list2[i], "Input list should not be modified"


def check_median(nums: list[int], expected: float) -> None:
    """Check result of median, and that the input list is not modified"""
    original_nums = nums.copy()
    assert task1.median(nums) == expected
    check_unmodified(nums, original_nums)


def check_mode(nums: list[int], expected: float) -> None:
    """Check result of mode, and that the input list is not modified"""
    original_nums = nums.copy()
    actual = task1.mode(nums)
    actual.sort()
    assert actual == expected
    check_unmodified(nums, original_nums)


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([1, 20, 300], 20),
        ([1, 20, 300, 4000], 160),
    ],
)
def test_task1_median(nums: list[int], expected: float) -> None:
    """For these median tests, the input lists are in sorted in order"""
    check_median(nums, expected)


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([1, 300, 20], 20),
        ([1, 20, 4000, 300], 160),
    ],
)
def test_task1_median_unsorted(nums: list[int], expected: float) -> None:
    """For these median tests, the input lists are _not_ in sorted in order"""
    check_median(nums, expected)


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([0, 0, 1, 2, 4], [0]),
        ([1, 2, 4], [1, 2, 4]),
        ([], []),
    ],
)
def test_task1_mode(nums: list[int], expected: float) -> None:
    """For these mode tests, the input lists are in sorted in order"""
    check_mode(nums, expected)


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([1, 4, 2, 0, 0], [0]),
        ([1, 4, 2], [1, 2, 4]),
        ([], []),
    ],
)
def test_task1_mode_unsorted(nums: list[int], expected: float) -> None:
    """For these mode tests, the input lists are _not_ in sorted in order"""
    check_mode(nums, expected)


def test_task1_mean_empty_list() -> None:
    with pytest.raises(ValueError):
        task1.mean([])


def test_task1_median_empty_list() -> None:
    with pytest.raises(ValueError):
        task1.median([])


### HELPERS FOR TESTING TASKS 2 AND 3 TESTS ###

# To test Task 2, pass in task2.BSTEmpty() for empty_tree parameter.
# To test Task 3, pass in task3.BSTEmpty() for empty_tree parameter.

# This works because, in the BSTEmpty class in task2.py the insert method
# produces BSTNode nodes, and in the BSTEmptyclass in task3.py the insert
# method produces BSTNodeOpt nodes.


def make_balanced_tree(empty_tree: BST) -> BST:
    """
    Make a perfectly balanced BST with integer values 1 through 7.

          4
        /   \\
      2       6
     / \\     / \\
    1   3   5   7
    """
    t = empty_tree
    for v in [4, 2, 1, 3, 6, 5, 7]:
        t = t.insert(v)
    return t


def tasks_2_and_3_balanced_tree(empty_tree: BST) -> None:
    t = make_balanced_tree(empty_tree)
    assert t.num_nodes() == 7
    assert t.height() == 3
    assert t.elements() == [1, 2, 3, 4, 5, 6, 7]
    assert t.min() == 1
    assert t.max() == 7
    assert t.mean() == 4
    assert t.median() == 4


def tasks_2_and_3_balanced_tree_node_2(empty_tree: BST) -> None:
    t = make_balanced_tree(empty_tree)
    t2 = t.left()
    assert t2.num_nodes() == 3
    assert t2.height() == 2
    assert t2.elements() == [1, 2, 3]
    assert t2.min() == 1
    assert t2.max() == 3
    assert t2.mean() == 2
    assert t2.median() == 2


def tasks_2_and_3_balanced_tree_node_6(empty_tree: BST) -> None:
    t = make_balanced_tree(empty_tree)
    t6 = t.right()
    assert t6.num_nodes() == 3
    assert t6.height() == 2
    assert t6.elements() == [5, 6, 7]
    assert t6.min() == 5
    assert t6.max() == 7
    assert t6.mean() == 6
    assert t6.median() == 6


def make_crooked_right_tree() -> BST:
    """
    Make a BST that has a single, right-only path
    with integer values 1 through 7.

    1
     \\
      2
       \\
        3
         \\
         ...
    """
    t: BST = task2.BSTEmpty()
    for v in range(1, 8):
        t = t.insert(v)
    return t


def test_task2_crooked_right_tree() -> None:
    t = make_crooked_right_tree()
    assert t.num_nodes() == 7
    assert t.height() == 7
    assert t.elements() == [1, 2, 3, 4, 5, 6, 7]
    assert t.min() == 1
    assert t.max() == 7
    assert t.mean() == 4
    assert t.median() == 4


def test_task2_crooked_right_tree_node_2() -> None:
    t = make_crooked_right_tree()
    t2 = t.right()
    assert t2.num_nodes() == 6
    assert t2.height() == 6
    assert t2.elements() == [2, 3, 4, 5, 6, 7]
    assert t2.min() == 2
    assert t2.max() == 7
    assert t2.mean() == 4.5
    assert t2.median() == 4.5


def test_task2_crooked_right_tree_node_6() -> None:
    t = make_crooked_right_tree()
    t6 = t.right().right().right().right().right()
    assert t6.num_nodes() == 2
    assert t6.height() == 2
    assert t6.elements() == [6, 7]
    assert t6.min() == 6
    assert t6.max() == 7
    assert t6.mean() == 6.5
    assert t6.median() == 6.5


### TASK 2 TESTS ###


def test_task2_balanced_tree() -> None:
    tasks_2_and_3_balanced_tree(task2.BSTEmpty())


def test_task2_balanced_tree_node_2() -> None:
    tasks_2_and_3_balanced_tree_node_2(task2.BSTEmpty())


def test_task2_balanced_tree_node_6() -> None:
    tasks_2_and_3_balanced_tree_node_6(task2.BSTEmpty())


### TASK 3 TESTS ###


def test_task3_balanced_tree() -> None:
    tasks_2_and_3_balanced_tree(task3.BSTEmpty())


def test_task3_balanced_tree_node_2() -> None:
    tasks_2_and_3_balanced_tree_node_2(task3.BSTEmpty())


def test_task3_balanced_tree_node_6() -> None:
    tasks_2_and_3_balanced_tree_node_6(task3.BSTEmpty())
