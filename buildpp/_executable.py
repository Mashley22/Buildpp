from buildpp import Library, LibType

from pathlib import Path
import inspect


__EXECUTABLE_CONSTRUCTOR_PROC_VAR = 90876546789796543


class Executable(Library):
    def __init__(self,
                 proc_var : str,
                 name : str,
                 buildListDir : Path):

        assert proc_var == __EXECUTABLE_CONSTRUCTOR_PROC_VAR, "Error, use add_Executable function, do not use Executable constructor directly"

        super().__init__(name, buildListDir, LibType.EXECUTABLE)


def add_Executable(name : str) -> Executable:

    return Executable(__EXECUTABLE_CONSTRUCTOR_PROC_VAR,
                      name,
                      Path(inspect.stack()[1].filename).resolve().parent)


__all__ = [name for name in dir() if not name.startswith('_')]
