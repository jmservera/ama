import json
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from zava_forward.agents.dispatch import ResultMessage
from zava_forward.agents.runtime import (
    ApiResultSink,
    ConfigError,
    beat,
    build_runtime,
    healthy,
    identity_token,
    limits_active,
    token_opener,
)

SENTINEL = "sentinel-secret-value"


def environment(**changes: str | None) -> dict[str, str]:
    expires = (datetime.now(UTC) + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    env = dict(
        QUEUE_ENDPOINT="https://acct.queue.core.windows.net",
        TASK_QUEUE="agent-tasks",
        POISON_QUEUE="agent-tasks-poison",
        API_BASE_URL="https://api.example.test",
        API_AUDIENCE="api://client",
        FOUNDRY_ENDPOINT="https://foundry.example.test",
        MODEL_DEPLOYMENT_DEFAULT="standard",
        MODEL_DEPLOYMENT_CAPABLE="capable",
        IDENTITY_ENDPOINT="http://127.0.0.1:42356/msi/token",
        IDENTITY_HEADER=SENTINEL,
        ZF_AGENT_RESULT_ROUTE="enabled",
        ZF_ASSIST_AUTHORITY="op",
        ZF_ASSIST_CALL_ALLOWANCE="10",
        ZF_ASSIST_TOKEN_ALLOWANCE="1000000",
        ZF_ASSIST_EXPIRES=expires,
    )
    for key, value in changes.items():
        if value is None:
            env.pop(key, None)
        else:
            env[key] = value
    return env


def result() -> ResultMessage:
    return ResultMessage("t1", 1, "owner", {"usage": None}, None, "failed")


class FakeResponse:
    def __init__(self, body: bytes) -> None:
        self.body = body

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def read(self, _: int = -1) -> bytes:
        return self.body


class Opener:
    def __init__(self, body: bytes) -> None:
        self.body = body
        self.requests: list[Any] = []

    def open(self, request: Any, timeout: float = 0) -> FakeResponse:
        self.requests.append(request)
        return FakeResponse(self.body)


class IdentityTokenTests(unittest.TestCase):
    def test_requests_resource_with_header_and_caches(self) -> None:
        opener = Opener(b'{"access_token": "tok", "expires_on": "9999999999"}')
        env = environment(AZURE_CLIENT_ID="client-1")
        token = identity_token("https://storage.azure.com/", env, opener)
        self.assertEqual(token(), "tok")
        self.assertEqual(token(), "tok")
        self.assertEqual(len(opener.requests), 1)
        request = opener.requests[0]
        self.assertIn("resource=https%3A%2F%2Fstorage.azure.com%2F", request.full_url)
        self.assertIn("client_id=client-1", request.full_url)
        self.assertEqual(request.get_header("X-identity-header"), SENTINEL)

    def test_missing_endpoint_and_bad_response_use_fixed_text(self) -> None:
        with self.assertRaises(ConfigError):
            identity_token("r", environment(IDENTITY_ENDPOINT=None), Opener(b"{}"))
        token = identity_token("r", environment(), Opener(SENTINEL.encode()))
        with self.assertRaises(RuntimeError) as caught:
            token()
        self.assertNotIn(SENTINEL, str(caught.exception))
        self.assertIsNone(caught.exception.__cause__)

    def test_redirects_are_refused(self) -> None:
        opener: Any = token_opener()
        self.assertIn("_NoRedirect", [type(h).__name__ for h in opener.handlers])


class ApiResultSinkTests(unittest.TestCase):
    def sink(self, status: int, calls: list[Any]) -> ApiResultSink:
        def transport(
            method: str, url: str, headers: dict[str, str], body: bytes | None
        ) -> tuple[int, bytes]:
            calls.append((method, url, headers, body))
            return status, b""

        return ApiResultSink("https://api.example.test", lambda: "bearer-1", transport)

    def test_posts_result_json_with_bearer(self) -> None:
        calls: list[Any] = []
        self.sink(202, calls).post(result())
        method, url, headers, body = calls[0]
        self.assertEqual((method, url), ("POST", "https://api.example.test/api/agent-results"))
        self.assertEqual(headers["Authorization"], "Bearer bearer-1")
        self.assertEqual(json.loads(body)["task_id"], "t1")

    def test_other_status_raises_so_message_is_not_acknowledged(self) -> None:
        for status in (401, 404, 500):
            with self.subTest(status=status), self.assertRaises(RuntimeError):
                self.sink(status, []).post(result())

    def test_refuses_plain_http_base(self) -> None:
        with self.assertRaises(ValueError):
            ApiResultSink("http://api.example.test", lambda: "t", lambda *a: (200, b""))


class BuildRuntimeTests(unittest.TestCase):
    def test_builds_from_complete_environment(self) -> None:
        runtime = build_runtime(environment(), opener=Opener(b"{}"))
        self.assertEqual(runtime.queue.queue, "agent-tasks")
        self.assertEqual(runtime.queue.poison_queue, "agent-tasks-poison")
        self.assertTrue(runtime.limits.valid)

    def test_missing_names_listed_without_values(self) -> None:
        env = environment(QUEUE_ENDPOINT=None, API_AUDIENCE=None, ZF_AGENT_RESULT_ROUTE=None)
        with self.assertRaises(ConfigError) as caught:
            build_runtime(env, opener=Opener(b"{}"))
        text = str(caught.exception)
        for name in ("QUEUE_ENDPOINT", "API_AUDIENCE", "ZF_AGENT_RESULT_ROUTE"):
            self.assertIn(name, text)
        self.assertNotIn(SENTINEL, text)

    def test_route_must_be_enabled_so_no_message_is_drained_early(self) -> None:
        with self.assertRaisesRegex(ConfigError, "ZF_AGENT_RESULT_ROUTE"):
            build_runtime(environment(ZF_AGENT_RESULT_ROUTE="no"), opener=Opener(b"{}"))

    def test_invalid_or_expired_allowance_is_refused(self) -> None:
        for env in (
            environment(ZF_ASSIST_AUTHORITY=""),
            environment(ZF_ASSIST_EXPIRES="2001-01-01T00:00:00Z"),
        ):
            with self.subTest(env=env["ZF_ASSIST_EXPIRES"]), self.assertRaises(ConfigError):
                build_runtime(env, opener=Opener(b"{}"))

    def test_bad_endpoint_is_a_config_error_without_value(self) -> None:
        env = environment(QUEUE_ENDPOINT="http://" + SENTINEL)
        with self.assertRaises(ConfigError) as caught:
            build_runtime(env, opener=Opener(b"{}"))
        self.assertNotIn(SENTINEL, str(caught.exception))

    def test_unmetered_model_call_fails_closed_without_network(self) -> None:
        runtime = build_runtime(environment(), opener=Opener(b"{}"))
        raw = runtime.provider("system", "prompt", 100, 5)
        self.assertEqual(raw["outcome"], "financial-held")
        self.assertIsNone(raw["text"])

    def test_limits_active_tracks_expiry(self) -> None:
        runtime = build_runtime(environment(), opener=Opener(b"{}"))
        self.assertTrue(limits_active(runtime.limits, 0.0))
        self.assertFalse(limits_active(runtime.limits, 1e12))


class HeartbeatTests(unittest.TestCase):
    def test_beat_and_health_age(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "worker-heartbeat"
            self.assertFalse(healthy(path, 60, 100.0))
            beat(path, 100.0)
            self.assertTrue(healthy(path, 60, 130.0))
            self.assertFalse(healthy(path, 60, 200.0))
            path.write_text("not a number", encoding="utf-8")
            self.assertFalse(healthy(path, 60, 100.0))


if __name__ == "__main__":
    unittest.main()
