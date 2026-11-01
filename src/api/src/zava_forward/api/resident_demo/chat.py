"""Host-owned housing routes, protected replies and grounding for optional AI."""

import re
from dataclasses import replace
from typing import Any

from zava_forward.core.resident_assistant import NOTICE as ADVISORY_NOTICE
from zava_forward.core.resident_assistant import Advice, Topic
from zava_forward.core.resident_preview import STAGE_TEXT

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
        (Topic.DOCUMENTS, r"(?:documents?|docs?|papers|paperwork)"),
        (Topic.FORMS, r"(?:forms?|paper forms?)"),
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
        r"(?:what (?:else )?do you (?:still )?need from me|"
        r"what (?:else )?(?:do|should) i (?:still )?(?:need to )?"
        r"(?:send|provide|give|upload|hand in)(?: you)?|"
        r"what (?:is|s) (?:still )?(?:outstanding|needed)(?: from me)?(?: (?:on|for) my case)?|"
        r"is there anything (?:else )?(?:you|i) need(?: from me| to send)?)",
        sentence,
    ):
        return Topic.DOCUMENTS
    if re.fullmatch(
        r"(?:what (?:is|s) (?:happening|going on) with my (?:case|retrofit)|"
        r"what (?:happens|is) next(?: for my (?:case|retrofit))?|"
        r"what (?:is|s) the next step(?: for my (?:case|retrofit))?|"
        r"what stage is my (?:case|retrofit) (?:at|in)|"
        r"has anything changed(?: (?:on|with) my (?:case|retrofit))?|"
        r"any news(?: (?:on|about) my (?:case|retrofit))?)",
        sentence,
    ):
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
        r"(?:documents?|docs?|paperwork)"
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


BLOCKED_WORDS = frozenset(
    {
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
    }
)
ACTION_WORDS = frozenset(
    {"report", "contact", "notify", "email", "call", "arrange", "schedule", "fix"}
)
# Harmless-looking words that still ask the chat to act, impersonate or reach other records.
BOUNDARY_WORDS = frozenset(
    {
        "forget",
        "disregard",
        "bypass",
        "jailbreak",
        "reveal",
        "developer",
        "admin",
        "sudo",
        "sign",
        "agree",
        "accept",
        "confirm",
        "authorise",
        "authorize",
        "reschedule",
        "change",
        "delete",
        "withdraw",
        "send",
        "forward",
        "share",
        "his",
        "her",
        "hers",
        "their",
        "theirs",
        "him",
        "them",
        "someone",
        "somebody",
        "anyone",
        "anybody",
        "everyone",
        "everybody",
        "resident",
        "residents",
        "tenant",
        "tenants",
        "customer",
        "customers",
        "neighbours",
        "neighbors",
        "choose",
        "pick",
        "reserve",
        "approved",
        "colleague",
        "colleagues",
        "mr",
        "mrs",
        "ms",
        "miss",
        "dr",
        "all",
        "every",
    }
)
RECORD_WORDS = frozenset(
    "case cases record records file files account accounts address addresses home homes".split()
)
FIRST_PERSON = frozenset({"my", "me", "i", "our", "we", "mine"})
QUESTION_WORDS = frozenset(
    "what whats why how when where who which is are am can could do does did will would should "
    "have has may".split()
)
OTHER_PERSON = re.compile(
    r"\b(?!(?:what|how|where|there|it|that|who|let|here|when|why|she|he)['\u2019]s\b)"
    r"[a-z]+['\u2019]s\b|\b(?:act as|you are now|as an? (?:admin|developer))\b"
)

