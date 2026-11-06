"""Local invocation runner for ranking snapshot publication (PR-006, ADR 0002 decision 4, issue 79).

schedule, publish and verify run through ranking_publication; this module adds only the
invocation contract a scheduler (or a person at a terminal) calls:

    python3 -m zava_forward.core.ranking_publication_runner publish \
        --archive DIR --today YYYY-MM-DD --cases FILE [--policy VERSION] [--exercise]

Nothing reads a clock, an environment variable or a default data folder: the date,
the archive and the case file are all explicit. Ranking is a pure function, so no
random seed is consumed; the run key (policy hash, as_of, window start) is the only
identity a repeat run needs. Publishing fails closed and says why when the policy
rule order has no recorded named-owner sign-off, the case source is missing or
unusable, the archive is unverified, or there is no room to write. The retained
publication contract stays a proposal: it is reported as proposed, never approved,
and the retention period stays a separate Legal decision. An exercise run computes
what would be archived and writes nothing. Nothing here changes a ranking or a policy.
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import sys
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from . import ranking, ranking_publication

EXIT_OK, EXIT_PROBLEM, EXIT_REFUSED = 0, 1, 2

PROPOSED_SCHEDULE: dict[str, Any] = {
    "status": "proposed, not an approved operational rule",
    "cadence": ranking_publication.SCHEDULE["cadence"],
    "minimum_frequency_hours": ranking_publication.SCHEDULE["minimum_frequency_hours"],
    "window": "one calendar day, starting on the supplied date",
    "runner": "ranking_publication_runner module; scheduler not yet configured",
    "owner": ranking_publication.SCHEDULE["owner"],
    "retention": ranking_publication.SCHEDULE["retention"],
}

_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
Path = str | os.PathLike[str]


def _refusal(code: str, message: str, next_action: str) -> dict[str, str]:
    return {"code": code, "message": message, "next_action": next_action}


def _date(value: Any) -> datetime.date | None:
    if not isinstance(value, str) or not _DATE.match(value):
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


def load_cases(path: Path) -> tuple[list[Mapping[str, Any]], str | None]:
    """Read open cases and the data's as_of from an explicit store-shaped JSON file; read only."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    cases = data["cases"]
    if not isinstance(cases, list):
        raise TypeError("cases is not a list")
    for c in cases:
        if not isinstance(c, Mapping) or not isinstance(c.get("closed"), bool):
            raise TypeError("a case is not a mapping with a boolean closed flag")
    return [c for c in cases if not c["closed"]], data.get("as_of")


def _free_bytes(archive_dir: Path) -> int:
    probe = os.path.abspath(archive_dir)
    while not os.path.exists(probe):
        probe = os.path.dirname(probe)
    return shutil.disk_usage(probe).free if os.access(probe, os.W_OK) else 0


def _policy_view(
    policy: Mapping[str, Any] | None, problems: Sequence[str]
) -> dict[str, Any] | None:
    if policy is None:
        return None
    return {
        "version": policy["version"],
        "content_hash": policy["content_hash"],
        "owner": policy["owner"],
        "status": policy["status"],
        "signed": not problems,
        "signoff_problems": list(problems),
    }


