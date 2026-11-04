"""Phase 0 baseline population and wait analysis (BG-011; issue #124).

Pure, deterministic arithmetic for the discovery brief's population and time
attribution method. It reads no company data, calls no model and writes no
store, so the analysis stays manual and works when AI is unavailable. Fixtures
that use it are synthetic demonstration data. Results are candidates for the
named operational owners to validate; unknown or disputed causes stay visible
and are never assigned by inference.
"""

from collections import Counter
from dataclasses import dataclass
from datetime import date

UNKNOWN, DISPUTED = "UNKNOWN", "DISPUTED"
UNATTRIBUTED = "Unattributed"
LOOP_KINDS = ("return", "rejection", "repeat visit", "reopen")
LEGS = (
    ("installation to physical acceptance", "installation", "physical acceptance"),
    ("physical acceptance to evidence acceptance", "physical acceptance", "evidence acceptance"),
    ("evidence acceptance to resident handover", "evidence acceptance", "resident handover"),
)
NOTICE = "Candidate analysis. Not a company finding until the named owner validates it."


@dataclass(frozen=True)
class Candidate:
    property_id: str
    identified_on: date
    excluded_reason: str = ""
    outcome_known: bool = True


def baseline_summary(candidates: list[Candidate], start: date, end: date) -> dict[str, object]:
    """Population report; properties that did not progress are kept, never dropped."""
    if end < start:
        raise ValueError("The baseline end date cannot be before the start date")
    ids = Counter(c.property_id for c in candidates)
    inside = [c for c in candidates if start <= c.identified_on <= end]
    return dict(
        start=start,
        end=end,
        candidates=len(inside),
        before_window=sum(c.identified_on < start for c in candidates),
        after_window=sum(c.identified_on > end for c in candidates),
        excluded=dict(
            Counter(c.excluded_reason.strip() for c in inside if c.excluded_reason.strip())
        ),
        open_outcome_unknown=sum(not c.outcome_known for c in inside),
        duplicate_ids=sorted(i for i, n in ids.items() if n > 1),
        notice=NOTICE,
    )


@dataclass(frozen=True)
class LifecycleEvent:
    property_id: str
    event: str
    on: date


def leg_days(events: list[LifecycleEvent], property_id: str) -> dict[str, int | None]:
    """Calendar days per handover leg; None when either event is missing or out of order."""
    first: dict[str, date] = {}
    for e in events:
        if e.property_id == property_id and (e.event not in first or e.on < first[e.event]):
            first[e.event] = e.on
    out: dict[str, int | None] = {}
    for label, a, b in LEGS:
        ok = a in first and b in first and first[b] >= first[a]
        out[label] = (first[b] - first[a]).days if ok else None
    return out


@dataclass(frozen=True)
class Wait:
    property_id: str
    party: str
    start: date
    end: date | None = None
    primary_code: str = UNKNOWN
    contributing: tuple[str, ...] = ()


def wait_days(wait: Wait, as_of: date) -> int:
    end = wait.end if wait.end is not None else as_of
    if end < wait.start:
        raise ValueError("A wait cannot end before it starts")
    return (end - wait.start).days


def waits_by_party(waits: list[Wait], as_of: date) -> list[dict[str, object]]:
    """Calendar days awaiting each named party, largest first, with unattributed time visible."""
    days: Counter[str] = Counter()
    open_waits: Counter[str] = Counter()
    unexplained: Counter[str] = Counter()
    for w in waits:
        party = w.party.strip() or UNATTRIBUTED
        days[party] += wait_days(w, as_of)
        open_waits[party] += w.end is None
        unexplained[party] += w.primary_code in (UNKNOWN, DISPUTED, "")
    return [
        dict(
            party=p,
            days=n,
            open_waits=open_waits[p],
            unknown_or_disputed_cause=unexplained[p],
            notice=NOTICE,
        )
        for p, n in sorted(days.items(), key=lambda kv: (-kv[1], kv[0]))
    ]


@dataclass(frozen=True)
class Loop:
    property_id: str
    kind: str
    on: date


def loop_counts(loops: list[Loop]) -> dict[str, dict[str, int]]:
    """Return, rejection, repeat-visit and reopen counts per property."""
    out: dict[str, dict[str, int]] = {}
    for item in loops:
        if item.kind not in LOOP_KINDS:
            raise ValueError(f"Loop kind must be one of {', '.join(LOOP_KINDS)}")
        row = out.setdefault(item.property_id, dict.fromkeys(LOOP_KINDS, 0))
        row[item.kind] += 1
    return out
