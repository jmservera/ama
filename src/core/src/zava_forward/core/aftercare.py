"""Aftercare concern route and lived-performance evaluator view (FR-049, AC-063, #133).

A store-independent register for constructed concerns. A household or representative raises a
discomfort, higher-bill or control-use concern by a digital or staff-recorded (non-digital) route.
Each concern has a named human owner, an investigation outcome and a remedy status. Handover and
financial closure are recorded separately and never change a concern. A sensor reading is context
only and never dismisses a resident report. It reads or writes no consent, sanction or hazard state.
"""

import re
import unicodedata
from collections.abc import Callable, Iterable, Mapping
from copy import deepcopy
from datetime import date
from functools import lru_cache
from typing import Any, cast

from . import ai_registry

Record = dict[str, Any]
_registry_get = cast(Callable[[str], dict[str, Any] | None], ai_registry.get)
_authorizes_live = cast(
    Callable[[str, Mapping[str, str] | None], bool], ai_registry.authorizes_live
)

ROUTES = ("digital", "staff_recorded")
NON_DIGITAL_CHANNELS = ("phone", "in_person", "paper", "assisted_visit", "representative")
RAISED_BY = ("household", "representative")
CONCERN_KINDS = ("discomfort", "higher_bill", "control_use", "other")
INVESTIGATION = ("received", "under_investigation", "outcome_recorded")
OUTCOMES = ("remedy_needed", "no_remedy_needed", "advice_given", "cannot_determine")
HUMAN_BASES = ("home_visit", "household_conversation", "specialist_review", "records_review")
REMEDY_STATUSES = ("not_assessed", "open", "in_progress", "completed", "not_needed")
CLOSURE_KINDS = ("handover", "financial")
PACK_TASK: str = str(ai_registry.CONCERN_PACK_TASK)
PACK_ACTIONS = ("accept", "reject")
PACK_NOT_REVIEWED = "Not reviewed"
PACK_MANUAL_ROUTE = (
    "Use the concern record and the named owner; the pack is optional and no model is needed."
)
ACCESSIBLE_ROUTE = (
    "You can also raise this by phone, in person, on paper, with help at a visit or through a "
    "representative, and a member of staff will record it for you. No digital access is needed."
)
SUPPORT_OPTIONS = (
    ("large_print", "Large print"),
    ("easy_read", "Easy read"),
    ("interpreter", "Language interpreter"),
    ("bsl", "British Sign Language (BSL)"),
    ("callback_window", "Agreed phone call-back time"),
    ("paper_letter", "Paper letter or form by post"),
    ("support_person", "A visit where someone you trust can be with you"),
)
SUPPORT_OPTION_CODES: tuple[str, ...] = tuple(code for code, _ in SUPPORT_OPTIONS)
SUPPORT_NOTE = (
    "Tell the member of staff what would help and they will arrange it. You do not need to "
    "explain why, and you can bring or send a person to speak for you."
)
FORM_TITLE = "Raise a concern about your home"
FORM_INTRO = (
    "Tell us if your home feels uncomfortable, your bills are higher than you "
    "expected, or you are unsure how to use your controls."
)
INTAKE_ERROR_MESSAGES = {
    "raised_by": "Say whether you live in the home or act for the household.",
    "representative_basis": "Say how you are authorised to act for the household.",
    "home_ref": "Enter the home reference from your handover pack.",
    "kind": "Choose what your concern is about.",
    "statement": "Tell us your concern in your own words.",
    "support_needed": "Choose from the listed support options, or leave this blank.",
}
EVALUATOR_UNKNOWNS = (
    "Baseline coverage is unknown.",
    "Households that did not raise a concern may still have one.",
)
PACK_APPROVAL_LABELS = {
    "accept": "Accepted for reference",
    "reject": "Rejected",
}
PACK_QUESTIONS = (
    "What did the household describe, in their own words?",
    "What does a visit or conversation with the household show?",
    "What remedy, if any, does the household need, and who owns it?",
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


_HOUSEHOLD = r"(?:tenant|resident|household|occupant)"
_RETROFIT = r"(?:retrofit|works|insulation|measures|installation|upgrade|heating|ventilation)"
_CONTROL_OR_HABIT = (
    r"(?:thermostat|heating controls?|controls?|ventilation|windows?|trickle vents?|"
    r"lifestyle|habits?|behaviou?r)"
)
PARAPHRASE_PATTERNS = tuple(
    re.compile(p)
    for p in (
        r"\byou'?ll (?:save|pay less)\b",
        r"\bcut(?:s|ting)? your (?:energy )?bills?\b",
        r"\bbills? will (?:fall|drop|go down|reduce)\b",
        r"\bsavings? of\b",
        rf"\b{_HOUSEHOLD}s? (?:has |have |had )?(?:caused|misunderstood)\b",
        rf"\b{_HOUSEHOLD}s? (?:is|was|were|are) at fault\b",
        (
            rf"\b(?:{_HOUSEHOLD}|user)(?:s'|'s|s)? "
            r"(?:error|mistake|misuse|neglect|lifestyle|habits?|behaviou?r)\b"
        ),
        r"\b(?:reduces?|lowers?|cuts?|trims?) (?:your|the|household|energy) "
        r"(?:energy )?(?:bills?|costs?)\b",
        r"\b(?:lower|smaller|cheaper) (?:energy )?bills?\b",
        r"\bbills? (?:will|would) be (?:cheaper|lower|smaller)\b",
        rf"\b{_RETROFIT} (?:has |have |had )?made (?:the home|your home|it|things|the house)?\s*"
        r"(?:colder|warmer|damper|worse|better)\b",
        r"\b(?:saves?|saving) (?:you |the household )?(?:money|energy|costs?)\b",
        r"\byou (?:could|can|may|should) (?:save|pay less)\b",
        r"\b(?:bills?|costs?) (?:should|are expected to|is expected to|are likely to) "
        r"(?:fall|drop|go down|reduce)\b",
        r"\bsavings? (?:is|are) (?:likely|expected|certain|assured)\b",
        rf"\b(?:due|owing|down) to (?:the )?(?:{_HOUSEHOLD}s?|{_RETROFIT})\b",
        rf"\b(?:due|owing|down) to (?:[\w'-]+ ){{0,4}}{_CONTROL_OR_HABIT}\b",
        rf"\b{_HOUSEHOLD}(?:s'|'s|s)? (?:own )?fault\b",
        rf"\b{_HOUSEHOLD}s? (?:has |have |had )?failed to\b",
        rf"\b{_HOUSEHOLD}s? (?:waste|wastes|wasted|overuse|overuses|overused)\b",
        r"\b(?:over-?use|overconsumption)\b",
        rf"\b(?:result|consequence) of (?:the )?(?:new |recent )?{_RETROFIT}\b",
        (
            r"\b(?:result(?:s|ed|ing)?|aris(?:es|en|ing)|arose|stem(?:s|med|ming)?) from "
            r"(?:the |your |their )?(?:new |recent |poor |incorrect |wrong )?"
            rf"(?:{_RETROFIT}|{_HOUSEHOLD}(?:s'|'s|s)?|{_CONTROL_OR_HABIT})\b"
        ),
        (
            rf"\b(?:{_RETROFIT}|{_HOUSEHOLD}(?:s'|'s|s)?|{_CONTROL_OR_HABIT}) "
            r"(?:is|are|was|were) responsible for\b"
        ),
        (
            r"\b(?:is|are|was|were) responsible for (?:[\w'-]+ ){0,3}"
            r"(?:damp|mould|mold|condensation|chill|cold|discomfort|higher bills?|heat loss)\b"
        ),
        (
            r"\b(?:triggered|provoked|created|produced|induced|driven) by "
            rf"(?:the )?(?:new |recent )?(?:{_HOUSEHOLD}s?|{_RETROFIT}|{_CONTROL_OR_HABIT})\b"
        ),
        (
            rf"\b{_RETROFIT} (?:has |have |had )?"
            r"(?:led to|leads to|resulted in|results in|caused|causes)\b"
        ),
        (
            r"\bbecause (?:of )?(?:the |your |their )?"
            rf"(?:{_HOUSEHOLD}s?|{_RETROFIT}|{_CONTROL_OR_HABIT})\b"
        ),
        r"\b(?:attributable|attributed) to\b",
        rf"\b(?:fault|error|mistake|negligence) of (?:the )?{_HOUSEHOLD}s?\b",
        r"\bpoor (?:ventilation|heating|thermostat|control) (?:habits?|use|practices?)\b",
        (
            r"\b(?:incorrect|wrong|improper|poor) (?:use of (?:the )?|way of using (?:the )?)?"
            r"(?:thermostat|heating controls?|controls?|ventilation|trickle vents?|heating)\b"
        ),
        (
            rf"\b{_HOUSEHOLD}(?:s'|'s|s)? (?:has |have |had |is |are |was |were )?"
            r"(?:turn(?:s|ed|ing)?|set(?:s|ting)?|keep(?:s|ing)?|kept|leav(?:es|ing)|left|"
            r"shut(?:s|ting)?|clos(?:es|ed|ing)) (?:the |their )?"
            r"(?:thermostat|heating|controls?|windows?|trickle vents?)\b"
        ),
        (
            r"\b(?:leaving|keeping|left|kept) (?:the |their )?"
            r"(?:windows?|trickle vents?|vents?) (?:closed|shut)\b"
        ),
        r"\b(?:turning|turned) (?:the |their )?(?:thermostat|heating) (?:down|off|up too high)\b",
        r"\bnot ventilating(?: the home)? properly\b|\bfailure to ventilate\b",
        r"\bdrying (?:wet )?(?:clothes|laundry|washing) indoors\b",
        r"\bblam(?:e|ed|es|ing)\b",
        r"\bmis[-_ ]?us(?:e|ed|es|ing)\b",
        r"\bwast(?:e|ed|es|ing) (?:heat|energy|power|money)\b",
        (
            r"\b(?:guarantees?|guaranteeing|guaranteed|promis(?:e|es|ed|ing)|assur(?:e|es|ed|ing)) "
            r"(?:[\w'-]+ ){0,4}"
            r"(?:(?:energy |bill |cost )?savings?|bill (?:reductions?|cuts?|drops?)|"
            r"(?:lower|cheaper|smaller|reduced)(?:\b| (?:energy |heating )?(?:bills?|costs?)))\b"
        ),
        (
            r"\b(?:energy |heating )?bill reductions? "
            r"(?:are |is )?(?:guaranteed|promised|assured|certain)\b"
        ),
        (
            r"\bslash(?:es|ed|ing)? "
            r"(?:your |the |their |household |energy |heating )*(?:bills?|costs?)\b"
        ),
        r"\b(?:save|saving|pay less) on (?:your |the |their |household )?"
        r"(?:energy |heating )?(?:bills?|costs?)\b",
        r"(?:[£$€]\s*\d+|\b\d+\s*(?:pounds?|percent|%))\s+off\s+"
        r"(?:your |the |their |household )?(?:energy |heating )?(?:bills?|costs?)\b",
        r"\bwill (?:cost less|be cheaper|cut costs?|reduce costs?)\b",
    )
)
_CLAUSE_STOP = (
    r"(?=\s(?:and|but|or|while|yet|though|although|because|so|whereas)\s|"
    r"--|[.!?;,:\n\u2013\u2014()]|$)"
)
# Only a single-clause "whether/if" phrase stating uncertainty is exempt; it stops at any break.
_UNCERTAIN = re.compile(
    r"\b(?:cannot determine|can ?not determine|unknown|not known|no evidence)\s+(?:whether|if)\b"
    r"[^.!?;,:\n\u2013\u2014()]*?" + _CLAUSE_STOP
)


# A plain statement that no claim or promise is made is a caveat, never a mask for a second clause.
_NEGATED_CLAIM = re.compile(
    r"(?:\b(?:no|not a|never a)\s+(?:claim|promise|guarantee|finding|attribution)s?\s+"
    r"(?:of|about)\b[^.!?;,:\n\u2013\u2014()]*?" + _CLAUSE_STOP + r"|"
    r"\b(?:(?:do|does|did|can|will)\s+not|cannot|never)\s+"
    r"(?:(?:show|assign|attribute|prove|find|make)\s+"
    r"(?:a\s+|any\s+)?(?:cause|fault|blame|claim)(?:,\s*|\s+or\s+))*"
    r"(?:(?:claim|promise|guarantee)(?:\s+or\s+|\s*,\s*)?)+\s+"
    r"(?:any\s+)?(?:energy\s+|bill\s+|cost\s+)?savings?\b)"
)


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} is required.")
    return value.strip()


