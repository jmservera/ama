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
import contextlib
import errno
import hashlib
import json
import os
import re
import stat
from collections.abc import Mapping
from typing import Any

from . import ranking
from . import ranking_archive_blob as rab

SCHEDULE: dict[str, Any] = {
    "cadence": "daily",
    "minimum_frequency_hours": 24,
    "runner": "deployment scheduler (not yet configured)",
    "owner": "to be named",
    "retention": "not set; archive keeps every snapshot until a named owner approves a purge",
}

_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DIR_FD_OK = {os.open, os.link, os.unlink, os.stat} <= os.supports_dir_fd
_PUBLISHED_ON = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
Path = str | os.PathLike[str]
Archive = Path | rab.BlobRankingArchive


class PublicationError(Exception):
    """A snapshot cannot be published, or an archived record does not verify."""


class ArchiveStorageError(Exception):
    """The archive location cannot take a record (for example no hard-link support)."""


class DurabilityUnconfirmedError(OSError):
    """The record is at its final name but the archive folder or a parent folder sync failed.

    The record stays; whether the name survives a crash is unknown, so this is
    neither a confirmed publication nor a rollback. written is True when this call
    created the record, False for an existing record or a lost race, and None when
    the caller does not know.
    """

    def __init__(
        self, path: str, published_on: str, cause: OSError, written: bool | None = None
    ) -> None:
        super().__init__(
            cause.errno,
            f"{os.path.basename(path)} was written but the archive folder or a parent "
            f"folder could not be synced ({type(cause).__name__}); durability is unconfirmed.",
        )
        self.path = path
        self.published_on = published_on
        self.written = written


class ArchiveWriteUncertainError(DurabilityUnconfirmedError):
    """A Blob create was sent and its outcome is unknown: the record may or may not exist.

    Nothing is rolled back and nothing is claimed as written (written is None). Retrying the
    same snapshot confirms the record: it is created or reported as already published.
    """

    def __init__(self, path: str, published_on: str) -> None:
        OSError.__init__(
            self,
            errno.EIO,
            f"{path} may or may not be stored; the write outcome is unconfirmed and nothing "
            "was rolled back. Retry the same publication to confirm.",
        )
        self.path = path
        self.published_on = published_on
        self.written = None


class _MetadataMismatch(ValueError):
    """A Blob record does not match its stored verification metadata."""


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


def _existing(
    held: int, name: str, path: str, snap: Mapping[str, Any]
) -> tuple[dict[str, Any], int]:
    try:
        with open(os.open(name, os.O_RDONLY, dir_fd=held), encoding="utf-8") as f:
            ino = os.fstat(f.fileno()).st_ino
            rec = json.load(f)
        stored = rec["snapshot"]
        published_on = rec["published_on"]
        ok = (
            _canonical(stored) == _canonical(snap)
            and snapshot_hash(stored) == stored["snapshot_hash"]
            and name == _name(stored)
            and _valid_date(published_on)
        )
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        raise PublicationError(
            f"{name} exists but cannot be read as this snapshot "
            f"({type(e).__name__}); not overwritten. A named owner must review the archive."
        ) from e
    if not ok:
        raise PublicationError(
            f"{name} exists but does not match this snapshot, its hash, "
            "its name or a valid publication date; not overwritten. "
            "A named owner must review the archive."
        )
    return {"path": path, "written": False, "published_on": published_on}, ino


def _mount_id(fd: int) -> int:
    with open(f"/proc/self/fdinfo/{fd}", encoding="utf-8") as f:
        return _parse_mount_id(f.read())


def _parse_mount_id(text: str) -> int:
    for line in text.splitlines():
        key, _, value = line.partition(":")
        if key == "mnt_id":
            try:
                return int(value.strip())
            except ValueError:
                break
    raise OSError(errno.EIO, "The mount identity of a folder could not be read.")


def _close(fds: list[int]) -> None:
    for fd in fds:
        with contextlib.suppress(OSError):
            os.close(fd)


def _walk(held: int) -> tuple[list[int], list[tuple[int, int, int]]]:
    """Open the parent folders of a held folder, nearest first, to its mount boundary.

    The walk follows the kernel's parent link from the descriptor, so it names the folders
    that actually hold the entries and not whatever a path resolves to later. It ends at
    the filesystem root or just before the first parent on another mount; the last
    folder on the mount is included because its entries are on the archive's mount. The
    mount id is per open descriptor, so a bind mount (same device) is a boundary and a
    Btrfs subvolume root (different device, same mount) is not. Returns the open
    descriptors and the (device, inode, mount id) of the held folder and each parent.
    Any open or read error is raised.
    """
    opened: list[int] = []
    try:
        child = os.fstat(held)
        mount = _mount_id(held)
        identities = [(child.st_dev, child.st_ino, mount)]
        current = held
        while True:
            parent = os.open("..", os.O_RDONLY | os.O_DIRECTORY, dir_fd=current)
            opened.append(parent)
            st = os.fstat(parent)
            if os.path.samestat(st, child) or _mount_id(parent) != mount:
                _close([opened.pop()])
                return opened, identities
            identities.append((st.st_dev, st.st_ino, mount))
            current, child = parent, st
    except BaseException:
        _close(opened)
        raise


