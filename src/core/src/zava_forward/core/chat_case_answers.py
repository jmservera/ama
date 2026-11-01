"""Rules-only, case-grounded answers for the stateless employee chat.

Reads only the case card already projected for the signed-in user. No model call, nothing
stored, no record changed. Each reply cites the recorded facts it used.
"""

import re
from collections.abc import Callable, Mapping
from functools import partial
from typing import Any

VALUE_LIMIT = 240
MAX_CITATIONS = 20
TRUNCATED = "Further recorded detail is not shown here. Open the case card to see all of it."
FUNDING_DOCUMENTS = ("EPC", "Survey", "Design", "Funding evidence")
OTHER_CASE = re.compile(r"\bZF-\d+\b", re.I)
CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")

INTENTS: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (name, re.compile(pattern, re.I))
    for name, pattern in (
        ("funding", r"\b(fund\w*|grants?|claims?|money|financ\w*|budget|invoic\w*|paid)\b"),
        (
            "blocked",
            r"\b(block\w*|stuck|stall\w*|paus\w*|stop\w*|held\s+up|delay\w*|"
            r"why|not\s+moving|reason|problem|hazard\w*)\b",
        ),
        (
            "missing",
            r"\b(missing|outstanding|lack\w*|incomplete|need\w*|require\w*|"
            r"evidence|documents?|checklist|what\s+is\s+left)\b",
        ),
        (
            "next",
            r"\b(next|what\s+now|what\s+should|do\s+now|action|happens?\s+now|move\s+(it\s+)?on)\b",
        ),
        ("owner", r"\b(who|owner\w*|owns?|responsible|assigned|in\s+charge)\b"),
        (
            "status",
            r"\b(status|stage|where|progress|update|state|how\s+is|how\s+far|going\s+on)\b",
        ),
    )
)

SUGGESTIONS = (
    "Why is this case blocked?",
    "Why is funding not started yet?",
    "What is the next step and who owns it?",
    "What is missing on this case?",
    "What is the status of this case?",
)


def _text(value: Any) -> str:
    return CONTROL.sub(" ", str(value))[:VALUE_LIMIT].strip()


def _rows(value: Any) -> list[Mapping[str, Any]]:
    return [row for row in value if isinstance(row, Mapping)] if isinstance(value, list) else []


def case_facts(detail: Mapping[str, Any], *, reason_visible: bool) -> dict[str, str]:
    """Recorded facts from the user's own projected case card, keyed by field path."""
    facts: dict[str, str] = {}

    def put(path: str, value: Any) -> None:
        if value not in (None, "", [], {}):
            facts[path] = _text(value)

    for key in ("stage", "status", "owner", "waiting_on", "days_in_stage"):
        put(key, detail.get(key))
    if reason_visible:
        put("reason", detail.get("reason"))
    funding = detail.get("funding")
    if isinstance(funding, Mapping):
        for key in ("status", "route", "reference"):
            put(f"funding.{key}", funding.get(key))
    if "funding_ok" in detail:
        put("funding_ok", "confirmed" if detail["funding_ok"] else "not confirmed")
    put("closed", "yes" if detail.get("closed") else None)
    work = detail.get("work")
    if isinstance(work, Mapping):
        for key in ("reason", "next_action", "owner", "source", "recorded_at"):
            put(f"work.{key}", work.get(key))
        for i, row in enumerate(_rows(work.get("blockers"))[:6]):
            for key in ("step", "reason", "owner", "responsible_role", "next_action", "source"):
                put(f"work.blockers.{i}.{key}", row.get(key))
            put(f"work.blockers.{i}.current_stop", "yes" if row.get("current_stop") else None)
    for i, line in enumerate(detail.get("gate") or []):
        if isinstance(line, str):
            put(f"gate.{i}", line)
    for i, row in enumerate([h for h in _rows(detail.get("hazards")) if not h.get("released")][:4]):
        for key in ("category", "owner", "state"):
            put(f"hazards.{i}.{key}", row.get(key))
    for i, item in enumerate(_rows(detail.get("checklist"))):
        if not item.get("present"):
            put(f"checklist.{i}.missing", item.get("kind"))
    for i, item in enumerate(detail.get("technical_missing") or []):
        put(f"technical_missing.{i}", item if isinstance(item, str) else item.get("item"))
    kinds = sorted({str(d.get("kind")) for d in _rows(detail.get("documents")) if d.get("kind")})
    put("documents", ", ".join(kinds) if kinds else "none recorded")
    return facts


