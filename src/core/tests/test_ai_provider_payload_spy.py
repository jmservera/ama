"""Offline provider-payload spies for the AI wrappers (#116). Constructed data only.

The real `Ai` serializes each request; `urllib.request.urlopen` is replaced by a spy that
records the exact bytes, so no provider, network or credential is involved. Expected values
come from source-defined contracts (`Ai.provider_body`, `ai_prompts`, the closed `capture`
lists, `build_request`). Reason-role payloads characterise the current default and are not
an approval of OD-14 or OD-19.
"""

from __future__ import annotations

import base64
import copy
import io
import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

import dataset
from zava_forward.core import ai as _ai
from zava_forward.core import ai_prompts
from zava_forward.core import ai_tasks as _ai_tasks
from zava_forward.core import assistants as _assistants
from zava_forward.core import projection as _projection
from zava_forward.core import quality as _quality
from zava_forward.core import ranking as _ranking
from zava_forward.core.sqlstore import SqlStore as _SqlStore

# The migrated core modules are not typed yet; the tests call them through Any.
ai: Any = _ai
ai_tasks: Any = _ai_tasks
assistants: Any = _assistants
projection: Any = _projection
quality: Any = _quality
ranking: Any = _ranking
SqlStore: Any = _SqlStore
MAX_IMAGE_BYTES: int = ai.MAX_IMAGE_BYTES

TOKEN = "SYN-BEARER-TOKEN"
PRIVATE = re.compile(r"PRIVATE-[A-Z0-9-]+")
ENVELOPE = json.dumps({"choices": [{"message": {"content": "No cited proposal."}}]}).encode()


class Transport:
    """Replaces urlopen: records each Request and returns a fixed provider envelope."""

    def __init__(self) -> None:
        self.requests: list[Any] = []

    def __call__(self, request: Any, timeout: float | None = None) -> io.BytesIO:
        self.requests.append(request)
        return io.BytesIO(ENVELOPE)

    def body(self) -> dict[str, Any]:
        self.assert_single()
        data: bytes = self.requests[-1].data
        data.decode("ascii")
        return dict(json.loads(data))

    def assert_single(self) -> None:
        if len(self.requests) != 1:
            raise AssertionError(f"expected one provider request, saw {len(self.requests)}")


