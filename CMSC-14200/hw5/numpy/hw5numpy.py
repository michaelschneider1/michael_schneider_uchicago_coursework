"""
HW5 numpy exercises (Task1 and Task2).
"""

from abc import abstractmethod, ABC
from copy import deepcopy
from typing import Any
import sys

# Task1, Task2: complete every unimplemented method in the
# classes NDArray1 and NDArray2 below


class NDArray(ABC):
    """
    Abstract class for n-dimensional arrays.
    """

    @abstractmethod
    def shape(self) -> int | tuple[int, int]:
        """
        Return the shape of the data, either an int (for 1d array)
        or pair of ints (for 2d array) in row, col order.
        """
        raise NotImplementedError("shape")

    @abstractmethod
    def values(self) -> list[int] | list[list[int]]:
        """
        Return the values (either a list or list of lists).
        """
        raise NotImplementedError("values")

    @abstractmethod
    def flatten(self) -> "NDArray1":
        """
        Flatten the data (either 1- or 2-dimensional)
        into a 1-dimensional array.
        """
        raise NotImplementedError("flatten")

    @abstractmethod
    def reshape(self, n: int, m: int) -> "NDArray2":
        """
        Reshape the data into an n x m array.

        Raises ValueError if the data does not have n * m elements,
        in which case the NDArray cannot be reshaped as such.
        """
        raise NotImplementedError("reshape")


# ====== Task1


class NDArray1(NDArray):
    """
    One-dimensional arrays of integers.
    """

    _data: list[int]
    # you can add additional attributes if you like

    def __init__(self, data: list[int]):
        """
        Construct an NDArray1 from a list of int.
        """
        self._data = deepcopy(data)

    def __pow__(self, n: int) -> "NDArray1":
        """
        Raise every item in the array to the given power.
        Produce a new array (functional style).

        Raises ValueError if n is negative.
        """
        if n < 0:
            raise ValueError("n can not be negative")
        
        new_array = []
        for num in self._data:
            new_array.append(num ** n)
        return NDArray1(new_array)

    def __neg__(self) -> "NDArray1":
        """
        Negate every item in the array.
        Produce a new array (functional style).
        """
        new_array = []
        for num in self._data:
            new_array.append(num * -1)
        return NDArray1(new_array)

    def __iadd__(self, n: int) -> "NDArray1":
        """
        Add n to all integers in the array, in place.
        Returns self.
        """
        for index, num in enumerate(self._data):
            self._data[index] = num + n
        return self

    def __isub__(self, n: int) -> "NDArray1":
        """
        Subtract n from all integers in the array, in place.
        Returns self.
        """
        for index, num in enumerate(self._data):
            self._data[index] = num - n
        return self

    def __gt__(self, other: Any) -> list[bool]:
        """
        Return a list of bools indicating greater than given int.
        """
        bool_list: list[bool] = []
        for num in self._data:
            if num > other:
                bool_list.append(True)
            else:
                bool_list.append(False)
        return bool_list

    def __contains__(self, other: Any) -> bool:
        """
        Test whether the given int is in the array.
        """
        if other in self._data:
            return True
        return False

    def __eq__(self, other: Any) -> bool:
        """
        Test whether other is an NDArray1 with the same shape and
        containing the same numbers in the same positions.
        """
        return isinstance(other, NDArray1) and self._data == other._data

    def __repr__(self) -> str:
        """
        Produce a string representation of the object.

        Note: __repr__ will not be tested or scored by us.
        It's a convenience for you during development.
        """
        return f"NDArray1: {self._data}"

    def shape(self) -> int:
        """
        see NDArray
        """
        return len(self._data)

    def values(self) -> list[int]:
        """
        see NDArray
        """
        return self._data

    def flatten(self) -> "NDArray1":
        """
        see NDArray
        """
        return self

    def reshape(self, n: int, m: int) -> "NDArray2":
        """
        see NDArray
        """
        if len(self._data) != n * m:
            raise ValueError("Can not reshape to this dimmension!")

        new_array: list[list[int]] = []
        row_num = 0
        for i in range(n):
            current_row = []
            for j in range(m):
                current_row.append(self._data[row_num])
                row_num += 1
            new_array.append(current_row)
        return NDArray2(new_array)


