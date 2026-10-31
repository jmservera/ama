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
        r"(?:rats?(?: smell)?|pests?|smell(?: (?:of|like) (?:a )?dead rat)?|"
        r"odour|odor|noise|leak|repairs?|"
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
            rf"why {household} (?:is|are) {state}|"
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


def _natural_record_question(question: str) -> Topic | str:
    question = question.lower().strip().replace("\u2019", "'")
    if not re.fullmatch(r"[a-z]+(?:[ ']+[a-z]+)*[?.!]*", question):
        return "unknown"
    # Keep token order and consume one whole intent; keyword presence alone admits extra requests.
    sentence = " ".join(re.findall(r"[a-z]+", question))
    case = r"my (?:case|retrofit(?: case)?)"
    status = (
        rf"(?:how (?:is|s) {case} (?:going|doing|progressing)|"
        rf"is {case} (?:blocked|stuck|waiting|on hold)"
        r"(?: (?:on|for) (?:anything|something))?|"
        rf"(?:any|is there (?:any|an)|are there any) updates? (?:on|about|for) {case}|"
        rf"(?:what (?:is|s) (?:blocking|holding up|delaying) {case}|"
        rf"what (?:is|s) {case} waiting (?:on|for)|"
        rf"why is {case} (?:blocked|stuck|waiting|on hold))|"
        rf"where (?:is|s) {case}(?: (?:up to|at))?|"
        rf"where {case} is (?:up to|at))"
    )
    for topic, noun in (
        (Topic.DOCUMENTS, r"(?:documents?|paperwork)"),
        (Topic.FORMS, r"forms?"),
    ):
        record = rf"(?:(?:my|the) )?{noun}"
        intent = (
            rf"(?:(?:what|which) {record} (?:am i (?:still )?missing|"
            rf"(?:do you have|have you (?:got|received))(?: (?:from|for) me)?)|"
            rf"(?:do you have|have you (?:got|received)) my {noun}|"
            rf"(?:is|are) my {noun} (?:missing|received)|"
            rf"(?:has|have) my {noun} arrived|"
            rf"(?:what|which) {record} (?:are|is) (?:still )?missing(?: from {case})?"
            rf"|(?:what|which) {record} (?:do i|am i going to) need(?: for {case})?"
            + (
                rf"|(?:can i get |i need )?help (?:with|filling in|filling out) my {noun}"
                rf"|how (?:do|can|should) i (?:fill in|fill out|complete) {record}"
                if topic is Topic.FORMS
                else ""
            )
            + ")"
        )
        if re.fullmatch(intent, sentence):
            return topic
    if re.fullmatch(status, sentence):
        return Topic.STATUS
    if re.fullmatch(
        r"(?:where (?:is|s) my (?:home|house|flat)|"
        r"what (?:is|s) my (?:home )?address|"
        r"(?:what|which) address (?:do you have|have you got|is recorded)(?: for me)?|"
        r"what (?:do you know|is recorded) about my (?:home|house|flat))",
        sentence,
    ):
        return "home"
    return "unknown"


def _record_question(question: str) -> Topic | str:
    subject = (
        r"(?:(?:electric |electrical )?"
        r"(?:smoke alarm|smoke detector|co alarm|co detector|carbon[- ]monoxide detector)"
        r"(?:'s light)?|water meter|co-operative home|home|house|flat|sockets?|"
        r"(?:electric )?(?:water heater|heater)|boiler|heating)"
    )
    documents = (
        r"(?:(?:my|the) )?(?:(?:smoke alarm|smoke-free policy|carbon-monoxide detector) )?"
        r"(?:documents?|paperwork)"
    )
    forms = r"(?:(?:my|the) )?forms?"
    patterns = (
        (
            Topic.DOCUMENTS,
            rf"(?:{documents}|where (?:is|are) {documents}|can i see {documents}|"
            rf"when (?:is|are) {documents} coming|"
            rf"what documents cover (?:the |my )?{subject}|"
            rf"(?:what|which) {documents} (?:are missing(?: from my case)?|"
            r"do i (?:still )?need(?: to (?:provide|send|upload))?)|"
            r"there is a smoke alarm in my home; what documents do i need|"
            rf"how (?:do|can|should) i (?:provide|send|upload) {documents}|"
            rf"what is wrong with {documents}(?: warnings?(?: or errors?)?| errors?)?|"
            rf"what (?:does {documents} (?:warning(?: or error)?|error)|"
            rf"do {documents} (?:warnings(?: or errors)?|errors)) mean)",
        ),
        (
            Topic.STATUS,
            r"(?:(?:my )?(?:case|status|progress|case status|case progress)|"
            r"(?:my )?case update|"
            r"what is happening with my (?:case|retrofit)|"
            r"what's happening with my (?:case|retrofit)|"
            r"what is my (?:case )?(?:status|progress)|"
            rf"what is the (?:status|progress) of (?:my|the) {subject}|"
            rf"what is my {subject} status|how is my case progressing)",
        ),
        (
            Topic.FORMS,
            rf"(?:{forms}|what {forms} do i need|"
            rf"i need help filling {forms}(?: for (?:my|a) {subject})?|"
            rf"where are {forms}(?: for (?:my|a) {subject})?|"
            rf"how do i fill (?:in|out) {forms})",
        ),
        (
            "home",
            r"(?:my home|(?:what|which) (?:is|are) (?:my )?address|"
            r"(?:what|which) (?:is )?recorded about my home|"
            rf"(?:what|which) improvements are planned(?: for my {subject})?)",
        ),
    )
    for topic, pattern in patterns:
        if re.fullmatch(pattern + r"[?.!]*", question.lower().strip()):
            return topic
    return _natural_record_question(question)


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
    # Only remove a complete polite envelope; the remaining message must still match in full.
    question = question.lower().strip()
    polite = re.fullmatch(
        r"(?:please )?(?:(?:can|could|would) you (?:tell me|show me|explain|help me with) "
        r"(?:about )?|please )(.+?)(?: please)?[?.!]*",
        question,
    )
    if polite:
        question = polite[1]
    tokens = words(question)
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
    if tokens & {
        "law",
        "laws",
        "legal",
        "legally",
        "regulation",
        "regulations",
        "rules",
        "compliant",
        "duty",
    }:
        return "regulations"
    if tokens & {"consent", "consents", "permission"}:
        return "consents"
    if tokens & {"appointment", "appointments", "callback", "agenda", "slots"}:
        return "appointments"
    if repair:
        return "repair"
    return _record_question(question)


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
            'Try asking: "How is my case going?", "What documents am I missing?", '
            '"What forms do I need?" or "What is my address?" '
            "I cannot approve, decide, diagnose, give consent, book from chat text or "
            "access anyone else's record. A person can help through your housing officer."
        )
        sources = ("Assistant task limits",)
    return Advice(answer, sources, "Summary by rules - workflow only, no AI used", notice=notice)
