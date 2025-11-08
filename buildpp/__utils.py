from pathlib import Path
from typing import List, Iterable
from collections import Counter
import collections.abc as abc

__all__ = []

'''!
@brief recieves a bunch of relative filepaths and a single root path and checks
whether these all exist
@retval returns a list of the absolute paths that it cant find the files for
'''


def findNonExistFiles(root : Path,
                      relPaths : Iterable[str]) -> List[Path]:

    retval = list()

    for rel in relPaths:
        absolutePath = root / rel
        if not absolutePath.exists():
            retval.append(absolutePath)

    return retval


def findDuplicates(m_list : Iterable) -> list:

    assert isinstance(m_list, abc.Iterable), "TypeError"

    counter = Counter(m_list)
    return [item for item, count in counter.items() if count > 1]


'''!
@brief changes a list to remove duplicates while preserving order
'''


def deDuplicateList(m_list : list) -> list:

    m_list[:] = list(dict.fromkeys(m_list))

    return m_list


class GenericStringList:
    __list : List[str]

    def __init__(self,
                 eles : Iterable[str] | str = None):

        self.__list = []

        if eles is not None:
            self.add(eles)

    def _addOne(self,
                ele : str) -> None:

        self.__list.append(ele)

    def add(self,
            newEles : Iterable[str] | str) -> None:

        if isinstance(newEles, str):
            self._addOne(newEles)

        elif isinstance(newEles, abc.Iterable) and all(isinstance(ele, str) for ele in newEles):
            self.__list.extend(newEles)

        else:
            assert False, "TypeError"

    def merge(self,
              other : "GenericStringList") -> None:

        assert isinstance(other, GenericStringList), "TypeError"

        self.__list.extend(other.__list)

    def deDuplicate(self) -> None:

        deDuplicateList(self.__list)

    @property 
    def list(self) -> List[str]:

        return self.__list

    def __eq__(self,
               other : "GenericStringList") -> bool:

        assert isinstance(other, GenericStringList), "TypeError"

        return sorted(self.__list) == sorted(other.__list)
