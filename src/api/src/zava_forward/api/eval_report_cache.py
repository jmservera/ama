"""Single-flight cache for the report's scripted evaluations.

The golden-file evaluations replay about 150 scripted turns and cost seconds of CPU each,
so recomputing them per request made GET /api/ai/report take over a minute on the demo
container (issue #2303). The key is the evaluation function plus the SHA-256 of its golden
file, so a changed golden file or a patched function recomputes.
"""

from __future__ import annotations

import copy
import hashlib
import threading
from collections import OrderedDict
from collections.abc import Callable
from pathlib import Path
from typing import Any

MAX_ENTRIES = 8
_lock = threading.Lock()
_entries: OrderedDict[tuple[Any, str], Any] = OrderedDict()


def cached(func: Callable[[], Any], golden: Path | str) -> Any:
    digest = hashlib.sha256(Path(golden).read_bytes()).hexdigest()
    key = (func, digest)
    with _lock:
        if key not in _entries:
            _entries[key] = func()
            while len(_entries) > MAX_ENTRIES:
                _entries.popitem(last=False)
        return copy.deepcopy(_entries[key])


def clear() -> None:
    with _lock:
        _entries.clear()
