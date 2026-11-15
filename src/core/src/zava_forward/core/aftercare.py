"""Aftercare concern route and lived-performance evaluator view (FR-049, AC-063, #133).

A store-independent register for constructed concerns. A household or representative raises a
discomfort, higher-bill or control-use concern by a digital or staff-recorded (non-digital) route.
Each concern has a named human owner, an investigation outcome and a remedy status. Handover and
financial closure are recorded separately and never change a concern. A sensor reading is context
only and never dismisses a resident report. It reads or writes no consent, sanction or hazard state.
"""

import re
import unicodedata
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
    "because of the tenant",
    "because of the household",
    "because of the occupant",
    "resident error",
    "user error",
    "operator error",
    "misuse",
    "your fault",
    "blame",
    "wasting",
    "payback",
    "pays for itself",
    "pay for itself",
    "drying clothes",
    "drying laundry",
    "lifestyle choice",
)

_INVISIBLE = dict.fromkeys([*range(0x200B, 0x2010), 0x00AD, 0x2060, 0xFEFF])
_INVISIBLE_SPACE = dict.fromkeys([*range(0x200B, 0x2010), 0x00AD, 0x2060, 0xFEFF], " ")
_HOUSEHOLD = r"(?:tenant|resident|household|occupant)"
_MEASURE = (
    r"(?:retrofit|works|insulation|measures?|installation|upgrade|heating|ventilation|"
    r"heat pump|airtightness|glazing|controls?)"
)
_PARAPHRASE_SPECS: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (label, re.compile(pattern))
    for label, pattern in (
        ("future_save_promise", r"\byou'?ll (?:save|pay less)\b"),
        (
            "bill_cut_claim",
            r"\b(?:cut|slash)(?:s|es|ing)? (?:your |the |household )?(?:energy |heating )?"
            r"(?:bills?|costs?)\b",
        ),
        (
            "bills_will_fall",
            r"\b(?:energy |heating )?bills? will (?:fall|drop|go down|reduce)\b",
        ),
        ("savings_of", r"\bsavings? of\b"),
        (
            "quantified_savings_promise",
            r"\bsav(?:e|es|ing) (?:up to |around |over |about )?"
            r"(?:(?:£|\$|€|gbp ?)\d+(?:\.\d+)?|\d+(?:\.\d+)? ?(?:%|\b(?:percent|per cent|"
            r"pounds?|gbp)\b))",
        ),
        (
            "named_savings_claim",
            r"\b(?:promised|guaranteed|expected|assured|projected) "
            r"(?:(?:energy|bill|cost|financial|heating) )?(?:savings?|reductions?)\b",
        ),
        (
            "category_savings_claim",
            r"\b(?:energy|bill|cost|financial) savings?\b",
        ),
        (
            "cheaper_to_run",
            r"\bcheaper to (?:run|heat)\b",
        ),
        ("blame_inflections", r"\bblam(?:e|es|ed|ing)\b"),
        (
            "household_caused_or_misunderstood",
            rf"\b{_HOUSEHOLD}s? (?:has |have |had )?(?:caused|misunderstood|misused|ignored)\b",
        ),
        ("household_at_fault", rf"\b{_HOUSEHOLD}s? (?:is|was|were|are) at fault\b"),
        ("fault_of_household", rf"\bfault of (?:the )?{_HOUSEHOLD}s?\b"),
        ("household_behaviour", rf"\b{_HOUSEHOLD}s?'?s? (?:behaviou?r|lifestyle|habits?)\b"),
        ("heating_or_ventilation_habits", r"\b(?:heating|ventilation|occupancy) habits?\b"),
        (
            "window_or_ventilation_blame",
            r"\b(?:not opening windows?|windows? (?:kept |left )?(?:closed|shut)|"
            r"(?:lack of|failing to|failure to) (?:ventilat(?:e|ion)|heat))\b",
        ),
        (
            "improper_use_or_negligence",
            r"\b(?:(?:improper|incorrect) use|negligen(?:ce|t)|careless(?:ness)?)\b",
        ),
        (
            "reduces_bills_or_costs",
            r"\b(?:reduces?|reducing|lowers?|lowering|cuts?|trims?) "
            r"(?:your|the|household|energy|heating) (?:(?:energy|heating) )?(?:bills?|costs?)\b",
        ),
        ("lower_bills_claim", r"\b(?:lower|smaller|cheaper) (?:(?:energy|heating) )?bills?\b"),
        (
            "bills_will_be_cheaper",
            r"\bbills? (?:will|would) be (?:cheaper|lower|smaller)\b",
        ),
        (
            "measure_made_home_worse_or_better",
            rf"\b{_MEASURE} (?:has |have |had )?made "
            r"(?:the home|your home|it|things|the house|the room)?\s*"
            r"(?:colder|warmer|damper|mouldier|worse|better)\b",
        ),
        (
            "saves_money_or_energy",
            r"\b(?:saves?|saving) (?:you |the household )?(?:money|energy|costs?)\b",
        ),
        ("you_could_save", r"\byou (?:could|can|may|should) (?:save|pay less)\b"),
        (
            "bills_expected_to_fall",
            r"\b(?:bills?|costs?) (?:should|are expected to|is expected to|are likely to) "
            r"(?:fall|drop|go down|reduce)\b",
        ),
        (
            "savings_likely",
            r"\bsavings? (?:is|are) (?:likely|expected|certain|assured)\b",
        ),
        ("due_to_household", rf"\b(?:due|owing|down) to (?:the )?{_HOUSEHOLD}s?\b"),
        ("household_fault", rf"\b{_HOUSEHOLD}s?'?s? (?:own )?fault\b"),
        (
            "household_wastes_or_overuses",
            rf"\b{_HOUSEHOLD}s? (?:waste|wastes|wasted|overuse|overuses|overused)\b",
        ),
        ("overconsumption", r"\b(?:over-?use|overconsumption)\b"),
        ("result_of_measure", rf"\b(?:result|consequence) of (?:the )?{_MEASURE}\b"),
        (
            "measure_led_to_or_caused",
            rf"\b{_MEASURE} (?:has |have |had )?"
            r"(?:led to|leads to|resulted in|results in|caused|causes)\b",
        ),
        (
            "proven_or_attributable_causation",
            r"\b(?:(?:proven|proved) to cause|proves (?:that|the)\b|attribut(?:able|ed) to|"
            r"caused (?:the )?(?:damp|mould|mold|condensation|cold|higher|heat loss)|"
            r"is why (?:the|your)\b|reason (?:your bills?|the (?:room|home|house))\b)",
        ),
    )
)
PARAPHRASE_PATTERNS: tuple[re.Pattern[str], ...] = tuple(p for _, p in _PARAPHRASE_SPECS)

