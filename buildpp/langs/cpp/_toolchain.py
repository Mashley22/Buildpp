from ._compiler import findCompiler

__enabled : bool = False


def enable() -> None:

    if __enabled:
        return
    
    if not findCompiler():
        print("Warning, couldn't find any cpp compiler")
