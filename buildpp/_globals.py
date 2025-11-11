from buildpp import CompileDefinitionsList

_globalDefs = CompileDefinitionsList


def get_GlobalCompileDefs() -> CompileDefinitionsList:

    return _globalDefs


def add_GlobalCompileDef(symbol : str,
                         value : CompileDefinitionsList.definitionValues_t = None) -> None:

    _globalDefs.add(symbol, value)
