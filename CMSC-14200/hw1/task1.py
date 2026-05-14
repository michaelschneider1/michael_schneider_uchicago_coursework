"""
CMSC 14200, Spring 2025
Homework #1, Task #1

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""


def digits_of_int(n: int) -> list[int]:
    """Compute the list of digits of a non-negative integer."""
    if n < 10:
        return [n]
    return digits_of_int(n // 10) + [(n % 10)]

def helper(n: int) -> tuple[int, int]:
    """
    Takes an integer and returns a tuple that contains the additive persistence
    and digital root, where the first value of the tuple is the additive 
    persistence and the second the digital root
    Input:
    n(int): integer of interest
    Output (tuple[int, int]): returns a tuple of two ints, the first being the 
    additive persistence, second the digital root
    """
    if n < 10:
        return (0, n)
    added_digits = sum(digits_of_int(n))
    counter = 1
    while added_digits >= 10:
        added_digits = sum(digits_of_int(added_digits))
        counter += 1
    return (counter, added_digits)

def additive_persistence(n: int) -> int:
    """Compute the additive persistence of a non-negative integer."""
    addit_persis, _ = helper(n)
    return addit_persis

def digital_root(n: int) -> int:
    """computes the digital root of a non-negative integer."""
    _, dig_root = helper(n)
    return dig_root

def digital_roots(start: int, end: int) -> dict[int, list[int]]:
    """
    Compute the digital roots of all numbers starting from start
    to end (both inclusive), and group the numbers in this range
    based on their digital root.

    For example, the resulting dictionary will map the digit 3 to
    the list of numbers in the input range whose digital root is 3.
    The numbers in each list should appear in increasing order.

    Inputs:
      start: An int
      end: An int

    Returns: A dictionary mapping each digit i to the list of
    numbers in the input range whose digital root is i.
    """
    final_dict: dict[int, list[int]] = {0: [], 1: [], 2: [], 3: [], 4: [], 5: \
    [], 6: [], 7: [], 8: [], 9: []}

    for num in range(start, end + 1):
        nums_dig_root = digital_root(num)
        final_dict[nums_dig_root].append(num)
    return final_dict
