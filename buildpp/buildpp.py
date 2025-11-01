from .library import Library, LibType
from pathlib import Path
import inspect
import importlib

__libraries = dict()


class DuplicateLibraryErr:
    libName : str

    def __init__(self,
                 name : str):

        self.libName = name
        print(f"Error: Duplicate library added {name}")


def check_invalid_dependencies(lib : Library):

    return [ele for ele in lib.dependencies.all() if ele not in __libraries.keys()]


def add_library(name : str,
                libType : LibType = LibType.STATIC) -> Library:

    if not isinstance(name, str):
        raise TypeError

    if name in __libraries:
        raise DuplicateLibraryErr(name)

    __libraries[name] = Library(name,
                                Path(inspect.stack()[1].filename).resolve().parent,
                                libType)

    return __libraries[name]


def import_buildList(relative_path: str):

    base = Path(__file__).parent
    path = (base / relative_path).resolve()
    name = path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
