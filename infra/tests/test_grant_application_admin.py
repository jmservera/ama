import importlib.util
import sys
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
    def run_grant(self, graph, *, apply, tenant=TENANT, perms=("AppRoleAssignment.ReadWrite.All",)):
        with mock.patch.object(grant.setup, "token_permissions", side_effect=lambda g, t=None: (
                (_ for _ in ()).throw(grant.SetupError("different tenant")) if t and t != TENANT else set(perms))):
            return grant.grant(graph, tenant, APP, "admin@example.test", apply=apply)

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
        ]
        for graph, kw in cases:
            with self.subTest(kw=kw), mock.patch.object(grant.setup, "authority_help"):
                with self.assertRaises(grant.SetupError):
                    self.run_grant(graph, apply=True, **kw)
            self.assertEqual(graph.posts, [])


if __name__ == "__main__":
    unittest.main()
