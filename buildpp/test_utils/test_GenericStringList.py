from buildpp.__utils import GenericStringList

import pytest


@pytest.mark.dependency()
class Test_GenericStringList:

    def test_constructEmpty(self):

        test = GenericStringList()
        assert test.list == []

    def test_add_str(self):

        test = GenericStringList()

        test.add("foo")

        assert test.list == ["foo"]

        test.add("bar")

        assert sorted(test.list) == sorted(["foo", "bar"])

    def test_addlist(self):

        test = GenericStringList()

        testList = ["foo", "bar", "67"]
        test.add(testList)

        assert sorted(test.list) == sorted(testList)

    def test_construct_str(self):

        test = GenericStringList("foo")

        assert test.list == ["foo"]

    def test_constructlist(self):

        testList = ["foo", "bar", "i"]

        test = GenericStringList(testList)

        assert sorted(test.list) == sorted(testList)

    def test_constructAndAdd(self):

        test = GenericStringList("foo")
        test.add(["foo", "test"])

        assert sorted(test.list) == sorted(["foo", "foo", "test"])

    def test_construct_TypeErrAssert(self):

        test = GenericStringList("foo")

        with pytest.raises(AssertionError):
            test.add(67)

        with pytest.raises(AssertionError):
            test.add(["foo", 76, "ko"])

        with pytest.raises(AssertionError):
            GenericStringList(4.0)

        with pytest.raises(AssertionError):
            GenericStringList(["list", "array", 9])