def intent(question: str) -> str | None:
    for name, pattern in INTENTS:
        if pattern.search(question):
            return name
    return None


class Reply:
    """Answer sentences with the fact ids that support them."""

    def __init__(self, case_id: str, facts: Mapping[str, str]) -> None:
        self.case_id, self.facts = case_id, facts
        self.lines: list[str] = []
        self.cites: list[str] = []
        self.groups: list[tuple[str, list[str]]] = []
        self._seen = 0
        self._capture: list[str] | None = None

    def fact(self, path: str) -> str:
        if path in self.facts:
            cite = f"{self.case_id}/{path}"
            if self._capture is not None:
                if cite not in self._capture:
                    self._capture.append(cite)
            elif cite not in self.cites:
                self.cites.append(cite)
        return self.facts.get(path, "")

    def say(self, line: str, cites: list[str] | None = None) -> None:
        self.lines.append(line)
        if cites is None:
            cites = self.cites[self._seen :]
        else:
            self.cites.extend(c for c in cites if c not in self.cites)
        self.groups.append((line, cites))
        self._seen = len(self.cites)

    def cited(self, build: Callable[[], str]) -> tuple[str, list[str]]:
        """Run build and return its text with only the facts it used."""
        self._capture = []
        try:
            return build(), self._capture
        finally:
            self._capture = None

    def render(self) -> tuple[str, list[str]]:
        """Text and citations bounded together so every shown line keeps its support."""
        lines: list[str] = []
        cites: list[str] = []
        for line, new in self.groups:
            fresh = [c for c in new if c not in cites]
            if len(cites) + len(fresh) > MAX_CITATIONS:
                lines.append(TRUNCATED)
                return "\n".join(lines), cites
            lines.append(line)
            cites.extend(fresh)
        for cite in self.cites[self._seen :]:
            if cite not in cites and len(cites) < MAX_CITATIONS:
                cites.append(cite)
        return "\n".join(lines), cites

    def text(self) -> str:
        return "\n".join(self.lines)


def _indexes(facts: Mapping[str, str], prefix: str) -> list[int]:
    found = {int(m.group(1)) for k in facts if (m := re.match(rf"{re.escape(prefix)}\.(\d+)\.", k))}
    return sorted(found)


def _who_to_ask(r: Reply) -> str:
    owner = r.fact("owner") or r.fact("work.owner")
    return f"Ask {owner}, who owns this case." if owner else "Ask the person who owns this case."


def _blocker_owner(r: Reply, i: int) -> str:
    p = f"work.blockers.{i}"
    owner = r.fact(f"{p}.owner")
    if owner and owner.casefold() != "unknown":
        return owner
    reason = r.facts.get(f"{p}.reason", "")
    embedded = re.search(r"\bOwner:\s*(.+?)(?=\s*(?:\.\s+)?Next action:|$)", reason)
    if embedded and embedded.group(1).strip().casefold() != "unknown":
        r.fact(f"{p}.reason")
        return embedded.group(1).strip().rstrip(".")
    role = r.fact(f"{p}.responsible_role")
    return f"{role} (role)" if role else ""


def _blocker_line(r: Reply, i: int) -> str:
    p = f"work.blockers.{i}"
    step, reason = r.fact(f"{p}.step"), re.split(r"\s+Owner:", r.fact(f"{p}.reason"))[0]
    owner, nxt, src = _blocker_owner(r, i), r.fact(f"{p}.next_action"), r.fact(f"{p}.source")
    parts = [f"{step}: {reason}" if step and reason else (reason or step)]
    parts.append(f"Owner: {owner}." if owner else "No owner is recorded for this.")
    parts.append(f"Next step: {nxt}" if nxt else "No next step is recorded for it.")
    if src:
        parts.append(f"Recorded source: {src}.")
    return " ".join(p if p.endswith((".", "?")) else p + "." for p in parts if p)


