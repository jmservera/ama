"""Retained publication of ranking snapshots (PR-006, ADR 0002 decision 4, issue 79).

publish() writes one immutable, dated file per policy version, as_of date and
snapshot hash into an archive folder. The write is idempotent: the same snapshot
gives the same file and is not rewritten, and an archived record is never
overwritten or deleted here. Each writer stages its content in its own uniquely
named file in the same folder and links it to the record name, which fails if the
record exists, so concurrent writers of one snapshot keep exactly one record and
the loser reports it. That needs a local filesystem with hard links; a folder
without them refuses to publish (OSError) and nothing is overwritten. The only
file removed is the staging file this call created; if that removal fails after the
record is committed, the result still reports the record and names the retained stage
(stage_retained). A stage kept by the writer that committed the record shares its
bytes and inode, but a stage kept by a writer that lost the race was never linked and
can differ, so an operator checks it before removing it. verify()
re-hashes every archived snapshot so an edited or damaged record is reported. Nothing reads a
clock: the publication date is an input. Retention period and the scheduler are
not set here. The legal period is a Legal decision and the schedule is run by the
deployment; SCHEDULE states the contract the deployment is expected to meet.
Nothing here changes a ranking.
"""

import calendar
import hashlib
import json
import os
import re
from collections.abc import Mapping
from typing import Any

from . import ranking

SCHEDULE: dict[str, Any] = {
    "cadence": "daily",
    "minimum_frequency_hours": 24,
    "runner": "deployment scheduler (not yet configured)",
    "owner": "to be named",
    "retention": "not set; archive keeps every snapshot until a named owner approves a purge",
}

_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_PUBLISHED_ON = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
Path = str | os.PathLike[str]


class PublicationError(Exception):
    """A snapshot cannot be published, or an archived record does not verify."""


class ArchiveStorageError(Exception):
    """The archive location cannot take a record (for example no hard-link support)."""


def _valid_date(value: Any) -> bool:
    if not isinstance(value, str) or not _PUBLISHED_ON.fullmatch(value):
        return False
    year, month, day = (int(part) for part in value.split("-"))
    return year >= 1 and 1 <= month <= 12 and 1 <= day <= calendar.monthrange(year, month)[1]


def _canonical(value: Mapping[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def snapshot_hash(snap: Mapping[str, Any]) -> str:
    body = {k: v for k, v in snap.items() if k != "snapshot_hash"}
    return hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()


def _name(snap: Mapping[str, Any]) -> str:
    version, as_of, digest = snap["policy_version"], snap["as_of"], snap["snapshot_hash"][:12]
    return f"ranking-{version}-{as_of}-{digest}.json"


def _existing(path: str, snap: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the record already at the final name against the snapshot being published."""
    try:
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
        held = rec["snapshot"]
        published_on = rec["published_on"]
        ok = (
            _canonical(held) == _canonical(snap)
            and snapshot_hash(held) == held["snapshot_hash"]
            and os.path.basename(path) == _name(held)
            and _valid_date(published_on)
        )
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        raise PublicationError(
            f"{os.path.basename(path)} exists but cannot be read as this snapshot "
            f"({type(e).__name__}); not overwritten. A named owner must review the archive."
        ) from e
    if not ok:
        raise PublicationError(
            f"{os.path.basename(path)} exists but does not match this snapshot, its hash, "
            "its name or a valid publication date; not overwritten. "
            "A named owner must review the archive."
        )
    return {"path": path, "written": False, "published_on": published_on}


def _fsync_dir(archive_dir: Path) -> None:
    fd = os.open(archive_dir, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def publish(snap: Mapping[str, Any], archive_dir: Path, published_on: str) -> dict[str, Any]:
    """Archive a snapshot. published_on is an ISO date supplied by the caller.

    Returns path, written (False when the identical snapshot was already archived)
    and the original published_on. The record is written to a unique stage file, synced
    and linked to its final name, so the first writer wins and nothing is overwritten;
    the stage is removed and the folder synced before the result is returned, including
    for an existing record, which is validated and refused when it is damaged. A failed
    folder sync is raised as OSError although the record may already be committed; a
    retry then reports it as already published.
    """
    if not _valid_date(published_on):
        raise PublicationError("published_on must be an ISO date, YYYY-MM-DD.")
    if not _DATE.match(str(snap.get("as_of"))) or snapshot_hash(snap) != snap.get("snapshot_hash"):
        raise PublicationError("Snapshot is incomplete or does not match its hash; refused.")
    os.makedirs(archive_dir, exist_ok=True)
    path = os.path.join(archive_dir, _name(snap))
    if os.path.lexists(path):
        return _confirmed(_existing(path, snap), archive_dir)
    text = _canonical({"published_on": published_on, "snapshot": snap})
    stage = os.path.join(archive_dir, f".{_name(snap)}.{os.urandom(8).hex()}.tmp")
    fd = os.open(stage, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o666)
    try:
        with open(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        try:
            os.link(stage, path)
            outcome = {"path": path, "written": True, "published_on": published_on}
        except FileExistsError:
            outcome = _existing(path, snap)
    except BaseException as e:
        if _remove(stage):
            e.add_note(f"Staging file {os.path.basename(stage)} could not be removed.")
        raise
    if _remove(stage):
        outcome["stage_retained"] = os.path.basename(stage)
    return _confirmed(outcome, archive_dir)


def _confirmed(outcome: dict[str, Any], archive_dir: Path) -> dict[str, Any]:
    """Sync the archive folder so the committed name is durable before the caller is told."""
    _fsync_dir(archive_dir)
    return outcome


def _remove(stage: str) -> bool:
    """Remove this call's own staging file. True when it could not be removed and remains."""
    try:
        os.unlink(stage)
    except FileNotFoundError:
        return False
    except OSError:
        return True
    return False


def _names(archive_dir: Path) -> list[str]:
    if not os.path.isdir(archive_dir):
        return []
    names = os.listdir(archive_dir)
    return sorted(n for n in names if n.startswith("ranking-") and n.endswith(".json"))


def verify(archive_dir: Path, registry: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Check every archived record. Returns count, problems and latest publication date."""
    reg = ranking.POLICIES if registry is None else registry
    problems: list[str] = []
    dates: list[str] = []
    names = _names(archive_dir)
    for n in names:
        try:
            with open(os.path.join(archive_dir, n), encoding="utf-8") as f:
                rec = json.load(f)
            snap = rec["snapshot"]
            known = reg.get(snap["policy_version"])
            if snapshot_hash(snap) != snap["snapshot_hash"]:
                problems.append(f"{n}: content does not match its snapshot hash.")
            elif n != _name(snap):
                problems.append(f"{n}: file name does not match its content.")
            elif known is None or known["content_hash"] != snap["policy_hash"]:
                problems.append(f"{n}: policy version or hash is not in the policy registry.")
            elif not _valid_date(rec["published_on"]):
                problems.append(f"{n}: publication date is not a valid calendar date.")
            else:
                dates.append(rec["published_on"])
        except (OSError, ValueError, KeyError, TypeError):
            problems.append(f"{n}: unreadable or incomplete.")
    return {"count": len(names), "problems": problems, "latest": max(dates) if dates else None}


def overdue(archive_dir: Path, today: str) -> bool:
    """True when nothing is published or the latest is before today (supplied by the caller)."""
    latest = verify(archive_dir)["latest"]
    return latest is None or bool(latest < today)
