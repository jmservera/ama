"""Fixed worker for the issue #107 older-image SQL probe.

Runs INSIDE the pinned older image (`python -I -B /probe/old_image_worker.py /probe/<spec>.json`) or,
for the labelled self-test only, in the current source over SQLite. It imports only the standard
library and the packaged `zava_forward` modules, and prints exactly one JSON line. The provider is a
local constructed double with a call counter; no network, credential or real model is used.
"""

import hashlib
import importlib
import json
import os
import socket
import sys
import traceback
from typing import Any

PACKAGED = (
    "zava_forward.core.assistants",
    "zava_forward.core.assistant_release",
    "zava_forward.core.mssqlstore",
    "zava_forward.core.sqlstore",
    "zava_forward.core.ai_registry",
    "zava_forward.core.rai_release",
)
VERSIONS = ("zava-forward-core", "zava-forward-agents", "zava-forward-api")
SECRET_KEYS = ("ZF_SQL_PASSWORD", "ZF_SQL_USER")


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


class Provider:
    """Constructed double matching the shape of `test_assistants.Provider`; counts every call."""

    configured = True
    release: Any = None
    sends_no_bytes = True
    provider, endpoint, fast = "local-test-double", "local-test", "test"

    def __init__(self) -> None:
        self.calls = 0
        self.model_version = self.model_version_strong = "test-model"

    def evidence(self, system: str, prompt: str, max_tokens: int, timeout: int) -> dict[str, Any]:
        self.calls += 1
        value = dict(
            summary="Check supplied evidence with the responsible human.",
            findings=[
                dict(
                    text="The home facts are supplied evidence, not an approval.",
                    citations=["source:home"],
                )
            ],
            unknowns=[],
        )
        usage = dict(prompt_tokens=100, completion_tokens=30, total_tokens=130)
        return dict(
            text=canonical(value),
            provider="local-test-double",
            deployment="test",
            model="test-model",
            source="ai",
            outcome="returned",
            usage=usage,
        )


def redact(text: str) -> str:
    for key in SECRET_KEYS:
        secret = os.environ.get(key)
        if secret:
            text = text.replace(secret, "***")
    return text


def sha256(path: str) -> str:
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def identify() -> dict[str, Any]:
    """Which code actually loaded, and which protocol members it offers. Never touches a database."""
    from importlib import metadata

    modules: dict[str, Any] = {}
    missing: list[str] = []
    for name in PACKAGED:
        try:
            module = importlib.import_module(name)
            path = str(module.__file__)
            modules[name] = dict(path=path, sha256=sha256(path))
        except Exception as error:
            missing.append(f"{name}: {type(error).__name__}")
    versions: dict[str, str | None] = {}
    for dist in VERSIONS:
        try:
            versions[dist] = metadata.version(dist)
        except metadata.PackageNotFoundError:
            versions[dist] = None
    needed = (
        ("zava_forward.core.assistants", ("Assistants", "REGISTRY", "runtime_binding")),
        ("zava_forward.core.rai_release", ("CHANGE_TRIGGERS", "EVALUATION_VERSION", "digest")),
        ("zava_forward.core.ai_registry", ("get", "LEGACY", "legacy_binding")),
        ("zava_forward.core.assistant_release", ("releases", "change", "BOUND")),
    )
    for name, members in needed:
        try:
            module = importlib.import_module(name)
        except Exception:
            continue
        missing += [f"{name}.{m}" for m in members if not hasattr(module, m)]
    store_module = (
        "zava_forward.core.mssqlstore" if sql_backend() == "mssql" else "zava_forward.core.sqlstore"
    )
    store_class = "MssqlStore" if sql_backend() == "mssql" else "SqlStore"
    try:
        cls = getattr(importlib.import_module(store_module), store_class)
        missing += [
            f"{store_class}.{m}"
            for m in ("assistant_connection", "release_context")
            if not hasattr(cls, m)
        ]
    except Exception as error:
        missing.append(f"{store_class}: {type(error).__name__}")
    try:
        sys.path.append(os.environ.get("ZF_PROBE_FIXTURES", "/probe"))
        importlib.import_module("release_support")
    except Exception as error:
        missing.append(f"release_support: {type(error).__name__}")
    return dict(
        python=sys.version.split()[0],
        versions=versions,
        modules=modules,
        missing=missing,
        hostname=socket.gethostname(),
        pid=os.getpid(),
    )


