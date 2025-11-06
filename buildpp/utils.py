from pathlib import Path
from typing import List
from collections import Counter

__all__ = []

'''!
@brief recieves a bunch of relative filepaths and a single root path and checks
whether these all exist
@retval returns a list of the absolute paths that it cant find the files for
'''


def findNonExistFiles(root : Path,
                      relPaths : List[str]) -> List[Path]:

    retval = list()

    for rel in relPaths:
        absolutePath = root / rel
        if not absolutePath.exists():
            retval.append(absolutePath)

    return retval


def findDuplicates(m_list : list) -> list:

    if not isinstance(m_list, list):
        raise TypeError

    counter = Counter(m_list)
    return [item for item, count in counter.items() if count > 1]


'''!
@brief changes a list to remove duplicates while preserving order
'''


def deDuplicateList(m_list : list) -> list:

    m_list[:] = list(dict.fromkeys(m_list))

    return m_list


class GenericStringList:
    _list : List[str]

    def __init__(self,
                 eles : List[str] | str = None):

        self._list = [] if eles is None else eles
        self.add(eles)

    def _addOne(self,
                ele : str) -> None:

        if isinstance(ele, str):
            self._list.append(ele)
        else:
            raise TypeError

    def add(self,
            newEles : List[str] | str) -> None:

        if isinstance(newEles, list):
            if all(isinstance(ele, str) for ele in newEles):
                self._list.extend(newEles)
            else:
                raise TypeError
        else:
            self._addOne(newEles)

    def deDuplicate(self) -> None:

        deDuplicateList(self._list)
