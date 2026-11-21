"""Scheduled orchestrator entrypoint: version probe (`no args`) and bounded `run` job check."""

from __future__ import annotations

import json
import os
import sys
from collections.abc import Mapping, Sequence
from urllib.parse import urlparse

from zava_forward.core.container_hardening import (
    ContainerHardeningError,
    enforce_from_env,
    prepare_private_scratch,
)
from zava_forward.core.diagnostic_logging import install_diagnostic_redaction

from zava_forward.orchestrator.version import __version__


def _valid_url(raw: str, *, schemes: tuple[str, ...]) -> bool:
    parsed = urlparse(raw)
    return parsed.scheme in schemes and bool(parsed.hostname)


def main(
    argv: Sequence[str] | None = None,
    env: Mapping[str, str] | None = None,
) -> int:
    active_env = os.environ if env is None else env
    try:
        prepare_private_scratch(active_env)
        enforce_from_env(active_env)
    except ContainerHardeningError as error:
        print(f"Refusing to start: {error}", file=sys.stderr, flush=True)
        return 2
    install_diagnostic_redaction()
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(f"zava-forward-orchestrator {__version__}")
        return 0
    if args == ["run"]:
        task_queue = active_env.get("TASK_QUEUE", "").strip()
        queue_endpoint = active_env.get("QUEUE_ENDPOINT", "").strip()
        api_base_url = active_env.get("API_BASE_URL", "").strip()
        dispatch_mode = active_env.get("ZF_ORCHESTRATOR_DISPATCH", "standby").strip().lower()
        if not task_queue:
            print(
                "zava-forward-orchestrator run: TASK_QUEUE is required.",
                file=sys.stderr,
                flush=True,
            )
            return 2
        if queue_endpoint and not _valid_url(queue_endpoint, schemes=("https",)):
            print(
                "zava-forward-orchestrator run: QUEUE_ENDPOINT must be an https URL.",
                file=sys.stderr,
                flush=True,
            )
            return 2
        if api_base_url and not _valid_url(api_base_url, schemes=("http", "https")):
            print(
                "zava-forward-orchestrator run: API_BASE_URL must be an http(s) URL.",
                file=sys.stderr,
                flush=True,
            )
            return 2
        if dispatch_mode not in ("", "standby", "off"):
            print(
                "zava-forward-orchestrator run: autonomous queue dispatch is gated off; "
                "expected standby mode.",
                file=sys.stderr,
                flush=True,
            )
            return 2
        print(
            json.dumps(
                {
                    "job": "orchestrator",
                    "mode": "standby",
                    "status": "ok",
                    "taskQueue": task_queue,
                    "version": __version__,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        return 0
    print("Usage: python -m zava_forward.orchestrator [run]", file=sys.stderr, flush=True)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
