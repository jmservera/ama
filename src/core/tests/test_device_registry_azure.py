"""Actual installed-SDK contract tests for the keyless IoT Hub Registry adapter (#185).

The real `azure-iot-hub` serialisation, authentication and request path run unmodified; only the
final `requests` adapter is replaced by a simulator that models the documented IoT Hub REST
conditional-header table. This is a local contract test, not proof of Azure service behaviour.
"""

import importlib
import json
import os
import subprocess
import sys
import traceback
import unittest
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any
from unittest import mock
from urllib.parse import parse_qs, urlsplit

from azure.core.credentials import AccessToken

from test_device_identity import FakeStore, sensors
from zava_forward.core.synthetic import device_identity as di
from zava_forward.core.synthetic import device_registry_azure as dra

requests: Any = importlib.import_module("requests")
HOST = "zf-test-hub.azure-devices.net"
RUN = "run-185"
SECRET = "PRIVATE-SENTINEL-SECRET"
TOKEN = "sentinel-entra-token-value"
MARKER = dra.MARKER_PREFIX + RUN
IDS = ("SYN-A1", "SYN-A2")


def thumb(n: int, width: int = 40) -> str:
    return f"{n:0{width}X}"


def make_spec(
    ids: Sequence[str] = IDS, run: str = RUN, secondary: bool = False
) -> dra.EnrollmentSpec:
    items = tuple(
        dra.X509Enrollment(d, thumb(i + 1), thumb(i + 501) if secondary else None)
        for i, d in enumerate(ids)
    )
    return dra.EnrollmentSpec(run, items)


class Credential:
    def __init__(self, fail: bool = False) -> None:
        self.calls: list[tuple[str, ...]] = []
        self.fail = fail

    def get_token(self, *scopes: str, **kwargs: Any) -> AccessToken:
        self.calls.append(scopes)
        if self.fail:
            raise RuntimeError(SECRET)
        return AccessToken(TOKEN, 4102444800)


@dataclass(frozen=True)
class Seen:
    method: str
    url: str
    headers: dict[str, str]
    body: Any
    kwargs: dict[str, Any]
    retries: Any

    def header(self, name: str) -> str | None:
        for key, value in self.headers.items():
            if key.lower() == name.lower():
                return value
        return None

    @property
    def path(self) -> str:
        return urlsplit(self.url).path


@dataclass
class Fault:
    method: str
    when: str
    effect: str | int
    device: str | None = None


class HubSimulator:
    """Models the documented PUT and DELETE conditional-header table, GET and list."""

    def __init__(self) -> None:
        self.devices: dict[str, dict[str, Any]] = {}
        self.requests: list[Seen] = []
        self.faults: list[Fault] = []
        self.before_delete: Callable[[], None] | None = None
        self.create_status = 200
        self.delete_status = 204
        self.list_omits_reason = False
        self.list_padding = 0
        self.counter = 0

    def put_device(self, device_id: str, reason: str | None, status: str = "disabled") -> None:
        self.counter += 1
        self.devices[device_id] = {
            "etag": f"ETAG{self.counter}==",
            "generationId": f"GEN{self.counter}",
            "body": {"status": status, "statusReason": reason},
        }

    def seen(self, method: str) -> list[Seen]:
        return [s for s in self.requests if s.method == method]

    def send(self, adapter: Any, request: Any, **kwargs: Any) -> Any:
        body = json.loads(request.body) if request.body else None
        self.requests.append(
            Seen(
                request.method,
                request.url,
                dict(request.headers),
                body,
                kwargs,
                adapter.max_retries.total,
            )
        )
        parts = urlsplit(request.url)
        if parts.netloc != HOST:
            raise AssertionError("unexpected host")
        device_id = parts.path.removeprefix("/devices/") if parts.path != "/devices" else None
        fault = next(
            (
                f
                for f in self.faults
                if f.method == request.method and f.device in (None, device_id)
            ),
            None,
        )
        if fault is not None:
            self.faults.remove(fault)
            if fault.when == "before":
                if fault.effect == "timeout":
                    raise requests.exceptions.ReadTimeout(SECRET)
                return self.reply(request, int(fault.effect), {"Message": SECRET})
        if request.method == "DELETE" and self.before_delete is not None:
            self.before_delete()
        response = self.apply(request, device_id, body, parts.query)
        if fault is not None and fault.when == "after":
            raise requests.exceptions.ReadTimeout(SECRET)
        return response

    def apply(self, request: Any, device_id: str | None, body: Any, query: str) -> Any:
        headers = {k.lower(): v for k, v in request.headers.items()}
        if_match, none_match = headers.get("if-match"), headers.get("if-none-match")
        if device_id is None:
            top = int(parse_qs(query).get("top", ["1000"])[0])
            listed = [self.view(d, listing=True) for d in sorted(self.devices)]
            listed += [
                {"deviceId": f"PAD-{i}", "etag": "x", "generationId": "g", "statusReason": "pad"}
                for i in range(self.list_padding)
            ]
            return self.reply(request, 200, listed[:top])
        current = self.devices.get(device_id)
        if request.method == "GET":
            if current is None:
                return self.reply(request, 404, {"Message": SECRET})
            return self.reply(request, 200, self.view(device_id))
        if request.method == "PUT":
            if current is None and if_match is None:
                self.counter += 1
                self.devices[device_id] = {
                    "etag": f"ETAG{self.counter}==",
                    "generationId": f"GEN{self.counter}",
                    "body": {k: v for k, v in body.items() if k != "deviceId"},
                }
                return self.reply(request, self.create_status, self.view(device_id))
            if current is None or none_match == "*":
                return self.reply(request, 412, {"Message": SECRET})
            self.counter += 1
            current["etag"] = f"ETAG{self.counter}=="
            current["body"] = {k: v for k, v in body.items() if k != "deviceId"}
            return self.reply(request, 200, self.view(device_id))
        if current is None:
            return self.reply(request, 204, None)
        if if_match not in (None, "*", f'"{current["etag"]}"'):
            return self.reply(request, 412, {"Message": SECRET})
        del self.devices[device_id]
        return self.reply(request, self.delete_status, None)

    def view(self, device_id: str, listing: bool = False) -> dict[str, Any]:
        current = self.devices[device_id]
        view = {
            "deviceId": device_id,
            "etag": current["etag"],
            "generationId": current["generationId"],
            **current["body"],
        }
        if listing and self.list_omits_reason:
            view.pop("statusReason", None)
        return view

    def reply(self, request: Any, status: int, body: Any) -> Any:
        response = requests.Response()
        response.status_code = status
        response._content = b"" if body is None else json.dumps(body).encode()
        response.headers["Content-Type"] = "application/json"
        response.url = request.url
        response.request = request
        return response


