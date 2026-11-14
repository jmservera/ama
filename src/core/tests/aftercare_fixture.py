"""Ensure bare unittest discovery in a git worktree loads sibling src/core/src."""

import sys
from pathlib import Path

CORE_SRC: Path = Path(__file__).resolve().parents[1] / "src"


def ensure_worktree_src() -> Path:
    src_str = str(CORE_SRC)
    if sys.path[:1] != [src_str]:
        sys.path[:] = [src_str, *(entry for entry in sys.path if entry != src_str)]

    zf_dir = str(CORE_SRC / "zava_forward")
    zf_mod = sys.modules.get("zava_forward")
    if zf_mod is not None and hasattr(zf_mod, "__path__"):
        zf_paths = list(zf_mod.__path__)
        if zf_paths[:1] != [zf_dir]:
            zf_mod.__path__ = [zf_dir, *(entry for entry in zf_paths if entry != zf_dir)]

    for name in list(sys.modules):
        if name == "zava_forward.core" or name.startswith("zava_forward.core."):
            mod = sys.modules.get(name)
            mod_file = getattr(mod, "__file__", None)
            if mod_file is not None:
                if not Path(mod_file).resolve().is_relative_to(CORE_SRC):
                    sys.modules.pop(name, None)
            else:
                core_dir = str(CORE_SRC / "zava_forward" / "core")
                mod_paths = list(getattr(mod, "__path__", ()))
                if mod_paths[:1] != [core_dir]:
                    sys.modules.pop(name, None)

    return CORE_SRC


ensure_worktree_src()
