import shutil
from pathlib import Path


def _find_in_path(program_name: str) -> Path | None:

    val = shutil.which(program_name)

    if val is not None:
        return Path(val)

    else: 
        return None


__all__ = [name for name in dir() if not name.startswith('_')]
