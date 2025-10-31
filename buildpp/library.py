import os
from typing import List, Union, Type, TypeVar
from enum import Enum


'''
Note that all these classes refer to the Libraries personal dependencies/includes, not the includes inherited from
its dependencies or the dependencies inherited from the dependencies
'''


class LibType(Enum):
    STATIC = 0
    SHARED = 0


'''!
@note the errors are raised only at the end
'''


class DuplicateDependency_err:
    duplicateDep : str

    def __init__(self,
                 duplicate : str):

        self.duplicateDep = duplicate


class DuplicateIncludeDir_err:
    _duplicateDir : str

    def __init__(self,
                 DuplicateDir : str):
        self.duplicateDir = DuplicateDir


class LibInterfacingForm:
    T = TypeVar('T')
    _private : T
    _public : T
    _interface : T

    def __init__(self, cls: Type[T]):
        self._private = cls()
        self._public = cls()
        self._interface = cls()

    @property
    def private(self) -> T:
        return self._private

    @property
    def public(self) -> T:
        return self._public

    @property
    def interface(self) -> T:
        return self._interface


class DependenciesList:
    _names : List[str]

    def __init__(self,
                 dependencies : List[Union[str, 'Library']] = []):

        if len(dependencies) == 0:
            self._names = []
        else:
            self.add(dependencies)

    @property
    def names(self) -> List[str]:
        return self._names

    def add(self,
            newDependencies : Union[List[Union[str, 'Library']], str, 'Library']) -> None:

        if isinstance(newDependencies, list):
            for ele in newDependencies:
                self._addOne(ele)
        else:
            self._addOne(newDependencies)

    def _addOne(self,
                newDependecy : Union[str, 'Library']) -> None:

        if isinstance(newDependecy, Library):
            name = newDependecy.name
        elif isinstance(newDependecy, str):
            name = newDependecy
        else:
            raise TypeError

        self._names.append(name)


class Dependencies(LibInterfacingForm):
    def __init__(self):
        super().__init__(DependenciesList)


class GenericStringList:
    _list : List[str]

    def __init__(self,
                 eles : Union[List[str], str] = []):

        self.add(eles)

    def _addOne(self,
                ele : str) -> None:

        if isinstance(ele, str):
            self._list.append(ele)
        else:
            raise TypeError

    def add(self,
            newEles : Union[List[str], str]) -> None:

        if isinstance(newEles, list):
            if all(isinstance(ele, str) for ele in newEles):
                self._list.extend(newEles)
            else:
                raise TypeError
        else:
            self._addOne(newEles)


class IncludeDirsList(GenericStringList):
    def __init__(self,
                 dirs : Union[List[str], str] = []):

        super().__init__(dirs)

    @property
    def dirs(self) -> List[str]:
        return super()._list


class IncludeDirs(LibInterfacingForm):
    def __init__(self):
        super().__init__(IncludeDirsList)


class CompilerFlagsList(GenericStringList):
    def __init__(self,
                 flags : Union[List[str], str] = []):

        super().__init__(flags)

    @property
    def flags(self) -> List[str]:
        return super()._list


class CompilerFlags(LibInterfacingForm):
    def __init__(self):
        super().__init__(CompilerFlagsList)


class CompileDefinitionsList(GenericStringList):
    def __init__(self,
                 defs : List[str]):
        super().__init__(defs)

    @property
    def defs(self) -> List[str]:
        return super()._list


class CompileDefinitions(LibInterfacingForm):
    def __init__(self):
        super().__init__(CompileDefinitionsList)


'''!
@warning Do not create Library objects directly please, use the @ref AddLibrary function
'''


class Library:

    _sources : GenericStringList
    _dependencies : Dependencies
    _includeDirs : IncludeDirs
    _compilerFlags : CompilerFlags
    _compileDefinitions : CompileDefinitions
    _libType : LibType
    _root : os.PathLike

    def __init__(self,
                 libType : LibType = LibType.STATIC):

        assert isinstance(libType, LibType)

        self._root = os.path.dirname(__file__)
        self._sources = GenericStringList()
        self._dependencies = Dependencies()
        self._includeDirs = IncludeDirs()
        self._compilerFlags = CompilerFlags()
        self._compileDefinitions = CompileDefinitions()
        self._libType = libType

    '''!
    @brief RELATIVE
    '''
    @property
    def sources(self) -> GenericStringList:
        return self._sources

    @property
    def dependencies(self) -> Dependencies:
        return self._dependencies

    @property
    def includeDirs(self) -> IncludeDirs:
        return self._includeDirs

    @property
    def compilerFlags(self) -> CompilerFlags:
        return self._compilerFlags

    @property
    def compilerDefs(self) -> CompileDefinitions:
        return self._compileDefinitions

    @property
    def libType(self) -> LibType:
        return self._libType
