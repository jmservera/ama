"""Offline acceptance checks against constructed authenticated /api/me responses."""

import base64
import json
import subprocess
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from typing import Any, cast

from test_auth import ENV, OID_NEW, OID_SAM, TENANT, Base, principal
from zava_forward.api import auth
from zava_forward.api.server import App, make_handler

EXPECTED = {"tid": TENANT, "oid": OID_NEW, "email": "expected@example.test"}

HARNESS = r"""
const fs = require('node:fs');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const calls = [];
const timeout = AbortSignal.timeout;
AbortSignal.timeout = ms => {
  calls.push({timeout:ms});
  return timeout(ms);
};
global.fetch = async (url, options) => {
  calls.push({url, redirect:options.redirect,
    signal:options.signal instanceof AbortSignal && !options.signal.aborted});
  if(input.fault === 'fetch') throw new Error('PRIVATE_CANARY');
  if(input.fault === 'abort') throw new DOMException('PRIVATE_CANARY', 'AbortError');
  return {
    status:input.status ?? 200, redirected:input.redirected ?? false,
    headers:{get:name => name === 'content-type' ?
      (input.contentType ?? 'application/json') : null},
    json:async () => {
      if(input.fault === 'json') throw new SyntaxError('PRIVATE_CANARY');
      return input.payload;
    }
  };
};
(async () => {
  const check = CHECK;
  const result = await check(input.expected);
  if(calls.length && JSON.stringify(calls) !== JSON.stringify([
    {timeout:120000}, {url:'/api/me',redirect:'error',signal:true}
  ])) throw new Error('request contract');
  process.stdout.write(JSON.stringify(result));
})().catch(() => { process.stderr.write('predicate rejected'); process.exitCode = 1; });
"""


def evaluate(
    binding: str, payload: Any, expected: Any = EXPECTED, **options: Any
) -> dict[str, bool]:
    result = subprocess.run(
        ["node", "-e", HARNESS.replace("CHECK", binding)],
        input=json.dumps(dict(payload=payload, expected=expected, **options)),
        text=True,
        capture_output=True,
        timeout=15,
        check=True,
    )
    if result.stderr or "PRIVATE_CANARY" in result.stdout:
        raise AssertionError("predicate diagnostics escaped")
    projection: dict[str, bool] = json.loads(result.stdout)
    if not projection or any(type(value) is not bool for value in projection.values()):
        raise AssertionError("non-boolean projection")
    return projection


