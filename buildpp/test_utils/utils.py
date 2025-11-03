from typing import List

__all__ = []


def multiCopyRange(upper : int,
                   copyNum : int = 1) -> List[int]:

    retval = []
    myRange = [x for x in range(upper)]
    for i in range(copyNum):
        retval .extend(myRange)
    return retval
