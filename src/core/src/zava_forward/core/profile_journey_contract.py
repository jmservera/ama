"""Profile journey contract validator for the eleven perspectives (Refs #134, slice 5).

A walkthrough record states, for each of the five contract elements, the linked record ids it
inspected, the textual state meaning shown, whether it was keyboard operable and the status
announcement text. `validate` returns blockers only and never marks a perspective as accepted:
constructed-fixture records are not user validation or owner approval. `gaps` lists, per
perspective, the elements the coverage register still records as unmet or not observed by the
keyboard probe. Both read only what they are given.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from zava_forward.core import perspective_walkthroughs as pw

ELEMENTS = pw.ELEMENTS
NOTICE = (
    "Constructed-fixture contract check, not user validation. A clean result means the record "
    "is complete in shape; it does not mean a perspective journey is accepted."
)
# Text that alone would not tell a reader the state (colour or icon only labels).
NON_TEXT = frozenset({"red", "green", "amber", "yellow", "ok", "x", "-", "?"})


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def validate(walkthrough: Mapping[str, Any]) -> dict[str, Any]:
    """Return blockers for one perspective walkthrough record."""
    pid = _text(walkthrough.get("perspective")) or "?"
    steps = walkthrough.get("steps")
    steps = steps if isinstance(steps, Mapping) else {}
    blockers: list[str] = []
    for el in ELEMENTS:
        step = steps.get(el)
        if not isinstance(step, Mapping):
            blockers.append(f"{pid}.{el}:missing")
            continue
        ids = step.get("record_ids")
        if not isinstance(ids, list) or not [i for i in ids if _text(i)]:
            blockers.append(f"{pid}.{el}:no_linked_records")
        state = _text(step.get("state_text"))
        if not state or state.lower() in NON_TEXT:
            blockers.append(f"{pid}.{el}:state_not_textual")
        if step.get("keyboard_operable") is not True:
            blockers.append(f"{pid}.{el}:not_keyboard_operable")
        if not _text(step.get("announcement")):
            blockers.append(f"{pid}.{el}:no_status_announcement")
    handoff = steps.get("handoff")
    if isinstance(handoff, Mapping) and not _text(handoff.get("owner")):
        blockers.append(f"{pid}.handoff:no_accountable_owner")
    return dict(
        status="blocked" if blockers else "complete_in_shape",
        blockers=blockers,
        accepted=False,
        notice=NOTICE,
    )


def gaps(root: Path) -> dict[str, dict[str, list[str]]]:
    """Per perspective: elements unmet in the register and elements the probe did not observe."""
    reg = pw.check(root)
    if reg["blockers"]:
        raise ValueError(f"walkthrough register blocked: {reg['blockers']}")
    out: dict[str, dict[str, list[str]]] = {}
    for pid, cells in pw.register().items():
        out[pid] = dict(
            unmet=[e for e in ELEMENTS if cells[e]["status"] == "unmet"],
            not_probed=[e for e in ELEMENTS if e not in pw.PROBE_OBSERVED.get(pid, ())],
        )
    return out
