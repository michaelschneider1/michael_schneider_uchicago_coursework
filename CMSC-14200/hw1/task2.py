"""
CMSC 14200, Spring 2025
Homework #1, Task #2

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

def subsequences(ints: list[int]) -> list[list[int]]:
    """
    Given a list, produce all subsequences, including the empty and
    full subsequences. Subsequences can appear in any order in the
    result. You can assume the input list does not contain duplicates.

    Inputs:
        ints: List of integers

    Returns: List of all subsequences of the input
    """
    if len(ints) == 0:
        return [[]]
    first, *rest = ints
    smaller_subsequences = subsequences(rest)

    new_subsequences = []
    for num in smaller_subsequences:
        new_subsequences.append([first] + num)
    return smaller_subsequences + new_subsequences
