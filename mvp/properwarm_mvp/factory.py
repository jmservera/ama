"""Choose the store from the environment: PW_STORE=json (default), sqlite or mssql (Azure SQL)."""
import os
import json
import sqlite3
from pathlib import Path

from .sqlstore import SqlStore
from .store import Store


def open_store(env=None):
    env = os.environ if env is None else env
    if env.get("PW_PROGRAMME") == "1":
        return _open_programme(env)
    if env.get("PW_EXERCISE") == "1":
        from . import exercise
        kind = env.get("PW_STORE", "sqlite")
        if kind not in ("sqlite", "mssql") or env.get("PW_DATA"):
            raise SystemExit("Exercise mode requires its fictional seed and SQLite or MSSQL, not PW_DATA.")
        doc_kind = env.get("PW_DOC_STORE", "local")
        if doc_kind not in ("local", "azure-blob") or (kind == "sqlite" and doc_kind != "local"):
            raise SystemExit("Exercise storage must be SQLite/local or MSSQL with local/azure-blob evidence.")
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
        if kind == "mssql":
            return _open_exercise_mssql(env, state, seed)
        if db.exists():
            with sqlite3.connect(f"file:{db}?mode=ro", uri=True) as connection:
                try:
                    rows = connection.execute("SELECT id, body FROM cases").fetchall()
                    observed_as_of = connection.execute("SELECT value FROM meta WHERE key='as_of'").fetchone()
                    recovery = connection.execute("SELECT value FROM meta WHERE key='exercise_recovery_pending'").fetchone()
                except sqlite3.Error as error:
                    raise SystemExit("Incompatible exercise database; choose a new state directory.") from error
            expected = {case["id"] for case in exercise.dataset()["cases"]}
            if {row[0] for row in rows} != expected or any(
                json.loads(row[1]).get("exercise", {}).get("fixture_version") != exercise.FIXTURE_VERSION for row in rows
            ):
                raise SystemExit("Exercise database is incompatible; no data was overwritten.")
            if observed_as_of is None or observed_as_of[0] != exercise.AS_OF:
                raise SystemExit("Exercise database as-of metadata is incompatible; no silent date migration.")
            if recovery is not None:
                raise SystemExit("Exercise restore awaits offline operator reconciliation. No controlled work may resume; preserve the recovery marker and missing-event evidence.")
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


def _open_exercise_mssql(env, state, seed):
    """Check remote fixture identity before the SQL store can migrate or seed."""
    from . import exercise
    from .documents import open_document_store
    from .mssqlstore import MssqlStore, _Conn, connection_string

    connection = _Conn(connection_string(env), env.get("PW_SQL_TOKEN"))
    try:
        tables = {row[0] for row in connection.execute(
            "SELECT name FROM sys.tables WHERE is_ms_shipped=0").fetchall()}
        existing = bool(tables)
        if existing:
            if not {"cases", "meta", "staff", "audit", "audit_head"}.issubset(tables):
                raise SystemExit("Incompatible exercise SQL schema; no migration or seed was performed.")
            rows = connection.execute("SELECT id, body FROM cases").fetchall()
            metadata = dict(connection.execute("SELECT [key], value FROM meta").fetchall())
            expected = {case["id"] for case in exercise.dataset()["cases"]}
            if {row[0] for row in rows} != expected or any(
                json.loads(row[1]).get("exercise", {}).get("fixture_version") != exercise.FIXTURE_VERSION
                for row in rows
            ):
                raise SystemExit("Exercise SQL database is incompatible; no data was overwritten.")
            if metadata.get("as_of") != exercise.AS_OF:
                raise SystemExit("Exercise SQL as-of metadata is incompatible; no silent date migration.")
            if "exercise_recovery_pending" in metadata:
                raise SystemExit("Exercise SQL restore awaits offline operator reconciliation.")
    finally:
        connection.raw.close()
    if not seed.exists():
        exercise.create_seed(seed)
    store = MssqlStore(str(seed), env=env, state_dir=str(state))
    if not existing:
        store._meta_set("as_of", exercise.AS_OF)
    store.as_of = exercise.AS_OF
    store.docstore = open_document_store(str(state / "docs"), env=env)
    return store


def _open_programme(env):
    """Open the operator-imported original dataset without a fixture reseed."""
    from .mssqlstore import MssqlStore, _Conn, connection_string
    from .programme import SOURCE_KEYS
    from .documents import open_document_store

    if (env.get("PW_EXERCISE") != "1" or env.get("PW_STORE") != "mssql"
            or env.get("PW_AI") != "on" or not env.get("AI_ENDPOINT")
            or env.get("PW_DOC_STORE") != "azure-blob"):
        raise SystemExit("Programme MVP requires Azure SQL/Blob and enabled real AI with bounded exercise controls.")
    state = Path(env.get("PW_STATE", ""))
    if not state.is_absolute() or state.is_symlink():
        raise SystemExit("Programme MVP requires an explicit absolute state directory.")
    connection = _Conn(connection_string(env), env.get("PW_SQL_TOKEN"))
    try:
        row = connection.execute("SELECT [value] FROM meta WHERE [key]='programme_source'").fetchone()
        if row is None:
            raise SystemExit("Import the original generated programme and stock before app startup.")
        source = json.loads(row[0])
        if (not all(source.get(key) for key in SOURCE_KEYS)
                or source["stock_count"] != 60000 or source["case_count"] != 980
                or source["programme_sha256"] != env.get("PW_PROGRAMME_SHA256")
                or source["stock_sha256"] != env.get("PW_STOCK_SHA256")):
            raise SystemExit("Programme source lineage does not match the reviewed deployment.")
        if (connection.execute("SELECT COUNT(*) FROM stock").fetchone()[0] != 60000
                or connection.execute("SELECT COUNT(*) FROM cases").fetchone()[0] != 980):
            raise SystemExit("Programme dataset counts differ; no automatic replacement or reseed.")
        if connection.execute("SELECT value FROM meta WHERE [key]='exercise_recovery_pending'").fetchone():
            raise SystemExit("Programme restore awaits offline operator reconciliation.")
    finally:
        connection.raw.close()
    state.mkdir(parents=True, exist_ok=True)
    store = MssqlStore(env.get("PW_DATA", "/data/properwarm.json"), env=env, state_dir=str(state))
    store.docstore = open_document_store(str(state / "docs"), env=env)
    return store