# ====== Task2


class NDArray2(NDArray):
    """
    Two-dimensional arrays of integers.
    """

    _data: list[list[int]]
    # you can add additional attributes if you like

    def __init__(self, data: list[list[int]]):
        """
        Construct an NDArray2 from a list of lists of int.

        Raises ValueError if list of lists is jagged.
        """
        self._data = deepcopy(data)
        row_len = len(self._data[0])
        for row in self._data:
            if len(row) != row_len:
                raise ValueError("Invalid matrix!")

    def __pow__(self, n: int) -> "NDArray2":
        """
        Raise every item in the array to the given power.
        Produce a new array (functional style).

        Raises ValueError if n is negative.
        """
        if n < 0:
            raise ValueError("n can not be negative")
        
        new_array: list[list[int]] = []
        for row in self._data:
            row_to_add = []
            for num in row:
                row_to_add.append(num ** n)
            new_array.append(row_to_add)
        return NDArray2(new_array)

    def __iadd__(self, n: int) -> "NDArray2":
        """
        Add n to all integers in the array, in place.
        Returns self.
        """
        for row_index, row in enumerate(self._data):
            for col_index, num in enumerate(row):
                self._data[row_index][col_index] = num + n
        return self

    def __isub__(self, n: int) -> "NDArray2":
        """
        Subtract n from all integers in the array, in place.
        Returns self.
        """
        for row_index, row in enumerate(self._data):
            for col_index, num in enumerate(row):
                self._data[row_index][col_index] = num - n
        return self

    def __neg__(self) -> "NDArray2":
        """
        Negate every item in the array.
        Produce a new array (functional style).
        """
        new_array: list[list[int]] = []
        for row in self._data:
            row_to_add = []
            for num in row:
                row_to_add.append(num * -1)
            new_array.append(row_to_add)
        return NDArray2(new_array)

    def __gt__(self, other: Any) -> list[list[bool]]:
        """
        Return a list of lists of bools indicating greater than given int.
        """
        bool_list: list[list[bool]] = []

        for row in self._data:
            row_to_add = []
            for num in row:
                row_to_add.append(num > other)
            bool_list.append(row_to_add)
        return bool_list

    def __contains__(self, other: Any) -> bool:
        """
        Test whether the given int is in the array.
        """
        for row in self._data:
            if other in row:
                return True
        return False

    def __eq__(self, other: Any) -> bool:
        """
        Test whether other is an NDArray2 with the same shape and
        containing the same numbers in the same positions.
        """
        return isinstance(other, NDArray2) and self._data == other._data

    def __repr__(self) -> str:
        """
        Produce a string representation of the object.

        Note: __repr__ will not be tested or scored by us.
        It's a convenience for you during development.
        """
        return f"{self._data}"

    def shape(self) -> tuple[int, int]:
        """
        see NDArray
        """
        return (len(self._data), len(self._data[0]))

    def values(self) -> list[list[int]]:
        """
        see NDArray
        """
        return self._data
        

    def flatten(self) -> "NDArray1":
        """
        see NDArray
        """
        flattened_array = []
        for row in self._data:
            for num in row:
                flattened_array.append(num)
        return NDArray1(flattened_array)

    def reshape(self, n: int, m: int) -> "NDArray2":
        """
        see NDArray
        """
        flattened_array = self.flatten().values()
        if len(flattened_array) != n * m:
            raise ValueError("Can not reshape to this dimmension!")
        
        new_array: list[list[int]] = []
        row_num = 0
        for i in range(n):
            current_row = []
            for j in range(m):
                current_row.append(flattened_array[row_num])
                row_num += 1
            new_array.append(current_row)
        return NDArray2(new_array)