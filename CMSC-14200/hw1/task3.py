"""
CMSC 14200, Spring 2025
Homework #1, Task #3

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from tree import TreeNode

def affordable_paths(t: TreeNode, budget: int) -> list[list[int]]:
    """
    Given a tree, produce a list of all root-to-node paths where the sum
    of values in the path are less than or equal to budget.

    Inputs:
        t: A tree
        budget: Maximum integer budget

    Returns: List of all root-to-leaf paths whose sum of values is
      within the budget. Each list contains the values along a path.
    """
    if t.value > budget:
        return []

    final = [[t.value]]

    for child in t.children:
        child_paths = affordable_paths(child, budget - t.value)
        for path in child_paths:
            final.append([t.value] + path)
    return final