_CLAUSE_STOP = (
    r"(?=\s(?:and|but|or|however|therefore|thus|hence|consequently|yet|so|whereas|while|"
    r"though|although)\b|[.!?;:,\u2014\u2013]|\s-\s|--|$)"
)
# Only a "whether/if" phrase stating uncertainty is exempt; it ends at a comma, conjunction or stop.
_UNCERTAIN = re.compile(
    r"\b(?:cannot determine|can ?not determine|unknown|not known|no evidence)\s+(?:whether|if)\b"
    rf".*?{_CLAUSE_STOP}"
)


# A plain statement that no claim, causation, fault or promise is made is a caveat, not a claim.
_NEGATED_CLAIM = re.compile(
    r"(?:\b(?:no|not a|never a)\s+(?:claim|promise|guarantee)s?\s+(?:of|about)\b"
    r"|\b(?:do|does|did|can)\s*not\s+(?:show|prove|establish|claim|promise|assign|attribute)\b)"
    rf".*?{_CLAUSE_STOP}"
)


def _normalize_for_guard(text: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    nfkc = (
        unicodedata.normalize("NFKC", text)
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .lower()
    )
    variants = dict.fromkeys((nfkc.translate(_INVISIBLE), nfkc.translate(_INVISIBLE_SPACE)))
    collapsed = tuple(re.sub(r"\s+", " ", v).strip() for v in variants)
    claused = tuple(
        re.sub(r"[ \t\f\v]+", " ", re.sub(r"[\r\n]+", "; ", v)).strip() for v in variants
    )
    return collapsed, claused


def neutral_violations(text: str) -> tuple[str, ...]:
    """Return deterministic violation identifiers for causation, blame or savings-promise text."""
    collapsed_variants, claused_variants = _normalize_for_guard(text)
    found: list[str] = []
    for phrase in BANNED_PHRASES:
        if any(phrase in collapsed for collapsed in collapsed_variants):
            found.append(f"phrase:{phrase}")
    stripped_variants = tuple(
        _NEGATED_CLAIM.sub(" ", _UNCERTAIN.sub(" ", claused)) for claused in claused_variants
    )
    for label, pattern in _PARAPHRASE_SPECS:
        if any(pattern.search(stripped) for stripped in stripped_variants):
            found.append(f"pattern:{label}")
    return tuple(found)


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} is required.")
    return value.strip()


def neutral_text(text: str) -> str:
    """Return the text, or raise if it states causation, blame or a savings promise."""
    violations = neutral_violations(text)
    if violations:
        first = violations[0]
        if first.startswith("phrase:"):
            phrase = first.split(":", 1)[1]
            raise ValueError(f"Generated text must not contain '{phrase}'.")
        raise ValueError("Generated text must not state causation, blame or a savings promise.")
    return text