class HubCase(unittest.TestCase):
    def setUp(self) -> None:
        self.hub = HubSimulator()
        self.credential = Credential()
        patch = mock.patch.object(
            requests.adapters.HTTPAdapter,
            "send",
            new=lambda adapter, request, **kw: self.hub.send(adapter, request, **kw),
        )
        patch.start()
        self.addCleanup(patch.stop)

    def registry(
        self, spec: dra.EnrollmentSpec | None = None, **kw: Any
    ) -> dra.AzureIotHubRegistry:
        kw.setdefault("credential", self.credential)
        registry = dra.AzureIotHubRegistry(HOST, spec or make_spec(), **kw)
        self.addCleanup(registry.close)
        return registry

    def refused(self, call: Callable[[], object]) -> dra.RegistryError:
        with self.assertRaises(dra.RegistryError) as caught:
            call()
        return caught.exception


class ImportAndRefusalTests(HubCase):
    def test_import_has_no_sdk_credential_or_network_effects(self) -> None:
        code = (
            "import sys\n"
            "import zava_forward.core.synthetic.device_registry_azure\n"
            "names = ('azure.iot', 'uamqp', 'msrest', 'six')\n"
            "print([m for m in sys.modules if m.split('.')[0] in names or m in names])\n"
        )
        env = {**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)}
        done = subprocess.run(
            [sys.executable, "-c", code], env=env, capture_output=True, text=True, check=True
        )
        self.assertEqual(done.stdout.strip(), "[]")

    def test_core_imports_without_sdk_and_reports_it_at_first_use_only(self) -> None:
        blocked = {"azure.iot.hub": None, "azure.iot.hub.protocol.models": None}
        with mock.patch.dict(sys.modules, blocked):
            registry = self.registry()
            for call in (
                lambda: registry.create("SYN-A1", RUN),
                lambda: registry.run_of("SYN-A1"),
                lambda: registry.list_run(RUN),
            ):
                self.assertEqual(self.refused(call).code, "SDK_MISSING")
        self.assertEqual((self.credential.calls, self.hub.requests), ([], []))

    def test_construction_close_and_dry_use_touch_nothing(self) -> None:
        registry = self.registry()
        registry.close()
        registry.close()
        self.assertEqual((self.credential.calls, self.hub.requests), ([], []))
        self.assertEqual(self.refused(lambda: registry.run_of("SYN-A1")).code, "CLOSED")
        self.assertEqual(self.hub.requests, [])

    def test_invalid_inputs_refuse_before_any_sdk_effect(self) -> None:
        spec = make_spec()
        bad_hosts = [
            "",
            "https://zf-test-hub.azure-devices.net",
            "ZF-Test-Hub.azure-devices.net",
            "zf-test-hub.azure-devices.net:443",
            "zf-test-hub.azure-devices.net/",
            "zf-test-hub.example.com",
            "zf-test-hub.azure-devices.net.evil.example",
            "-bad.azure-devices.net",
            "ab.azure-devices.net",
        ]
        for host in bad_hosts:
            with self.subTest(host=host):
                error = self.refused(
                    lambda host=host: dra.AzureIotHubRegistry(  # type: ignore[misc]
                        host, spec, credential=self.credential
                    )
                )
                self.assertEqual(error.code, "INVALID_CONFIGURATION")
        configs: dict[str, dict[str, Any]] = {
            "neither": {},
            "both": {"credential": self.credential, "client": object()},
            "timeout low": {"credential": self.credential, "timeout": 0},
            "timeout high": {"credential": self.credential, "timeout": 61},
            "timeout nan": {"credential": self.credential, "timeout": float("nan")},
            "timeout bool": {"credential": self.credential, "timeout": True},
            "no get_token": {"credential": object()},
        }
        for label, kw in configs.items():
            with self.subTest(config=label):
                error = self.refused(
                    lambda kw=kw: dra.AzureIotHubRegistry(HOST, spec, **kw)  # type: ignore[misc]
                )
                self.assertEqual(error.code, "INVALID_CONFIGURATION")
        good = thumb(1)
        enrolments: dict[str, Callable[[], object]] = {
            "device id": lambda: dra.X509Enrollment("OTHER-A1", good),
            "lowercase id": lambda: dra.X509Enrollment("syn-a1", good),
            "lowercase print": lambda: dra.X509Enrollment("SYN-A1", good.lower().replace("0", "a")),
            "short print": lambda: dra.X509Enrollment("SYN-A1", good[:-1]),
            "non hex": lambda: dra.X509Enrollment("SYN-A1", "G" * 40),
            "same secondary": lambda: dra.X509Enrollment("SYN-A1", good, good),
            "no enrolments": lambda: dra.EnrollmentSpec(RUN, ()),
            "list": lambda: dra.EnrollmentSpec(RUN, [dra.X509Enrollment("SYN-A1", good)]),  # type: ignore[arg-type]
            "bad run": lambda: dra.EnrollmentSpec("Run_1", (dra.X509Enrollment("SYN-A1", good),)),
            "dup id": lambda: dra.EnrollmentSpec(
                RUN,
                (dra.X509Enrollment("SYN-A1", thumb(1)), dra.X509Enrollment("SYN-A1", thumb(2))),
            ),
            "dup print": lambda: dra.EnrollmentSpec(
                RUN, (dra.X509Enrollment("SYN-A1", good), dra.X509Enrollment("SYN-A2", good))
            ),
            "too many": lambda: dra.EnrollmentSpec(
                RUN,
                tuple(dra.X509Enrollment(f"SYN-A{i}", thumb(i + 1)) for i in range(101)),
            ),
        }
        for label, build in enrolments.items():
            with self.subTest(enrolment=label):
                self.assertEqual(self.refused(build).code, "INVALID_ENROLLMENT")
        self.assertEqual((self.credential.calls, self.hub.requests), ([], []))

    def test_operations_outside_the_enrolment_refuse_before_the_sdk(self) -> None:
        registry = self.registry()
        for call in (
            lambda: registry.create("SYN-ZZ", RUN),
            lambda: registry.create("SYN-A1", "other-run"),
            lambda: registry.run_of("SYN-ZZ"),
            lambda: registry.delete("SYN-ZZ", RUN),
            lambda: registry.delete("SYN-A1", "other-run"),
            lambda: registry.list_run("other-run"),
        ):
            self.assertEqual(self.refused(call).code, "NOT_ENROLLED")
        self.assertEqual((self.credential.calls, self.hub.requests), ([], []))