class EmployeeIdentityTests(Base):
    def setUp(self) -> None:
        cast(Any, super()).setUp()
        provider: Any = auth.TrustedProxyProvider
        application: Any = App
        handler: Any = make_handler
        self.httpd = ThreadingHTTPServer(
            ("127.0.0.1", 0), handler(application(self.store, provider=provider(self.store, ENV)))
        )
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}/api/me"

    def tearDown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join()
        cast(Any, super()).tearDown()

    def payload(
        self, *, oid: str = OID_NEW, emails: tuple[str, ...] = (), name: str = ""
    ) -> dict[str, Any]:
        make_principal: Any = principal
        header = make_principal(roles=("ZavaForward.ProgrammeManager",), oid=oid)
        claims = json.loads(base64.b64decode(header))
        claims["claims"].extend(
            {"typ": key, "val": value}
            for key, value in zip(("preferred_username", "email", "upn"), emails, strict=False)
        )
        if name:
            claims["claims"].append({"typ": "name", "val": name})
        request = urllib.request.Request(
            self.url,
            headers={
                "X-MS-CLIENT-PRINCIPAL": base64.b64encode(json.dumps(claims).encode()).decode()
            },
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            self.assertEqual(response.status, 200)
            payload: dict[str, Any] = json.loads(response.read())
        return payload

    def check(self, payload: Any, expected: Any = EXPECTED, **options: Any) -> dict[str, bool]:
        from checks.employee_identity_check import BINDING

        return evaluate(BINDING, payload, expected, **options)

    def test_correct_rosterless_account_needs_no_display_email(self) -> None:
        payload = self.payload()
        self.assertEqual(payload["account"]["email"], "")
        self.assertNotIn("bound", payload["user"])
        result = self.check(payload)
        self.assertTrue(result["authenticated"])
        self.assertTrue(result["expectedIdentity"])
        self.assertFalse(result["displayEmailMatches"])
        self.assertFalse(result["rosterBound"])
        self.assertTrue(self.check(payload, {"tid": TENANT, "oid": OID_NEW})["authenticated"])

    def test_display_alias_multiple_claims_name_and_case_do_not_control_identity(self) -> None:
        for emails, name in (
            (("alias@example.test",), "Other display name"),
            (("expected@example.test", "expected@example.test"), ""),
            (("expected@example.test", "other@example.test"), ""),
            ((" EXPECTED@EXAMPLE.TEST ",), "Expected display name"),
        ):
            with self.subTest(emails=emails, name=name):
                payload = self.payload(emails=emails, name=name)
                result = self.check(
                    payload, dict(EXPECTED, tid=TENANT.upper(), oid=OID_NEW.upper())
                )
                self.assertTrue(result["authenticated"])
                self.assertEqual(
                    result["displayEmailMatches"],
                    len(emails) == 1 and emails[0].strip().lower() == EXPECTED["email"],
                )

    def test_roster_binding_is_optional_metadata(self) -> None:
        payload = self.payload(oid=OID_SAM, emails=("expected@example.test",))
        self.assertIn("bound", payload["user"])
        result = self.check(payload, dict(EXPECTED, oid=OID_SAM))
        self.assertTrue(result["authenticated"])
        self.assertTrue(result["rosterBound"])

    def test_same_display_email_cannot_admit_another_account(self) -> None:
        payload = self.payload(emails=("expected@example.test",))
        invalid_expectations: tuple[Any, ...] = (
            dict(EXPECTED, oid=OID_SAM),
            dict(EXPECTED, tid="99999999-2222-3333-4444-555555555555"),
        )
        for expected in invalid_expectations:
            result = self.check(payload, expected)
            self.assertTrue(result["displayEmailMatches"])
            self.assertFalse(result["expectedIdentity"])
            self.assertFalse(result["authenticated"])

    def test_expected_ids_are_mandatory_and_strict(self) -> None:
        payload = self.payload(emails=("expected@example.test",))
        invalid_expectations: tuple[Any, ...] = (
            None,
            {},
            [],
            "expected@example.test",
            dict(EXPECTED, tid=None),
            dict(EXPECTED, oid="bad"),
            dict(EXPECTED, oid=" " + OID_NEW),
            dict(EXPECTED, oid=OID_NEW + "\n"),
            dict(EXPECTED, oid=1),
        )
        for expected in invalid_expectations:
            with self.subTest(expected=expected):
                result = self.check(payload, expected)
                self.assertFalse(result["expectationValid"])
                self.assertFalse(result["authenticated"])

    def test_schema_provider_role_and_view_only_fail_closed(self) -> None:
        valid = self.payload(emails=("expected@example.test",))
        for key, value in (
            ("tid", None),
            ("oid", "bad"),
            ("oid", OID_NEW + "\n"),
            ("identity_source", "staff"),
            ("code", ""),
            ("email", ""),
            ("app_roles", None),
            ("app_roles", ["ZavaForward.ProgrammeManager", 42]),
            ("app_roles", ["ZavaForward.Coordinator"]),
            ("role", "Contractor"),
            ("auth_provider", "password"),
            ("view_only", "false"),
            ("view_only", True),
        ):
            with self.subTest(key=key, value=value):
                payload = json.loads(json.dumps(valid))
                payload["user"][key] = value
                self.assertFalse(self.check(payload)["authenticated"])
        invalid_accounts: tuple[Any, ...] = (
            None,
            [],
            {},
            {"email": 1, "provider": "trusted-proxy"},
            {"email": "expected@example.test", "provider": "password"},
        )
        for account in invalid_accounts:
            payload = dict(valid, account=account)
            self.assertFalse(self.check(payload)["authenticated"])
        for payload in (None, [], "bad", {}, dict(valid, user=[]), dict(valid, user=None)):
            self.assertFalse(self.check(payload)["authenticated"])

    def test_transport_and_json_failures_are_explicit_and_capture_free(self) -> None:
        payload = self.payload()
        self.assertTrue(
            self.check(payload, contentType="Application/JSON; charset=utf-8")["authenticated"]
        )
        for options in (
            {"status": 401},
            {"status": 500},
            {"redirected": True},
            {"contentType": "text/html"},
            {"contentType": "text/application/json"},
            {"fault": "fetch"},
            {"fault": "abort"},
            {"fault": "json"},
        ):
            with self.subTest(options=options):
                result = self.check(payload, **options)
                self.assertFalse(result["authenticated"])
                self.assertEqual(
                    result["transportFailed"], options.get("fault") in ("fetch", "abort")
                )
                self.assertEqual(result["jsonFailed"], options.get("fault") == "json")


if __name__ == "__main__":
    unittest.main()
