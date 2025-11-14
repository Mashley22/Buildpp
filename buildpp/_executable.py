from buildpp import Library, LibType

from pathlib import Path
from typing import Dict
import inspect


__executableList : Dict[str, 'Executable'] = {}


class Executable(Library):
    def __init__(self,
                 name : str,
                 buildListDir : Path):

        super().__init__(name, buildListDir, LibType.EXECUTABLE)


def add_Executable(name : str) -> Executable:

    assert isinstance(name, str), "TypeError"

    if name in __executableList.keys():
        print("Warning, Executable name already in use")
    
    __executableList[name] = Executable(name,
                                        Path(inspect.stack()[1].filename).resolve().parent)

    return __executableList[name]


__all__ = [name for name in dir() if not name.startswith('_')]
