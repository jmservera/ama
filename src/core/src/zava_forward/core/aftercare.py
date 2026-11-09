"""Aftercare concern route and lived-performance evaluator view (FR-049, AC-063, #133).

A store-independent register for constructed concerns. A household or representative raises a
discomfort, higher-bill or control-use concern by a digital or staff-recorded (non-digital) route.
Each concern has a named human owner, an investigation outcome and a remedy status. Handover and
financial closure are recorded separately and never change a concern. A sensor reading is context
only and never dismisses a resident report. It reads or writes no consent, sanction or hazard state.
"""

from collections.abc import Iterable, Mapping
from copy import deepcopy
from datetime import date
from typing import Any

Record = dict[str, Any]

ROUTES = ("digital", "staff_recorded")
NON_DIGITAL_CHANNELS = ("phone", "in_person", "paper", "assisted_visit")
RAISED_BY = ("household", "representative")
CONCERN_KINDS = ("discomfort", "higher_bill", "control_use", "other")
INVESTIGATION = ("received", "under_investigation", "outcome_recorded")
OUTCOMES = ("remedy_needed", "no_remedy_needed", "advice_given", "cannot_determine")
HUMAN_BASES = ("home_visit", "household_conversation", "specialist_review", "records_review")
REMEDY_STATUSES = ("not_assessed", "open", "in_progress", "completed", "not_needed")
CLOSURE_KINDS = ("handover", "financial")
PACK_TASK = "aftercare-concern-pack"
PACK_ACTIONS = ("accept", "reject")
PACK_NOT_REVIEWED = "Not reviewed"
PACK_MANUAL_ROUTE = (
    "Use the concern record and the named owner; the pack is optional and no model is needed."
)
ACCESSIBLE_ROUTE = (
    "You can also raise this by phone, in person or on paper, and a member of staff will "
    "record it for you. No digital access is needed."
)
PROTECTION = (
    "Raising a concern will not change your tenancy, repairs or services. A named person looks "
    "into it, and a normal sensor reading does not close it."
)
EVALUATOR_NOTICE = (
    "These figures describe what was recorded. They do not show what caused a concern, they do "
    "not assign fault to any household, and they are not a promise of savings."
)
# Templated or generated text must not state causation, blame or savings.
BANNED_PHRASES = (
    "will save",
    "guaranteed",
    "you will pay less",
    "caused by",
    "because of the resident",
    "resident error",
    "misuse",
    "your fault",
    "blame",
    "wasting",
)


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} is required.")
    return value.strip()


def neutral_text(text: str) -> str:
    """Return the text, or raise if it states causation, blame or a savings promise."""
    lowered = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lowered:
            raise ValueError(f"Generated text must not contain '{phrase}'.")
    return text


def _context(value: Mapping[str, str] | None) -> dict[str, str] | None:
    """Sensor context is short descriptive text only; it passes the same neutral-text guard."""
    if not value:
        return None
    out: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not isinstance(item, str):
            raise ValueError("Sensor context must be short text.")
        out[key] = neutral_text(item)
    return out


def _labelled(pairs: Iterable[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"value": v, "label": neutral_text(label)} for v, label in pairs]


def intake_form() -> Record:
    """Plain-language household route definition for any screen or paper form to follow."""
    form: Record = {
        "title": "Raise a concern about your home",
        "intro": "Tell us if your home feels uncomfortable, your bills are higher than you "
        "expected, or you are unsure how to use your controls.",
        "accessible_route": ACCESSIBLE_ROUTE,
        "protection": PROTECTION,
        "fields": [
            {
                "name": "raised_by",
                "label": "Who is raising this?",
                "required": True,
                "options": _labelled(
                    [
                        ("household", "Someone who lives in the home"),
                        ("representative", "A person acting for the household"),
                    ]
                ),
            },
            {
                "name": "representative_basis",
                "required": False,
                "label": "If you are acting for the household, how are you authorised?",
                "required_when": "raised_by is representative",
            },
            {
                "name": "home_ref",
                "label": "Home reference from your handover pack",
                "required": True,
            },
            {
                "name": "kind",
                "label": "What is your concern about?",
                "required": True,
                "options": _labelled(
                    [
                        ("discomfort", "The home is too cold, too warm or damp"),
                        ("higher_bill", "My energy bill is higher than I expected"),
                        ("control_use", "I am not sure how to use my controls"),
                        ("other", "Something else"),
                    ]
                ),
            },
            {"name": "statement", "label": "Tell us in your own words", "required": True},
        ],
        "non_digital_channels": _labelled(
            [
                ("phone", "By phone"),
                ("in_person", "In person"),
                ("paper", "On paper"),
                ("assisted_visit", "With help at a visit"),
            ]
        ),
    }
    for field in form["fields"]:
        neutral_text(field["label"])
    neutral_text(form["intro"])
    return form


