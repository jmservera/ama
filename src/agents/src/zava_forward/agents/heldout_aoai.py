"""Opt-in Azure OpenAI provider for the held-out token runner (#435 AC4, refs #432).

Builds the ``Call`` that ``heldout_batch.run_batch`` expects. It sends one non-streaming chat
completion per proposal with a bearer token from ``az account get-access-token`` or a managed
identity. It never retries, never follows redirects, never stores or logs the token or the
response body, and maps every failure to an unmeasured envelope so the runner charges the worst
case and stops. Constructing it makes no network call.
"""

from __future__ import annotations

import importlib
import json
import re
import subprocess
import urllib.error
import urllib.request
from collections.abc import Callable
from typing import Any

ENDPOINT = re.compile(r"https://[a-z0-9-]{2,64}\.(openai|cognitiveservices)\.azure\.com/?")
DEPLOYMENT = re.compile(r"[A-Za-z0-9._-]{1,64}")
RESOURCE = "https://cognitiveservices.azure.com"
API_VERSION = "2024-10-21"
MAX_RESPONSE_BYTES = 1024 * 1024
TOKEN_TIMEOUT_SECONDS = 30
AUTH_MODES = ("az-cli", "managed-identity")
Call = Callable[[str, str, int, int], dict[str, Any]]
Opener = Callable[..., Any]


class AdapterError(Exception):
    """Fixed-message failure; never carries a token, header or response body."""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args: Any, **kwargs: Any) -> None:
        return None


def az_cli_token(run: Callable[..., Any] = subprocess.run) -> str:
    argv = [
        "az", "account", "get-access-token", "--resource", RESOURCE,
        "--query", "accessToken", "-o", "tsv",
    ]  # fmt: skip
    try:
        done = run(argv, capture_output=True, text=True, timeout=TOKEN_TIMEOUT_SECONDS, check=False)
        token = done.stdout.strip() if done.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        token = ""
    if not token:
        raise AdapterError("az CLI access token unavailable") from None
    return str(token)


def managed_identity_token(credential_factory: Callable[[], Any] | None = None) -> str:
    try:
        factory = credential_factory
        if factory is None:
            factory = importlib.import_module("azure.identity").ManagedIdentityCredential
        token = str(factory().get_token(RESOURCE + "/.default").token)
    except Exception:
        token = ""
    if not token:
        raise AdapterError("managed identity access token unavailable") from None
    return token


def get_token(auth: str) -> str:
    if auth == "managed-identity":
        return managed_identity_token()
    return az_cli_token()


def valid_target(endpoint: str, deployment: str) -> bool:
    return bool(ENDPOINT.fullmatch(endpoint) and DEPLOYMENT.fullmatch(deployment))


def _serves(served: str, model: str) -> bool:
    """Exact model name, optionally with the provider's date version suffix."""
    return re.fullmatch(re.escape(model) + r"(-\d{4}-\d{2}-\d{2})?", served) is not None


def _cached_tokens(usage: dict[str, Any]) -> int | None:
    details = usage.get("prompt_tokens_details")
    cached = details.get("cached_tokens") if isinstance(details, dict) else None
    return cached if isinstance(cached, int) and not isinstance(cached, bool) else None


def _envelope(body: Any, model: str) -> dict[str, Any]:
    usage = body.get("usage") if isinstance(body, dict) else None
    served = body.get("model") if isinstance(body, dict) else None
    if not isinstance(usage, dict) or not isinstance(served, str) or not _serves(served, model):
        return dict(outcome="failed")
    cached = _cached_tokens(usage)
    if cached is None:
        return dict(outcome="failed")
    return dict(
        outcome="returned",
        text=None,
        usage=dict(
            prompt_tokens=usage.get("prompt_tokens"),
            completion_tokens=usage.get("completion_tokens"),
            total_tokens=usage.get("total_tokens"),
            cached_tokens=cached,
        ),
    )


def make_provider(
    endpoint: str, deployment: str, model: str, token: str, opener: Opener | None = None
) -> Call:
    """Return a ``Call`` bound to one deployment; raises ValueError for an unsafe target."""
    if not valid_target(endpoint, deployment):
        raise ValueError("endpoint or deployment is not an accepted Azure OpenAI target")
    url = (
        f"{endpoint.rstrip('/')}/openai/deployments/{deployment}/chat/completions"
        f"?api-version={API_VERSION}"
    )
    send = opener or urllib.request.build_opener(urllib.request.ProxyHandler({}), _NoRedirect).open

    def call(system: str, prompt: str, max_tokens: int, timeout: int) -> dict[str, Any]:
        messages = ([dict(role="system", content=system)] if system else []) + [
            dict(role="user", content=prompt)
        ]
        payload = json.dumps(dict(messages=messages, max_tokens=max_tokens, temperature=0))
        request = urllib.request.Request(
            url,
            data=payload.encode("utf-8"),
            method="POST",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        )
        try:
            with send(request, timeout=timeout) as response:
                raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                return dict(outcome="failed")
            return _envelope(json.loads(raw), model)
        except Exception:
            return dict(outcome="failed")

    return call
