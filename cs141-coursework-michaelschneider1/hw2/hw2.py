"""
CMSC 14100
Winter 2025
Homework #2

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

#############################################################################
#                                                                           #
# Important note: some of the tasks in this assignment have task-specific   #
# requirements/restrictions concerning the language constructs that you are #
# allowed to use in your solution. See the assignment writeup for details.  #
#                                                                           #
#############################################################################


def add_one_and_multiply(a, x):
    """
    Add 1 to a, and multiply by x.

    input:
        a (int): an integer value
        x (int): an integer value

    Output (int): The result of adding 1 to a and then multiplying by x.

    Examples:
        >>> add_one_and_multiply(2, 4)
        12
        >>> add_one_and_multiply(-13, 5)
        -60
    """
    return (a+1)*x

def are_conjugate_strings(u, v):
    """
    Given two strings u and v, determine whether they are conjugate.

    input:
        u (str): a string
        v (str): a string

    Output (bool): u and v are conjugate

    Examples:
        >>> are_conjugate_strings("a","b")
        False
        >>> are_conjugate_strings("cat", "catcat")
        True
    """
    word = u + v == v + u
    result = word

    return result

def mean_is_median(a, b, c):
    """
    Given three integers, determine whether the mean of the integers is 
    equal to their median.

    input:
        a (int): an integer
        b (int): an integer
        c (int): an integer

    Output (bool): the mean of a, b, c is the median of a, b, c

    Examples:
        >>> mean_is_median(-2, 8, 4)
        False
        >>> mean_is_median(-3, 0, 3)
        True
    """
    fact_check = a - b == b - c or b - a == a - c or a -c ==c - b
    
    result = fact_check
    return result


def progress_report(num_problems, adjective, intensity):
    """
    Produces a progress report, describing progress qualitatively via an
    adjective, and quantitatively, via the number of problems solved intensity.

    Input:
        num_problems (int): The number of problems that were solved
        adjective (str): an adjective describing the experience of solving
                         those problems
        intensity (int): A positive integer quantifying the intensity of
                         the mood when trying to solve those problems.
        
    Output (str): A progress report

    Examples:
        >>> progress_report(3, "fun", 2)
        'Today, I solved 3 problems!! It was fun!!'
        >>> progress_report(-2, "hard", 5)
        'Today, I solved -2 problems!!!!! It was hard!!!!!'
    """
    num_exclam = "!" * intensity
    statement = ("Today, I solved " + str(num_problems) + " problems" + 
                num_exclam + " It was " + adjective + num_exclam)
    result = statement

    return result


def is_valid_grade(grade):
    """
    Determine whether the given grade of execution is valid.

    input:
        grade (float): Grade of execution

    Output (bool): Is a valid grade of execution
    
    Examples:
        >>> is_valid_grade(4)
        True
        >>> is_valid_grade(9)
        False
        >>> is_valid_grade(-2.5)
        False
    """
    outcome = (grade == -5 or grade == -4 or grade == -3 or grade == -2 or 
               grade ==  -1 or grade == 0 or grade ==  1 or grade ==  2 or 
               grade ==  3 or grade ==  4 or grade == 5)
    result = outcome

    return result



def technical_element_score(base_value, j1, j2, j3, j4, j5, j6):    
    """
    Computes a technical element score for an element, based on judges' grades 
    and element base value.

    input:
        base_value (float): base value of element
        j1 (float): grade from Judge 1
        j2 (float): grade from Judge 2
        j3 (float): grade from Judge 3
        j4 (float): grade from Judge 4
        j5 (float): grade from Judge 5
        j6 (float): grade from Judge 6

    Output (float): Computed technical element score

    Examples:
        >>> technical_element_score(11.5, 4, 5, 4, 4, 4, 5)
        16.3875
        >>> technical_element_score(11, 2, 1, 1, 3, 1, 3)
        12.925
    """
    assert (is_valid_grade(j1) and is_valid_grade(j2) and is_valid_grade(j3) 
            and is_valid_grade(j4) and is_valid_grade(j5) and 
            is_valid_grade(j6))
    
    tot = j1 + j2 + j3 + j4 + j5 + j6
    top_score = max(j1, j2, j3, j4, j5, j6)
    low_score = min(j1, j2, j3, j4, j5, j6)
    remaining = tot - top_score - low_score
    average_of_remaining = remaining / 4
    goe = average_of_remaining * (.1 * base_value)
    final_score = goe + base_value
    result = final_score

    return result


def is_valid_color(r, g, b):
    """
    Determine whether or not an RGB color is valid. A color is valid if
    each R, G, B channel is an integer value between 0 and 255 (inclusive).

    Input:
        r (any): red channel
        g (any): green channel
        b (any): blue channel

    Output (bool): True if the color is valid, False otherwise.

    Examples:
        >>> is_valid_color(0, 0, 0)
        True
        >>> is_valid_color(0, 0, 0.5)
        False
        >>> is_valid_color(256, 0, 0)
        False
    """
    is_a_color = (isinstance(r, int) and isinstance(g, int) and 
                  isinstance(b, int) and r >= 0 and r <= 255 and b >= 0 and 
                  b <= 255 and g >= 0 and g<= 255)
    result = is_a_color

    return result



def relative_luminance(r, g, b):
    """
    Compute the relative luminance of a colour.

    Input:
        r (int): red channel of color 
        g (int): green channel of color 
        b (int): blue channel of color 

    Output (float): The relative luminance of the colour

    Examples:
        >>> relative_luminance(144, 12, 63)
        0.0655111725173826
        >>> relative_luminance(255, 195, 11)
        0.603143754654111
    """
    assert is_valid_color(r, g, b)

    red_score = (((r / 255) + 0.055) / 1.055) ** 2.4
    blue_score = (((b / 255) + 0.055) / 1.055) **2.4
    green_score = (((g / 255) + 0.055) / 1.055) **2.4
    final_score = (0.2126 * red_score + 0.7152 * green_score + 0.0722 * 
                   blue_score)
    result = final_score

    return result


def has_sufficient_contrast(r1, g1, b1, r2, g2, b2):
    """
    Test whether the two colours satisfy WCAG Success Criterion 1.4.3.

    Input:
        r1 (int): red channel of color 1
        g1 (int): green channel of color 1
        b1 (int): blue channel of color 1
        r2 (int): red channel of color 2
        g2 (int): green channel of color 2
        b2 (int): blue channel of color 2
    
    Output (bool): color 1 and color 2 have a contrast ratio of at least 4.5.

    Examples:
        >>> has_sufficient_contrast(144, 12, 63, 255, 195, 11)
        True
        >>> has_sufficient_contrast(144, 12, 63, 100, 148, 237)
        False
    """
    assert is_valid_color(r1, g1, b1)
    assert is_valid_color(r2, g2, b2)

    red1_score = (((r1 / 255) + 0.055) / 1.055) ** 2.4
    blue1_score = (((b1 / 255) + 0.055) / 1.055) ** 2.4
    green1_score = (((g1 / 255) + 0.055) / 1.055) ** 2.4
    lum_score1 = (0.2126 * red1_score + 0.7152 * green1_score + 0.0722 * 
                  blue1_score)
    numerator = lum_score1 + 0.05

    red2_score = (((r2 / 255) + 0.055) / 1.055) ** 2.4
    blue2_score = (((b2 / 255) + 0.055) / 1.055) ** 2.4
    green2_score = (((g2 / 255) + 0.055) / 1.055) ** 2.4
    lum_score2 = (0.2126 * red2_score + 0.7152 * green2_score + 0.0722 * 
                  blue2_score)
    denominator = lum_score2 + 0.05

    contrast_value = numerator/denominator
    final_result = contrast_value >= 4.5 or contrast_value <= (1/4.5)
    result = final_result

    return result
