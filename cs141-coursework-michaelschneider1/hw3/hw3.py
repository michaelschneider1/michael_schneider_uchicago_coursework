"""
CMSC 14100
Winter 2025
Homework #3

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

##################################################
#                                                #
# Important note: some of the tasks in this      #
#  assignment have task-specific                 #
#  reqirements/restrictions concerning           #
#  the language constructs that you are          #
#  allowed to use in your solution.  See the     #
#  assignment writeup for details.               #
#                                                #
##################################################

# Some useful constants
NORMAL = 0
PREDIABETES = 1
DIABETES = 2
NEITHER = -1

#Modified 2, 3, 6, and 9 to call previous functions to avoid repeated code
#Modified 1, 2, 3, 9 to utilize defined constants
#Changed for loops to not go through the index if not needed
#Changed several variable names for clarity
#Added blank lines for visual appeal
#Added doc strings for all excersices
#For 3, I used reversed() to get rid of the unnecessary code (line 117)
#For 5, Instead of doing and if tree for each violation, I assigned points to
#each violation, then multiplied based on location
#For 6, I unpacked the tuple to make the for loop simplified (line 211)
#For 8, I removed a previous variable "scaler" to shorten code (line 267)
#For 9, I used enumerate for the for loop to simplify code (line 283)

# Exercise 1
def categorize_a1c(a1c):
    """
    Given the A1C concentration, categorize the A1C concentration
    according to the following table:

    A1C Category          A1C Range
    NORMAL                Below 5.7%
    PREDIABETES           5.7% to below 6.5%
    DIABETES              6.5% and above

    Args:
        a1c (float): the A1C concentration

    Returns (int): the category of the A1C concentration
    """
    if a1c < 5.7:
        return NORMAL 
    elif a1c < 6.5:
        return PREDIABETES 
    else:
        return DIABETES

# Exercise 2
def which_comes_first(scores):
    """
    Given a list of A1C concentrations, go through the list. Once the first 
    value that is not in the normal range is listed, return the categorey of 
    that value. If all values in list are normal, return normal.

    A1C Category          A1C Range
    NORMAL                Below 5.7%
    PREDIABETES           5.7% to below 6.5%
    DIABETES              6.5% and above

    Args: 
        which_comes_first(scores): list of A1C concentration values
    Returns (int): category of the first non-normal value. If all values are in
    normal range, return normal.
    Will return 2 if returning diabetes, 1 if returning prediabetes, and -1 if
    returning normal
    """
    for val in scores: 
        if categorize_a1c(val) != NORMAL: 
            return categorize_a1c(val)
    return NEITHER 

# Exercise 3
def which_comes_last(scores):
    """
    Given a list of A1C concentrations, go through the list backwards. Once the 
    first value (from the back) that is not in the normal range is listed, 
    return the categorey of that value. If all values in list are normal, 
    return normal.

    A1C Category          A1C Range
    NORMAL                Below 5.7%
    PREDIABETES           5.7% to below 6.5%
    DIABETES              6.5% and above

    Args: 
        which_comes_last(scores): list of A1C concentration values
    Returns (int): category of the first (from the back) non-normal value. 
    If all values are in
    normal range, return normal.
    Will return 2 if returning diabetes, 1 if returning prediabetes, and -1 if
    returning normal
    """
    for score in reversed(scores): 
        if categorize_a1c(score) != NORMAL: 
            return categorize_a1c(score) 
    return NEITHER 

# Exercise 4
def is_multiples_of_first(scores):
    """
    Given a list scores (of ints), it will take the first value of the list and 
    check to see if all values in the list are multiples of the first value. If
    they are, return True. Else return False
    
    Input:
        scores (list[int]): list of integers
    Output (bool):
        True, if all ints in list are multiples of the first value. False
        otherwise
    """
    if scores == []:
        return False
    first_value = scores[0]
    for num in scores: 
        if (num % first_value) != 0:
            return False
    return True

# Exercise 5
def violation_points(violation_type, location):
    """
    Takes a violation_type (str) and location (str). Assigns points (int) 
    based on violation type. Based on location, will multiply the points. 
    Return points after multiplier is applied.

    violation types:
    "RECKLESS DRIVING" is 20 points
    "SPEEDING" is 10 points
    "PARKING" is 5 points

    location multipliers:
    "CONSTRUCTION" multiplies points by 3
    "SCHOOL" multiplies points by 2
    Other locations multiplies points by 1

    Input:
        violation_type(str): the name of the violation commited
        location(str): the location of the violation
    Output:
        points (int): total poitns based on violation_type and location
    """

    if violation_type == "RECKLESS DRIVING":
        points = 20
    elif violation_type == "SPEEDING":
        points = 10
    else:
        points = 5

    if location == "CONSTRUCTION":
        return points * 3
    elif location == "SCHOOL":
        return points * 2
    else:
        return points


#Exercise 6
def is_suspended(violations, driver_age):
    """
    Takes in a list of (violation_type, location) and calculates total points of
    the violations commited. Based on total points, determines whether license 
    is suspended. Based on age, those under 25 can have up to 25 total points 
    before being suspened. Ages 25 and up can have up to 30 points before
    suspenision. If suspended, function will return True. Otherwise, return
    False.

    violation types:
    "RECKLESS DRIVING" is 20 points
    "SPEEDING" is 10 points
    "PARKING" is 5 points

    location multipliers:
    "CONSTRUCTION" multiplies points by 3
    "SCHOOL" multiplies points by 2
    Other locations multiplies points by 1

    Input:
        violations(list(violation_type, location)): list of tuples that contain
        violation_type and location
        driver_age: age of driver
    Output (bool):
        True if license should be suspended. False otherwise.
    """
    total_points = 0

    for violation_type, location in violations: 
        total_points += violation_points(violation_type, location)

    if driver_age < 25:
        if total_points > 25:
            return True
    else:
        if total_points > 30:
            return True
    return False

# Exercise 7
def valid_grades(grades):
    """
    Takes a list of grades (ints). Goes through each grade. If all grades are 
    valid grades then returns true, returns false otherwise. A valid score is a 
    int that is in the range of -5 to 5, inclusive of -5 and 5. 

    Input:
        grades(list(int)): list of ints 
    Output (bool):
        True if all grades are valid grades, False otherwise.
    """
    if grades == []:
        return True 
    
    for score in grades: 
        if -5 > score or score > 5:
            return False
    return True

# Exercise 8
def technical_element_score(base_value, grades):
    """
    Computes a technical element score based on a list of grades and the given
    base value score.

    Input:
        base_value (float): base value score given
        grades(list[float]): list of judge's scores
    Output:
        final score (float): technical element score computed
    """

    numerator = 0
    current_small = 5
    current_big = -5 

    for score in grades:
        numerator = numerator + score
        if current_small >= score:
            current_small = score
        if current_big <= score:
            current_big = score 
    
    average = (numerator - current_big - current_small) / (len(grades) - 2)
    goe = (base_value * .1) * average 
    return goe + base_value

# Exercise 9
# Restriction: you may not use the index method in your solution for this task.
def get_first_non_normal(scores):
    """
    Goes through a list of a1c scores. Returns the index of the first non 
    normal score. If allo scores are normal, returns None.

    Input:
        scores(list[float]): list of A1C concentration values
    Output(int):
        index of the first non normal score. Returns None otherwise.
    """

    for index, score in enumerate(scores): 
        if categorize_a1c(score) != NORMAL: 
            return index
    return None