class CreateTests(HubCase):
    def test_create_sends_exact_create_only_disabled_marker_and_public_thumbprints(self) -> None:
        registry = self.registry(make_spec(secondary=True), timeout=7)
        registry.create("SYN-A1", RUN)
        (put,) = self.hub.seen("PUT")
        self.assertEqual(len(self.hub.requests), 1)
        self.assertEqual(urlsplit(put.url).netloc, HOST)
        self.assertEqual(put.path, "/devices/SYN-A1")
        self.assertEqual(put.header("If-None-Match"), "*")
        self.assertIsNone(put.header("If-Match"))
        self.assertEqual(put.header("Authorization"), f"Bearer {TOKEN}")
        self.assertEqual(
            put.body,
            {
                "deviceId": "SYN-A1",
                "status": "disabled",
                "statusReason": MARKER,
                "authentication": {
                    "type": "selfSigned",
                    "x509Thumbprint": {
                        "primaryThumbprint": thumb(1),
                        "secondaryThumbprint": thumb(501),
                    },
                },
                "capabilities": {"iotEdge": False},
            },
        )
        self.assertNotIn("SharedAccessSignature", json.dumps(put.headers))
        self.assertEqual((put.retries, put.kwargs["timeout"]), (0, 7.0))
        self.assertEqual(self.credential.calls[0], ("https://iothubs.azure.net/.default",))
        self.assertEqual(self.hub.devices["SYN-A1"]["body"]["status"], "disabled")

    def test_primary_only_enrolment_omits_the_secondary_thumbprint(self) -> None:
        self.registry().create("SYN-A2", RUN)
        thumbprint = self.hub.seen("PUT")[0].body["authentication"]["x509Thumbprint"]
        self.assertEqual(thumbprint, {"primaryThumbprint": thumb(2)})

    def test_existing_identity_conflicts_and_is_never_adopted_or_overwritten(self) -> None:
        for existing in (None, "somebody else", MARKER, dra.MARKER_PREFIX + "other-run"):
            with self.subTest(existing=existing):
                self.hub.requests.clear()
                self.hub.put_device("SYN-A1", existing, status="enabled")
                before = json.dumps(self.hub.devices, sort_keys=True)
                error = self.refused(lambda: self.registry().create("SYN-A1", RUN))
                self.assertEqual(error.code, "IDENTITY_CONFLICT")
                self.assertEqual(json.dumps(self.hub.devices, sort_keys=True), before)
                self.assertEqual(len(self.hub.requests), 1)

    def test_documented_201_created_is_success_even_though_the_sdk_raises(self) -> None:
        self.hub.create_status = 201
        self.registry().create("SYN-A1", RUN)
        self.assertIn("SYN-A1", self.hub.devices)

    def test_definitive_rejections_are_not_unknown_and_do_not_retry(self) -> None:
        for status, code in (
            (401, "ACCESS_DENIED"),
            (403, "ACCESS_DENIED"),
            (400, "REJECTED"),
            (429, "REJECTED"),
        ):
            with self.subTest(status=status):
                self.hub.requests.clear()
                self.hub.faults.append(Fault("PUT", "before", status))
                error = self.refused(lambda: self.registry().create("SYN-A1", RUN))
                self.assertEqual((error.code, error.readback), (code, None))
                self.assertEqual([s.method for s in self.hub.requests], ["PUT"])

    def test_timeout_after_the_write_is_unknown_with_safe_readback_and_no_retry(self) -> None:
        self.hub.faults.append(Fault("PUT", "after", "timeout"))
        error = self.refused(lambda: self.registry().create("SYN-A1", RUN))
        self.assertEqual((error.code, error.readback), ("WRITE_OUTCOME_UNKNOWN", "owned"))
        self.assertEqual([s.method for s in self.hub.requests], ["PUT", "GET"])
        self.assertIn("SYN-A1", self.hub.devices)

    def test_timeout_or_server_error_before_the_write_reads_back_absent(self) -> None:
        for effect in ("timeout", 503):
            with self.subTest(effect=effect):
                self.hub.requests.clear()
                self.hub.faults.append(Fault("PUT", "before", effect))
                error = self.refused(lambda: self.registry().create("SYN-A1", RUN))
                self.assertEqual((error.code, error.readback), ("WRITE_OUTCOME_UNKNOWN", "absent"))
                self.assertEqual(len(self.hub.seen("PUT")), 1)

    def test_unreadable_or_foreign_readback_is_reported_not_adopted(self) -> None:
        self.hub.faults += [Fault("PUT", "before", "timeout"), Fault("GET", "before", 500)]
        error = self.refused(lambda: self.registry().create("SYN-A1", RUN))
        self.assertEqual((error.code, error.readback), ("WRITE_OUTCOME_UNKNOWN", "unreadable"))
        self.hub.faults.append(Fault("PUT", "before", "timeout"))
        self.hub.put_device("SYN-A2", "someone else")
        error = self.refused(lambda: self.registry().create("SYN-A2", RUN))
        self.assertEqual((error.code, error.readback), ("WRITE_OUTCOME_UNKNOWN", "foreign"))

    def test_credential_failure_is_a_fixed_code_before_any_request(self) -> None:
        self.credential.fail = True
        error = self.refused(lambda: self.registry().create("SYN-A1", RUN))
        self.assertEqual(error.code, "CREDENTIAL_UNAVAILABLE")
        self.assertEqual(self.hub.requests, [])


