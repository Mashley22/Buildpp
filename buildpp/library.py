from typing import List, Type, TypeVar, Iterable
from enum import Enum
from pathlib import Path
import collections.abc as abc
import inspect

from buildpp.utils import findDuplicates, findNonExistFiles, deDuplicateList, GenericStringList
from buildpp.versions import Version


'''
Note that all these classes refer to the Libraries personal dependencies/includes, not the includes inherited from
its dependencies or the dependencies inherited from the dependencies
'''


class LibType(Enum):
    STATIC = 0
    SHARED = 0


"""!
@brief A generalised template class over public, pivate and interface accesses
@note to use a class with this it must have a property and setter over the _list attribute and a deDuplicate function
"""


class LibInterfacingForm:
    T = TypeVar('T')
    __private : T
    __public : T
    __interface : T
    __underlying_t : type

    '''!
    @tparam cls the underling type for each access member
    '''

    def __init__(self,
                 cls : Type[T]):

        self.__private = cls()
        self.__public = cls()
        self.__interface = cls()

        self.__underlying_t = cls

    def _setterTypeCheck(self,
                         accessLvl : str,
                         setVal) -> None:

        assert self.__underlying_t == type(setVal), f"{type} setter type mismatch! Needs to be {self.__underlying_t}, got {type(setVal)}"

    def _inheritTypeCheck(self,
                          other : "LibInterfacingForm") -> None:

        assert self.__underlying_t == other.__underlying_t, f"Inherit type mismatch, expected {self.__underlying_t}, got {other.__underlying_t}"

    @property
    def private(self) -> T:
        return self.__private

    @private.setter
    def private(self,
                priv : T) -> None:

        self._setterTypeCheck("private", priv)

        self.__private = priv

    @property
    def public(self) -> T:
        return self.__public

    @public.setter
    def public(self,
               val : T) -> None:

        self._setterTypeCheck("public", val)

        self.__public = val

    @property
    def interface(self) -> T:
        return self.__interface

    @interface.setter
    def interface(self,
                  interface : T) -> None:

        self._setterTypeCheck("interface", interface)

        self.__interface = interface

    def all(self):

        retval = []
        retval.extend(self.__public._list)
        retval.extend(self.__private._list)
        retval.extend(self.__interface._list)

        return retval

    def inheritPublic(self,
                      other : 'LibInterfacingForm') -> None:

        self._inheritTypeCheck(other)

        self.__public._list.extend(other.__public._list)
        self.__public._list.extend(other.__interface._list)

        self.__public.deDuplicate()

    def inheritPrivate(self,
                       other : 'LibInterfacingForm') -> None:

        self._inheritTypeCheck(other)

        self.__private._list.extend(other.__public._list)
        self.__private._list.extend(other.__interface._list)

        self.__private.deDuplicate()

    def inheritInterface(self,
                         other : 'LibInterfacingForm') -> None:

        self._inheritTypeCheck(other)

        self.__interface._list.extend(other.__public._list)
        self.__interface._list.extend(other.__interface._list)

        self.__interface.deDuplicate()


'''!
@brief a class to contain a list of dependencies
'''


class DependenciesList:
    __list : List['Library']

    def __init__(self,
                 dependencies : Iterable['Library'] = None):

        if dependencies is not None:
            self.add(dependencies)
        else:
            self.__list = []

    @property
    def libs(self) -> List['Library']:
        return self.__list

    def add(self,
            newDependencies : Iterable['Library'] | 'Library') -> None:

        if isinstance(newDependencies, Library):
            self.__list.append(newDependencies)

        elif isinstance(newDependencies, abc.Iterable) and all(isinstance(x, Library) for x in newDependencies):
            self.__list.extend(newDependencies)

        else:
            assert False, "TypeError"

    def deDuplicate(self) -> None:

        deDuplicateList(self.__list)

    '''!
    @friend LibInterfaceForm
    '''
    @property
    def _list(self) -> List['Library']:

        return self.__list

    '''!
    @friend LibInterfaceForm
    '''
    @_list.setter
    def _list(self,
              val : List['Library']) -> None:

        self.__list = val


class Dependencies(LibInterfacingForm):
    def __init__(self):
        super().__init__(DependenciesList)


