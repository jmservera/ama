"""Choose the store from the environment: PW_STORE=json (default), sqlite or mssql (Azure SQL)."""
import os
import json
import sqlite3
from pathlib import Path

from .sqlstore import SqlStore
from .store import Store


def open_store(env=None):
    env = os.environ if env is None else env
    if env.get("PW_EXERCISE") == "1":
        from . import exercise
        if env.get("PW_STORE", "sqlite") != "sqlite" or env.get("PW_DATA"):
            raise SystemExit("Exercise mode requires its fictional seed and SQLite, not PW_DATA.")
        if env.get("PW_DOC_STORE", "local") != "local":
            raise SystemExit("Exercise mode requires local evidence storage, not an external backend.")
        state = Path(env.get("PW_STATE", "")).expanduser()
        if not env.get("PW_STATE") or not state.is_absolute() or state.is_symlink():
            raise SystemExit("PW_STATE must name an explicit absolute exercise state directory.")
        state.mkdir(parents=True, exist_ok=True)
        seed, db = state / "exercise.json", state / "properwarm.sqlite"
        existing_database = db.exists()
        if seed.is_symlink() or db.is_symlink():
            raise SystemExit("Exercise seed/database must not be symlinks.")
        if seed.exists():
            with seed.open(encoding="utf-8") as stream:
                if json.load(stream) != exercise.dataset():
                    raise SystemExit("Exercise seed is incompatible; choose a new state directory.")
        if db.exists():
            with sqlite3.connect(f"file:{db}?mode=ro", uri=True) as connection:
                try:
                    rows = connection.execute("SELECT id, body FROM cases").fetchall()
                    observed_as_of = connection.execute("SELECT value FROM meta WHERE key='as_of'").fetchone()
                except sqlite3.Error as error:
                    raise SystemExit("Incompatible exercise database; choose a new state directory.") from error
            expected = {case["id"] for case in exercise.dataset()["cases"]}
            if {row[0] for row in rows} != expected or any(
                json.loads(row[1]).get("exercise", {}).get("fixture_version") != exercise.FIXTURE_VERSION for row in rows
            ):
                raise SystemExit("Exercise database is incompatible; no data was overwritten.")
            if observed_as_of is None or observed_as_of[0] != exercise.AS_OF:
                raise SystemExit("Exercise database as-of metadata is incompatible; no silent date migration.")
        if not seed.exists():
            exercise.create_seed(seed)
        store = SqlStore(str(seed), str(db), docs_dir=str(state / "docs"), digest_dir=str(state / "digests"))
        if not existing_database:
            store.db.execute("UPDATE meta SET value=? WHERE key='as_of'", (exercise.AS_OF,))
            store.db.commit()
        store.as_of = exercise.AS_OF
        return store
    data = env.get("PW_DATA", str(Path(__file__).resolve().parents[1] / "data" / "properwarm.json"))
    state = env.get("PW_STATE")
    kind = (env.get("PW_STORE") or "json").lower()
    if kind == "sqlite":
        db = env.get("PW_SQLITE") or os.path.join(state or os.path.dirname(data), "properwarm.sqlite")
        return SqlStore(data, db)
    if kind == "mssql":
        from .mssqlstore import MssqlStore
        return MssqlStore(data, env=env, state_dir=state)
    if kind != "json":
        raise SystemExit(f"Unknown PW_STORE {kind!r}. Use json, sqlite or mssql.")
    return Store(data, os.path.join(state, "live.json") if state else None,
                 os.path.join(state, "audit.jsonl") if state else None)