_INVISIBLE = dict.fromkeys([*range(0x200B, 0x2010), 0x2060, 0xFEFF, 0x00AD])
_NEUTRAL_ERROR = "Generated text must not state causation, blame or a savings promise."


def _squash_lines(value: str) -> str:
    return "\n".join(" ".join(line.split()) for line in re.split(r"[\r\n]+", value))


def _variants(text: str) -> list[str]:
    """Lower-cased forms preserving line breaks while folding width, spacing and hidden chars."""
    folded = unicodedata.normalize("NFKC", text).lower().replace("\u2019", "'")
    joined = _squash_lines(folded.translate(_INVISIBLE))
    spaced = _squash_lines(folded.translate(dict.fromkeys(_INVISIBLE, " ")))
    dehyphen = _squash_lines(re.sub(r"(?<=\w)[-_]+(?=\w)", " ", joined))
    out: list[str] = []
    for candidate in (joined, spaced, dehyphen):
        if candidate not in out:
            out.append(candidate)
    return out


@lru_cache(maxsize=512)
def _check_neutral(text: str) -> None:
    for lowered in _variants(text):
        collapsed = " ".join(lowered.split())
        unhyphen = re.sub(r"(?<=\w)[-_]+(?=\w)", "", collapsed)
        for phrase in BANNED_PHRASES:
            if phrase in collapsed or phrase in unhyphen:
                raise ValueError(_NEUTRAL_ERROR)
        stripped = _NEGATED_CLAIM.sub(" ; ", _UNCERTAIN.sub(" ; ", lowered))
        stripped_collapsed = " ".join(stripped.split())
        for pattern in PARAPHRASE_PATTERNS:
            if pattern.search(stripped) or pattern.search(stripped_collapsed):
                raise ValueError(_NEUTRAL_ERROR)


