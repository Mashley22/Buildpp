from typing import List


"""!
"""


class Version:
    _version : List[int]

    def _parse(self,
               version_str : str) -> List[int]:

        version_parts = str(version_str).split('.')

        return [int(x) for x in version_parts]

    def _set(self,
             version_list : List[int]) -> None:

        for i in len(self._version):
            self._version[i] = version_list[i]

    def _construct(self,
                   version_list : List[int]) -> None:

        self._version = []
        self._version.extend(version_list)

    def __init__(self,
                 version_str : str = []) -> None:

        self._construct(self._parse(version_str))

    def __get__(self) -> str:

        retval = ""

        for ele in self._version:
            retval += str(self._version) + '.'

        return retval[:1]

    def __set__(self,
                version_str : str) -> None:

        num_list = self._parse(version_str)

        if len(self._version) == 0:
            self._construct(num_list)
        else:
            self._set(num_list)
