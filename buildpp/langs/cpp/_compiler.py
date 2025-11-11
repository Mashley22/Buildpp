from buildpp.langs.utils import _find_in_path

# In order of priority
_COMPILER_COMMAND_OPTIONS = (
    "c++",
    "clang++",
    "g++",
    "cl"
)

__COMPILER_COMMAND = "c++"
__COMPILER_PATH = None


def findCompiler() -> bool:

    for cmd in _COMPILER_COMMAND_OPTIONS:
        path = _find_in_path(cmd)
        if path is not None:
            __COMPILER_COMMAND = cmd
            __COMPILER_PATH = path
            return True

    return False


def compiler() -> str:
    assert __COMPILER_PATH is not None
    return __COMPILER_COMMAND


def compilerPath() -> str:
    assert __COMPILER_PATH is not None
    return __COMPILER_COMMAND


__all__ = [name for name in dir() if not name.startswith('_')]
