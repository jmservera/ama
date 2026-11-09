"""Second operating-system process for the two-process dispatch-fence regressions.

It is built like the API process: its own working store connection, its own Assistants service and
its own real Ai client, all over the same shared databases and the same loopback TLS peer as the
parent. It admits one sealed simulation request through the production App route, stalls where the
financial meter's last check sits (after admission, before the first request byte), and resumes only
when the parent signals. It prints one JSON line with what the route returned and what it counted.
"""

from __future__ import annotations

import json
import os
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from zava_forward.core.ai import Ai
from zava_forward.core.assistants import Assistants
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App

build_app: Callable[..., Any] = App


class Nobody:
    name = "none"

    def authenticate(self, headers: Any) -> None:
        return None


class StallingMeter:
    """Counts reservations and checks; stalls at the last check until the parent signals."""

    def __init__(self, admitted: Path, go: Path, stall: float) -> None:
        self.admitted, self.go, self.stall = admitted, go, stall
        self.reserved = self.checked = 0

    def reserve(self, *args: object, **kwargs: object) -> str:
        self.reserved += 1
        return "rid"

    def dispatch_check(self, rid: str) -> None:
        self.checked += 1
        self.admitted.write_text("admitted")
        deadline = time.monotonic() + 60
        while not self.go.exists() and time.monotonic() < deadline:
            time.sleep(0.05)
        time.sleep(self.stall)

    def complete(self, *args: object, **kwargs: object) -> None:
        return None


def main(spec: dict[str, Any]) -> dict[str, Any]:
    store = SqlStore(spec["seed"], spec["db"])
    ai = Ai()
    ai.endpoint, ai.token, ai.expires = spec["endpoint"], "t", time.time() + 3600
    tokens: list[int] = []
    real_token = ai._token

    def counted_token() -> str:
        tokens.append(1)
        token: str = real_token()
        return token

    ai._token = counted_token
    ai.model_version = ai.model_version_strong = (
        "test-model"  # the parent's constructed release binds this
    )
    store.ai = ai
    ai.release = store.release_context
    service = Assistants(store, spec["settings"])
    meter = StallingMeter(Path(spec["admitted"]), Path(spec["go"]), float(spec["stall"]))
    app = build_app(store, provider=Nobody())
    app.assistants = service
    ai.consumption = meter  # the app and service install their own ledger; count instead
    result = app.simulation_act(spec["user"], "request")
    service.stop()
    return dict(
        status=result.get("status"),
        reason=result.get("reason"),
        reserved=meter.reserved,
        checked=meter.checked,
        tokens=len(tokens),
    )


if __name__ == "__main__":
    print(json.dumps(main(json.loads(sys.argv[1])), sort_keys=True), flush=True)
    os._exit(0)