def _same_folder(archive_dir: Path, held: int, name: str, ino: int) -> None:
    """The archive path still names the held folder and the committed name still holds the
    record that was written or validated."""
    if not os.path.samestat(os.stat(archive_dir), os.fstat(held)):
        raise OSError(errno.ESTALE, "The archive folder changed during publication.")
    if os.stat(name, dir_fd=held).st_ino != ino:
        raise OSError(errno.ESTALE, "The record changed during confirmation.")


def publish(snap: Mapping[str, Any], archive_dir: Archive, published_on: str) -> dict[str, Any]:
    """Archive a snapshot. A BlobRankingArchive takes a single conditional create (see
    _publish_blob); the rest of this docstring describes the local folder adapter.
    published_on is an ISO date supplied by the caller.

    Returns path, written (False when the identical snapshot was already archived)
    and the original published_on. The archive folder is opened once and the stage, link,
    existing-record read and removal all go through that open folder, so the folder that
    receives the record is the folder that is synced. The record is written to a unique
    stage file, synced and linked to its final name, so the first writer wins and nothing
    is overwritten; the stage is removed and the folder and every parent folder (up to
    the archive's mount boundary or the root) are synced before the result is returned,
    including for an existing record, which is validated and refused when it is damaged.
    The confirmation also checks that the path still names that folder, the record is
    unchanged and the parent folders and their mounts are the same before and after the
    syncs. A failed sync or check is raised as DurabilityUnconfirmedError (an OSError
    carrying the cause's errno) although the record is committed and kept; a retry
    syncs again and reports the record as already published once the sync succeeds. A
    platform without descriptor-relative calls refuses before anything is written. A
    folder moved or remounted and put back inside one confirmation is not detected.
    """
    if not _valid_date(published_on):
        raise PublicationError("published_on must be an ISO date, YYYY-MM-DD.")
    if not _DATE.match(str(snap.get("as_of"))) or snapshot_hash(snap) != snap.get("snapshot_hash"):
        raise PublicationError("Snapshot is incomplete or does not match its hash; refused.")
    if isinstance(archive_dir, rab.BlobRankingArchive):
        return _publish_blob(snap, archive_dir, published_on)
    if not _DIR_FD_OK:
        raise OSError(errno.ENOSYS, "This platform cannot publish through an open folder.")
    os.makedirs(archive_dir, exist_ok=True)
    held = os.open(archive_dir, os.O_RDONLY | os.O_DIRECTORY)
    try:
        return _publish_held(snap, archive_dir, published_on, held)
    finally:
        os.close(held)


def _blob_record(raw: bytes, meta: Mapping[str, str]) -> dict[str, Any]:
    rec = json.loads(raw)
    expected = rab.metadata_for(rec["snapshot"], rec["published_on"], raw)
    if any(meta.get(k) != v for k, v in expected.items()):
        raise _MetadataMismatch("metadata does not match the record")
    return dict(rec)


def _publish_blob(
    snap: Mapping[str, Any], archive: rab.BlobRankingArchive, published_on: str
) -> dict[str, Any]:
    """One conditional create. The create-only request is the idempotence and concurrency check:
    the first writer wins and a repeat or a loser reads back and validates the existing record.
    An unknown outcome after the request was sent is raised as ArchiveWriteUncertainError and
    never as a success or a rollback. The returned path is the opaque record name."""
    name = _name(snap)
    raw = _canonical({"published_on": published_on, "snapshot": snap}).encode("utf-8")
    uncertain = False
    try:
        created = archive.create(name, raw, rab.metadata_for(snap, published_on, raw))
    except rab.BlobArchiveUncertain:
        uncertain = True
    if uncertain:
        raise ArchiveWriteUncertainError(name, published_on)
    if created:
        return {"path": name, "written": True, "published_on": published_on}
    stored, meta = archive.read(name)
    try:
        rec = _blob_record(stored, meta)
        stored_snap = rec["snapshot"]
        published = rec["published_on"]
        ok = (
            _canonical(stored_snap) == _canonical(snap)
            and snapshot_hash(stored_snap) == stored_snap["snapshot_hash"]
            and name == _name(stored_snap)
            and _valid_date(published)
        )
    except (ValueError, KeyError, TypeError, AttributeError) as e:
        raise PublicationError(
            f"{name} exists but cannot be read as this snapshot "
            f"({type(e).__name__}); not overwritten. A named owner must review the archive."
        ) from None
    if not ok:
        raise PublicationError(
            f"{name} exists but does not match this snapshot, its hash, "
            "its name or a valid publication date; not overwritten. "
            "A named owner must review the archive."
        )
    return {"path": name, "written": False, "published_on": published}


