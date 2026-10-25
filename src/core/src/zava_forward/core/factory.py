"""Choose the store from the environment: ZF_STORE=json (default), sqlite or mssql (Azure SQL)."""
import os

from .data_paths import data_file
from .sqlstore import SqlStore
from .store import Store


def sqlite_path(env=None):
    env = os.environ if env is None else env
    return env.get("ZF_SQLITE") or os.path.join(env.get("ZF_STATE") or os.path.dirname(str(data_file(env))), "zavaforward.sqlite")


def open_store(env=None):
    env = os.environ if env is None else env
    data = str(data_file(env))
    state = env.get("ZF_STATE")
    kind = (env.get("ZF_STORE") or "json").lower()
    if kind == "sqlite":
        return SqlStore(data, sqlite_path(env))
    if kind == "mssql":
        from .mssqlstore import MssqlStore
        return MssqlStore(data, env=env, state_dir=state)
    if kind != "json":
        raise SystemExit(f"Unknown ZF_STORE {kind!r}. Use json, sqlite or mssql.")
    return Store(data, os.path.join(state, "live.json") if state else None,
                 os.path.join(state, "audit.jsonl") if state else None)
