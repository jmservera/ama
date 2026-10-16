"""Seeded synthetic data tools. No image entry point imports this sub-package."""

from collections.abc import Mapping
from pathlib import Path

from zava_forward.core.data_paths import data_file


def output_dir(name: str, env: Mapping[str, str] | None = None) -> Path:
    """Default folder for generated working data, outside the repository (ADR 0006).

    ZF_DATA may name a folder or the data file the runtime opens; a file means its folder.
    Without ZF_DATA the per-user folder ~/.zava-forward/data is used. Never under src/.
    """
    return data_file(env).parent / name
