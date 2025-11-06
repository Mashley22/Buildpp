from buildpp.utils import deDuplicateList

import pytest

import numpy as np


def _simpleRange(lower : int,
                 upper : int,
                 interval : int):

    testRange = [i for i in range(lower, upper, interval)]

    newList = deDuplicateList(testRange)

    assert newList == testRange


@pytest.mark.dependency()
class Test_deDuplicateList():

    def test_empty(self):

        testList = []
        deDuplicateList(testList)
        assert testList == []

    def test_ref_ret(self):

        refList = [1, 1, 2]
        expList = [1, 2]

        retList = deDuplicateList(refList)

        assert expList == retList, "uuuhh.... v. bad"
        assert expList == refList, "The reference parameter behaviour is not working"

    def test_simpleRange(self):

        _simpleRange(0, 500, 1)
        _simpleRange(5, -100, -1)
        _simpleRange(4, 981, 40)

    def test_bigRange(self):

        _simpleRange(0, 1000000, 1)

    def test_str(self):

        refList = ["a", "a", "b"]
        expList = ["a", "b"]

        retList = deDuplicateList(refList)

        assert expList == retList, "uuuhh.... v. bad"
        assert expList == refList, "The reference parameter behaviour is not working"

    def test_random(self):  # only tests the number of elements doesnt check the order, tho this is not importatn

        for _ in range(10):
            testList = np.random.randint(0, 1000, 10000).tolist()
            res = deDuplicateList(testList.copy())

            assert len(res) == len(set(testList))
