"""Optional Azure topic-selector adapter. No runtime auto-enablement or credential discovery."""

import json
import re
import time
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime

from zava_forward.core.resident_assistant import AssistantUnavailable, Topic

EXPIRES = datetime(2026, 11, 1, tzinfo=UTC).timestamp()
MAX_REPLY = 4096
MAX_PROMPT_BYTES = 512
MAX_OUTPUT_TOKENS = 16
TIMEOUT_SECONDS = 5


@dataclass(frozen=True)
class RequestEnvelope:
    """Host reserves the tariff's conservative cost for this exact bounded request."""

    prompt: str
    max_output_tokens: int = MAX_OUTPUT_TOKENS


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: object,
        code: int,
        msg: str,
        headers: object,
        newurl: str,
    ) -> None:
        return None


def _post(url: str, payload: bytes, token: str) -> bytes:
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.build_opener(_NoRedirect()).open(
        request, timeout=TIMEOUT_SECONDS
    ) as response:
        body: bytes = response.read(MAX_REPLY + 1)
        return body


class AzureTopicProvider:
    """Disabled by default, requiring explicit host-supplied identity and durable budget control.

    The reservation callback must atomically reserve a reviewed upper-bound cost for
    RequestEnvelope across all workers/restarts under the USD 4 inference allocation.
    Never refund failed/ambiguous attempts automatically. No production ledger is supplied here.
    """

    ai = True

    def __init__(
        self,
        endpoint: str,
        deployment: str,
        *,
        enabled: bool = False,
        token: Callable[[], str] | None = None,
        reserve: Callable[[RequestEnvelope], bool] | None = None,
        transport: Callable[[str, bytes, str], bytes] = _post,
        clock: Callable[[], float] = time.time,
    ) -> None:
        if not re.fullmatch(r"https://[a-z0-9][a-z0-9-]{0,62}\.openai\.azure\.com", endpoint):
            raise ValueError("Use a reviewed HTTPS Azure OpenAI endpoint.")
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", deployment):
            raise ValueError("Use a valid deployment name.")
        self.url = (
            f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2024-10-21"
        )
        self.enabled, self.token, self.reserve = enabled, token, reserve
        self.transport, self.clock = transport, clock

    def select(self, topic: Topic) -> Topic:
        if not isinstance(topic, Topic):
            raise AssistantUnavailable("invalid_topic")
        if (
            not self.enabled
            or self.clock() >= EXPIRES
            or self.token is None
            or self.reserve is None
        ):
            raise AssistantUnavailable("not_activated")
        envelope = RequestEnvelope(
            f"Return only this exact topic word, without punctuation: {topic.value}"
        )
        if len(envelope.prompt.encode("ascii")) > MAX_PROMPT_BYTES:
            raise AssistantUnavailable("prompt_limit")
        if not self.reserve(envelope):
            raise AssistantUnavailable("budget_unavailable")
        try:
            token = self.token()
            if not token or "\r" in token or "\n" in token:
                raise AssistantUnavailable("credential_unavailable")
            if self.clock() >= EXPIRES:
                raise AssistantUnavailable("expired")
            payload = json.dumps(
                {
                    "messages": [{"role": "user", "content": envelope.prompt}],
                    "max_tokens": envelope.max_output_tokens,
                    "n": 1,
                    "stream": False,
                }
            ).encode("ascii")
            raw = self.transport(self.url, payload, token)
            if len(raw) > MAX_REPLY:
                raise AssistantUnavailable("reply_limit")
            body = json.loads(raw)
            choices = body["choices"]
            if (
                len(choices) != 1
                or choices[0]["finish_reason"] != "stop"
                or choices[0]["message"].get("tool_calls")
                or choices[0]["message"]["content"] != topic.value
            ):
                raise AssistantUnavailable("invalid_reply")
        except (
            OSError,
            ValueError,
            KeyError,
            IndexError,
            TypeError,
            AttributeError,
        ):
            raise AssistantUnavailable("provider_failed") from None
        return topic
