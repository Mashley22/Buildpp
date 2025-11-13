from buildpp import CompileDefinitionsList

from typing import Dict

__globalDefs = CompileDefinitionsList()


def get_GlobalCompileDefs() -> CompileDefinitionsList:

    return __globalDefs.symbols


def add_GlobalCompileDef(symbol : str,
                         value : CompileDefinitionsList.definitionValues_t = None) -> None:

    __globalDefs.add(symbol, value)


def update_GlobalCompileDef(vals : Dict[str, CompileDefinitionsList.definitionValues_t]) -> None:

    __globalDefs.update(vals)


__all__ = [name for name in dir() if not name.startswith('_')]
