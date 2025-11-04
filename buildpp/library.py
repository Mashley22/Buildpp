from typing import List, Union, Type, TypeVar
from enum import Enum
from pathlib import Path

from buildpp.utils import findDuplicates, findNonExistFiles, deDuplicateList, GenericStringList
from buildpp.versions import Version


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
    _underlying_t : type

    def __init__(self,
                 cls : Type[T]):

        self._private = cls()
        self._public = cls()
        self._interface = cls()

        self._underlying_t = cls

    @property
    def private(self) -> T:
        return self._private

    @private.setter
    def private(self,
                priv : T) -> None:

        assert isinstance(priv, self._underlying_t)

        self._private = priv

    @property
    def public(self) -> T:
        return self._public

    @public.setter
    def public(self,
               val : T) -> None:

        assert isinstance(val, self._underlying_t)

        self._public = val

    @property
    def interface(self) -> T:
        return self._interface

    @interface.setter
    def interface(self,
                  interface : T) -> None:

        assert isinstance(interface, self._underlying_t)

        self._interface = interface

    def all(self):
        retval = []
        retval.extend(self._public)
        retval.extend(self._private)
        retval.extend(self._interface)

    def inheritPublic(self,
                      other : 'LibInterfacingForm') -> None:

        assert other._underlying_t == self._underlying_t

        self._public._list.extend(other._public._list)
        self._public._list.extend(other._interface._list)

        self._public.deDuplicate()

    def inheritPrivate(self,
                       other : 'LibInterfacingForm') -> None:

        assert other._underlying_t == self._underlying_t

        self._private._list.extend(other._public._list)
        self._private._list.extend(other._interface._list)

        self._private.deDuplicate()

    def inheritInterface(self,
                         other : 'LibInterfacingForm') -> None:

        assert other._underlying_t == self._underlying_t

        self._interface._list.extend(other._public._list)
        self._interface._list.extend(other._interface._list)

        self._interface.deDuplicate


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


class SourcesList(GenericStringList):
    def __init__(self,
                 sources : Union[List[str], str] = []):

        super().__init__(sources)

    @property
    def sources(self) -> List[str]:
        return super()._list


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

    _sources : SourcesList
    _dependencies : Dependencies
    _includeDirs : IncludeDirs
    _compilerFlags : CompilerFlags
    _compileDefinitions : CompileDefinitions
    _libType : LibType
    _root : Path
    _subDeps : DependenciesList
    _name : str
    _dependenciesHandled : bool
    _version : Version

    def __init__(self,
                 name : str,
                 buildListDir : Path,
                 libType : LibType = LibType.STATIC):

        assert isinstance(libType, LibType)

        self._root = buildListDir
        self._sources = SourcesList()
        self._dependencies = Dependencies()
        self._includeDirs = IncludeDirs()
        self._compilerFlags = CompilerFlags()
        self._compileDefinitions = CompileDefinitions()
        self._libType = libType
        self._name = name
        self._dependenciesHandled = False
        self._version = Version()

    '''!
    @brief RELATIVE
    '''
    @property
    def sources(self) -> SourcesList:
        return self._sources

    @sources.setter
    def sources(self,
                sources : SourcesList) -> None:

        if not isinstance(sources, SourcesList):
            raise TypeError

        self._sources = sources

    @property
    def dependencies(self) -> Dependencies:
        return self._dependencies

    @property
    def includeDirs(self) -> IncludeDirs:
        return self._includeDirs

    @property
    def compilerFlags(self) -> CompilerFlags:
        return self._compilerFlags

    @compilerFlags.setter
    def compilerFlags(self,
                      flags : CompilerFlags):

        if not isinstance(flags, CompilerFlags):
            raise TypeError

        self._compilerFlags = flags

    @property
    def compilerDefs(self) -> CompileDefinitions:
        return self._compileDefinitions

    @compilerDefs.setter
    def compilerDefs(self,
                     defs : CompileDefinitions):

        if not isinstance(defs, CompileDefinitions):
            raise TypeError

        self._compilerDefs = defs

    @property
    def libType(self) -> LibType:
        return self._libType

    @property
    def version(self) -> Version:
        return self._version

    @version.setter
    def version(self,
                val : Version) -> None:

        if not isinstance(val, Version):
            raise TypeError

        self._version = val

    def setLibType(self,
                   libType : LibType) -> None:

        if not isinstance(libType):
            raise TypeError

        self._libType = libType

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

        self._dependenciesHandled = True


__all__ = [name for name in dir() if not name.startswith('_')]
