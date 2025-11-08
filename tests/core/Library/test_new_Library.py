from buildpp import new_Library
from buildpp import LibType

import pytest


def test_new_library():

    test = new_Library("testLib", LibType.SHARED)

    assert test.libType == LibType.SHARED

    test = new_Library("testLib", LibType.STATIC)

    assert test.libType == LibType.STATIC


def test_new_Library_TypeError():

    with pytest.raises(AssertionError):
        new_Library(6)

    with pytest.raises(AssertionError):
        new_Library("name", [])

    with pytest.raises(AssertionError):
        new_Library([], [])
