from buildpp.library import PathList, IncludeDirsList, new_AbsIncludeDirsList, new_RelIncludeDirsList

from test_PathList import absPaths

from pathlib import Path


# Not doing much testing here, in principle very shallow over PathList
# Could copy PathList tests over here but i dont see any point in that
# ____________________CONSTRUCTORS____________________
def test_IncludeDirsList_constructEmpty():

    test = IncludeDirsList()

    assert test.dirs == []
    assert test.root is None


def test_IncludeDirsList_construct_PathList():

    # empty PathList
    test = IncludeDirsList(PathList())

    assert test.dirs == []
    assert test.root is None

    # root only
    var = PathList(Path(__file__))

    test = IncludeDirsList(var)

    assert test.dirs == []
    assert test.root == Path(__file__) and test.root == var.root

    # paths and root
    var.addAbs(absPaths)

    test = IncludeDirsList(var)
    assert test.dirs == absPaths
    assert test.root == Path(__file__) and test.root == var.root

    # dirs only
    var = PathList()
    var.addAbs(absPaths)

    test = IncludeDirsList(var)
    assert test.dirs == absPaths
    assert test.root is None