def intake_errors(values: Mapping[str, object]) -> dict[str, str]:
    """Plain-language problems per field, so a screen or staff member can help fix them."""
    errors: dict[str, str] = {}
    raised_by = values.get("raised_by")
    if raised_by not in RAISED_BY:
        errors["raised_by"] = "Say whether you live in the home or act for the household."
    if raised_by == "representative" and not _present(values.get("representative_basis")):
        errors["representative_basis"] = "Say how you are authorised to act for the household."
    if not _present(values.get("home_ref")):
        errors["home_ref"] = "Enter the home reference from your handover pack."
    if values.get("kind") not in CONCERN_KINDS:
        errors["kind"] = "Choose what your concern is about."
    if not _present(values.get("statement")):
        errors["statement"] = "Tell us your concern in your own words."
    return errors


def _present(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _fraction(count: int, denominator: int | None) -> dict[str, Any]:
    return {"count": count, "denominator": denominator}


class AftercareRegister:
    """Concerns, separate closure records and an evaluator view with stated denominators."""

    def __init__(self) -> None:
        self.concerns: dict[str, Record] = {}
        self.closures: list[Record] = []
        self.packs: dict[str, Record] = {}

    def to_state(self) -> Record:
        """JSON-safe snapshot for any store; a restore is checked by `from_state`."""
        return deepcopy({"concerns": self.concerns, "closures": self.closures, "packs": self.packs})

    @classmethod
    def from_state(cls, state: Mapping[str, Any]) -> "AftercareRegister":
        """Restore a snapshot, refusing one that would lose or weaken a recorded concern."""
        reg = cls()
        reg.concerns = deepcopy(dict(state.get("concerns", {})))
        reg.closures = deepcopy(list(state.get("closures", [])))
        reg.packs = deepcopy(dict(state.get("packs", {})))
        for n, (cid, rec) in enumerate(reg.concerns.items(), start=1):
            outcome = rec.get("outcome")
            if (
                cid != f"AC-{n:03d}"
                or rec.get("id") != cid
                or rec.get("route") not in ROUTES
                or rec.get("raised_by") not in RAISED_BY
                or rec.get("kind") not in CONCERN_KINDS
                or rec.get("investigation") not in INVESTIGATION
                or rec.get("dismissed_by_sensor") is not False
                or not _present(rec.get("owner"))
                or rec.get("remedy", {}).get("status") not in REMEDY_STATUSES
                or (rec["investigation"] == "outcome_recorded") != (outcome is not None)
                or (outcome is not None and outcome.get("basis") not in HUMAN_BASES)
            ):
                raise ValueError(f"Snapshot concern {cid} is not valid.")
        if any(i.get("kind") not in CLOSURE_KINDS for i in reg.closures):
            raise ValueError("Snapshot closure is not valid.")
        if any(p.get("concern_id") not in reg.concerns for p in reg.packs.values()):
            raise ValueError("Snapshot pack has no concern.")
        return reg

    def _get(self, cid: str) -> Record:
        if cid not in self.concerns:
            raise KeyError(cid)
        return self.concerns[cid]

    def _own(self, rec: Record, owner: str) -> None:
        if _text(owner, "Owner") != rec["owner"]:
            raise PermissionError("Only the named human owner can act on this concern.")

    def raise_concern(
        self,
        route: str,
        raised_by: str,
        home_ref: str,
        kind: str,
        statement: str,
        owner: str,
        next_update: str,
        representative_basis: str | None = None,
        recorded_by: str | None = None,
        channel: str | None = None,
        sensor_context: Mapping[str, str] | None = None,
    ) -> Record:
        if route not in ROUTES:
            raise ValueError("Route must be digital or staff_recorded.")
        if raised_by not in RAISED_BY:
            raise ValueError("Raised by must be household or representative.")
        if kind not in CONCERN_KINDS:
            raise ValueError("Concern kind must be discomfort, higher_bill, control_use or other.")
        extra: Record = {}
        if route == "staff_recorded":
            if channel not in NON_DIGITAL_CHANNELS:
                raise ValueError("Channel must be phone, in_person, paper or assisted_visit.")
            extra = {
                "recorded_by": _text(recorded_by, "Recording staff member"),
                "channel": channel,
            }
        if raised_by == "representative":
            extra["representative_basis"] = _text(representative_basis, "Representative basis")
        seq = len(self.concerns) + 1
        cid = f"AC-{seq:03d}"
        rec: Record = {
            "id": cid,
            "route": route,
            "raised_by": raised_by,
            "home_ref": _text(home_ref, "Home reference"),
            "kind": kind,
            "statement": _text(statement, "Concern statement"),
            "owner": _text(owner, "Human owner"),
            "next_update": date.fromisoformat(next_update).isoformat(),
            "accessible_route": ACCESSIBLE_ROUTE,
            "investigation": "received",
            "outcome": None,
            "remedy": {"status": "not_assessed", "evidence": None},
            "sensor_context": _context(sensor_context),
            "dismissed_by_sensor": False,
            "history": [{"event": "received"}],
            **extra,
        }
        self.concerns[cid] = rec
        return deepcopy(rec)

    def add_sensor_context(self, cid: str, context: Mapping[str, str]) -> Record:
        """Attach a later sensor signal as context only. No state, outcome or remedy changes."""
        rec = self._get(cid)
        new = _context(context)
        if new is None:
            raise ValueError("Sensor context is required.")
        rec["sensor_context"] = {**(rec["sensor_context"] or {}), **new}
        rec["history"].append({"event": "sensor_context_added"})
        return deepcopy(rec)

    def start_investigation(self, cid: str, owner: str, next_update: str) -> Record:
        rec = self._get(cid)
        self._own(rec, owner)
        if rec["investigation"] == "outcome_recorded":
            raise ValueError("An outcome is already recorded for this concern.")
        rec["investigation"] = "under_investigation"
        rec["next_update"] = date.fromisoformat(next_update).isoformat()
        rec["history"].append({"event": "under_investigation"})
        return deepcopy(rec)

    def record_outcome(
        self, cid: str, owner: str, outcome: str, basis: str, evidence: str
    ) -> Record:
        """The named owner records a human-evidenced outcome; a sensor reading is not a basis."""
        rec = self._get(cid)
        self._own(rec, owner)
        if outcome not in OUTCOMES:
            raise ValueError("Outcome must be one of " + ", ".join(OUTCOMES) + ".")
        if basis not in HUMAN_BASES:
            raise ValueError("Basis must be a human investigation, not a sensor reading.")
        if rec["investigation"] == "outcome_recorded":
            raise ValueError("An outcome is already recorded for this concern.")
        rec["investigation"] = "outcome_recorded"
        rec["outcome"] = {
            "outcome": outcome,
            "basis": basis,
            "evidence": _text(evidence, "Outcome evidence"),
        }
        if outcome == "remedy_needed" and rec["remedy"]["status"] == "not_assessed":
            rec["remedy"]["status"] = "open"
        rec["history"].append({"event": f"outcome_{outcome}"})
        return deepcopy(rec)

    def set_remedy(self, cid: str, owner: str, status: str, evidence: str | None = None) -> Record:
        rec = self._get(cid)
        self._own(rec, owner)
        if status not in REMEDY_STATUSES or status == "not_assessed":
            raise ValueError("Remedy status must be open, in_progress, completed or not_needed.")
        if status in ("completed", "not_needed"):
            _text(evidence, "Remedy evidence")
            if rec["investigation"] != "outcome_recorded":
                raise ValueError("Record an investigation outcome before completing a remedy.")
        rec["remedy"] = {"status": status, "evidence": evidence}
        rec["history"].append({"event": f"remedy_{status}"})
        return deepcopy(rec)

    def record_closure(self, home_ref: str, kind: str, closed_on: str, owner: str) -> Record:
        """Record handover or financial closure. It never changes any concern or remedy."""
        if kind not in CLOSURE_KINDS:
            raise ValueError("Closure kind must be handover or financial.")
        item = {
            "home_ref": _text(home_ref, "Home reference"),
            "kind": kind,
            "closed_on": date.fromisoformat(closed_on).isoformat(),
            "owner": _text(owner, "Closure owner"),
        }
        self.closures.append(item)
        return dict(item)

    def unresolved(self, home_ref: str | None = None) -> list[Record]:
        """Concerns with no outcome, or an outcome that needs a remedy not yet completed."""
        out = []
        for rec in self.concerns.values():
            if home_ref is not None and rec["home_ref"] != home_ref:
                continue
            no_outcome = rec["investigation"] != "outcome_recorded"
            outcome = (rec["outcome"] or {}).get("outcome")
            open_remedy = rec["remedy"]["status"] in ("open", "in_progress")
            undetermined = outcome == "cannot_determine"
            if no_outcome or open_remedy or undetermined:
                out.append(deepcopy(rec))
        return out

    def overdue(self, today: str) -> list[Record]:
        cutoff = date.fromisoformat(today).isoformat()
        return [r for r in self.unresolved() if r["next_update"] < cutoff]

    def view(self, cid: str) -> Record:
        """Household-facing view: owner, next update, outcome and remedy, without sensor context."""
        rec = deepcopy(self._get(cid))
        rec.pop("sensor_context", None)
        rec["protection"] = PROTECTION
        return rec

    def evaluator_view(
        self,
        handed_over_homes: Iterable[str],
        baseline_homes: Iterable[str] | None = None,
    ) -> Record:
        """Descriptive counts with denominators and unknowns; no causation, blame or savings."""
        homes = sorted(set(handed_over_homes))
        total = len(homes)
        scope = set(homes)
        concerns = [c for c in self.concerns.values() if c["home_ref"] in scope]
        out_of_scope = len(self.concerns) - len(concerns)
        baseline = None if baseline_homes is None else scope & set(baseline_homes)
        raising = {c["home_ref"] for c in concerns}
        unresolved_ids = {c["id"] for c in self.unresolved()}
        by_outcome: dict[str, int] = {o: 0 for o in OUTCOMES}
        by_outcome["no_outcome_yet"] = 0
        for c in concerns:
            by_outcome[(c["outcome"] or {}).get("outcome", "no_outcome_yet")] += 1
        closed = {
            k: {i["home_ref"] for i in self.closures if i["kind"] == k} for k in CLOSURE_KINDS
        }
        unresolved_after_closure = sum(
            1
            for c in concerns
            if c["id"] in unresolved_ids
            and c["home_ref"] in closed["handover"] | closed["financial"]
        )
        unknowns = ["Households that did not raise a concern may still have one."]
        if baseline is None:
            unknowns.insert(0, "Baseline coverage is unknown.")
        return {
            "homes_handed_over": total,
            "homes_with_baseline": _fraction(len(baseline), total)
            if baseline is not None
            else None,
            "homes_baseline_unknown": None if baseline is None else total - len(baseline),
            "households_raising_concern": _fraction(len(raising), total),
            "concerns_raised": len(concerns),
            "concerns_by_outcome": by_outcome,
            "concerns_unresolved": _fraction(
                sum(1 for c in concerns if c["id"] in unresolved_ids), len(concerns)
            ),
            "unresolved_with_handover_or_financial_closure": unresolved_after_closure,
            "concerns_outside_stated_scope": out_of_scope,
            "unknowns": unknowns,
            "notice": neutral_text(EVALUATOR_NOTICE),
        }

    def propose_pack(self, cid: str, ai_summary: str | None = None) -> Record:
        """Draft an unreviewed concern pack for the named owner; it changes nothing on the concern.

        The pack is always built from the record by template, so it exists when AI is unavailable.
        An optional AI summary is attached only after the neutral-text guard and is a proposal.
        """
        rec = self._get(cid)
        facts = [
            f"Raised by: {rec['raised_by']} by the {rec['route']} route.",
            f"Concern kind: {rec['kind']}.",
            f"Named owner: {rec['owner']}. Next update: {rec['next_update']}.",
            f"Investigation: {rec['investigation']}.",
            f"Remedy status: {rec['remedy']['status']}.",
        ]
        questions = [
            "What did the household describe, in their own words?",
            "What does a visit or conversation with the household show?",
            "What remedy, if any, does the household need, and who owns it?",
        ]
        summary = None if ai_summary is None else neutral_text(_text(ai_summary, "AI summary"))
        pack: Record = {
            "id": f"PK-{len(self.packs) + 1:03d}",
            "task": PACK_TASK,
            "concern_id": cid,
            "household_statement": rec["statement"],
            "recorded_facts": [neutral_text(f) for f in facts],
            "questions_for_investigator": [neutral_text(q) for q in questions],
            "ai_summary": summary,
            "source": "ai" if summary else "template",
            "approval": PACK_NOT_REVIEWED,
            "approved": False,
            "reviewer_function": rec["owner"],
            "review": None,
            "manual_route": PACK_MANUAL_ROUTE,
            "notice": neutral_text(EVALUATOR_NOTICE),
        }
        self.packs[pack["id"]] = pack
        rec["history"].append({"event": f"pack_proposed_{pack['id']}"})
        return deepcopy(pack)

    def review_pack(self, pack_id: str, reviewer: str, action: str, reason: str) -> Record:
        """Only the named owner accepts or rejects a pack; neither action alters the concern."""
        if pack_id not in self.packs:
            raise KeyError(pack_id)
        pack = self.packs[pack_id]
        self._own(self._get(pack["concern_id"]), reviewer)
        if action not in PACK_ACTIONS:
            raise ValueError("Action must be accept or reject.")
        if pack["review"] is not None:
            raise ValueError("This pack has already been reviewed.")
        pack["review"] = {
            "by": reviewer.strip(),
            "action": action,
            "reason": _text(reason, "Reason"),
        }
        pack["approval"] = "Accepted for reference" if action == "accept" else "Rejected"
        pack["approved"] = action == "accept"
        return deepcopy(pack)
