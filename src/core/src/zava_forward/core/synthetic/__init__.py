"""Seeded synthetic data tools. No image entry point imports this sub-package."""

import os
from collections.abc import Mapping
from pathlib import Path


def output_dir(name: str, env: Mapping[str, str] | None = None) -> Path:
    """Default folder for generated working data, outside the repository (ADR 0006).

    ZF_DATA may name a folder or the data file the runtime opens; a file means its folder.
    Without ZF_DATA the per-user folder ~/.zava-forward/data is used. Never under src/.
    """
    values: Mapping[str, str] = os.environ if env is None else env
    configured = values.get("ZF_DATA")
    if not configured:
        root = Path.home() / ".zava-forward" / "data"
    else:
        path = Path(configured).expanduser()
        root = path if path.is_dir() or not path.suffix else path.parent
    return root / name
