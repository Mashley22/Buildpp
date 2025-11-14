from pathlib import Path
import inspect
import importlib

from buildpp import Library, LibType
from ._library import _LIBRARY_CONSTRUCTOR_PROC_VAR


def new_Library(name : str,
                libType : LibType = LibType.STATIC) -> Library:

    assert isinstance(name, str) and isinstance(libType, LibType), "TypeError"

    return Library(_LIBRARY_CONSTRUCTOR_PROC_VAR,
                   name,
                   Path(inspect.stack()[1].filename).resolve().parent,
                   libType)


def import_buildList(relative_path: str):

    base = Path(inspect.stack()[1].filename).resolve().parent
    path = (base / relative_path).resolve()
    name = path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


__all__ = [name for name in dir() if not name.startswith('_')]
