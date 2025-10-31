from .library import Library, LibType

__libraries = dict()


class DuplicateLibraryErr:
    libName : str

    def __init__(self,
                 name : str):

        self.libName = name
        print(f"Duplicate library added {name}")


def add_library(name : str,
                libType : LibType = LibType.STATIC) -> Library:

    if not isinstance(name, str):
        raise TypeError

    if name in __libraries:
        raise DuplicateLibraryErr(name)

    __libraries[name] = Library(libType)

    return __libraries[name]


