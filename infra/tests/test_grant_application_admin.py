import base64
import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
spec = importlib.util.spec_from_file_location("grant_application_admin", SCRIPTS / "grant-application-admin.py")
grant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grant)

TENANT = "11111111-1111-1111-1111-111111111111"
APP = "22222222-2222-2222-2222-222222222222"
SP = "33333333-3333-3333-3333-333333333333"
ROLE = "44444444-4444-4444-4444-444444444444"
USER = "55555555-5555-5555-5555-555555555555"
OTHER_ROLE = "66666666-6666-6666-6666-666666666666"


class FakeGraph:
    def __init__(self, *, sps=None, user=None, assigned=(), roles=None):
        self.sps = sps if sps is not None else [{"id": SP, "appId": APP, "appRoles": roles if roles is not None else [
            {"id": ROLE, "value": grant.ROLE_VALUE, "isEnabled": True, "allowedMemberTypes": ["User"]}]}]
        self.user = user or {"id": USER, "accountEnabled": True, "userType": "Member"}
        self.assigned = list(assigned)
        self.posts = []

    def rest(self, url, method="GET", body=None, etag=None):
        if method == "POST":
            self.posts.append(body)
            self.assigned.append(dict(body))
            return {}
        return {"value": self.sps} if "servicePrincipals" in url else self.user

    def pages(self, path):
        return list(self.assigned)


class GrantTests(unittest.TestCase):
    def run_grant(self, graph, *, apply, tenant=TENANT, perms=("AppRoleAssignment.ReadWrite.All",), expected=USER):
        with mock.patch.object(grant.setup, "token_permissions", side_effect=lambda g, t=None: (
                (_ for _ in ()).throw(grant.SetupError("different tenant")) if t and t != TENANT else set(perms))):
            return grant.grant(graph, tenant, APP, "admin@example.test", expected, apply=apply)

    def test_dry_run_writes_nothing_and_apply_adds_one_assignment(self):
        g = FakeGraph()
        self.assertEqual(self.run_grant(g, apply=False), "would-assign")
        self.assertEqual(g.posts, [])
        self.assertEqual(self.run_grant(g, apply=True), "assigned")
        self.assertEqual(g.posts, [{"principalId": USER, "resourceId": SP, "appRoleId": ROLE}])

    def test_idempotent_and_preserves_other_assignments(self):
        other = {"principalId": USER, "appRoleId": OTHER_ROLE}
        g = FakeGraph(assigned=[other])
        self.assertEqual(self.run_grant(g, apply=True), "assigned")
        self.assertIn(other, g.assigned)
        self.assertEqual(self.run_grant(g, apply=True), "already-assigned")
        self.assertEqual(len(g.posts), 1)

    def test_refuses_wrong_tenant_app_role_principal_and_missing_authority(self):
        cases = [
            (FakeGraph(), dict(tenant="99999999-9999-9999-9999-999999999999")),
            (FakeGraph(sps=[]), {}),
            (FakeGraph(sps=[{"id": SP, "appId": APP, "appRoles": []}] * 2), {}),
            (FakeGraph(roles=[]), {}),
            (FakeGraph(roles=[{"id": ROLE, "value": grant.ROLE_VALUE, "isEnabled": False, "allowedMemberTypes": ["User"]}]), {}),
            (FakeGraph(user={"id": USER, "accountEnabled": False, "userType": "Member"}), {}),
            (FakeGraph(user={"id": USER, "accountEnabled": True, "userType": "Guest"}), {}),
            (FakeGraph(), dict(perms=("User.Read",))),
            (FakeGraph(), dict(expected="77777777-7777-7777-7777-777777777777")),
        ]
        for graph, kw in cases:
            with self.subTest(kw=kw), mock.patch.object(grant.setup, "authority_help"):
                with self.assertRaises(grant.SetupError):
                    self.run_grant(graph, apply=True, **kw)
            self.assertEqual(graph.posts, [])

    def test_dry_run_a_then_apply_b_cannot_assign_a_different_person(self):
        g = FakeGraph(user={"id": "88888888-8888-8888-8888-888888888888", "accountEnabled": True, "userType": "Member"})
        for apply in (False, True):
            with self.assertRaises(grant.SetupError):
                self.run_grant(g, apply=apply)
        self.assertEqual(g.posts, [])


