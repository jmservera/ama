"""Host-owned housing routes, protected replies and grounding for optional AI."""

import re
from typing import Any

from zava_forward.core.resident_assistant import NOTICE as ADVISORY_NOTICE
from zava_forward.core.resident_assistant import Advice, Topic

from .agenda import MANUAL, NOTICE

REGULATORY_SOURCE = (
    "docs/reference/regulatory/social-housing-regulation/"
    "social-housing-safety-and-quality-standard-2024.md; "
    "Safety and Quality Standard, sections 2.3.1, 2.3.2 and 2.3.3; "
    "regulatory standard; source date 2024-04-01; retrieved 2026-09-19."
    " Selected provisions checked against https://www.gov.uk/government/publications/"
    "safety-and-quality-standard on 2026-10-28."
)
REGULATORY_ANSWER = (
    "The local copy of the Safety and Quality Standard says providers must make it easy to "
    "report repairs, tell tenants repair timescales and keep tenants informed about work. "
    "This is an explanation of a dated local copy, not legal advice. "
    "These selected provisions match the official publication checked on 2026-10-28. "
    "Currentness has not been verified for the wider rules. "
    "Other rules or later changes may apply. "
    "I cannot decide that a legal duty is met, that your home is safe, or that a provider "
    "has complied. Ask your housing officer to arrange a qualified legal or compliance review."
)
SAFETY = (
    "Do not wait for chat or a callback if someone may be in danger. "
    "For an immediate emergency, call 999. Report damp, mould or another safety concern "
    "to your housing officer or emergency repairs service using your usual contact details. "
    "A person must handle safety reports. This chat has not sent a report or alerted anyone."
)


def words(question: str) -> set[str]:
    return set(re.findall(r"[a-z]+", question.lower()))


def _hazard_report(question: str, tokens: set[str]) -> bool:
    electrical = tokens & {
        "electric",
        "electrical",
        "electricity",
        "electrics",
        "power",
        "socket",
        "sockets",
        "outlet",
        "outlets",
        "plug",
        "plugs",
        "wiring",
        "wire",
        "wires",
        "cable",
        "cables",
        "light",
        "lights",
        "fuse",
        "fusebox",
        "charger",
        "appliance",
        "appliances",
    }
    active_alarm = tokens & {
        "sounding",
        "beeping",
        "beeps",
        "chirping",
        "ringing",
        "blaring",
        "alerting",
        "triggered",
        "activated",
    } or any(pair <= tokens for pair in ({"going", "off"}, {"gone", "off"}, {"won", "stop"}))
    detector = tokens & {"alarm", "alarms", "detector", "detectors"}
    present = {"there", "is"} <= tokens and not detector
    monoxide = {"carbon", "monoxide"} <= tokens or "co" in tokens
    return bool(
        (
            monoxide
            and (
                active_alarm
                or present
                or tokens
                & {"detected", "leak", "leaking", "poisoning", "poisoned", "exposed", "exposure"}
            )
        )
        or (
            "smoke" in tokens
            and (
                active_alarm
                or (electrical and not detector and not tokens & {"free", "policy"})
                or re.search(
                    r"\bsmoke\s+(?:is\s+)?(?:in|from|through|everywhere|coming|pouring|billowing)\b"
                    r"|\b(?:see|seeing|smell|smelling|with|of)\s+(?:thick\s+|some\s+)?smoke\b"
                    r"(?![-\s]+(?:alarm|detector|free))",
                    question,
                    re.IGNORECASE,
                )
            )
        )
        or (
            electrical
            and (
                tokens
                & {
                    "sparks",
                    "sparking",
                    "smoking",
                    "smouldering",
                    "smoldering",
                    "burning",
                    "shock",
                    "shocks",
                    "shocked",
                    "zapped",
                    "electrocuted",
                    "flood",
                    "flooded",
                    "flooding",
                    "wet",
                    "soaked",
                }
                or (
                    "water" in tokens
                    and (
                        tokens & {"leak", "leaking", "dripping", "pouring", "touching", "around"}
                        or ("coming" in tokens and tokens & {"through", "onto"})
                    )
                )
            )
        )
    )


def _repair_question(question: str) -> bool:
    household = (
        r"(?:my|our|the) (?:(?:electric|broken|leaking|noisy|dripping) )*"
        r"(?:(?:kitchen|bathroom|bedroom) )?"
        r"(?:home|house|flat|bungalow|kitchen|bathroom|bedroom|ceiling|roof|"
        r"boiler|heater|heating|radiator|tap|pipes|toilet)"
    )
    issue = (
        r"(?:a |an |some )?(?:(?:dead|strange|bad|unpleasant) )?"
        r"(?:rats?(?: smell)?|pests?|smell|odour|odor|noise|leak|repairs?|"
        r"broken heating|hot water problem)"
    )
    location = rf"(?:in|at|from|under|near) {household}"
    state = r"(?:not working|broken|leaking|dripping|(?:very |too |so )?(?:noisy|cold))"
    smell = rf"smells?(?: (?:strange|bad|unpleasant|awful|(?:like|of) {issue}))?"
    return bool(
        re.fullmatch(
            rf"(?:{household} (?:{smell}|(?:is|are) {state}|"
            rf"(?:isn't|aren't) working|has {issue}|has no hot water|"
            rf"needs (?:repairs?|improvements)(?: because of {issue})?)|"
            rf"there (?:is|are) {issue} {location}|"
            rf"i (?:can smell|smell|can hear|hear|have noticed) {issue} {location}|"
            rf"(?:why|how|when) (?:is|are) {household} {state}|"
            rf"(?:is|are) {household} {state}|"
            rf"when (?:will|does) {household} (?:work|start working)|"
            rf"when is hot water coming back (?:to|in) {household}|"
            rf"how (?:do|can|should) (?:i|we) report {issue} {location}|"
            rf"who (?:do|can|should) (?:i|we) contact about "
            rf"(?:{household}|{issue} {location}))"
            r"[?.!]*",
            question.lower().strip(),
        )
    )


