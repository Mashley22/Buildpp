from buildpp.utils import findDuplicates
from .utils import multiCopyRange

import pytest

__all__ = []


@pytest.mark.dependency()
class Test_findDuplicates:

    def test_empty(self):

        assert findDuplicates([]) == []

    def test_simpleRanges(self):

        assert findDuplicates([x for x in range(0, 50)]) == []
        assert findDuplicates([x for x in range(-100, 100)]) == []
        assert findDuplicates([x for x in range(100, 50, -1)]) == []
        assert findDuplicates([x for x in range(0, 5000, 100)]) == []

    def test_bigRange(self):

        assert findDuplicates([x for x in range(0, 1000000)]) == []

    def test_doubleRange(self):

        for i in range(2, 4):
            assert findDuplicates(multiCopyRange(500, i)) == [i for i in range(500)]
