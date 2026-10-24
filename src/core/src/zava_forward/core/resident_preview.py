"""Read-only synthetic resident preview boundary: default-deny grants and a positive-allowlist view.

This is development feedback tooling over synthetic data. It is not a live resident service,
does not approve any resident-portal design and adds no write path. The staff payloads and
`projection.py` are never reused: the resident view is built field by field from named,
mapped values so that a new staff field stays hidden until it is deliberately added here.
"""

import json
import shutil
import tempfile
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from . import resident_decisions as _resident_decisions
from .data_paths import data_file
from .insights import STAGE_ORDER

_domain: Any = _resident_decisions

BANNER = "Synthetic preview - not a live resident service"
FIELD_CATALOG = ("home", "measures", "progress", "next_step", "appointments", "help")
KINDS = ("resident", "representative")
TASKS = ("Receive information", "Communicate", "Attend", "Works decision")
TASK_FIELDS = {
    "Receive information": ("measures", "progress", "next_step"),
    "Attend": ("appointments",),
}
LOOPBACK_HOSTS = ("127.0.0.1", "::1")
FORBIDDEN_ENV_PREFIXES = (
    "ZF_",
    "AI_",
    "IDENTITY_",
    "MSI_",
    "AZURE_",
    "MSSQL",
    "APPLICATIONINSIGHTS",
    "OPENAI",
    "SQL",
)
GRANT_KEYS = {
    "grant_id",
    "subject",
    "case_id",
    "kind",
    "fields",
    "actions",
    "valid_from",
    "valid_to",
    "revoked",
}
REPRESENTATIVE_KEYS = {"representative_ref", "tasks", "measure"}
APPOINTMENT_PERIODS = ("Morning", "Afternoon", "Evening", "All day")

UNKNOWN_PROGRESS = "We do not have a plain-language update for this step yet."
UNKNOWN_NEXT = "We cannot say what happens next. Please use the help route below."
STAGE_TEXT = {
    "Home identified": (
        "Your home has been identified for the programme.",
        "We will contact you to talk about what could be done.",
    ),
    "Checking lease": (
        "We are checking the tenure and lease details for your home.",
        "We will tell you if we need anything from you.",
    ),
    "Rescheduled": (
        "A step has been moved to a new time.",
        "We will tell you the new arrangements when they are confirmed.",
    ),
    "Contacting resident": (
        "We are getting in touch with you.",
        "We will agree with you how and when to talk.",
    ),
    "Contact paused": (
        "Contact is paused.",
        "We will not contact you until the pause is lifted. You can ask for help below.",
    ),
    "Survey being booked": (
        "We are arranging a survey of your home.",
        "We will offer you a time. Nothing is booked until it is confirmed.",
    ),
    "Survey booked": (
        "A survey of your home is booked.",
        "Check the confirmed arrangements below.",
    ),
    "Survey write-up": (
        "The survey has happened and is being written up.",
        "We will share what we can once it is ready.",
    ),
    "Design starting": (
        "Design work is about to begin.",
        "We will tell you when there is something to look at.",
    ),
    "Design in progress": (
        "Design work is under way.",
        "We will tell you when there is something to look at.",
    ),
    "Design awaiting approval": (
        "The design is waiting for checks.",
        "We will tell you what the checks decide.",
    ),
    "Design being corrected": (
        "The design is being corrected after checks.",
        "We will tell you when the corrected design is ready.",
    ),
    "Waiting on other works": (
        "Other works need to finish before yours can continue.",
        "We will tell you when that changes.",
    ),
    "Waiting for resident decision": (
        "We are waiting for your decision.",
        "Please speak to your housing officer. This preview cannot record decisions.",
    ),
    "Resident paused works": (
        "Works are paused.",
        "Nothing will go ahead until a person has spoken to you.",
    ),
    "Funding check": (
        "We are checking the funding for the works.",
        "We will tell you if this affects you.",
    ),
    "Final checks before ordering": (
        "Final checks are being done before anything is ordered.",
        "We will tell you when they are complete.",
    ),
    "Waiting for block programme": (
        "Your works are waiting for a wider programme.",
        "We will tell you when a date is known.",
    ),
    "With contractor": (
        "The works have been passed to the contractor.",
        "We will share any confirmed visit below.",
    ),
    "Install booked": (
        "Installation is recorded as booked.",
        "Check the confirmed arrangements below.",
    ),
    "Works under way": (
        "Works are under way.",
        "Your contractor and housing officer can answer questions.",
    ),
    "Handover to arrange": ("The works are nearly done.", "We will arrange the handover with you."),
    "Quality check": ("The finished works are being checked.", "We will tell you the outcome."),
    "Closing down": (
        "The case is being finished off.",
        "We will tell you if anything else is needed.",
    ),
    "Aftercare issue": (
        "An aftercare issue is being looked at.",
        "We will tell you what happens next.",
    ),
}
UNAVAILABLE = (
    ("Messages", "Messaging is not available in this preview."),
    ("Uploads", "Uploading documents is not available in this preview."),
    ("Downloads", "Downloading documents is not available in this preview."),
    ("Replying to an appointment", "You cannot accept or change an appointment here."),
    ("Consent and decisions", "You cannot give or change consent here."),
    ("Automated answers", "AI answers are not available in this preview."),
)
HELP = {
    "summary": "A person can help. You do not need to use this page.",
    "routes": [
        "Speak to your housing officer.",
        "Write to or visit your local Zava North Homes office.",
        "Ask someone you trust to contact us for you, if you want to.",
    ],
    "note": "This preview shows no phone numbers or addresses and promises no response times.",
}