class Offline(unittest.TestCase):
    def setUp(self) -> None:
        env = mock.patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        for name in ("ZF_REASON_ROLES", "ZF_AI", "ZF_DATA_PROCESSING", "AI_MODEL_VERSION"):
            os.environ.pop(name, None)
        self.client: Any = ai.Ai()
        self.client.endpoint = "https://provider.invalid"
        self.client.fast, self.client.strong = "fast-dep", "strong-dep"
        self.client.model_version = self.client.model_version_strong = "unattested"
        self.meter = mock.Mock()
        self.meter.reserve.return_value = "a" * 64
        self.meter.publish_output.return_value = None
        self.client.consumption = self.meter
        self.transport = Transport()
        for patcher in (
            mock.patch("urllib.request.urlopen", self.transport),
            mock.patch.object(self.client, "_token", return_value=TOKEN),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def assert_no_provider_call(self) -> None:
        self.assertEqual(self.transport.requests, [])
        self.meter.reserve.assert_not_called()


class WrapperBodies(Offline):
    def test_run_chat_wire_body_is_exactly_the_serializer_contract(self) -> None:
        system, user = "SYN-SYSTEM", "SYN-USER \u00e9"
        out = self.client.run("syn-task-name", system, user, "SYN-TEMPLATE-CANARY")
        self.assertEqual(out["source"], "ai")
        request = self.transport.requests[0]
        self.assertEqual(
            self.transport.body(),
            {
                "messages": [
                    {"role": "system", "content": "SYN-SYSTEM"},
                    {"role": "user", "content": "SYN-USER \u00e9"},
                ],
                "max_tokens": 700,
                "temperature": 0.3,
            },
        )
        self.assertEqual(request.data, ai.Ai.provider_body(system, user, 700, 0.3))
        self.assertNotIn(b"\xc3", request.data)
        for hidden in (TOKEN, "SYN-TEMPLATE-CANARY", "syn-task-name"):
            self.assertNotIn(hidden.encode(), request.data)
        self.assertEqual(
            request.full_url,
            "https://provider.invalid/openai/deployments/fast-dep/chat/completions"
            "?api-version=2024-10-21",
        )
        self.assertEqual(request.get_header("Authorization"), f"Bearer {TOKEN}")

    def test_strong_run_changes_only_the_deployment_in_the_url(self) -> None:
        self.client.run("syn-task", "s", "u", "t", strong=True)
        self.assertIn("/deployments/strong-dep/", self.transport.requests[0].full_url)
        self.assertEqual(self.transport.body()["max_tokens"], 700)

    def test_evidence_wire_body_and_bounds(self) -> None:
        out = self.client.evidence("SYN-SYSTEM", "SYN-USER")
        self.assertEqual(out["outcome"], "returned")
        self.assertEqual(
            self.transport.body(),
            {
                "messages": [
                    {"role": "system", "content": "SYN-SYSTEM"},
                    {"role": "user", "content": "SYN-USER"},
                ],
                "max_tokens": 600,
                "temperature": 0,
            },
        )
        self.assertNotIn(TOKEN.encode(), self.transport.requests[0].data)
        self.assertIn("/deployments/fast-dep/", self.transport.requests[0].full_url)

    def test_run_and_evidence_do_not_call_the_provider_when_not_permitted(self) -> None:
        self.client.run("syn-task", "s", "u", "t", off=True)
        self.client.endpoint = ""
        self.client.run("syn-task", "s", "u", "t")
        self.assertEqual(self.client.evidence("s", "u")["outcome"], "disabled")
        self.assert_no_provider_call()


class LookAtBodies(Offline):
    def test_text_document_sends_instruction_and_first_6000_characters_only(self) -> None:
        for mime in ("text/plain", "text/csv", "application/json"):
            self.transport.requests.clear()
            data = ("A" * 6000 + "SYN-TAIL-CANARY").encode()
            out = self.client.look_at("note.txt", data, mime)
            self.assertEqual(out["source"], "ai")
            system, instruction = ai_prompts.render("read_document", name="note.txt")
            self.assertEqual(
                self.transport.body(),
                {
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": instruction + "\n\n" + "A" * 6000},
                    ],
                    "max_tokens": 500,
                    "temperature": 0.3,
                },
            )
            self.assertNotIn(b"SYN-TAIL-CANARY", self.transport.requests[0].data)
            self.assertIn("/deployments/strong-dep/", self.transport.requests[0].full_url)

    def test_image_document_sends_the_closed_content_list(self) -> None:
        data = b"\x89PNG\r\nsynthetic"
        self.client.look_at("photo.png", data, "image/png")
        system, instruction = ai_prompts.render("read_document", name="photo.png")
        self.assertEqual(
            self.transport.body(),
            {
                "messages": [
                    {"role": "system", "content": system},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": instruction},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": "data:image/png;base64,"
                                    + base64.b64encode(data).decode()
                                },
                            },
                        ],
                    },
                ],
                "max_tokens": 500,
                "temperature": 0.3,
            },
        )

    def test_file_name_reaches_only_the_instruction(self) -> None:
        self.client.look_at("SYN-NAME-CANARY.txt", b"body", "text/plain")
        messages = self.transport.body()["messages"]
        self.assertNotIn("SYN-NAME-CANARY", messages[0]["content"])
        self.assertIn("File name: SYN-NAME-CANARY.txt", messages[1]["content"])

    def test_unreadable_inputs_stop_before_any_provider_request(self) -> None:
        for name, data, mime in (
            ("a.svg", b"<svg/>", "image/svg+xml"),
            ("a.png", b"\0" * (MAX_IMAGE_BYTES + 1), "image/png"),
            ("a.pdf", b"%PDF", "application/pdf"),
        ):
            with self.subTest(mime=mime):
                self.assertEqual(self.client.look_at(name, data, mime)["source"], "template")
        malformed: list[tuple[Any, Any]] = [
            ({"x": "SYN-PRIVATE-NAME"}, "text/plain"),
            ("a.txt", ["text/plain"]),
        ]
        for name, mime in malformed:
            with self.subTest(name=name), self.assertRaises(ValueError) as error:
                self.client.look_at(name, b"body", mime)
            self.assertNotIn("SYN-PRIVATE-NAME", str(error.exception))
        self.assert_no_provider_call()