def _blocked(r: Reply) -> None:
    status = r.fact("status")
    if r.fact("closed"):
        r.say("This case is closed, so nothing is blocking it.")
        return
    blockers = _indexes(r.facts, "work.blockers")
    if status:
        r.say(f"Recorded status: {status}.")
    if blockers:
        stops = [i for i in blockers if r.facts.get(f"work.blockers.{i}.current_stop") == "yes"]
        later = [i for i in blockers if i not in stops]
        if stops:
            r.say("What is recorded as stopping this case now, most important first:")
            for n, i in enumerate(stops, 1):
                r.say(f"{n}. {_blocker_line(r, i)}")
        else:
            reason = r.fact("work.reason") or r.fact("reason")
            if reason:
                r.say(f"Recorded reason: {reason}")
            waiting = r.fact("waiting_on")
            if waiting:
                r.say(f"Waiting on: {waiting}.")
            if not (reason or waiting):
                r.say("Nothing is recorded as stopping this case in its current stage.")
        if later:
            r.say("Still needed before a later step, but not stopping the case now:")
            for n, i in enumerate(later, 1):
                r.say(f"{n}. {_blocker_line(r, i)}")
        return
    gates = [r.fact(f"gate.{i}") for i in range(8) if f"gate.{i}" in r.facts]
    if gates:
        r.say("Recorded reasons: " + " ".join(gates))
        return
    reason = r.fact("work.reason") or r.fact("reason")
    if status == "Ready":
        r.say("No blocker is recorded. The case shows Ready for the next step.")
    elif reason:
        r.say(f"Recorded reason: {reason}")
        waiting = r.fact("waiting_on")
        if waiting:
            r.say(f"Waiting on: {waiting}.")
    else:
        r.say("The case record does not say why this case is stopped. " + _who_to_ask(r))


def _funding_missing(r: Reply) -> list[tuple[str, list[str]]]:
    missing: list[tuple[str, list[str]]] = []
    blockers = [
        i
        for i in _indexes(r.facts, "work.blockers")
        if "funding" in r.facts.get(f"work.blockers.{i}.source", "").casefold()
        or "funding" in r.facts.get(f"work.blockers.{i}.step", "").casefold()
    ]
    if r.facts.get("funding_ok") == "not confirmed" and not blockers:
        missing.append(
            r.cited(
                partial(
                    _fact_line, r, "funding_ok", "Funding has not been confirmed on the record."
                )
            )
        )
    docs = r.facts.get("documents", "none recorded")
    recorded = {d.strip() for d in docs.split(",")}
    absent = [kind for kind in FUNDING_DOCUMENTS if kind not in recorded]
    cites: list[str] = []
    for k in sorted(r.facts):
        kind = r.facts[k]
        if k.endswith(".missing") and k.startswith("checklist.") and kind not in absent:
            _, used = r.cited(partial(r.fact, k))
            cites.extend(used)
            absent.append(kind)
    if absent:
        _, used = r.cited(partial(r.fact, "documents"))
        missing.append(("No recorded document for: " + ", ".join(absent) + ".", cites + used))
    missing.extend(r.cited(partial(_blocker_line, r, i)) for i in blockers)
    return missing


def _funding(r: Reply) -> None:
    status, route, ref = (
        r.fact("funding.status"),
        r.fact("funding.route"),
        r.fact("funding.reference"),
    )
    if status:
        r.say(
            f"Recorded funding status: {status}. Route: {route or 'not recorded'}. "
            f"Reference: {ref or 'none recorded'}."
        )
    else:
        r.say("No funding status is recorded for this case.")
    if not status or status.casefold() == "not started":
        r.say("The record gives no reason why funding has not started. " + _who_to_ask(r))
    missing = _funding_missing(r)
    if missing:
        r.say("What is missing:")
        for line, cites in missing:
            r.say(f"* {line}", cites)
    r.say("A person confirms funding. This chat cannot start, approve or record it.")


