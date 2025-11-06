from buildpp.utils import GenericStringList

import pytest


def test_GenericStringList_constructEmpty():

    test = GenericStringList()
    assert test._list == []


def test_GenericStringList_add_str():

    test = GenericStringList()

    test.add("foo")

    assert test._list == ["foo"]

    test.add("bar")

    assert sorted(test._list) == sorted(["foo", "bar"])


def test_GenericStringList_add_list():

    test = GenericStringList()

    testList = ["foo", "bar", "67"]
    test.add(testList)

    assert sorted(test._list) == sorted(testList)


def test_GenericStringList_construct_str():

    test = GenericStringList("foo")

    assert test._list == ["foo"]


def test_GenericStringList_construct_list():

    testList = ["foo", "bar", "i"]

    test = GenericStringList(testList)

    assert sorted(test._list) == sorted(testList)


def test_GenericStringList_constructAndAdd():

    test = GenericStringList("foo")
    test.add(["foo", "test"])

    assert sorted(test._list) == sorted(["foo", "foo", "test"])


def test_GenericStringList_construct_TypeErrAssert():

    test = GenericStringList("foo")

    with pytest.raises(AssertionError):
        test.add(67)

    with pytest.raises(AssertionError):
        test.add(["foo", 76, "ko"])

    with pytest.raises(AssertionError):
        GenericStringList(4.0)

    with pytest.raises(AssertionError):
        GenericStringList(["list", "array", 9])