class GrantDenied(Exception):
    """Access denied by default. `code` is for tests and logs; `str` is safe for the resident."""

    def __init__(self, code: str):
        super().__init__("You cannot see this page.")
        self.code = code


class PreviewConfigError(Exception):
    """Unsafe or incomplete start-up configuration."""


@dataclass(frozen=True)
class Grant:
    grant_id: str
    subject: str
    case_id: str
    kind: str
    fields: tuple[str, ...]
    valid_from: datetime
    valid_to: datetime
    representative_ref: str = ""
    tasks: tuple[str, ...] = ()
    measure: str = ""


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value.strip() != "*"


def _when(value: Any) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.utcoffset() is None:
        raise ValueError("naive")
    return parsed


def _parse(record: Any) -> tuple[Grant, bool]:
    """Strictly parse one grant; any deviation is malformed. Returns grant and revoked flag."""
    if not isinstance(record, dict):
        raise ValueError("record")
    kind = record.get("kind")
    expected = GRANT_KEYS | (REPRESENTATIVE_KEYS if kind == "representative" else set())
    if kind not in KINDS or set(record) != expected:
        raise ValueError("keys")
    if not all(_text(record[key]) for key in ("grant_id", "subject", "case_id")):
        raise ValueError("ids")
    fields = record["fields"]
    if (
        not isinstance(fields, list)
        or not fields
        or len(set(fields)) != len(fields)
        or any(f not in FIELD_CATALOG for f in fields)
    ):
        raise ValueError("fields")
    if record["actions"] != [] or type(record["revoked"]) is not bool:
        raise ValueError("actions")
    start, end = _when(record["valid_from"]), _when(record["valid_to"])
    if end <= start:
        raise ValueError("window")
    extra: dict[str, Any] = {}
    if kind == "representative":
        tasks = record["tasks"]
        if (
            not isinstance(tasks, list)
            or not tasks
            or len(set(tasks)) != len(tasks)
            or any(t not in TASKS for t in tasks)
            or not _text(record["representative_ref"])
            or not _text(record["measure"])
        ):
            raise ValueError("representative")
        extra = dict(
            representative_ref=record["representative_ref"],
            tasks=tuple(tasks),
            measure=record["measure"],
        )
    grant = Grant(
        record["grant_id"],
        record["subject"],
        record["case_id"],
        kind,
        tuple(fields),
        start,
        end,
        **extra,
    )
    return grant, record["revoked"]


