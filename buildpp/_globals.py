from buildpp import CompileDefinitionsList

from Typing import Dict

__globalDefs = CompileDefinitionsList


def get_GlobalCompileDefs() -> CompileDefinitionsList:

    return __globalDefs.symbols


def add_GlobalCompileDef(symbol : str,
                         value : CompileDefinitionsList.definitionValues_t = None) -> None:

    __globalDefs.add(symbol, value)


def update_GlobalCompileDef(vals : Dict[str, CompileDefinitionsList.definitionValues_t]) -> None:

    __globalDefs.update(vals)