class OwnershipReadTests(HubCase):
    def test_run_of_distinguishes_absent_owned_foreign_and_unmarked(self) -> None:
        registry = self.registry()
        self.assertIsNone(registry.run_of("SYN-A1"))
        self.hub.put_device("SYN-A1", MARKER)
        self.assertEqual(registry.run_of("SYN-A1"), RUN)
        self.hub.put_device("SYN-A1", dra.MARKER_PREFIX + "other-run")
        self.assertEqual(registry.run_of("SYN-A1"), "other-run")
        near = (
            None,
            "",
            "SYN-A1",
            MARKER + " ",
            MARKER + "\n",
            MARKER.upper(),
            dra.MARKER_PREFIX + "Bad_Run",
        )
        for reason in near:
            with self.subTest(reason=reason):
                self.hub.put_device("SYN-A1", reason)
                self.assertEqual(registry.run_of("SYN-A1"), dra.NOT_RUN_OWNED)
        self.assertIsNone(di.RUN_ID.fullmatch(dra.NOT_RUN_OWNED))
        self.assertTrue(all(s.header("If-Match") is None for s in self.hub.requests))
        self.assertEqual({s.method for s in self.hub.requests}, {"GET"})

    def test_unavailable_is_never_reported_as_absent(self) -> None:
        registry = self.registry()
        for effect, code in (
            (401, "ACCESS_DENIED"),
            (403, "ACCESS_DENIED"),
            (500, "UNAVAILABLE"),
            (404 + 1, "UNAVAILABLE"),
            ("timeout", "UNAVAILABLE"),
        ):
            with self.subTest(effect=effect):
                self.hub.faults.append(Fault("GET", "before", effect))
                self.assertEqual(self.refused(lambda: registry.run_of("SYN-A1")).code, code)

    def test_a_response_for_a_different_device_is_unreadable(self) -> None:
        self.hub.put_device("SYN-A1", MARKER)
        registry = self.registry()
        original = self.hub.view

        def wrong(device_id: str, listing: bool = False) -> dict[str, Any]:
            return {**original(device_id, listing), "deviceId": "SYN-A2"}

        with mock.patch.object(self.hub, "view", wrong):
            self.assertEqual(self.refused(lambda: registry.run_of("SYN-A1")).code, "UNAVAILABLE")


