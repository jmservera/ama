"""Full-stack connected same-home profile journey and redaction acceptance tests (Refs #134)."""

from __future__ import annotations

import copy
import http.client
import json
import subprocess
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import dataset
from test_finance_signoffs import STAFF as FINANCE_STAFF
from test_finance_signoffs import lines, person
from test_grant_lifecycle_controls import designate
from test_quality_procurement import EVIDENCE
from test_stock_reconciliation import query
from zava_forward.core import job_pack as jp
from zava_forward.core import journey_acceptance as ja
from zava_forward.core import journey_trace as jt
from zava_forward.core import perspective_walkthroughs as pw
from zava_forward.core import profile_journey_contract as pjc
from zava_forward.core import projection, taskqueues
from zava_forward.core.store import Store
from zava_forward.core.synthetic.resident_preview_fixture import LIMITATIONS

from zava_forward.api.resident_preview.app import ResidentPreview, serve
from zava_forward.api.server import App, make_handler

ROOT = Path(__file__).resolve().parents[3]
WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
HOME = "ZF-1"
SIBLING = "ZF-2"
PASSWORD = "synthetic-password-134"
SECRET_REASON = "SYN-ADJ-SENSORY-77: quiet knock and allow 60 seconds at the door"
SIBLING_MARKER = "SYN-SIBLING-ONLY-ZF2"


def _grants_payload() -> dict[str, Any]:
    return dict(
        fixture=dict(
            id="SYN-SAME-HOME-134",
            synthetic=True,
            disposable=True,
            lineage="Constructed same-home acceptance fixture; no real resident or staff data.",
            limitations=LIMITATIONS,
        ),
        subjects=[dict(subject="SYN-RES-ZF1"), dict(subject="SYN-RES-ZF2")],
        grants=[
            dict(
                grant_id="G-ZF1",
                subject="SYN-RES-ZF1",
                case_id=HOME,
                kind="resident",
                fields=["home", "measures", "progress", "next_step", "appointments", "help"],
                actions=[],
                valid_from="2025-01-01T00:00:00+00:00",
                valid_to="2099-01-01T00:00:00+00:00",
                revoked=False,
            ),
            dict(
                grant_id="G-ZF2",
                subject="SYN-RES-ZF2",
                case_id=SIBLING,
                kind="resident",
                fields=["home", "measures", "progress", "next_step", "appointments", "help"],
                actions=[],
                valid_from="2025-01-01T00:00:00+00:00",
                valid_to="2099-01-01T00:00:00+00:00",
                revoked=False,
            ),
        ],
    )


