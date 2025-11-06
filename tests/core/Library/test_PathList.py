from buildpp.library import PathList

import pytest
from pathlib import Path


absPaths = [Path(__file__).parent / "foo",
            Path(__file__) / "bar.py",
            Path(__file__) / "pp.py"]

relPaths = ["../foo",
            "bar",
            "pp.py"]


# ____________________CONSTRUCTORS____________________
def test_PathList_constructEmpty():

    test = PathList()

    assert test.paths == []


def test_PathList_constructWithRoot():

    test = PathList(Path(__file__))

    assert test.root == Path(__file__)


# ____________________ABSOLUTE_PATHS____________________
def test_PathList_addAbs_Path():

    test = PathList()

    for path in absPaths:
        test.addAbs(path)

    assert sorted(test.paths) == sorted(absPaths)


def test_PathList_addAbs_List():

    test = PathList()

    test.addAbs(absPaths)

    assert sorted(test.paths) == sorted(absPaths)


def test_PathList_addAbs_TypeError():

    test = PathList()

    with pytest.raises(AssertionError):
        test.addAbs("foo")

    with pytest.raises(AssertionError):
        test.addAbs(relPaths)

    with pytest.raises(AssertionError):
        test.addAbs([Path(__file__), "ele", Path(__file__)])


# ____________________RELATIVE_PATHS____________________
def test_PathList_addRel_noRoot():

    test = PathList()

    with pytest.raises(AssertionError):

        test.addRel("wrong")

    with pytest.raises(AssertionError):

        test.addRel(["w", "p"])


def test_PathList_addRel_str():

    test = PathList(Path(__file__).parent)

    for path in relPaths:
        test.addRel(path)

    assert sorted(test.paths) == sorted([Path(__file__).parent / ele for ele in relPaths])


def test_PathList_addRel_list():

    test = PathList(Path(__file__).parent)

    test.addRel(relPaths)

    assert sorted(test.paths) == sorted([Path(__file__).parent / ele for ele in relPaths])


def test_PathList_addRel_TypeError():

    test = PathList(Path(__file__).parent)

    with pytest.raises(AssertionError):
        test.addRel(Path(__file__))

    with pytest.raises(AssertionError):
        test.addRel(absPaths)

    with pytest.raises(AssertionError):
        test.addRel(["foo", Path(), "foo"])


# ____________________._LIST_ATTRIBUTE____________________
def test_PathList_list_attribute():

    test = PathList()

    assert test.paths == test._list and test.paths == []

    test.addAbs(absPaths)

    assert test.paths == test._list and sorted(test.paths) == sorted(absPaths)