def neutral_text(text: str) -> str:
    """Return the text, or raise if it states causation, blame or a savings promise."""
    _check_neutral(text)
    return text


def strip_unsafe_sentences(text: str) -> str:
    """Drop every sentence or line stating causation, blame or a savings promise; keep the rest."""
    kept: list[str] = []
    for paragraph in re.split(r"\n\s*\n+", text.strip()):
        folded = " ".join(paragraph.split())
        if not folded:
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", folded):
            if not sentence:
                continue
            try:
                neutral_text(sentence)
                neutral_text(" ".join([*kept, sentence]))
            except ValueError:
                continue
            kept.append(sentence)
    return " ".join(kept)


def assert_templates_neutral(*templates: object) -> None:
    """Fail fast when a fixed template, label or note (str, list, tuple, dict) is not neutral."""
    for item in templates:
        if isinstance(item, str):
            neutral_text(item)
        elif isinstance(item, Mapping):
            assert_templates_neutral(*item.keys(), *item.values())
        elif isinstance(item, (list, tuple)):
            assert_templates_neutral(*item)


assert_templates_neutral(
    ACCESSIBLE_ROUTE,
    PROTECTION,
    EVALUATOR_NOTICE,
    PACK_MANUAL_ROUTE,
    PACK_NOT_REVIEWED,
    PACK_APPROVAL_LABELS,
    PACK_QUESTIONS,
    SUPPORT_OPTIONS,
    SUPPORT_NOTE,
    FORM_TITLE,
    FORM_INTRO,
    INTAKE_ERROR_MESSAGES,
    EVALUATOR_UNKNOWNS,
)