def _context(value: Mapping[str, str] | None) -> dict[str, str] | None:
    """Sensor context is short descriptive text only; keys and values pass neutral_text."""
    if not value:
        return None
    out: dict[str, str] = {}
    for key, item in value.items():
        if (
            not isinstance(key, str)
            or not key.strip()
            or not isinstance(item, str)
            or not item.strip()
        ):
            raise ValueError("Sensor context must be short text.")
        neutral_text(key)
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
    for key in ("title", "intro", "accessible_route", "protection"):
        form[key] = neutral_text(form[key])
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
    return {k: neutral_text(v) for k, v in errors.items()}


def _present(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _concern_number(cid: object) -> int:
    """Numeric part of an `AC-nnn` identifier; anything else is -1 and fails `from_state` checks."""
    if isinstance(cid, str) and re.fullmatch(r"AC-\d{3,}", cid):
        return int(cid[3:])
    return -1


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
        stored = deepcopy(dict(state.get("concerns", {})))
        reg.closures = deepcopy(list(state.get("closures", [])))
        reg.packs = deepcopy(dict(state.get("packs", {})))
        # Canonical JSON sorts keys as text, so AC-1000 precedes AC-101: restore in numeric order.
        reg.concerns = dict(sorted(stored.items(), key=lambda item: _concern_number(item[0])))
        for n, (cid, rec) in enumerate(reg.concerns.items(), start=1):
            outcome = rec.get("outcome")
            remedy = rec.get("remedy")
            if (
                cid != f"AC-{n:03d}"
                or rec.get("id") != cid
                or rec.get("route") not in ROUTES
                or rec.get("raised_by") not in RAISED_BY
                or rec.get("kind") not in CONCERN_KINDS
                or rec.get("investigation") not in INVESTIGATION
                or rec.get("dismissed_by_sensor") is not False
                or not _present(rec.get("home_ref"))
                or not _present(rec.get("statement"))
                or not _present(rec.get("owner"))
                or not _present(rec.get("accessible_route"))
                or not isinstance(remedy, Mapping)
                or remedy.get("status") not in REMEDY_STATUSES
                or (rec["investigation"] == "outcome_recorded") != (outcome is not None)
                or (
                    outcome is not None
                    and (
                        not isinstance(outcome, Mapping)
                        or outcome.get("outcome") not in OUTCOMES
                        or outcome.get("basis") not in HUMAN_BASES
                        or not _present(outcome.get("evidence"))
                    )
                )
                or (
                    remedy["status"] in ("completed", "not_needed")
                    and (outcome is None or not _present(remedy.get("evidence")))
                )
                or (remedy.get("evidence") is not None and not _present(remedy.get("evidence")))
                or (
                    rec["route"] == "staff_recorded"
                    and (
                        rec.get("channel") not in NON_DIGITAL_CHANNELS
                        or not _present(rec.get("recorded_by"))
                    )
                )
            ):
                raise ValueError(f"Snapshot concern {cid} is not valid.")
            neutral_text(rec["home_ref"])
            neutral_text(rec["owner"])
            neutral_text(rec["accessible_route"])
            if rec["route"] == "staff_recorded":
                neutral_text(rec["recorded_by"])
            sensor_ctx = rec.get("sensor_context")
            if sensor_ctx is not None:
                if not isinstance(sensor_ctx, Mapping) or not sensor_ctx:
                    raise ValueError(f"Snapshot concern {cid} sensor context is not valid.")
                _context(sensor_ctx)
            if outcome is not None:
                neutral_text(outcome["evidence"])
            if remedy.get("evidence") is not None:
                neutral_text(remedy["evidence"])
        for closure in reg.closures:
            if (
                not isinstance(closure, Mapping)
                or closure.get("kind") not in CLOSURE_KINDS
                or not _present(closure.get("home_ref"))
                or not _present(closure.get("owner"))
            ):
                raise ValueError("Snapshot closure is not valid.")
            neutral_text(closure["home_ref"])
            neutral_text(closure["owner"])
        for pid, pack in reg.packs.items():
            if not isinstance(pack, Mapping) or pack.get("concern_id") not in reg.concerns:
                raise ValueError("Snapshot pack has no concern.")
            if (
                pack.get("id") != pid
                or pack.get("task") != PACK_TASK
                or "sensor_context" in pack
                or not _present(pack.get("reviewer_function"))
                or not _present(pack.get("notice"))
                or not _present(pack.get("manual_route"))
                or not _present(pack.get("approval"))
                or not isinstance(pack.get("recorded_facts"), list)
                or not pack["recorded_facts"]
                or not all(_present(f) for f in pack["recorded_facts"])
                or not isinstance(pack.get("questions_for_investigator"), list)
                or not pack["questions_for_investigator"]
                or not all(_present(q) for q in pack["questions_for_investigator"])
                or (pack.get("ai_summary") is not None and not _present(pack.get("ai_summary")))
            ):
                raise ValueError(f"Snapshot pack {pid} is not valid.")
            neutral_text(pack["reviewer_function"])
            neutral_text(pack["notice"])
            neutral_text(pack["manual_route"])
            neutral_text(pack["approval"])
            for fact in pack["recorded_facts"]:
                neutral_text(fact)
            for question in pack["questions_for_investigator"]:
                neutral_text(question)
            if pack.get("ai_summary") is not None:
                neutral_text(pack["ai_summary"])
            review = pack.get("review")
            if review is not None:
                if (
                    not isinstance(review, Mapping)
                    or review.get("action") not in PACK_ACTIONS
                    or not _present(review.get("by"))
                    or not _present(review.get("reason"))
                ):
                    raise ValueError(f"Snapshot pack {pid} review is not valid.")
                neutral_text(review["by"])
                neutral_text(review["reason"])
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
                "recorded_by": neutral_text(_text(recorded_by, "Recording staff member")),
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
            "home_ref": neutral_text(_text(home_ref, "Home reference")),
            "kind": kind,
            "statement": _text(statement, "Concern statement"),
            "owner": neutral_text(_text(owner, "Human owner")),
            "next_update": date.fromisoformat(next_update).isoformat(),
            "accessible_route": neutral_text(ACCESSIBLE_ROUTE),
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
        checked_evidence = neutral_text(_text(evidence, "Outcome evidence"))
        rec["investigation"] = "outcome_recorded"
        rec["outcome"] = {
            "outcome": outcome,
            "basis": basis,
            "evidence": checked_evidence,
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
        checked_evidence: str | None
        if status in ("completed", "not_needed"):
            checked_evidence = neutral_text(_text(evidence, "Remedy evidence"))
            if rec["investigation"] != "outcome_recorded":
                raise ValueError("Record an investigation outcome before completing a remedy.")
        elif evidence is None:
            checked_evidence = None
        elif not isinstance(evidence, str):
            raise ValueError("Remedy evidence is required.")
        else:
            checked_evidence = neutral_text(evidence.strip()) if evidence.strip() else None
        rec["remedy"] = {"status": status, "evidence": checked_evidence}
        rec["history"].append({"event": f"remedy_{status}"})
        return deepcopy(rec)

    def record_closure(self, home_ref: str, kind: str, closed_on: str, owner: str) -> Record:
        """Record handover or financial closure. It never changes any concern or remedy."""
        if kind not in CLOSURE_KINDS:
            raise ValueError("Closure kind must be handover or financial.")
        item = {
            "home_ref": neutral_text(_text(home_ref, "Home reference")),
            "kind": kind,
            "closed_on": date.fromisoformat(closed_on).isoformat(),
            "owner": neutral_text(_text(owner, "Closure owner")),
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
        rec["protection"] = neutral_text(PROTECTION)
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
            "unknowns": [neutral_text(u) for u in unknowns],
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
            "approval": neutral_text(PACK_NOT_REVIEWED),
            "approved": False,
            "reviewer_function": neutral_text(_text(rec["owner"], "Human owner")),
            "review": None,
            "manual_route": neutral_text(PACK_MANUAL_ROUTE),
            "notice": neutral_text(EVALUATOR_NOTICE),
        }
        self.packs[pack["id"]] = pack
        return deepcopy(pack)

    def review_pack(self, pack_id: str, reviewer: str, action: str, reason: str) -> Record:
        """Only the named owner accepts or rejects a pack; neither action alters the concern."""
        if pack_id not in self.packs:
            raise KeyError(pack_id)
        pack = self.packs[pack_id]
        checked_reviewer = neutral_text(_text(reviewer, "Owner"))
        self._own(self._get(pack["concern_id"]), checked_reviewer)
        if action not in PACK_ACTIONS:
            raise ValueError("Action must be accept or reject.")
        if pack["review"] is not None:
            raise ValueError("This pack has already been reviewed.")
        checked_reason = neutral_text(_text(reason, "Reason"))
        pack["review"] = {
            "by": checked_reviewer,
            "action": action,
            "reason": checked_reason,
        }
        pack["approval"] = neutral_text(
            "Accepted for reference" if action == "accept" else "Rejected"
        )
        pack["approved"] = action == "accept"
        return deepcopy(pack)