class _SameHomeStackBase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="zf-same-home-134-")
        base_dir = Path(self.tmp.name)
        data = copy.deepcopy(dataset.DATA)
        staff = copy.deepcopy(FINANCE_STAFF) + [
            person("QI-2", "Quality Inspector"),
            person("PSO-1", "Programme Support Officer"),
            person("CON-2", "Contractor", contractor="Other Supplier Ltd"),
        ]
        for idx in (1, 2):
            staff[idx] = designate(staff[idx])
            for permission in staff[idx]["financial_authority"]["permissions"]:
                permission["route"] = "Warm Homes"
        data["staff"] = staff
        self.u = {s["code"]: s for s in staff}

        home = data["cases"][0]
        home["owner_code"] = "RLO-1"
        home["owner"] = self.u["RLO-1"]["name"]
        home["owner_role"] = "Resident Liaison Officer"
        home["waiting_on"] = self.u["RLO-1"]["name"]
        home["measures"] = "Loft insulation, Cavity wall"
        home["funding_ok"] = True
        home["resident"]["adjustment"] = SECRET_REASON
        home["resident"]["priority_support"] = True
        home["resident"]["phone"] = "07700 900134"
        home["documents"] = [
            dict(
                id=f"SYN-{kind}",
                kind=kind,
                name=f"SYN-{kind}.pdf",
                at="2026-01-01",
                by="Synthetic reviewer",
                scan=dict(status="clean", scanner="Synthetic metadata fixture"),
            )
            for kind in Store.EVIDENCE
        ]

        sibling = data["cases"][1]
        sibling["home"]["address"] = "99 Sibling Walk"
        sibling["home"]["postcode"] = "SB9 9SB"
        sibling["notes"] = [dict(by="Sam", at="2026-01-01", text=SIBLING_MARKER)]

        store_path = base_dir / "dataset.json"
        store_path.write_text(json.dumps(data))
        self.store = Store(str(store_path))

        app_cls: Any = App
        handler_fn: Any = make_handler
        self.app = app_cls(self.store, PASSWORD)
        self.api_server = ThreadingHTTPServer(("127.0.0.1", 0), handler_fn(self.app))
        self.api_base = f"http://127.0.0.1:{self.api_server.server_address[1]}"
        self.api_thread = threading.Thread(target=self.api_server.serve_forever, daemon=True)
        self.api_thread.start()

        self.grants_path = base_dir / "grants.json"
        self.grants_path.write_text(json.dumps(_grants_payload()))
        self.res_app = ResidentPreview(self.store, self.grants_path, "SYN-RES-ZF1", "127.0.0.1", 0)
        self.res_server = serve(self.res_app)
        self.res_thread = threading.Thread(target=self.res_server.serve_forever, daemon=True)
        self.res_thread.start()

        self.sibling_res_app = ResidentPreview(
            self.store, self.grants_path, "SYN-RES-ZF2", "127.0.0.1", 0
        )
        self.sibling_res_server = serve(self.sibling_res_app)
        self.sibling_res_thread = threading.Thread(
            target=self.sibling_res_server.serve_forever, daemon=True
        )
        self.sibling_res_thread.start()

        self.staff_emails_by_role = {
            "Retrofit Programme Manager": self.u["PM-1"]["email"],
            "Retrofit Coordinator": self.u["RC-1"]["email"],
            "Resident Liaison Officer": self.u["RLO-1"]["email"],
            "Building Safety Liaison": self.u["BSL-1"]["email"],
            "Quality Inspector": self.u["QI-2"]["email"],
            "Grants and Evidence Officer": self.u["GEO-1"]["email"],
            "Programme Support Officer": self.u["PSO-1"]["email"],
        }
        self.cookies: dict[str, str] = {}

    def tearDown(self) -> None:
        for srv, thr in (
            (self.sibling_res_server, self.sibling_res_thread),
            (self.res_server, self.res_thread),
            (self.api_server, self.api_thread),
        ):
            srv.shutdown()
            srv.server_close()
            thr.join(5)
        self.tmp.cleanup()

    def api_call(
        self, path: str, cookie: str = "", body: dict[str, Any] | None = None
    ) -> tuple[int, Any, Any]:
        req = Request(
            self.api_base + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Content-Type": "application/json", "Cookie": cookie, "X-ZF-CSRF": "1"},
        )
        try:
            with urlopen(req, timeout=5) as resp:
                return resp.status, json.loads(resp.read()), resp.headers
        except HTTPError as exc:
            return exc.code, json.loads(exc.read() or b"{}"), {}

    def login(self, email: str) -> str:
        if email not in self.cookies:
            code, _, headers = self.api_call(
                "/api/login", body={"email": email, "password": PASSWORD}
            )
            self.assertEqual(code, 200, email)
            self.cookies[email] = str(headers["Set-Cookie"]).split(";")[0]
        return self.cookies[email]

    def resident_http_view(self, port: int | None = None) -> tuple[int, dict[str, Any]]:
        target = port if port is not None else self.res_app.port
        conn = http.client.HTTPConnection("127.0.0.1", target, timeout=5)
        try:
            conn.request("GET", "/resident/view", headers={"Host": f"127.0.0.1:{target}"})
            resp = conn.getresponse()
            return resp.status, json.loads(resp.read())
        finally:
            conn.close()

    def capture_http_bundle(
        self,
        *,
        work_order_id: str | None = None,
        job_pack_receipt: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        staff_views: dict[str, Any] = {}
        for role, email in self.staff_emails_by_role.items():
            code, body, _ = self.api_call(f"/api/cases/{HOME}", self.login(email))
            self.assertEqual(code, 200, role)
            staff_views[role] = body

        con_cookie = self.login(self.u["CON-1"]["email"])
        code, con_list, _ = self.api_call("/api/cases?view=all&limit=20&offset=0", con_cookie)
        self.assertEqual(code, 200)
        con_summary = next((r for r in con_list["items"] if r.get("id") == HOME), None)
        code, con_detail, _ = self.api_call(f"/api/cases/{HOME}", con_cookie)
        self.assertEqual(code, 200)
        code, con_orders_resp, _ = self.api_call(f"/api/workorders?case={HOME}", con_cookie)
        self.assertEqual(code, 200)
        con_orders = (
            con_orders_resp["items"] if isinstance(con_orders_resp, dict) else con_orders_resp
        )

        pack = None
        if work_order_id:
            pm_cookie = self.login(self.u["PM-1"]["email"])
            code, pack, _ = self.api_call(f"/api/workorders/{work_order_id}/job-pack", pm_cookie)
            self.assertEqual(code, 200)

        rstatus, rview = self.resident_http_view()
        self.assertEqual(rstatus, 200)
        trace = jt.journey_trace(list(self.store.audit_entries()), HOME)
        return dict(
            case_id=HOME,
            staff=staff_views,
            staff_views=staff_views,
            contractor_summary=con_summary,
            contractor_detail=con_detail,
            work_orders=con_orders,
            job_pack=pack,
            job_pack_receipt=job_pack_receipt,
            resident_view=rview,
            audit_trace=trace,
        )


class SameHomeApiAndResidentPortalWalkTests(_SameHomeStackBase):
    def test_http_and_resident_portal_same_home_walk_and_rbac_boundaries(self) -> None:
        u = self.u
        transitions: list[dict[str, Any]] = []

        # Unassigned contractor CON-2 cannot read ZF-1 (404) or its work orders ([]).
        unassigned_cookie = self.login(u["CON-2"]["email"])
        self.assertEqual(self.api_call(f"/api/cases/{HOME}", unassigned_cookie)[0], 404)
        code, unassigned_orders, _ = self.api_call(
            f"/api/workorders?case={HOME}", unassigned_cookie
        )
        self.assertEqual(code, 200)
        items = (
            unassigned_orders["items"] if isinstance(unassigned_orders, dict) else unassigned_orders
        )
        self.assertEqual(items, [])

        # Step 0: stock conflict reconciled and free-text handoff offered (held for redacted roles).
        q = query()
        q["query_owner"] = u["PM-1"]["email"]
        self.store.stock_reconcile(u["PM-1"], HOME, q)
        self.store.stock_query_event(
            u["PM-2"],
            HOME,
            dict(query_id="SQ-1", action="resolve", reason="Constructed", evidence="SYN-1"),
        )
        meta = dataset.change_metadata(self.store, HOME)
        meta["next_action"] = "Confirm sensory access plan before design visit"
        self.store.offer_handoff(
            u["RLO-1"], HOME, u["RC-1"]["email"], "Coordinate technical design", metadata=meta
        )
        step0 = self.capture_http_bundle()
        self.assertEqual(
            step0["staff"]["Resident Liaison Officer"]["work"]["next_action"],
            "Confirm sensory access plan before design visit",
        )
        self.assertEqual(
            step0["staff"]["Retrofit Coordinator"]["work"]["next_action"],
            projection.NOTE_HELD,
        )
        transitions.append(step0)

        # Step 1: handoff accepted & completed, technical sign-offs, resident scope & Accepted,
        # work order issued & appointed, staff-mediated job pack & receipt recorded.
        self.store.accept_handoff(
            u["RC-1"], HOME, metadata=dataset.change_metadata(self.store, HOME)
        )
        self.store.technical_action(
            u["RC-1"], HOME, dict(action="design_submit", note="Loft and cavity wall")
        )
        self.store.technical_action(u["QI-1"], HOME, dict(action="signoff_give", type="assessment"))
        self.store.technical_action(u["RC-2"], HOME, dict(action="signoff_give", type="design"))
        self.store.technical_action(u["BSL-1"], HOME, dict(action="signoff_give", type="building"))
        self.store.complete_handoff(u["RC-1"], HOME, "Technical sign-offs complete")
        self.store.offer_handoff(
            u["RC-1"],
            HOME,
            u["RLO-1"]["email"],
            "Record resident scope and answer",
            metadata=dataset.change_metadata(self.store, HOME),
        )
        self.store.accept_handoff(
            u["RLO-1"], HOME, metadata=dataset.change_metadata(self.store, HOME)
        )
        self.store.complete_handoff(u["RLO-1"], HOME, "Ready for resident choice")
        design_ver = self.store.cases[HOME]["technical"]["design_version"]
        self.store.resident_action(
            u["RLO-1"],
            HOME,
            dict(
                action="scope_record",
                measure="Loft insulation",
                scope="Synthetic loft scope",
                design_version=design_ver,
                source="Synthetic supplied scope",
            ),
        )
        self.store.resident_action(
            u["RLO-1"],
            HOME,
            dict(
                action="decision_record",
                measure="Loft insulation",
                status="Accepted",
                answered_by="The resident",
                context_revision=1,
                source="Synthetic supplied resident statement",
            ),
        )
        pid = self.store.create_package(
            u["PM-1"],
            "Warm Homes Wave 1",
            "2026-01-01",
            "2099-12-31",
            "Loft insulation works",
            "C-1",
            "SYN-1",
        )
        cap_details = dataset.supplied_contract_fixture(self.store, pid, u["PM-1"], "Test Ltd")
        self.store.set_capacity(u["PM-1"], pid, "Test Ltd", 2, 1, "SYN-CAP-1", details=cap_details)
        wid = self.store.issue_work_order(
            u["PM-1"],
            pid,
            HOME,
            scope="Loft insulation only",
            resident_bindings=[dict(measure="Loft insulation", context_revision=1)],
        )
        dataset.supplied_appointment_fixture(self.store, u["PM-1"], wid, when="2099-01-01")
        self.store.record_wo_appointment(u["PM-1"], wid, "Booked", "2099-01-01")

        # Assigned Contractor CON-1 is denied staff-only /job-pack endpoint (403).
        con_cookie = self.login(u["CON-1"]["email"])
        self.assertEqual(self.api_call(f"/api/workorders/{wid}/job-pack", con_cookie)[0], 403)

        _, pack, _ = self.api_call(
            f"/api/workorders/{wid}/job-pack", self.login(u["PM-1"]["email"])
        )
        raw_receipt = jp.worker_receipt(
            pack,
            "Loft insulation",
            EVIDENCE,
            confirmed_by="Kim Builder",
            confirmed=True,
            capture_ref="SYN-HTTP-REC-1",
            captured_at="2026-03-01T10:00:00+00:00",
            recorded_by={"email": u["RLO-1"]["email"], "role": u["RLO-1"]["role"]},
        )
        receipt = jp.acknowledge_receipt(raw_receipt, u["RLO-1"], "2026-03-01T10:05:00+00:00")
        transitions.append(self.capture_http_bundle(work_order_id=wid, job_pack_receipt=receipt))

        # Step 2: work order completed, quality accepted independently, handed over, invoice paid.
        self.store.complete_work_order(u["PM-1"], wid, "Install finished")
        self.store.submit_quality(
            u["RLO-1"],
            HOME,
            "Loft insulation",
            "Install Team",
            "Installer",
            EVIDENCE,
            context_revision=1,
        )
        self.store.accept_quality(u["QI-2"], HOME, 0, "Independent inspection passed")
        self.store.hand_over_quality(u["RLO-1"], HOME, 0, "Resident pack handed over", True)
        self.store.finance_action(u["GEO-1"], HOME, dict(action="budget_propose", amount=10000))
        self.store.finance_action(u["PM-1"], HOME, dict(action="budget_approve"))
        self.store.finance_action(
            u["GEO-1"],
            HOME,
            dict(
                action="commit_raise",
                supplier="Test Ltd",
                contract="C-1",
                work_order=wid,
                measure="Loft insulation",
                amount=5000,
                quantity=10,
            ),
        )
        self.store.finance_action(u["PM-1"], HOME, dict(action="commit_approve", id="COM-1"))
        self.store.finance_action(
            u["GEO-1"],
            HOME,
            dict(
                action="invoice_receive",
                supplier="Test Ltd",
                work_order=wid,
                ref="INV-100",
                lines=lines(),
            ),
        )
        inv_id = self.store.detail(HOME)["finance"]["invoices"][-1]["id"]
        self.store.finance_action(u["GEO-1"], HOME, dict(action="invoice_match", id=inv_id))
        self.store.finance_action(
            u["PM-2"],
            HOME,
            dict(action="disposition", id=inv_id, decision="Accept for payment", note="Checked"),
        )
        self.store.finance_action(
            u["GEO-1"],
            HOME,
            dict(action="payment_status", id=inv_id, status="Paid outside this system"),
        )
        transitions.append(self.capture_http_bundle(work_order_id=wid, job_pack_receipt=receipt))

        report = pjc.validate_same_home_walk(
            transitions,
            case_id=HOME,
            vulnerability_reason=SECRET_REASON,
            private_markers=("SYN-ADJ-SENSORY-77", "quiet knock"),
            contractor_private_markers=("07700 900134",),
            sibling_ids=(SIBLING,),
            sibling_markers=(SIBLING_MARKER, "99 Sibling Walk"),
        )
        self.assertTrue(report["ok"], report["blockers"])
        self.assertEqual(report["status"], "complete_in_shape")
        self.assertFalse(report["accepted"])
        self.assertEqual(report["boundaries"], pjc.BOUNDARIES)

        # Sibling resident portal stays strictly isolated to ZF-2.
        sib_status, sib_view = self.resident_http_view(self.sibling_res_app.port)
        self.assertEqual(sib_status, 200)
        self.assertEqual(sib_view["home"]["address"], "99 Sibling Walk")
        self.assertNotIn("1 Test Road", json.dumps(sib_view))
        self.assertNotIn(SECRET_REASON, json.dumps(sib_view))

        self.assertEqual(pw.check(ROOT)["elements_met"], 0)
        self.assertEqual(ja.check(ROOT)["passed"], [])


class RoleScreensSameHomeWalkAndRedactionTests(_SameHomeStackBase):
    def _render_screen_in_node(
        self, screen_id: str, role: str, cookie: str, case_id: str = HOME
    ) -> dict[str, Any]:
        script = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const [webDir, apiBase, cookie, role, screenId, caseId] = process.argv.slice(1);
const app = fs.readFileSync(webDir + "/app.js", "utf8");
const host = fs.readFileSync(webDir + "/role-screens.js", "utf8");
let rendered = [];
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date,
  location: {hash: `#/screens?screen=${screenId}&case=${caseId}`},
  history: {replaceState: () => {}},
  me: {user: {role}},
  routeController: new AbortController(),
  workspaceStatus: {},
  api: async (path) => {
    const res = await fetch(apiBase + path, {headers: {Cookie: cookie}});
    if (!res.ok) throw new Error(`HTTP ${res.status} for ${path}`);
    return await res.json();
  },
  h: (tag, attrs, ...kids) => {
    const node = {
      tag,
      attrs: attrs || {},
      kids: kids.flat(Infinity).filter((k) => k !== false && k !== null && k !== undefined),
    };
    Object.defineProperty(node, "replaceChildren", {value: (...k) => { node.kids = k; }});
    Object.defineProperty(node, "textContent", {set: (v) => { node.kids = [v]; }});
    return node;
  },
  show: (...nodes) => { rendered = nodes; },
});
vm.runInContext(
  app.slice(app.indexOf("function workSummary("), app.indexOf("function workSteps("))
    + "\n" + host,
  context
);
vm.runInContext("roleScreensView()", context).then(() => {
  function textOf(node) {
    if (node === null || node === undefined) return "";
    if (typeof node !== "object") return String(node);
    return (node.kids || []).map(textOf).filter(Boolean).join(" ");
  }
  let evidenceNode = null;
  let sameHomeText = null;
  let nextActionText = null;
  const stageHrefs = [];
  function walk(node) {
    if (!node || typeof node !== "object") return;
    const attrs = node.attrs || {};
    if (node.tag === "section" && String(attrs.class || "").includes("screen-evidence")) {
      evidenceNode = node;
    }
    if (attrs["data-same-home"]) sameHomeText = textOf(node);
    if (attrs["data-same-home-next-action"]) nextActionText = textOf(node);
    if (node.tag === "a" && typeof attrs.href === "string" && attrs.href.startsWith("#/screens?")) {
      stageHrefs.push(attrs.href);
    }
    for (const child of node.kids || []) walk(child);
  }
  rendered.forEach(walk);
  console.log(JSON.stringify({
    sameHomeText,
    nextActionText,
    evidenceText: evidenceNode ? textOf(evidenceNode) : "",
    stageHrefs,
  }));
}).catch((err) => { console.error(err); process.exitCode = 1; });
"""
        proc = subprocess.run(
            [
                "node",
                "-e",
                script,
                str(WEB),
                self.api_base,
                cookie,
                role,
                screen_id,
                case_id,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out: dict[str, Any] = json.loads(proc.stdout)
        return out

    def test_staff_screens_preserve_same_home_continuity_and_contractor_redacts_reasons(
        self,
    ) -> None:
        u = self.u
        # Offer a free-text handoff so reason-roles see the text and redacted roles see HELD.
        meta = dataset.change_metadata(self.store, HOME)
        meta["next_action"] = "Agree quiet-knock arrival window with resident"
        self.store.offer_handoff(
            u["RLO-1"], HOME, u["RC-1"]["email"], "Check design access", metadata=meta
        )

        # Also prepare a work order so procurement-packages and contractor-job-pack have live data.
        self.store.technical_action(u["RC-1"], HOME, dict(action="design_submit", note="Loft"))
        self.store.resident_action(
            u["RLO-1"],
            HOME,
            dict(
                action="scope_record",
                measure="Loft insulation",
                scope="Synthetic loft scope",
                design_version=1,
                source="Synthetic supplied scope",
            ),
        )
        self.store.resident_action(
            u["RLO-1"],
            HOME,
            dict(
                action="decision_record",
                measure="Loft insulation",
                status="Accepted",
                answered_by="The resident",
                context_revision=1,
                source="Synthetic supplied resident statement",
            ),
        )
        pid = self.store.create_package(
            u["PM-1"],
            "Warm Homes Wave 1",
            "2026-01-01",
            "2099-12-31",
            "Loft insulation works",
            "C-1",
            "SYN-1",
        )
        cap_details = dataset.supplied_contract_fixture(self.store, pid, u["PM-1"], "Test Ltd")
        self.store.set_capacity(u["PM-1"], pid, "Test Ltd", 2, 1, "SYN-CAP-1", details=cap_details)
        self.store.issue_work_order(
            u["PM-1"],
            pid,
            HOME,
            scope="Loft insulation only",
            resident_bindings=[dict(measure="Loft insulation", context_revision=1)],
        )

        staff_screen_visits = (
            ("programme-queue", "Retrofit Programme Manager", True),
            ("technical-queue", "Retrofit Coordinator", False),
            ("resident-choice", "Resident Liaison Officer", True),
            ("procurement-packages", "Retrofit Programme Manager", True),
            ("quality-queue", "Quality Inspector", False),
            ("finance-invoices", "Grants and Evidence Officer", False),
            ("safety-lead", "Building Safety Liaison", True),
        )
        for screen_id, role, can_see_reason in staff_screen_visits:
            with self.subTest(screen=screen_id, role=role):
                cookie = self.login(self.staff_emails_by_role[role])
                view = self._render_screen_in_node(screen_id, role, cookie, HOME)
                self.assertIn(f"Same home: case {HOME}", view["sameHomeText"] or "")
                self.assertIn(
                    f"Current owner: {u['RLO-1']['name']}. Next action: ",
                    view["nextActionText"] or "",
                )
                if can_see_reason:
                    self.assertIn(
                        "Agree quiet-knock arrival window with resident",
                        view["nextActionText"] or "",
                    )
                else:
                    self.assertIn(taskqueues.HELD, view["nextActionText"] or "")
                    self.assertNotIn(SECRET_REASON, view["evidenceText"])
                self.assertTrue(
                    any(f"case={HOME}" in href for href in view["stageHrefs"]),
                    view["stageHrefs"],
                )
                self.assertNotIn(SIBLING_MARKER, view["evidenceText"])
                self.assertNotIn("99 Sibling Walk", view["evidenceText"])

        # Contractor job-pack screen shows Needs notice + named contact, omits staff work continuity
        # and redacts both raw vulnerability reasons and staff "Extra support noted" markers.
        con_cookie = self.login(u["CON-1"]["email"])
        cview = self._render_screen_in_node("contractor-job-pack", "Contractor", con_cookie, HOME)
        self.assertIn(f"Same home: case {HOME}", cview["sameHomeText"] or "")
        self.assertIsNone(cview["nextActionText"])
        self.assertIn("Needs notice", cview["evidenceText"])
        self.assertIn(
            "The reason for any notice is not shared with contractors.", cview["evidenceText"]
        )
        self.assertIn("Not shown for this role", cview["evidenceText"])
        self.assertNotIn(SECRET_REASON, cview["evidenceText"])
        self.assertNotIn("SYN-ADJ-SENSORY-77", cview["evidenceText"])
        self.assertNotIn(projection.REDACTED, cview["evidenceText"])
        self.assertNotIn("07700 900134", cview["evidenceText"])
        self.assertNotIn(SIBLING_MARKER, cview["evidenceText"])


if __name__ == "__main__":
    unittest.main()
