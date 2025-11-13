from buildpp import CompileDefinitionsList, CompilerFlagsList

from Typing import Dict, Iterable

__global_symbols = CompileDefinitionsList()

__global_flags = CompilerFlagsList()


def get_compileDefs() -> Dict[str, CompileDefinitionsList.definitionValues_t]:

    return __global_symbols.symbols


def add_compileDef(key : str,
                   val : CompileDefinitionsList.definitionValues_t) -> None:

    __global_symbols.add(key, val)


def update_compileDef(vals : Dict[str, CompileDefinitionsList.definitionValues_t]) -> None:

    __global_symbols.update(vals)


def get_compilerFlags() -> Iterable[str]:

    return __global_flags.list


def add_compilerFlags(flag : str | Iterable[str]) -> None:

    __global_flags.add(flag)
