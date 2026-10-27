"""Own-case advisory answers with a deliberately fact-free provider boundary."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

NOTICE = (
    "Advisory only. This assistant cannot submit forms, give consent, book works or make decisions."
)
HUMAN_HELP = "Speak to your housing officer, or write to or visit your local office."


class Topic(StrEnum):
    STATUS = "status"
    DOCUMENTS = "documents"
    FORMS = "forms"


class AssistantUnavailable(Exception):
    """Expected provider failure; no provider details are safe for the resident."""


class Provider(Protocol):
    ai: bool

    def select(self, topic: Topic) -> Topic: ...


class FakeProvider:
    """Deterministic local provider. Never makes model or network calls."""

    ai = False

    def select(self, topic: Topic) -> Topic:
        return topic


@dataclass(frozen=True)
class CaseProgress:
    progress: str
    next_step: str
    closed: str = ""


@dataclass(frozen=True)
class Advice:
    answer: str
    sources: tuple[str, ...]
    label: str
    notice: str = NOTICE
    help: str = HUMAN_HELP


class Advisor(Protocol):
    def answer(self, topic: Topic, case: CaseProgress, resident: str) -> Advice: ...


def guidance(topic: Topic, case: CaseProgress) -> dict[str, str]:
    """Optional explanations contain no inferred case facts or specialist advice."""
    if topic is Topic.STATUS:
        return {
            "contact": "Ask your housing officer if you need more detail about this update.",
            "closed": "Ask your housing officer what a closed record means for your question.",
            "unknown": "Your housing officer can check information that is missing from this view.",
        }
    if topic is Topic.DOCUMENTS:
        return {
            "confirm": "Before sending anything, ask which document and which pages are needed.",
            "privacy": "Ask your housing officer how to send a document securely.",
        }
    return {
        "explain": (
            "Ask your housing officer to explain any words on the form you do not understand."
        ),
        "check": "Read your answers again before you choose whether to send the form.",
    }


def advise(topic: Topic, case: CaseProgress, provider: Provider) -> Advice:
    """Only locally owned text renders; a provider cannot add facts or change the task."""
    if not isinstance(topic, Topic):
        raise ValueError("Choose one of the listed questions.")
    if provider.select(topic) is not topic:
        raise AssistantUnavailable("invalid_selection")
    sources: tuple[str, ...]
    if topic is Topic.STATUS:
        answer = " ".join(part for part in (case.progress, case.closed, case.next_step) if part)
        sources = ("Your case: Where things are", "Your case: What happens next")
    elif topic is Topic.DOCUMENTS:
        answer = (
            "This showcase does not show which documents have been requested for your case. "
            "It cannot tell you what to send. Ask your housing officer to confirm the documents "
            "and a safe way to send them. Do not send passwords or bank details here."
        )
        sources = ("Showcase limit: requested documents are not available",)
    else:
        answer = (
            "Read each question on your form. Use details you know are correct. "
            "Do not guess if you are unsure. Ask your housing officer to explain the question "
            "or help you complete the form. Check your answers before you decide whether to "
            "send it yourself. This assistant cannot fill in or send the form for you."
        )
        sources = ("General form guidance, not a check of your form",)
    return Advice(
        answer, sources, "AI suggestion, not approved" if provider.ai else "Summary by rules"
    )