HOME = dict(
    address="1 Test Road",
    town="Testville",
    postcode="TE1 1ST",
    type="Mid terrace",
    built=1950,
    epc="D",
    tenure="Social rent",
)
SURVEY = dict(
    epc="D", type="Mid terrace", built=1950, version=1, status="Done", evidence_hash="HASH-1"
)
FIRST_DOC = dict(id="DOC-1", kind="Survey", version=1, content_sha256="abc", at="2026-01-01")
SECOND_DOC = dict(id="DOC-2", kind="Other", version=1, content_sha256="def", at="2026-01-02")
GRANT_DOC = dict(
    id="DOC-3", kind="Funding evidence", version=1, content_sha256="ghi", at="2026-01-03"
)
FUNDING = dict(
    route="ECO4", status="To prepare", reference="REF-1", terms_version="t1", terms_hash="th"
)
FINANCE: dict[str, Any] = dict(
    budget=dict(amount=9183461, status="Approved"),
    commitments=[
        dict(
            id="C-1",
            supplier="Test Ltd",
            contract="K-1",
            work_order="WO-1",
            measure="Loft insulation",
            amount=100,
            quantity=1,
            status="Open",
        )
    ],
    invoices=[
        dict(
            id="I-1",
            kind="Invoice",
            supplier="Test Ltd",
            work_order="WO-1",
            ref="R-1",
            status="Received",
            version=1,
            evidence_hash="IH",
            lines=[dict(measure="Loft insulation", quantity=1, amount=100, milestone_ref="M-1")],
        )
    ],
)
GRANT_EVIDENCE = [dict(state="Claimable", source="S-1", amount=50, at="2026-01-03")]
GRANTS = [dict(id="G-1", scheme="ECO4", state="Claimable", evidence=GRANT_EVIDENCE)]
QUALITY = [
    dict(
        measure="Loft insulation",
        state="Accepted",
        checklist_version="v1",
        evidence_version=1,
        items=[dict(label="Photo", evidence="EV-1")],
    )
]
POLICY = {k: v for k, v in ranking.describe(ranking.CURRENT).items() if k != "versions"}
REASONS = [
    dict(code="waiting_days", text="Waiting 10 days in this stage"),
    dict(code="stage_order", text="At 'Contacting resident'"),
]
EXPECTED: dict[str, dict[str, Any]] = {
    "stock-prioritisation": dict(
        home=HOME,
        survey=SURVEY,
        ranking=dict(
            policy=POLICY,
            stage="Contacting resident",
            waiting_days=10,
            reasons=REASONS,
            disclosure=(
                "Resident support and safety ranking inputs are not disclosed to this audience."
            ),
        ),
    ),
    "assessment-preparation": dict(
        home=HOME,
        survey=SURVEY,
        measures=["Loft insulation"],
        technical=dict(design_version="v1"),
        documents=[FIRST_DOC],
    ),
    "funding-evidence": dict(
        home=HOME,
        measures=["Loft insulation"],
        funding=FUNDING,
        finance=dict(
            budget=dict(amount=9183461, status="Approved"),
            commitments=FINANCE["commitments"],
            invoices=FINANCE["invoices"],
        ),
        grants=GRANTS,
        documents=[FIRST_DOC, GRANT_DOC],
    ),
    "works-resident-coordination": dict(
        home=HOME,
        measures=["Loft insulation"],
        preferences=dict(preferred="Phone", unavailable="Tuesdays"),
        appointments=[
            dict(type="Survey", date="2026-01-05", slot="AM", outcome=projection.NOTE_HELD),
            dict(type="Visit", date="2026-01-06", slot="PM", outcome="Booked"),
        ],
        handoff=dict(state="Offered", to_code="ROLE-0", at="2026-01-02"),
        requests=[dict(id="SR-1", status="Open", next_update="2026-02-01")],
        capacity=[],
    ),
    "quality-evidence": dict(
        home=HOME,
        measures=["Loft insulation"],
        documents=[SECOND_DOC],
        quality=[
            dict(
                measure="Loft insulation",
                state="Accepted",
                checklist_version="v1",
                evidence_version=1,
                items=[dict(label="Photo", evidence="EV-1")],
            )
        ],
        checklists={"Loft insulation": quality.checklist_for("Loft insulation")},
    ),
}
EVIDENCE_KEYS = {
    "sources",
    "citations",
    "unknowns",
    "schema",
    "rules",
    "registry",
    "registry_hash",
    "schema_hash",
    "rule_hash",
    "exercise_predicate",
    "exercise_rule",
}


