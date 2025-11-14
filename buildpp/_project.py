from buildpp import CompileDefinitionsList, CompilerFlagsList

from Typing import Dict


'''!
@brief Each project compiles a completely different set of flags and definitions etc.
Project is a top level structure that passes its components down to everything,
Hence each project compiles seperately, but they still inherit from the globals
A structure for some repo therefore may look like:
- some libraries, to be inherited and used by either testing, samples or a user
- One or more Test projects, each with some executables which link the libraries,
  with certain flags enabled disabled etc.
- One or more samples projects, similiar to the tests

May add support for a project to override sources and includes etc..
Or for different language versions etc...

DONT USE THE CONSTRUCTOR DIRECTLY PLEASE
'''


__PROJECT_CONSTRUCTOR_PROC_VAR = 19345.09


class Project:
    __compileDefs : CompileDefinitionsList
    __compilerFlags : CompilerFlagsList

    def __init__(self,
                 name : str):
        
        if name is not __PROJECT_CONSTRUCTOR_PROC_VAR:
            print("Error, do not call the constructor of Project, use the add_project function instead please")

        self.__compileDefs = CompileDefinitionsList()
        self.__compilerFlags = CompilerFlagsList()

    @property
    def compileDefs(self) -> CompileDefinitionsList:

        return self.__compileDefs

    @property
    def compilerFlags(self) -> CompilerFlagsList:

        return self.__compilerFlags


__projects : Dict[str, Project] = {}


def add_Project(name : str) -> Project:  # Note: do not make a getter for the Projects

    assert name not in __projects.keys(), "Project already in project list"

    __projects[name] = Project(__PROJECT_CONSTRUCTOR_PROC_VAR)

    return __projects[name]


__all__ = [name for name in dir() if not name.startswith('_')]