PAUSE_OBJECT = (
    r"(?:it|this|that|the pause|the block|the lock|the freeze|my case|my retrofit|the case|"
    r"contact|my contact|the contact|the contact pause|the pause on (?:my case|contact)|"
    r"the block on my case|the pause on my case)"
)
_STRONG = r"(?:un ?pause|unlock|unblock|unfreeze|unstick|restart|re-?start|resume|reopen)"
_WEAK = r"(?:lift|remove|end|clear|undo)"
_ASKER = (
    r"(?:(?:can|could|may|will|would) (?:i|we|you|someone|somebody|anyone|a person)"
    r"|how (?:do|can|could|should|would) (?:i|we)|how to|"
    r"(?:i|we) (?:want|need|would like|'d like) to|i want you to|i'd like to)"
)
_AFTER = r"(?: (?:again|now|myself))?"
_REACH = (
    r"(?:contact|ask|call|speak to|talk to|write to|go to|visit|get in touch with|email|"
    r"phone|reach)"
)
_ABOUT = r"(?: (?:about (?:this|it|that|the pause|my case|the block)|for help|first|instead))?"
_PAUSED = r"(?:paused|locked|frozen|stopped|blocked|stuck|on hold)"
PAUSE_INTENTS = (
    rf"(?:{_ASKER} )?{_STRONG}(?: {PAUSE_OBJECT})?{_AFTER}",
    rf"(?:{_ASKER} )?{_WEAK} (?:the )?(?:pause|block|lock|freeze|hold)(?: on (?:my case|contact))?"
    rf"{_AFTER}",
    rf"(?:{_ASKER} )?{_WEAK} (?:it|this|that){_AFTER}",
    rf"what (?:do|should|can) (?:i|we) do to {_STRONG} {PAUSE_OBJECT}",
    r"(?:when|how long until) (?:will|can|do|does|is) "
    r"(?:contact|you|we|someone|the pause|it|my case)"
    r"(?: be)? (?:restart(?:ed)?|resum(?:e|ed)|start|lifted|un ?paused|unblocked|unlocked|"
    r"contact me)(?: again)?(?: for me)?",
    rf"(?:why|how come) (?:is|has|was) (?:contact|it|everything)(?: been)? {_PAUSED}",
    r"(?:why|how come) (?:is|has|was) my (?:case|contact|retrofit)(?: been)? "
    r"(?:paused|locked|frozen|stopped)",
    r"(?:is|has) (?:my case|contact|my contact|it)(?: been)? (?:paused|locked|frozen|stopped)",
    r"(?:why|how come) (?:have|has|did|are) (?:you|we|they|zava|nobody|no one) "
    r"(?:stopped?|not)(?: (?:contacting|calling|writing to))? me",
)
CONTACT_INTENTS = (
    rf"(?:who|which person|which team|which office|where) (?:should|can|do|could|must|would) "
    rf"(?:i|we) {_REACH}{_ABOUT}",
    r"how (?:do|can|could|should) (?:i|we) (?:contact|reach|get in touch with|speak to|talk to) "
    r"(?:my housing officer|my officer|the housing officer|my local office|the local office|"
    r"someone|a person|you|the team|the office|them)",
    r"(?:who is|what is the name of|what is the (?:phone )?number for|where is) "
    r"(?:my )?(?:housing officer|local office|officer)",
)


def _pause_question(question: str) -> str | None:
    """Return "pause" or "contact" only when every sentence is a whole pause or contact intent."""
    if re.search(r"\d", question):
        return None
    text = re.sub(r"[^a-z' \-.?!;,]", " ", question.lower().replace("\u2019", "'"))
    text = re.sub(r"\b(?:please|pls|thanks|thank you)\b", " ", text)
    parts = [
        " ".join(p.split()) for p in re.split(r"[.?!;,]+|\b(?:and|then|or)\b", text) if p.strip()
    ]
    if not parts or len(parts) > 3:
        return None
    pause = False
    for part in parts:
        if any(re.fullmatch(pattern, part) for pattern in PAUSE_INTENTS):
            pause = True
        elif not any(re.fullmatch(pattern, part) for pattern in CONTACT_INTENTS):
            return None
    return "pause" if pause else "contact"


# A resident asking how to send a document is not asking chat to send anything.
HOW_TO_VERBS = frozenset({"send", "share", "forward"})
DOCUMENT_HOW_TO = re.compile(
    r"(?:where|how)\s+(?:do|can|should)\s+i\s+(?:send|share|forward|upload)\s+my\s+[a-z ]{1,40}\??"
)


POLITE_ENVELOPE = re.compile(
    r"(?:please )?(?:(?:can|could|would) you (?:tell me|show me|explain|help me with) "
    r"(?:about )?|please )(.+?)(?: please)?[?.!]*"
)


def _strip_polite(question: str) -> str:
    """Remove a complete polite envelope; shared by routing and refusal classification."""
    text = question.lower().strip()
    polite = POLITE_ENVELOPE.fullmatch(text)
    return polite[1] if polite else text


def is_refusal(question: str) -> bool:
    """True for instruction injection and anything beyond the advisory boundary."""
    question = _strip_polite(question)
    tokens = words(question)
    blocked = BLOCKED_WORDS | ACTION_WORDS | BOUNDARY_WORDS
    if DOCUMENT_HOW_TO.fullmatch(question.strip().lower()):
        blocked -= HOW_TO_VERBS
    if tokens & blocked or OTHER_PERSON.search(question.lower()):
        return True
    # Digits point at a case id or slot; record nouns without "my" point at someone else's record.
    if re.search(r"\d", question) or (tokens & RECORD_WORDS and not tokens & FIRST_PERSON):
        return True
    # Every part must read as a question or a short topic phrase, so a trailing command is refused.
    keywords = frozenset().union(*(item[2] for item in TOPIC_EXAMPLES))
    joined = re.sub(r"(?<=\w)\.(?=\w)", "", question.lower())
    for part in re.split(r"[.?!;\n\r]+", joined):
        part_words = re.findall(r"[a-z]+", part)
        if part_words and not (
            part_words[0] in QUESTION_WORDS or (len(part_words) <= 4 and set(part_words) & keywords)
        ):
            return True
    return False


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
    question = _strip_polite(question)
    tokens = words(question)
    pause = _pause_question(question)
    if tokens & BLOCKED_WORDS and not pause:
        return "unknown"
    repair = _repair_question(question)
    if pause and not repair:
        return pause
    if tokens & ACTION_WORDS and not repair:
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