def constructed_case() -> dict[str, Any]:
    return dict(
        id="SYN-1",
        stage="Contacting resident",
        days_in_stage=10,
        resident=dict(
            name="PRIVATE-NAME",
            adjustment="PRIVATE-REASON",
            phone="PRIVATE-PHONE",
            email="PRIVATE-EMAIL",
            preferred="Phone",
            unavailable="Tuesdays",
        ),
        home=dict(HOME, diagnostics={"nested": "PRIVATE-DIAGNOSTICS"}, lat=1.5),
        monitoring={"device": "PRIVATE-DEVICE"},
        notes="PRIVATE-NOTE",
        measures="Loft insulation",
        survey=dict(SURVEY, note="PRIVATE-SURVEY-NOTE"),
        technical=dict(design_version="v1", secret="PRIVATE-TECHNICAL"),
        documents=[
            dict(FIRST_DOC, name="PRIVATE-DOC-NAME", summary="PRIVATE-AI-SUMMARY"),
            dict(SECOND_DOC, name="PRIVATE-OTHER-NAME", summary="PRIVATE-OTHER-SUMMARY"),
            dict(GRANT_DOC, name="PRIVATE-GRANT-NAME"),
            dict(
                id="DOC-4",
                kind="Consent",
                version=1,
                content_sha256="jkl",
                at="x",
                name="PRIVATE-CONSENT-NAME",
            ),
        ],
        funding=dict(FUNDING, internal="PRIVATE-FUNDING"),
        finance=copy.deepcopy(FINANCE),
        grants=[
            dict(
                id="G-1",
                scheme="ECO4",
                state="Claimable",
                owner="PRIVATE-GRANT-OWNER",
                history=[dict(GRANT_EVIDENCE[0], reviewer="PRIVATE-REVIEWER")],
            )
        ],
        handoff=dict(state="Offered", to_code="ROLE-0", at="2026-01-02", note="PRIVATE-HANDOFF"),
        appointments=[
            dict(
                type="Survey",
                date="2026-01-05",
                slot="AM",
                outcome="PRIVATE-OUTCOME-TEXT",
                notes="PRIVATE-APPOINTMENT-NOTE",
            ),
            dict(type="Visit", date="2026-01-06", slot="PM", outcome="Booked"),
        ],
        service_requests=[
            dict(id="SR-1", status="Open", next_update="2026-02-01", detail="PRIVATE-REQUEST")
        ],
        quality=copy.deepcopy(QUALITY),
    )


