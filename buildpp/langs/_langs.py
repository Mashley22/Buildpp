from enum import Enum, auto


class Langs(Enum):
    CPP = auto()


__all__ = [name for name in dir() if not name.startswith('_')]
