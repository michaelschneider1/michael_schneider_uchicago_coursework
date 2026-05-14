import pytest
import os
from hw5numpy import NDArray, NDArray1, NDArray2


def test_task1_init1() -> None:
    d = NDArray1([1, 2, 3])
    assert len(d.values()) == 3


def test_task1_pow0() -> None:
    d = NDArray1([1, 2, 3])
    assert (d**0).values() == [1, 1, 1]


def test_task1_pow2() -> None:
    d = NDArray1([1, 2, 3])
    assert (d**2).values() == [1, 4, 9]


def test_task1_pow3() -> None:
    d = NDArray1(list(range(1000)))
    assert (d**3).values() == list(map(lambda n: n**3, range(1000)))


def test_task1_pow4() -> None:
    d = NDArray1(list(range(100)))
    assert ((d**2) ** 2).values() == list(map(lambda n: n**4, range(100)))


def test_task1_pow5() -> None:
    d = NDArray1([10, 20, 30, 200, 300, 400])
    assert (((d**2) ** 2) ** 0).values() == [1, 1, 1, 1, 1, 1]


def test_task1_neg1() -> None:
    d = NDArray1([1, 2, 3])
    assert (-d).values() == [-1, -2, -3]


def test_task1_neg2() -> None:
    d = NDArray1(list(range(1000)))
    assert (-d).values() == list(map(lambda n: -1 * n, range(1000)))


def test_task1_neg3() -> None:
    d = NDArray1(list(range(1000)))
    assert (-(-d)).values() == d.values()


def test_task1_iadd0() -> None:
    d = NDArray1([1, 2, 3])
    d += 0
    assert d.values() == [1, 2, 3]


def test_task1_iadd1() -> None:
    d = NDArray1([1, 2, 3])
    d += 1
    assert d.values() == [2, 3, 4]


def test_task1_iadd2() -> None:
    d = NDArray1(list(range(9999)))
    d += 2
    assert d.values() == list(range(2, 9999 + 2))


def test_task1_isub0() -> None:
    d = NDArray1([1, 2, 3])
    d -= 0
    assert d.values() == [1, 2, 3]


def test_task1_isub1() -> None:
    d = NDArray1([1, 2, 3])
    d -= 1
    assert d.values() == [0, 1, 2]


def test_task1_isub2() -> None:
    d = NDArray1(list(range(9999)))
    d -= 2
    assert d.values() == list(range(-2, 9997))


def test_task1_gt0() -> None:
    d = NDArray1(list(range(100)))
    assert (d > -1) == ([True] * 100)


def test_task1_gt1() -> None:
    d = NDArray1(list(range(100)))
    expected = ([False] * 50) + ([True] * 50)
    assert (d > 49) == expected


def test_task1_gt2() -> None:
    d = NDArray1([1, 0] * 100)
    expected = [True, False] * 100
    assert (d > 0) == expected


def test_task1_contains1() -> None:
    d = NDArray1([1, 2, 3])
    assert 1 in d


def test_task1_contains2() -> None:
    d = NDArray1([1, 2, 3])
    assert 11 not in d


def test_task1_contains3() -> None:
    d = NDArray1(list(range(1000)))
    assert 123 in d


def test_task1_contains4() -> None:
    d = NDArray1(list(range(1000)))
    assert 999 in d


def test_task1_contains5() -> None:
    d = NDArray1(list(range(1000)))
    assert 9999 not in d


def test_task1_shape1() -> None:
    d = NDArray1([1, 2, 3])
    assert d.shape() == 3


def test_task1_shape2() -> None:
    d = NDArray1(list(range(1000)))
    assert d.shape() == 1000


def test_task1_eq1() -> None:
    d = NDArray1([1, 2, 3])
    e = NDArray1([1, 2, 3])
    assert d == e and e == d and d is not e and e is not d


def test_task1_eq2() -> None:
    d = NDArray1([1, 2, 3])
    e = NDArray1([3, 2, 1])
    assert d != e and e != d


def test_task1_eq3() -> None:
    d = NDArray1(list(range(789)))
    e = NDArray1(list(range(789)))
    assert d == e and e == d and d is not e and e is not d


def test_task1_eq4() -> None:
    d = NDArray1(list(range(789)))
    assert d != "Chicago"


def test_task1_flatten1() -> None:
    d = NDArray1([1, 2, 3, 4, 5])
    assert d.flatten().values() == [1, 2, 3, 4, 5]


def test_task1_reshape1() -> None:
    d = NDArray1([1, 2, 3])
    assert d.reshape(3, 1).values() == [[1], [2], [3]]


def test_task1_reshape2() -> None:
    d = NDArray1([1])
    assert d.reshape(1, 1).values() == [[1]]


def test_task1_reshape3() -> None:
    d = NDArray1(list(range(100)))
    assert d.reshape(100, 1).values() == list(map(lambda n: [n], range(100)))


def test_task1_reshape4() -> None:
    d = NDArray1([1, 2, 3])
    with pytest.raises(ValueError):
        d.reshape(1, 2)


def test_task2_init1() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    assert d.shape() == (2, 3)


def test_task2_init2() -> None:
    with pytest.raises(ValueError):
        d = NDArray2([[1, 2, 3], [4, 5, 6, 7]])