def run(
    operation: str,
    archive_dir: Path,
    today: str,
    *,
    cases: Sequence[Mapping[str, Any]] | None = None,
    as_of: str | None = None,
    policy_version: str | None = None,
    exercise: bool = False,
    registry: Mapping[str, Any] | None = None,
    free_bytes: Callable[[Path], int] = _free_bytes,
) -> dict[str, Any]:
    """Run schedule, publish or verify for the window starting on today.

    Expected failures are returned as refusals, not raised.
    """
    reg = ranking.POLICIES if registry is None else registry
    out: dict[str, Any] = {
        "operation": operation,
        "today": today,
        "status": "refused",
        "refusals": [],
        "warnings": [],
        "schedule": PROPOSED_SCHEDULE,
        "policy": None,
        "run_key": None,
        "window": None,
        "retention_note": "Retention is a separate Legal decision; nothing is purged here.",
    }
    refusals: list[dict[str, str]] = out["refusals"]
    day = _date(today)
    if operation not in ("schedule", "publish", "verify"):
        refusals.append(
            _refusal(
                "unknown_operation",
                f"Unknown operation {operation!r}.",
                "Use schedule, publish or verify.",
            )
        )
    if day is None:
        refusals.append(
            _refusal(
                "bad_date",
                "today must be an ISO date, YYYY-MM-DD.",
                "Supply the run date explicitly.",
            )
        )
    if refusals:
        return out
    assert day is not None
    if day == datetime.date.max:
        refusals.append(
            _refusal(
                "bad_date",
                "today has no representable next day, so no window can be reported.",
                "Supply a run date before 9999-12-31.",
            )
        )
        return out
    out["window"] = {"start": today, "end": (day + datetime.timedelta(days=1)).isoformat()}

    if operation == "verify":
        res = ranking_publication.verify(archive_dir, reg)
        out.update(res, overdue=bool(res["latest"] is None or res["latest"] < today))
        out["status"] = "ok" if not res["problems"] and not out["overdue"] else "problem"
        return out

    policy = reg.get(policy_version) if policy_version else (ranking.latest(reg) if reg else None)
    if policy is None:
        refusals.append(
            _refusal(
                "policy_unknown",
                "The ranking policy version is not in the verified registry.",
                f"Choose one of: {', '.join(sorted(reg))}.",
            )
        )
    else:
        problems = ranking.signoff_problems(policy)
        out["policy"] = _policy_view(policy, problems)
        if problems and not exercise:
            refusals.append(
                _refusal(
                    "approval_missing",
                    "; ".join(problems),
                    "The named policy owner must sign the rule order as a new policy version. "
                    "Until then a manager can publish manually, or run an exercise.",
                )
            )
    check = ranking_publication.verify(archive_dir, reg)
    latest = check["latest"]
    problems = list(check["problems"])
    due = bool(latest is None or latest < today)
    next_start: str | None = today
    if not due:
        last = datetime.date.fromisoformat(latest)
        if last == datetime.date.max:
            next_start = None
            problems.append("The latest publication date has no representable next window.")
        else:
            next_start = (last + datetime.timedelta(days=1)).isoformat()
    out.update(
        count=check["count"],
        problems=problems,
        latest=latest,
        due=due,
        next_window_start=next_start,
    )
    if problems and operation == "publish" and not exercise:
        refusals.append(
            _refusal(
                "archive_unverified",
                f"{len(problems)} archived record(s) do not verify.",
                "Run verify, repair the archive by hand, then rerun. Nothing is overwritten.",
            )
        )

    if operation == "schedule":
        out["status"] = (
            "problem"
            if problems
            else "blocked"
            if refusals
            else ("due" if out["due"] else "current")
        )
        return out

    snap_date = as_of
    if cases is None:
        refusals.append(
            _refusal(
                "source_missing",
                "No case source was supplied.",
                "Supply an explicit case file; no default data is read.",
            )
        )
    elif not _date(snap_date):
        refusals.append(
            _refusal(
                "source_missing",
                "The case source has no ISO as_of date.",
                "Supply as_of with the case data.",
            )
        )
    elif snap_date is not None and snap_date > today:
        refusals.append(
            _refusal(
                "source_future",
                f"The case data is dated {snap_date}, after the run date {today}.",
                "Check the case file and the run date, then rerun.",
            )
        )
    if refusals or policy is None or cases is None or snap_date is None:
        return out
    try:
        snap = ranking.snapshot(list(cases), policy, snap_date)
    except (KeyError, TypeError, ValueError, AttributeError) as e:
        refusals.append(
            _refusal(
                "source_invalid",
                f"The case source cannot be ranked: {type(e).__name__}.",
                "Fix the case file and rerun.",
            )
        )
        return out
    out["run_key"] = hashlib.sha256(
        ranking.canonical(
            {"policy_hash": policy["content_hash"], "as_of": snap_date, "window": today}
        ).encode("utf-8")
    ).hexdigest()[:16]
    if snap_date != today:
        out["warnings"].append(
            _refusal(
                "source_not_current",
                f"The case data is dated {snap_date}, not the run date {today}.",
                "Refresh the case file; verify checks the publication date, not the data age.",
            )
        )
    out.update(
        snapshot_hash=snap["snapshot_hash"],
        as_of=snap_date,
        total=snap["total"],
        source_current=snap_date == today,
    )
    if exercise:
        out["status"] = "exercise"
        out["written"] = False
        return out
    need = len(
        ranking_publication._canonical({"published_on": today, "snapshot": snap}).encode("utf-8")
    )
    exists = os.path.exists(os.path.join(archive_dir, ranking_publication._name(snap)))
    if not exists and free_bytes(archive_dir) < need:
        refusals.append(
            _refusal(
                "capacity_missing",
                f"The archive location is not writable or has less than {need} bytes free.",
                "Free space or fix permissions, then rerun.",
            )
        )
        return out
    try:
        res = ranking_publication.publish(snap, archive_dir, today)
    except (ranking_publication.PublicationError, OSError) as e:
        refusals.append(_refusal("publish_failed", str(e), "Check the archive location and rerun."))
        return out
    out.update(path=res["path"], written=res["written"], published_on=res["published_on"])
    out["status"] = "published" if res["written"] else "already_published"
    return out


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Run ranking snapshot schedule, publish or verify locally."
    )
    ap.add_argument("operation", choices=["schedule", "publish", "verify"])
    ap.add_argument("--archive", required=True, help="archive folder; no default is used")
    ap.add_argument("--today", required=True, help="ISO date of the run window; no clock is read")
    ap.add_argument(
        "--cases", help="store-shaped JSON file with cases and as_of; required to publish"
    )
    ap.add_argument("--as-of", dest="as_of", help="override the case data's as_of date")
    ap.add_argument("--policy", help="policy version; default is the latest in the registry")
    ap.add_argument(
        "--exercise",
        action="store_true",
        help="compute only; allow an unsigned policy and write nothing",
    )
    a = ap.parse_args(argv)
    cases, as_of = None, a.as_of
    if a.cases and a.operation == "publish":
        try:
            cases, data_as_of = load_cases(a.cases)
            as_of = as_of or data_as_of
        except (OSError, ValueError, KeyError, TypeError) as e:
            print(
                f"Case file {a.cases} is unreadable or not store-shaped: {type(e).__name__}",
                file=sys.stderr,
            )
    res = run(
        a.operation,
        a.archive,
        a.today,
        cases=cases,
        as_of=as_of,
        policy_version=a.policy,
        exercise=a.exercise,
    )
    for w in res["warnings"]:
        print(f"Warning {w['code']}: {w['message']}", file=sys.stderr)
    print(json.dumps(res, sort_keys=True, indent=2))
    if res["status"] == "refused":
        return EXIT_REFUSED
    return EXIT_PROBLEM if res["status"] == "problem" else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
