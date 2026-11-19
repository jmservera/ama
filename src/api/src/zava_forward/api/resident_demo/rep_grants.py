"""Load synthetic task-limited representative grants for the resident showcase.

The file is local, synthetic and secret-free. Every grant needs a recorded expiry, which the
evaluator in core/resident_showcase.py enforces at request time. Any defect fails closed
without echoing a value.
"""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from zava_forward.core import resident_showcase as rs

MAX_BYTES = 64 * 1024
MAX_GRANTS = 20
REQUIRED = frozenset(
    {"case_id", "email", "representative_ref", "measure", "tasks", "valid_from", "expires_at"}
)
ALLOWED = REQUIRED | {"revoked"}


def _utc(value: Any, name: str) -> datetime:
    try:
        moment = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        raise rs.ShowcaseConfigError(f"Representative grant {name} is not an ISO time.") from None
    offset = moment.utcoffset()
    if offset is None or offset.total_seconds() != 0:
        raise rs.ShowcaseConfigError(f"Representative grant {name} must be an explicit UTC time.")
    return moment.astimezone(UTC)


def _grant(item: Any) -> rs.RepresentativeShowcaseGrant:
    if not isinstance(item, dict) or set(item) - ALLOWED or REQUIRED - set(item):
        raise rs.ShowcaseConfigError("Representative grant has missing or unknown fields.")
    tasks = item["tasks"]
    if not isinstance(tasks, list) or not all(isinstance(t, str) for t in tasks):
        raise rs.ShowcaseConfigError("Representative grant tasks must be a list of names.")
    revoked = item.get("revoked", False)
    if not isinstance(revoked, bool):
        raise rs.ShowcaseConfigError("Representative grant revoked must be true or false.")
    for key in ("case_id", "email", "representative_ref", "measure"):
        if not isinstance(item[key], str):
            raise rs.ShowcaseConfigError(f"Representative grant {key} must be text.")
    valid_from, expires_at = (
        _utc(item["valid_from"], "valid_from"),
        _utc(item["expires_at"], "expires_at"),
    )
    if expires_at <= valid_from or expires_at > rs.AUTHORITY_END:
        raise rs.ShowcaseConfigError("Representative grant expiry is outside its window.")
    grant = rs.RepresentativeShowcaseGrant(
        case_id=item["case_id"],
        email=item["email"],
        representative_ref=item["representative_ref"],
        measure=item["measure"],
        tasks=tuple(tasks),
        valid_from=valid_from,
        expires_at=expires_at,
        revoked=revoked,
    )
    try:
        rs.admit_representative_grant(grant)
    except rs.ShowcaseDenied:
        raise rs.ShowcaseConfigError("Representative grant failed admission.") from None
    return grant


def load_grants(path_text: str | None) -> tuple[rs.RepresentativeShowcaseGrant, ...]:
    """Return the grants in the named file, or none when no file is configured."""
    if not path_text:
        return ()
    path = Path(path_text)
    if not path.is_absolute() or path.is_symlink() or not path.is_file():
        raise rs.ShowcaseConfigError("The representative grants file must be an absolute file.")
    if path.stat().st_size > MAX_BYTES:
        raise rs.ShowcaseConfigError("The representative grants file is too large.")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise rs.ShowcaseConfigError("The representative grants file is not valid JSON.") from None
    if not isinstance(data, list) or len(data) > MAX_GRANTS:
        raise rs.ShowcaseConfigError("The representative grants file must be a short list.")
    return tuple(_grant(item) for item in data)
