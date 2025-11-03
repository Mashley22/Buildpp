from .library import Library, LibType
from pathlib import Path
import inspect
import importlib


def new_library(name : str,
                libType : LibType = LibType.STATIC) -> Library:

    if not isinstance(name, str):
        raise TypeError

    return Library(name,
                   Path(inspect.stack()[1].filename).resolve().parent,
                   libType)


def import_buildList(relative_path: str):

    base = Path(__file__).parent
    path = (base / relative_path).resolve()
    name = path.stem
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