def _context(value: Mapping[str, str] | None) -> dict[str, str] | None:
    """Sensor context is short descriptive text only; it passes the same neutral-text guard."""
    if not value:
        return None
    out: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not isinstance(item, str):
            raise ValueError("Sensor context must be short text.")
        out[neutral_text(key)] = neutral_text(item)
    return out


def _labelled(pairs: Iterable[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"value": v, "label": neutral_text(label)} for v, label in pairs]


def normalize_support_needed(value: object) -> list[str]:
    """Validate optional communication/accessibility support codes without requiring a reason."""
    if value is None:
        return []
    if isinstance(value, str):
        parts = [part.strip() for part in value.split(",") if part.strip()]
        if not parts:
            return []
        value = parts
    if isinstance(value, (bytes, bytearray, Mapping)) or not isinstance(value, Iterable):
        raise ValueError("Support needed must be chosen from SUPPORT_OPTIONS.")
    out: list[str] = []
    for item in value:
        if not isinstance(item, str):
            raise ValueError("Support needed must be chosen from SUPPORT_OPTIONS.")
        code = item.strip()
        if code == "call_back":
            code = "callback_window"
        if code not in SUPPORT_OPTION_CODES:
            raise ValueError("Support needed must be chosen from SUPPORT_OPTIONS.")
        if code not in out:
            out.append(code)
    return out


