"""Finite run control for the live synthetic simulator (issue 184, stage 2).

An admin-written JSON control document names the bounded demo cohort, an owner, an approval
reference and a hard expiry. The simulator and the receiver host both read it, so a stop or an
expiry takes effect at the next slot without a redeploy. Write access to the document is the admin
boundary (Azure RBAC on the file share); this module holds no secret and makes no network call.
"""

import argparse
import fcntl
import json
import os
import re
import sys
import tempfile
from collections.abc import Iterator, Sequence
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

from zava_forward.core.synthetic import sensor_identity
from zava_forward.core.synthetic.sensor_stream import StreamError

VERSION = "live-sim-control-v1"
MAX_COHORT = 100
MAX_WINDOW = timedelta(days=14)
STAMP = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ\Z")
PLACEHOLDERS = frozenset({"tbc", "tbd", "todo", "n/a", "na", "none", "unknown", "unassigned"})
FIELDS = frozenset({"version", "enabled", "expires_at", "approval_reference", "owner", "homes"})
SEND, STOPPED, EXPIRED, INVALID = "send", "stopped", "expired", "invalid"


def _stamp(value: object) -> datetime:
    if type(value) is not str or not STAMP.fullmatch(value):
        raise StreamError("CONTROL_INVALID")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except ValueError:
        raise StreamError("CONTROL_INVALID") from None


@dataclass(frozen=True)
class Control:
    enabled: bool
    expires_at: datetime
    approval_reference: str
    owner: str
    homes: tuple[str, ...]

    def as_document(self) -> dict[str, object]:
        return {
            "version": VERSION,
            "enabled": self.enabled,
            "expires_at": self.expires_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "approval_reference": self.approval_reference,
            "owner": self.owner,
            "homes": list(self.homes),
        }


def parse(document: object) -> Control:
    """Validate a decoded control document; every refusal is a fixed code."""
    if not isinstance(document, dict) or set(document) != FIELDS or document["version"] != VERSION:
        raise StreamError("CONTROL_INVALID")
    homes, enabled = document["homes"], document["enabled"]
    text = (document["approval_reference"], document["owner"])
    if (
        type(enabled) is not bool
        or any(
            type(v) is not str or not v.strip() or v.strip().lower() in PLACEHOLDERS for v in text
        )
        or type(homes) is not list
        or not 1 <= len(homes) <= MAX_COHORT
        or not all(type(h) is str and sensor_identity.home_key(h) for h in homes)
        or len(set(homes)) != len(homes)
    ):
        raise StreamError("CONTROL_INVALID")
    return Control(
        enabled, _stamp(document["expires_at"]), text[0].strip(), text[1].strip(), tuple(homes)
    )


def load(path: Path) -> Control:
    try:
        return parse(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        raise StreamError("CONTROL_UNAVAILABLE") from None


def decide(control: Control, now: datetime) -> str:
    """Only SEND allows work; an expiry beyond the 14-day maximum is INVALID for every reader."""
    if now >= control.expires_at:
        return EXPIRED
    if control.expires_at > now + MAX_WINDOW:
        return INVALID
    return SEND if control.enabled else STOPPED


def check_window(control: Control, now: datetime) -> None:
    """A start must be finite: in the future and at most 14 days away."""
    if not now < control.expires_at <= now + MAX_WINDOW:
        raise StreamError("CONTROL_WINDOW_INVALID")


@contextmanager
def locked(path: Path) -> Iterator[None]:
    """Hold an exclusive advisory lock on a sidecar file so writers cannot interleave.

    Readers never lock (a replace is atomic). A held lock refuses with CONTROL_BUSY.
    """
    try:
        handle = os.open(path.with_name(path.name + ".lock"), os.O_CREAT | os.O_RDWR, 0o600)
    except OSError:
        raise StreamError("CONTROL_UNAVAILABLE") from None
    try:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise StreamError("CONTROL_BUSY") from None
        yield
    finally:
        os.close(handle)


def write(path: Path, control: Control) -> None:
    """Replace the document atomically so a reader never sees a partial file."""
    handle, temporary = tempfile.mkstemp(dir=path.parent, prefix=".control-")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(control.as_document(), stream, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def main(argv: Sequence[str] | None = None, now: datetime | None = None) -> int:
    parser = argparse.ArgumentParser(prog="zava_forward.api.live_control", description=__doc__)
    parser.add_argument("action", choices=("start", "stop", "status"))
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument(
        "--expires-at", help="start: UTC YYYY-MM-DDTHH:MM:SSZ, at most 14 days away"
    )
    parser.add_argument("--approval")
    parser.add_argument("--owner")
    parser.add_argument("--homes", help="start: comma separated home ids, at most 100")
    args = parser.parse_args(list(argv) if argv is not None else None)
    moment = now or datetime.now(UTC)
    try:
        with locked(args.file) if args.action != "status" else nullcontext():
            if args.action == "start":
                control = parse(
                    {
                        "version": VERSION,
                        "enabled": True,
                        "expires_at": args.expires_at,
                        "approval_reference": args.approval,
                        "owner": args.owner,
                        "homes": [h for h in (args.homes or "").split(",") if h],
                    }
                )
                check_window(control, moment)
            else:
                current = load(args.file)
                control = Control(
                    False if args.action == "stop" else current.enabled,
                    current.expires_at,
                    current.approval_reference,
                    current.owner,
                    current.homes,
                )
            if args.action != "status":
                write(args.file, control)
    except (StreamError, OSError) as error:
        print(f"Cannot continue: {error}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            control.as_document()
            | {"state": decide(control, moment), "cohort_size": len(control.homes)},
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
