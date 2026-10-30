"""Offline constructed safety tests; no credential reads or browser launch."""

import contextlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "acceptance", Path(__file__).with_name("acceptance.py")
)
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class SafetyTests(unittest.TestCase):
    def test_second_launch_requires_verified_first_cleanup_and_kmsi(self):
        spec = importlib.util.spec_from_file_location(
            "attempt2", Path(__file__).parent / "second" / "attempt2.py"
        )
        assert spec and spec.loader
        second = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(second)
        self.assertEqual(second.verify_first(), second.EXPECTED)
        with tempfile.TemporaryDirectory() as tmp:
            second.FIRST = Path(tmp)
            for name in second.EXPECTED:
                (second.FIRST / name).write_text("constructed altered provenance")
            with self.assertRaises(ValueError):
                second.verify_first()

    def test_literal_trim_only(self):
        self.assertEqual(runner.credentials(" [literal:pw] \n"), ("[literal:pw]",))
        self.assertEqual(
            runner.credentials("person@example.test\npassword:literal\n", True),
            ("person@example.test", "password:literal"),
        )
        for raw in ("", "one\ntwo", " \n"):
            with self.assertRaises(ValueError):
                runner.credentials(raw)

    def test_origin_guard(self):
        for url in (
            "http://login.microsoftonline.com",
            "https://login.microsoftonline.com.evil.test",
            "https://secret@login.microsoftonline.com",
            "https://login.microsoftonline.com:444",
        ):
            self.assertFalse(runner.allowed(url, runner.PROVIDERS))
        self.assertTrue(
            runner.allowed(
                "https://login.microsoftonline.com/a?secret=canary", runner.PROVIDERS
            )
        )

    def test_diagnostics_rejected(self):
        runner.diagnostics_guard({})
        for key in ("DEBUG", "PWDEBUG", "PLAYWRIGHT_DEBUG", "DEBUG_FILE"):
            with self.assertRaises(ValueError):
                runner.diagnostics_guard({key: "canary"})

    def test_secret_output_refused_without_emission(self):
        output = io.StringIO()
        with (
            contextlib.redirect_stdout(output),
            contextlib.redirect_stderr(output),
            self.assertRaises(ValueError),
        ):
            runner.safe_json({"error": "https://fake.test/?pw=CANARY"}, ["CANARY"])
        self.assertEqual(output.getvalue(), "")

    def test_durable_admission_and_restart_refusal(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            guard = runner.Guard(path)
            entry = guard.admit("employee")
            disk = json.loads(path.read_text())
            self.assertEqual(disk["attempts"]["employee"][0]["number"], 1)
            with self.assertRaises(FileExistsError):
                runner.Guard(path)
            guard.submit(entry)
            self.assertTrue(
                json.loads(path.read_text())["attempts"]["employee"][0][
                    "submission_intent"
                ]
            )
            with self.assertRaises(ValueError):
                guard.submit(entry)
            with self.assertRaises(ValueError):
                guard.admit("employee")

    def test_cap_and_independent_sites(self):
        with tempfile.TemporaryDirectory() as tmp:
            guard = runner.Guard(Path(tmp) / "manifest.json")
            guard.admit("resident")
            guard.admit("resident")
            with self.assertRaises(ValueError):
                guard.admit("resident")
            self.assertEqual(guard.admit("employee")["number"], 1)

    def test_failure_status_does_not_emit_exception(self):
        with tempfile.TemporaryDirectory() as tmp:
            previous = runner.OUT
            runner.OUT = Path(tmp)
            try:
                evidence = runner.Evidence()

                def fail():
                    raise RuntimeError("CANARY https://evil.test/?secret=CANARY")

                self.assertIsNone(evidence.step("constructed failure", fail))
                text = (runner.OUT / "evidence.json").read_text()
                self.assertNotIn("CANARY", text)
                self.assertIn("operation_failed_unproven", text)
            finally:
                runner.OUT = previous

    def test_strict_binding_projection(self):
        js = """
          const valid={user:{code:'staff',email:'roster@example.test',
            tid:'12345678-1234-1234-1234-123456789012',
            oid:'12345678-1234-1234-1234-123456789013',
            view_only:false,app_roles:['ZavaForward.ProgrammeManager'],
            role:'Retrofit Programme Manager',auth_provider:'trusted-proxy'},
            account:{email:'expected@example.test',provider:'trusted-proxy'}};
          global.fetch=async()=>({status:200,redirected:false,
            headers:{get:()=> 'application/json'},json:async()=>payload});
          const check=CHECK;
          (async()=>{
            let payload=valid;
            global.fetch=async()=>({status:200,redirected:false,
              headers:{get:()=> 'application/json'},json:async()=>payload});
            if(!(await check('expected@example.test')).authenticated)process.exit(1);
            for(const mutate of [
              p=>p.user.view_only='false',
              p=>p.account.email='wrong@example.test',
              p=>p.user.role='Contractor',
              p=>p.account.provider='demo',
              p=>delete p.user.oid
            ]){
              payload=JSON.parse(JSON.stringify(valid)); mutate(payload);
              const out=await check('expected@example.test');
              if(out.authenticated||Object.values(out).some(v=>typeof v!=='boolean'))
                process.exit(2);
            }
          })().catch(()=>process.exit(3));
        """.replace("CHECK", runner.BINDING)
        result = subprocess.run(["node", "-e", js], capture_output=True, check=False)
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