class DeleteTests(HubCase):
    def test_delete_of_an_owned_identity_uses_the_exact_snapshot_etag(self) -> None:
        for status in (204, 200):
            with self.subTest(delete_status=status):
                self.hub.requests.clear()
                self.hub.delete_status = status
                self.hub.put_device("SYN-A1", MARKER)
                etag = self.hub.devices["SYN-A1"]["etag"]
                self.registry().delete("SYN-A1", RUN)
                (delete,) = self.hub.seen("DELETE")
                self.assertEqual(delete.header("If-Match"), f'"{etag}"')
                self.assertNotIn("*", delete.header("If-Match") or "")
                self.assertEqual((delete.retries, delete.kwargs["timeout"]), (0, 30.0))
                self.assertNotIn("SYN-A1", self.hub.devices)

    def test_foreign_unmarked_and_missing_identities_are_not_deleted(self) -> None:
        registry = self.registry()
        registry.delete("SYN-A1", RUN)
        for reason in (dra.MARKER_PREFIX + "other-run", None, "SYN-A1", MARKER + " "):
            self.hub.put_device("SYN-A1", reason)
            registry.delete("SYN-A1", RUN)
            self.assertIn("SYN-A1", self.hub.devices)
        self.assertEqual(self.hub.seen("DELETE"), [])

    def test_identity_recreated_or_modified_after_the_snapshot_is_refused(self) -> None:
        mutations: dict[str, Callable[[], None]] = {
            "recreated owned": lambda: self.hub.put_device("SYN-A1", MARKER),
            "recreated foreign": lambda: self.hub.put_device("SYN-A1", "someone else"),
            "modified": lambda: self.hub.devices["SYN-A1"].update(etag="CHANGED=="),
        }
        for label, mutate in mutations.items():
            with self.subTest(change=label):
                self.hub.requests.clear()
                self.hub.put_device("SYN-A1", MARKER)
                self.hub.before_delete = mutate
                error = self.refused(lambda: self.registry().delete("SYN-A1", RUN))
                self.assertEqual(error.code, "PRECONDITION_FAILED")
                self.assertIn("SYN-A1", self.hub.devices)
                self.assertEqual(len(self.hub.seen("DELETE")), 1)

    def test_a_snapshot_without_an_exact_etag_and_generation_never_deletes(self) -> None:
        registry = self.registry()
        for patch in (
            {"etag": "*"},
            {"etag": '"quoted"'},
            {"etag": "a,b"},
            {"etag": ""},
            {"generationId": ""},
        ):
            with self.subTest(patch=patch):
                self.hub.put_device("SYN-A1", MARKER)
                self.hub.devices["SYN-A1"].update(patch)
                self.assertEqual(
                    self.refused(lambda: registry.delete("SYN-A1", RUN)).code, "OWNERSHIP_UNCERTAIN"
                )
        self.assertEqual(self.hub.seen("DELETE"), [])

    def test_unreadable_ownership_never_deletes(self) -> None:
        self.hub.put_device("SYN-A1", MARKER)
        for effect, code in (
            (403, "ACCESS_DENIED"),
            (500, "UNAVAILABLE"),
            ("timeout", "UNAVAILABLE"),
        ):
            self.hub.faults.append(Fault("GET", "before", effect))
            self.assertEqual(self.refused(lambda: self.registry().delete("SYN-A1", RUN)).code, code)
        self.assertEqual(self.hub.seen("DELETE"), [])

    def test_timeout_after_delete_reads_back_absent_and_never_retries(self) -> None:
        self.hub.put_device("SYN-A1", MARKER)
        self.hub.faults.append(Fault("DELETE", "after", "timeout"))
        self.registry().delete("SYN-A1", RUN)
        self.assertEqual(len(self.hub.seen("DELETE")), 1)

    def test_timeout_before_delete_leaves_it_with_an_explicit_unknown_outcome(self) -> None:
        self.hub.put_device("SYN-A1", MARKER)
        self.hub.faults.append(Fault("DELETE", "before", "timeout"))
        error = self.refused(lambda: self.registry().delete("SYN-A1", RUN))
        self.assertEqual((error.code, error.readback), ("DELETE_OUTCOME_UNKNOWN", "owned"))
        self.assertIn("SYN-A1", self.hub.devices)
        self.assertEqual(len(self.hub.seen("DELETE")), 1)

    def test_definitive_delete_rejections_are_fixed_codes(self) -> None:
        for status, code in ((403, "ACCESS_DENIED"), (400, "REJECTED")):
            self.hub.put_device("SYN-A1", MARKER)
            self.hub.faults.append(Fault("DELETE", "before", status))
            self.assertEqual(self.refused(lambda: self.registry().delete("SYN-A1", RUN)).code, code)
            self.assertIn("SYN-A1", self.hub.devices)


