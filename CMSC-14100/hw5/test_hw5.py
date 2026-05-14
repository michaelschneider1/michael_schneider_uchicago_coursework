"""
CMSC 14100
Winter 2025

Test code for Homework #5
"""

import copy
import json
import os
import sys
import traceback
import pytest
import helpers as helpers

# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

# Don't complain about the position of the import
# pylint: disable=wrong-import-position
import hw5
from hw5_tables import *
from math import log

MODULE = "hw5"

table11 = [["a", "b", "c"], 
          [1, 2, 3], 
          [5, 4, 6],
          [9, 8, 6]]

results1 = [
        [1, 5, 9], 
        [2, 4, 8], 
        [435400, 924800, 930802, 949460, 1011669, 1167904, 1209900, 1270274, 1244209, 1235085, 1209756, 1199772, 1246516, 1437883, 1530391, 1803397, 2203730, 2401397, 1200685, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [(2024, 10, 1), (2024, 10, 2), (2024, 10, 3), (2024, 10, 4), (2024, 10, 5), (2024, 10, 6), (2024, 10, 7), (2024, 10, 8), (2024, 10, 9), (2024, 10, 10), (2024, 10, 11), (2024, 10, 12), (2024, 10, 13), (2024, 10, 14), (2024, 10, 15), (2024, 10, 16), (2024, 10, 17), (2024, 10, 18), (2024, 10, 19), (2024, 10, 20), (2024, 10, 21), (2024, 10, 22), (2024, 10, 23), (2024, 10, 24), (2024, 10, 25), (2024, 10, 26), (2024, 10, 27), (2024, 10, 28), (2024, 10, 29), (2024, 10, 30), (2024, 10, 31)], 
        [457355, 452173, 454449, 409598, 318359, 248486, 406230, 459661, 467517, 485221, 456909, 369877, 466771, 384342, 444249, 462121, 466090, 413404, 354109, 239392, 403752, 451887, 461471, 465121, 408835, 296326, 215594, 389359, 444706, 451915, 425596], 
        [0, 274, 5, 347, 0, 22, 28, 26, 9, 89, 59, 50, 148, 32, 13, 56, 118, 40, 20, 0, 25, 0, 12, 50, 0, 0, 12, 27, 0, 0, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 31, 9, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 8, 0, 35, 15], 
        [201, 708, 157, 414, 38, 65, 121, 128, 11, 38, 61, 47, 106, 447, 390, 175, 176, 12, 129, 10, 20, 31, 0, 137, 118, 0, 0, 60, 0, 0, 0, 16, 92, 0, 0, 0, 0, 0, 20, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 7, 0, 91, 0, 88, 2, 8, 27, 38, 36, 181, 14, 0, 0, 25, 0, 0, 0, 0, 8, 33, 176], 
        ['Anthropology', 'Applied Math', 'Art History', 'Astrophysics', 'Biological Chemistry', 'Biological Sciences', 'Chemistry', 'Chemistry (M.S.)', 'Cinema and Media Studies', 'Classical Studies', 'Cognitive Science', 'Common Year', 'Comparative Human Development', 'Comparative Literature', 'Computational Analysis (M.S.)', 'Computational and Applied Math', 'Computer Science', 'Computer Science (M.S.)', 'Computer Science (Rsch), (M.S.)', 'Creative Writing', 'Critical Race/Ethn Studies', 'Data Science', 'Digital Studies (M.A.)', 'East Asian Lang/Civ', 'Economics', 'English Language/Literature', 'Environment/Geog/Urbanization', 'Environmental Science', 'Environmental/Urban Studies', 'Financial Mathematics (M.S.)', 'Fundamentals: Issues/Texts', 'Gender and Sexuality Studies', 'Geophysical Sciences', 'Germanic Studies', 'Global Studies', 'HIPSS', 'History', 'Human Rights', 'Inquiry/Research Humanities', 'International Relations (M.A.)', 'Jewish Studies', 'Latin American/Carib Studies', 'Law/Letters/Society', 'Linguistics', 'M.A., Prog Hum Language Option', 'M.A., Program Humanities', 'Mathematics', 'Mathematics (M.S.)', 'Media Arts and Design', 'Medieval Studies', 'Middle Eastern Studies HUM MA', 'Molecular Engineering', 'Music', 'Near Eastern Lang/Civ', 'Neuroscience', 'Philosophy', 'Philosophy and Allied Fields', 'Physics', 'Political Science', 'Psychology', 'Public Policy (M.P.P.)', 'Public Policy Studies', 'Race/Diaspora/Indigeneity', 'Religious Studies', 'Romance Lang/Lit', 'Russian/East European Studies', 'Social Sciences (M.A.)', 'Social Sciences/Econ Conc MA', 'Social Sciences/Psych Conc MA', 'Social Sciences/Quant Conc MA', 'Social Work (M.A.)', 'Sociology', 'South Asian Lang/Civ', 'Statistics', 'Statistics (M.S.)', 'Theater/Performance Studies', 'Visual Arts'], 
        [21.9, 21.7, 22.1, 21.8, 22.0, 21.8, 21.5, 21.7, 21.7, 21.6, 21.2, 21.3, 21.5, 21.4, 21.3, 21.2, 20.8, 21.3, 21.4, 21.9, 21.8, 22.0, 22.2, 21.9, 21.6, 21.6, 21.3, 21.3, 21.3, 21.3, 21.2, 21.4, 21.4, 21.4, 21.2, 21.0, 20.8, 20.8, 20.7, 20.5, 20.6, 20.5, 20.5, 20.5, 20.6, 20.8, 21.0, 21.4, 21.7, 21.8, 21.8, 21.2, 21.3, 21.0, 20.7, 20.9, 21.1, 21.1, 21.7, 22.1, 22.4], 
        [6, 6, 10, 2, 2, 6, 1, 3, 7, 3, 4, 3, 4, 10, 4, 6, 4, 1, 3, 11, 7, 5, 9, 5, 6, 3, 6, 6, 5, 5, 8, 5, 5, 4, 9, 7, 9, 10, 2, 9, 9, 8, 9, 7, 6, 8, 7, 8, 10, 11, 8, 7, 8, 7, 12, 11, 9, 12, 11, 8, 6, 7, 11, 10, 13, 13, 10, 5, 7, 10, 6, 13, 15, 9, 14, 7, 16, 14, 20, 12, 13, 16, 12, 18, 21, 12, 17, 22, 10, 21, 11, 13, 17, 21, 16, 22, 20, 17, 25, 15, 21, 17, 19, 9, 25, 18, 22, 20, 20, 16, 19, 23, 19, 21, 20, 21, 10, 26, 25, 31, 32, 22, 24, 22, 27, 33, 33, 38, 31, 19, 31, 40, 40, 44, 48, 22]
    ]

@pytest.mark.parametrize("table, column, expected",
                         [(table11, 'a', results1[0]),
                          (table11, 'b', results1[1]),
                          (CTA_ANNUAL, CTA_ANNUAL[0][2], results1[2]),
                          (CTA_DAILY, CTA_DAILY[0][0], results1[3]),
                          (CTA_DAILY, CTA_DAILY[0][3], results1[4]),
                          (LANGUAGES, LANGUAGES[0][10], results1[5]),
                          (LANGUAGES, LANGUAGES[0][23], results1[6]),
                          (AUTUMN2024, AUTUMN2024[0][0], results1[7]),
                          (BEACH_WEATHER, BEACH_WEATHER[0][2], results1[8]),
                          (COVID, COVID[0][3], results1[9])
                          ])
def test_extract_column(table, column, expected):
    """
    Test code for Exercise 1: extract_column
    """
    steps = [f"table = {table})",
             f"actual = hw5.extract_column(table, '{column}')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw5.extract_column(table, column)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)



table21 = copy.deepcopy(table11)

table22 = [["a", "b", "c", "c"], 
          [1, 2, 3], 
          [5, 4, 6],
          [9, 8, 6]]

table23 = [["a", "b", "c"], 
          [1, 2, "3"], 
          [5, 4, 6],
          [9, 8, 6]]

table24 = [["a", "b", "c"], 
          [1, 2, 3], 
          [5, 4, 6, 7],
          [9, 8, 6]]

table25 = [["a", "b", "c"], 
          [1, 2, 3], 
          [5.0, 4, 6],
          [9, 8, 6]]

table26 = [["a", "b", "c"], 
          [1.0, "2", 3], 
          [5.0, "4", 6],
          [9.0, "8", 6]]

table27 = [["b", "b", "c"], 
          [1.0, "2", 3], 
          [5.0, "4", 6],
          [9.0, "8", 6]]

table28 = [["b", 23, "c"], 
          [1.0, "2", 3], 
          [5.0, "4", 6],
          [9.0, "8", 6]]

@pytest.mark.parametrize("table, expected",
                         [(table21, True),
                          (table22, False),
                          (table23, False),
                          (table24, False),
                          (table25, False),
                          (table26, True),
                          (table27, False),
                          (table28, False),
                          (LANGUAGES, True),
                          (COVID, True)]
                         )
def test_is_valid_table(table, expected):
    """
    Test code for Exercise 2: is_valid_table
    """
    steps = [f"table = {table}",
             f"actual = hw5.is_valid_table(table)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw5.is_valid_table(table)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

table31 = copy.deepcopy(table11)

results3 = [
    [['a', 'b', 'c'], [1, 2, 3]], 
    [['a', 'b', 'c'], [5, 4, 6], [9, 8, 6]], 
    [['a', 'b', 'c']], 
    [['a', 'b', 'c'], [1, 2, 3], [5, 4, 6], [9, 8, 6]], 
    [['service_date', 'day_type', 'bus', 'rail_boardings', 'total_rides'], [(2024, 10, 2), 'W', 663546, 452173, 1115719]], 
    [['Sort', 'Year', 'Term', 'Remedial Number Successfully Completing Courses', 'Remedial Total Enrollment', 'Remedial Course Success Rate', 'Occupational/Workforce Number Successfully Completing Courses', 'Occupational/Workforce Total Enrollment', 'Occupational/Workforce Course Success Rate', 'Baccalaureate/Transfer Number Successfully Completing Courses', 'Baccalaureate/Transfer Total Enrollment', 'Baccalaureate/Transfer Course Success Rate', 'Row Order'], [1, '2000 Fall', 'Fall', 8322, 15660, 53.0, 13282, 17713, 75, 28372, 44383, 64, 1], [3, '2001 Fall', 'Fall', 9864, 17069, 57.78897416369, 13273, 17811, 75, 31771, 48859, 65, 3], [5, '2002 Fall', 'Fall', 10997, 18701, 58.8043420138, 13723, 17935, 77, 36377, 53368, 68, 5], [7, '2003 Fall', 'Fall', 11221, 19734, 56.86125468734, 12944, 16904, 77, 38529, 57084, 67, 7], [9, '2004 Fall', 'Fall', 10531, 19604, 53.71862885125, 12034, 17142, 70, 37356, 57236, 65, 9], [11, '2005 Fall', 'Fall', 9646, 18055, 53.42564386597, 12710, 16911, 75, 35688, 54370, 66, 11], [13, '2006 Fall', 'Fall', 9971, 17909, 55.67591713664, 12780, 16802, 76, 35699, 54145, 66, 13], [15, '2007 Fall', 'Fall', 9919, 17532, 56.57654574492, 13431, 18046, 74, 37214, 55981, 66, 15], [17, '2008 Fall', 'Fall', 10318, 18433, 55.97569576303, 11729, 16368, 72, 39188, 59228, 66, 17], [19, '2009 Fall', 'Fall', 12124, 21573, 56.19987947898, 15072, 20056, 75, 47038, 69163, 68, 19], [21, '2010 Fall', 'Fall', 12688, 22492, 56.41116841544, 15499, 21222, 73, 48560, 73721, 66, 21]], 
    [['Date', 'Cases - Total', 'Deaths - Total', 'Hospitalizations - Total', 'Cases - Age 0-17', 'Cases - Age 18-29', 'Cases - Age 30-39', 'Cases - Age 40-49', 'Cases - Age 50-59', 'Cases - Age 60-69', 'Cases - Age 70-79', 'Cases -  Age 80+', 'Cases - Age Unknown', 'Cases - Female', 'Cases - Male', 'Cases - Unknown Gender', 'Cases - Latinx', 'Cases - Asian Non-Latinx', 'Cases - Black Non-Latinx', 'Cases - White Non-Latinx', 'Cases - Other Race Non-Latinx', 'Cases - Unknown Race/Ethnicity', 'Deaths - Age 0-17', 'Deaths - Age 18-29', 'Deaths - Age 30-39', 'Deaths - Age 40-49', 'Deaths - Age 50-59', 'Deaths - Age 60-69', 'Deaths - Age 70-79', 'Deaths - Age 80+', 'Deaths - Age Unknown', 'Deaths - Female', 'Deaths - Male', 'Deaths - Unknown Gender', 'Deaths - Latinx', 'Deaths - Asian Non-Latinx', 'Deaths - Black Non-Latinx', 'Deaths - White Non-Latinx', 'Deaths - Other Race Non-Latinx', 'Deaths - Unknown Race/Ethnicity', 'Hospitalizations - Age 0-17', 'Hospitalizations - Age 18-29', 'Hospitalizations - Age 30-39', 'Hospitalizations - Age 40-49', 'Hospitalizations - Age 50-59', 'Hospitalizations - Age 60-69', 'Hospitalizations - Age 70-79', 'Hospitalizations - Age 80+', 'Hospitalizations - Age Unknown', 'Hospitalizations - Female', 'Hospitalizations - Male', 'Hospitalizations - Unknown Gender', 'Hospitalizations - Latinx', 'Hospitalizations - Asian Non-Latinx', 'Hospitalizations - Black Non-Latinx', 'Hospitalizations - White Non-Latinx', 'Hospitalizations - Other Race Non-Latinx', 'Hospitalizations - Unknown Race/Ethnicity'], [(2024, 5, 8), 36, 0, 3, 4, 8, 5, 1, 2, 7, 6, 3, 0, 25, 11, 0, 5, 4, 12, 11, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 1, 0, 0, 1, 0, 2, 0, 0]], 
    [['service_date', 'day_type', 'bus', 'rail_boardings', 'total_rides'], [(2024, 10, 1), 'W', 675858, 457355, 1133213], [(2024, 10, 3), 'W', 670461, 454449, 1124910], [(2024, 10, 4), 'W', 619444, 409598, 1029042], [(2024, 10, 5), 'A', 431370, 318359, 749729], [(2024, 10, 6), 'U', 336190, 248486, 584676], [(2024, 10, 7), 'W', 623133, 406230, 1029363], [(2024, 10, 8), 'W', 652969, 459661, 1112630], [(2024, 10, 9), 'W', 661361, 467517, 1128878], [(2024, 10, 10), 'W', 650278, 485221, 1135499], [(2024, 10, 11), 'W', 624145, 456909, 1081054], [(2024, 10, 12), 'A', 427732, 369877, 797609], [(2024, 10, 13), 'U', 280965, 466771, 747736], [(2024, 10, 14), 'W', 486971, 384342, 871313], [(2024, 10, 15), 'W', 582685, 444249, 1026934], [(2024, 10, 16), 'W', 652964, 462121, 1115085], [(2024, 10, 17), 'W', 650082, 466090, 1116172], [(2024, 10, 18), 'W', 627426, 413404, 1040830], [(2024, 10, 19), 'A', 425987, 354109, 780096], [(2024, 10, 20), 'U', 321239, 239392, 560631], [(2024, 10, 21), 'W', 619582, 403752, 1023334], [(2024, 10, 22), 'W', 642373, 451887, 1094260], [(2024, 10, 23), 'W', 653689, 461471, 1115160], [(2024, 10, 24), 'W', 654696, 465121, 1119817], [(2024, 10, 25), 'W', 611655, 408835, 1020490], [(2024, 10, 26), 'A', 427475, 296326, 723801], [(2024, 10, 27), 'U', 312965, 215594, 528559], [(2024, 10, 28), 'W', 611041, 389359, 1000400], [(2024, 10, 29), 'W', 652674, 444706, 1097380], [(2024, 10, 30), 'W', 657942, 451915, 1109857], [(2024, 10, 31), 'W', 605292, 425596, 1030888]]
]

@pytest.mark.parametrize("table, column, value, negate, expected",
                         [(table31, "a", 1, False, table31[:2]),
                          (table31, "a", 1, True, [table31[0][:]] + table31[2:]),
                          (table31, "a", 30, False, [table31[0][:]]),
                          (table31, "a", 30, True, copy.deepcopy(table31)),
                          (CTA_DAILY, 
                           CTA_DAILY[0][0], 
                           CTA_DAILY[2][0], 
                           False, 
                           results3[4]),
                          (COLLEGES, 
                           COLLEGES[0][2], 
                           COLLEGES[1][2], 
                           False, 
                           results3[5]),
                          (COVID, 
                           COVID[0][4], 
                           COVID[8][4], 
                           False, 
                           results3[6]),
                          (CTA_DAILY, 
                           CTA_DAILY[0][0], 
                           CTA_DAILY[2][0], 
                           True, 
                           results3[7])
                          ])
def test_filter_exact(table, column, value, negate, expected):
    """
    Test code for Exercise 3: filter_exact with negate specified
    """
    steps = [
             f"table = {table}",
             f"actual = hw5.filter_exact(table, '{column}', {helpers.add_quotes_if_needed(value)}, {negate})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    table_copy = copy.deepcopy(table) # check that the table wasn't modified

    try:
        actual = hw5.filter_exact(table, column, value, negate)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

    err_msg = helpers.check_2D_list_unmodified("table", table_copy, table)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

@pytest.mark.parametrize("table, column, value, expected",
                         [(table31, "a", 1, table31[:2]),
                          (table31, "a", 30, [table31[0][:]]),
                          (CTA_DAILY, 
                           CTA_DAILY[0][0], 
                           CTA_DAILY[2][0], 
                           results3[4])
                          ])
def test_filter_exact_optional(table, column, value, expected):
    """
    Test code for Exercise 3: filter_exact without optional parameter
    """
    steps = [
             f"table = {table}",
             f"actual = hw5.filter_exact(table, '{column}', {helpers.add_quotes_if_needed(value)})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    table_copy = copy.deepcopy(table) # check that the table wasn't modified

    try:
        actual = hw5.filter_exact(table, column, value)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

    err_msg = helpers.check_2D_list_unmodified("table", table_copy, table)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

        

@pytest.mark.parametrize("table",
                         [(table22), (table23)])
def test_filter_exact_valid(table):
    """
    Test for: assert is_valid_table(table)
    """
    steps = [
             f"table = {table}",
             f"actual = hw5.filter_exact(table, 'a', 1)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)
    
    try:
        actual = hw5.filter_exact(table, column, value)
    except Exception as AssertionError:
        return # correct
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = "\n\nInput table is invalid."
    err_msg += "\n  Expected: AssertionError"

    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


table41 = copy.deepcopy(table11)
table42 = [AUTUMN2024[0]] + AUTUMN2024[10:15]
table43 = [AUTUMN2024[0]] + AUTUMN2024[1:7]
table44 = [SOCIOECONOMIC[0]] + SOCIOECONOMIC[1:8]
table45 = [COVID[0]] + COVID[12:20]
table46 = [LANGUAGES[0]] + LANGUAGES[21:32]
table47 = [BEACH_WEATHER[0]] + BEACH_WEATHER[31:39]

results4 = [
        [['a'], [1], [5], [9]], 
        [['c', 'a'], [3, 1], [6, 5], [6, 9]], 
        [['b', 'c', 'a'], [2, 3, 1], [4, 6, 5], [8, 6, 9]], 
        [['First', 'Second', 'Academic Plan'], [15, 9, 'Classical Studies'], [52, 37, 'Cognitive Science'], [3469, 0, 'Common Year'], [33, 17, 'Comparative Human Development'], [8, 1, 'Comparative Literature']], 
        [['Academic Plan', 'Fourth', 'First', 'Academic Plan'], ['Anthropology', 0, 33, 'Anthropology'], ['Applied Math', 0, 4, 'Applied Math'], ['Art History', 0, 23, 'Art History'], ['Astrophysics', 0, 40, 'Astrophysics'], ['Biological Chemistry', 0, 44, 'Biological Chemistry'], ['Biological Sciences', 0, 249, 'Biological Sciences']], 
        [['Community Area Number', 'HARDSHIP INDEX', 'PERCENT AGED 16+ UNEMPLOYED'], [1, 39, 8.7], [2, 46, 8.8], [3, 20, 8.9], [4, 17, 8.2], [5, 6, 5.2], [6, 5, 4.7], [7, 2, 5.1]], 
        [['Date', 'Cases - Female', 'Cases - Age 60-69', 'Cases - Unknown Gender', 'Cases - Age 40-49', 'Cases - Age 0-17'], [(2024, 5, 4), 22, 4, 0, 7, 0], [(2024, 5, 3), 48, 38, 16, 12, 22], [(2024, 5, 2), 23, 3, 0, 1, 8], [(2024, 5, 1), 26, 3, 0, 5, 6], [(2024, 4, 30), 27, 9, 0, 5, 10], [(2024, 4, 29), 32, 10, 0, 1, 10], [(2024, 4, 28), 19, 2, 0, 4, 5], [(2024, 4, 27), 17, 7, 0, 3, 6]], 
        [['HEBREW', 'LAOTIAN', 'CREOLE', 'ARABIC', 'Community Area'], [0, 0, 0, 15, 21], [7, 0, 0, 0, 22], [0, 0, 0, 0, 23], [0, 0, 29, 33, 24], [0, 0, 10, 0, 25], [0, 0, 0, 0, 26], [9, 0, 0, 0, 27], [0, 0, 3, 145, 28], [0, 0, 0, 0, 29], [0, 0, 0, 1, 30], [0, 0, 0, 53, 31]], 
        [['Community Area', 'CAMBODIAN (MON-KHMER)', 'CREOLE', 'OTHER ASIAN', 'HUNGARIAN'], [21, 0, 0, 201, 0], [22, 0, 0, 12, 11], [23, 0, 0, 0, 2], [24, 0, 29, 0, 18], [25, 0, 10, 0, 0], [26, 0, 0, 0, 0], [27, 0, 0, 0, 0], [28, 10, 3, 197, 0], [29, 0, 0, 0, 0], [30, 0, 0, 0, 0], [31, 0, 0, 0, 0]], 
        [['Rain Intensity', 'Air Temperature'], [0.0, 21.2], [0.0, 21.4], [0.0, 21.4], [0.0, 21.4], [0.0, 21.2], [0.0, 21.0], [0.0, 20.8], [0.0, 20.8]]
    ]
@pytest.mark.parametrize("table, columns, expected",
    [(table41, ['a'], results4[0]),
     (table41, [table41[0][2], table41[0][0]], results4[1]),
     (table41, [table41[0][i] for i in [1,2,0]], results4[2]),
     (table42, [table42[0][i] for i in [1,2,0]], results4[3]),
     (table43, [table43[0][i] for i in [0,4,1,0]], results4[4]),
     (table44, [table44[0][i] for i in [0,8,4]], results4[5]),
     (table45, [table45[0][i] for i in [0,13,9,15,7,4]], results4[6]),
     (table46, [table46[0][i] for i in [12,19,7,3,0]], results4[7]),
     (table46, [table46[0][i] for i in [0,5,7,21,15]], results4[8]),
     (table47, [table47[0][5], table47[0][2]], results4[9]),
     ]
     )
def test_select_columns(table, columns, expected):
    """
    Test code for Exercise 4: select_columns
    """
    steps = [
             f"table = {table}",
             f"columns = {columns}",
             f"actual = hw5.select_columns(table, columns)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    table_copy = copy.deepcopy(table) # check that the table wasn't modified

    try:
        actual = hw5.select_columns(table, columns)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

    err_msg = helpers.check_2D_list_unmodified("table", table_copy, table)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

@pytest.mark.parametrize("table",
                         [(table22), (table23)])
def test_select_columns_valid(table):
    """
    Test for: assert is_valid_table(table)
    """
    steps = [
             f"table = {table}",
             f"actual = hw5.select_columns(table, ['a'])"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)
    
    try:
        actual = hw5.select_columns(table, ['a'])
    except Exception as AssertionError:
        return # correct
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = "\n\nInput table is invalid."
    err_msg += "\n  Expected: AssertionError"

    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)



table51 = copy.deepcopy(table11)
table52 = copy.deepcopy(AUTUMN2024)
table53 = COVID[:15]
table54 = [LANGUAGES[0]] + LANGUAGES[20:40]

results5 = [
        [['a', 'b', 'c', 'd'], [1, 2, 3, 6], [5, 4, 6, 15], [9, 8, 6, 23]], 
        [['a', 'b', 'c', 'd'], [1, 2, 3, 4], [5, 4, 6, 11], [9, 8, 6, 15]], 
        [['Academic Plan', 'First', 'Second', 'Third', 'Fourth', 'Total'], ['Anthropology', 33, 18, 0, 0, 51], ['Applied Math', 4, 3, 0, 0, 7], ['Art History', 23, 13, 3, 0, 39], ['Astrophysics', 40, 13, 0, 0, 53], ['Biological Chemistry', 44, 14, 2, 0, 60], ['Biological Sciences', 249, 25, 2, 0, 276], ['Chemistry', 78, 27, 7, 0, 112], ['Chemistry (M.S.)', 0, 2, 1, 0, 3], ['Cinema and Media Studies', 13, 18, 1, 0, 32], ['Classical Studies', 15, 9, 1, 0, 25], ['Cognitive Science', 52, 37, 0, 0, 89], ['Common Year', 3469, 0, 0, 0, 3469], ['Comparative Human Development', 33, 17, 4, 0, 54], ['Comparative Literature', 8, 1, 2, 0, 11], ['Computational Analysis (M.S.)', 0, 2, 0, 0, 2], ['Computational and Applied Math', 66, 24, 1, 0, 91], ['Computer Science', 345, 130, 4, 0, 479], ['Computer Science (M.S.)', 0, 20, 7, 1, 28], ['Computer Science (Rsch), (M.S.)', 0, 2, 0, 0, 2], ['Creative Writing', 43, 40, 1, 0, 84], ['Critical Race/Ethn Studies', 5, 2, 0, 0, 7], ['Data Science', 92, 83, 1, 0, 176], ['Digital Studies (M.A.)', 0, 1, 0, 0, 1], ['East Asian Lang/Civ', 11, 10, 1, 0, 22], ['Economics', 1210, 312, 11, 1, 1534], ['English Language/Literature', 43, 26, 1, 0, 70], ['Environment/Geog/Urbanization', 22, 20, 3, 0, 45], ['Environmental Science', 43, 14, 0, 0, 57], ['Environmental/Urban Studies', 13, 10, 1, 0, 24], ['Financial Mathematics (M.S.)', 0, 4, 3, 0, 7], ['Fundamentals: Issues/Texts', 28, 5, 0, 0, 33], ['Gender and Sexuality Studies', 8, 26, 6, 0, 40], ['Geophysical Sciences', 13, 6, 0, 0, 19], ['Germanic Studies', 3, 5, 0, 0, 8], ['Global Studies', 38, 32, 1, 0, 71], ['HIPSS', 9, 5, 0, 0, 14], ['History', 87, 50, 2, 0, 139], ['Human Rights', 21, 20, 4, 1, 46], ['Inquiry/Research Humanities', 1, 5, 1, 0, 7], ['International Relations (M.A.)', 0, 20, 9, 0, 29], ['Jewish Studies', 0, 0, 1, 0, 1], ['Latin American/Carib Studies', 3, 3, 0, 0, 6], ['Law/Letters/Society', 56, 35, 2, 0, 93], ['Linguistics', 30, 16, 0, 0, 46], ['M.A., Prog Hum Language Option', 0, 0, 1, 0, 1], ['M.A., Program Humanities', 0, 3, 5, 0, 8], ['Mathematics', 239, 98, 7, 0, 344], ['Mathematics (M.S.)', 0, 3, 1, 0, 4], ['Media Arts and Design', 31, 31, 0, 0, 62], ['Medieval Studies', 1, 1, 0, 0, 2], ['Middle Eastern Studies HUM MA', 0, 0, 1, 0, 1], ['Molecular Engineering', 104, 6, 1, 0, 111], ['Music', 5, 21, 4, 0, 30], ['Near Eastern Lang/Civ', 16, 9, 0, 0, 25], ['Neuroscience', 123, 18, 1, 0, 142], ['Philosophy', 61, 64, 3, 0, 128], ['Philosophy and Allied Fields', 7, 4, 2, 0, 13], ['Physics', 122, 34, 1, 0, 157], ['Political Science', 174, 77, 0, 0, 251], ['Psychology', 110, 98, 3, 2, 213], ['Public Policy (M.P.P.)', 0, 7, 3, 0, 10], ['Public Policy Studies', 120, 92, 0, 0, 212], ['Race/Diaspora/Indigeneity', 6, 12, 0, 0, 18], ['Religious Studies', 4, 27, 1, 0, 32], ['Romance Lang/Lit', 14, 51, 1, 0, 66], ['Russian/East European Studies', 1, 9, 0, 0, 10], ['Social Sciences (M.A.)', 0, 24, 11, 1, 36], ['Social Sciences/Econ Conc MA', 0, 4, 8, 1, 13], ['Social Sciences/Psych Conc MA', 0, 2, 0, 0, 2], ['Social Sciences/Quant Conc MA', 0, 2, 0, 0, 2], ['Social Work (M.A.)', 0, 1, 0, 0, 1], ['Sociology', 40, 34, 4, 0, 78], ['South Asian Lang/Civ', 2, 1, 2, 0, 5], ['Statistics', 50, 53, 13, 0, 116], ['Statistics (M.S.)', 0, 0, 3, 0, 3], ['Theater/Performance Studies', 7, 10, 0, 0, 17], ['Visual Arts', 10, 18, 0, 0, 28]], 
        [['Academic Plan', 'First', 'Second', 'Third', 'Fourth', 'Total'], ['Anthropology', 33, 18, 0, 0, 51], ['Applied Math', 4, 3, 0, 0, 7], ['Art History', 23, 13, 3, 0, 36], ['Astrophysics', 40, 13, 0, 0, 53], ['Biological Chemistry', 44, 14, 2, 0, 58], ['Biological Sciences', 249, 25, 2, 0, 274], ['Chemistry', 78, 27, 7, 0, 105], ['Chemistry (M.S.)', 0, 2, 1, 0, 2], ['Cinema and Media Studies', 13, 18, 1, 0, 31], ['Classical Studies', 15, 9, 1, 0, 24], ['Cognitive Science', 52, 37, 0, 0, 89], ['Common Year', 3469, 0, 0, 0, 3469], ['Comparative Human Development', 33, 17, 4, 0, 50], ['Comparative Literature', 8, 1, 2, 0, 9], ['Computational Analysis (M.S.)', 0, 2, 0, 0, 2], ['Computational and Applied Math', 66, 24, 1, 0, 90], ['Computer Science', 345, 130, 4, 0, 475], ['Computer Science (M.S.)', 0, 20, 7, 1, 20], ['Computer Science (Rsch), (M.S.)', 0, 2, 0, 0, 2], ['Creative Writing', 43, 40, 1, 0, 83], ['Critical Race/Ethn Studies', 5, 2, 0, 0, 7], ['Data Science', 92, 83, 1, 0, 175], ['Digital Studies (M.A.)', 0, 1, 0, 0, 1], ['East Asian Lang/Civ', 11, 10, 1, 0, 21], ['Economics', 1210, 312, 11, 1, 1522], ['English Language/Literature', 43, 26, 1, 0, 69], ['Environment/Geog/Urbanization', 22, 20, 3, 0, 42], ['Environmental Science', 43, 14, 0, 0, 57], ['Environmental/Urban Studies', 13, 10, 1, 0, 23], ['Financial Mathematics (M.S.)', 0, 4, 3, 0, 4], ['Fundamentals: Issues/Texts', 28, 5, 0, 0, 33], ['Gender and Sexuality Studies', 8, 26, 6, 0, 34], ['Geophysical Sciences', 13, 6, 0, 0, 19], ['Germanic Studies', 3, 5, 0, 0, 8], ['Global Studies', 38, 32, 1, 0, 70], ['HIPSS', 9, 5, 0, 0, 14], ['History', 87, 50, 2, 0, 137], ['Human Rights', 21, 20, 4, 1, 41], ['Inquiry/Research Humanities', 1, 5, 1, 0, 6], ['International Relations (M.A.)', 0, 20, 9, 0, 20], ['Jewish Studies', 0, 0, 1, 0, 0], ['Latin American/Carib Studies', 3, 3, 0, 0, 6], ['Law/Letters/Society', 56, 35, 2, 0, 91], ['Linguistics', 30, 16, 0, 0, 46], ['M.A., Prog Hum Language Option', 0, 0, 1, 0, 0], ['M.A., Program Humanities', 0, 3, 5, 0, 3], ['Mathematics', 239, 98, 7, 0, 337], ['Mathematics (M.S.)', 0, 3, 1, 0, 3], ['Media Arts and Design', 31, 31, 0, 0, 62], ['Medieval Studies', 1, 1, 0, 0, 2], ['Middle Eastern Studies HUM MA', 0, 0, 1, 0, 0], ['Molecular Engineering', 104, 6, 1, 0, 110], ['Music', 5, 21, 4, 0, 26], ['Near Eastern Lang/Civ', 16, 9, 0, 0, 25], ['Neuroscience', 123, 18, 1, 0, 141], ['Philosophy', 61, 64, 3, 0, 125], ['Philosophy and Allied Fields', 7, 4, 2, 0, 11], ['Physics', 122, 34, 1, 0, 156], ['Political Science', 174, 77, 0, 0, 251], ['Psychology', 110, 98, 3, 2, 208], ['Public Policy (M.P.P.)', 0, 7, 3, 0, 7], ['Public Policy Studies', 120, 92, 0, 0, 212], ['Race/Diaspora/Indigeneity', 6, 12, 0, 0, 18], ['Religious Studies', 4, 27, 1, 0, 31], ['Romance Lang/Lit', 14, 51, 1, 0, 65], ['Russian/East European Studies', 1, 9, 0, 0, 10], ['Social Sciences (M.A.)', 0, 24, 11, 1, 24], ['Social Sciences/Econ Conc MA', 0, 4, 8, 1, 4], ['Social Sciences/Psych Conc MA', 0, 2, 0, 0, 2], ['Social Sciences/Quant Conc MA', 0, 2, 0, 0, 2], ['Social Work (M.A.)', 0, 1, 0, 0, 1], ['Sociology', 40, 34, 4, 0, 74], ['South Asian Lang/Civ', 2, 1, 2, 0, 3], ['Statistics', 50, 53, 13, 0, 103], ['Statistics (M.S.)', 0, 0, 3, 0, 0], ['Theater/Performance Studies', 7, 10, 0, 0, 17], ['Visual Arts', 10, 18, 0, 0, 28]], 
        [['Academic Plan', 'First', 'Second', 'Third', 'Fourth', 'Total'], ['Anthropology', 33, 18, 0, 0, 18], ['Applied Math', 4, 3, 0, 0, 3], ['Art History', 23, 13, 3, 0, 13], ['Astrophysics', 40, 13, 0, 0, 13], ['Biological Chemistry', 44, 14, 2, 0, 14], ['Biological Sciences', 249, 25, 2, 0, 25], ['Chemistry', 78, 27, 7, 0, 27], ['Chemistry (M.S.)', 0, 2, 1, 0, 2], ['Cinema and Media Studies', 13, 18, 1, 0, 18], ['Classical Studies', 15, 9, 1, 0, 9], ['Cognitive Science', 52, 37, 0, 0, 37], ['Common Year', 3469, 0, 0, 0, 0], ['Comparative Human Development', 33, 17, 4, 0, 17], ['Comparative Literature', 8, 1, 2, 0, 1], ['Computational Analysis (M.S.)', 0, 2, 0, 0, 2], ['Computational and Applied Math', 66, 24, 1, 0, 24], ['Computer Science', 345, 130, 4, 0, 130], ['Computer Science (M.S.)', 0, 20, 7, 1, 21], ['Computer Science (Rsch), (M.S.)', 0, 2, 0, 0, 2], ['Creative Writing', 43, 40, 1, 0, 40], ['Critical Race/Ethn Studies', 5, 2, 0, 0, 2], ['Data Science', 92, 83, 1, 0, 83], ['Digital Studies (M.A.)', 0, 1, 0, 0, 1], ['East Asian Lang/Civ', 11, 10, 1, 0, 10], ['Economics', 1210, 312, 11, 1, 313], ['English Language/Literature', 43, 26, 1, 0, 26], ['Environment/Geog/Urbanization', 22, 20, 3, 0, 20], ['Environmental Science', 43, 14, 0, 0, 14], ['Environmental/Urban Studies', 13, 10, 1, 0, 10], ['Financial Mathematics (M.S.)', 0, 4, 3, 0, 4], ['Fundamentals: Issues/Texts', 28, 5, 0, 0, 5], ['Gender and Sexuality Studies', 8, 26, 6, 0, 26], ['Geophysical Sciences', 13, 6, 0, 0, 6], ['Germanic Studies', 3, 5, 0, 0, 5], ['Global Studies', 38, 32, 1, 0, 32], ['HIPSS', 9, 5, 0, 0, 5], ['History', 87, 50, 2, 0, 50], ['Human Rights', 21, 20, 4, 1, 21], ['Inquiry/Research Humanities', 1, 5, 1, 0, 5], ['International Relations (M.A.)', 0, 20, 9, 0, 20], ['Jewish Studies', 0, 0, 1, 0, 0], ['Latin American/Carib Studies', 3, 3, 0, 0, 3], ['Law/Letters/Society', 56, 35, 2, 0, 35], ['Linguistics', 30, 16, 0, 0, 16], ['M.A., Prog Hum Language Option', 0, 0, 1, 0, 0], ['M.A., Program Humanities', 0, 3, 5, 0, 3], ['Mathematics', 239, 98, 7, 0, 98], ['Mathematics (M.S.)', 0, 3, 1, 0, 3], ['Media Arts and Design', 31, 31, 0, 0, 31], ['Medieval Studies', 1, 1, 0, 0, 1], ['Middle Eastern Studies HUM MA', 0, 0, 1, 0, 0], ['Molecular Engineering', 104, 6, 1, 0, 6], ['Music', 5, 21, 4, 0, 21], ['Near Eastern Lang/Civ', 16, 9, 0, 0, 9], ['Neuroscience', 123, 18, 1, 0, 18], ['Philosophy', 61, 64, 3, 0, 64], ['Philosophy and Allied Fields', 7, 4, 2, 0, 4], ['Physics', 122, 34, 1, 0, 34], ['Political Science', 174, 77, 0, 0, 77], ['Psychology', 110, 98, 3, 2, 100], ['Public Policy (M.P.P.)', 0, 7, 3, 0, 7], ['Public Policy Studies', 120, 92, 0, 0, 92], ['Race/Diaspora/Indigeneity', 6, 12, 0, 0, 12], ['Religious Studies', 4, 27, 1, 0, 27], ['Romance Lang/Lit', 14, 51, 1, 0, 51], ['Russian/East European Studies', 1, 9, 0, 0, 9], ['Social Sciences (M.A.)', 0, 24, 11, 1, 25], ['Social Sciences/Econ Conc MA', 0, 4, 8, 1, 5], ['Social Sciences/Psych Conc MA', 0, 2, 0, 0, 2], ['Social Sciences/Quant Conc MA', 0, 2, 0, 0, 2], ['Social Work (M.A.)', 0, 1, 0, 0, 1], ['Sociology', 40, 34, 4, 0, 34], ['South Asian Lang/Civ', 2, 1, 2, 0, 1], ['Statistics', 50, 53, 13, 0, 53], ['Statistics (M.S.)', 0, 0, 3, 0, 0], ['Theater/Performance Studies', 7, 10, 0, 0, 10], ['Visual Arts', 10, 18, 0, 0, 18]], 
        [['Date', 'Cases - Total', 'Deaths - Total', 'Hospitalizations - Total', 'Cases - Age 0-17', 'Cases - Age 18-29', 'Cases - Age 30-39', 'Cases - Age 40-49', 'Cases - Age 50-59', 'Cases - Age 60-69', 'Cases - Age 70-79', 'Cases -  Age 80+', 'Cases - Age Unknown', 'Cases - Female', 'Cases - Male', 'Cases - Unknown Gender', 'Cases - Latinx', 'Cases - Asian Non-Latinx', 'Cases - Black Non-Latinx', 'Cases - White Non-Latinx', 'Cases - Other Race Non-Latinx', 'Cases - Unknown Race/Ethnicity', 'Deaths - Age 0-17', 'Deaths - Age 18-29', 'Deaths - Age 30-39', 'Deaths - Age 40-49', 'Deaths - Age 50-59', 'Deaths - Age 60-69', 'Deaths - Age 70-79', 'Deaths - Age 80+', 'Deaths - Age Unknown', 'Deaths - Female', 'Deaths - Male', 'Deaths - Unknown Gender', 'Deaths - Latinx', 'Deaths - Asian Non-Latinx', 'Deaths - Black Non-Latinx', 'Deaths - White Non-Latinx', 'Deaths - Other Race Non-Latinx', 'Deaths - Unknown Race/Ethnicity', 'Hospitalizations - Age 0-17', 'Hospitalizations - Age 18-29', 'Hospitalizations - Age 30-39', 'Hospitalizations - Age 40-49', 'Hospitalizations - Age 50-59', 'Hospitalizations - Age 60-69', 'Hospitalizations - Age 70-79', 'Hospitalizations - Age 80+', 'Hospitalizations - Age Unknown', 'Hospitalizations - Female', 'Hospitalizations - Male', 'Hospitalizations - Unknown Gender', 'Hospitalizations - Latinx', 'Hospitalizations - Asian Non-Latinx', 'Hospitalizations - Black Non-Latinx', 'Hospitalizations - White Non-Latinx', 'Hospitalizations - Other Race Non-Latinx', 'Hospitalizations - Unknown Race/Ethnicity', 'name'], [(2024, 5, 15), 50, 0, 6, 6, 3, 9, 9, 8, 5, 6, 4, 0, 28, 22, 0, 10, 8, 10, 17, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 2, 1, 0, 3, 3, 0, 0, 0, 4, 2, 0, 0, 38], [(2024, 5, 14), 47, 0, 6, 10, 5, 10, 8, 7, 5, 2, 0, 0, 30, 17, 0, 11, 2, 10, 15, 3, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 1, 1, 0, 2, 4, 0, 2, 0, 0, 2, 1, 1, 32], [(2024, 5, 13), 55, 0, 10, 12, 7, 7, 6, 4, 8, 6, 5, 0, 37, 18, 0, 13, 1, 18, 15, 3, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 3, 2, 2, 0, 5, 5, 0, 1, 0, 4, 5, 0, 0, 48], [(2024, 5, 12), 32, 0, 2, 3, 8, 2, 4, 3, 3, 5, 4, 0, 18, 14, 0, 7, 2, 9, 12, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 27], [(2024, 5, 11), 32, 0, 2, 6, 0, 3, 4, 8, 4, 4, 3, 0, 17, 15, 0, 5, 1, 11, 10, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 24], [(2024, 5, 10), 38, 0, 6, 8, 3, 3, 7, 4, 5, 5, 3, 0, 25, 13, 0, 10, 1, 12, 9, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 0, 3, 3, 0, 0, 0, 3, 2, 0, 1, 33], [(2024, 5, 9), 33, 0, 1, 8, 2, 8, 3, 6, 1, 5, 0, 0, 23, 10, 0, 10, 1, 11, 10, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 28], [(2024, 5, 8), 36, 0, 3, 4, 8, 5, 1, 2, 7, 6, 3, 0, 25, 11, 0, 5, 4, 12, 11, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 1, 0, 0, 1, 0, 2, 0, 0, 34], [(2024, 5, 7), 53, 1, 7, 9, 6, 14, 5, 4, 5, 6, 4, 0, 34, 19, 0, 12, 4, 21, 10, 2, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 2, 1, 1, 0, 4, 3, 0, 0, 1, 5, 0, 1, 0, 44], [(2024, 5, 6), 53, 0, 3, 7, 7, 4, 5, 11, 10, 4, 5, 0, 25, 23, 5, 9, 2, 13, 16, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 2, 1, 0, 1, 0, 1, 1, 0, 0, 34], [(2024, 5, 5), 20, 0, 4, 3, 5, 5, 3, 0, 2, 0, 2, 0, 13, 7, 0, 4, 0, 9, 4, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2, 0, 3, 1, 0, 1, 0, 1, 2, 0, 0, 15], [(2024, 5, 4), 36, 1, 3, 0, 8, 8, 7, 1, 4, 5, 3, 0, 22, 14, 0, 7, 1, 9, 12, 3, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 2, 0, 1, 0, 30], [(2024, 5, 3), 138, 0, 4, 22, 13, 10, 12, 33, 38, 6, 4, 0, 48, 74, 16, 8, 1, 38, 13, 4, 74, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 2, 2, 0, 0, 0, 3, 0, 1, 0, 58], [(2024, 5, 2), 38, 0, 10, 8, 3, 6, 1, 11, 3, 1, 5, 0, 23, 15, 0, 10, 4, 6, 14, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 2, 1, 1, 3, 0, 4, 6, 0, 4, 0, 4, 2, 0, 0, 29]], 
        [['Date', 'Cases - Total', 'Deaths - Total', 'Hospitalizations - Total', 'Cases - Age 0-17', 'Cases - Age 18-29', 'Cases - Age 30-39', 'Cases - Age 40-49', 'Cases - Age 50-59', 'Cases - Age 60-69', 'Cases - Age 70-79', 'Cases -  Age 80+', 'Cases - Age Unknown', 'Cases - Female', 'Cases - Male', 'Cases - Unknown Gender', 'Cases - Latinx', 'Cases - Asian Non-Latinx', 'Cases - Black Non-Latinx', 'Cases - White Non-Latinx', 'Cases - Other Race Non-Latinx', 'Cases - Unknown Race/Ethnicity', 'Deaths - Age 0-17', 'Deaths - Age 18-29', 'Deaths - Age 30-39', 'Deaths - Age 40-49', 'Deaths - Age 50-59', 'Deaths - Age 60-69', 'Deaths - Age 70-79', 'Deaths - Age 80+', 'Deaths - Age Unknown', 'Deaths - Female', 'Deaths - Male', 'Deaths - Unknown Gender', 'Deaths - Latinx', 'Deaths - Asian Non-Latinx', 'Deaths - Black Non-Latinx', 'Deaths - White Non-Latinx', 'Deaths - Other Race Non-Latinx', 'Deaths - Unknown Race/Ethnicity', 'Hospitalizations - Age 0-17', 'Hospitalizations - Age 18-29', 'Hospitalizations - Age 30-39', 'Hospitalizations - Age 40-49', 'Hospitalizations - Age 50-59', 'Hospitalizations - Age 60-69', 'Hospitalizations - Age 70-79', 'Hospitalizations - Age 80+', 'Hospitalizations - Age Unknown', 'Hospitalizations - Female', 'Hospitalizations - Male', 'Hospitalizations - Unknown Gender', 'Hospitalizations - Latinx', 'Hospitalizations - Asian Non-Latinx', 'Hospitalizations - Black Non-Latinx', 'Hospitalizations - White Non-Latinx', 'Hospitalizations - Other Race Non-Latinx', 'Hospitalizations - Unknown Race/Ethnicity', 'title'], [(2024, 5, 15), 50, 0, 6, 6, 3, 9, 9, 8, 5, 6, 4, 0, 28, 22, 0, 10, 8, 10, 17, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 2, 1, 0, 3, 3, 0, 0, 0, 4, 2, 0, 0, 50], [(2024, 5, 14), 47, 0, 6, 10, 5, 10, 8, 7, 5, 2, 0, 0, 30, 17, 0, 11, 2, 10, 15, 3, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 1, 1, 0, 2, 4, 0, 2, 0, 0, 2, 1, 1, 47], [(2024, 5, 13), 55, 0, 10, 12, 7, 7, 6, 4, 8, 6, 5, 0, 37, 18, 0, 13, 1, 18, 15, 3, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 3, 2, 2, 0, 5, 5, 0, 1, 0, 4, 5, 0, 0, 55], [(2024, 5, 12), 32, 0, 2, 3, 8, 2, 4, 3, 3, 5, 4, 0, 18, 14, 0, 7, 2, 9, 12, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 32], [(2024, 5, 11), 32, 0, 2, 6, 0, 3, 4, 8, 4, 4, 3, 0, 17, 15, 0, 5, 1, 11, 10, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 32], [(2024, 5, 10), 38, 0, 6, 8, 3, 3, 7, 4, 5, 5, 3, 0, 25, 13, 0, 10, 1, 12, 9, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 0, 3, 3, 0, 0, 0, 3, 2, 0, 1, 38], [(2024, 5, 9), 33, 0, 1, 8, 2, 8, 3, 6, 1, 5, 0, 0, 23, 10, 0, 10, 1, 11, 10, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 33], [(2024, 5, 8), 36, 0, 3, 4, 8, 5, 1, 2, 7, 6, 3, 0, 25, 11, 0, 5, 4, 12, 11, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 1, 0, 0, 1, 0, 2, 0, 0, 36], [(2024, 5, 7), 53, 1, 7, 9, 6, 14, 5, 4, 5, 6, 4, 0, 34, 19, 0, 12, 4, 21, 10, 2, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 2, 1, 1, 0, 4, 3, 0, 0, 1, 5, 0, 1, 0, 53], [(2024, 5, 6), 53, 0, 3, 7, 7, 4, 5, 11, 10, 4, 5, 0, 25, 23, 5, 9, 2, 13, 16, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 2, 1, 0, 1, 0, 1, 1, 0, 0, 58], [(2024, 5, 5), 20, 0, 4, 3, 5, 5, 3, 0, 2, 0, 2, 0, 13, 7, 0, 4, 0, 9, 4, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2, 0, 3, 1, 0, 1, 0, 1, 2, 0, 0, 20], [(2024, 5, 4), 36, 1, 3, 0, 8, 8, 7, 1, 4, 5, 3, 0, 22, 14, 0, 7, 1, 9, 12, 3, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 2, 0, 1, 0, 36], [(2024, 5, 3), 138, 0, 4, 22, 13, 10, 12, 33, 38, 6, 4, 0, 48, 74, 16, 8, 1, 38, 13, 4, 74, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 2, 2, 0, 0, 0, 3, 0, 1, 0, 154], [(2024, 5, 2), 38, 0, 10, 8, 3, 6, 1, 11, 3, 1, 5, 0, 23, 15, 0, 10, 4, 6, 14, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 2, 1, 1, 3, 0, 4, 6, 0, 4, 0, 4, 2, 0, 0, 38]], 
        [['Community Area', 'Community Area Name', 'AFRICAN LANGUAGES', 'ARABIC', 'ARMENIAN', 'CAMBODIAN (MON-KHMER)', 'CHINESE', 'CREOLE', 'FRENCH', 'GERMAN', 'GREEK', 'GUJARATI', 'HEBREW', 'HINDI', 'HMONG', 'HUNGARIAN', 'ITALIAN', 'JAPANESE', 'KOREAN', 'LAOTIAN', 'NAVAJO', 'OTHER ASIAN', 'OTHER INDIC', 'OTHER INDO EURPOEAN', 'OTHER NATIVE NORTH AMERICAN', 'OTHER PACIFIC ISLAND', 'OTHER SLAVIC', 'OTHER WEST GERMANIC', 'PERSIAN', 'POLISH', 'PORTUGUESE', 'RUSSIAN', 'SCANDINAVIAN', 'SERBO-CROATIAN', 'SPANISH', 'TAGALOG', 'THAI', 'UNSPECIFIED', 'URDU', 'VIETNAMESE', 'YIDDISH', 'name'], [20, 'Hermosa', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 31, 0, 10, 0, 0, 43, 0, 0, 166, 0, 12, 0, 94, 8725, 16, 0, 0, 0, 0, 0, 9], [21, 'Avondale', 0, 15, 0, 0, 112, 0, 7, 9, 25, 0, 0, 0, 0, 0, 32, 13, 10, 0, 0, 201, 0, 20, 0, 0, 99, 0, 0, 1381, 10, 43, 0, 72, 12167, 96, 8, 0, 0, 41, 0, 25], [22, 'Logan Square', 0, 0, 0, 0, 39, 0, 13, 7, 0, 5, 7, 0, 0, 11, 0, 5, 34, 0, 0, 12, 0, 31, 0, 7, 24, 0, 0, 432, 0, 89, 0, 11, 14530, 70, 10, 0, 0, 0, 0, 12], [23, 'Humboldt Park', 0, 0, 0, 0, 0, 0, 34, 17, 12, 0, 0, 0, 0, 2, 2, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 66, 0, 35, 0, 0, 9103, 24, 0, 0, 0, 0, 0, 12], [24, 'West Town', 36, 33, 0, 0, 24, 29, 4, 0, 50, 0, 0, 21, 0, 18, 83, 13, 32, 0, 0, 0, 12, 137, 0, 0, 1278, 0, 0, 935, 33, 123, 0, 20, 7782, 133, 0, 54, 48, 68, 0, 71], [25, 'Austin', 39, 0, 0, 0, 12, 10, 50, 0, 0, 19, 0, 0, 0, 0, 0, 12, 70, 0, 0, 0, 0, 118, 0, 8, 0, 0, 0, 134, 128, 0, 0, 0, 2472, 12, 0, 0, 0, 0, 0, 19], [26, 'West Garfield Park', 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0], [27, 'East Garfield Park', 11, 0, 0, 0, 0, 0, 41, 12, 12, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 68, 0, 7, 0, 0, 0, 0, 21], [28, 'Near West Side', 0, 145, 0, 10, 678, 3, 40, 33, 27, 81, 0, 130, 0, 0, 34, 38, 353, 0, 0, 197, 16, 60, 0, 0, 47, 0, 0, 77, 0, 105, 0, 0, 843, 75, 155, 0, 38, 76, 0, 238], [29, 'North Lawndale', 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 791, 10, 0, 0, 19, 0, 0, 0], [30, 'South Lawndale', 21, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 36, 8, 0, 0, 28120, 32, 0, 0, 0, 0, 0, 2], [31, 'Lower West Side', 0, 53, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 41, 0, 0, 0, 0, 13416, 9, 7, 0, 0, 0, 0, 0], [32, 'Loop', 0, 25, 0, 0, 433, 0, 0, 6, 45, 0, 0, 50, 0, 0, 17, 220, 230, 0, 0, 148, 14, 16, 0, 0, 5, 0, 0, 0, 0, 60, 0, 0, 302, 0, 64, 0, 12, 0, 0, 95], [33, 'Near South Side', 14, 18, 0, 0, 403, 0, 0, 14, 0, 0, 0, 99, 0, 0, 0, 191, 44, 0, 0, 36, 14, 92, 0, 0, 0, 0, 0, 34, 0, 41, 0, 0, 160, 8, 51, 0, 12, 0, 0, 99], [34, 'Armour Square', 4, 1, 0, 0, 5899, 0, 11, 0, 0, 0, 0, 9, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 184, 0, 0, 0, 0, 79, 0, 9], [35, 'Douglas', 42, 2, 0, 0, 586, 0, 216, 0, 0, 27, 0, 21, 0, 0, 0, 12, 135, 0, 0, 69, 32, 0, 0, 35, 0, 0, 6, 15, 7, 3, 0, 0, 250, 7, 20, 0, 0, 10, 0, 48], [36, 'Oakland', 67, 0, 0, 0, 19, 0, 16, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 103, 0, 0, 0, 0, 0, 0, 0], [37, 'Fuller Park', 33, 0, 0, 0, 11, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 67, 0, 0, 0, 0, 0, 0, 0], [38, 'Grand Boulevard', 0, 0, 0, 0, 0, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 57, 0, 5, 0, 0, 237, 0, 0, 0, 0, 0, 0, 0], [39, 'Kenwood', 54, 0, 0, 0, 72, 0, 74, 51, 0, 9, 8, 0, 0, 0, 0, 26, 112, 0, 0, 28, 0, 20, 0, 0, 6, 0, 0, 16, 4, 0, 0, 0, 192, 25, 0, 0, 0, 0, 0, 17]], 
        [['Community Area', 'Community Area Name', 'AFRICAN LANGUAGES', 'ARABIC', 'ARMENIAN', 'CAMBODIAN (MON-KHMER)', 'CHINESE', 'CREOLE', 'FRENCH', 'GERMAN', 'GREEK', 'GUJARATI', 'HEBREW', 'HINDI', 'HMONG', 'HUNGARIAN', 'ITALIAN', 'JAPANESE', 'KOREAN', 'LAOTIAN', 'NAVAJO', 'OTHER ASIAN', 'OTHER INDIC', 'OTHER INDO EURPOEAN', 'OTHER NATIVE NORTH AMERICAN', 'OTHER PACIFIC ISLAND', 'OTHER SLAVIC', 'OTHER WEST GERMANIC', 'PERSIAN', 'POLISH', 'PORTUGUESE', 'RUSSIAN', 'SCANDINAVIAN', 'SERBO-CROATIAN', 'SPANISH', 'TAGALOG', 'THAI', 'UNSPECIFIED', 'URDU', 'VIETNAMESE', 'YIDDISH', 'title'], [20, 'Hermosa', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 31, 0, 10, 0, 0, 43, 0, 0, 166, 0, 12, 0, 94, 8725, 16, 0, 0, 0, 0, 0, 18], [21, 'Avondale', 0, 15, 0, 0, 112, 0, 7, 9, 25, 0, 0, 0, 0, 0, 32, 13, 10, 0, 0, 201, 0, 20, 0, 0, 99, 0, 0, 1381, 10, 43, 0, 72, 12167, 96, 8, 0, 0, 41, 0, 208], [22, 'Logan Square', 0, 0, 0, 0, 39, 0, 13, 7, 0, 5, 7, 0, 0, 11, 0, 5, 34, 0, 0, 12, 0, 31, 0, 7, 24, 0, 0, 432, 0, 89, 0, 11, 14530, 70, 10, 0, 0, 0, 0, 121], [23, 'Humboldt Park', 0, 0, 0, 0, 0, 0, 34, 17, 12, 0, 0, 0, 0, 2, 2, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 66, 0, 35, 0, 0, 9103, 24, 0, 0, 0, 0, 0, 73], [24, 'West Town', 36, 33, 0, 0, 24, 29, 4, 0, 50, 0, 0, 21, 0, 18, 83, 13, 32, 0, 0, 0, 12, 137, 0, 0, 1278, 0, 0, 935, 33, 123, 0, 20, 7782, 133, 0, 54, 48, 68, 0, 274], [25, 'Austin', 39, 0, 0, 0, 12, 10, 50, 0, 0, 19, 0, 0, 0, 0, 0, 12, 70, 0, 0, 0, 0, 118, 0, 8, 0, 0, 0, 134, 128, 0, 0, 0, 2472, 12, 0, 0, 0, 0, 0, 173], [26, 'West Garfield Park', 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 1], [27, 'East Garfield Park', 11, 0, 0, 0, 0, 0, 41, 12, 12, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 68, 0, 7, 0, 0, 0, 0, 74], [28, 'Near West Side', 0, 145, 0, 10, 678, 3, 40, 33, 27, 81, 0, 130, 0, 0, 34, 38, 353, 0, 0, 197, 16, 60, 0, 0, 47, 0, 0, 77, 0, 105, 0, 0, 843, 75, 155, 0, 38, 76, 0, 1427], [29, 'North Lawndale', 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 791, 10, 0, 0, 19, 0, 0, 0], [30, 'South Lawndale', 21, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 36, 8, 0, 0, 28120, 32, 0, 0, 0, 0, 0, 2], [31, 'Lower West Side', 0, 53, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 41, 0, 0, 0, 0, 13416, 9, 7, 0, 0, 0, 0, 32], [32, 'Loop', 0, 25, 0, 0, 433, 0, 0, 6, 45, 0, 0, 50, 0, 0, 17, 220, 230, 0, 0, 148, 14, 16, 0, 0, 5, 0, 0, 0, 0, 60, 0, 0, 302, 0, 64, 0, 12, 0, 0, 1001], [33, 'Near South Side', 14, 18, 0, 0, 403, 0, 0, 14, 0, 0, 0, 99, 0, 0, 0, 191, 44, 0, 0, 36, 14, 92, 0, 0, 0, 0, 0, 34, 0, 41, 0, 0, 160, 8, 51, 0, 12, 0, 0, 751], [34, 'Armour Square', 4, 1, 0, 0, 5899, 0, 11, 0, 0, 0, 0, 9, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 184, 0, 0, 0, 0, 79, 0, 5939], [35, 'Douglas', 42, 2, 0, 0, 586, 0, 216, 0, 0, 27, 0, 21, 0, 0, 0, 12, 135, 0, 0, 69, 32, 0, 0, 35, 0, 0, 6, 15, 7, 3, 0, 0, 250, 7, 20, 0, 0, 10, 0, 997], [36, 'Oakland', 67, 0, 0, 0, 19, 0, 16, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 103, 0, 0, 0, 0, 0, 0, 42], [37, 'Fuller Park', 33, 0, 0, 0, 11, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 67, 0, 0, 0, 0, 0, 0, 14], [38, 'Grand Boulevard', 0, 0, 0, 0, 0, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 57, 0, 5, 0, 0, 237, 0, 0, 0, 0, 0, 0, 42], [39, 'Kenwood', 54, 0, 0, 0, 72, 0, 74, 51, 0, 9, 8, 0, 0, 0, 0, 26, 112, 0, 0, 28, 0, 20, 0, 0, 6, 0, 0, 16, 4, 0, 0, 0, 192, 25, 0, 0, 0, 0, 0, 352]], 
        [['Community Area', 'Community Area Name', 'AFRICAN LANGUAGES', 'ARABIC', 'ARMENIAN', 'CAMBODIAN (MON-KHMER)', 'CHINESE', 'CREOLE', 'FRENCH', 'GERMAN', 'GREEK', 'GUJARATI', 'HEBREW', 'HINDI', 'HMONG', 'HUNGARIAN', 'ITALIAN', 'JAPANESE', 'KOREAN', 'LAOTIAN', 'NAVAJO', 'OTHER ASIAN', 'OTHER INDIC', 'OTHER INDO EURPOEAN', 'OTHER NATIVE NORTH AMERICAN', 'OTHER PACIFIC ISLAND', 'OTHER SLAVIC', 'OTHER WEST GERMANIC', 'PERSIAN', 'POLISH', 'PORTUGUESE', 'RUSSIAN', 'SCANDINAVIAN', 'SERBO-CROATIAN', 'SPANISH', 'TAGALOG', 'THAI', 'UNSPECIFIED', 'URDU', 'VIETNAMESE', 'YIDDISH', 'total'], [20, 'Hermosa', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 31, 0, 10, 0, 0, 43, 0, 0, 166, 0, 12, 0, 94, 8725, 16, 0, 0, 0, 0, 0, 9106], [21, 'Avondale', 0, 15, 0, 0, 112, 0, 7, 9, 25, 0, 0, 0, 0, 0, 32, 13, 10, 0, 0, 201, 0, 20, 0, 0, 99, 0, 0, 1381, 10, 43, 0, 72, 12167, 96, 8, 0, 0, 41, 0, 14193], [22, 'Logan Square', 0, 0, 0, 0, 39, 0, 13, 7, 0, 5, 7, 0, 0, 11, 0, 5, 34, 0, 0, 12, 0, 31, 0, 7, 24, 0, 0, 432, 0, 89, 0, 11, 14530, 70, 10, 0, 0, 0, 0, 15266], [23, 'Humboldt Park', 0, 0, 0, 0, 0, 0, 34, 17, 12, 0, 0, 0, 0, 2, 2, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 66, 0, 35, 0, 0, 9103, 24, 0, 0, 0, 0, 0, 9238], [24, 'West Town', 36, 33, 0, 0, 24, 29, 4, 0, 50, 0, 0, 21, 0, 18, 83, 13, 32, 0, 0, 0, 12, 137, 0, 0, 1278, 0, 0, 935, 33, 123, 0, 20, 7782, 133, 0, 54, 48, 68, 0, 10769], [25, 'Austin', 39, 0, 0, 0, 12, 10, 50, 0, 0, 19, 0, 0, 0, 0, 0, 12, 70, 0, 0, 0, 0, 118, 0, 8, 0, 0, 0, 134, 128, 0, 0, 0, 2472, 12, 0, 0, 0, 0, 0, 2954], [26, 'West Garfield Park', 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 22], [27, 'East Garfield Park', 11, 0, 0, 0, 0, 0, 41, 12, 12, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 68, 0, 7, 0, 0, 0, 0, 75], [28, 'Near West Side', 0, 145, 0, 10, 678, 3, 40, 33, 27, 81, 0, 130, 0, 0, 34, 38, 353, 0, 0, 197, 16, 60, 0, 0, 47, 0, 0, 77, 0, 105, 0, 0, 843, 75, 155, 0, 38, 76, 0, 2114], [29, 'North Lawndale', 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 791, 10, 0, 0, 19, 0, 0, 820], [30, 'South Lawndale', 21, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 36, 8, 0, 0, 28120, 32, 0, 0, 0, 0, 0, 28222], [31, 'Lower West Side', 0, 53, 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 41, 0, 0, 0, 0, 13416, 9, 7, 0, 0, 0, 0, 13488], [32, 'Loop', 0, 25, 0, 0, 433, 0, 0, 6, 45, 0, 0, 50, 0, 0, 17, 220, 230, 0, 0, 148, 14, 16, 0, 0, 5, 0, 0, 0, 0, 60, 0, 0, 302, 0, 64, 0, 12, 0, 0, 1088], [33, 'Near South Side', 14, 18, 0, 0, 403, 0, 0, 14, 0, 0, 0, 99, 0, 0, 0, 191, 44, 0, 0, 36, 14, 92, 0, 0, 0, 0, 0, 34, 0, 41, 0, 0, 160, 8, 51, 0, 12, 0, 0, 683], [34, 'Armour Square', 4, 1, 0, 0, 5899, 0, 11, 0, 0, 0, 0, 9, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 184, 0, 0, 0, 0, 79, 0, 284], [35, 'Douglas', 42, 2, 0, 0, 586, 0, 216, 0, 0, 27, 0, 21, 0, 0, 0, 12, 135, 0, 0, 69, 32, 0, 0, 35, 0, 0, 6, 15, 7, 3, 0, 0, 250, 7, 20, 0, 0, 10, 0, 601], [36, 'Oakland', 67, 0, 0, 0, 19, 0, 16, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 103, 0, 0, 0, 0, 0, 0, 103], [37, 'Fuller Park', 33, 0, 0, 0, 11, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 67, 0, 0, 0, 0, 0, 0, 67], [38, 'Grand Boulevard', 0, 0, 0, 0, 0, 11, 16, 0, 0, 0, 0, 0, 0, 0, 0, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 57, 0, 5, 0, 0, 237, 0, 0, 0, 0, 0, 0, 314], [39, 'Kenwood', 54, 0, 0, 0, 72, 0, 74, 51, 0, 9, 8, 0, 0, 0, 0, 26, 112, 0, 0, 28, 0, 20, 0, 0, 6, 0, 0, 16, 4, 0, 0, 0, 192, 25, 0, 0, 0, 0, 0, 429]]
    ]

@pytest.mark.parametrize("table, columns, name, expected",
    [(table51, table51[0], "d", results5[0]),
     (table51, ['a','c'], "d", results5[1]),
     (table52, table52[0][1:], "Total", results5[2]),
     (table52, table52[0][1:3], "Total", results5[3]),
     (table52, [table52[0][2], table52[0][4]], "Total", results5[4]),
     (table53, table53[0][10:14], "name", results5[5]),
     (table53, table53[0][15:24], "title", results5[6]),
     (table54, table54[0][10:14], "name", results5[7]),
     (table54, table54[0][5:20], "title", results5[8]),
     (table54, table54[0][15:40], "total", results5[9])
     ]
     )
def test_add_row_sum_column(table, columns, name, expected):
    """
    Test code for Exercise 5: add_row_sum_column
    """
    steps = [
             f"table = {table}",
             f"columns = {columns}",
             f"hw5.add_row_sum_column(table, columns, '{name}')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    work_table = copy.deepcopy(table)

    try:
        hw5.add_row_sum_column(work_table, columns, name)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)


    err_msg = helpers.check_2D_vals(lambda x, y: x == y,
                                       work_table,
                                       expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)
        

@pytest.mark.parametrize("table",
                         [(table22), (table23)])
def test_add_row_sum_column_valid(table):
    """
    Test for: assert is_valid_table(table)
    """
    steps = [
             f"table = {table}",
             f"actual = hw5.add_row_sum_column(table, table[0], 'total')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)
    
    try:
        actual = hw5.add_row_sum_column(table, table[0], 'total')
    except Exception as AssertionError:
        return # correct
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = "\n\nInput table is invalid."
    err_msg += "\n  Expected: AssertionError"

    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


table61 = copy.deepcopy(table11)
table62 = CTA_ANNUAL[:10]
table63 = [LANGUAGES[0]] + LANGUAGES[41:59]
table64 = copy.deepcopy(COLLEGES)

results6 = [
        [['a', 'b', 'c', 'd'], [1, 2, 3, 1.0], [5, 4, 6, 3.0], [9, 8, 6, 5.0]], 
        [['a', 'b', 'c', 'd'], [1, 2, 3, 2.0], [5, 4, 6, 3.0], [9, 8, 6, 4.666666666666667]], 
        [['year', 'bus', 'paratransit', 'rail', 'total', 'name'], [1988, 430089500, 435400, 174436000, 604960900, 435400.0], [1989, 420572700, 924800, 168658800, 590156300, 680100.0], [1990, 421183734, 930802, 165732575, 587847111, 763667.3333333334], [1991, 392088602, 949460, 147608116, 540646178, 810115.5], [1992, 370335119, 1011669, 137372830, 508719618, 850426.2], [1993, 326655953, 1167904, 135369734, 463193591, 903339.1666666666], [1994, 331520700, 1209900, 143579100, 476309700, 947133.5714285715], [1995, 306075585, 1270274, 135461619, 442807478, 987526.125], [1996, 302115116, 1244209, 142040486, 445399811, 1016046.4444444445]], 
        [['year', 'bus', 'paratransit', 'rail', 'total', 'title'], [1988, 430089500, 435400, 174436000, 604960900, 604960900.0], [1989, 420572700, 924800, 168658800, 590156300, 597558600.0], [1990, 421183734, 930802, 165732575, 587847111, 594321437.0], [1991, 392088602, 949460, 147608116, 540646178, 580902622.25], [1992, 370335119, 1011669, 137372830, 508719618, 566466021.4], [1993, 326655953, 1167904, 135369734, 463193591, 549253949.6666666], [1994, 331520700, 1209900, 143579100, 476309700, 538833342.5714285], [1995, 306075585, 1270274, 135461619, 442807478, 526830109.5], [1996, 302115116, 1244209, 142040486, 445399811, 517782298.5555556]], 
        [['Community Area', 'Community Area Name', 'AFRICAN LANGUAGES', 'ARABIC', 'ARMENIAN', 'CAMBODIAN (MON-KHMER)', 'CHINESE', 'CREOLE', 'FRENCH', 'GERMAN', 'GREEK', 'GUJARATI', 'HEBREW', 'HINDI', 'HMONG', 'HUNGARIAN', 'ITALIAN', 'JAPANESE', 'KOREAN', 'LAOTIAN', 'NAVAJO', 'OTHER ASIAN', 'OTHER INDIC', 'OTHER INDO EURPOEAN', 'OTHER NATIVE NORTH AMERICAN', 'OTHER PACIFIC ISLAND', 'OTHER SLAVIC', 'OTHER WEST GERMANIC', 'PERSIAN', 'POLISH', 'PORTUGUESE', 'RUSSIAN', 'SCANDINAVIAN', 'SERBO-CROATIAN', 'SPANISH', 'TAGALOG', 'THAI', 'UNSPECIFIED', 'URDU', 'VIETNAMESE', 'YIDDISH', 'name'], [41, 'Hyde Park', 16, 22, 7, 0, 419, 19, 96, 23, 7, 0, 14, 7, 0, 0, 17, 21, 174, 0, 0, 10, 19, 0, 0, 0, 50, 0, 0, 28, 24, 56, 0, 52, 387, 22, 5, 0, 5, 17, 0, 10.0], [42, 'Woodlawn', 0, 11, 0, 0, 20, 23, 70, 13, 0, 0, 0, 0, 0, 0, 8, 0, 23, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 219, 0, 0, 0, 0, 0, 0, 5.0], [43, 'South Shore', 157, 0, 8, 0, 16, 0, 258, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 309, 17, 0, 0, 0, 0, 0, 3.3333333333333335], [44, 'Chatham', 22, 0, 0, 0, 11, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 120, 0, 0, 0, 0, 0, 0, 2.5], [45, 'Avalon Park', 33, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 21, 0, 0, 0, 0, 2.0], [46, 'South Chicago', 399, 0, 0, 0, 0, 151, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 2, 0, 0, 0, 0, 2378, 0, 0, 0, 0, 0, 0, 1.6666666666666667], [47, 'Burnside', 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.4285714285714286], [48, 'Calumet Heights', 50, 0, 0, 0, 0, 59, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 0, 0, 0, 0, 0, 0, 1.25], [49, 'Roseland', 8, 0, 0, 0, 0, 0, 21, 12, 0, 17, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 150, 34, 0, 0, 0, 0, 0, 1.1111111111111112], [50, 'Pullman', 0, 0, 0, 0, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 1.0], [51, 'South Deering', 0, 0, 0, 0, 0, 16, 8, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 1626, 0, 0, 0, 0, 0, 0, 0.9090909090909091], [52, 'East Side', 0, 10, 0, 13, 0, 0, 0, 27, 9, 0, 23, 0, 0, 0, 98, 0, 34, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 292, 5480, 0, 0, 0, 0, 0, 0, 0.8333333333333334], [53, 'West Pullman', 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 19, 0, 0, 0, 0, 607, 0, 0, 0, 0, 0, 0, 0.7692307692307693], [54, 'Riverdale', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 66, 0, 0, 0, 0, 0, 0, 0.7142857142857143], [55, 'Hegewisch', 0, 59, 0, 0, 0, 0, 0, 0, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 90, 8, 0, 0, 42, 568, 17, 0, 0, 0, 0, 0, 0.6666666666666666], [56, 'Garfield Ridge', 0, 100, 0, 0, 40, 0, 0, 0, 9, 0, 0, 0, 0, 0, 70, 0, 0, 0, 0, 17, 0, 7, 0, 0, 76, 0, 0, 2012, 0, 0, 0, 35, 3080, 72, 0, 0, 0, 9, 0, 1.6875], [57, 'Archer Heights', 0, 66, 0, 0, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 871, 0, 0, 0, 0, 3800, 0, 0, 0, 6, 0, 0, 1.588235294117647], [58, 'Brighton Park', 0, 29, 0, 0, 1399, 0, 0, 9, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 91, 0, 12, 0, 0, 13, 275, 0, 11, 0, 0, 15146, 35, 42, 0, 0, 6, 0, 1.5]], 
        [['Community Area', 'Community Area Name', 'AFRICAN LANGUAGES', 'ARABIC', 'ARMENIAN', 'CAMBODIAN (MON-KHMER)', 'CHINESE', 'CREOLE', 'FRENCH', 'GERMAN', 'GREEK', 'GUJARATI', 'HEBREW', 'HINDI', 'HMONG', 'HUNGARIAN', 'ITALIAN', 'JAPANESE', 'KOREAN', 'LAOTIAN', 'NAVAJO', 'OTHER ASIAN', 'OTHER INDIC', 'OTHER INDO EURPOEAN', 'OTHER NATIVE NORTH AMERICAN', 'OTHER PACIFIC ISLAND', 'OTHER SLAVIC', 'OTHER WEST GERMANIC', 'PERSIAN', 'POLISH', 'PORTUGUESE', 'RUSSIAN', 'SCANDINAVIAN', 'SERBO-CROATIAN', 'SPANISH', 'TAGALOG', 'THAI', 'UNSPECIFIED', 'URDU', 'VIETNAMESE', 'YIDDISH', 'title'], [41, 'Hyde Park', 16, 22, 7, 0, 419, 19, 96, 23, 7, 0, 14, 7, 0, 0, 17, 21, 174, 0, 0, 10, 19, 0, 0, 0, 50, 0, 0, 28, 24, 56, 0, 52, 387, 22, 5, 0, 5, 17, 0, 0.0], [42, 'Woodlawn', 0, 11, 0, 0, 20, 23, 70, 13, 0, 0, 0, 0, 0, 0, 8, 0, 23, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 219, 0, 0, 0, 0, 0, 0, 0.0], [43, 'South Shore', 157, 0, 8, 0, 16, 0, 258, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 309, 17, 0, 0, 0, 0, 0, 0.0], [44, 'Chatham', 22, 0, 0, 0, 11, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 120, 0, 0, 0, 0, 0, 0, 0.0], [45, 'Avalon Park', 33, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 21, 0, 0, 0, 0, 0.0], [46, 'South Chicago', 399, 0, 0, 0, 0, 151, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 2, 0, 0, 0, 0, 2378, 0, 0, 0, 0, 0, 0, 0.0], [47, 'Burnside', 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0], [48, 'Calumet Heights', 50, 0, 0, 0, 0, 59, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 0, 0, 0, 0, 0, 0, 0.0], [49, 'Roseland', 8, 0, 0, 0, 0, 0, 21, 12, 0, 17, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 150, 34, 0, 0, 0, 0, 0, 0.0], [50, 'Pullman', 0, 0, 0, 0, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0.0], [51, 'South Deering', 0, 0, 0, 0, 0, 16, 8, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 1626, 0, 0, 0, 0, 0, 0, 0.0], [52, 'East Side', 0, 10, 0, 13, 0, 0, 0, 27, 9, 0, 23, 0, 0, 0, 98, 0, 34, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 292, 5480, 0, 0, 0, 0, 0, 0, 0.0], [53, 'West Pullman', 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 19, 0, 0, 0, 0, 607, 0, 0, 0, 0, 0, 0, 0.0], [54, 'Riverdale', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 66, 0, 0, 0, 0, 0, 0, 0.0], [55, 'Hegewisch', 0, 59, 0, 0, 0, 0, 0, 0, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 90, 8, 0, 0, 42, 568, 17, 0, 0, 0, 0, 0, 0.0], [56, 'Garfield Ridge', 0, 100, 0, 0, 40, 0, 0, 0, 9, 0, 0, 0, 0, 0, 70, 0, 0, 0, 0, 17, 0, 7, 0, 0, 76, 0, 0, 2012, 0, 0, 0, 35, 3080, 72, 0, 0, 0, 9, 0, 0.0], [57, 'Archer Heights', 0, 66, 0, 0, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 871, 0, 0, 0, 0, 3800, 0, 0, 0, 6, 0, 0, 0.0], [58, 'Brighton Park', 0, 29, 0, 0, 1399, 0, 0, 9, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 91, 0, 12, 0, 0, 13, 275, 0, 11, 0, 0, 15146, 35, 42, 0, 0, 6, 0, 0.0]], 
        [['Community Area', 'Community Area Name', 'AFRICAN LANGUAGES', 'ARABIC', 'ARMENIAN', 'CAMBODIAN (MON-KHMER)', 'CHINESE', 'CREOLE', 'FRENCH', 'GERMAN', 'GREEK', 'GUJARATI', 'HEBREW', 'HINDI', 'HMONG', 'HUNGARIAN', 'ITALIAN', 'JAPANESE', 'KOREAN', 'LAOTIAN', 'NAVAJO', 'OTHER ASIAN', 'OTHER INDIC', 'OTHER INDO EURPOEAN', 'OTHER NATIVE NORTH AMERICAN', 'OTHER PACIFIC ISLAND', 'OTHER SLAVIC', 'OTHER WEST GERMANIC', 'PERSIAN', 'POLISH', 'PORTUGUESE', 'RUSSIAN', 'SCANDINAVIAN', 'SERBO-CROATIAN', 'SPANISH', 'TAGALOG', 'THAI', 'UNSPECIFIED', 'URDU', 'VIETNAMESE', 'YIDDISH', 'column'], [41, 'Hyde Park', 16, 22, 7, 0, 419, 19, 96, 23, 7, 0, 14, 7, 0, 0, 17, 21, 174, 0, 0, 10, 19, 0, 0, 0, 50, 0, 0, 28, 24, 56, 0, 52, 387, 22, 5, 0, 5, 17, 0, 17.0], [42, 'Woodlawn', 0, 11, 0, 0, 20, 23, 70, 13, 0, 0, 0, 0, 0, 0, 8, 0, 23, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 219, 0, 0, 0, 0, 0, 0, 12.5], [43, 'South Shore', 157, 0, 8, 0, 16, 0, 258, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 309, 17, 0, 0, 0, 0, 0, 8.333333333333334], [44, 'Chatham', 22, 0, 0, 0, 11, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 120, 0, 0, 0, 0, 0, 0, 6.25], [45, 'Avalon Park', 33, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 21, 0, 0, 0, 0, 5.0], [46, 'South Chicago', 399, 0, 0, 0, 0, 151, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 2, 0, 0, 0, 0, 2378, 0, 0, 0, 0, 0, 0, 4.166666666666667], [47, 'Burnside', 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.5714285714285716], [48, 'Calumet Heights', 50, 0, 0, 0, 0, 59, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 0, 0, 0, 0, 0, 0, 3.125], [49, 'Roseland', 8, 0, 0, 0, 0, 0, 21, 12, 0, 17, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 150, 34, 0, 0, 0, 0, 0, 2.7777777777777777], [50, 'Pullman', 0, 0, 0, 0, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 3.0], [51, 'South Deering', 0, 0, 0, 0, 0, 16, 8, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 1626, 0, 0, 0, 0, 0, 0, 2.909090909090909], [52, 'East Side', 0, 10, 0, 13, 0, 0, 0, 27, 9, 0, 23, 0, 0, 0, 98, 0, 34, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 292, 5480, 0, 0, 0, 0, 0, 0, 10.833333333333334], [53, 'West Pullman', 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 19, 0, 0, 0, 0, 607, 0, 0, 0, 0, 0, 0, 10.0], [54, 'Riverdale', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 66, 0, 0, 0, 0, 0, 0, 9.285714285714286], [55, 'Hegewisch', 0, 59, 0, 0, 0, 0, 0, 0, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 90, 8, 0, 0, 42, 568, 17, 0, 0, 0, 0, 0, 8.666666666666666], [56, 'Garfield Ridge', 0, 100, 0, 0, 40, 0, 0, 0, 9, 0, 0, 0, 0, 0, 70, 0, 0, 0, 0, 17, 0, 7, 0, 0, 76, 0, 0, 2012, 0, 0, 0, 35, 3080, 72, 0, 0, 0, 9, 0, 12.5], [57, 'Archer Heights', 0, 66, 0, 0, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 871, 0, 0, 0, 0, 3800, 0, 0, 0, 6, 0, 0, 12.823529411764707], [58, 'Brighton Park', 0, 29, 0, 0, 1399, 0, 0, 9, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 91, 0, 12, 0, 0, 13, 275, 0, 11, 0, 0, 15146, 35, 42, 0, 0, 6, 0, 12.11111111111111]], 
        [['Community Area', 'Community Area Name', 'AFRICAN LANGUAGES', 'ARABIC', 'ARMENIAN', 'CAMBODIAN (MON-KHMER)', 'CHINESE', 'CREOLE', 'FRENCH', 'GERMAN', 'GREEK', 'GUJARATI', 'HEBREW', 'HINDI', 'HMONG', 'HUNGARIAN', 'ITALIAN', 'JAPANESE', 'KOREAN', 'LAOTIAN', 'NAVAJO', 'OTHER ASIAN', 'OTHER INDIC', 'OTHER INDO EURPOEAN', 'OTHER NATIVE NORTH AMERICAN', 'OTHER PACIFIC ISLAND', 'OTHER SLAVIC', 'OTHER WEST GERMANIC', 'PERSIAN', 'POLISH', 'PORTUGUESE', 'RUSSIAN', 'SCANDINAVIAN', 'SERBO-CROATIAN', 'SPANISH', 'TAGALOG', 'THAI', 'UNSPECIFIED', 'URDU', 'VIETNAMESE', 'YIDDISH', 'numbers'], [41, 'Hyde Park', 16, 22, 7, 0, 419, 19, 96, 23, 7, 0, 14, 7, 0, 0, 17, 21, 174, 0, 0, 10, 19, 0, 0, 0, 50, 0, 0, 28, 24, 56, 0, 52, 387, 22, 5, 0, 5, 17, 0, 0.0], [42, 'Woodlawn', 0, 11, 0, 0, 20, 23, 70, 13, 0, 0, 0, 0, 0, 0, 8, 0, 23, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 219, 0, 0, 0, 0, 0, 0, 0.0], [43, 'South Shore', 157, 0, 8, 0, 16, 0, 258, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 309, 17, 0, 0, 0, 0, 0, 0.0], [44, 'Chatham', 22, 0, 0, 0, 11, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 120, 0, 0, 0, 0, 0, 0, 0.0], [45, 'Avalon Park', 33, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 21, 0, 0, 0, 0, 0.0], [46, 'South Chicago', 399, 0, 0, 0, 0, 151, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 2, 0, 0, 0, 0, 2378, 0, 0, 0, 0, 0, 0, 0.0], [47, 'Burnside', 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0], [48, 'Calumet Heights', 50, 0, 0, 0, 0, 59, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 0, 0, 0, 0, 0, 0, 0.0], [49, 'Roseland', 8, 0, 0, 0, 0, 0, 21, 12, 0, 17, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 150, 34, 0, 0, 0, 0, 0, 0.0], [50, 'Pullman', 0, 0, 0, 0, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0.0], [51, 'South Deering', 0, 0, 0, 0, 0, 16, 8, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 1626, 0, 0, 0, 0, 0, 0, 0.0], [52, 'East Side', 0, 10, 0, 13, 0, 0, 0, 27, 9, 0, 23, 0, 0, 0, 98, 0, 34, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 292, 5480, 0, 0, 0, 0, 0, 0, 1.0833333333333333], [53, 'West Pullman', 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 19, 0, 0, 0, 0, 607, 0, 0, 0, 0, 0, 0, 1.0], [54, 'Riverdale', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 66, 0, 0, 0, 0, 0, 0, 0.9285714285714286], [55, 'Hegewisch', 0, 59, 0, 0, 0, 0, 0, 0, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 90, 8, 0, 0, 42, 568, 17, 0, 0, 0, 0, 0, 0.8666666666666667], [56, 'Garfield Ridge', 0, 100, 0, 0, 40, 0, 0, 0, 9, 0, 0, 0, 0, 0, 70, 0, 0, 0, 0, 17, 0, 7, 0, 0, 76, 0, 0, 2012, 0, 0, 0, 35, 3080, 72, 0, 0, 0, 9, 0, 0.8125], [57, 'Archer Heights', 0, 66, 0, 0, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 871, 0, 0, 0, 0, 3800, 0, 0, 0, 6, 0, 0, 0.7647058823529411], [58, 'Brighton Park', 0, 29, 0, 0, 1399, 0, 0, 9, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 91, 0, 12, 0, 0, 13, 275, 0, 11, 0, 0, 15146, 35, 42, 0, 0, 6, 0, 0.7222222222222222]], 
        [['Sort', 'Year', 'Term', 'Remedial Number Successfully Completing Courses', 'Remedial Total Enrollment', 'Remedial Course Success Rate', 'Occupational/Workforce Number Successfully Completing Courses', 'Occupational/Workforce Total Enrollment', 'Occupational/Workforce Course Success Rate', 'Baccalaureate/Transfer Number Successfully Completing Courses', 'Baccalaureate/Transfer Total Enrollment', 'Baccalaureate/Transfer Course Success Rate', 'Row Order', 'workforce'], [1, '2000 Fall', 'Fall', 8322, 15660, 53.0, 13282, 17713, 75, 28372, 44383, 64, 1, 13282.0], [2, '2001 Spring', 'Spring', 6709, 12788, 52.46324679387, 12987, 17086, 76, 29577, 45170, 65, 2, 13134.5], [3, '2001 Fall', 'Fall', 9864, 17069, 57.78897416369, 13273, 17811, 75, 31771, 48859, 65, 3, 13180.666666666666], [4, '2002 Spring', 'Spring', 7695, 14041, 54.80378890392, 13095, 17267, 76, 33494, 50141, 67, 4, 13159.25], [5, '2002 Fall', 'Fall', 10997, 18701, 58.8043420138, 13723, 17935, 77, 36377, 53368, 68, 5, 13272.0], [6, '2003 Spring', 'Spring', 8410, 15606, 53.88952966808, 14272, 18426, 77, 37148, 54427, 68, 6, 13438.666666666666], [7, '2003 Fall', 'Fall', 11221, 19734, 56.86125468734, 12944, 16904, 77, 38529, 57084, 67, 7, 13368.0], [8, '2004 Spring', 'Spring', 8080, 15435, 52.34855847101, 13466, 17464, 77, 37044, 55890, 66, 8, 13380.25], [9, '2004 Fall', 'Fall', 10531, 19604, 53.71862885125, 12034, 17142, 70, 37356, 57236, 65, 9, 13230.666666666666], [10, '2005 Spring', 'Spring', 7844, 15469, 50.7078673476, 13734, 18120, 76, 36368, 55756, 65, 10, 13281.0], [11, '2005 Fall', 'Fall', 9646, 18055, 53.42564386597, 12710, 16911, 75, 35688, 54370, 66, 11, 13229.09090909091], [12, '2006 Spring', 'Spring', 6862, 14014, 48.96532039389, 12212, 16288, 75, 35096, 53510, 66, 12, 13144.333333333334], [13, '2006 Fall', 'Fall', 9971, 17909, 55.67591713664, 12780, 16802, 76, 35699, 54145, 66, 13, 13116.307692307691], [14, '2007 Spring', 'Spring', 6956, 13841, 50.25648435807, 10791, 15831, 68, 35895, 53880, 67, 14, 12950.214285714286], [15, '2007 Fall', 'Fall', 9919, 17532, 56.57654574492, 13431, 18046, 74, 37214, 55981, 66, 15, 12982.266666666666], [16, '2008 Spring', 'Spring', 7190, 13685, 52.5392765802, 11824, 15973, 74, 36855, 56368, 65, 16, 12909.875], [17, '2008 Fall', 'Fall', 10318, 18433, 55.97569576303, 11729, 16368, 72, 39188, 59228, 66, 17, 12840.411764705883], [18, '2009 Spring', 'Spring', 8571, 16496, 51.95805043647, 13637, 17787, 77, 41457, 62771, 66, 18, 12884.666666666666], [19, '2009 Fall', 'Fall', 12124, 21573, 56.19987947898, 15072, 20056, 75, 47038, 69163, 68, 19, 12999.78947368421], [20, '2010 Spring', 'Spring', 9830, 19750, 49.77215189873, 15320, 20739, 74, 48454, 73593, 66, 20, 13115.8], [21, '2010 Fall', 'Fall', 12688, 22492, 56.41116841544, 15499, 21222, 73, 48560, 73721, 66, 21, 13229.285714285714], [22, '2011 Spring', 'Spring', 10410, 20291, 51.30353358632, 15640, 21729, 72, 49074, 75912, 65, 22, 13338.863636363636]], 
        [['Sort', 'Year', 'Term', 'Remedial Number Successfully Completing Courses', 'Remedial Total Enrollment', 'Remedial Course Success Rate', 'Occupational/Workforce Number Successfully Completing Courses', 'Occupational/Workforce Total Enrollment', 'Occupational/Workforce Course Success Rate', 'Baccalaureate/Transfer Number Successfully Completing Courses', 'Baccalaureate/Transfer Total Enrollment', 'Baccalaureate/Transfer Course Success Rate', 'Row Order', 'transfers'], [1, '2000 Fall', 'Fall', 8322, 15660, 53.0, 13282, 17713, 75, 28372, 44383, 64, 1, 28372.0], [2, '2001 Spring', 'Spring', 6709, 12788, 52.46324679387, 12987, 17086, 76, 29577, 45170, 65, 2, 28974.5], [3, '2001 Fall', 'Fall', 9864, 17069, 57.78897416369, 13273, 17811, 75, 31771, 48859, 65, 3, 29906.666666666668], [4, '2002 Spring', 'Spring', 7695, 14041, 54.80378890392, 13095, 17267, 76, 33494, 50141, 67, 4, 30803.5], [5, '2002 Fall', 'Fall', 10997, 18701, 58.8043420138, 13723, 17935, 77, 36377, 53368, 68, 5, 31918.2], [6, '2003 Spring', 'Spring', 8410, 15606, 53.88952966808, 14272, 18426, 77, 37148, 54427, 68, 6, 32789.833333333336], [7, '2003 Fall', 'Fall', 11221, 19734, 56.86125468734, 12944, 16904, 77, 38529, 57084, 67, 7, 33609.71428571428], [8, '2004 Spring', 'Spring', 8080, 15435, 52.34855847101, 13466, 17464, 77, 37044, 55890, 66, 8, 34039.0], [9, '2004 Fall', 'Fall', 10531, 19604, 53.71862885125, 12034, 17142, 70, 37356, 57236, 65, 9, 34407.555555555555], [10, '2005 Spring', 'Spring', 7844, 15469, 50.7078673476, 13734, 18120, 76, 36368, 55756, 65, 10, 34603.6], [11, '2005 Fall', 'Fall', 9646, 18055, 53.42564386597, 12710, 16911, 75, 35688, 54370, 66, 11, 34702.181818181816], [12, '2006 Spring', 'Spring', 6862, 14014, 48.96532039389, 12212, 16288, 75, 35096, 53510, 66, 12, 34735.0], [13, '2006 Fall', 'Fall', 9971, 17909, 55.67591713664, 12780, 16802, 76, 35699, 54145, 66, 13, 34809.153846153844], [14, '2007 Spring', 'Spring', 6956, 13841, 50.25648435807, 10791, 15831, 68, 35895, 53880, 67, 14, 34886.71428571428], [15, '2007 Fall', 'Fall', 9919, 17532, 56.57654574492, 13431, 18046, 74, 37214, 55981, 66, 15, 35041.86666666667], [16, '2008 Spring', 'Spring', 7190, 13685, 52.5392765802, 11824, 15973, 74, 36855, 56368, 65, 16, 35155.1875], [17, '2008 Fall', 'Fall', 10318, 18433, 55.97569576303, 11729, 16368, 72, 39188, 59228, 66, 17, 35392.41176470588], [18, '2009 Spring', 'Spring', 8571, 16496, 51.95805043647, 13637, 17787, 77, 41457, 62771, 66, 18, 35729.333333333336], [19, '2009 Fall', 'Fall', 12124, 21573, 56.19987947898, 15072, 20056, 75, 47038, 69163, 68, 19, 36324.52631578947], [20, '2010 Spring', 'Spring', 9830, 19750, 49.77215189873, 15320, 20739, 74, 48454, 73593, 66, 20, 36931.0], [21, '2010 Fall', 'Fall', 12688, 22492, 56.41116841544, 15499, 21222, 73, 48560, 73721, 66, 21, 37484.76190476191], [22, '2011 Spring', 'Spring', 10410, 20291, 51.30353358632, 15640, 21729, 72, 49074, 75912, 65, 22, 38011.545454545456]]
    ]

@pytest.mark.parametrize("table, column, name, expected",
    [(table61, 'a', "d", results6[0]),
     (table61, 'b', "d", results6[1]),
     (table62, table62[0][2], "name", results6[2]),
     (table62, table62[0][4], "title", results6[3]),
     (table63, table63[0][21], "name", results6[4]),
     (table63, table63[0][14], "title", results6[5]),
     (table63, table63[0][16], "column", results6[6]),
     (table63, table63[0][5], "numbers", results6[7]),
     (table64, table64[0][6], "workforce", results6[8]),
     (table64, table64[0][9], "transfers", results6[9]),
     ]
     )
def test_add_running_mean_column(table, column, name, expected):
    """
    Test code for Exercise 6: add_running_mean_column
    """
    steps = [
             f"table = {table}",
             f"hw5.add_running_mean_column(table, '{column}', '{name}')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    work_table = copy.deepcopy(table)

    try:
        hw5.add_running_mean_column(work_table, column, name)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)


    err_msg = helpers.check_2D_vals(lambda x, y: pytest.approx(x) == y,
                                       work_table,
                                       expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)
        

@pytest.mark.parametrize("table",
                         [(table22), (table23)])
def test_add_running_mean_column_valid(table):
    """
    Test for: assert is_valid_table(table)
    """
    steps = [
             f"table = {table}",
             f"actual = hw5.add_running_mean_column(table, 'a', 'mean')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)
    
    try:
        actual = hw5.add_running_mean_column(table, 'a', 'mean')
    except Exception as AssertionError:
        return # correct
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = "\n\nInput table is invalid."
    err_msg += "\n  Expected: AssertionError"

    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)
        

table71 = copy.deepcopy(table11)
table72 = [COVID[0]] + COVID[-5:]
table73 = [LANGUAGES[0]] + LANGUAGES[-15:]

results7 = [
        [['a', 'b', 'c', 'd'], [1, 2, 3, 1], [5, 4, 6, 4], [9, 8, 6, 4]], 
        [['a', 'b', 'c', 'd'], [1, 2, 3, 2], [5, 4, 6, 2], [9, 8, 6, 4]], 
        [['Date', 'Cases - Total', 'Deaths - Total', 'Hospitalizations - Total', 'Cases - Age 0-17', 'Cases - Age 18-29', 'Cases - Age 30-39', 'Cases - Age 40-49', 'Cases - Age 50-59', 'Cases - Age 60-69', 'Cases - Age 70-79', 'Cases -  Age 80+', 'Cases - Age Unknown', 'Cases - Female', 'Cases - Male', 'Cases - Unknown Gender', 'Cases - Latinx', 'Cases - Asian Non-Latinx', 'Cases - Black Non-Latinx', 'Cases - White Non-Latinx', 'Cases - Other Race Non-Latinx', 'Cases - Unknown Race/Ethnicity', 'Deaths - Age 0-17', 'Deaths - Age 18-29', 'Deaths - Age 30-39', 'Deaths - Age 40-49', 'Deaths - Age 50-59', 'Deaths - Age 60-69', 'Deaths - Age 70-79', 'Deaths - Age 80+', 'Deaths - Age Unknown', 'Deaths - Female', 'Deaths - Male', 'Deaths - Unknown Gender', 'Deaths - Latinx', 'Deaths - Asian Non-Latinx', 'Deaths - Black Non-Latinx', 'Deaths - White Non-Latinx', 'Deaths - Other Race Non-Latinx', 'Deaths - Unknown Race/Ethnicity', 'Hospitalizations - Age 0-17', 'Hospitalizations - Age 18-29', 'Hospitalizations - Age 30-39', 'Hospitalizations - Age 40-49', 'Hospitalizations - Age 50-59', 'Hospitalizations - Age 60-69', 'Hospitalizations - Age 70-79', 'Hospitalizations - Age 80+', 'Hospitalizations - Age Unknown', 'Hospitalizations - Female', 'Hospitalizations - Male', 'Hospitalizations - Unknown Gender', 'Hospitalizations - Latinx', 'Hospitalizations - Asian Non-Latinx', 'Hospitalizations - Black Non-Latinx', 'Hospitalizations - White Non-Latinx', 'Hospitalizations - Other Race Non-Latinx', 'Hospitalizations - Unknown Race/Ethnicity', 'test'], [(2024, 1, 5), 317, 0, 40, 30, 47, 51, 39, 57, 40, 29, 24, 0, 188, 129, 0, 71, 14, 105, 88, 18, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 2, 2, 8, 13, 9, 0, 17, 23, 0, 8, 2, 16, 11, 3, 0, 40], [(2024, 1, 4), 323, 3, 40, 29, 48, 58, 40, 47, 33, 40, 28, 0, 204, 118, 1, 85, 20, 101, 88, 9, 20, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 2, 0, 1, 0, 0, 1, 1, 0, 1, 3, 3, 3, 5, 8, 6, 11, 0, 16, 24, 0, 11, 0, 15, 13, 1, 0, -7], [(2024, 1, 3), 304, 1, 44, 25, 43, 56, 41, 42, 40, 28, 29, 0, 192, 111, 1, 71, 12, 102, 77, 14, 28, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 1, 3, 2, 4, 9, 12, 11, 0, 22, 22, 0, 11, 1, 18, 11, 1, 2, 7], [(2024, 1, 2), 363, 1, 48, 28, 50, 39, 46, 42, 68, 50, 40, 0, 206, 157, 0, 83, 11, 108, 108, 33, 20, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 4, 3, 8, 9, 10, 13, 0, 22, 26, 0, 8, 1, 17, 17, 4, 1, 28], [(2024, 1, 1), 129, 1, 22, 24, 18, 20, 13, 20, 12, 12, 10, 0, 81, 48, 0, 36, 5, 38, 37, 5, 8, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 2, 6, 2, 5, 4, 0, 11, 11, 0, 3, 1, 9, 8, 1, 0, -56]], 
        [['Date', 'Cases - Total', 'Deaths - Total', 'Hospitalizations - Total', 'Cases - Age 0-17', 'Cases - Age 18-29', 'Cases - Age 30-39', 'Cases - Age 40-49', 'Cases - Age 50-59', 'Cases - Age 60-69', 'Cases - Age 70-79', 'Cases -  Age 80+', 'Cases - Age Unknown', 'Cases - Female', 'Cases - Male', 'Cases - Unknown Gender', 'Cases - Latinx', 'Cases - Asian Non-Latinx', 'Cases - Black Non-Latinx', 'Cases - White Non-Latinx', 'Cases - Other Race Non-Latinx', 'Cases - Unknown Race/Ethnicity', 'Deaths - Age 0-17', 'Deaths - Age 18-29', 'Deaths - Age 30-39', 'Deaths - Age 40-49', 'Deaths - Age 50-59', 'Deaths - Age 60-69', 'Deaths - Age 70-79', 'Deaths - Age 80+', 'Deaths - Age Unknown', 'Deaths - Female', 'Deaths - Male', 'Deaths - Unknown Gender', 'Deaths - Latinx', 'Deaths - Asian Non-Latinx', 'Deaths - Black Non-Latinx', 'Deaths - White Non-Latinx', 'Deaths - Other Race Non-Latinx', 'Deaths - Unknown Race/Ethnicity', 'Hospitalizations - Age 0-17', 'Hospitalizations - Age 18-29', 'Hospitalizations - Age 30-39', 'Hospitalizations - Age 40-49', 'Hospitalizations - Age 50-59', 'Hospitalizations - Age 60-69', 'Hospitalizations - Age 70-79', 'Hospitalizations - Age 80+', 'Hospitalizations - Age Unknown', 'Hospitalizations - Female', 'Hospitalizations - Male', 'Hospitalizations - Unknown Gender', 'Hospitalizations - Latinx', 'Hospitalizations - Asian Non-Latinx', 'Hospitalizations - Black Non-Latinx', 'Hospitalizations - White Non-Latinx', 'Hospitalizations - Other Race Non-Latinx', 'Hospitalizations - Unknown Race/Ethnicity', 'data'], [(2024, 1, 5), 317, 0, 40, 30, 47, 51, 39, 57, 40, 29, 24, 0, 188, 129, 0, 71, 14, 105, 88, 18, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 2, 2, 8, 13, 9, 0, 17, 23, 0, 8, 2, 16, 11, 3, 0, 88], [(2024, 1, 4), 323, 3, 40, 29, 48, 58, 40, 47, 33, 40, 28, 0, 204, 118, 1, 85, 20, 101, 88, 9, 20, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 2, 0, 1, 0, 0, 1, 1, 0, 1, 3, 3, 3, 5, 8, 6, 11, 0, 16, 24, 0, 11, 0, 15, 13, 1, 0, 0], [(2024, 1, 3), 304, 1, 44, 25, 43, 56, 41, 42, 40, 28, 29, 0, 192, 111, 1, 71, 12, 102, 77, 14, 28, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 1, 3, 2, 4, 9, 12, 11, 0, 22, 22, 0, 11, 1, 18, 11, 1, 2, -11], [(2024, 1, 2), 363, 1, 48, 28, 50, 39, 46, 42, 68, 50, 40, 0, 206, 157, 0, 83, 11, 108, 108, 33, 20, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 4, 3, 8, 9, 10, 13, 0, 22, 26, 0, 8, 1, 17, 17, 4, 1, 31], [(2024, 1, 1), 129, 1, 22, 24, 18, 20, 13, 20, 12, 12, 10, 0, 81, 48, 0, 36, 5, 38, 37, 5, 8, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 2, 6, 2, 5, 4, 0, 11, 11, 0, 3, 1, 9, 8, 1, 0, -71]], 
        [['Date', 'Cases - Total', 'Deaths - Total', 'Hospitalizations - Total', 'Cases - Age 0-17', 'Cases - Age 18-29', 'Cases - Age 30-39', 'Cases - Age 40-49', 'Cases - Age 50-59', 'Cases - Age 60-69', 'Cases - Age 70-79', 'Cases -  Age 80+', 'Cases - Age Unknown', 'Cases - Female', 'Cases - Male', 'Cases - Unknown Gender', 'Cases - Latinx', 'Cases - Asian Non-Latinx', 'Cases - Black Non-Latinx', 'Cases - White Non-Latinx', 'Cases - Other Race Non-Latinx', 'Cases - Unknown Race/Ethnicity', 'Deaths - Age 0-17', 'Deaths - Age 18-29', 'Deaths - Age 30-39', 'Deaths - Age 40-49', 'Deaths - Age 50-59', 'Deaths - Age 60-69', 'Deaths - Age 70-79', 'Deaths - Age 80+', 'Deaths - Age Unknown', 'Deaths - Female', 'Deaths - Male', 'Deaths - Unknown Gender', 'Deaths - Latinx', 'Deaths - Asian Non-Latinx', 'Deaths - Black Non-Latinx', 'Deaths - White Non-Latinx', 'Deaths - Other Race Non-Latinx', 'Deaths - Unknown Race/Ethnicity', 'Hospitalizations - Age 0-17', 'Hospitalizations - Age 18-29', 'Hospitalizations - Age 30-39', 'Hospitalizations - Age 40-49', 'Hospitalizations - Age 50-59', 'Hospitalizations - Age 60-69', 'Hospitalizations - Age 70-79', 'Hospitalizations - Age 80+', 'Hospitalizations - Age Unknown', 'Hospitalizations - Female', 'Hospitalizations - Male', 'Hospitalizations - Unknown Gender', 'Hospitalizations - Latinx', 'Hospitalizations - Asian Non-Latinx', 'Hospitalizations - Black Non-Latinx', 'Hospitalizations - White Non-Latinx', 'Hospitalizations - Other Race Non-Latinx', 'Hospitalizations - Unknown Race/Ethnicity', 'name'], [(2024, 1, 5), 317, 0, 40, 30, 47, 51, 39, 57, 40, 29, 24, 0, 188, 129, 0, 71, 14, 105, 88, 18, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 2, 2, 8, 13, 9, 0, 17, 23, 0, 8, 2, 16, 11, 3, 0, 0], [(2024, 1, 4), 323, 3, 40, 29, 48, 58, 40, 47, 33, 40, 28, 0, 204, 118, 1, 85, 20, 101, 88, 9, 20, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 2, 0, 1, 0, 0, 1, 1, 0, 1, 3, 3, 3, 5, 8, 6, 11, 0, 16, 24, 0, 11, 0, 15, 13, 1, 0, 0], [(2024, 1, 3), 304, 1, 44, 25, 43, 56, 41, 42, 40, 28, 29, 0, 192, 111, 1, 71, 12, 102, 77, 14, 28, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 1, 3, 2, 4, 9, 12, 11, 0, 22, 22, 0, 11, 1, 18, 11, 1, 2, 0], [(2024, 1, 2), 363, 1, 48, 28, 50, 39, 46, 42, 68, 50, 40, 0, 206, 157, 0, 83, 11, 108, 108, 33, 20, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 4, 3, 8, 9, 10, 13, 0, 22, 26, 0, 8, 1, 17, 17, 4, 1, 0], [(2024, 1, 1), 129, 1, 22, 24, 18, 20, 13, 20, 12, 12, 10, 0, 81, 48, 0, 36, 5, 38, 37, 5, 8, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 2, 6, 2, 5, 4, 0, 11, 11, 0, 3, 1, 9, 8, 1, 0, 0]], 
        [['Community Area', 'Community Area Name', 'AFRICAN LANGUAGES', 'ARABIC', 'ARMENIAN', 'CAMBODIAN (MON-KHMER)', 'CHINESE', 'CREOLE', 'FRENCH', 'GERMAN', 'GREEK', 'GUJARATI', 'HEBREW', 'HINDI', 'HMONG', 'HUNGARIAN', 'ITALIAN', 'JAPANESE', 'KOREAN', 'LAOTIAN', 'NAVAJO', 'OTHER ASIAN', 'OTHER INDIC', 'OTHER INDO EURPOEAN', 'OTHER NATIVE NORTH AMERICAN', 'OTHER PACIFIC ISLAND', 'OTHER SLAVIC', 'OTHER WEST GERMANIC', 'PERSIAN', 'POLISH', 'PORTUGUESE', 'RUSSIAN', 'SCANDINAVIAN', 'SERBO-CROATIAN', 'SPANISH', 'TAGALOG', 'THAI', 'UNSPECIFIED', 'URDU', 'VIETNAMESE', 'YIDDISH', 'test'], [63, 'Gage Park', 0, 22, 0, 0, 46, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 27, 0, 0, 10, 0, 0, 35, 0, 9, 0, 0, 16024, 8, 31, 0, 0, 57, 0, 0], [64, 'Clearing', 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 155, 0, 0, 0, 0, 0, 0, 38, 0, 0, 38, 0, 0, 873, 0, 0, 0, 33, 2642, 27, 0, 0, 0, 2, 0, 0], [65, 'West Lawn', 0, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 18, 0, 36, 0, 0, 17, 0, 0, 193, 0, 23, 0, 0, 9019, 9, 0, 0, 22, 0, 0, 0], [66, 'Chicago Lawn', 24, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 95, 0, 0, 0, 0, 181, 0, 0, 0, 0, 0, 10, 0, 10, 0, 0, 9366, 95, 0, 0, 0, 0, 0, 0], [67, 'West Englewood', 9, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 389, 0, 0, 0, 0, 0, 0, 0], [68, 'Englewood', 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 104, 10, 0, 0, 0, 0, 0, 0], [69, 'Greater Grand Crossing', 76, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 31, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 125, 0, 0, 0, 0, 0, 0, 0], [70, 'Ashburn', 53, 97, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 49, 0, 0, 0, 0, 4627, 18, 0, 0, 11, 0, 0, 0], [71, 'Auburn Gresham', 56, 0, 0, 0, 15, 66, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 27, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 203, 9, 0, 0, 0, 0, 0, 0], [72, 'Beverly', 0, 0, 0, 0, 0, 0, 52, 0, 9, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 9, 177, 5, 0, 0, 0, 0, 0, 0], [73, 'Washington Heights', 7, 0, 0, 0, 0, 0, 53, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0], [74, 'Mount Greenwood', 0, 0, 0, 0, 47, 0, 0, 18, 8, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 89, 24, 0, 0, 0, 0, 0, 0], [75, 'Morgan Park', 0, 0, 0, 0, 0, 0, 32, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 22, 0, 37, 5, 0, 126, 0, 0, 0, 0, 0, 0, 5], [76, "O'Hare", 0, 329, 0, 0, 12, 0, 0, 0, 35, 0, 0, 85, 0, 32, 105, 11, 24, 0, 0, 207, 0, 33, 0, 0, 577, 0, 30, 1463, 0, 77, 0, 437, 515, 113, 15, 0, 74, 0, 0, -5], [77, 'Edgewater', 699, 77, 12, 0, 519, 0, 43, 12, 15, 56, 0, 43, 0, 31, 11, 15, 215, 0, 0, 304, 247, 176, 0, 0, 21, 0, 3, 172, 0, 697, 0, 520, 2415, 163, 95, 0, 148, 257, 0, 0]], 
        [['Community Area', 'Community Area Name', 'AFRICAN LANGUAGES', 'ARABIC', 'ARMENIAN', 'CAMBODIAN (MON-KHMER)', 'CHINESE', 'CREOLE', 'FRENCH', 'GERMAN', 'GREEK', 'GUJARATI', 'HEBREW', 'HINDI', 'HMONG', 'HUNGARIAN', 'ITALIAN', 'JAPANESE', 'KOREAN', 'LAOTIAN', 'NAVAJO', 'OTHER ASIAN', 'OTHER INDIC', 'OTHER INDO EURPOEAN', 'OTHER NATIVE NORTH AMERICAN', 'OTHER PACIFIC ISLAND', 'OTHER SLAVIC', 'OTHER WEST GERMANIC', 'PERSIAN', 'POLISH', 'PORTUGUESE', 'RUSSIAN', 'SCANDINAVIAN', 'SERBO-CROATIAN', 'SPANISH', 'TAGALOG', 'THAI', 'UNSPECIFIED', 'URDU', 'VIETNAMESE', 'YIDDISH', 'data'], [63, 'Gage Park', 0, 22, 0, 0, 46, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 27, 0, 0, 10, 0, 0, 35, 0, 9, 0, 0, 16024, 8, 31, 0, 0, 57, 0, 0], [64, 'Clearing', 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 155, 0, 0, 0, 0, 0, 0, 38, 0, 0, 38, 0, 0, 873, 0, 0, 0, 33, 2642, 27, 0, 0, 0, 2, 0, 0], [65, 'West Lawn', 0, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 18, 0, 36, 0, 0, 17, 0, 0, 193, 0, 23, 0, 0, 9019, 9, 0, 0, 22, 0, 0, 0], [66, 'Chicago Lawn', 24, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 95, 0, 0, 0, 0, 181, 0, 0, 0, 0, 0, 10, 0, 10, 0, 0, 9366, 95, 0, 0, 0, 0, 0, 0], [67, 'West Englewood', 9, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 389, 0, 0, 0, 0, 0, 0, 0], [68, 'Englewood', 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 104, 10, 0, 0, 0, 0, 0, 0], [69, 'Greater Grand Crossing', 76, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 31, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 125, 0, 0, 0, 0, 0, 0, 0], [70, 'Ashburn', 53, 97, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 49, 0, 0, 0, 0, 4627, 18, 0, 0, 11, 0, 0, 0], [71, 'Auburn Gresham', 56, 0, 0, 0, 15, 66, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 27, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 203, 9, 0, 0, 0, 0, 0, 0], [72, 'Beverly', 0, 0, 0, 0, 0, 0, 52, 0, 9, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 9, 177, 5, 0, 0, 0, 0, 0, 0], [73, 'Washington Heights', 7, 0, 0, 0, 0, 0, 53, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0], [74, 'Mount Greenwood', 0, 0, 0, 0, 47, 0, 0, 18, 8, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 89, 24, 0, 0, 0, 0, 0, 0], [75, 'Morgan Park', 0, 0, 0, 0, 0, 0, 32, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 22, 0, 37, 5, 0, 126, 0, 0, 0, 0, 0, 0, 0], [76, "O'Hare", 0, 329, 0, 0, 12, 0, 0, 0, 35, 0, 0, 85, 0, 32, 105, 11, 24, 0, 0, 207, 0, 33, 0, 0, 577, 0, 30, 1463, 0, 77, 0, 437, 515, 113, 15, 0, 74, 0, 0, 0], [77, 'Edgewater', 699, 77, 12, 0, 519, 0, 43, 12, 15, 56, 0, 43, 0, 31, 11, 15, 215, 0, 0, 304, 247, 176, 0, 0, 21, 0, 3, 172, 0, 697, 0, 520, 2415, 163, 95, 0, 148, 257, 0, 247]]
    ]

@pytest.mark.parametrize("table, column, name, expected",
    [(table71, 'a', "d", results7[0]),
     (table71, 'b', "d", results7[1]),
     (table72, table72[0][9], "test", results7[2]), 
     (table72, table72[0][19], "data", results7[3]), 
     (table72, table72[0][25], "name", results7[4]), 
     (table73, table73[0][-9], "test", results7[5]), 
     (table73, table73[0][-19], "data", results7[6]), 
     ]
     )
def test_add_difference_column(table, column, name, expected):
    """
    Test code for Exercise 7: add_difference_column with default values
    """
    steps = [
             f"table = {table}",
             f"hw5.add_difference_column(table, '{column}', '{name}')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    work_table = copy.deepcopy(table)

    try:
        hw5.add_difference_column(work_table, column, name)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)


    err_msg = helpers.check_2D_vals(lambda x, y: x == y,
                                       work_table,
                                       expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

results7a = [
        [['a', 'b', 'c', 'd'], [1, 2, 3, 1], [5, 4, 6, 4], [9, 8, 6, 4]], 
        [['a', 'b', 'c', 'd'], [1, 2, 3, 2], [5, 4, 6, 2], [9, 8, 6, 4]], 
        [['a', 'b', 'c', 'd'], [1, 2, 3, -8], [5, 4, 6, 2], [9, 8, 6, 4]], 
        [['a', 'b', 'c', 'd'], [1, 2, 3, 21], [5, 4, 6, 4], [9, 8, 6, 4]], 
        [['Date', 'Cases - Total', 'Deaths - Total', 'Hospitalizations - Total', 'Cases - Age 0-17', 'Cases - Age 18-29', 'Cases - Age 30-39', 'Cases - Age 40-49', 'Cases - Age 50-59', 'Cases - Age 60-69', 'Cases - Age 70-79', 'Cases -  Age 80+', 'Cases - Age Unknown', 'Cases - Female', 'Cases - Male', 'Cases - Unknown Gender', 'Cases - Latinx', 'Cases - Asian Non-Latinx', 'Cases - Black Non-Latinx', 'Cases - White Non-Latinx', 'Cases - Other Race Non-Latinx', 'Cases - Unknown Race/Ethnicity', 'Deaths - Age 0-17', 'Deaths - Age 18-29', 'Deaths - Age 30-39', 'Deaths - Age 40-49', 'Deaths - Age 50-59', 'Deaths - Age 60-69', 'Deaths - Age 70-79', 'Deaths - Age 80+', 'Deaths - Age Unknown', 'Deaths - Female', 'Deaths - Male', 'Deaths - Unknown Gender', 'Deaths - Latinx', 'Deaths - Asian Non-Latinx', 'Deaths - Black Non-Latinx', 'Deaths - White Non-Latinx', 'Deaths - Other Race Non-Latinx', 'Deaths - Unknown Race/Ethnicity', 'Hospitalizations - Age 0-17', 'Hospitalizations - Age 18-29', 'Hospitalizations - Age 30-39', 'Hospitalizations - Age 40-49', 'Hospitalizations - Age 50-59', 'Hospitalizations - Age 60-69', 'Hospitalizations - Age 70-79', 'Hospitalizations - Age 80+', 'Hospitalizations - Age Unknown', 'Hospitalizations - Female', 'Hospitalizations - Male', 'Hospitalizations - Unknown Gender', 'Hospitalizations - Latinx', 'Hospitalizations - Asian Non-Latinx', 'Hospitalizations - Black Non-Latinx', 'Hospitalizations - White Non-Latinx', 'Hospitalizations - Other Race Non-Latinx', 'Hospitalizations - Unknown Race/Ethnicity', 'test'], [(2024, 1, 5), 317, 0, 40, 30, 47, 51, 39, 57, 40, 29, 24, 0, 188, 129, 0, 71, 14, 105, 88, 18, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 2, 2, 8, 13, 9, 0, 17, 23, 0, 8, 2, 16, 11, 3, 0, 27], [(2024, 1, 4), 323, 3, 40, 29, 48, 58, 40, 47, 33, 40, 28, 0, 204, 118, 1, 85, 20, 101, 88, 9, 20, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 2, 0, 1, 0, 0, 1, 1, 0, 1, 3, 3, 3, 5, 8, 6, 11, 0, 16, 24, 0, 11, 0, 15, 13, 1, 0, -7], [(2024, 1, 3), 304, 1, 44, 25, 43, 56, 41, 42, 40, 28, 29, 0, 192, 111, 1, 71, 12, 102, 77, 14, 28, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 1, 3, 2, 4, 9, 12, 11, 0, 22, 22, 0, 11, 1, 18, 11, 1, 2, 7], [(2024, 1, 2), 363, 1, 48, 28, 50, 39, 46, 42, 68, 50, 40, 0, 206, 157, 0, 83, 11, 108, 108, 33, 20, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 4, 3, 8, 9, 10, 13, 0, 22, 26, 0, 8, 1, 17, 17, 4, 1, 28], [(2024, 1, 1), 129, 1, 22, 24, 18, 20, 13, 20, 12, 12, 10, 0, 81, 48, 0, 36, 5, 38, 37, 5, 8, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 2, 6, 2, 5, 4, 0, 11, 11, 0, 3, 1, 9, 8, 1, 0, -56]]
    ]
@pytest.mark.parametrize("table, column, name, initial, expected",
    [(table71, 'a', "d", 0, results7a[0]),
     (table71, 'b', "d", 0, results7a[1]),
     (table71, 'b', "d", 10, results7a[2]),
     (table71, 'a', "d", -20, results7a[3]),
     (table72, table72[0][9], "test", 13, results7a[4]),
     ]
     )
def test_add_difference_column_optional(table, column, name, initial, expected):
    """
    Test code for Exercise 7: add_difference_column with optional argument
    """
    steps = [
             f"table = {table}",
             f"hw5.add_difference_column(table, '{column}', '{name}', start_from={initial})"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    work_table = copy.deepcopy(table)

    try:
        hw5.add_difference_column(work_table, column, name, start_from=initial)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)


    err_msg = helpers.check_2D_vals(lambda x, y: x == y,
                                       work_table,
                                       expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)
        

@pytest.mark.parametrize("table",
                         [(table22), (table23)])
def test_add_difference_column_valid(table):
    """
    Test for: assert is_valid_table(table)
    """
    steps = [
             f"table = {table}",
             f"actual = hw5.add_difference_column(table, 'a', 'mean')"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)
    
    try:
        actual = hw5.add_difference_column(table, 'a', 'diff')
    except Exception as AssertionError:
        return # correct
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = "\n\nInput table is invalid."
    err_msg += "\n  Expected: AssertionError"

    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)
        
        
table81 = copy.deepcopy(table11)
table82 = [['trick', 'or', 'treat'], [1]*3, [0]*3]
table83 = ([["crow", "cat", "owl", "snake"]] 
           + [row[10:14] for row in LANGUAGES[1:5]])
table84 = ([["bread", "rice", "noodles", "pasta", "corn"]] 
           + [row[-6:-1] for row in LANGUAGES[15:20]])
table85 = ([["bread", "rice", "noodles", "pasta", "corn"]] 
           + [row[-6:-1] for row in LANGUAGES[15:20]])
table86 = ([["term", "diction", "grammar", "crinkle", "suspect", "hammer"]] 
           + [row[-7:-1] for row in LANGUAGES[20:30]])
table87 = ([["car", "trouble", "break", "pixel"]] 
           + [row[-4:] for row in AUTUMN2024[15:35]])
table88 = ([["try", "fiction", "junction", "shelter", "crisp", "chill", "trust"]] 
           + [row[-8:-1] for row in LANGUAGES[15:30]])
table89 = ([["weather", "wire", "helicopter", "trace", "Eglinton", "pickle", "cricket", "string", "language"]] 
           + [row[-10:-1] for row in LANGUAGES[-20:]])
results8 = [
        [],
        [('a', 0.0), ('b', 0.0), ('c', 0.0)], 
        [('trick', 0.30102999566398114), ('or', 0.30102999566398114), ('treat', 0.30102999566398114)], 
        [('crow', 0.1249387366082999), ('cat', 0.30102999566398114), ('owl', 0.6020599913279623), ('snake', 0.1249387366082999)], 
        [('bread', 0.0), ('rice', 0.22184874961635637), ('noodles', 0.3979400086720376), ('pasta', 0.3979400086720376), ('corn', 0.22184874961635637)], 
        [('bread', 0.0), ('rice', 0.22184874961635637), ('noodles', 0.3979400086720376), ('pasta', 0.3979400086720376), ('corn', 0.22184874961635637)], 
        [('term', 0.0), ('diction', 0.0969100130080564), ('grammar', 0.3979400086720376), ('crinkle', 1.0), ('suspect', 0.5228787452803376), ('hammer', 0.5228787452803376)], 
        [('car', 0.1249387366082999), ('trouble', 0.0), ('break', 0.22184874961635637), ('pixel', 1.0)], 
        [('try', 0.22184874961635637), ('fiction', 0.0), ('junction', 0.06214790674884443), ('shelter', 0.33099321904142437), ('crisp', 0.6989700043360187), ('chill', 0.47712125471966244), ('trust', 0.3979400086720376)], 
        [('weather', 0.34678748622465627), ('wire', 1.301029995663981), ('helicopter', 0.4559319556497243), ('trace', 0.0), ('Eglinton', 0.15490195998574316), ('pickle', 0.5228787452803376), ('cricket', 1.301029995663981), ('string', 0.6989700043360187), ('language', 0.6020599913279623)]
    ]
@pytest.mark.parametrize("table, expected",
    [(table81, results8[1]),
     (table82, results8[2]),
     (table83, results8[3]),
     (table84, results8[4]),
     (table85, results8[5]),
     (table86, results8[6]),
     (table87, results8[7]),
     (table88, results8[8]),
     (table89, results8[9]),
     ]
     )
def test_inverse_document_frequency(table, expected):
    """
    Test code for Exercise 8: inverse_document_frequency
    """
    steps = [
             f"table = {table}",
             f"actual = hw5.inverse_document_frequency(table)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    table_copy = copy.deepcopy(table) # check that the table wasn't modified

    try:
        actual = hw5.inverse_document_frequency(table)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

    err_msg = helpers.check_2D_list_unmodified("table", table_copy, table)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

@pytest.mark.parametrize("table",
                         [(table22), (table23)])
def test_inverse_document_frequency_valid(table):
    """
    Test for: assert is_valid_table(table)
    """
    steps = [
             f"table = {table}",
             f"actual = hw5.inverse_document_frequency(table)"]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)
    
    try:
        actual = hw5.inverse_document_frequency(table, ['a'])
    except Exception as AssertionError:
        return # correct
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = "\n\nInput table is invalid."
    err_msg += "\n  Expected: AssertionError"

    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

        
