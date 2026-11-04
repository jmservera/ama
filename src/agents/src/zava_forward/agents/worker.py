"""Run loop for the agents worker: poll, stop on signal, never crash on one bad task.

The loop drives the `dispatch` ports. It adds no transport: the `agent-tasks`
queue adapter and the API post-back are still to be built, so `serve` exits with
a clear refusal until both are supplied. Stopping is cooperative: an in-flight
task finishes or is released for redelivery, and nothing is acknowledged before
its result is posted.
"""

from __future__ import annotations

import signal
import threading
from typing import Any

from zava_forward.agents.dispatch import AgentWorker, ResultSink, TaskQueue, run_once

IDLE_SECONDS = 2.0
ERROR_BACKOFF_SECONDS = 5.0
NOT_CONFIGURED = 2


def serve(
    queue: TaskQueue,
    worker: AgentWorker,
    sink: ResultSink,
    limits: Any,
    stop: threading.Event,
    idle: float = IDLE_SECONDS,
    backoff: float = ERROR_BACKOFF_SECONDS,
) -> int:
    """Process tasks until `stop` is set; returns the number of tasks completed."""
    done = 0
    while not stop.is_set():
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
    """`serve` is refused until a queue adapter and API post-back exist."""
    import sys

    args = sys.argv[1:] if argv is None else argv
    if args[:1] == ["serve"]:
        print(
            "zava-forward-agents serve: no task queue or result post-back is configured; "
            "no tasks will be processed.",
            file=sys.stderr,
        )
        return NOT_CONFIGURED
    from zava_forward.agents.version import __version__

    print(f"zava-forward-agents {__version__}")
    return 0
