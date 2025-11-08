from buildpp import PathList, IncludeDirsList, new_AbsIncludeDirsList, new_RelIncludeDirsList

from test_PathList import absPaths, relPaths

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
    assert sorted(test.dirs) == sorted(absPaths)
    assert test.root == Path(__file__) and test.root == var.root

    # dirs only
    var = PathList()
    var.addAbs(absPaths)

    test = IncludeDirsList(var)
    assert sorted(test.dirs) == sorted(absPaths)
    assert test.root is None


def test_IncludeDirsList_new_AbsIncludeDirsList():

    test = new_AbsIncludeDirsList(absPaths)

    assert test.root is None
    assert sorted(test.dirs) == sorted(absPaths)


def test_IncludeDirsList_new_RelIncludeDirsList():

    test = new_RelIncludeDirsList(relPaths)

    assert test.root == Path(__file__).parent
    assert sorted(test.dirs) == sorted([Path(__file__).parent / x for x in relPaths])

    testRoot = Path("testPath")
    test = new_RelIncludeDirsList(relPaths, testRoot)

    assert test.root == testRoot
    assert sorted(test.dirs) == sorted([testRoot / x for x in relPaths])
