"""
CMSC 14200, Spring 2025
Homework #2, Task #1

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""


def mean(nums: list[int]) -> float:
    """
    Compute the mean (average) of a list of integers.

    Raises: ValueError, if the list is empty
    """
    if nums == []:
        raise ValueError
    return (sum(nums) / len(nums))


def median(nums: list[int]) -> float:
    """
    Compute the median of a list of integers.

    Inputs:
        nums (list[int]): Not necessarily in sorted order

    Returns (float): The middlemost element. If the list has even length,
        the result is the average of the two middlemost elements.

    Raises: ValueError, if the list is empty
    """
    if nums == []:
        raise ValueError

    nums = sorted(nums)
    if len(nums) == 1:
        return nums[0]
    elif len(nums) == 2:
        return (nums[0] + nums[1]) / 2
    else:
        return median(nums[1:len(nums) - 1])

def mode(nums: list[int]) -> list[int]:
    """
    Compute the mode(s) of a list of integers.

    Inputs:
        nums (list[int]): Not necessarily in sorted order

    Returns (float): The most common element(s)
    """
    frequency: dict[int, int] = {}
    if nums == []:
        return []
    for num in nums:
        if num in frequency:
            frequency[num] += 1
        else:
            frequency[num] = 1
    max_frequency = max(frequency.values())
    return_list = []
    for num, occurences in frequency.items():
        if occurences == max_frequency:
            return_list.append(num)
    return return_list
