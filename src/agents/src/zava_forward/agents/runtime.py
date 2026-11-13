"""Environment wiring for the standalone agents worker, using only the standard library.

Builds the queue adapter, API post-back and model provider from the Container App
settings. Failures name the missing setting, never its value. Nothing here decides
anything about a case: the worker stays fail-closed when the result route, the
operator allowance or the financial meter is absent.
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from zava_forward.core import assistants
from zava_forward.core.ai import Ai

from zava_forward.agents.dispatch import (
    AgentWorker,
    Provider,
    ResultMessage,
    foundry_provider,
)
from zava_forward.agents.queue_azure import (
    AzureTaskQueue,
    TokenSource,
    Transport,
    _NoRedirect,
    checked_endpoint,
    urllib_transport,
)

STORAGE_RESOURCE = "https://storage.azure.com/"
RESULT_PATH = "/api/agent-results"
ROUTE_FLAG = "ZF_AGENT_RESULT_ROUTE"
ACCEPTED = (200, 201, 202, 204)
HEARTBEAT_NAME = "worker-heartbeat"
HEARTBEAT_MAX_AGE_SECONDS = 120.0
REQUIRED = (
    "QUEUE_ENDPOINT",
    "TASK_QUEUE",
    "POISON_QUEUE",
    "API_BASE_URL",
    "API_AUDIENCE",
    "FOUNDRY_ENDPOINT",
)


class ConfigError(RuntimeError):
    """The worker is not configured; the message names settings, never values."""


def token_opener() -> urllib.request.OpenerDirector:
    return urllib.request.build_opener(_NoRedirect)


def identity_token(resource: str, env: Mapping[str, str], opener: Any | None = None) -> TokenSource:
    """Managed-identity bearer token source with a small cache."""
    endpoint = env.get("IDENTITY_ENDPOINT", "")
    header = env.get("IDENTITY_HEADER", "")
    if not endpoint or not header:
        raise ConfigError("IDENTITY_ENDPOINT and IDENTITY_HEADER are required.")
    parameters = {"resource": resource, "api-version": "2019-08-01"}
    if env.get("AZURE_CLIENT_ID"):
        parameters["client_id"] = env["AZURE_CLIENT_ID"]
    url = f"{endpoint}?{urllib.parse.urlencode(parameters)}"
    client = opener if opener is not None else token_opener()
    cache: dict[str, Any] = {"token": "", "expires": 0.0}

    def source() -> str:
        if cache["token"] and time.time() < cache["expires"] - 120:
            return str(cache["token"])
        request = urllib.request.Request(url, headers={"X-IDENTITY-HEADER": header})  # noqa: S310
        try:
            with client.open(request, timeout=5) as response:
                data = json.loads(response.read(65536))
            token = data["access_token"]
            expires = float(data.get("expires_on", time.time() + 1800))
        except Exception:
            raise RuntimeError("Managed identity token request failed.") from None
        cache.update(token=token, expires=expires)
        return str(token)

    return source


class ApiResultSink:
    """Posts a result to the API; any non-success status raises so nothing is acknowledged."""

    def __init__(
        self,
        base_url: str,
        token: TokenSource,
        transport: Transport = urllib_transport,
    ) -> None:
        self.url = f"{checked_endpoint(base_url)}{RESULT_PATH}"
        self.token = token
        self.transport = transport

    def post(self, result: ResultMessage) -> None:
        headers = {
            "Authorization": f"Bearer {self.token()}",
            "Content-Type": "application/json",
        }
        status, _ = self.transport("POST", self.url, headers, result.to_json().encode("utf-8"))
        if status not in ACCEPTED:
            raise RuntimeError(f"Result post-back failed with status {status}.")


@dataclass
class Runtime:
    queue: AzureTaskQueue
    worker: AgentWorker
    sink: ApiResultSink
    limits: Any
    provider: Provider


def limits_active(limits: Any, now: float | None = None) -> bool:
    return bool(limits.valid and (time.time() if now is None else now) < limits.expiry)


def build_runtime(env: Mapping[str, str], opener: Any | None = None) -> Runtime:
    missing = [name for name in REQUIRED if not env.get(name)]
    if env.get(ROUTE_FLAG) != "enabled":
        missing.append(ROUTE_FLAG)
    if missing:
        raise ConfigError("Missing or not enabled: " + ", ".join(missing) + ".")
    limits = assistants.Limits(dict(env))
    if not limits.valid:
        raise ConfigError("ZF_ASSIST_* operator allowance is missing or invalid.")
    if not limits_active(limits):
        raise ConfigError("ZF_ASSIST_EXPIRES has passed.")
    try:
        queue = AzureTaskQueue(
            env["QUEUE_ENDPOINT"],
            env["TASK_QUEUE"],
            env["POISON_QUEUE"],
            identity_token(STORAGE_RESOURCE, env, opener),
            lease=limits.lease,
        )
        sink = ApiResultSink(env["API_BASE_URL"], identity_token(env["API_AUDIENCE"], env, opener))
    except ValueError:
        raise ConfigError("QUEUE_ENDPOINT, queue names or API_BASE_URL are invalid.") from None
    ai = Ai()
    ai.endpoint = env["FOUNDRY_ENDPOINT"].rstrip("/")
    ai.fast = env.get("MODEL_DEPLOYMENT_DEFAULT", ai.fast)
    ai.strong = env.get("MODEL_DEPLOYMENT_CAPABLE", ai.strong)
    provider = foundry_provider(ai)
    return Runtime(queue, AgentWorker(provider, limits.active_calls), sink, limits, provider)


def beat(path: Path, now: float | None = None) -> None:
    try:
        path.write_text(str(time.time() if now is None else now), encoding="utf-8")
    except OSError:
        pass  # a missing heartbeat is reported by the health check, not by crashing the worker


def healthy(path: Path, max_age: float, now: float | None = None) -> bool:
    try:
        written = float(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return (time.time() if now is None else now) - written <= max_age


__all__ = [
    "ApiResultSink",
    "ConfigError",
    "Runtime",
    "build_runtime",
    "beat",
    "healthy",
    "identity_token",
    "limits_active",
    "token_opener",
]
