"""Working dataset location shared by the runtime and synthetic generators."""

import os
from collections.abc import Mapping
from pathlib import Path


def data_file(env: Mapping[str, str] | None = None) -> Path:
    values = os.environ if env is None else env
    configured = values.get("ZF_DATA")
    if not configured:
        return Path.home() / ".zava-forward" / "data" / "zavaforward.json"
    path = Path(configured).expanduser()
    return path / "zavaforward.json" if path.is_dir() or not path.suffix else path
