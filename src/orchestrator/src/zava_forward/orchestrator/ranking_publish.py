"""Scheduled publication of the ranking snapshot to the Blob archive (Refs #79, criterion 4).

Reads the open cases and their as-of date from the configured store, ranks them under the latest
policy in the verified registry and writes one create-only, hash-verified record to the Blob
archive chosen by the owner (ZF_RANKING_ARCHIVE=azure-blob). All verification, sign-off refusal
and idempotency stay in ranking_publication_runner.run; nothing here overwrites or deletes a record.

The shipped policy is an unsigned draft, so until a named owner signs a new policy version the run
is refused and exits 1 with RANKING_PUBLISH_BLOCKED. That is the intended, visible state.

Exit codes: 0 published or already published for current data; 1 blocked, failed or the data is
not dated the run date (the record is still written); 2 the Blob archive is not configured.
"""

import argparse
import copy
import datetime
import json
import os
import sys
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from zava_forward.core import ranking_archive_blob, ranking_publication_runner

OK_MARKER = "RANKING_PUBLISH_OK"
BLOCKED_MARKER = "RANKING_PUBLISH_BLOCKED"
ALERT_MARKER = "RANKING_PUBLISH_ALERT"


def open_cases(store: Any) -> tuple[list[dict[str, Any]], str | None]:
    """Copy the open cases and as_of from a store; a non-boolean closed flag refuses the source."""
    with store.lock:
        cases = [copy.deepcopy(c) for c in store.cases.values()]
        as_of = store.as_of
    for c in cases:
        if not isinstance(c.get("closed"), bool):
            raise TypeError("a case has no boolean closed flag")
    return [c for c in cases if not c["closed"]], as_of


def _run(
    env: Mapping[str, str] | None,
    store: Any,
    archive: Any,
    today: str,
    registry: Mapping[str, Any] | None,
    out: Callable[[str], object],
) -> int:
    if archive is None:
        try:
            archive = ranking_archive_blob.open_ranking_archive(os.environ if env is None else env)
        except ranking_archive_blob.BlobArchiveError:
            archive = None
    if archive is None:
        out(
            "Blob archive is not configured: set ZF_RANKING_ARCHIVE=azure-blob, "
            "ZF_BLOB_ACCOUNT_URL and ZF_RANKING_BLOB_CONTAINER."
        )
        return 2
    if store is None:
        from zava_forward.core.factory import open_store

        store = open_store(env)
    cases, as_of = open_cases(store)
    res = ranking_publication_runner.run(
        "publish", archive, today, cases=cases, as_of=as_of, registry=registry
    )
    out(json.dumps(res, sort_keys=True, indent=2))
    status = res["status"]
    if status in ("published", "already_published"):
        detail = f"status={status} as_of={res['as_of']} published_on={res['published_on']}"
        if not res.get("source_current"):
            out(
                f"{ALERT_MARKER} {detail}; the case data is not current for run date {today}, "
                "so no fresh snapshot exists"
            )
            return 1
        out(f"{OK_MARKER} {detail}")
        return 0
    codes = ",".join(r["code"] for r in res["refusals"]) or status
    marker = BLOCKED_MARKER if res["refusals"] else ALERT_MARKER
    out(f"{marker} status={status} codes={codes}")
    return 1


def main(
    argv: Sequence[str] | None = None,
    env: Mapping[str, str] | None = None,
    store: Any = None,
    archive: Any = None,
    registry: Mapping[str, Any] | None = None,
    out: Callable[[str], object] = print,
) -> int:
    """python -m zava_forward.orchestrator.ranking_publish [--today YYYY-MM-DD]"""
    ap = argparse.ArgumentParser(description="Publish the ranking snapshot to the Blob archive.")
    ap.add_argument("--today", help="ISO run date; default is today in UTC")
    a = ap.parse_args(sys.argv[1:] if argv is None else argv)
    today = a.today or datetime.datetime.now(datetime.UTC).date().isoformat()
    try:
        return _run(env, store, archive, today, registry, out)
    except Exception as e:
        # Type name only: store and driver messages can carry connection details.
        out(f"{ALERT_MARKER} ranking publication could not run: {type(e).__name__}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
