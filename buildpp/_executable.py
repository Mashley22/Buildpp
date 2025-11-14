from buildpp import Library, LibType

from pathlib import Path
import inspect


class Executable(Library):
    def __init__(self,
                 name : str,
                 buildListDir : Path):

        super().__init__(name, buildListDir, LibType.EXECUTABLE)


def add_Executable(name : str) -> Executable:

    return Executable(name,
                      Path(inspect.stack()[1].filename).resolve().parent)


__all__ = [name for name in dir() if not name.startswith('_')]
