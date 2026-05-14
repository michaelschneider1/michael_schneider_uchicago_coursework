"""
CMSC 14100
Winter 2025

Test code for Homework #2
"""
import hw2
import os
import sys

import pytest
import helpers

# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

# Don't complain about the position of the import
# pylint: disable=wrong-import-position

MODULE = "hw2"

@pytest.mark.parametrize("a, x, expected",
                         [(0, 0, 0),
                          (5, 2, 12),
                          (5, 0, 0),
                          (9, 1, 10),
                          (9, -2, -20),
                          (-11, 2, -20)])
def test_add_one_and_multiply(a, x, expected):
    """
    Do a single test for Exercise 1: add_one_and_multiply
    """
    steps = [f"actual = hw2.add_one_and_multiply({a}, {x})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw2.add_one_and_multiply(a, x)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)
    
    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("u, v, expected",
                         [("a", "b", False),
                          ("a", "a", True),
                          ("", "", True),
                          ("cy", "cycy", True),
                          ("catca", "tcat", False),
                          ("burb", "burbur", False),
                          ("anananan", "ananan", True),
                          ("crab"*23, "crab"*72, True)])
def test_are_conjugate_strings(u, v, expected):
    """
    Do a single test for Exercise 2: are_conjugate_strings
    """
    steps = [f"actual = hw2.are_conjugate_strings({u}, {v})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw2.are_conjugate_strings(u, v)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)
    
    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("a, b, c, expected",
                         [(0, 0, 0, True),
                          (3, 2, 1, True),
                          (7, -3, 24, False),
                          (28, 61, -5, True),
                          (-170, 170, 170, False),
                          (-10431, -10431, -10431, True)])
def test_mean_is_median(a, b, c, expected):
    """
    Do a single test for Exercise 3: mean_is_median
    """
    steps = [f"actual = hw2.mean_is_median({a}, {b}, {c})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw2.mean_is_median(a, b, c)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)
    
    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("num_problems, adjective, intensity, expected",
                         [(11, "cool", 3, "Today, I solved 11 problems!!! It was cool!!!"),
                          (-4, "bad", 2, "Today, I solved -4 problems!! It was bad!!"),
                          (0, "frustrating", 5, "Today, I solved 0 problems!!!!! It was frustrating!!!!!"),
                          (387, "fsfsssfsfs", 3, "Today, I solved 387 problems!!! It was fsfsssfsfs!!!"),
                          (1102, "", 3, "Today, I solved 1102 problems!!! It was !!!"),
                          (1, "okay", 1, "Today, I solved 1 problems! It was okay!")])
def test_progress_report(num_problems, adjective, intensity, expected):
    """
    Do a single test for Exercise 4: progress_report
    """
    steps = [f"actual = hw2.progress_report({num_problems}, {adjective}, {intensity})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw2.progress_report(num_problems, adjective, intensity)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)
    
    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)



@pytest.mark.parametrize("grade, expected",
                         [(0, True),
                          (-2, True),
                          (-7, False),
                          (5, True),
                          (12, False),
                          (1.4, False),
                          (-2.6, False)
                          ])
def test_is_valid_grade(grade, expected):
    """
    Do a single test for Exercise 5: is_valid_grade
    """
    steps = [f"actual = hw2.is_valid_grade({grade})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw2.is_valid_grade(grade)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)
    
    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("base_value, j1, j2, j3, j4, j5, j6, expected",
                         [
                             (11.5, 4, 5, 4, 4, 4, 5, 16.3875), 
                             (11.0, 2, 1, 1, 3, 1, 3, 12.925) ,
                             (3.5, 3, 4, 4, 4, 4, 5, 4.9) ,
                             (3.9, 2, -1, -1, -3, 1, 3, 3.9975) ,
                             (9.5, 0, 1, 1, 1, 0, 2, 10.2125) ,
                             (8.0, -2, 3, 4, 5, 5, -5, 10.0) ,
                             (3.5, 2, 5, 5, 4, 3, 3, 4.8125) ,
                             (3.0, 2, 2, 5, 4, 4, 3, 3.975) 
                         ])
def test_technical_element_score(base_value, j1, j2, j3, j4, j5, j6, expected):
    """
    Do a single test for Exercise 6: technical_element_score
    """
    steps = [f"actual = hw2.technical_element_score({base_value}, {j1}, {j2}, {j3}, {j4}, {j5}, {j6})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw2.technical_element_score(base_value, j1, j2, j3, j4, j5, j6)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)
    
    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)



@pytest.mark.parametrize("r, g, b, expected",
                         [(0, 0, 0, True),
                          (255, 255, 0, True),
                          (0, 255, 0, True),
                          (125, 125, 125, True),
                          ("H", 10, 0, False),
                          (255, -10, 0, False),
                          (0, 255, 256, False),
                          (0.5, 0, 0, False)])
def test_is_valid_color(r, g, b, expected):
    """
    Do a single test for Exercise 7: is_valid_color
    """
    steps = [f"actual = hw2.is_valid_color({r}, {g}, {b})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw2.is_valid_color(r, g, b)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)
    
    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)




@pytest.mark.parametrize("r, g, b, expected",
                         [(144, 12, 63, 0.0655111725173826),
                          (255, 195, 11, 0.603143754654111),
                          (255, 255, 255, 1.0),
                          (11, 11, 11, 0.0033465358),
                          (202, 21, 31, 0.1319181637),
                          (40, 52, 124, 0.043623353),
                          (23, 23, 61, 0.0113187262),
                          (117, 204, 173, 0.4998476921),
                          ])
def test_relative_luminance(r, g, b, expected):
    """
    Do a single test for Exercise 8: relative_luminance
    """
    steps = [f"actual = hw2.relative_luminance({r}, {g}, {b})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw2.relative_luminance(r, g, b)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)
    
    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)



@pytest.mark.parametrize("r1, g1, b1, r2, g2, b2, expected",
                         [
                          (255, 255, 255, 0, 0, 0, True),
                          (1, 1, 1, 255, 255, 255, True),
                          (144, 12, 63, 255, 195, 11, True),
                          (144, 12, 63, 100, 148, 237, False),
                          (144, 12, 63, 143, 13, 62, False),
                          (255, 255, 255, 57, 31, 67, True),
                          (255, 255, 255, 137, 137, 137, False)
                          ])
def test_has_sufficient_contrast(r1, g1, b1, r2, g2, b2, expected):
    """
    Do a single test for Exercise 9: has_sufficient_contrast
    """
    steps = [f"actual = hw2.has_sufficient_contrast({r1}, {g1}, {b1}, {r2}, {g2}, {b2})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw2.has_sufficient_contrast(r1, g1, b1, r2, g2, b2)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)
    
    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)
