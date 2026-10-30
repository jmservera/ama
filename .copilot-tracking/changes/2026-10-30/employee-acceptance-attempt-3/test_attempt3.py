"""Offline constructed safety tests; no credential reads or browser launches."""

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from attempt3 import (
    APP,
    BINDING_JS,
    Deadline,
    RunGuard,
    allowed,
    authenticate,
    booleans,
    method_action,
    parse_credentials,
    sanitize,
    submit_secret,
)


class SafetyTests(unittest.TestCase):
    def test_first_line_password_second_line_tap(self):
        self.assertEqual(
            parse_credentials("  fake-password  \n  fake-tap \n"),
            ("fake-password", "fake-tap"),
        )
        self.assertEqual(
            parse_credentials("fake-password\n\n"), ("fake-password", None)
        )
        self.assertEqual(
            parse_credentials("Password: fake-password\nTAP=fake-tap"),
            ("fake-password", "fake-tap"),
        )

    def test_missing_first_line_refused(self):
        for raw in ("", " \nsecond", '{"password":"fake"}'):
            with self.assertRaises(ValueError):
                parse_credentials(raw)

    def test_exact_origins(self):
        self.assertTrue(allowed(APP + "/app", app=True))
        self.assertTrue(allowed("https://login.microsoft.com/"))
        for url in (
            "http://login.microsoft.com/",
            "https://login.microsoft.com.attacker.invalid/",
            "https://user@login.microsoft.com/",
            "https://login.microsoft.com:444/",
            "https://login.microsoft.com:bad/",
        ):
            self.assertFalse(allowed(url))
        self.assertFalse(allowed("https://login.microsoft.com/", app=True))

    def test_redact_both_secrets_and_encoded_variants(self):
        text = sanitize(
            "x+y-secret x%2By-secret fake-tap https://example.invalid/?token=x a@b.invalid",
            ("x+y-secret", "fake-tap"),
        )
        for forbidden in ("x+y-secret", "x%2By-secret", "fake-tap", "a@b", "https://"):
            self.assertNotIn(forbidden, text)

    def test_boolean_projection_refuses_nonbooleans(self):
        self.assertEqual(booleans({"a": True, "b": False}), {"a": True, "b": False})
        for value in ({"x": 1}, {"x": "text"}, {"x": []}, {"x": {}}, {}, []):
            with self.assertRaises(ValueError):
                booleans(value)

    def test_supported_tap_route_priority(self):
        self.assertEqual(
            method_action(
                ["Use your password instead", "Temporary Access Pass"], set(), True
            ),
            ("tap", "Temporary Access Pass"),
        )
        self.assertIsNone(method_action(["Sign in with GitHub"], set(), True))
        self.assertIsNone(method_action(["Temporary Access Pass"], set(), False))
        self.assertIsNone(
            method_action(["Password"], {("password", "Password")}, False)
        )

    def test_deadline_rechecked_after_wait(self):
        clock = Mock(side_effect=[0, 0.9, 1.1])
        deadline = Deadline(1, clock)
        page = Mock()
        with self.assertRaises(TimeoutError):
            deadline.pause(page, 1000)
        self.assertLessEqual(page.wait_for_timeout.call_args.args[0], 100)

    def test_manifest_interruption_and_competing_invocations_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "manifest.json"
            guard = RunGuard(path, "constructed-hash")
            guard.admit()
            with self.assertRaises(FileExistsError):
                RunGuard(path, "constructed-hash")
            self.assertEqual(len(json.loads(path.read_text())["attempts"]), 1)
            with self.assertRaises(ValueError):
                guard.admit()

    def test_task_attempt_cap(self):
        with tempfile.TemporaryDirectory() as temp:
            guard = RunGuard(Path(temp) / "manifest.json", "constructed-hash")
            for _ in range(2):
                guard.admit()["status"] = "definitive_rejection"
                guard.save()
            with self.assertRaises(ValueError):
                guard.admit()

    def test_completed_precredential_continuation_uses_only_remaining_slot(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            snapshot = root / "attempt3-first-run.py.txt"
            snapshot.write_text("constructed source")
            digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
            path = root / "manifest.json"
            guard = RunGuard(path, digest)
            attempt = guard.admit()
            attempt["status"] = "browser_or_route_failure_stop"
            evidence = root / "attempt3-evidence.json"
            evidence.write_text(json.dumps({"attempts": guard.data["attempts"]}))
            guard.data.update(
                status="completed",
                evidence=evidence.name,
                evidence_sha256=hashlib.sha256(evidence.read_bytes()).hexdigest(),
            )
            guard.save()
            resumed = RunGuard.continue_completed_precredential(path, "new-source")
            self.assertEqual(resumed.admit()["number"], 2)
            with self.assertRaises((ValueError, BlockingIOError)):
                RunGuard.continue_completed_precredential(path, "new-source")
            resumed.data["attempts"][-1]["status"] = "definitive_rejection"
            with self.assertRaises(ValueError):
                resumed.admit()
            resumed.lock_stream.close()

    def test_continuation_refuses_unknown_or_interrupted_state(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "manifest.json"
            guard = RunGuard(path, "constructed-hash")
            guard.admit()
            with self.assertRaises(ValueError):
                RunGuard.continue_completed_precredential(path, "new-source")
            guard.data["status"] = "completed"
            guard.data["attempts"][0].update(
                status="browser_or_route_failure_stop",
                username_submission_attempted=True,
            )
            guard.save()
            with self.assertRaises(ValueError):
                RunGuard.continue_completed_precredential(path, "new-source")

    def test_submit_error_keeps_durable_unknown_intent(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "manifest.json"
            guard = RunGuard(path, "constructed-hash")
            attempt = guard.admit()
            page, field, submit = Mock(), Mock(), Mock()
            page.url = "https://login.microsoftonline.com/"
            submit.press.side_effect = TimeoutError()
            with self.assertRaises(TimeoutError):
                submit_secret(
                    page, field, submit, "fake", attempt, guard, Deadline(), "password"
                )
            stored = json.loads(path.read_text())["attempts"][0]
            self.assertTrue(stored["submission_attempted"])
            self.assertTrue(stored["credential_fill_completed"])
            self.assertEqual(stored["submission_delivery"], "unknown")
            with self.assertRaises(ValueError):
                submit_secret(
                    page, field, submit, "fake", attempt, guard, Deadline(), "password"
                )
            with self.assertRaises(FileExistsError):
                RunGuard(path, "constructed-hash")

    def test_fill_error_never_claims_completed_fill(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "manifest.json"
            guard = RunGuard(path, "constructed-hash")
            attempt = guard.admit()
            page, field = Mock(), Mock()
            page.url = "https://login.microsoftonline.com/"
            field.fill.side_effect = TimeoutError()
            with self.assertRaises(TimeoutError):
                submit_secret(
                    page, field, Mock(), "fake", attempt, guard, Deadline(), "password"
                )
            stored = json.loads(path.read_text())["attempts"][0]
            self.assertTrue(stored["credential_fill_attempted"])
            self.assertFalse(stored["credential_fill_completed"])
            self.assertFalse(stored["submission_attempted"])

    def test_expired_budget_prevents_secret_fill(self):
        deadline = Deadline(1, Mock(side_effect=[0, 2]))
        attempt = {"submission_attempted": False}
        page, field = Mock(), Mock()
        page.url = "https://login.microsoftonline.com/"
        with self.assertRaises(TimeoutError):
            submit_secret(page, field, Mock(), "fake", attempt, Mock(), deadline, "tap")
        field.fill.assert_not_called()

    def test_binding_requires_independent_expected_identity_contract(self):
        for fragment in (
            "r.status === 200",
            "!r.redirected",
            "application/json",
            "expected.toLowerCase()",
            "trusted-proxy",
            "ZavaForward.ProgrammeManager",
            "u?.view_only === false",
            "guid(u.tid)",
            "guid(u.oid)",
        ):
            self.assertIn(fragment, BINDING_JS)

    def test_decoy_password_on_username_page_is_never_filled(self):
        page, email, submit, secret = Mock(), Mock(), Mock(), Mock()
        page.url = "https://login.microsoftonline.com/"
        email.count.return_value = submit.count.return_value = (
            secret.count.return_value
        ) = 1
        submit.get_attribute.return_value = "Next"
        page.get_by_role.return_value.all_text_contents.return_value = ["Sign in"]
        page.locator.side_effect = lambda selector: (
            email
            if 'type="email"' in selector
            else submit
            if 'type="submit"' in selector
            else secret
        )
        attempt = {"submission_attempted": False}
        with patch(
            "attempt3.public_state", return_value={"text": "Sign in", "controls": []}
        ):
            self.assertEqual(
                authenticate(page, "fake", None, attempt, Mock()),
                "credential_route_not_offered",
            )
        secret.fill.assert_not_called()

    def test_binding_projection_executes_against_constructed_contracts(self):
        program = """
        const probe = BINDING;
        const valid = {user:{code:'derived',email:'derived@invalid',tid:'00000000-0000-0000-0000-000000000001',
          oid:'00000000-0000-0000-0000-000000000002',view_only:false,app_roles:['ZavaForward.ProgrammeManager'],
          role:'Retrofit Programme Manager',auth_provider:'trusted-proxy'},
          account:{email:'fixture@invalid',provider:'trusted-proxy'}};
        async function run(d, options={}) {
          global.fetch=async()=>({status:200,redirected:false,
            headers:{get:()=> 'application/json'},json:async()=>d,...options});
          return await probe({expected:'fixture@invalid',timeoutMs:8000});
        }
        (async()=>{
          const outcomes=[];
          const good=await run(valid);
          outcomes.push(good.authenticated && !good.rosterBound);
          for(const mutate of [
            d=>{d.account.email='wrong@invalid'},
            d=>{d.user.role='Contractor'},
            d=>{d.user.view_only=true},
            d=>{d.account.provider='password'},
            d=>{d.user.oid='not-guid'},
            d=>{delete d.user}
          ]){
            const d=structuredClone(valid);mutate(d);
            outcomes.push(!(await run(d)).authenticated);
          }
          for(const options of [
            {status:401},{redirected:true},{headers:{get:()=> 'text/html'}}
          ])outcomes.push(!(await run(valid,options)).authenticated);
          process.stdout.write(JSON.stringify(outcomes));
        })().catch(()=>process.exit(1));
        """.replace("BINDING", BINDING_JS)
        result = subprocess.run(
            ["node", "-e", program], check=True, capture_output=True, text=True
        )
        self.assertTrue(all(json.loads(result.stdout)))


if __name__ == "__main__":
    unittest.main()
