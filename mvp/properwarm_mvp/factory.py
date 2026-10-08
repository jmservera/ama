"""Choose the store from the environment: PW_STORE=json (default) or sqlite."""
import os
from pathlib import Path

from .sqlstore import SqlStore
from .store import Store


def open_store(env=None):
    env = os.environ if env is None else env
    data = env.get("PW_DATA", str(Path(__file__).resolve().parents[1] / "data" / "properwarm.json"))
    state = env.get("PW_STATE")
    kind = (env.get("PW_STORE") or "json").lower()
    if kind == "sqlite":
        db = env.get("PW_SQLITE") or os.path.join(state or os.path.dirname(data), "properwarm.sqlite")
        return SqlStore(data, db)
    if kind != "json":
        raise SystemExit(f"Unknown PW_STORE {kind!r}. Use json or sqlite.")
    return Store(data, os.path.join(state, "live.json") if state else None,
                 os.path.join(state, "audit.jsonl") if state else None)
