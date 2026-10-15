"""Issue 116: every role against every endpoint, contractor canaries, free-text notes (synthetic fixtures only)."""
import json
import re
import unittest
from pathlib import Path

from zavaforward_mvp import projection, server
from zavaforward_mvp.assistants import Assistants
from test_role_matrix import Matrix, PHONE, REASON, RESIDENT, ROLES

NOTE_CANARY = "FREETEXT-CANARY-reason-in-a-note"
OUTCOME_CANARY = "OUTCOME-CANARY-reason"

SERVER_SRC = (Path(server.__file__)).read_text()

GET_ENDPOINTS = ["/api/me", "/api/account/photo", "/api/cases?view=all", "/api/cases?view=all&q=Quentin", "/api/cases?view=all&q=" + REASON,
                 "/api/cases.csv?view=all", "/api/cases/ZF-1", "/api/ranking/policy", "/api/ranking/snapshot", "/api/ai/priority",
                 "/api/facets", "/api/stats", "/api/map", "/api/visits?view=all", "/api/funding", "/api/briefing", "/api/audit-check",
                 "/api/handoffs", "/api/packages", "/api/workorders", "/api/checklists", "/api/ai/report", "/api/finance",
                 "/api/governance", "/api/continuity", "/api/continuity/export", "/api/retention", "/api/docs/ZF-1/none",
                 "/api/time/status", "/api/time/mine", "/api/time/report", "/api/law/sources", "/api/law/search?q=x",
                 "/api/assistants", "/api/assistants/proposals", "/api/nothing"]
POST_ENDPOINTS = [("/api/ai/priority", {"n": 3}), ("/api/cases/ZF-1/ai", {"task": "summary"}), ("/api/cases/ZF-1/ai", {"task": "message"}),
                  ("/api/cases/ZF-1/draft", {"kind": "update"}), ("/api/cases/ZF-1/funding-draft", {}), ("/api/cases/ZF-1/read-doc", {}),
                  ("/api/cases/ZF-1/call", {"outcome": "x"}), ("/api/import-check", {"text": "a"}), ("/api/time/acknowledge", {}), ("/api/time/request-enable", {}), ("/api/time/enable", {}),
                  ("/api/ledger/digest", {}), ("/api/assistants/stock-prioritisation/invoke", {"case_id": "ZF-1"}),
                  ("/api/continuity/suspend", {})]


class RoleEndpointInventory(Matrix):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        c = cls.store.cases["ZF-1"]
        c["contacts"].append(dict(at="2026-01-02T10:00", purpose="Update", channel="Phone", direction="Outbound",
                                  outcome=OUTCOME_CANARY, note=NOTE_CANARY, by="User 1"))
        c["hazards"].append(dict(category="Damp", priority="Routine", state="Raised", job="", owner="User 1", released=False,
                                 raised_by="User 1", note=NOTE_CANARY))
        cls.store.audit("u1@example.test", "log_contact", "ZF-1", REASON)

    def email(self, role):
        return next(s["email"] for s in self.store.data["staff"] if s["role"] == role)

    def test_inventory_covers_every_route_in_the_server(self):
        routes = set(re.findall(r'"(/api/[a-z./-]+?)/?"', SERVER_SRC)) | set(re.findall(r'url\.path == "(/api/[a-z./-]+)"', SERVER_SRC))
        routes -= {"/api/login", "/api/logout"}
        tested = {u.split("?")[0].rstrip("/") for u in GET_ENDPOINTS} | {p for p, _ in POST_ENDPOINTS}
        missing = sorted(r for r in routes if not any(t == r or t.startswith(r + "/") for t in tested))
        self.assertEqual(missing, [], "add these routes to the role inventory")

    def test_every_role_against_every_endpoint(self):
        for role in ROLES + ["Mystery"]:
            if role == "Mystery":
                self.store.staff["u0@example.test"]["role"] = "Mystery"
                ck = self.session("u0@example.test")
            else:
                ck = self.session(self.email(role))
            try:
                results = [(p, *self.call(ck, p)) for p in GET_ENDPOINTS] + [(p, *self.call(ck, p, b)) for p, b in POST_ENDPOINTS]
            finally:
                self.store.staff["u0@example.test"]["role"] = ROLES[0]
            for path, code, text in results:
                self.assertNotEqual(code, 500, (role, path))
                if role in ("Mystery", projection.CONTRACTOR) and path not in ("/api/me", "/api/account/photo"):
                    allowed = role == projection.CONTRACTOR and path.split("?")[0] in ("/api/cases", "/api/cases/ZF-1", "/api/workorders")
                    if not allowed and path.split("?")[0] != "/api/cases":
                        self.assertIn(code, (403, 404), (role, path))
                if role not in projection.DEFAULT_REASON_ROLES:
                    self.assertNotIn(REASON, text, (role, path))
                if role == projection.CONTRACTOR:
                    for canary in (REASON, PHONE, RESIDENT, NOTE_CANARY, OUTCOME_CANARY, "adjustment", "priority_support"):
                        self.assertNotIn(canary, text, (role, path, canary))
                if role not in projection.DEFAULT_REASON_ROLES and path.startswith("/api/cases/ZF-1"):
                    self.assertNotIn(NOTE_CANARY, text, (role, path))

    def test_contractor_audit_view_and_export_are_denied(self):
        ck = self.session("u7@example.test")
        for path in ("/api/audit-check", "/api/cases.csv?view=all", "/api/continuity/export", "/api/ai/report", "/api/assistants/proposals"):
            self.assertEqual(self.call(ck, path)[0], 403, path)

    def test_staff_without_need_see_notes_held_but_need_roles_see_them(self):
        for role in ROLES:
            if role == projection.CONTRACTOR:
                continue
            text = self.call(self.session(self.email(role)), "/api/cases/ZF-1")[1]
            if role in projection.DEFAULT_REASON_ROLES:
                self.assertIn(NOTE_CANARY, text, role)
            else:
                self.assertNotIn(NOTE_CANARY, text, role)
                self.assertNotIn(OUTCOME_CANARY, text, role)
                self.assertIn(projection.NOTE_HELD, text, role)

    def test_provider_never_called_for_contractor_and_prompts_carry_no_free_text(self):
        prompts = []
        self.store.ai.endpoint = "http://x"
        self.store.ai._chat = lambda *a, **k: prompts.append(json.dumps(a) + json.dumps(k)) or "Draft."
        self.store.ai.evidence = lambda *a, **k: prompts.append(json.dumps(a) + json.dumps(k)) or ""
        try:
            ck = self.session("u7@example.test")
            for path, body in POST_ENDPOINTS:
                self.call(ck, path, body)
            self.assertEqual(prompts, [])
            for role in ROLES[:-1]:
                if role in projection.DEFAULT_REASON_ROLES:
                    continue
                ck = self.session(self.email(role))
                for path, body in POST_ENDPOINTS:
                    self.call(ck, path, body)
            joined = "".join(prompts)
            for canary in (REASON, NOTE_CANARY, OUTCOME_CANARY):
                self.assertNotIn(canary, joined)
        finally:
            self.store.ai.endpoint = ""
            del self.store.ai._chat
            del self.store.ai.evidence

    def test_assistant_capture_never_carries_reason_or_notes(self):
        from zavaforward_mvp import assistants
        c = self.store.cases["ZF-1"]
        for cap in assistants.REGISTRY:
            text = json.dumps(assistants.capture(cap, c))
            for canary in (REASON, NOTE_CANARY, OUTCOME_CANARY, PHONE, RESIDENT):
                self.assertNotIn(canary, text, cap)


del Matrix
if __name__ == "__main__":
    unittest.main()
