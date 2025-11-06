from buildpp.library import SourcesList


def test_SourcesList_construct_empty():

    test = SourcesList()

    assert test.sources == []


def test_SourcesList_construct_str():

    test = SourcesList("foo")

    assert test.sources == ["foo"]


def test_SourcesList_construct_list():

    testList = ["foo", "build", "make"]
    test = SourcesList(testList)

    assert test.sources == testList