def intake_form() -> Record:
    """Plain-language household route definition for any screen or paper form to follow."""
    form: Record = {
        "title": neutral_text(FORM_TITLE),
        "intro": neutral_text(FORM_INTRO),
        "accessible_route": neutral_text(ACCESSIBLE_ROUTE),
        "support_note": neutral_text(SUPPORT_NOTE),
        "support_options": _labelled(SUPPORT_OPTIONS),
        "protection": neutral_text(PROTECTION),
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
            {
                "name": "support_needed",
                "label": "Would any of these help us communicate with you?",
                "required": False,
                "multiple": True,
                "options": _labelled(SUPPORT_OPTIONS),
            },
        ],
        "non_digital_channels": _labelled(
            [
                ("phone", "By phone"),
                ("in_person", "In person"),
                ("paper", "On paper"),
                ("assisted_visit", "With help at a visit"),
                ("representative", "Through a representative"),
            ]
        ),
    }
    for field in form["fields"]:
        neutral_text(field["label"])
    return form


def intake_errors(values: Mapping[str, object]) -> dict[str, str]:
    """Plain-language problems per field, so a screen or staff member can help fix them."""
    errors: dict[str, str] = {}
    raised_by = values.get("raised_by")
    if raised_by not in RAISED_BY:
        errors["raised_by"] = neutral_text(INTAKE_ERROR_MESSAGES["raised_by"])
    if raised_by == "representative" and not _present(values.get("representative_basis")):
        errors["representative_basis"] = neutral_text(INTAKE_ERROR_MESSAGES["representative_basis"])
    if not _present(values.get("home_ref")):
        errors["home_ref"] = neutral_text(INTAKE_ERROR_MESSAGES["home_ref"])
    if values.get("kind") not in CONCERN_KINDS:
        errors["kind"] = neutral_text(INTAKE_ERROR_MESSAGES["kind"])
    if not _present(values.get("statement")):
        errors["statement"] = neutral_text(INTAKE_ERROR_MESSAGES["statement"])
    try:
        normalize_support_needed(values.get("support_needed"))
    except ValueError:
        errors["support_needed"] = neutral_text(INTAKE_ERROR_MESSAGES["support_needed"])
    return errors


