from typing import List, Union, Type, TypeVar
from enum import Enum
from pathlib import Path

from .utils import findDuplicates, findNonExistFiles, deDuplicateList


'''
Note that all these classes refer to the Libraries personal dependencies/includes, not the includes inherited from
its dependencies or the dependencies inherited from the dependencies
'''


class LibType(Enum):
    STATIC = 0
    SHARED = 0


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

    def all(self):
        retval = []
        retval.extend(self._public)
        retval.extend(self._private)
        retval.extend(self._interface)

    def inheritPublic(self,
                      other : 'LibInterfacingForm') -> None:

        self._public._list.extend(other._public._list)
        self._public._list.extend(other._interface._list)

    def inheritPrivate(self,
                       other : 'LibInterfacingForm') -> None:

        self._private._list.extend(other._public._list)
        self._private._list.extend(other._interface._list)

    def inheritInterface(self,
                         other : 'LibInterfacingForm') -> None:

        self._interface._list.extend(other._public._list)
        self._interface._list.extend(other._interface._list)


class DependenciesList:
    _list : List['Library']

    def __init__(self,
                 dependencies : List['Library'] = []):

        self.add(dependencies)

    @property
    def libs(self) -> List[str]:
        return self._list

    def add(self,
            newDependencies : Union[List['Library'], 'Library']) -> None:

        if isinstance(newDependencies, list):
            for ele in newDependencies:
                self._addOne(ele)
        else:
            self._addOne(newDependencies)

    def _addOne(self,
                newDependecy : 'Library') -> None:

        if isinstance(newDependecy, Library):
            self._list.append(newDependecy)
        else:
            raise TypeError

    def deDuplicate(self) -> None:

        deDuplicateList(self._list)


class Dependencies(LibInterfacingForm):
    def __init__(self):
        super().__init__(DependenciesList)


class PathList:
    _list : List[Path]
    _root : Path

    def __init__(self,
                 paths : Union[List[Path], Path] = []):

        self._list = paths

    def _addOneRel(self,
                   rel : str) -> None:

        self._list.append(self._root / rel)

    def _addOneAbs(self,
                   abs : Path) -> None:

        self._list.append(abs)

    def addRel(self,
               relDirs : Union[List[str], str]) -> None:

        if isinstance(relDirs, list):
            for dir in relDirs:
                self._addOneRel(dir)

        elif isinstance(relDirs, str):
            self._addOneRel(relDirs)

        else:
            raise TypeError

    def addAbs(self,
               relDirs : Union[List[str], str]) -> None:

        if isinstance(relDirs, list):
            for dir in relDirs:
                self._addOneAbs(dir)

        elif isinstance(relDirs, str):
            self._addOneAbs(relDirs)

        else:
            raise TypeError

    def deDuplicate(self) -> None:

        deDuplicateList(self._list)


class IncludeDirsList(PathList):
    def __init__(self,
                 dirs : Union[List[str], str] = []):

        super().__init__(dirs)

    @property
    def dirs(self) -> List[str]:
        return super()._list


class IncludeDirs(LibInterfacingForm):
    def __init__(self):
        super().__init__(IncludeDirsList)