def _fact_line(r: Reply, path: str, template: str) -> str:
    return r.fact(path) and template.format(r.fact(path))


def _missing(r: Reply) -> None:
    items = [(f"gate.{i}", "{}") for i in range(8) if f"gate.{i}" in r.facts]
    items += [(k, "{} is not on the checklist.") for k in sorted(r.facts) if k.endswith(".missing")]
    items += [(k, "{}") for k in sorted(r.facts) if k.startswith("technical_missing.")]
    if items:
        r.say("Recorded as missing or still open:")
        for path, template in items:
            line, cites = r.cited(partial(_fact_line, r, path, template))
            r.say(f"* {line}", cites)
    else:
        r.say("No missing item is recorded on this case card.")
    r.say("Items not shown on the card are not known to this chat. " + _who_to_ask(r))


def _next(r: Reply) -> None:
    nxt, src = r.fact("work.next_action"), r.fact("work.source")
    owner = ""
    if nxt:
        indexes = _indexes(r.facts, "work.blockers")
        chosen = next(
            (i for i in indexes if r.facts.get(f"work.blockers.{i}.next_action") == nxt), None
        )
        if chosen is None:
            chosen = next(
                (i for i in indexes if r.facts.get(f"work.blockers.{i}.current_stop") == "yes"),
                None,
            )
        if chosen is not None:
            owner = _blocker_owner(r, chosen)
    owner = owner or r.fact("work.owner") or r.fact("owner")
    if nxt:
        r.say(f"Recorded next step: {nxt}")
        r.say(f"Owner: {owner}." if owner else "No owner is recorded for it.")
        if src:
            r.say(f"Recorded source: {src}.")
    else:
        r.say("No next step is recorded for this case. " + _who_to_ask(r))


def _owner(r: Reply) -> None:
    owner, waiting = r.fact("owner"), r.fact("waiting_on")
    if owner:
        r.say(f"Case owner: {owner}.")
    if waiting:
        r.say(f"Waiting on: {waiting}.")
    if not (owner or waiting):
        r.say("No owner is recorded for this case. Ask your team lead who should own it.")


def _status(r: Reply) -> None:
    for label, path in (("Stage", "stage"), ("Status", "status"), ("Owner", "owner")):
        value = r.fact(path)
        if value:
            r.say(f"{label}: {value}.")
    days = r.fact("days_in_stage")
    if days:
        r.say(f"Days in this stage: {days}.")


ANSWERS = {
    "funding": _funding,
    "blocked": _blocked,
    "missing": _missing,
    "next": _next,
    "owner": _owner,
    "status": _status,
}


def suggestions_text(case_id: str) -> str:
    lines = [f"* {s}" for s in SUGGESTIONS]
    head = (
        f"I could not match that to a fact on case {case_id}. I can answer questions like these:"
        if case_id
        else "Open a case first. Then I can answer questions about that case, like these:"
    )
    return "\n".join([head, *lines])


def answer(case_id: str, question: str, facts: Mapping[str, str]) -> tuple[str, str, list[str]]:
    """Kind (answer or fallback), reply text and the fact ids cited."""
    if not case_id:
        return "fallback", suggestions_text(""), []
    other = {m.group(0).upper() for m in OTHER_CASE.finditer(question)} - {case_id.upper()}
    if other:
        named = ", ".join(sorted(other))
        return (
            "fallback",
            f"This chat is on case {case_id} and can only use that case. Open {named} "
            "from the case list to ask about it.",
            [],
        )
    name = intent(question)
    r = Reply(case_id, facts)
    if name is None:
        r.fact("stage")
        r.fact("status")
        return "fallback", suggestions_text(case_id), r.render()[1]
    ANSWERS[name](r)
    text, cites = r.render()
    return "answer", text, cites
