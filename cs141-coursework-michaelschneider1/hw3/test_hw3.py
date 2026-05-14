"""
CMSC 14100
Updated Spring 2024

Test code for Homework #3
"""
import os
import sys

import pytest

import hw3
import helpers

# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

# Don't complain about the position of the import
# pylint: disable=wrong-import-position

MODULE = "hw3"


@pytest.mark.parametrize("a1c, expected",
                        [
                        (5.56, hw3.NORMAL),
                        (2.22, hw3.NORMAL),
                        (4.78, hw3.NORMAL),
                        (7.93, hw3.DIABETES),
                        (9.81, hw3.DIABETES),
                        (1.98, hw3.NORMAL),
                        (7.06, hw3.DIABETES),
                        (5.94, hw3.PREDIABETES),
                        (6.02, hw3.PREDIABETES),
                        (6.29, hw3.PREDIABETES),
                        (8.29, hw3.DIABETES)])
def test_categorize_a1c(a1c, expected):
    """ Test code for categorize_a1c """
    steps = [f"actual = hw3.categorize_a1c({a1c})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw3.categorize_a1c(a1c)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

first_tests = [
    ([2.80, 8.32, 8.64, 1.57, 4.51, 4.45, 0.77, 2.07, 0.52, 2.82],hw3.DIABETES),
    ([2.91, 2.45, 5.73, 5.90, 6.31, 1.04, 2.10, 1.07, 7.39, 7.54], hw3.PREDIABETES),
    ([1.12, 2.73, 2.33, 1.79, 5.25, 0.29, 2.29, 4.46, 4.58, 2.14], hw3.NEITHER),
    ([1.44, 6.71, 5.27, 9.13, 9.41, 4.07, 1.86, 3.73, 4.71, 0.16], hw3.DIABETES),
    ([0.49, 1.22, 2.84, 8.31, 5.24, 5.37, 6.70, 6.77, 7.98, 1.56], hw3.DIABETES)
]

@pytest.mark.parametrize("scores, expected", first_tests)
def test_which_comes_first(scores, expected):
    """ Test code for which_comes_first """
    steps = [f"actual = hw3.which_comes_first({scores})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw3.which_comes_first((scores))
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


last_tests = [
    ([3.90, 1.97, 3.76, 1.76, 5.68, 3.33, 4.19, 1.49, 5.06, 2.98],hw3.NEITHER),
([7.57, 8.09, 7.67, 9.34, 8.77, 1.68, 9.86, 3.08, 5.23, 6.44],hw3.PREDIABETES),
([8.52, 7.42, 0.65, 4.81, 2.76, 1.23, 5.15, 5.26, 9.84, 6.40],hw3.PREDIABETES),
([8.36, 2.78, 8.50, 3.15, 5.20, 8.26, 5.58, 4.29, 9.17, 8.01],hw3.DIABETES),
([2.04, 6.12, 9.12, 9.10, 3.80, 7.95, 2.74, 7.13, 5.95, 9.15],hw3.DIABETES),
([3.90, 9.80, 4.87, 3.58, 5.61, 0.20, 3.44, 5.15, 2.85, 3.96],hw3.DIABETES),
([5.71, 3.38, 7.85, 2.76, 1.83, 8.28, 7.96, 5.44, 5.11, 5.65],hw3.DIABETES),
([2.13, 3.52, 7.92, 0.66, 7.85, 7.04, 2.46, 0.05, 8.21, 7.11],hw3.DIABETES),
([7.82, 9.98, 8.75, 9.96, 1.00, 4.53, 8.58, 0.08, 5.70, 5.73],hw3.PREDIABETES),
([9.90, 9.04, 3.39, 9.53, 8.43, 4.82, 2.21, 7.97, 3.50, 8.28],hw3.DIABETES),
]
@pytest.mark.parametrize("scores, expected", last_tests)
def test_which_comes_last(scores, expected):
    """ Test code for which_comes_last """
    steps = [f"actual = hw3.which_comes_last({scores})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw3.which_comes_last((scores))
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

@pytest.mark.parametrize("lst, expected",
                         [([], False),
                          ([50], True),
                          ([50, 100], True),
                          ([100]*10, True),
                          ([50]*5 + [100], True),
                          ([2,4,6,8,10], True),
                          ([10,100,1000,10000], True),
                          (list(range(2,20)), False),
                          ])
def test_is_multiples_of_first(lst, expected):
    """ Test code for is_multiples_of_first """
    steps = [f"lst = {lst}",
             f"actual = hw3.is_multiples_of_first(lst)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw3.is_multiples_of_first(lst)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)



violations = [("RECKLESS DRIVING","SCHOOL",40),
                ("PARKING","CONSTRUCTION",15),
                ("RECKLESS DRIVING","CONSTRUCTION",60),
                ("PARKING","SCHOOL",10),
                ("PARKING","CONSTRUCTION",15),
                ("RECKLESS DRIVING","SCHOOL",40),
                ("PARKING","CONSTRUCTION",15),
                ("SPEEDING","SCHOOL",20),
                ("SPEEDING","CONSTRUCTION",30),
                ("SPEEDING","CONSTRUCTION",30)]
@pytest.mark.parametrize("violation_type, location, expected", violations)
def test_violation_points(violation_type, location, expected):
    """ Test code for violation_points """
    steps = \
        [f"actual = hw3.violation_points({violation_type}, {location})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw3.violation_points(violation_type, location)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

suspension_tests = [
([('RECKLESS DRIVING', 'SCHOOL')], 19, True),
([('RECKLESS DRIVING', 'SCHOOL'), ('PARKING', 'CONSTRUCTION'), ('PARKING', 'SCHOOL'), ('SPEEDING', 'SCHOOL'), ('PARKING', 'CONSTRUCTION')], 42, True),
([('RECKLESS DRIVING', 'SCHOOL'), ('PARKING', 'CONSTRUCTION'), ('PARKING', 'CONSTRUCTION'), ('SPEEDING', 'SCHOOL')], 96, True),
([], 74, False),
([('SPEEDING', 'CONSTRUCTION'), ('PARKING', 'SCHOOL'), ('SPEEDING', 'CONSTRUCTION'), ('PARKING', 'CONSTRUCTION')], 77, True),
([('PARKING', 'CONSTRUCTION'), ('PARKING', 'CONSTRUCTION'), ('PARKING', 'SCHOOL')], 64, True),
([('SPEEDING', 'SCHOOL')], 69, False),
([('RECKLESS DRIVING', 'CONSTRUCTION'), ('RECKLESS DRIVING', 'CONSTRUCTION')], 26, True),
([('PARKING', 'CONSTRUCTION'), ('RECKLESS DRIVING', 'SCHOOL'), ('PARKING', 'SCHOOL')], 38, True),
([], 20, False)
]
@pytest.mark.parametrize("violations, driver_age, expected", suspension_tests)
def test_is_suspended(violations, driver_age, expected):
    """ Test code for is_suspended """
    steps = [f"violations = {violations}",
             f"actual = hw3.is_suspended(violations, driver_age)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw3.is_suspended(violations, driver_age)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


grade_tests = [([], True),
                ([7, 6, -1, 6, 3, 1, -5], False),
                ([-10, -6, -5, 9, -8, -8, 8, -3, 8, -2], False),
                ([8, -7], False),
                ([2, -9, 6, -6, -4, -8, 10], False),
                ([3, 4, -1, 2], True),
                ([-4, 4, -5, 3, -2], True),
                ([4, -5, -4, 3, 4, 5, -1, 1, 0], True),
                ([-3, -4, 2, -4, -2, 0], True),
                ([-1, 0, -3, -5, 5], True),
                ([3, -2, -1, 2, 1, 0, -2, 0, -2], True),
                ([-5, 5, -1, -4, 1, 5, 3, -3, 1, 0], True),
                ([-4, 0, 1, -5], True),
                ([4, -5, -3, 3, 2, 1, -4], True),
                ([4, 2, 3, -1, -4, -5, -1, 1, 1], True)]

@pytest.mark.parametrize("grades, expected", grade_tests)
def test_valid_grades(grades, expected):
    """ Test code for valid_grades """
    steps = [f"grades = {grades}",
             f"actual = hw3.valid_grades(grades)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw3.valid_grades(grades)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


tes_tests = [(5.03, [-5, 3, -2, -3, 1], 4.359333),
 (4.06, [-5, -1, -5, 1, 4], 3.383333),
 (8.18, [-4, -4, -4, -2], 4.908),
 (10.52, [-5, 3, 0, -5, 1, -4, 3, 0, -4], 9.167429),
 (3.12, [-5, 2, -1, 2, -2], 3.016),
 (7.04, [-2, 1, 0, 3, -3, 0, -4, 0, -4], 6.235429),
 (4.58, [2, 4, -2, 5, -4, -2, -1, -2], 4.503667),
 (4.22, [4, 2, 4, 0, 2], 5.345333),
 (3.96, [-3, -1, -4, 4, -5, -2, 1, -2], 3.234),
 (10.14, [-2, 2, -3, -4, 1, -3, 2, -1], 9.126)]

@pytest.mark.parametrize("base_value, grades, expected", tes_tests)
def test_technical_element_score(base_value, grades, expected):
    """ Test code for technical_element_score """
    steps = [f"grades = {grades}",
             f"actual = hw3.technical_element_score(base_value, grades)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw3.technical_element_score(base_value, grades)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

first_non_normal_tests = [
([],None),
([9.82, 1.62, 7.91, 9.77, 7.83, 1.41, 4.18, 4.72, 8.66, 3.00],0),
([4.68, 5.22, 2.52, 4.79, 3.82, 3.99, 5.59, 4.34, 1.92, 7.77],9),
([1.18, 1.35, 5.45, 2.11, 1.47, 5.22, 2.54, 3.25, 5.41, 1.79],None),
([2.61, 2.56, 7.06, 7.36, 1.85, 5.94, 5.67, 0.62, 2.14, 0.36],2),
([4.43, 2.10, 3.35, 9.75, 0.39, 5.45, 1.29, 0.60, 0.80, 5.72],3),
([8.86, 1.66, 4.80, 4.37, 0.10, 1.02, 2.88, 6.02, 1.31, 8.19],0),
([0.57, 2.94, 5.64, 6.14, 0.90, 1.07, 7.69, 6.56, 8.50, 0.21],3),
([7.14, 5.93, 6.77, 1.34, 9.68, 8.03, 5.08, 4.11, 2.40, 9.54],0),
([1.49, 1.17, 6.42, 0.75, 2.57, 8.55, 1.35, 8.59, 7.42, 5.70],2),
([2.22, 5.10, 3.11, 1.46, 5.20, 9.23, 4.98, 1.10, 2.62, 7.72],5),
]

@pytest.mark.parametrize("scores, expected", first_non_normal_tests)
def test_get_first_non_normal(scores, expected):
    """ Test code for get_first_non_normal """
    steps = [f"scores = {scores}",
             f"actual = hw3.get_first_non_normal(scores)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw3.get_first_non_normal(scores)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)