class ListTests(HubCase):
    def test_list_run_returns_exactly_the_marked_identities(self) -> None:
        self.hub.put_device("SYN-A2", MARKER)
        self.hub.put_device("SYN-A1", MARKER)
        self.hub.put_device("SYN-B1", dra.MARKER_PREFIX + "other-run")
        self.hub.put_device("SYN-B2", None)
        self.assertEqual(self.registry().list_run(RUN), ["SYN-A1", "SYN-A2"])
        list_request, *confirmations = self.hub.requests
        self.assertEqual(parse_qs(urlsplit(list_request.url).query)["top"], ["1000"])
        self.assertEqual([c.path for c in confirmations], ["/devices/SYN-B2"])

    def test_list_below_the_cap_is_complete_and_saturation_is_refused(self) -> None:
        self.hub.put_device("SYN-A1", MARKER)
        self.hub.list_padding = dra.MAX_LIST - 2
        self.assertEqual(self.registry().list_run(RUN), ["SYN-A1"])
        self.hub.list_padding = dra.MAX_LIST - 1
        self.assertEqual(
            self.refused(lambda: self.registry().list_run(RUN)).code, "LIST_INCOMPLETE"
        )
        self.hub.list_padding = dra.MAX_LIST + 5
        self.assertEqual(
            self.refused(lambda: self.registry().list_run(RUN)).code, "LIST_INCOMPLETE"
        )

    def test_payload_that_omits_the_marker_is_confirmed_by_a_bounded_read(self) -> None:
        self.hub.put_device("SYN-A1", MARKER)
        self.hub.put_device("SYN-A2", "someone else")
        self.hub.put_device("SYN-B1", MARKER)
        self.hub.put_device("SYN-B2", None)
        self.hub.put_device("SYN-B3", dra.MARKER_PREFIX + "other-run")
        self.hub.list_omits_reason = True
        self.assertEqual(self.registry().list_run(RUN), ["SYN-A1", "SYN-B1"])
        self.assertEqual(len(self.hub.seen("GET")), 6)
        self.hub.faults.append(Fault("GET", "before", 500))
        self.hub.faults.insert(0, Fault("GET", "before", "timeout"))
        self.assertEqual(self.refused(lambda: self.registry().list_run(RUN)).code, "UNAVAILABLE")

    def test_unreadable_confirmation_of_a_non_enrolled_entry_refuses(self) -> None:
        self.hub.put_device("SYN-B1", MARKER)
        self.hub.list_omits_reason = True
        for effect, code in ((403, "ACCESS_DENIED"), (500, "UNAVAILABLE")):
            self.hub.faults.append(Fault("GET", "before", effect, device="SYN-B1"))
            self.assertEqual(self.refused(lambda: self.registry().list_run(RUN)).code, code)

    def test_confirmation_budget_is_bounded_and_exhaustion_refuses(self) -> None:
        budget = di.MAX_DEVICES
        for n in range(budget):
            self.hub.put_device(f"SYN-C{n}", None)
        self.hub.list_omits_reason = True
        self.assertEqual(self.registry().list_run(RUN), [])
        self.assertEqual(len(self.hub.seen("GET")), budget + 1)
        self.hub.requests.clear()
        self.hub.put_device("SYN-CX", MARKER)
        refusal = self.refused(lambda: self.registry().list_run(RUN))
        self.assertEqual(refusal.code, "LIST_INCOMPLETE")
        self.assertEqual(len(self.hub.seen("GET")), budget + 1)
        self.assertEqual(self.hub.seen("PUT") + self.hub.seen("DELETE"), [])

    def test_list_failures_are_explicit(self) -> None:
        for effect, code in (
            (403, "ACCESS_DENIED"),
            (500, "UNAVAILABLE"),
            ("timeout", "UNAVAILABLE"),
        ):
            self.hub.faults.append(Fault("GET", "before", effect))
            self.assertEqual(self.refused(lambda: self.registry().list_run(RUN)).code, code)


