"""Read-only provenance guard for API tests that must run against this checkout (#1847)."""

from __future__ import annotations

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2]


def foreign_zava_modules(src_root: Path = SRC_ROOT) -> list[str]:
    """Loaded zava_forward modules whose file is outside src_root."""
    return sorted(
        name
        for name, mod in list(sys.modules.items())
        if (name == "zava_forward" or name.startswith("zava_forward."))
        and isinstance(mod_file := getattr(mod, "__file__", None), str)
        and not Path(mod_file).resolve().is_relative_to(src_root)
    )


def assert_source_isolated(label: str, src_root: Path = SRC_ROOT) -> None:
    """Reject a foreign layout without purging sys.modules or editing sys.path."""
    foreign = foreign_zava_modules(src_root)
    if foreign:
        raise ImportError(
            f"unsupported layout: zava_forward modules loaded from outside {src_root} "
            f"before {label}; use an editable install of this checkout or put its source "
            f"roots first on sys.path (foreign: {', '.join(foreign[:5])})"
        )