def sql_backend() -> str:
    return "mssql" if os.environ.get("ZF_PROBE_BACKEND", "mssql") == "mssql" else "sqlite"


def open_service(spec: dict[str, Any]) -> tuple[Any, Any, Provider]:
    assistants = importlib.import_module("zava_forward.core.assistants")
    seed = spec["seed"]
    if sql_backend() == "mssql":
        from zava_forward.core.mssqlstore import MssqlStore

        store: Any = MssqlStore(seed, env=dict(os.environ), state_dir=spec["state_dir"])
    else:
        from zava_forward.core.sqlstore import SqlStore

        store = SqlStore(seed, spec["db"])
    provider = Provider()
    provider.release = store.release_context
    store.ai = provider
    return store, assistants.Assistants(store, spec["config"]), provider


def pool(service: Any) -> list[list[Any]]:
    with service.transaction() as db:
        rows = db.execute(
            "SELECT calls,tokens,used_calls,reserved_tokens FROM assistant_allowance ORDER BY id"
        ).fetchall()
    return [list(row) for row in rows]


def task_state(service: Any, tid: str) -> str | None:
    with service.transaction() as db:
        row = db.execute("SELECT state FROM assistant_tasks WHERE id=?", (tid,)).fetchone()
    return None if row is None else str(row[0])


def spid(service: Any) -> int | None:
    if sql_backend() != "mssql":
        return None
    with service.transaction() as db:
        return int(db.execute("SELECT @@SPID").fetchone()[0])


def run(spec: dict[str, Any]) -> dict[str, Any]:
    """Run one step. `out` is published before each risky operation, so an error keeps what was observed."""
    out: dict[str, Any] = dict(action=spec["action"], identity=identify())
    if out["identity"]["missing"]:
        out["status"] = "unsupported"
        return out
    if spec["action"] == "identify":
        out["status"] = "ok"
        return out
    store, service, provider = open_service(spec)
    user = spec["principal"]
    tasks: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    again: list[dict[str, Any]] = []
    out.update(tasks=tasks, executed=results, reinvoked=again, provider_calls=0)
    try:
        if spec["action"] == "provision":
            release_support = importlib.import_module("release_support")
            release_support.install(store)
        out["spid"] = spid(service)
        for capability, case in spec.get("invoke", []):
            entry: dict[str, Any] = dict(capability=capability, case=case)
            tasks.append(entry)
            try:
                task = service.invoke(user, capability, case)
                entry.update(id=task["id"], state=task["state"])
            except Exception as error:
                entry["error"] = redact(f"{type(error).__name__}: {error}")
        wanted = list(spec.get("execute", [])) + [
            tasks[i].get("id") for i in spec.get("execute_index", [])
        ]
        for tid in wanted:
            if tid is None:
                results.append(dict(id=None, error="no task to execute"))
                continue
            entry = dict(id=tid, before=task_state(service, tid))
            results.append(entry)
            try:
                entry["result"] = bool(service.execute(tid))
            except Exception as error:
                entry["error"] = redact(f"{type(error).__name__}: {error}")
            out["provider_calls"] = provider.calls
            entry["after"] = task_state(service, tid)
        for capability, case in spec.get("reinvoke", []):
            entry = dict(capability=capability, case=case)
            again.append(entry)
            try:
                entry["state"] = service.invoke(user, capability, case)["state"]
            except Exception as error:
                entry["error"] = redact(f"{type(error).__name__}: {error}")
        out["provider_calls"] = provider.calls
        out["pool"] = pool(service)
        out["status"] = "ok"
    except Exception as error:
        out["status"] = "error"
        out["error"] = redact(f"{type(error).__name__}: {error}")
        out["trace"] = redact(traceback.format_exc()[-2000:])
    finally:
        out["provider_calls"] = provider.calls
        for close in (service.stop, store.db.close):
            try:
                close()
            except Exception as error:
                out.setdefault("close_errors", []).append(
                    redact(f"{type(error).__name__}: {error}")
                )
    return out


def main() -> int:
    try:
        with open(sys.argv[1], encoding="utf-8") as handle:
            result = run(json.load(handle))
    except BaseException as error:
        result = dict(
            status="error",
            error=redact(f"{type(error).__name__}: {error}"),
            trace=redact(traceback.format_exc()[-2000:]),
        )
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
