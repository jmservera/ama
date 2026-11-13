"""Run loop for the agents worker: poll, stop on signal, never crash on one bad task.

The loop drives the `dispatch` ports. `serve` builds the queue adapter, API
post-back and provider from the environment (`runtime`) and refuses, naming the
missing settings, until they are complete. While `ZF_AGENT_RESULT_ROUTE` is not
`enabled` it stays in standby: alive and healthy, consuming no messages, exit 0 on
SIGTERM. Stopping is cooperative: an in-flight
task finishes or is released for redelivery, and nothing is acknowledged before
its result is posted.
"""

from __future__ import annotations

import os
import signal
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any

from zava_forward.core.diagnostic_logging import install_diagnostic_redaction

from zava_forward.agents.dispatch import AgentWorker, ResultSink, TaskQueue, run_once
from zava_forward.agents.runtime import (
    HEARTBEAT_MAX_AGE_SECONDS,
    HEARTBEAT_NAME,
    ROUTE_FLAG,
    ConfigError,
    beat,
    build_runtime,
    healthy,
    limits_active,
)

IDLE_SECONDS = 2.0
ERROR_BACKOFF_SECONDS = 5.0
NOT_CONFIGURED = 2
EXPIRED = 3


def serve(
    queue: TaskQueue,
    worker: AgentWorker,
    sink: ResultSink,
    limits: Any,
    stop: threading.Event,
    idle: float = IDLE_SECONDS,
    backoff: float = ERROR_BACKOFF_SECONDS,
    alive: Callable[[], bool] | None = None,
    pulse: Callable[[], None] | None = None,
) -> int:
    """Process tasks until `stop` is set or `alive` turns false; returns tasks completed."""
    done = 0
    while not stop.is_set():
        if alive is not None and not alive():
            stop.set()
            break
        if pulse is not None:
            pulse()
        try:
            handled = run_once(queue, worker, sink, limits)
        except Exception:
            # A transport fault on receive must not end the worker; retry after a pause.
            stop.wait(backoff)
            continue
        if handled:
            done += 1
        else:
            stop.wait(idle)
    worker.stop_event.set()
    return done


def install_signal_handlers(stop: threading.Event) -> None:
    for signum in (signal.SIGTERM, signal.SIGINT):
        signal.signal(signum, lambda *_: stop.set())


def main(argv: list[str] | None = None) -> int:
    """`serve` runs the queue worker, `health` checks it, no argument prints the version."""
    import sys

    install_diagnostic_redaction()
    args = sys.argv[1:] if argv is None else argv
    heartbeat = Path(os.environ.get("ZF_STATE", "/state")) / HEARTBEAT_NAME
    if args[:1] == ["health"]:
        return 0 if healthy(heartbeat, HEARTBEAT_MAX_AGE_SECONDS) else 1
    if args[:1] == ["serve"]:
        if os.environ.get(ROUTE_FLAG) != "enabled":
            stop = threading.Event()
            install_signal_handlers(stop)
            print(
                "zava-forward-agents serve: standby, queue consumption is off. "
                "No tasks will be processed.",
                file=sys.stderr,
            )
            beat(heartbeat)
            while not stop.wait(IDLE_SECONDS):
                beat(heartbeat)
            return 0
        try:
            runtime = build_runtime(os.environ)
        except ConfigError as error:
            print(
                f"zava-forward-agents serve: {error} No tasks will be processed.",
                file=sys.stderr,
            )
            return NOT_CONFIGURED
        stop = threading.Event()
        install_signal_handlers(stop)
        serve(
            runtime.queue,
            runtime.worker,
            runtime.sink,
            runtime.limits,
            stop,
            idle=IDLE_SECONDS,
            alive=lambda: limits_active(runtime.limits),
            pulse=lambda: beat(heartbeat),
        )
        return EXPIRED if not limits_active(runtime.limits) else 0
    from zava_forward.agents.version import __version__

    print(f"zava-forward-agents {__version__}")
    return 0