PAUSED_PROGRESS = STAGE_TEXT["Contact paused"][0]
PAUSE_NOTE = (
    "Chat cannot lift a pause, restart contact or change your case. Only a person can do that. "
    "Speak to your housing officer, or write to or visit your local Zava North Homes office, "
    "and ask them to lift the pause if you want contact to restart. That is your choice. "
    "This showcase has no phone numbers or addresses recorded, so use your usual contact "
    "details. This chat has not sent a request or told anyone."
)
CONTACT_NOTE = (
    "Speak to your housing officer using your usual contact details, or write to or visit your "
    "local Zava North Homes office. This showcase has no names, phone numbers or addresses "
    "recorded for them, so I cannot give any. Chat cannot contact anyone for you. "
    "This chat has not sent a request or told anyone."
)
TOPIC_EXAMPLES: tuple[tuple[str, str, frozenset[str]], ...] = (
    (
        "status",
        "How is my case going?",
        frozenset("case status progress update going happening next stage step wait news".split()),
    ),
    (
        "documents",
        "What documents am I missing?",
        frozenset(
            "document documents doc docs paper papers paperwork upload send missing proof".split()
        ),
    ),
    ("forms", "What forms do I need?", frozenset("form forms fill complete filling".split())),
    (
        "home",
        "What is my address?",
        frozenset("home house flat address property improvements measures works".split()),
    ),
    (
        "pause",
        "Can I unpause my case?",
        frozenset("pause paused unpause block blocked stuck lock unlock restart resume".split()),
    ),
    (
        "appointments",
        "Can I find a callback time?",
        frozenset("appointment appointments callback visit time slot slots".split()),
    ),
)


def _is_paused(view: dict[str, Any]) -> bool:
    return bool(view.get("progress") == PAUSED_PROGRESS)


def suggestions(question: str) -> list[str]:
    """Up to three example questions closest to the words used; defaults to the common three."""
    tokens = words(question)
    ranked = sorted(
        (item for item in TOPIC_EXAMPLES if tokens & item[2]),
        key=lambda item: -len(tokens & item[2]),
    )
    chosen = [item[1] for item in ranked[:3]]
    for item in TOPIC_EXAMPLES[:3]:
        if len(chosen) < 3 and item[1] not in chosen:
            chosen.append(item[1])
    return chosen


def outcome(question: str, topic: Topic | str) -> str:
    """Learning label: the routed topic, or refused/unrouted when no topic answered."""
    if topic == "unknown":
        return "refused" if is_refusal(question) else "unrouted"
    return str(topic.value if isinstance(topic, Topic) else topic)


def with_pause_note(advice: Advice, topic: Topic | str, view: dict[str, Any]) -> Advice:
    """A paused case also says who can lift the pause; only the host adds this fixed text."""
    if topic is Topic.STATUS and _is_paused(view):
        return replace(advice, answer=f"{advice.answer} {PAUSE_NOTE}")
    return advice


def answer(topic: str, view: dict[str, Any], question: str = "") -> Advice:
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
    elif topic == "pause":
        current = " ".join(p for p in (view.get("progress"), view.get("next_step")) if p)
        if _is_paused(view):
            head = f"Your record shows: {view['progress']} "
        else:
            head = (
                "Your record does not show that contact is paused, so I cannot say what is "
                "stopping your case. " + (current + " " if current else "")
            )
        answer = head + PAUSE_NOTE
        sources = ("Your case: Where things are", "Housing officer and local office route")
    elif topic == "contact":
        answer = CONTACT_NOTE
        sources = ("Housing officer and local office route",)
    elif topic == "regulations":
        answer, sources = REGULATORY_ANSWER, (REGULATORY_SOURCE,)
    elif topic == "safety":
        answer, sources = SAFETY, ("Human emergency and repairs route, not a safety assessment",)
    elif question and not is_refusal(question):
        answer = (
            "I cannot answer that. Closest topics: "
            + ", ".join(f'"{example}"' for example in suggestions(question))
            + ". You can ask one of these in the box. "
            "Speak to your housing officer, or write to or visit your local office, for "
            "anything else. I cannot approve, decide, diagnose, give consent, book from chat "
            "text or access anyone else's record."
        )
        sources = ("Assistant task limits",)
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
