import pytest
import os
import numpy as np
import pandas as pd
import hw5pandas as hw5


# helper function for task3 tests
def read_expected(file: str) -> pd.DataFrame:
    return pd.read_csv(f"expected/{file}.csv").reset_index(drop=True)


def test_task3a_01() -> None:
    df = hw5.players_by_name_fragment("Homer Simpson")
    assert len(df) == 0


def test_task3a_02() -> None:
    df = hw5.players_by_name_fragment("Carmelo").reset_index(drop=True)
    expected = pd.DataFrame(
        {"personId": {0: 2546}, "personName": {0: "Carmelo Anthony"}}
    )
    cols = ["personId", "personName"]
    pd.testing.assert_frame_equal(df[cols], expected[cols])


def test_task3a_03() -> None:
    df = hw5.players_by_name_fragment("curry").reset_index(drop=True)
    expected = pd.DataFrame(
        {
            "personId": {0: 201939, 1: 203552, 2: 2201},
            "personName": {
                0: "Stephen Curry",
                1: "Seth Curry",
                2: "Eddy Curry",
            },
        }
    )
    cols = ["personId", "personName"]
    pd.testing.assert_frame_equal(df[cols], expected[cols])


def test_task3a_04() -> None:
    df = hw5.players_by_name_fragment("SMITH").reset_index(drop=True)
    expected = read_expected("smith")
    cols = ["personId", "personName"]
    pd.testing.assert_frame_equal(df[cols], expected[cols])


def test_task3b_01() -> None:
    with pytest.raises(ValueError):
        df = hw5.ppg_by_name("Homer Simpson")


def test_task3b_02() -> None:
    ppg = hw5.ppg_by_name("Seth Curry")
    assert pytest.approx(ppg) == np.float64(8.890459363957596)


def test_task3b_03() -> None:
    ppg = hw5.ppg_by_name("Stephen Curry")
    assert pytest.approx(ppg) == np.float64(24.579470198675498)


def test_task3c_01() -> None:
    with pytest.raises(ValueError):
        df = hw5.played_for("NO-SUCH-TEAM")


def test_task3c_02() -> None:
    pf = hw5.played_for("MIN")
    assert pf is not None  # to placate mypy
    pf = pf.reset_index(drop=True)
    expected = read_expected("played_for_MIN")
    cols = ["personId", "personName"]
    pd.testing.assert_frame_equal(pf[cols].sort_values("personId").reset_index(drop=True),
                                  expected[cols].sort_values("personId").reset_index(drop=True),
                                  check_like=True)

def test_task3c_03() -> None:
    pf = hw5.played_for("SAS")
    assert pf is not None  # to placate mypy
    pf = pf.reset_index(drop=True)
    expected = read_expected("played_for_SAS")
    cols = ["personId", "personName"]
    pd.testing.assert_frame_equal(pf[cols].sort_values("personId").reset_index(drop=True),
                                  expected[cols].sort_values("personId").reset_index(drop=True),
                                  check_like=True)


def test_task3d_01() -> None:
    with pytest.raises(ValueError):
        s = hw5.top_n_scorers_by_team("NO-SUCH-TEAM", 99)


def test_task3d_02() -> None:
    pf = hw5.top_n_scorers_by_team("UTA", 1)
    assert pf is not None  # placate mypy
    pf = pf.reset_index(drop=True)
    expected = read_expected("uta1")
    cols = ["personId", "personName"]
    pd.testing.assert_frame_equal(pf[cols], expected[cols])


def test_task3d_03() -> None:
    pf = hw5.top_n_scorers_by_team("BOS", 24)
    assert pf is not None  # placate mypy
    pf = pf.reset_index(drop=True)
    expected = read_expected("bos24")
    cols = ["personId", "personName"]
    pd.testing.assert_frame_equal(pf[cols], expected[cols])


def test_task3e_01() -> None:
    with pytest.raises(ValueError):
        x = hw5.played_on_both("NO-SUCH-TEAM", "NOT-A-TEAM")


def test_task3e_02() -> None:
    s = hw5.played_on_both("DAL", "MEM")
    expected = {
        "Vince Carter",
        "Brandan Wright",
        "O.J. Mayo",
        "Wayne Ellington",
        "Jae Crowder",
        "Courtney Lee",
        "James Johnson",
        "Chandler Parsons",
        "Justin Holiday",
        "Seth Curry",
        "Delon Wright",
        "Jarrod Uthoff",
        "Tyler Dorsey",
        "Tyrell Terry",
    }
    assert s == expected


def test_task3f_01() -> None:
    df = hw5.top_n_scorers_by_division("Atlantic", 1).reset_index(drop=True)
    expected = pd.DataFrame(
        {
            "personId": {0: 201142},
            "personName": {0: "Kevin Durant"},
            "ppg": {0: 27.529412},
        }
    )
    cols = ["personId", "personName", "ppg"]
    pd.testing.assert_frame_equal(df[cols], expected[cols])


def test_task3f_02() -> None:
    df = hw5.top_n_scorers_by_division("Pacific", 50).reset_index(drop=True)
    expected = read_expected("pac50")
    cols = ["personId", "personName", "ppg"]
    dfL = df[cols].sort_values(by="personId").reset_index(drop=True)
    dfR = expected[cols].sort_values(by="personId").reset_index(drop=True)
    pd.testing.assert_frame_equal(dfL, dfR)


def test_task3g_01() -> None:
    s = hw5.played_on_date("1980-09-09")  # no one played on that date
    assert s == set()


def test_task3g_02() -> None:
    s = hw5.played_on_date("2012-12-01")
    expected = read_expected("played_20121201")
    t = set(expected["personName"].values)
    assert s == t


def test_task3g_03() -> None:
    s = hw5.played_on_date("2015-12-25") & hw5.played_on_date("2016-01-25")
    expected = read_expected("played_20151225_20160125")
    t = set(expected["personName"].values)
    assert s == t