class SanitisedErrorTests(HubCase):
    def test_no_secret_or_response_text_reaches_any_error(self) -> None:
        self.hub.put_device("SYN-A2", MARKER)
        scenarios: dict[str, Callable[[], object]] = {}

        def fault(
            method: str, effect: str | int, call: Callable[[], object]
        ) -> Callable[[], object]:
            def run() -> object:
                self.hub.faults.append(Fault(method, "before", effect))
                return call()

            return run

        registry = self.registry()
        scenarios["create 403"] = fault("PUT", 403, lambda: registry.create("SYN-A1", RUN))
        scenarios["create timeout"] = fault(
            "PUT", "timeout", lambda: registry.create("SYN-A1", RUN)
        )
        scenarios["conflict"] = lambda: registry.create("SYN-A2", RUN)
        scenarios["read 500"] = fault("GET", 500, lambda: registry.run_of("SYN-A1"))
        scenarios["list timeout"] = fault("GET", "timeout", lambda: registry.list_run(RUN))
        scenarios["delete 412"] = fault("DELETE", 412, lambda: registry.delete("SYN-A2", RUN))
        failing = Credential(fail=True)
        scenarios["credential"] = lambda: self.registry(credential=failing).run_of("SYN-A1")
        for label, run in scenarios.items():
            with self.subTest(scenario=label):
                error = self.refused(run)
                text = "".join(traceback.format_exception(error)) + repr(error) + repr(error.args)
                for sentinel in (SECRET, TOKEN, "Message"):
                    self.assertNotIn(sentinel, text)
                self.assertIsNone(error.__cause__)
                self.assertIsNone(error.__context__)
                self.assertEqual(str(error), error.code)
        self.assertNotIn(SECRET, repr(registry))

    def test_refusals_raised_inside_a_caller_handler_do_not_print_the_callers_exception(
        self,
    ) -> None:
        caller = "CALLER-PRIVATE-SENTINEL-185"
        self.hub.put_device("SYN-A2", MARKER)
        registry = self.registry()
        failing = Credential(fail=True)
        thumb_a = thumb(1)

        def fault(
            method: str, effect: str | int, call: Callable[[], object]
        ) -> Callable[[], object]:
            def run() -> object:
                self.hub.faults.append(Fault(method, "before", effect))
                return call()

            return run

        scenarios: dict[str, Callable[[], object]] = {
            "invalid configuration": lambda: dra.AzureIotHubRegistry("bad", make_spec()),
            "invalid enrolment": lambda: dra.X509Enrollment("bad", thumb_a),
            "invalid spec": lambda: dra.EnrollmentSpec("", ()),
            "not enrolled": lambda: registry.create("SYN-ZZ", RUN),
            "wrong run": lambda: registry.list_run("other"),
            "create 403": fault("PUT", 403, lambda: registry.create("SYN-A1", RUN)),
            "create timeout": fault("PUT", "timeout", lambda: registry.create("SYN-A1", RUN)),
            "conflict": lambda: registry.create("SYN-A2", RUN),
            "read denied": fault("GET", 403, lambda: registry.run_of("SYN-A1")),
            "read unavailable": fault("GET", 500, lambda: registry.run_of("SYN-A1")),
            "delete 412": fault("DELETE", 412, lambda: registry.delete("SYN-A2", RUN)),
            "list unavailable": fault("GET", "timeout", lambda: registry.list_run(RUN)),
            "credential": lambda: self.registry(credential=failing).run_of("SYN-A1"),
        }
        for label, run in scenarios.items():
            with self.subTest(scenario=label):
                try:
                    raise RuntimeError(caller)
                except RuntimeError:
                    error = self.refused(run)
                text = "".join(traceback.format_exception(error)) + repr(error)
                self.assertNotIn(caller, text)
                self.assertTrue(error.__suppress_context__)
                self.assertIsNone(error.__cause__)


