"""Insert-only merge of a generated synthetic seed into a populated SQL store.

    ZF_STORE=mssql ... python -m zava_forward.core.seed_merge --seed PATH
    ZF_STORE=mssql ... python -m zava_forward.core.seed_merge --seed PATH --apply --expect-added N

The first form is a dry run. The store is opened from the environment like the app,
so the schema must already be current. Output is counts only.
"""

import argparse
import json
import os
import sys
import tempfile
from collections.abc import Mapping, Sequence

from .factory import open_store, sqlite_path
from .sqlstore import SeedMergeError, SqlStore


def main(argv: Sequence[str] | None = None, env: Mapping[str, str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument(
        "--seed", required=True, help="generated seed JSON (kept private, never committed)"
    )
    p.add_argument("--apply", action="store_true", help="write; the default is a dry run")
    p.add_argument(
        "--expect-added", type=int, help="refuse unless exactly this many cases would be added"
    )
    a = p.parse_args(argv)
    with tempfile.TemporaryDirectory() as tmp:
        # First-start seeding must never see the real seed, so an empty target stays empty.
        empty = os.path.join(tmp, "empty.json")
        with open(empty, "w", encoding="utf-8") as f:
            json.dump(dict(cases=[], staff=[]), f)
        values = dict(os.environ if env is None else env)
        # Fix the SQLite target before ZF_DATA is replaced, or the default path would move.
        if (values.get("ZF_STORE") or "").lower() == "sqlite":
            values["ZF_SQLITE"] = sqlite_path(values)
        return _merge(a, dict(values, ZF_DATA=empty))


def _merge(a: argparse.Namespace, env: dict[str, str]) -> int:
    if (env.get("ZF_STORE") or "").lower() not in ("sqlite", "mssql"):
        print("ZF_STORE must be sqlite or mssql.", file=sys.stderr)
        return 2
    store = open_store(env)
    assert isinstance(store, SqlStore)
    if store.db.execute("SELECT COUNT(*) FROM cases").fetchone()[0] == 0:
        print(
            "The target database has no cases; seed an empty one through the first start.",
            file=sys.stderr,
        )
        return 2
    try:
        report = store.merge_seed(a.seed, apply=a.apply, expect_added=a.expect_added)
    except SeedMergeError as e:
        print(json.dumps(dict(error=str(e), report=e.report)))
        return 3
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