class OfflineAz:
    """Stands in for the az executable so the real Azure transport and body files are exercised."""

    def __init__(self, *, roles=("AppRoleAssignment.ReadWrite.All",), fail_post=False):
        claims = base64.urlsafe_b64encode(json.dumps({"tid": TENANT, "roles": list(roles)}).encode()).decode().rstrip("=")
        self.token = f"x.{claims}.y"
        self.fail_post = fail_post
        self.assigned = []
        self.bodies = []
        self.calls = []

    def run(self, argv, **kwargs):
        self.calls.append(argv)
        out = lambda value, code=0: subprocess.CompletedProcess(argv, code, json.dumps(value), "" if not code else "boom")
        if argv[1] == "account":
            return out({"accessToken": self.token})
        method, url = argv[argv.index("--method") + 1], argv[argv.index("--url") + 1]
        if method == "POST":
            path = argv[argv.index("--body") + 1].lstrip("@")
            self.bodies.append(path)
            if self.fail_post:
                return out({}, 1)
            self.assigned.append(json.load(open(path)))
            return out({})
        if url.endswith("/appRoleAssignedTo"):
            return out({"value": list(self.assigned)})
        if "servicePrincipals" in url:
            return out({"value": [{"id": SP, "appId": APP, "appRoles": [
                {"id": ROLE, "value": grant.ROLE_VALUE, "isEnabled": True, "allowedMemberTypes": ["User"]}]}]})
        return out({"id": USER, "accountEnabled": True, "userType": "Member"})


class GrantCliTests(unittest.TestCase):
    def setUp(self):
        self.profile = tempfile.mkdtemp(prefix="grant-cli-")
        self.addCleanup(lambda: __import__("shutil").rmtree(self.profile, ignore_errors=True))

    def cli(self, az, *extra, profile=None):
        argv = ["--tenant", TENANT, "--app-id", APP, "--upn", "admin@example.test", "--expected-oid", USER,
                "--tenant-profile", profile or self.profile, *extra]
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(grant.setup.subprocess, "run", side_effect=az.run), \
                mock.patch.object(grant.setup.time, "sleep"), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = grant.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_apply_entrypoint_writes_through_a_removed_temporary_body(self):
        az = OfflineAz()
        code, out, _ = self.cli(az, "--apply")
        self.assertEqual((code, out.strip()), (0, "result: assigned"))
        self.assertEqual(az.assigned, [{"principalId": USER, "resourceId": SP, "appRoleId": ROLE}])
        self.assertEqual(len(az.bodies), 1)
        self.assertTrue(az.bodies[0].startswith(self.profile + os.sep))
        self.assertEqual(os.listdir(self.profile), [])
        self.assertEqual(self.cli(az, "--apply")[1].strip(), "result: already-assigned")
        self.assertEqual(len(az.bodies), 1)

    def test_dry_run_default_issues_no_write_and_needs_no_body_directory(self):
        az = OfflineAz()
        code, out, _ = self.cli(az)
        self.assertEqual((code, out.strip()), (0, "result: would-assign"))
        self.assertEqual(az.bodies, [])
        self.assertFalse(any("POST" in c for c in az.calls))

    def test_missing_write_permission_is_refused_without_a_write(self):
        az = OfflineAz(roles=("User.Read",))
        with mock.patch.object(grant.setup, "authority_help"), contextlib.redirect_stdout(io.StringIO()):
            code, _, err = self.cli(az, "--apply")
        self.assertEqual(code, 1)
        self.assertIn("permission is missing", err)
        self.assertEqual(az.bodies, [])

    def test_failed_write_is_refused_and_leaves_no_body_file(self):
        az = OfflineAz(fail_post=True)
        code, _, err = self.cli(az, "--apply")
        self.assertEqual(code, 1)
        self.assertTrue(err.startswith("refused:"))
        self.assertEqual(len(az.bodies), 1)
        self.assertEqual(os.listdir(self.profile), [])

    def test_apply_refuses_an_unsafe_profile_before_any_az_call(self):
        os.chmod(self.profile, 0o755)
        az = OfflineAz()
        code, _, err = self.cli(az, "--apply")
        self.assertEqual(code, 1)
        self.assertIn("0700", err)
        self.assertEqual(az.calls, [])
        repo_profile = str(grant.setup.REPO / "infra")
        code, _, err = self.cli(az, "--apply", profile=repo_profile)
        self.assertEqual(code, 1)
        self.assertEqual(az.calls, [])

    def test_apply_refuses_a_symlinked_profile_before_any_az_call(self):
        link = os.path.join(tempfile.mkdtemp(prefix="grant-cli-link-"), "profile")
        self.addCleanup(shutil.rmtree, os.path.dirname(link), True)
        os.symlink(self.profile, link)
        az = OfflineAz()
        code, _, err = self.cli(az, "--apply", profile=link)
        self.assertEqual(code, 1)
        self.assertIn("symbolic link", err)
        self.assertEqual(az.calls, [])
        self.assertEqual(os.listdir(self.profile), [])

    def test_output_carries_no_token(self):
        az = OfflineAz()
        _, out, err = self.cli(az, "--apply")
        self.assertNotIn(az.token, out + err)


if __name__ == "__main__":
    unittest.main()
