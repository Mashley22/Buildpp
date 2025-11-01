from pathlib import Path
from typing import List
import Counter


'''!
@brief recieves a bunch of relative filepaths and a single root path and checks
whether these all exist
@retval returns a list of the absolute paths that it cant find the files for
'''


def findNonExistFiles(root : Path,
                      relPaths : List[str]) -> List[Path]:

    retval = []

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


ValidCompileFlags = []  # TODO
