#!/usr/bin/env python3
"""Read-only completion notifier for an explicit set of run-owned tmux sessions.

Verifies every named session exists, then waits (bounded) for the first one to
disappear and prints structured JSON. It never launches, kills or changes a
session, and it grants no authority: the caller still verifies exit, head and
evidence. Exit codes: 0 finished, 3 timeout, 2 missing at start or bad input,
1 tmux or tool failure.
"""

import argparse
import datetime
import json
import math
import subprocess
import sys
import time

EXIT_FINISHED, EXIT_ERROR, EXIT_START_MISSING, EXIT_TIMEOUT = 0, 1, 2, 3


class WatchError(Exception):
    def __init__(self, message, code=EXIT_ERROR, missing=()):
        super().__init__(message)
        self.code = code
        self.missing = sorted(missing)


def list_sessions():
    try:
        result = subprocess.run(
            ["tmux", "list-sessions", "-F", "#{session_name}"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise WatchError(f"tmux unavailable: {exc}") from exc
    if result.returncode:
        stderr = result.stderr.strip()
        if "no server running" in stderr or (
            "error connecting" in stderr and "No such file or directory" in stderr
        ):
            return set()
        raise WatchError(f"tmux list-sessions failed: {stderr or result.returncode}")
    return set(result.stdout.splitlines())


def now():
    return datetime.datetime.now(datetime.UTC).isoformat()


def watch(
    sessions,
    timeout=600.0,
    poll=2.0,
    query=None,
    pause=time.sleep,
    clock=time.monotonic,
    stamp=now,
):
    query = query or list_sessions
    watched = set(sessions)
    if not watched or any(not name.strip() for name in watched):
        raise WatchError("explicit non-empty run-owned session names required", EXIT_START_MISSING)
    started_at = stamp()
    missing = watched - query()
    if missing:
        raise WatchError(
            "sessions absent before watch started; not a completion", EXIT_START_MISSING, missing
        )
    deadline = clock() + timeout
    while True:
        pause(min(poll, max(deadline - clock(), 0.0)))
        active = query()
        done = watched - active
        if done:
            at = stamp()
            return {
                "event": "native_sessions_finished",
                "started_at": started_at,
                "observed_at": at,
                "finished": [{"session": s, "observed_at": at} for s in sorted(done)],
                "remaining": sorted(watched & active),
            }, EXIT_FINISHED
        if clock() >= deadline:
            return {
                "event": "watch_timeout",
                "started_at": started_at,
                "observed_at": stamp(),
                "finished": [],
                "remaining": sorted(watched),
            }, EXIT_TIMEOUT


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("sessions", nargs="+", help="run-owned tmux session names")
    parser.add_argument("--timeout", type=float, default=600.0, help="seconds")
    parser.add_argument("--poll", type=float, default=2.0, help="seconds")
    args = parser.parse_args(argv)
    for value in (args.timeout, args.poll):
        if not math.isfinite(value) or value <= 0:
            parser.error("--timeout and --poll must be finite and positive")
    try:
        event, code = watch(args.sessions, args.timeout, args.poll)
    except WatchError as exc:
        event = {
            "event": "watch_error",
            "error": str(exc),
            "missing": exc.missing,
            "observed_at": now(),
        }
        code = exc.code
    print(json.dumps(event, indent=2), flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