class PathList:
    __list : List[Path]
    __root : Path

    def __init__(self,
                 root : Path = None):

        self.__root = root
        self.__list = []

    def __addOneRel(self,
                    rel : str) -> None:

        self.__list.append(self.__root / rel)

    def addRel(self,
               relPaths : Iterable[str] | str) -> None:

        assert self.__root is not None, "Assign a root before using relative additions"

        if isinstance(relPaths, str):
            self.__addOneRel(relPaths)

        elif isinstance(relPaths, abc.Iterable) and all(isinstance(x, str) for x in relPaths):
            for path in relPaths:
                self.__addOneRel(path)

        else:
            assert False, "TypeError"

    def addAbs(self,
               absPaths : Iterable[Path] | Path) -> None:

        if isinstance(absPaths, Path):
            self.__list.append(absPaths)

        elif isinstance(absPaths, abc.Iterable) and all(isinstance(x, Path) for x in absPaths):
            self.__list.extend(absPaths)

        else:
            assert False, "TypeError"

    def deDuplicate(self) -> None:

        deDuplicateList(self.__list)

    @property
    def paths(self) -> List[Path]:

        return self.__list

    '''!
    @friend LibInterfaceForm
    '''
    @property
    def _list(self) -> List[Path]:

        return self.__list

    '''!
    @friend LibInterfaceForm
    '''
    @_list.setter
    def _list(self,
              val : Iterable[Path]) -> None:

        assert isinstance(val, abc.Iterable) and all(isinstance(x, Path) for x in val), "TypeError"
        self.__list = val

    @property
    def root(self) -> Path:

        return self.__root

    @root.setter
    def root(self,
             root : Path) -> None:

        assert isinstance(root, Path), "Root must be of type pathlib.Path"

        self.__root = root


class IncludeDirsList(PathList):
    def __init__(self,
                 pathList : PathList = None):

        super().__init__()

        if pathList is not None:

            if pathList.root is not None:
                self.root = Path(pathList.root)

            if pathList._list is not None:
                self._list = list(pathList._list)

    @property
    def dirs(self) -> List[Path]:
        return self._list


def new_AbsIncludeDirsList(absDirsList : Path | List[Path]) -> IncludeDirsList:

    pathList = PathList()
    pathList.addAbs(absDirsList)

    return IncludeDirsList(pathList)


def new_RelIncludeDirsList(relDirsList : str | List[str],
                           root : Path = None) -> IncludeDirsList:

    if root is None:
        root = Path(inspect.stack()[1].filename).resolve().parent

    pathList = PathList(root)
    pathList.addRel(relDirsList)

    return IncludeDirsList(pathList)


class IncludeDirs(LibInterfacingForm):
    def __init__(self):

        super().__init__(IncludeDirsList)


class SourcesList(GenericStringList):
    def __init__(self,
                 sources : List[str] | str = None):

        super().__init__(sources)

    @property
    def sources(self) -> List[str]:
        return super()._list


class CompilerFlagsList(GenericStringList):
    def __init__(self,
                 flags : List[str] | str = None):

        super().__init__(flags)

    @property
    def flags(self) -> List[str]:
        return super()._list


class CompilerFlags(LibInterfacingForm):
    def __init__(self):
        super().__init__(CompilerFlagsList)


