"""Test-only OS-process worker for assistant release and allowance races (issue #107).

Not a test module. Opens a source-current store and service, logs fake provider calls to an
append-only file, and runs execute actions behind bounded file barriers. It never reads private
data and never calls a real provider.
"""

import importlib
import json
import os
import sys
import time
import traceback
from typing import Any

from zava_forward.core.assistants import Assistants

shared: Any = importlib.import_module("test_assistants")


def wait_for(path: str, deadline: float) -> None:
    while not os.path.exists(path):
        if time.monotonic() > deadline:
            raise TimeoutError(path)
        time.sleep(0.02)


def touch(path: str) -> None:
    with open(path, "w") as handle:
        handle.write(str(os.getpid()))


def main(spec: dict[str, Any]) -> None:
    barrier: str = spec["barrier"]
    deadline = time.monotonic() + spec["deadline"]
    if spec["kind"] == "mssql":
        from zava_forward.core.mssqlstore import MssqlStore

        store: Any = MssqlStore(spec["seed"], env=dict(os.environ), state_dir=spec["state_dir"])
    else:
        from zava_forward.core.sqlstore import SqlStore

        store = SqlStore(spec["seed"], spec["db"])
    provider: Any = shared.Provider()
    inner = provider.evidence

    def evidence(system: str, prompt: str, max_tokens: int, timeout: int) -> Any:
        fd = os.open(spec["call_log"], os.O_WRONLY | os.O_APPEND | os.O_CREAT)
        try:
            os.write(fd, f"{spec['label']} {os.getpid()}\n".encode())
        finally:
            os.close(fd)
        return inner(system, prompt, max_tokens, timeout)

    provider.evidence = evidence
    provider.model_version = provider.model_version_strong = "test-model"
    provider.release = store.release_context
    store.ai = provider
    service: Any = Assistants(store, shared.config(**spec["config"]))
    results: list[bool] = []
    try:
        if spec["gate"]:
            claim: Any = service.claim
            gated: list[str] = []

            def gated_claim(tid: str, owner: str) -> Any:
                if not gated:
                    gated.append(tid)
                    touch(os.path.join(barrier, f"claim-{spec['label']}"))
                    wait_for(os.path.join(barrier, "go"), deadline)
                return claim(tid, owner)

            service.claim = gated_claim
        touch(os.path.join(barrier, f"ready-{spec['label']}"))
        wait_for(os.path.join(barrier, "start"), deadline)
        for tid in spec["tasks"]:
            results.append(service.execute(tid))
    finally:
        service.stop()
        store.db.close()
    print(json.dumps(dict(label=spec["label"], pid=os.getpid(), results=results)))


if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as handle:
            main(json.load(handle))
    except BaseException:
        traceback.print_exc()
        sys.exit(2)
