from buildpp.utils import deDuplicateList

from .utils import multiCopyRange

import numpy as np


def _simpleRange(lower : int,
                 upper : int,
                 interval : int):

    testRange = [i for i in range(lower, upper, interval)]

    newList = deDuplicateList(testRange)

    assert newList == testRange


def test_deDuplicateList_empty():

    testList = []
    deDuplicateList(testList)
    assert testList == []


def test_deDuplicateList_ref_ret():

    refList = [1, 1, 2]
    expList = [1, 2]

    retList = deDuplicateList(refList)

    assert expList == retList, "uuuhh.... v. bad"
    assert expList == refList, "The reference parameter behaviour is not working"


def test_deDuplicateList_simpleRange():

    _simpleRange(0, 500, 1)
    _simpleRange(5, -100, -1)
    _simpleRange(4, 981, 40)


def test_deDuplicateList_bigRange():

    _simpleRange(0, 1000000, 1)


def test_deDuplicateList_str():

    refList = ["a", "a", "b"]
    expList = ["a", "b"]

    retList = deDuplicateList(refList)

    assert expList == retList, "uuuhh.... v. bad"
    assert expList == refList, "The reference parameter behaviour is not working"


def test_deDuplicateList_random():  # only tests the number of elements doesnt check the order, tho this is not importatn

    for _ in range(10):
        testList = np.random.randint(0, 1000, 10000).tolist()
        res = deDuplicateList(testList.copy())

        assert len(res) == len(set(testList))