def intake_error_summary(errors: Mapping[str, str]) -> str:
    """One plain sentence that leads an error list, so no one has to scan a form to find it."""
    if not errors:
        return ""
    count = len(errors)
    return neutral_text(
        f"There {'is 1 thing' if count == 1 else f'are {count} things'} to fix before we can "
        "record this. If it is easier, tell a member of staff and they will do it with you."
    )


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
            has_support = "support_needed" in rec
            support = rec.get("support_needed", [])
            valid_support = (
                isinstance(support, list)
                and all(isinstance(s, str) and s in SUPPORT_OPTION_CODES for s in support)
                and len(set(support)) == len(support)
            )
            if (
                cid != f"AC-{n:03d}"
                or rec.get("id") != cid
                or rec.get("route") not in ROUTES
                or rec.get("raised_by") not in RAISED_BY
                or rec.get("kind") not in CONCERN_KINDS
                or rec.get("investigation") not in INVESTIGATION
                or rec.get("dismissed_by_sensor") is not False
                or not _present(rec.get("owner"))
                or not valid_support
                or rec.get("remedy", {}).get("status") not in REMEDY_STATUSES
                or (rec["investigation"] == "outcome_recorded") != (outcome is not None)
                or (
                    outcome is not None
                    and (
                        outcome.get("basis") not in HUMAN_BASES
                        or not _present(outcome.get("evidence"))
                    )
                )
                or (
                    rec["remedy"]["status"] in ("completed", "not_needed")
                    and (outcome is None or not _present(rec["remedy"].get("evidence")))
                )
            ):
                raise ValueError(f"Snapshot concern {cid} is not valid.")
            neutral_text(rec["owner"])
            if outcome is not None:
                neutral_text(outcome["evidence"])
            remedy_evidence = rec["remedy"].get("evidence")
            if remedy_evidence is not None:
                if not isinstance(remedy_evidence, str):
                    raise ValueError(f"Snapshot concern {cid} is not valid.")
                if remedy_evidence.strip():
                    neutral_text(remedy_evidence)
            if rec.get("sensor_context") is not None:
                if not isinstance(rec["sensor_context"], Mapping):
                    raise ValueError(f"Snapshot concern {cid} is not valid.")
                _context(rec["sensor_context"])
            if not has_support:
                rec["support_needed"] = []
        for closure in reg.closures:
            if closure.get("kind") not in CLOSURE_KINDS or not _present(closure.get("owner")):
                raise ValueError("Snapshot closure is not valid.")
            neutral_text(closure["owner"])
        if any(p.get("concern_id") not in reg.concerns for p in reg.packs.values()):
            raise ValueError("Snapshot pack has no concern.")
        for pack in reg.packs.values():
            ai_summary = pack.get("ai_summary")
            if ai_summary is not None:
                if not isinstance(ai_summary, str) or not ai_summary.strip():
                    raise ValueError("Snapshot pack is not valid.")
                neutral_text(ai_summary)
            for list_key in ("recorded_facts", "questions_for_investigator"):
                entries = pack.get(list_key)
                if not isinstance(entries, list) or not all(isinstance(v, str) for v in entries):
                    raise ValueError("Snapshot pack is not valid.")
                for entry in entries:
                    neutral_text(entry)
            for str_key in ("approval", "manual_route", "notice"):
                val = pack.get(str_key)
                if not _present(val):
                    raise ValueError("Snapshot pack is not valid.")
                neutral_text(str(val))
            review = pack.get("review")
            if review is not None:
                if not isinstance(review, Mapping) or not _present(review.get("reason")):
                    raise ValueError("Snapshot pack is not valid.")
                neutral_text(str(review["reason"]))
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
        support_needed: object = None,
    ) -> Record:
        if route not in ROUTES:
            raise ValueError("Route must be digital or staff_recorded.")
        if raised_by not in RAISED_BY:
            raise ValueError("Raised by must be household or representative.")
        if kind not in CONCERN_KINDS:
            raise ValueError("Concern kind must be discomfort, higher_bill, control_use or other.")
        support = normalize_support_needed(support_needed)
        extra: Record = {}
        if route == "staff_recorded":
            if channel not in NON_DIGITAL_CHANNELS:
                raise ValueError(
                    "Channel must be phone, in_person, paper, assisted_visit or representative."
                )
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
            "owner": neutral_text(_text(owner, "Human owner")),
            "next_update": date.fromisoformat(next_update).isoformat(),
            "accessible_route": ACCESSIBLE_ROUTE,
            "support_needed": support,
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
        clean_evidence = neutral_text(_text(evidence, "Outcome evidence"))
        rec["investigation"] = "outcome_recorded"
        rec["outcome"] = {
            "outcome": outcome,
            "basis": basis,
            "evidence": clean_evidence,
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
        cleaned_evidence: str | None = None
        if evidence is not None:
            if not isinstance(evidence, str):
                raise ValueError("Remedy evidence is required.")
            if evidence.strip():
                cleaned_evidence = neutral_text(evidence.strip())
        if status in ("completed", "not_needed"):
            if cleaned_evidence is None:
                _text(evidence, "Remedy evidence")
            if rec["investigation"] != "outcome_recorded":
                raise ValueError("Record an investigation outcome before completing a remedy.")
        rec["remedy"] = {"status": status, "evidence": cleaned_evidence}
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
        unknowns = [neutral_text(EVALUATOR_UNKNOWNS[1])]
        if baseline is None:
            unknowns.insert(0, neutral_text(EVALUATOR_UNKNOWNS[0]))
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
        questions = list(PACK_QUESTIONS)
        summary = None if ai_summary is None else neutral_text(_text(ai_summary, "AI summary"))
        task_entry = _registry_get(PACK_TASK) or {}
        pack: Record = {
            "id": f"PK-{len(self.packs) + 1:03d}",
            "task": PACK_TASK,
            "requirement": "FR-036",
            "kind": neutral_text(str(task_entry.get("kind", "proposal-pack"))),
            "state": neutral_text(str(task_entry.get("state", "disabled"))),
            "approval_state": neutral_text(str(task_entry.get("approval_state", "unapproved"))),
            "live_authorized": _authorizes_live(PACK_TASK, None),
            "requires_human_review": True,
            "concern_id": cid,
            "household_statement": rec["statement"],
            "recorded_facts": [neutral_text(f) for f in facts],
            "questions_for_investigator": [neutral_text(q) for q in questions],
            "ai_summary": summary,
            "source": "ai" if summary else "template",
            "approval": neutral_text(PACK_NOT_REVIEWED),
            "approved": False,
            "reviewer_function": rec["owner"],
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
        self._own(self._get(pack["concern_id"]), reviewer)
        if action not in PACK_ACTIONS:
            raise ValueError("Action must be accept or reject.")
        if pack["review"] is not None:
            raise ValueError("This pack has already been reviewed.")
        pack["review"] = {
            "by": reviewer.strip(),
            "action": action,
            "reason": neutral_text(_text(reason, "Reason")),
        }
        pack["approval"] = neutral_text(PACK_APPROVAL_LABELS[action])
        pack["approved"] = action == "accept"
        return deepcopy(pack)