def route(question: str) -> Topic | str:
    tokens = words(question)
    if tokens & {
        "danger",
        "unsafe",
        "hazard",
        "safety",
        "mould",
        "mold",
        "damp",
        "fire",
        "gas",
    } or _hazard_report(question, tokens):
        return "safety"
    if tokens & {
        "ignore",
        "instructions",
        "system",
        "prompt",
        "another",
        "other",
        "neighbour",
        "neighbor",
        "approve",
        "diagnose",
        "decide",
        "submit",
        "book",
        "cancel",
        "write",
        "poem",
        "joke",
        "story",
        "pretend",
        "roleplay",
        "translate",
        "generate",
        "execute",
        "override",
        "tell",
        "compose",
        "play",
        "output",
    }:
        return "unknown"
    repair = _repair_question(question)
    if (
        tokens
        & {
            "report",
            "contact",
            "notify",
            "email",
            "call",
            "arrange",
            "schedule",
            "fix",
        }
        and not repair
    ):
        return "unknown"
    if tokens & {"documents", "document", "paperwork"}:
        return Topic.DOCUMENTS
    if "send" in tokens:
        return "unknown"
    if tokens & {"law", "laws", "legal", "regulation", "regulations", "rules", "compliant", "duty"}:
        return "regulations"
    if tokens & {"appointment", "appointments", "callback", "agenda", "slots"}:
        return "appointments"
    if tokens & {"consent", "consents", "permission"}:
        return "consents"
    if re.fullmatch(
        r"(?:my home|(?:what|which) (?:is|are) (?:my )?address|"
        r"(?:what|which) (?:is )?recorded about my home|"
        r"(?:what|which) improvements are planned(?: for my [a-z ]+)?)[?.!]*",
        question.lower().strip(),
    ):
        return "home"
    if tokens & {"status", "case", "progress"}:
        return Topic.STATUS
    if tokens & {"form", "forms"}:
        return Topic.FORMS
    if repair:
        return "repair"
    return "unknown"


def answer(topic: str, view: dict[str, Any]) -> Advice:
    sources: tuple[str, ...]
    notice = ADVISORY_NOTICE
    if topic == "home":
        home = view["home"]
        answer = (
            "Your recorded home: "
            + ", ".join(home[k] for k in ("address", "town", "postcode") if home[k])
            + ". Planned improvements: "
            + (", ".join(view["measures"]) if view["measures"] else "not recorded")
            + "."
        )
        sources = ("Your signed-in home record and planned improvements",)
    elif topic == "repair":
        notice += (
            " Chat cannot confirm the cause of a repair problem or assess safety. "
            "This chat has not sent a report or alerted anyone."
        )
        answer = (
            "I cannot confirm the cause of the problem from chat or tell you that your home "
            "is safe. Contact your housing officer using your usual contact details. "
            "Explain what you have noticed, where it is and when it started. "
            "Ask how to report a repair and what happens next. "
            "This chat has not sent a report or alerted anyone. "
            "If someone may be in immediate danger, do not wait for chat; call 999."
        )
        sources = ("General repair-reporting guidance, not a diagnosis or repair history",)
    elif topic == "consents":
        answer = (
            "Works consent is not available in this showcase. I cannot say whether you have "
            "given consent. Agreeing to use your record in chat is not consent to works. "
            "Ask your housing officer to check your consent record."
        )
        sources = ("Showcase limit: operational consent records are not available",)
    elif topic == "appointments":
        answer = (
            NOTICE + " Use Find callback times below to search the local agenda. "
            "You choose a time and confirm before anything is reserved. " + MANUAL
        )
        sources = ("Local synthetic callback agenda, not operational appointment history",)
    elif topic == "regulations":
        answer, sources = REGULATORY_ANSWER, (REGULATORY_SOURCE,)
    elif topic == "safety":
        answer, sources = SAFETY, ("Human emergency and repairs route, not a safety assessment",)
    else:
        answer = (
            "I cannot answer that or act on instructions in a message. "
            "Ask about your case, home, documents, forms, consent, appointments or rules. "
            "I cannot approve, decide, diagnose, give consent, book from chat text or "
            "access anyone else's record. A person can help through your housing officer."
        )
        sources = ("Assistant task limits",)
    return Advice(answer, sources, "Summary by rules - workflow only, no AI used", notice=notice)