def _publish_held(
    snap: Mapping[str, Any], archive_dir: Path, published_on: str, held: int
) -> dict[str, Any]:
    name = _name(snap)
    path = os.path.join(archive_dir, name)
    try:
        os.stat(name, dir_fd=held, follow_symlinks=False)
    except FileNotFoundError:
        pass
    else:
        return _confirmed(*_existing(held, name, path, snap), archive_dir, held)
    text = _canonical({"published_on": published_on, "snapshot": snap})
    stage = f".{name}.{os.urandom(8).hex()}.tmp"
    # Owner-only, like the earlier mkstemp stage: the linked record keeps this mode.
    fd = os.open(stage, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600, dir_fd=held)
    try:
        with open(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
            ino = os.fstat(f.fileno()).st_ino
        try:
            os.link(stage, name, src_dir_fd=held, dst_dir_fd=held)
            outcome = {"path": path, "written": True, "published_on": published_on}
        except FileExistsError:
            outcome, ino = _existing(held, name, path, snap)
    except BaseException as e:
        if _remove(stage, held):
            e.stage_retained = stage  # type: ignore[attr-defined]
            e.add_note(f"Staging file {stage} could not be removed.")
        raise
    if _remove(stage, held):
        outcome["stage_retained"] = stage
    return _confirmed(outcome, ino, archive_dir, held)


def _confirmed(outcome: dict[str, Any], ino: int, archive_dir: Path, held: int) -> dict[str, Any]:
    """Sync the archive folder and its parent folders so the committed name and any newly
    created folder entries are durable before the caller is told. Parents are synced on
    every confirmation, including a retry, so a failed earlier sync is never reported as
    already published. The folder, record and parent identities are checked before and
    after, and any difference is reported as unconfirmed."""
    name = os.path.basename(outcome["path"])
    opened: list[int] = []
    try:
        _same_folder(archive_dir, held, name, ino)
        opened, before = _walk(held)
        os.fsync(held)
        for parent in opened:
            os.fsync(parent)
        again, after = _walk(held)
        _close(again)
        if after != before:
            raise OSError(errno.ESTALE, "The parent folders changed during confirmation.")
        _same_folder(archive_dir, held, name, ino)
    except OSError as e:
        error = DurabilityUnconfirmedError(
            outcome["path"], outcome["published_on"], e, outcome["written"]
        )
        if "stage_retained" in outcome:
            error.stage_retained = outcome["stage_retained"]  # type: ignore[attr-defined]
        raise error from e
    finally:
        _close(opened)
    return outcome


def _remove(stage: str, held: int) -> bool:
    """Remove this call's own staging file. True when it could not be removed and remains."""
    try:
        os.unlink(stage, dir_fd=held)
    except FileNotFoundError:
        return False
    except OSError:
        return True
    return False


def _require_creatable(path: str) -> None:
    """Return when path is missing and its nearest existing ancestor is a real folder.

    Raises a path-free OSError for a dangling link, a non-folder or a stat failure, so an
    unusable archive location is never mistaken for an empty one.
    """
    while True:
        try:
            os.lstat(path)
        except FileNotFoundError:
            parent = os.path.dirname(path)
            if parent == path:
                return
            path = parent
            continue
        try:
            usable = stat.S_ISDIR(os.stat(path).st_mode)
        except FileNotFoundError:
            raise OSError(
                errno.ENOENT, "A symbolic link in the archive location is dangling"
            ) from None
        if not usable:
            raise NotADirectoryError(
                errno.ENOTDIR, "A parent of the archive location is not a folder"
            )
        return


def _names(archive_dir: Path) -> list[str]:
    path = os.fspath(archive_dir)
    try:
        usable = stat.S_ISDIR(os.stat(path).st_mode)
    except FileNotFoundError:
        _require_creatable(path)
        return []
    if not usable:
        raise NotADirectoryError(errno.ENOTDIR, "The archive location is not a folder")
    names = os.listdir(archive_dir)
    return sorted(n for n in names if n.startswith("ranking-") and n.endswith(".json"))


def verify(archive_dir: Archive, registry: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Check every archived record. Returns count, problems and latest publication date.

    For a Blob archive each record is also checked against its stored metadata, and a listing
    that cannot be read raises OSError instead of reporting an empty archive. For a local folder
    (fixture support only) an absent folder is empty (first run), while an existing non-folder, a
    dangling link or a stat failure raises a path-free OSError and is never reported as empty.
    """
    reg = ranking.POLICIES if registry is None else registry
    problems: list[str] = []
    dates: list[str] = []
    names = (
        archive_dir.names()
        if isinstance(archive_dir, rab.BlobRankingArchive)
        else _names(archive_dir)
    )
    for n in names:
        try:
            if isinstance(archive_dir, rab.BlobRankingArchive):
                rec = _blob_record(*archive_dir.read(n))
            else:
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
        except _MetadataMismatch:
            problems.append(f"{n}: stored metadata does not match the record.")
        except (OSError, ValueError, KeyError, TypeError):
            problems.append(f"{n}: unreadable or incomplete.")
    return {"count": len(names), "problems": problems, "latest": max(dates) if dates else None}


def overdue(archive_dir: Archive, today: str) -> bool:
    """True when nothing is published or the latest is before today (supplied by the caller)."""
    latest = verify(archive_dir)["latest"]
    return latest is None or bool(latest < today)
