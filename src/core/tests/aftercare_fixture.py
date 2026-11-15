"""Ensure bare unittest discovery in a git worktree loads sibling src/core/src."""

import sys
from pathlib import Path

CORE_SRC: Path = Path(__file__).resolve().parents[1] / "src"


def ensure_worktree_src() -> Path:
    src_str = str(CORE_SRC)
    if sys.path[:1] != [src_str]:
        sys.path[:] = [src_str, *(entry for entry in sys.path if entry != src_str)]

    pkg_dirs = (
        ("zava_forward", str(CORE_SRC / "zava_forward")),
        ("zava_forward.core", str(CORE_SRC / "zava_forward" / "core")),
    )
    for mod_name, pkg_dir in pkg_dirs:
        mod = sys.modules.get(mod_name)
        if mod is not None and hasattr(mod, "__path__"):
            mod_paths = list(mod.__path__)
            if mod_paths[:1] != [pkg_dir]:
                mod.__path__ = [pkg_dir, *(entry for entry in mod_paths if entry != pkg_dir)]

    return CORE_SRC


ensure_worktree_src()
