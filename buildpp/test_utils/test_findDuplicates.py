from buildpp.utils import findDuplicates
from .utils import multiCopyRange

__all__ = []


def test_findDuplicates_empty():

    assert findDuplicates([]) == []


def test_findDuplicates_simpleRanges():

    assert findDuplicates([x for x in range(0, 50)]) == []
    assert findDuplicates([x for x in range(-100, 100)]) == []
    assert findDuplicates([x for x in range(100, 50, -1)]) == []
    assert findDuplicates([x for x in range(0, 5000, 100)]) == []


def test_findDuplicates_bigRange():

    assert findDuplicates([x for x in range(0, 1000000)]) == []


def test_findDuplicates_doubleRange():

    for i in range(2, 4):
        assert findDuplicates(multiCopyRange(500, i)) == [i for i in range(500)]