class CompileDefinitionsList(GenericStringList):
    def __init__(self,
                 defs : List[str] = None):
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

    __sources : SourcesList
    __dependencies : Dependencies
    __includeDirs : IncludeDirs
    __compilerFlags : CompilerFlags
    __compileDefinitions : CompileDefinitions
    __libType : LibType
    __root : Path
    __name : str
    __dependenciesHandled : bool
    __version : Version

    def __init__(self,
                 name : str,
                 buildListDir : Path,
                 libType : LibType = LibType.STATIC):

        assert isinstance(libType, LibType)

        self.__root = buildListDir
        self.__sources = SourcesList()
        self.__dependencies = Dependencies()
        self.__includeDirs = IncludeDirs()
        self.__compilerFlags = CompilerFlags()
        self.__compileDefinitions = CompileDefinitions()
        self.__libType = libType
        self.__name = name
        self.__dependenciesHandled = False
        self.__version = Version()

    '''!
    @brief RELATIVE
    '''
    @property
    def sources(self) -> SourcesList:
        return self.__sources

    @sources.setter
    def sources(self,
                sources : SourcesList) -> None:

        if not isinstance(sources, SourcesList):
            raise TypeError

        self.__sources = sources

    @property
    def dependencies(self) -> Dependencies:
        return self.__dependencies

    @property
    def includeDirs(self) -> IncludeDirs:
        return self.__includeDirs

    @property
    def compilerFlags(self) -> CompilerFlags:
        return self.__compilerFlags

    @compilerFlags.setter
    def compilerFlags(self,
                      flags : CompilerFlags):

        if not isinstance(flags, CompilerFlags):
            raise TypeError

        self.__compilerFlags = flags

    @property
    def compilerDefs(self) -> CompileDefinitions:
        return self.__compileDefinitions

    @compilerDefs.setter
    def compilerDefs(self,
                     defs : CompileDefinitions):

        if not isinstance(defs, CompileDefinitions):
            raise TypeError

        self.__compilerDefinitions = defs

    @property
    def libType(self) -> LibType:
        return self.__libType

    @property
    def version(self) -> Version:
        return self.__version

    @version.setter
    def version(self,
                val : Version) -> None:

        if not isinstance(val, Version):
            raise TypeError

        self.__version = val

    def setLibType(self,
                   libType : LibType) -> None:

        if not isinstance(libType):
            raise TypeError

        self.__libType = libType

    def checkSourcesDups(self) -> List[str]:

        sourceDups = findDuplicates(self.__sources)
        if len(sourceDups) > 0:
            print(f"Warning: duplicate sources, lib: {self.__name}, dupicates: {sourceDups}")

        # findDuplicates should return empty list
        return sourceDups

    def checkSourceFilesExist(self) -> List[Path]:

        noExistSources = findNonExistFiles(self.__root,
                                           self.__sources)

        if len(noExistSources) > 0:
            print(f"Warning: source files not found, lib: {self.__name}, files: {noExistSources}")

        # findNonExistFiles should return []
        return noExistSources

    def checkIncludeDupes(self) -> List[str]:

        incDupes = findDuplicates(self.__includeDirs.all())

        if len(incDupes) > 0:
            print(f"Warning: duplicated include directories lib: {self.__name}, include dirs: {incDupes}")

        return incDupes

    def checkCompilerFlagDupes(self) -> List[str]:

        compFlagDupes = findDuplicates(self.__compilerFlags.all())

        if len(compFlagDupes) > 0:
            print(f"Warning: duplicated compiler flags lib: {self.__name}, flags: {compFlagDupes}")

        return compFlagDupes

    def checkCompileDefinitionDupes(self) -> List[str]:

        compDefDupes = findDuplicates(self.__compileDefinitions.all())

        if len(compDefDupes) > 0:
            print(f"Warning: duplicated compiler definitions lib: {self.__name}, flags: {compDefDupes}")

        return compDefDupes

    def checkDependencyDupes(self) -> List[str]:

        dupes = findDuplicates(self.__dependencies.all())

        if len(dupes) > 0:
            print(f"Warning: duplicated dependencies lib: {self.__name}, dependencies: {dupes}")

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

        return self.__dependenciesHandled

    def _getSubDependencies(self) -> List['Library']:

        subDeps = []

        for dep in self.dependencies:
            subDeps.extend(dep._getSubDependencies())

        deDuplicateList(subDeps)

    def _handlePublicDependencies(self) -> None:

        for dep in self.__dependencies.public:

            if dep.dependenciesHandled is not True:
                dep.handleDependencies()

            self.__includeDirs.inheritPublic(dep.includeDirs)
            self.__compileDefinitions.inheritPublic(dep.compileDefs)
            self.__compilerFlags.inheritPublic(dep.compilerFlags)

    def _handlePrivateDependencies(self) -> None:

        for dep in self.__dependencies.private:

            if dep.dependenciesHandled is not True:
                dep.handleDependencies()

            self.__includeDirs.inheritPrivate(dep.includeDirs)
            self.__compileDefinitions.inheritPrivate(dep.compileDefs)
            self.__compilerFlags.inheritPrivate(dep.compilerFlags)

    def _handleInterfaceDependencies(self) -> None:

        for dep in self.__dependencies.private:

            if dep.dependenciesHandled is not True:
                dep.handleDependencies()

            self.__includeDirs.inheritInterface(dep.includeDirs)
            self.__compileDefinitions.inheritInterface(dep.compileDefs)
            self.__compilerFlags.inheritInterface(dep.compilerFlags)

    def handleDependencies(self) -> None:

        self._handleInterfaceDependencies()
        self._handlePublicDependencies()
        self._handlePrivateDependencies()

        self.__dependenciesHandled = True


__all__ = [name for name in dir() if not name.startswith('_')]
