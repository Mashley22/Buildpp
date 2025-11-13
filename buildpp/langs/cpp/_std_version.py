from enum import IntEnum


class StdVersion(IntEnum):
    CPP98 = 98,
    CPP03 = 103,
    CPP11 = 111,
    CPP14 = 114,
    CPP17 = 117,
    CPP20 = 120,
    CPP23 = 123,
    CPP26 = 126


__stdVersion : StdVersion = StdVersion.CPP11  # Enforce one standard only throughout the system


__stdVersionFlagDict = {
    StdVersion.CPP98 : '--std=c++98',
    StdVersion.CPP03 : '--std=c++03',
    StdVersion.CPP11 : '--std=c++11',
    StdVersion.CPP14 : '--std=c++14',
    StdVersion.CPP17 : '--std=c++17',
    StdVersion.CPP20 : '--std=c++20',
    StdVersion.CPP23 : '--std=c++23',
    StdVersion.CPP26 : '--std=c++26'
}


def set_standard(version : StdVersion) -> None:

    assert isinstance(version, StdVersion), "TypeError"

    __stdVersion = version


def get_standard() -> StdVersion:

    return __stdVersion


def get_standardCompilerFlag() -> str:
    
    return __stdVersionFlagDict[__stdVersion]
