"""
CMSC 14100
Winter 2025
Homework #5

We will be using anonymous grading, so please do NOT include your name
in this file

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URL of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from math import log

# Exercise 1
def extract_column(table, column):
    """
    Produce a list of values in the given column from the given table.

    Input:
        table (list[list]): table of data
        column (str): name of column

    Output (list): list of column data
    """
    final_list = []
    for index, which_column in enumerate(table[0]):
        if which_column == column:
            column_index = index
    for row in table:
        final_list.append(row[column_index])
    final_list.remove(column)
    return final_list
# Exercise 2
def is_valid_table(table):
    """
    Check whether the table is a valid table.

    Input:
        table (list[list]): table of data

    Output (bool): True if table is valid, False otherwise
    """
    seen = []
    for row_one_value in table[0]:
        if isinstance(row_one_value, str) == False:
            return False
        if row_one_value in seen:
            return False
        seen.append(row_one_value)
    for row in table:
        if len(row) != len(table[0]):
            return False
    for column_index in range(len(table[0])):
        column_type = type(table[1][column_index])
        for row in table[1:]:
            if type(row[column_index]) != column_type:
                return False
    return True
# Exercise 3
def filter_exact(table, column, value, negate=False):
    """
    Produce a new table that consists of the rows that
    * contain value in column, if negate is False.
    * do not contain value in column, if negate is True.

    negate is False by default.

    Input:
        table (list[list]): table of data
        column (str): column name
        value (any): value to be matched
        negate (bool): negate match if True (False by default)

    Output (list[list]): table of rows with value in column
    """
    assert is_valid_table(table) is True
    final_list = [table[0]]
    column_index = table[0].index(column)
    for row in table[1:]:
        if negate == False:
            if value == row[column_index]:
                final_list.append(row)
        else:
            if value != row[column_index]:
                final_list.append(row)
    return final_list
# Exercise 4
def select_columns(table, columns):
    """
    Produce a new table that consists of the given columns from the given table.

    Input:
        table (list[list]): table of data
        columns (list[str]): list of column names

    Output (list[list]): new table with given columns
    """
    assert is_valid_table(table) is True
    final_list = [columns]
    wanted_indexes = []
    for title in columns:
        for index, header in enumerate(table[0]):
            if title == header:
                wanted_indexes.append(index)
    for row in table[1:]:
        temp_list = []
        for i in wanted_indexes:
            temp_list.append(row[i])
        final_list.append(temp_list)
    return final_list
# Exercise 5
def add_row_sum_column(table, columns, name):
    """
    Extend the table with a new column with given name that contains the sum
    of the values in the specified columns for each row.

    Input:
        table (list[list]): table of data
        column (list[str]): list of column names
        name (str): name of new column

    Output (None): None, mutates table
    """
    assert is_valid_table(table) is True
    list_of_intrests = select_columns(table, columns)
    list_of_intrests.pop(0)
    table[0].append(name)
    sums_list = []
    for value in list_of_intrests:
        sum = 0
        for num in value:
            sum += num
        sums_list.append(sum)
    
    for index, row in enumerate(table[1:]):
        row.append(sums_list[index])
# Exercise 6
def add_running_mean_column(table, column, name):
    """
    Extend the table with a new column with given name that contains the 
    running mean of the values in the specified column. The running mean is the
    mean of the values in the column of the current and previous rows.

    Input:
        table (list[list]): table of data
        column (str): column name
        name (str): name of new column

    Output (None): None, mutates table
    """
    assert is_valid_table(table) is True
    table[0].append(name)
    for index, value in enumerate(table[0]):
        if value == column:
            col_index = index
    numerator = 0
    denominator = 0
    for row in table[1:]:
        numerator += row[col_index]
        denominator += 1
        row.append(numerator / denominator)
# Exercise 7
def add_difference_column(table, column, name, start_from=0):
    """
    Extend the table with a new column with given name that contains the 
    difference of the value in the column of the current row with the value of
    the value in the row above in the same column.

    Input:
        table (list[list]): table of data
        column (str): column name
        name (str): name of new column
        start_from (float): initial value

    Output (None): None, mutates table
    """
    assert is_valid_table(table) is True
    table[0].append(name)
    for index, value in enumerate(table[0]):
        if value == column:
            col_index = index
    for row in table[1:]:
        if row == table[1]:
            row.append(row[col_index] - start_from)
            new_diff = row[col_index]
        else:
            row.append(row[col_index] - new_diff)
            new_diff = row[col_index]
# Exercise 8
def inverse_document_frequency(table):
    """
    Given a document-term matrix as a table, compute the inverse document 
    frequency (idf) of the terms, relative to the table.

    Input:
        table (list[list]): table representing the document-term matrix

    Output (list[tuple[str,float]]): list of (term, idf) pairs
    """
    assert is_valid_table(table) is True
    word_list = table[0]
    k_list =[0] * len(table[1])
    num_documents = 0
    for row in table[1:]:
        for index, num in enumerate(row):
            if num != 0:
                k_list[index] += 1
        num_documents += 1
    final_list = []
    for index, k in enumerate(k_list):
        final_list.append((word_list[index], log(num_documents / k, 10)))
    return final_list