def _load_fixture(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise GrantDenied("fixture_unavailable") from None
    fixture = data.get("fixture") if isinstance(data, dict) else None
    if (
        not isinstance(fixture, dict)
        or fixture.get("synthetic") is not True
        or fixture.get("disposable") is not True
        or not isinstance(data.get("subjects"), list)
        or not isinstance(data.get("grants"), list)
    ):
        raise GrantDenied("fixture_unavailable")
    return data  # type: ignore[no-any-return]


def resolve_grant(fixture_path: Path, subject: str, now: datetime | None = None) -> Grant:
    """Re-read the server-owned fixture and return the one current grant, else deny by default."""
    now = now or datetime.now(UTC)
    data = _load_fixture(fixture_path)
    known = {s.get("subject") for s in data["subjects"] if isinstance(s, dict)}
    if not _text(subject) or subject not in known:
        raise GrantDenied("unknown_subject")
    mine = [g for g in data["grants"] if isinstance(g, dict) and g.get("subject") == subject]
    if not mine:
        raise GrantDenied("no_grant")
    parsed: list[tuple[Grant, bool]] = []
    for record in mine:
        try:
            parsed.append(_parse(record))
        except (ValueError, TypeError):
            raise GrantDenied("malformed") from None
    current = [g for g, revoked in parsed if not revoked and g.valid_from <= now < g.valid_to]
    if len(current) > 1:
        raise GrantDenied("ambiguous")
    if current:
        return current[0]
    if any(revoked for _, revoked in parsed):
        raise GrantDenied("revoked")
    raise GrantDenied("expired")


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _bounded(value: Any, limit: int = 120) -> str:
    return value.strip()[:limit] if isinstance(value, str) else ""


def _stage(case: dict[str, Any]) -> tuple[str, str]:
    stage = case.get("stage")
    if isinstance(stage, str) and stage in STAGE_ORDER and stage in STAGE_TEXT:
        return STAGE_TEXT[stage]
    return UNKNOWN_PROGRESS, UNKNOWN_NEXT


def _authority_current(case: dict[str, Any], grant: Grant, task: str) -> bool:
    """Reuse the domain representative check; anything unexpected means not confirmed."""
    try:
        context = _domain.current_context(case, grant.measure)
        if not isinstance(context, dict) or type(context.get("revision")) is not int:
            return False
        versions = case.get("representative_authorities", {}).get(grant.representative_ref)
        if not isinstance(versions, list) or not versions or not isinstance(versions[-1], dict):
            return False
        _domain.authority_for(case, grant.representative_ref, task, grant.measure, context)
        return True
    except (ValueError, KeyError, TypeError, AttributeError):
        return False


def _work_orders(store: Any, case_id: str) -> list[dict[str, Any]]:
    procurement = store.data.get("procurement")
    orders = procurement.get("work_orders") if isinstance(procurement, dict) else None
    if not isinstance(orders, list):
        return []
    return [w for w in orders if isinstance(w, dict) and w.get("case_id") == case_id]


def _measure_bound(order: dict[str, Any], measure: str) -> bool:
    try:
        bindings = order["versions"][-1].get("resident_bindings") or []
        return any(isinstance(b, dict) and b.get("measure") == measure for b in bindings)
    except (KeyError, IndexError, TypeError, AttributeError):
        return False


def _appointments(store: Any, case_id: str, measure: str = "") -> dict[str, Any]:
    confirmed: list[dict[str, str]] = []
    offers: list[dict[str, str]] = []
    unknown = 0
    for order in _work_orders(store, case_id):
        if measure and not _measure_bound(order, measure):
            continue
        try:
            result = store.appointment_status(order)
            status = result.get("status")
            missing = [str(m) for m in result.get("missing") or []]
        except Exception:
            status, missing = "Unknown", []
        if status == "Offer" and not all(m.endswith(" confirmation missing") for m in missing):
            status = "Unknown"
        offer = _dict(order.get("appointment_offer"))
        entry: dict[str, str] = {}
        try:
            entry["date"] = date.fromisoformat(str(offer.get("date"))).isoformat()
        except (TypeError, ValueError):
            pass
        if offer.get("period") in APPOINTMENT_PERIODS:
            entry["period"] = offer["period"]
        if status == "Committed" and entry.get("date"):
            confirmed.append(entry)
        elif status == "Offer" and entry.get("date"):
            offers.append(entry)
        else:
            unknown += 1
    return dict(
        confirmed=dict(
            heading="Confirmed arrangements",
            note="These have been agreed and confirmed.",
            items=confirmed,
            empty="No confirmed arrangement is recorded.",
        ),
        offers=dict(
            heading="Offered times (not confirmed)",
            note="Offers only. Nothing is booked until it is under confirmed arrangements.",
            items=offers,
            empty="No offered time is recorded.",
        ),
        unknown=dict(
            count=unknown,
            note="We cannot show the state of some appointment records." if unknown else "",
        ),
    )


def resident_view(store: Any, grant: Grant) -> dict[str, Any]:
    """Build the response only from the grant's allowlisted fields. Never mutates the store."""
    case = store.cases.get(grant.case_id)
    if not isinstance(case, dict):
        raise GrantDenied("no_case")
    allowed = set(grant.fields)
    shown: set[str] = set()
    unavailable_tasks: list[str] = []
    measure = ""
    if grant.kind == "representative":
        for task in TASKS:
            if (
                task in grant.tasks
                and task in TASK_FIELDS
                and _authority_current(case, grant, task)
            ):
                shown |= set(TASK_FIELDS[task])
            else:
                unavailable_tasks.append(task)
        shown &= allowed
        if not shown:
            raise GrantDenied("no_current_authority")
        measure = grant.measure
    else:
        shown = allowed
    progress, next_step = _stage(case)
    out: dict[str, Any] = dict(
        banner=BANNER,
        viewer=dict(kind=grant.kind),
        read_only=True,
        unavailable=[dict(feature=f, reason=r) for f, r in UNAVAILABLE],
        help=HELP,
    )
    if grant.kind == "representative":
        out["authority_note"] = (
            "You are seeing information for the tasks a confirmed representative authority covers."
        )
        out["tasks_not_shown"] = [
            f"{task}: not shown, or not currently confirmed for this preview"
            for task in unavailable_tasks
        ]
    if "home" in shown and grant.kind == "resident":
        home = _dict(case.get("home"))
        out["home"] = {k: _bounded(home.get(k)) for k in ("address", "town", "postcode")}
    if "measures" in shown:
        items = _domain.case_measures(case)
        names = [_bounded(m) for m in items if isinstance(m, str)]
        out["measures"] = [m for m in names if not measure or m == measure][:20]
    if "progress" in shown:
        out["progress"] = progress
        if case.get("closed") is True:
            out["closed"] = "This case is recorded as closed."
    if "next_step" in shown:
        out["next_step"] = next_step
    if "appointments" in shown:
        out["appointments"] = _appointments(store, grant.case_id, measure)
    return out


def _real(path: str | Path, label: str) -> Path:
    raw = Path(path).expanduser()
    if raw.is_symlink():
        raise PreviewConfigError(f"The {label} path must not be a symbolic link.")
    try:
        resolved = raw.resolve(strict=True)
    except OSError:
        raise PreviewConfigError(
            f"The {label} file was not found. Build a synthetic fixture first."
        ) from None
    if not resolved.is_file():
        raise PreviewConfigError(f"The {label} path must be a regular file.")
    return resolved


def safe_start(
    env: Any,
    dataset: str | Path,
    fixture: str | Path,
    host: str,
) -> tuple[Path, Path]:
    """Refuse cloud, normal-data and non-loopback configuration. Returns resolved paths."""
    bad = sorted(k for k in env if str(k).upper().startswith(FORBIDDEN_ENV_PREFIXES))
    if bad:
        raise PreviewConfigError(
            "Refusing to start with application, cloud, store or AI settings in the environment "
            f"({', '.join(bad[:5])}). Start the preview from a clean environment."
        )
    if host not in LOOPBACK_HOSTS:
        raise PreviewConfigError("The preview binds to loopback only (127.0.0.1 or ::1).")
    data_path, fixture_path = _real(dataset, "dataset"), _real(fixture, "fixture")
    normal = data_file({}).parent.resolve()
    for path in (data_path, fixture_path):
        for guarded in (normal, (Path.home() / ".zava-forward").resolve()):
            if path == guarded or guarded in path.parents:
                raise PreviewConfigError("Refusing to read the normal working data location.")
    try:
        dataset_marker = json.loads(data_path.read_text(encoding="utf-8")).get("synthetic_preview")
        fixture_data = json.loads(fixture_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, AttributeError):
        raise PreviewConfigError("The dataset or fixture is not readable JSON.") from None
    fixture_meta = fixture_data.get("fixture") if isinstance(fixture_data, dict) else None
    if (
        not isinstance(dataset_marker, dict)
        or dataset_marker.get("disposable") is not True
        or not isinstance(fixture_meta, dict)
        or fixture_meta.get("synthetic") is not True
        or fixture_meta.get("disposable") is not True
        or dataset_marker.get("fixture_id") != fixture_meta.get("id")
    ):
        raise PreviewConfigError(
            "The dataset and fixture must be matching disposable synthetic preview files."
        )
    return data_path, fixture_path


def open_store(data_path: Path) -> tuple[Any, tempfile.TemporaryDirectory[str]]:
    """Open a private copy so the preview can never write beside the synthetic dataset."""
    from . import store as _store

    work = tempfile.TemporaryDirectory(prefix="ama444-resident-")
    root = Path(work.name)
    shutil.copy2(data_path, root / "dataset.json")
    docs = data_path.parent / "docs"
    if docs.is_dir() and not docs.is_symlink():
        shutil.copytree(docs, root / "docs", symlinks=False)
    store_class: Any = _store.Store
    store = store_class(
        str(root / "dataset.json"), str(root / "live.json"), str(root / "audit.jsonl")
    )
    return store, work


def fixture_summary(fixture_path: Path) -> dict[str, Any]:
    meta = _load_fixture(fixture_path)["fixture"]
    return dict(
        id=meta.get("id"), lineage=meta.get("lineage"), limitations=meta.get("limitations", [])
    )


def subjects(fixture_path: Path) -> list[str]:
    return [s["subject"] for s in _load_fixture(fixture_path)["subjects"] if isinstance(s, dict)]


__all__ = [
    "BANNER",
    "FIELD_CATALOG",
    "Grant",
    "GrantDenied",
    "PreviewConfigError",
    "fixture_summary",
    "resident_view",
    "resolve_grant",
    "safe_start",
    "subjects",
]
