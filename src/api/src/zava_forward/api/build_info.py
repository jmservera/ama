"""Build provenance: the source commit baked into the image at build time."""

import os
import re
from collections.abc import Mapping

_COMMIT = re.compile(r"[0-9a-f]{7,40}")


def commit(env: Mapping[str, str] | None = None) -> str:
    value = (os.environ if env is None else env).get("ZF_BUILD_COMMIT", "").strip().lower()
    return value if _COMMIT.fullmatch(value) else "unknown"


def startup_line(env: Mapping[str, str] | None = None) -> str:
    return f"build: commit={commit(env)}"