class GenericStringList:
    _list : List[str]

    def __init__(self,
                 eles : Union[List[str], str] = []):
        self._list = []
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

    def deDuplicate(self) -> None:

        deDuplicateList(self._list)


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
                 defs : List[str] = []):
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
    _root : Path
    _subDeps : DependenciesList
    _name : str
    _dependenciesHandled : bool

    def __init__(self,
                 name : str,
                 buildListDir : Path,
                 libType : LibType = LibType.STATIC):

        assert isinstance(libType, LibType)

        self._root = buildListDir
        self._sources = GenericStringList()
        self._dependencies = Dependencies()
        self._includeDirs = IncludeDirs()
        self._compilerFlags = CompilerFlags()
        self._compileDefinitions = CompileDefinitions()
        self._libType = libType
        self._name = name
        self._dependenciesHandled = False

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

    def checkSourcesDups(self) -> List[str]:

        sourceDups = findDuplicates(self._sources)
        if len(sourceDups) > 0:
            print(f"Warning: duplicate sources, lib: {self._name}, dupicates: {sourceDups}")

        # findDuplicates should return empty list
        return sourceDups

    def checkSourceFilesExist(self) -> List[Path]:

        noExistSources = findNonExistFiles(self._root,
                                           self._sources)

        if len(noExistSources) > 0:
            print(f"Warning: source files not found, lib: {self._name}, files: {noExistSources}")

        # findNonExistFiles should return []
        return noExistSources

    def checkIncludeDupes(self) -> List[str]:

        incDupes = findDuplicates(self._includeDirs.all())

        if len(incDupes) > 0:
            print(f"Warning: duplicated include directories lib: {self._name}, include dirs: {incDupes}")

        return incDupes

    def checkCompilerFlagDupes(self) -> List[str]:

        compFlagDupes = findDuplicates(self._compilerFlags.all())

        if len(compFlagDupes) > 0:
            print(f"Warning: duplicated compiler flags lib: {self._name}, flags: {compFlagDupes}")

        return compFlagDupes

    def checkCompileDefinitionDupes(self) -> List[str]:

        compDefDupes = findDuplicates(self._compileDefinitions.all())

        if len(compDefDupes) > 0:
            print(f"Warning: duplicated compiler definitions lib: {self._name}, flags: {compDefDupes}")

        return compDefDupes

    def checkDependencyDupes(self) -> List[str]:

        dupes = findDuplicates(self._dependencies.all())

        if len(dupes) > 0:
            print(f"Warning: duplicated dependencies lib: {self._name}, dependencies: {dupes}")

        return dupes

    def allChecks(self) -> List[str]:

        retval = {
            "src_dupes" : self.checkSourcesDups(),
            "src_noexist" : self.checkSourceFilesExist(),
            "inc_dupes" : self.checkIncludeDupes(),
            "flag_dupes" : self.checkCompilerFlagDupes(),
            "opt_dupes" : self.checkCompileDefinitionDupes(),
            "dep_dupes" : self.checkDependencyDupes()
        }

        return retval

    def header_only(self) -> bool:  # perhaps no_link in future?

        if len(self._sources) == 0:
            return True
        else:
            return False

    @property
    def dependenciesHandled(self) -> bool:

        return self._dependenciesHandled

    def _getSubDependencies(self) -> List['Library']:

        subDeps = []

        for dep in self.dependencies:
            subDeps.extend(dep._getSubDependencies())

        deDuplicateList(subDeps)

    def _handlePublicDependencies(self) -> None:

        for dep in self._dependencies.public:

            if dep.dependenciesHandled is not True:
                dep.handleDependencies()

            self._includeDirs.inheritPublic(dep.includeDirs)
            self._compileDefinitions.inheritPublic(dep.compileDefs)
            self._compilerFlags.inheritPublic(dep.compilerFlags)

    def _handlePrivateDependencies(self) -> None:

        for dep in self._dependencies.private:

            if dep.dependenciesHandled is not True:
                dep.handleDependencies()

            self._includeDirs.inheritPrivate(dep.includeDirs)
            self._compileDefinitions.inheritPrivate(dep.compileDefs)
            self._compilerFlags.inheritPrivate(dep.compilerFlags)

    def _handleInterfaceDependencies(self) -> None:

        for dep in self._dependencies.private:

            if dep.dependenciesHandled is not True:
                dep.handleDependencies()

            self._includeDirs.inheritInterface(dep.includeDirs)
            self._compileDefinitions.inheritInterface(dep.compileDefs)
            self._compilerFlags.inheritInterface(dep.compilerFlags)

    def handleDependencies(self) -> None:

        self._handleInterfaceDependencies()
        self._handlePublicDependencies()
        self._handlePrivateDependencies()