def test_task2_init3() -> None:
    with pytest.raises(ValueError):
        d = NDArray2([[1, 2, 3], [4, 7]])


def test_task2_pow0() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    assert (d**0).values() == [[1, 1, 1], [1, 1, 1]]


def test_task2_pow1() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    assert (d**1).values() == d.values()


def test_task2_pow2() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    assert (d**2).values() == [[1, 4, 9], [16, 25, 36]]


def test_task2_pow3() -> None:
    d = NDArray2([[-1, 2, -3], [4, -5, 6]])
    assert (d**2).values() == [[1, 4, 9], [16, 25, 36]]


def test_task2_neg0() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    assert (-d).values() == [[-1, -2, -3], [-4, -5, -6]]


def test_task2_neg1() -> None:
    d = NDArray2(
        [[1, 2, 3, -7, -8], [4, 5, 6, -9, -6], [-22, 0, -11, -22, 33]]
    )
    assert (-(-d)).values() == d.values()


def test_task2_iadd0() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    d += 0
    assert d.values() == [[1, 2, 3], [4, 5, 6]]


def test_task2_iadd1() -> None:
    d = NDArray2([[1, 2, 3, 8], [4, 5, 6, 9]])
    d += 1
    assert d.values() == [[2, 3, 4, 9], [5, 6, 7, 10]]


def test_task2_iadd2() -> None:
    d = NDArray2([[1, 2], [3, 8], [4, 5], [6, 9]])
    d += 2
    assert d.values() == [[3, 4], [5, 10], [6, 7], [8, 11]]


def test_task2_isub0() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    d -= 0
    assert d.values() == [[1, 2, 3], [4, 5, 6]]


def test_task2_isub1() -> None:
    d = NDArray2([[1, 2, 3, 8], [4, 5, 6, 9]])
    d -= 1
    assert d.values() == [[0, 1, 2, 7], [3, 4, 5, 8]]


def test_task2_isub2() -> None:
    d = NDArray2([[1, 2], [3, 8], [4, 5], [6, 9]])
    d -= 2
    assert d.values() == [[-1, 0], [1, 6], [2, 3], [4, 7]]


def test_task2_gt0() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    assert (d > 0) == [[True] * 3] * 2


def test_task2_gt1() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    assert (d > 1) == [[False, True, True], [True, True, True]]


def test_task2_gt2() -> None:
    d = NDArray2([[1, 2, 300, 4], [4, 500, 6, 7], [33, 43, 53, 13]])
    assert (d > 22) == [
        [False, False, True, False],
        [False, True, False, False],
        [True, True, True, False],
    ]


def test_task2_contains0() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    assert 1 in d


def test_task2_contains1() -> None:
    d = NDArray2([[1, 2, 3, 7], [4, 5, 6, 9]])
    assert 2 in d and 6 in d


def test_task2_contains2() -> None:
    d = NDArray2([[1, 2], [3, 4], [5, 6]])
    assert 0 not in d and 66 not in d


def test_task2_eq1() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    e = NDArray2([[1, 2, 3], [4, 5, 6]])
    assert d == e and e == d and d is not e and e is not d


def test_task2_eq2() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    e = "foo"
    assert d != e


def test_task2_eq3() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    e = NDArray2([[1, 2], [3, 4], [5, 6]])
    assert d != e


def test_task2_eq4() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    e = NDArray1([1, 2, 3, 4, 5, 6])
    assert d != e and e != d


def test_task2_eq5() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    e = NDArray2([[1, 2, 3], [4, 0, 6]])
    assert d != e


def test_task2_eq6() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    e = NDArray2([[1, 2, 3], [4, 5, 69]])
    assert d != e


def test_task2_shape1() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    assert d.shape() == (2, 3)


def test_task2_shape2() -> None:
    d = NDArray2([[1, 2], [3, 4], [5, 6]])
    assert d.shape() == (3, 2)


def test_task2_flatten1() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    assert d.flatten().values() == [1, 2, 3, 4, 5, 6]


def test_task2_flatten2() -> None:
    d = NDArray2([[], [], []])
    assert d.shape() == (3, 0)
    assert d.flatten().shape() == 0 and d.flatten().values() == []


def test_task2_reshape1() -> None:
    d = NDArray2([[1, 2, 3], [4, 5, 6]])
    assert d.reshape(3, 2).shape() == (3, 2) and d.reshape(3, 2).values() == [
        [1, 2],
        [3, 4],
        [5, 6],
    ]


def test_task2_reshape2() -> None:
    d = NDArray2([[1], [2], [3]])
    assert d.reshape(1, 3).shape() == (1, 3) and d.reshape(1, 3).values() == [
        [1, 2, 3]
    ]


def test_task2_reshape3() -> None:
    d = NDArray2([[1], [2], [3]])
    with pytest.raises(ValueError):
        d.reshape(1, 2)


def test_task2_reshape4() -> None:
    n = 24
    d = NDArray1(list(range(n)))
    for r in range(n):
        for c in range(n):
            if r * c == n:
                assert d.reshape(r, c).shape() == (r, c), f"{n} {r} {c}"
            else:
                with pytest.raises(ValueError):
                    d.reshape(r, c)