class AssistantSerializer(Offline):
    def wire(self, capability: str, case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        snapshot = assistants.capture(capability, case)
        task = dict(capability=capability, snapshot=snapshot, dispatch={})
        system, prompt = assistants.build_request(task)
        self.transport.requests.clear()
        self.assertEqual(self.client.evidence(system, prompt)["outcome"], "returned")
        return self.transport.body(), snapshot

    def test_each_capability_sends_only_its_closed_source_fields(self) -> None:
        for capability, spec in assistants.REGISTRY.items():
            with self.subTest(capability=capability):
                body, snapshot = self.wire(capability, constructed_case())
                self.assertEqual(
                    body["messages"][0], {"role": "system", "content": assistants.SYSTEM}
                )
                user = body["messages"][1]
                self.assertEqual(user["role"], "user")
                self.assertEqual(
                    user["content"],
                    assistants.canonical(
                        dict(capability=capability, purpose=spec["purpose"], evidence=snapshot)
                    ),
                )
                evidence = json.loads(user["content"])["evidence"]
                self.assertEqual(set(evidence), EVIDENCE_KEYS)
                self.assertEqual(evidence["sources"], EXPECTED[capability])
                self.assertEqual(
                    set(evidence["citations"]), {f"source:{key}" for key in EXPECTED[capability]}
                )
                self.assertTrue(all(u.startswith("source.") for u in evidence["unknowns"]))
                self.assertEqual(
                    {k: body[k] for k in ("max_tokens", "temperature")},
                    {"max_tokens": 600, "temperature": 0},
                )
                self.assertEqual(set(body), {"messages", "max_tokens", "temperature"})
                self.assertEqual(PRIVATE.findall(self.transport.requests[0].data.decode()), [])
                self.assertEqual(len(self.transport.requests), 1)
                if capability != "funding-evidence":
                    self.assertNotIn(b"9183461", self.transport.requests[0].data)
                    self.assertNotIn(b"source:finance", self.transport.requests[0].data)

    def test_appointment_outcome_text_is_held_unless_every_role_has_a_recorded_need(self) -> None:
        capability = "works-resident-coordination"
        body, _ = self.wire(capability, constructed_case())
        self.assertNotIn("PRIVATE-OUTCOME-TEXT", body["messages"][1]["content"])
        roles = ",".join(assistants.REGISTRY[capability]["roles"])
        with mock.patch.dict(os.environ, {"ZF_REASON_ROLES": roles}):
            body, _ = self.wire(capability, constructed_case())
        sources = json.loads(body["messages"][1]["content"])["evidence"]["sources"]
        self.assertEqual(
            [a["outcome"] for a in sources["appointments"]], ["PRIVATE-OUTCOME-TEXT", "Booked"]
        )
        self.assertEqual(
            PRIVATE.findall(self.transport.requests[0].data.decode()), ["PRIVATE-OUTCOME-TEXT"]
        )

    def test_unknown_capability_is_refused_before_any_provider_request(self) -> None:
        with self.assertRaises(KeyError):
            assistants.capture("SYN-UNKNOWN", constructed_case())
        self.assert_no_provider_call()


FACTS = (
    "Case ZF-1. Resident: Pat Test. Home: 1 Test Road, Testville. "
    "Stage: Contacting resident for 10 days. Waiting on Sam Example to agree a visit. "
    "Resident adjustments: {adjustment}. Resident prefers: Phone. "
    "Resident decision: {decision}. Funding: {funding}. Open safety issues: 0. "
    "Recent contacts: 2026-01-02 {contact}"
)
CITABLE = (
    "Stage: Contacting resident; Days in stage: 10; Waiting on: Sam Example; "
    "Owner: Sam Example; Resident decision: {decision}; Preferred contact: Phone; "
    "Address: 1 Test Road; Home type: Mid terrace; EPC band: D; Built: 1950; "
    "Measures: Loft insulation; Funding: {funding}; Funding route: {route}; "
    "Open safety issues: 0"
)


class LegacyRoleProjection(Offline):
    def setUp(self) -> None:
        super().setUp()
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        seed = root / "seed.json"
        seed.write_text(json.dumps(dataset.DATA))
        self.store: Any = SqlStore(str(seed), str(root / "test.db"))
        self.addCleanup(self.store.db.close)
        self.store.ai = self.client
        self.client.gate = self.client.release = None
        case = self.store.cases["ZF-1"]
        case["resident"].update(
            adjustment="PRIVATE-REASON", phone="PRIVATE-PHONE", email="PRIVATE-EMAIL"
        )
        case["home"].update(postcode="PRIVATE-POSTCODE", diagnostics={"n": "PRIVATE-DIAGNOSTICS"})
        case["notes"] = "PRIVATE-NOTE"
        case["contacts"] = [
            dict(at="2026-01-02T10:00:00Z", outcome="PRIVATE-CONTACT-OUTCOME", channel="Phone")
        ]
        case["documents"] = []
        self.sam = self.store.staff["sam@example.test"]
        self.coordinator = dict(self.sam, role="Retrofit Coordinator")

    def expected_user(self, **facts: str) -> str:
        case = self.store.cases["ZF-1"]
        shared = dict(
            decision=ai_tasks.resident_status(case),
            funding=f"{case['funding']['route']} ({case['funding']['status']})",
        )
        _, prompt = ai_prompts.render(
            "summary", owner="Sam Example", facts=FACTS.format(**shared, **facts)
        )
        labels = CITABLE.format(**shared, route=case["funding"]["route"])
        return (
            prompt
            + "\n\nCitable facts (cite only these, copied exactly): \nZF-1: "
            + labels
            + ai_prompts.CITATION_RULE[0]
            + ai_prompts.CITATION_RULE[2]
        )

    def run_summary(self, user: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
        self.transport.requests.clear()
        self.store.ai_run(user, "ZF-1", "summary")
        return self.transport.body(), self.transport.requests[0].data

    def test_non_reason_role_payload_equals_the_expected_prompt_without_canaries(self) -> None:
        self.assertFalse(projection.can_see_reason(self.coordinator))
        body, raw = self.run_summary(self.coordinator)
        user = self.expected_user(adjustment="extra support needed", contact="Phone")
        self.assertEqual(
            body,
            {
                "messages": [
                    {"role": "system", "content": ai_prompts.TEXT_SYSTEM},
                    {"role": "user", "content": user},
                ],
                "max_tokens": 700,
                "temperature": 0.3,
            },
        )
        self.assertEqual(PRIVATE.findall(raw.decode()), [])

    def test_reason_role_differs_only_in_the_adjustment_and_contact_outcome(self) -> None:
        self.assertTrue(projection.can_see_reason(self.sam))
        body, raw = self.run_summary(self.sam)
        user = self.expected_user(adjustment="PRIVATE-REASON", contact="PRIVATE-CONTACT-OUTCOME")
        self.assertEqual(body["messages"][1]["content"], user)
        self.assertEqual(
            sorted(PRIVATE.findall(raw.decode())), ["PRIVATE-CONTACT-OUTCOME", "PRIVATE-REASON"]
        )

    def test_unknown_task_and_malformed_selected_field_stop_before_the_provider(self) -> None:
        with self.assertRaises(ValueError):
            self.store.ai_run(self.sam, "ZF-1", "approve_funding")
        self.store.cases["ZF-1"]["home"]["address"] = {"nested": "PRIVATE-ADDRESS"}
        with self.assertRaises(ValueError) as error:
            self.store.ai_run(self.sam, "ZF-1", "summary")
        self.assertNotIn("PRIVATE-ADDRESS", str(error.exception))
        self.assert_no_provider_call()


if __name__ == "__main__":
    unittest.main()