class ClientOwnershipTests(HubCase):
    def test_an_owned_manager_is_closed_exactly_once_and_calls_afterwards_refuse(self) -> None:
        registry = self.registry()
        registry.run_of("SYN-A1")
        manager = registry._manager
        amqp_close = mock.Mock(wraps=manager.amqp_svc_client.disconnect_sync)
        http_close = mock.Mock(wraps=manager.protocol.close)
        manager.amqp_svc_client.disconnect_sync = amqp_close
        manager.protocol.close = http_close
        registry.close()
        registry.close()
        amqp_close.assert_called_once_with()
        http_close.assert_called_once_with()
        self.assertEqual(self.refused(lambda: registry.run_of("SYN-A1")).code, "CLOSED")

    def test_an_injected_client_is_used_bounded_but_never_closed(self) -> None:
        sdk = importlib.import_module("azure.iot.hub")
        manager = sdk.IoTHubRegistryManager.from_token_credential(HOST, self.credential)
        self.addCleanup(manager.amqp_svc_client.disconnect_sync)
        amqp_close = mock.Mock()
        http_close = mock.Mock()
        manager.amqp_svc_client.disconnect_sync = amqp_close
        manager.protocol.close = http_close
        registry = self.registry(client=manager, credential=None, timeout=9)
        self.assertIsNone(registry.run_of("SYN-A1"))
        registry.close()
        amqp_close.assert_not_called()
        http_close.assert_not_called()
        (get,) = self.hub.requests
        self.assertEqual((get.retries, get.kwargs["timeout"]), (0, 9.0))
        self.assertEqual(len(self.credential.calls), 2)


class ExistingProtocolIntegrationTests(HubCase):
    def manifest(self) -> di.Manifest:
        return di.plan(RUN, "owner-role", sensors(3))

    def spec_for(self, manifest: di.Manifest) -> dra.EnrollmentSpec:
        return dra.EnrollmentSpec(
            RUN,
            tuple(
                dra.X509Enrollment(i.device_id, thumb(n + 1))
                for n, i in enumerate(manifest.identities)
            ),
        )

    def test_provision_and_teardown_run_through_the_real_sdk_path(self) -> None:
        manifest = self.manifest()
        registry, store = self.registry(self.spec_for(manifest)), FakeStore()
        issued = di.provision(manifest, registry, store)
        self.assertEqual(len(store.references()), 3)
        self.assertEqual(len(issued.identities), 3)
        self.assertEqual(sorted(self.hub.devices), sorted(i.device_id for i in manifest.identities))
        self.assertTrue(all(d["body"]["status"] == "disabled" for d in self.hub.devices.values()))
        self.assertTrue(all(s.header("If-None-Match") == "*" for s in self.hub.seen("PUT")))
        di.teardown(issued, registry, store)
        self.assertEqual(self.hub.devices, {})
        self.assertTrue(
            all(s.header("If-Match") not in (None, "*") for s in self.hub.seen("DELETE"))
        )
        self.assertEqual(len(self.hub.seen("DELETE")), 3)

    def test_failed_provision_rolls_back_only_the_run_owned_identities(self) -> None:
        manifest = self.manifest()

        class Failing(FakeStore):
            def issue(self, device_id: str, run_id: str) -> str:
                if len(self.secrets) == 2:
                    raise RuntimeError(SECRET)
                return super().issue(device_id, run_id)

        registry = self.registry(self.spec_for(manifest))
        error = self.refused_identity(lambda: di.provision(manifest, registry, Failing()))
        self.assertEqual(str(error), "PROVISION_FAILED_ROLLED_BACK")
        self.assertEqual(self.hub.devices, {})

    def test_a_foreign_same_id_identity_conflicts_and_survives_rollback(self) -> None:
        manifest = self.manifest()
        self.hub.put_device(manifest.identities[1].device_id, "someone else", status="enabled")
        before = json.dumps(self.hub.devices, sort_keys=True)
        registry = self.registry(self.spec_for(manifest))
        error = self.refused_identity(lambda: di.provision(manifest, registry, FakeStore()))
        self.assertEqual(str(error), "PROVISION_FAILED_ROLLED_BACK")
        self.assertEqual(json.dumps(self.hub.devices, sort_keys=True), before)

    def test_whole_run_teardown_refuses_with_a_hidden_marked_identity_and_deletes_nothing(
        self,
    ) -> None:
        manifest = self.manifest()
        registry, store = self.registry(self.spec_for(manifest)), FakeStore()
        issued = di.provision(manifest, registry, store)
        self.hub.put_device("SYN-HIDDEN-1", MARKER)
        self.hub.list_omits_reason = True
        before = json.dumps(self.hub.devices, sort_keys=True)
        error = self.refused_identity(lambda: di.teardown(issued, registry, store))
        self.assertEqual(str(error), "TEARDOWN_MANIFEST_INCOMPLETE:1")
        self.assertEqual(self.hub.seen("DELETE"), [])
        self.assertEqual(json.dumps(self.hub.devices, sort_keys=True), before)

    def refused_identity(self, call: Callable[[], object]) -> di.DeviceIdentityError:
        with self.assertRaises(di.DeviceIdentityError) as caught:
            call()
        return caught.exception


if __name__ == "__main__":
    unittest.main()
