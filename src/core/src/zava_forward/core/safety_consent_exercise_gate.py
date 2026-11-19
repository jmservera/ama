"""Deterministic exercise-scenario safety and resident consent gate verifier (Refs #81).

Proves across all constructed and synthetic exercise scenario suites in ``zava_forward.core``
that:
1. Every controlled progression attempt on a case with unresolved safety evidence
   (active hazard, unaccepted referral, repaired-but-unreleased hold, open standalone
   safeguarding item, or missing/malformed safety state) is refused fail-closed under
   ``RULE-001`` / ``PRD FR-008`` without mutating case, work-order, or audit state.
2. Every attempt to start or activate work (work-order issuance, contractor appointment
   activation to ``Appointed``, booking ``advance``, completion, quality acceptance, or
   handover) without a valid active resident/representative agreement or an explicitly
   authorised exception approved by a named human with resident notification is refused
   fail-closed under ``RULE-002`` / ``BRD FR-011`` / ``BRD FR-014`` / ``PRD FR-008``.

All rule records and scenario inputs here are synthetic offline exercise fixtures, never
live legal sign-off, live resident consent evidence, or production release authority.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from copy import deepcopy
from datetime import UTC, date, datetime
from functools import partial
from pathlib import Path
from typing import Any

from . import controls, gates, learning_test_bundles
from .quality import checklist_for
from .resident_decisions import (
    AUTHORISED_EXCEPTION_RULE_ID,
    resident_gate,
    validate_authorised_works_exception,
)
from .sqlstore import SqlStore
from .store import READY_STAGE, GateError, Store
from .synthetic import resident_preview_fixture, scale_fixture, sensor_scenarios

SAFETY_GATE_RULE_ID = "RULE-001; PRD FR-008"
CONSENT_GATE_RULE_ID = "RULE-002; BRD FR-011; PRD FR-008"
EXERCISE_QUALIFICATION = (
    "Unreviewed exercise rule: synthetic offline verification only; named human legal, "
    "safety and service owners required before live use."
)
DEFAULT_AS_OF = "2026-11-15"
MEASURE = "Loft insulation"
CONTRACTOR = "Test Ltd"


def _normalize_as_of(as_of: str) -> tuple[str, str]:
    if not isinstance(as_of, str) or len(as_of.strip()) != 10:
        raise ValueError("as_of must be an ISO YYYY-MM-DD date string.")
    raw = as_of.strip()
    parsed = date.fromisoformat(raw)
    if parsed.isoformat() != raw:
        raise ValueError("as_of must be an ISO YYYY-MM-DD date string.")
    utc_iso = datetime(parsed.year, parsed.month, parsed.day, 12, 0, 0, tzinfo=UTC).isoformat()
    return raw, utc_iso


def _delegation_authority(
    contract_ref: str = "SYN-CONTRACT",
    contractor: str = CONTRACTOR,
) -> dict[str, Any]:
    return dict(
        reference="SYN-DELEGATION-81",
        version="1",
        contract_ref=contract_ref,
        contract_version="SYN-1",
        revoked=False,
        valid_from="2026-01-01",
        valid_to="2099-12-31",
        actions=[
            "rescope",
            "capacity",
            "issue",
            "reissue",
            "appointment",
            "complete",
            "correct",
            "withdraw",
        ],
        suppliers=[contractor],
        scope_versions=[1, 2],
    )


def _staff_seed(contractor: str = CONTRACTOR) -> list[dict[str, Any]]:
    return [
        dict(
            code="RLO-01",
            name="Sam Example",
            email="sam@example.test",
            role="Resident Liaison Officer",
        ),
        dict(
            code="PM-01",
            name="Pam Lead",
            email="pam@example.test",
            role="Retrofit Programme Manager",
            contract_authorities=[_delegation_authority(contractor=contractor)],
        ),
        dict(
            code="RC-01",
            name="Robin Coord",
            email="robin@example.test",
            role="Retrofit Coordinator",
        ),
        dict(
            code="BSL-01",
            name="Bea Safe",
            email="bea@example.test",
            role="Building Safety Liaison",
        ),
        dict(
            code="BSL-02",
            name="Blair Safe",
            email="blair@example.test",
            role="Building Safety Liaison",
        ),
        dict(
            code="QI-01",
            name="Quin Inspect",
            email="quin@example.test",
            role="Quality Inspector",
        ),
        dict(
            code="QI-02",
            name="Quil Second",
            email="quil@example.test",
            role="Quality Inspector",
        ),
    ]


def _evidence_documents() -> list[dict[str, Any]]:
    return [
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


def _signed_technical(design_version: int = 1) -> dict[str, Any]:
    return dict(
        design_version=design_version,
        design_by="robin@example.test",
        design_name="Robin Coord",
        design_at="2026-01-01T09:00",
        versions=[
            dict(
                version=design_version,
                by="Robin Coord",
                by_email="robin@example.test",
                role="Retrofit Coordinator",
                at="2026-01-01T09:00",
                note="SYN technical baseline",
            )
        ],
        signoffs={
            "assessment": dict(
                status="Signed off",
                version=design_version,
                by="Quin Inspect",
                by_email="quin@example.test",
                role="Quality Inspector",
                at="2026-01-01T09:10",
                note="SYN",
                reason="",
                history=[],
            ),
            "design": dict(
                status="Signed off",
                version=design_version,
                by="Pam Lead",
                by_email="pam@example.test",
                role="Retrofit Programme Manager",
                at="2026-01-01T09:20",
                note="SYN",
                reason="",
                history=[],
            ),
            "building": dict(
                status="Signed off",
                version=design_version,
                by="Bea Safe",
                by_email="bea@example.test",
                role="Building Safety Liaison",
                at="2026-01-01T09:30",
                note="SYN",
                reason="",
                history=[],
            ),
            "coordination": dict(
                status="Signed off",
                version=design_version,
                by="SamCoord Override",
                by_email="coord-override@example.test",
                role="Programme Support Officer",
                at="2026-01-01T09:40",
                note="SYN",
                reason="",
                history=[],
            ),
        },
    )


def _apply_resident_scope(
    case: dict[str, Any],
    *,
    measure: str = MEASURE,
    design_version: int = 1,
    accepted: bool = False,
    answered_by: str = "The resident",
    representative_ref: str | None = None,
    authority_version: int | None = None,
) -> None:
    case["technical"] = _signed_technical(design_version=design_version)
    case["documents"] = _evidence_documents()
    case.setdefault("resident_scopes", {})[measure] = [
        dict(
            revision=1,
            case_id=case["id"],
            measure=measure,
            scope="SYN-LOFT-SCOPE",
            design_version=design_version,
            source="SYN-SCOPE",
            recorded_by="sam@example.test",
            at="2026-01-01",
        )
    ]
    if accepted:
        decision: dict[str, Any] = dict(
            version=1,
            context_revision=1,
            status="Accepted",
            answered_by=answered_by,
            case_id=case["id"],
            measure=measure,
            scope="SYN-LOFT-SCOPE",
            design_version=design_version,
            source="SYN-SUPPLIED-RESIDENT-ANSWER",
            recorded_by="Sam Example",
            recorded_by_email="sam@example.test",
            at="2026-01-01",
        )
        if representative_ref is not None:
            decision["representative_ref"] = representative_ref
        if authority_version is not None:
            decision["authority_version"] = authority_version
        case.setdefault("measure_decisions", {})[measure] = [decision]


def _base_case(
    cid: str,
    *,
    owner_code: str = "RLO-01",
    stage: str = "Contacting resident",
    decision: str = "Waiting",
    funding: bool = False,
    hazards: Sequence[dict[str, Any]] = (),
    contractor: str = CONTRACTOR,
) -> dict[str, Any]:
    return dict(
        id=cid,
        wave="Wave 1",
        closed=False,
        stage=stage,
        stage_since="2026-01-01",
        days_in_stage=10,
        waiting_on="Sam Example",
        reason="to agree a visit",
        owner_code=owner_code,
        owner="Sam Example",
        owner_role="Resident Liaison Officer",
        resident=dict(
            title="Ms",
            name=f"Pat {cid}",
            formal=f"Ms {cid}",
            phone="01000 000000",
            email="",
            preferred="Phone",
            adjustment="None",
            priority_support=False,
            unavailable="",
            representative=None,
        ),
        home=dict(
            address=f"1 {cid} Test Road",
            town="Testville",
            postcode="TE1 1ST",
            area="Test",
            type="Mid terrace",
            built=1950,
            epc="D",
            tenure="Social rent",
            lat=0,
            lon=0,
        ),
        measures=MEASURE,
        contractor=dict(name=contractor, phone="0", scope="x", contact="Kim Builder"),
        decision=dict(status=decision, by=None, at=None),
        funding_ok=funding,
        funding=dict(
            route="SHDF Wave 3" if funding else "Not decided",
            status="Confirmed" if funding else "Not started",
            reference="SYN-FUND-81" if funding else "",
            draft="",
            approved_by="Pam Lead" if funding else None,
        ),
        contacts=[dict(at="2026-01-02T10:00", channel="Phone", outcome="Initial exercise contact")],
        appointments=[],
        hazards=list(hazards),
        documents=_evidence_documents(),
        history=[],
    )


def _constructed_workbench_dataset(as_of_day: str) -> dict[str, Any]:
    zf1 = _base_case("ZF-1")
    zf2 = _base_case("ZF-2", stage=READY_STAGE, funding=True)
    _apply_resident_scope(zf2, accepted=False)
    zf3 = _base_case("ZF-3", stage=READY_STAGE, decision="Accepted", funding=True)
    _apply_resident_scope(zf3, accepted=True)
    zf3_legacy = _base_case("ZF-3-LEGACY", stage=READY_STAGE, decision="Accepted", funding=True)
    _apply_resident_scope(zf3_legacy, accepted=False)
    zf4 = _base_case(
        "ZF-4",
        stage=READY_STAGE,
        decision="Accepted",
        funding=True,
        hazards=[
            dict(
                category="Damp",
                priority="P1",
                noticed="2026-01-01",
                referred=None,
                repaired=None,
                released=False,
                job="J1",
                owner="Bea Safe",
            )
        ],
    )
    _apply_resident_scope(zf4, accepted=True)
    zf5 = _base_case("ZF-5", owner_code="PM-01", stage=READY_STAGE, funding=True)
    zf5["measures"] = "Loft insulation, Wall insulation"
    _apply_resident_scope(zf5, measure="Loft insulation", accepted=True)
    _apply_resident_scope(zf5, measure="Wall insulation", accepted=True)
    return dict(
        as_of=as_of_day,
        staff=_staff_seed(),
        cases=[zf1, zf2, zf3, zf3_legacy, zf4, zf5],
    )


@contextmanager
def _open_exercise_store(
    data: dict[str, Any],
    *,
    use_sql: bool,
    docs_source_dir: Path | None = None,
) -> Iterator[Store]:
    with tempfile.TemporaryDirectory(prefix="zf-81-gate-") as tmp:
        root = Path(tmp)
        seed_path = root / "seed.json"
        seed_path.write_text(json.dumps(data), encoding="utf-8")
        docs_dir = root / "docs"
        if docs_source_dir is not None and docs_source_dir.exists():
            import shutil

            shutil.copytree(docs_source_dir, docs_dir)
        store: Store
        if use_sql:
            store = SqlStore(  # type: ignore[no-untyped-call]
                str(seed_path),
                str(root / "zavaforward.sqlite3"),
                docs_dir=str(docs_dir),
                digest_dir=str(root / "digests"),
            )
        else:
            store = Store(  # type: ignore[no-untyped-call]
                str(seed_path),
                str(root / "live.json"),
                str(root / "audit.jsonl"),
            )
        try:
            yield store
        finally:
            db = getattr(store, "db", None)
            if db is not None:
                db.close()


def _seed_package_and_capacity(
    store: Store,
    *,
    contractor: str = CONTRACTOR,
    capacity: int = 25,
    package_name: str = "PKG-81-EXERCISE",
    doc_id: str = "SYN-COMMITMENT-81",
) -> str:
    pam = store.staff["pam@example.test"]
    pid = store.create_package(  # type: ignore[no-untyped-call]
        pam,
        package_name,
        "2026-01-01",
        "2099-12-31",
        "SYN-LOFT-SCOPE",
        "SYN-CONTRACT",
        "SYN-1",
    )
    content = b"SYNTHETIC ONLY: exercise capacity commitment bytes; no live instruction."
    today_iso = date.today().isoformat()
    with store.lock:
        package = store._package(pid)  # type: ignore[no-untyped-call]
        package["contract_version"] = "SYN-1"
        actor = store.staff[pam["email"]]
        if not actor.get("contract_authorities"):
            actor["contract_authorities"] = [_delegation_authority(contractor=contractor)]
            if hasattr(store, "db"):
                store.db.execute(
                    "UPDATE staff SET body=? WHERE email=?",
                    (json.dumps(actor), actor["email"]),
                )
        case_ids = [
            cid
            for cid, c in sorted(store.cases.items())
            if c.get("contractor", {}).get("name") == contractor
        ]
        source_case = store._case(case_ids[0])  # type: ignore[no-untyped-call]
        doc = dict(
            id=doc_id,
            name="synthetic-commitment-81.txt",
            kind="Other",
            version="1",
            content_sha256=hashlib.sha256(content).hexdigest(),
            at=today_iso,
            scan=dict(status="clean", scanner="Synthetic exercise fixture"),
        )
        source_case["documents"] = [
            d for d in source_case.get("documents", []) if d.get("id") != doc_id
        ] + [doc]
        store.docstore.put(source_case["id"], doc_id, content, "text/plain")
        store.save()  # type: ignore[no-untyped-call]
        details = dict(
            source_case_id=source_case["id"],
            document_id=doc_id,
            source_version="1",
            source_date=today_iso,
            reviewed_on=today_iso,
            valid_from="2026-01-01",
            valid_to="2099-12-31",
            unit="home-work-order",
            case_ids=case_ids,
            status="Committed",
        )
    store.set_capacity(  # type: ignore[no-untyped-call]
        pam,
        pid,
        contractor,
        capacity,
        capacity,
        "SYN-CAPACITY-81",
        details,
    )
    return str(pid)


def _offer_and_confirm_appointment(
    store: Store,
    actor: dict[str, Any],
    wid: str,
    *,
    when: str = "2098-05-01",
    confirm_all: bool = True,
) -> str:
    wo = store._work_order(wid)  # type: ignore[no-untyped-call]
    cid = str(wo["case_id"])
    case = store.cases[cid]
    if not (case.get("resident_update") or {}).get("version"):
        store.resident_action(  # type: ignore[no-untyped-call]
            actor,
            cid,
            dict(
                action="update_record",
                expected_version=0,
                owner=actor["email"],
                purpose="SYN appointment update",
                due_at="2099-01-01T10:00:00+00:00",
                basis="SYN manual arrangement",
                status="Outstanding",
            ),
        )
    offer_id = f"SYN-offer-{wid}-{len(wo.get('appointment_events', []))}"
    store.appointment_control(
        actor,
        wid,
        dict(
            action="offer",
            event_ref=offer_id,
            date=when,
            period="Morning",
            expected_offer_id=(wo.get("appointment_offer") or {}).get("id"),
            options=["Morning", "Different day", "Pause"],
            constraints="SYN morning only",
            instructions="Knock and wait",
            paused=False,
            deferred=False,
            bundle=False,
        ),
    )
    steps: tuple[tuple[str, str], ...] = (
        ("resident", str(case["resident"]["name"])),
        ("staff", str(actor["name"])),
    )
    if confirm_all:
        steps = steps + (("capacity", "SYN supplier authorized contact"),)
    for kind, person in steps:
        store.appointment_control(
            actor,
            wid,
            dict(
                action="confirm",
                event_ref=f"{offer_id}-{kind}",
                offer_id=offer_id,
                kind=kind,
                person=person,
                source=f"SYN explicit recorded agreement {kind}",
                channel="Phone, manually recorded",
            ),
        )
    return offer_id


def _state_fingerprint(store: Store, case_id: str) -> tuple[str, str, int]:
    with store.lock:
        case_json = json.dumps(store.cases[case_id], sort_keys=True)
        wos = [
            w
            for w in store.data.get("procurement", {}).get("work_orders", [])
            if w.get("case_id") == case_id
        ]
        wo_json = json.dumps(wos, sort_keys=True)
    audit_len = len(list(store.audit_entries()))  # type: ignore[no-untyped-call]
    return case_json, wo_json, audit_len


def _assert_blocked_attempt(
    store: Store,
    case_id: str,
    *,
    attempt_label: str,
    gate_kind: str,
    expected_substrings: tuple[str, ...],
    fn: Callable[[], object],
    attempts_out: list[dict[str, Any]],
    violations_out: list[dict[str, Any]],
) -> bool:
    before = _state_fingerprint(store, case_id)
    rule_id = SAFETY_GATE_RULE_ID if gate_kind == "safety" else CONSENT_GATE_RULE_ID
    try:
        fn()
    except (GateError, PermissionError, ValueError) as exc:
        msg = str(exc)
        after = _state_fingerprint(store, case_id)
        mutated = before != after
        matched = any(sub.casefold() in msg.casefold() for sub in expected_substrings)
        blocked_cleanly = matched and not mutated
        attempts_out.append(
            dict(
                case_id=case_id,
                attempt=attempt_label,
                gate=gate_kind,
                rule_id=rule_id,
                blocked=blocked_cleanly,
                exception_type=type(exc).__name__,
                state_unchanged=not mutated,
            )
        )
        if not blocked_cleanly:
            violations_out.append(
                dict(
                    case_id=case_id,
                    check=attempt_label,
                    gate=gate_kind,
                    rule_id=rule_id,
                    detail=(
                        "Refusal mutated store/audit state or missed expected gate reason: "
                        f"{msg[:160]}"
                    ),
                )
            )
        return blocked_cleanly
    violations_out.append(
        dict(
            case_id=case_id,
            check=attempt_label,
            gate=gate_kind,
            rule_id=rule_id,
            detail="Controlled transition or work start unexpectedly succeeded without refusal.",
        )
    )
    attempts_out.append(
        dict(
            case_id=case_id,
            attempt=attempt_label,
            gate=gate_kind,
            rule_id=rule_id,
            blocked=False,
            exception_type=None,
            state_unchanged=False,
        )
    )
    return False


def verify_store_safety_and_consent_invariants(
    store: Store,
    *,
    suite_name: str = "custom",
    as_of: str = DEFAULT_AS_OF,
) -> dict[str, Any]:
    """Inspect static work-order/progression invariants and isolated dynamic gate refusals."""
    as_of_day, as_of_utc = _normalize_as_of(as_of)
    with store.lock:
        snapshot = deepcopy(store.data)
        snapshot["cases"] = [deepcopy(c) for c in store.cases.values()]
        snapshot["staff"] = [
            deepcopy(s) for s in (snapshot.get("staff") or list(store.staff.values()))
        ]
        staff_list = list(snapshot["staff"])
        cases_by_id = {str(c["id"]): c for c in snapshot["cases"]}
        work_orders = list((snapshot.get("procurement") or {}).get("work_orders") or [])

    violations: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    safety_breaches = 0
    consent_breaches = 0

    for wo in work_orders:
        state = str(wo.get("state") or "")
        if state == "Withdrawn":
            continue
        cid = str(wo.get("case_id") or "")
        wid = str(wo.get("id") or "")
        case = cases_by_id.get(cid)
        if case is None:
            consent_breaches += 1
            violations.append(
                dict(
                    suite=suite_name,
                    case_id=cid,
                    work_order_id=wid,
                    gate="resident",
                    rule_id=CONSENT_GATE_RULE_ID,
                    detail="Active work order references a missing home case.",
                )
            )
            continue
        versions = wo.get("versions")
        latest = versions[-1] if isinstance(versions, list) and versions else {}
        bindings = latest.get("resident_bindings") if isinstance(latest, dict) else None
        consent_reasons = (
            resident_gate(case, bindings, now=as_of_utc)  # type: ignore[no-untyped-call]
            if isinstance(bindings, list) and bindings
            else ["Work order has no explicit resident scope bindings."]
        )
        if consent_reasons:
            consent_breaches += 1
            violations.append(
                dict(
                    suite=suite_name,
                    case_id=cid,
                    work_order_id=wid,
                    gate="resident",
                    rule_id=CONSENT_GATE_RULE_ID,
                    detail=f"Work order in state '{state}' lacks valid agreement or exception.",
                )
            )
        if state in ("Appointed", "Completed"):
            open_safety = Store._open_safety_items(case, staff=staff_list)  # type: ignore[no-untyped-call]
            if open_safety or gates._case_safety_state(case) is not True:
                safety_breaches += 1
                violations.append(
                    dict(
                        suite=suite_name,
                        case_id=cid,
                        work_order_id=wid,
                        gate="safety",
                        rule_id=SAFETY_GATE_RULE_ID,
                        detail=(
                            f"Work order in state '{state}' exists with unresolved safety evidence."
                        ),
                    )
                )

    for cid, case in sorted(cases_by_id.items()):
        open_safety = Store._open_safety_items(case, staff=staff_list)  # type: ignore[no-untyped-call]
        safety_ok = not open_safety and gates._case_safety_state(case) is True
        advance_events = [
            ev
            for ev in (case.get("returns") or [])
            if isinstance(ev, dict) and ev.get("event_type") == "advance"
        ]
        if advance_events:
            if not safety_ok:
                safety_breaches += 1
                violations.append(
                    dict(
                        suite=suite_name,
                        case_id=cid,
                        gate="safety",
                        rule_id=SAFETY_GATE_RULE_ID,
                        detail="Recorded controlled advance event on case with unresolved safety.",
                    )
                )
            if resident_gate(case, now=as_of_utc):  # type: ignore[no-untyped-call]
                consent_breaches += 1
                violations.append(
                    dict(
                        suite=suite_name,
                        case_id=cid,
                        gate="resident",
                        rule_id=CONSENT_GATE_RULE_ID,
                        detail=(
                            "Recorded controlled advance event without valid agreement "
                            "or exception."
                        ),
                    )
                )
        for qrec in case.get("quality") or []:
            if not isinstance(qrec, dict) or qrec.get("state") not in ("Accepted", "Handed over"):
                continue
            if not safety_ok:
                safety_breaches += 1
                violations.append(
                    dict(
                        suite=suite_name,
                        case_id=cid,
                        gate="safety",
                        rule_id=SAFETY_GATE_RULE_ID,
                        detail=f"Quality record '{qrec.get('state')}' with unresolved safety.",
                    )
                )
            binding = qrec.get("resident_binding")
            q_reasons = resident_gate(  # type: ignore[no-untyped-call]
                case,
                [binding] if isinstance(binding, dict) else [],
                now=as_of_utc,
            )
            if q_reasons:
                consent_breaches += 1
                violations.append(
                    dict(
                        suite=suite_name,
                        case_id=cid,
                        gate="resident",
                        rule_id=CONSENT_GATE_RULE_ID,
                        detail=(
                            f"Quality record '{qrec.get('state')}' lacks valid agreement "
                            "or exception."
                        ),
                    )
                )

    with _open_exercise_store(snapshot, use_sql=False) as probe_store:
        for cid in sorted(probe_store.cases):
            c = probe_store.cases[cid]
            open_safety = Store._open_safety_items(c, staff=staff_list)  # type: ignore[no-untyped-call]
            resident_reasons = resident_gate(c, now=as_of_utc)  # type: ignore[no-untyped-call]
            booking = {r.gate: r for r in gates.booking_gates(c, resident_reasons, on=as_of_day)}
            if open_safety or gates._case_safety_state(c) is not True:
                if booking["safety"].passed:
                    safety_breaches += 1
                    violations.append(
                        dict(
                            suite=suite_name,
                            case_id=cid,
                            gate="safety",
                            rule_id=SAFETY_GATE_RULE_ID,
                            detail=(
                                "gates.booking_gates passed safety despite unresolved safety state."
                            ),
                        )
                    )
                ok = _assert_blocked_attempt(
                    probe_store,
                    cid,
                    attempt_label="probe_require_safety_clear",
                    gate_kind="safety",
                    expected_substrings=("stopped for safety review",),
                    fn=partial(probe_store.require_safety_clear, c),
                    attempts_out=attempts,
                    violations_out=violations,
                )
                if not ok:
                    safety_breaches += 1
            if resident_reasons:
                if booking["resident"].passed:
                    consent_breaches += 1
                    violations.append(
                        dict(
                            suite=suite_name,
                            case_id=cid,
                            gate="resident",
                            rule_id=CONSENT_GATE_RULE_ID,
                            detail=(
                                "gates.booking_gates passed resident despite unmet consent gate."
                            ),
                        )
                    )
                ok = _assert_blocked_attempt(
                    probe_store,
                    cid,
                    attempt_label="probe_require_resident_clear",
                    gate_kind="resident",
                    expected_substrings=(
                        "resident decision or authority needs confirmation",
                        "resident scope is unknown",
                        "tenure and lease",
                        "past retention",
                    ),
                    fn=partial(probe_store.require_resident_clear, c),
                    attempts_out=attempts,
                    violations_out=violations,
                )
                if not ok:
                    consent_breaches += 1

    safety_attempts = [a for a in attempts if a["gate"] == "safety"]
    consent_attempts = [a for a in attempts if a["gate"] == "resident"]
    return dict(
        suite=suite_name,
        as_of=as_of_day,
        passed=safety_breaches == 0 and consent_breaches == 0 and not violations,
        cases_checked=len(cases_by_id),
        work_orders_checked=len(work_orders),
        safety_progression_attempts=len(safety_attempts),
        safety_progression_blocked=sum(1 for a in safety_attempts if a["blocked"]),
        controlled_progressions_with_unresolved_safety=safety_breaches,
        consent_work_start_attempts=len(consent_attempts),
        consent_work_start_blocked=sum(1 for a in consent_attempts if a["blocked"]),
        work_started_without_agreement_or_exception=consent_breaches,
        attempts=attempts,
        violations=violations,
    )


def _run_constructed_workbench_suite(*, as_of_day: str, use_sql: bool) -> dict[str, Any]:
    data = _constructed_workbench_dataset(as_of_day)
    attempts: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []
    safety_breaches = 0
    consent_breaches = 0
    positive_controls = 0

    with _open_exercise_store(data, use_sql=use_sql) as store:
        base_inv = verify_store_safety_and_consent_invariants(
            store,
            suite_name="constructed_workbench_seed",
            as_of=as_of_day,
        )
        attempts.extend(base_inv["attempts"])
        violations.extend(base_inv["violations"])
        safety_breaches += int(base_inv["controlled_progressions_with_unresolved_safety"])
        consent_breaches += int(base_inv["work_started_without_agreement_or_exception"])

        pid = _seed_package_and_capacity(store, package_name="PKG-81-ISSUED")
        pid_appt = _seed_package_and_capacity(
            store, package_name="PKG-81-APPOINTED", doc_id="SYN-COMMITMENT-81B"
        )
        pid_done = _seed_package_and_capacity(
            store, package_name="PKG-81-COMPLETED", doc_id="SYN-COMMITMENT-81C"
        )
        sam = store.staff["sam@example.test"]
        pam = store.staff["pam@example.test"]
        bea = store.staff["bea@example.test"]
        blair = store.staff["blair@example.test"]
        quin = store.staff["quin@example.test"]
        quil = store.staff["quil@example.test"]
        bindings = [dict(measure=MEASURE, context_revision=1)]
        q_items = {
            lab: "SYN photographed and checked"
            for lab in checklist_for(MEASURE)["items"]  # type: ignore[no-untyped-call]
        }
        q_wall_items = {
            lab: "SYN photographed and checked"
            for lab in checklist_for("Wall insulation")["items"]  # type: ignore[no-untyped-call]
        }

        # Prepare ZF-5 with work orders across Issued (2/3 confirmed), Appointed (3/3 confirmed),
        # and Completed states plus Submitted and Accepted quality records so all 10 controlled
        # progression entrypoints hit require_safety_clear directly.
        wid_zf5 = store.issue_work_order(pam, pid, "ZF-5", resident_bindings=bindings)  # type: ignore[no-untyped-call]
        offer_zf5 = _offer_and_confirm_appointment(
            store, pam, wid_zf5, when="2098-06-01", confirm_all=False
        )
        wid_zf5_appointed = store.issue_work_order(  # type: ignore[no-untyped-call]
            pam, pid_appt, "ZF-5", resident_bindings=bindings
        )
        _offer_and_confirm_appointment(
            store, pam, wid_zf5_appointed, when="2098-06-15", confirm_all=True
        )
        wid_zf5_completed = store.issue_work_order(  # type: ignore[no-untyped-call]
            pam, pid_done, "ZF-5", resident_bindings=bindings
        )
        _offer_and_confirm_appointment(
            store, pam, wid_zf5_completed, when="2098-06-20", confirm_all=True
        )
        store.complete_work_order(pam, wid_zf5_completed, "SYN baseline completion")  # type: ignore[no-untyped-call]
        q_idx_zf5 = store.submit_quality(  # type: ignore[no-untyped-call]
            sam, "ZF-5", MEASURE, "Install Team", "Installer", q_items, context_revision=1
        )
        q_idx_zf5_accepted = store.submit_quality(  # type: ignore[no-untyped-call]
            sam,
            "ZF-5",
            "Wall insulation",
            "Wall Team",
            "Installer",
            q_wall_items,
            context_revision=1,
        )
        store.accept_quality(quil, "ZF-5", q_idx_zf5_accepted, "SYN baseline acceptance")  # type: ignore[no-untyped-call]

        # Raise, refer, receive, accept, and record repair on ZF-4 to verify FR-002 emergency
        # referral stays open and repaired-but-unreleased still blocks progression.
        store.refer_hazard(  # type: ignore[no-untyped-call]
            sam,
            "ZF-4",
            0,
            bea["email"],
            "EXT-HAZ-81",
            metadata=dict(evidence="SYN referral sent to Building Safety Liaison"),
        )
        store.receive_hazard(bea, "ZF-4", 0, "SYN external receipt ref")  # type: ignore[no-untyped-call]
        store.accept_hazard(bea, "ZF-4", 0, "SYN external acceptance ref")  # type: ignore[no-untyped-call]
        store.record_repair(bea, "ZF-4", 0, "SYN external damp remediation certificate")  # type: ignore[no-untyped-call]

        # Same-person safety release check must fail closed.
        same_person_verdict = gates.safety_release_gate(
            {"accountable_role": "Building Safety Liaison"},
            bea,
            [bea["email"]],
            on=as_of_day,
        )
        if same_person_verdict.passed:
            safety_breaches += 1
            violations.append(
                dict(
                    case_id="ZF-4",
                    check="same_person_safety_release_gate",
                    gate="safety",
                    rule_id=SAFETY_GATE_RULE_ID,
                    detail="Same-person safety release unexpectedly passed.",
                )
            )

        safety_mutations: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
            (
                "active_hazard",
                lambda c: c.update(
                    hazards=[
                        dict(
                            category="Damp and mould",
                            priority="Emergency",
                            noticed="2026-01-05",
                            referred=None,
                            repaired=None,
                            released=False,
                            job="J-ACT",
                            owner="Bea Safe",
                        )
                    ]
                ),
            ),
            (
                "repaired_unreleased_hazard",
                lambda c: c.update(hazards=deepcopy(store.cases["ZF-4"]["hazards"])),
            ),
            (
                "standalone_safeguarding_item",
                lambda c: c.update(
                    hazards=[],
                    safeguarding_items=[
                        dict(
                            id="SG-81-1",
                            category="Safeguarding",
                            priority="Urgent",
                            aware_at="2026-01-05T09:00:00Z",
                            released=False,
                            status="Open",
                            owner="Bea Safe",
                        )
                    ],
                ),
            ),
            (
                "non_boolean_released_string",
                lambda c: c.update(
                    hazards=[dict(category="Electrical", priority="P1", released="false")],
                    safeguarding_items=[],
                ),
            ),
            (
                "malformed_legacy_safeguarding",
                lambda c: c.update(hazards=[], safeguarding_items=[], safeguarding="corrupt"),
            ),
            (
                "missing_none_hazards",
                lambda c: c.update(hazards=None, safeguarding_items=[], safeguarding=None),
            ),
        )

        for shape_name, mutate_case in safety_mutations:
            with store.lock:
                zf5_ref = store._case("ZF-5")  # type: ignore[no-untyped-call]
                saved_case = deepcopy(zf5_ref)
                mutate_case(zf5_ref)
                store.save()  # type: ignore[no-untyped-call]
            try:
                safety_entrypoints: tuple[tuple[str, Callable[[], object]], ...] = (
                    (f"{shape_name}:advance", lambda: store.advance(pam, "ZF-5")),  # type: ignore[no-untyped-call]
                    (
                        f"{shape_name}:signoff_give",
                        lambda: store.technical_action(  # type: ignore[no-untyped-call]
                            quin,
                            "ZF-5",
                            dict(action="signoff_give", type="assessment", note="SYN"),
                        ),
                    ),
                    (
                        f"{shape_name}:issue_work_order",
                        lambda: store.issue_work_order(  # type: ignore[no-untyped-call]
                            pam, pid, "ZF-4", resident_bindings=bindings
                        ),
                    ),
                    (
                        f"{shape_name}:reissue_work_order",
                        lambda: store.reissue_work_order(  # type: ignore[no-untyped-call]
                            pam, wid_zf5, "SYN updated scope", "SYN scope note", bindings
                        ),
                    ),
                    (
                        f"{shape_name}:appointment_confirm_activate",
                        partial(
                            store.appointment_control,
                            pam,
                            wid_zf5,
                            dict(
                                action="confirm",
                                event_ref=f"{offer_zf5}-cap-{shape_name}",
                                offer_id=offer_zf5,
                                kind="capacity",
                                person="SYN supplier authorized contact",
                                source="SYN capacity confirmation",
                                channel="Phone, manually recorded",
                            ),
                        ),
                    ),
                    (
                        f"{shape_name}:record_wo_appointment_booked",
                        lambda: store.record_wo_appointment(  # type: ignore[no-untyped-call]
                            pam, wid_zf5_appointed, "Booked", "2098-06-15"
                        ),
                    ),
                    (
                        f"{shape_name}:complete_work_order",
                        lambda: store.complete_work_order(  # type: ignore[no-untyped-call]
                            pam, wid_zf5_appointed, "SYN complete"
                        ),
                    ),
                    (
                        f"{shape_name}:correct_work_order",
                        lambda: store.correct_work_order(  # type: ignore[no-untyped-call]
                            pam, wid_zf5_completed, "SYN correction", "SYN scope", bindings
                        ),
                    ),
                    (
                        f"{shape_name}:accept_quality",
                        lambda: store.accept_quality(quil, "ZF-5", q_idx_zf5, "SYN accept"),  # type: ignore[no-untyped-call]
                    ),
                    (
                        f"{shape_name}:hand_over_quality",
                        lambda: store.hand_over_quality(  # type: ignore[no-untyped-call]
                            sam, "ZF-5", q_idx_zf5_accepted, "SYN handover pack", True
                        ),
                    ),
                )
                for label, call in safety_entrypoints:
                    target_cid = "ZF-4" if label.endswith(":issue_work_order") else "ZF-5"
                    if not _assert_blocked_attempt(
                        store,
                        target_cid,
                        attempt_label=label,
                        gate_kind="safety",
                        expected_substrings=("stopped for safety review",),
                        fn=call,
                        attempts_out=attempts,
                        violations_out=violations,
                    ):
                        safety_breaches += 1
            finally:
                with store.lock:
                    restored_zf5 = store._case("ZF-5")  # type: ignore[no-untyped-call]
                    restored_zf5.clear()
                    restored_zf5.update(saved_case)
                    store.save()  # type: ignore[no-untyped-call]

        # Consent / agreement refusals on ZF-1 (Waiting, no scope), ZF-2 (Waiting, scoped),
        # ZF-3-LEGACY (legacy case-wide Accepted, no measure_decisions), consultation note,
        # paused/withdrawn decision, and FR-008 design-version bump.
        store.log_call(sam, "ZF-2", "Discussed loft insulation options", "Consultation call only")  # type: ignore[no-untyped-call]
        for unconsented_cid in ("ZF-1", "ZF-2", "ZF-3-LEGACY"):
            for label, call in (
                (
                    f"{unconsented_cid}:issue_work_order_unconsented",
                    partial(
                        store.issue_work_order,
                        pam,
                        pid,
                        unconsented_cid,
                        resident_bindings=bindings,
                    ),
                ),
                (
                    f"{unconsented_cid}:issue_work_order_unbound",
                    partial(store.issue_work_order, pam, pid, unconsented_cid),
                ),
            ):
                if not _assert_blocked_attempt(
                    store,
                    unconsented_cid,
                    attempt_label=label,
                    gate_kind="resident",
                    expected_substrings=(
                        "resident decision or authority needs confirmation",
                        "resident scope is unknown",
                    ),
                    fn=call,
                    attempts_out=attempts,
                    violations_out=violations,
                ):
                    consent_breaches += 1
            if store.cases[unconsented_cid]["stage"] == READY_STAGE:
                if not _assert_blocked_attempt(
                    store,
                    unconsented_cid,
                    attempt_label=f"{unconsented_cid}:advance_unconsented",
                    gate_kind="resident",
                    expected_substrings=("resident decision or authority needs confirmation",),
                    fn=partial(store.advance, pam, unconsented_cid),
                    attempts_out=attempts,
                    violations_out=violations,
                ):
                    consent_breaches += 1

        # Positive control on ZF-3 (valid scoped acceptance + clear safety): issue, appoint,
        # and advance.
        wid_zf3 = store.issue_work_order(pam, pid, "ZF-3", resident_bindings=bindings)  # type: ignore[no-untyped-call]
        _offer_and_confirm_appointment(store, pam, wid_zf3, when="2098-07-01", confirm_all=True)
        store.advance(pam, "ZF-3")  # type: ignore[no-untyped-call]
        if store.cases["ZF-3"]["stage"] == "Install booked":
            positive_controls += 1

        # FR-008 scope/design drift on ZF-5: bumping design_version to 2 invalidates prior consent
        # and immediately blocks appointment activation, completion, and quality acceptance.
        store.technical_action(  # type: ignore[no-untyped-call]
            pam, "ZF-5", dict(action="design_change", note="Revised loft hatch specification")
        )
        for label, call in (
            (
                "ZF-5:design_drift_appointment_confirm",
                lambda: store.appointment_control(
                    pam,
                    wid_zf5,
                    dict(
                        action="confirm",
                        event_ref=f"{offer_zf5}-cap-drift",
                        offer_id=offer_zf5,
                        kind="capacity",
                        person="SYN supplier authorized contact",
                        source="SYN capacity confirmation",
                        channel="Phone, manually recorded",
                    ),
                ),
            ),
            (
                "ZF-5:design_drift_accept_quality",
                lambda: store.accept_quality(quil, "ZF-5", q_idx_zf5, "SYN accept after drift"),  # type: ignore[no-untyped-call]
            ),
        ):
            if not _assert_blocked_attempt(
                store,
                "ZF-5",
                attempt_label=label,
                gate_kind="resident",
                expected_substrings=(
                    "resident decision or authority needs confirmation",
                    "scope changed",
                ),
                fn=call,
                attempts_out=attempts,
                violations_out=violations,
            ):
                consent_breaches += 1

        # Same-person safety release by the repair recorder (bea) must fail closed, then
        # independent Building Safety Liaison (blair) release succeeds and unlocks ZF-4.
        if not _assert_blocked_attempt(
            store,
            "ZF-4",
            attempt_label="ZF-4:same_person_release_hazard",
            gate_kind="safety",
            expected_substrings=("someone other than the reporter and repair recorder",),
            fn=partial(
                store.release_hazard,
                bea,
                "ZF-4",
                0,
                "Self-release attempt",
                "SYN self-release",
            ),
            attempts_out=attempts,
            violations_out=violations,
        ):
            safety_breaches += 1

        store.release_hazard(  # type: ignore[no-untyped-call]
            blair,
            "ZF-4",
            0,
            "External damp remediation verified",
            "SYN independent safety clearance certificate",
        )
        wid_zf4 = store.issue_work_order(pam, pid, "ZF-4", resident_bindings=bindings)  # type: ignore[no-untyped-call]
        if wid_zf4:
            positive_controls += 1

    safety_attempts = [a for a in attempts if a["gate"] == "safety"]
    consent_attempts = [a for a in attempts if a["gate"] == "resident"]
    return dict(
        suite="constructed_workbench",
        passed=safety_breaches == 0 and consent_breaches == 0 and not violations,
        cases_checked=len(data["cases"]),
        positive_controls_verified=positive_controls,
        safety_progression_attempts=len(safety_attempts),
        safety_progression_blocked=sum(1 for a in safety_attempts if a["blocked"]),
        controlled_progressions_with_unresolved_safety=safety_breaches,
        consent_work_start_attempts=len(consent_attempts),
        consent_work_start_blocked=sum(1 for a in consent_attempts if a["blocked"]),
        work_started_without_agreement_or_exception=consent_breaches,
        violations=violations,
    )


def _run_resident_preview_suite(*, as_of_day: str, use_sql: bool) -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []
    safety_breaches = 0
    consent_breaches = 0

    with tempfile.TemporaryDirectory(prefix="zf-81-preview-") as tmp:
        preview_dir = Path(tmp) / "preview"
        dataset_path, _ = resident_preview_fixture.build(preview_dir)
        raw_data = json.loads(dataset_path.read_text(encoding="utf-8"))
        with _open_exercise_store(
            raw_data,
            use_sql=use_sql,
            docs_source_dir=preview_dir / "docs",
        ) as store:
            inv = verify_store_safety_and_consent_invariants(
                store,
                suite_name="resident_preview",
                as_of=as_of_day,
            )
            attempts.extend(inv["attempts"])
            violations.extend(inv["violations"])
            safety_breaches += int(inv["controlled_progressions_with_unresolved_safety"])
            consent_breaches += int(inv["work_started_without_agreement_or_exception"])

            sam = store.staff["sam@example.test"]
            pam = store.staff["pam@example.test"]
            pid = str(store.data["procurement"]["packages"][0]["id"])
            wos_by_case = {
                str(w["case_id"]): str(w["id"]) for w in store.data["procurement"]["work_orders"]
            }
            bindings = [dict(measure=resident_preview_fixture.MEASURES[0], context_revision=1)]

            # SYN-C3 has an active P1 Damp hazard and Waiting decision and zero work orders.
            if "SYN-C3" in wos_by_case:
                safety_breaches += 1
                consent_breaches += 1
                violations.append(
                    dict(
                        case_id="SYN-C3",
                        check="syn_c3_static_no_work_order",
                        gate="safety",
                        rule_id=SAFETY_GATE_RULE_ID,
                        detail="SYN-C3 unexpectedly has an issued or appointed work order.",
                    )
                )

            if not _assert_blocked_attempt(
                store,
                "SYN-C3",
                attempt_label="SYN-C3:issue_work_order_with_hazard",
                gate_kind="safety",
                expected_substrings=("stopped for safety review",),
                fn=lambda: store.issue_work_order(  # type: ignore[no-untyped-call]
                    pam, pid, "SYN-C3", resident_bindings=bindings
                ),
                attempts_out=attempts,
                violations_out=violations,
            ):
                safety_breaches += 1

            # Even if SYN-C3's hazard were cleared in isolation, consent is still Waiting ->
            # blocked.
            with store.lock:
                syn_c3_ref = store._case("SYN-C3")  # type: ignore[no-untyped-call]
                saved_hazards = deepcopy(syn_c3_ref["hazards"])
                syn_c3_ref["hazards"] = []
                store.save()  # type: ignore[no-untyped-call]
            try:
                if not _assert_blocked_attempt(
                    store,
                    "SYN-C3",
                    attempt_label="SYN-C3:issue_work_order_without_consent",
                    gate_kind="resident",
                    expected_substrings=(
                        "resident decision or authority needs confirmation",
                        "confirm the current measure scope",
                    ),
                    fn=lambda: store.issue_work_order(  # type: ignore[no-untyped-call]
                        pam, pid, "SYN-C3", resident_bindings=bindings
                    ),
                    attempts_out=attempts,
                    violations_out=violations,
                ):
                    consent_breaches += 1
            finally:
                with store.lock:
                    syn_c3_restore = store._case("SYN-C3")  # type: ignore[no-untyped-call]
                    syn_c3_restore["hazards"] = saved_hazards
                    store.save()  # type: ignore[no-untyped-call]

            # SYN-C2 representative SYN-REP-B has Attend/Receive information only (not Works
            # decision).
            if not _assert_blocked_attempt(
                store,
                "SYN-C2",
                attempt_label="SYN-C2:attend_only_rep_works_decision",
                gate_kind="resident",
                expected_substrings=("representative authority needs human confirmation",),
                fn=lambda: store.resident_action(  # type: ignore[no-untyped-call]
                    sam,
                    "SYN-C2",
                    dict(
                        action="decision_record",
                        measure=resident_preview_fixture.MEASURES[0],
                        context_revision=1,
                        status="Accepted",
                        answered_by="Their representative",
                        representative_ref="SYN-REP-B",
                        source="SYN-REP-CALL",
                        note="SYN",
                    ),
                ),
                attempts_out=attempts,
                violations_out=violations,
            ):
                consent_breaches += 1

            # Pausing consent on SYN-C1 (Appointed work order) immediately blocks completion.
            wid_c1 = wos_by_case["SYN-C1"]
            store.resident_action(  # type: ignore[no-untyped-call]
                sam,
                "SYN-C1",
                dict(
                    action="decision_record",
                    measure=resident_preview_fixture.MEASURES[0],
                    context_revision=1,
                    status="Paused",
                    answered_by="The resident",
                    source="SYN-PAUSE",
                    note="Resident asked to pause works",
                ),
            )
            if not _assert_blocked_attempt(
                store,
                "SYN-C1",
                attempt_label="SYN-C1:complete_after_resident_pause",
                gate_kind="resident",
                expected_substrings=("resident decision or authority needs confirmation",),
                fn=lambda: store.complete_work_order(pam, wid_c1, "SYN complete"),  # type: ignore[no-untyped-call]
                attempts_out=attempts,
                violations_out=violations,
            ):
                consent_breaches += 1

    safety_attempts = [a for a in attempts if a["gate"] == "safety"]
    consent_attempts = [a for a in attempts if a["gate"] == "resident"]
    return dict(
        suite="resident_preview",
        passed=safety_breaches == 0 and consent_breaches == 0 and not violations,
        cases_checked=3,
        safety_progression_attempts=len(safety_attempts),
        safety_progression_blocked=sum(1 for a in safety_attempts if a["blocked"]),
        controlled_progressions_with_unresolved_safety=safety_breaches,
        consent_work_start_attempts=len(consent_attempts),
        consent_work_start_blocked=sum(1 for a in consent_attempts if a["blocked"]),
        work_started_without_agreement_or_exception=consent_breaches,
        violations=violations,
    )


def _run_sensor_retrofit_suite(*, as_of_day: str, use_sql: bool) -> dict[str, Any]:
    generated = sensor_scenarios.generate(seed=sensor_scenarios.SEED)
    retrofit_views = {
        str(row["case_id"]): row
        for row in sensor_scenarios.retrofit_exercise_scenarios(seed=sensor_scenarios.SEED)
    }
    cases: list[dict[str, Any]] = []
    for sc in generated:
        cid = f"SENS-{sc.case_id}"
        is_damp_hold = sc.truth.family == "damp" and sc.truth.expected_outcome in (
            sensor_scenarios.REVIEW,
            sensor_scenarios.INSUFFICIENT,
        )
        hazards = (
            [
                dict(
                    category="Damp and mould",
                    priority="Significant",
                    noticed="2026-01-10",
                    referred=None,
                    repaired=None,
                    released=False,
                    job=f"JOB-{sc.case_id}",
                    owner="Bea Safe",
                )
            ]
            if is_damp_hold
            else []
        )
        c = _base_case(
            cid,
            stage=READY_STAGE,
            decision="Accepted" if is_damp_hold else "Waiting",
            funding=True,
            hazards=hazards,
        )
        # Give damp-hold cases valid consent so safety is the sole blocker, and give retrofit
        # cases C08..C11 clear safety with Waiting consent so consent is the sole blocker.
        _apply_resident_scope(c, accepted=is_damp_hold)
        if sc.case_id in retrofit_views:
            c["notes"] = str(retrofit_views[sc.case_id]["value_status"])
        cases.append(c)

    data = dict(as_of=as_of_day, staff=_staff_seed(), cases=cases)
    attempts: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []
    safety_breaches = 0
    consent_breaches = 0

    with _open_exercise_store(data, use_sql=use_sql) as store:
        pid = _seed_package_and_capacity(store, capacity=30)
        sam = store.staff["sam@example.test"]
        pam = store.staff["pam@example.test"]
        bea = store.staff["bea@example.test"]
        bindings = [dict(measure=MEASURE, context_revision=1)]

        for sc in generated:
            cid = f"SENS-{sc.case_id}"
            is_damp_hold = sc.truth.family == "damp" and sc.truth.expected_outcome in (
                sensor_scenarios.REVIEW,
                sensor_scenarios.INSUFFICIENT,
            )
            if is_damp_hold:
                for label, call in (
                    (
                        f"{cid}:damp_hold_issue_work_order",
                        partial(store.issue_work_order, pam, pid, cid, resident_bindings=bindings),
                    ),
                    (
                        f"{cid}:damp_hold_advance",
                        partial(store.advance, pam, cid),
                    ),
                ):
                    if not _assert_blocked_attempt(
                        store,
                        cid,
                        attempt_label=label,
                        gate_kind="safety",
                        expected_substrings=("stopped for safety review",),
                        fn=call,
                        attempts_out=attempts,
                        violations_out=violations,
                    ):
                        safety_breaches += 1
            elif sc.case_id in retrofit_views:
                for label, call in (
                    (
                        f"{cid}:retrofit_unconsented_issue_work_order",
                        partial(store.issue_work_order, pam, pid, cid, resident_bindings=bindings),
                    ),
                    (
                        f"{cid}:retrofit_unconsented_advance",
                        partial(store.advance, pam, cid),
                    ),
                ):
                    if not _assert_blocked_attempt(
                        store,
                        cid,
                        attempt_label=label,
                        gate_kind="resident",
                        expected_substrings=("resident decision or authority needs confirmation",),
                        fn=call,
                        attempts_out=attempts,
                        violations_out=violations,
                    ):
                        consent_breaches += 1

        # Sensor telemetry / absence-of-signal can never release a safety hold (RULE-001).
        store.refer_hazard(  # type: ignore[no-untyped-call]
            sam,
            "SENS-C02",
            0,
            bea["email"],
            "EXT-SENS-C02",
            metadata=dict(evidence="SYN human inspection referral"),
        )
        store.receive_hazard(bea, "SENS-C02", 0, "SYN safety receipt")  # type: ignore[no-untyped-call]
        store.accept_hazard(bea, "SENS-C02", 0, "SYN safety acceptance")  # type: ignore[no-untyped-call]
        if not _assert_blocked_attempt(
            store,
            "SENS-C02",
            attempt_label="SENS-C02:sensor_telemetry_repair_refused",
            gate_kind="safety",
            expected_substrings=(controls.SENSOR_REFUSAL,),
            fn=lambda: store.record_repair(  # type: ignore[no-untyped-call]
                bea, "SENS-C02", 0, "NO_EXERCISE_SIGNAL from sensor_reading:1"
            ),
            attempts_out=attempts,
            violations_out=violations,
        ):
            safety_breaches += 1

    safety_attempts = [a for a in attempts if a["gate"] == "safety"]
    consent_attempts = [a for a in attempts if a["gate"] == "resident"]
    return dict(
        suite="sensor_retrofit",
        passed=safety_breaches == 0 and consent_breaches == 0 and not violations,
        cases_checked=len(cases),
        retrofit_cases_checked=len(retrofit_views),
        safety_progression_attempts=len(safety_attempts),
        safety_progression_blocked=sum(1 for a in safety_attempts if a["blocked"]),
        controlled_progressions_with_unresolved_safety=safety_breaches,
        consent_work_start_attempts=len(consent_attempts),
        consent_work_start_blocked=sum(1 for a in consent_attempts if a["blocked"]),
        work_started_without_agreement_or_exception=consent_breaches,
        violations=violations,
    )


def _scale_case_from_row(
    cid: str,
    *,
    open_safety_issue: bool,
    consent_state: str,
    rep_state: str,
) -> tuple[dict[str, Any], bool]:
    """Project one scale_fixture combination into a Store case and return (case, allow_work)."""
    hazards = (
        [
            dict(
                category="Structural",
                priority="P1",
                noticed="2026-01-12",
                referred=None,
                repaired=None,
                released=False,
                job=f"SC-{cid}",
                owner="Bea Safe",
            )
        ]
        if open_safety_issue
        else []
    )
    c = _base_case(
        cid,
        stage=READY_STAGE,
        decision="Accepted" if consent_state == "Given" else "Waiting",
        funding=True,
        hazards=hazards,
    )
    if rep_state == "None recorded":
        _apply_resident_scope(c, accepted=(consent_state == "Given"))
        valid_consent = consent_state == "Given"
    elif rep_state == "Claimed - unverified":
        # Representative claimed without confirmed safe-contact authority -> must fail closed!
        _apply_resident_scope(
            c,
            accepted=(consent_state == "Given"),
            answered_by="Their representative",
            representative_ref="REP-UNVERIFIED",
            authority_version=1,
        )
        valid_consent = False
    else:
        # Authorised - evidence on file
        rep_ref = f"REP-AUTH-{cid}"
        c["resident_safe_contact"] = f"SAFE-{cid}"
        c["resident_contact_history"] = [
            dict(revision=1, safe_contact_ref=f"SAFE-{cid}", source="SYN-SAFE", at="2026-01-01")
        ]
        c["representative_authorities"] = {
            rep_ref: [
                dict(
                    version=1,
                    representative_ref=rep_ref,
                    status="Confirmed",
                    tasks=["Receive information", "Communicate", "Attend", "Works decision"],
                    measure=MEASURE,
                    context_revision=1,
                    safe_contact_ref=f"SAFE-{cid}",
                    safe_contact_revision=1,
                    authority_date="2026-01-01",
                    review_date="2099-01-01",
                    source="SYN-AUTH-FILE",
                    resident_wishes="SYN",
                )
            ]
        }
        _apply_resident_scope(
            c,
            accepted=(consent_state == "Given"),
            answered_by="Their representative",
            representative_ref=rep_ref,
            authority_version=1,
        )
        valid_consent = consent_state == "Given"

    if consent_state in ("Declined", "Withdrawn"):
        c.setdefault("measure_decisions", {})[MEASURE] = [
            dict(
                version=1,
                context_revision=1,
                status=consent_state,
                answered_by="The resident",
                case_id=cid,
                measure=MEASURE,
                scope="SYN-LOFT-SCOPE",
                design_version=1,
                source="SYN-SCALE",
                recorded_by="Sam Example",
                recorded_by_email="sam@example.test",
                at="2026-01-02",
            )
        ]
        if consent_state == "Withdrawn":
            c["resident_reviews"] = {MEASURE: dict(status="Needs human review")}
    return c, (not open_safety_issue and valid_consent)


def _run_scale_matrix_suite(*, as_of_day: str, use_sql: bool) -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    expected_allow: dict[str, bool] = {}
    expected_safety_block: dict[str, bool] = {}

    idx = 0
    for open_safety in (False, True):
        for consent_state in scale_fixture.CONSENT_STATES:
            for rep_state in scale_fixture.REP_STATES:
                idx += 1
                cid = f"SCALE-M{idx:02d}"
                c, allow = _scale_case_from_row(
                    cid,
                    open_safety_issue=open_safety,
                    consent_state=consent_state,
                    rep_state=rep_state,
                )
                cases.append(c)
                expected_allow[cid] = allow
                expected_safety_block[cid] = open_safety

    for home, hh in zip(
        scale_fixture.homes(n=12, seed=scale_fixture.SEED),  # type: ignore[no-untyped-call]
        scale_fixture.households(n=12, seed=scale_fixture.SEED),  # type: ignore[no-untyped-call]
        strict=True,
    ):
        cid = f"SCALE-{home['id']}"
        open_safety = bool(home["open_safety_issue"])
        consent_state = str(hh["works_consent_state"])
        rep_state = (
            str(hh["representative_state"])
            if hh.get("works_consent_given_by") == "Representative"
            else "None recorded"
        )
        c, allow = _scale_case_from_row(
            cid,
            open_safety_issue=open_safety,
            consent_state=consent_state,
            rep_state=rep_state,
        )
        cases.append(c)
        expected_allow[cid] = allow
        expected_safety_block[cid] = open_safety

    data = dict(as_of=as_of_day, staff=_staff_seed(), cases=cases)
    attempts: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []
    safety_breaches = 0
    consent_breaches = 0
    allowed_count = 0

    with _open_exercise_store(data, use_sql=use_sql) as store:
        pid = _seed_package_and_capacity(store, capacity=60)
        pam = store.staff["pam@example.test"]
        bindings = [dict(measure=MEASURE, context_revision=1)]

        for cid in sorted(expected_allow):
            if expected_allow[cid]:
                wid = store.issue_work_order(pam, pid, cid, resident_bindings=bindings)  # type: ignore[no-untyped-call]
                _offer_and_confirm_appointment(store, pam, wid, when="2098-08-01", confirm_all=True)
                store.advance(pam, cid)  # type: ignore[no-untyped-call]
                allowed_count += 1
            elif expected_safety_block[cid]:
                for label, call in (
                    (
                        f"{cid}:safety_block_issue_work_order",
                        partial(store.issue_work_order, pam, pid, cid, resident_bindings=bindings),
                    ),
                    (
                        f"{cid}:safety_block_advance",
                        partial(store.advance, pam, cid),
                    ),
                ):
                    if not _assert_blocked_attempt(
                        store,
                        cid,
                        attempt_label=label,
                        gate_kind="safety",
                        expected_substrings=("stopped for safety review",),
                        fn=call,
                        attempts_out=attempts,
                        violations_out=violations,
                    ):
                        safety_breaches += 1
            else:
                for label, call in (
                    (
                        f"{cid}:consent_block_issue_work_order",
                        partial(store.issue_work_order, pam, pid, cid, resident_bindings=bindings),
                    ),
                    (
                        f"{cid}:consent_block_advance",
                        partial(store.advance, pam, cid),
                    ),
                ):
                    if not _assert_blocked_attempt(
                        store,
                        cid,
                        attempt_label=label,
                        gate_kind="resident",
                        expected_substrings=("resident decision or authority needs confirmation",),
                        fn=call,
                        attempts_out=attempts,
                        violations_out=violations,
                    ):
                        consent_breaches += 1

    safety_attempts = [a for a in attempts if a["gate"] == "safety"]
    consent_attempts = [a for a in attempts if a["gate"] == "resident"]
    return dict(
        suite="scale_matrix",
        passed=safety_breaches == 0 and consent_breaches == 0 and not violations,
        cases_checked=len(cases),
        positive_work_starts_verified=allowed_count,
        safety_progression_attempts=len(safety_attempts),
        safety_progression_blocked=sum(1 for a in safety_attempts if a["blocked"]),
        controlled_progressions_with_unresolved_safety=safety_breaches,
        consent_work_start_attempts=len(consent_attempts),
        consent_work_start_blocked=sum(1 for a in consent_attempts if a["blocked"]),
        work_started_without_agreement_or_exception=consent_breaches,
        violations=violations,
    )


def _valid_exception_record(
    *,
    measure: str = MEASURE,
    context_revision: int = 1,
    design_version: int = 1,
    **overrides: Any,
) -> dict[str, Any]:
    record: dict[str, Any] = dict(
        reference="EXC-81-001",
        status="Authorised",
        measure=measure,
        context_revision=context_revision,
        design_version=design_version,
        rule_source="Tenancy urgent fabric protection clause 14.2 (exercise fixture)",
        reason="Prevent imminent winter water ingress into loft void where resident unavailable",
        approved_by="Bea Safe",
        approved_by_role="Building Safety Liaison",
        effective_date="2026-01-01",
        review_date="2099-01-01",
        expires_at="2099-01-01T00:00:00+00:00",
        resident_notified=True,
        notification_ref="NOTIF-LETTER-81-001",
    )
    record.update(overrides)
    return record


def _run_authorised_exception_suite(
    *,
    as_of_day: str,
    as_of_utc: str,
    use_sql: bool,
) -> dict[str, Any]:
    valid_case = _base_case("EXC-VALID", stage=READY_STAGE, funding=True)
    _apply_resident_scope(valid_case, accepted=False)
    valid_case["authorised_works_exceptions"] = {MEASURE: [_valid_exception_record()]}

    invalid_specs: tuple[tuple[str, dict[str, Any], bool], ...] = (
        ("EXC-AI", dict(approved_by="AI Assistant Bot"), False),
        ("EXC-ROLE", dict(approved_by_role="Resident Liaison Officer"), False),
        ("EXC-UNNOTIFIED", dict(resident_notified=False), False),
        ("EXC-BLANK-NOTIF", dict(notification_ref="   "), False),
        ("EXC-SENSOR-REF", dict(rule_source="sensor_reading:42"), False),
        ("EXC-EXPIRED-REVIEW", dict(review_date="2026-01-15"), False),
        ("EXC-EXPIRED-UTC", dict(expires_at="2026-01-15T00:00:00+00:00"), False),
        ("EXC-REVOKED", dict(status="Revoked"), False),
        ("EXC-DESIGN-MISMATCH", dict(design_version=2), False),
        ("EXC-WITH-HAZARD", {}, True),
    )
    cases = [valid_case]
    for cid, overrides, with_hazard in invalid_specs:
        hazards = (
            [
                dict(
                    category="Electrical",
                    priority="P1",
                    noticed="2026-01-08",
                    referred=None,
                    repaired=None,
                    released=False,
                    job=f"J-{cid}",
                    owner="Bea Safe",
                )
            ]
            if with_hazard
            else []
        )
        c = _base_case(cid, stage=READY_STAGE, funding=True, hazards=hazards)
        _apply_resident_scope(c, accepted=False)
        c["authorised_works_exceptions"] = {MEASURE: [_valid_exception_record(**overrides)]}
        cases.append(c)

    data = dict(as_of=as_of_day, staff=_staff_seed(), cases=cases)
    attempts: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []
    safety_breaches = 0
    consent_breaches = 0
    positive_exceptions = 0

    with _open_exercise_store(data, use_sql=use_sql) as store:
        pid = _seed_package_and_capacity(store, capacity=20)
        pam = store.staff["pam@example.test"]
        bindings = [dict(measure=MEASURE, context_revision=1)]

        # Valid current-scope exception approved by a named human with notification permits start
        # when safety is clear.
        ctx_valid = store.cases["EXC-VALID"]["resident_scopes"][MEASURE][-1]
        direct_valid = validate_authorised_works_exception(
            store.cases["EXC-VALID"],
            MEASURE,
            ctx_valid,
            now=as_of_utc,
        )
        if not direct_valid["permitted"]:
            consent_breaches += 1
            violations.append(
                dict(
                    case_id="EXC-VALID",
                    check="validate_authorised_works_exception_positive",
                    gate="resident",
                    rule_id=AUTHORISED_EXCEPTION_RULE_ID,
                    detail=f"Valid exception rejected: {direct_valid['reason']}",
                )
            )
        else:
            wid_exc = store.issue_work_order(  # type: ignore[no-untyped-call]
                pam, pid, "EXC-VALID", resident_bindings=bindings
            )
            _offer_and_confirm_appointment(store, pam, wid_exc, when="2098-09-01", confirm_all=True)
            store.advance(pam, "EXC-VALID")  # type: ignore[no-untyped-call]
            positive_exceptions += 1

        # All 10 invalid/unsafe exception variants must fail closed.
        for cid, _, with_hazard in invalid_specs:
            gate_kind = "safety" if with_hazard else "resident"
            expected_substrings = (
                ("stopped for safety review",)
                if with_hazard
                else ("resident decision or authority needs confirmation",)
            )
            if not with_hazard:
                ctx_c = store.cases[cid]["resident_scopes"][MEASURE][-1]
                direct = validate_authorised_works_exception(
                    store.cases[cid],
                    MEASURE,
                    ctx_c,
                    now=as_of_utc,
                )
                if direct["permitted"]:
                    consent_breaches += 1
                    violations.append(
                        dict(
                            case_id=cid,
                            check=f"{cid}:validate_authorised_works_exception_negative",
                            gate="resident",
                            rule_id=AUTHORISED_EXCEPTION_RULE_ID,
                            detail="Invalid works exception unexpectedly returned permitted=True.",
                        )
                    )
            for label, call in (
                (
                    f"{cid}:issue_work_order",
                    partial(store.issue_work_order, pam, pid, cid, resident_bindings=bindings),
                ),
                (
                    f"{cid}:advance",
                    partial(store.advance, pam, cid),
                ),
            ):
                if not _assert_blocked_attempt(
                    store,
                    cid,
                    attempt_label=label,
                    gate_kind=gate_kind,
                    expected_substrings=expected_substrings,
                    fn=call,
                    attempts_out=attempts,
                    violations_out=violations,
                ):
                    if with_hazard:
                        safety_breaches += 1
                    else:
                        consent_breaches += 1

    safety_attempts = [a for a in attempts if a["gate"] == "safety"]
    consent_attempts = [a for a in attempts if a["gate"] == "resident"]
    return dict(
        suite="authorised_exception_controls",
        passed=safety_breaches == 0 and consent_breaches == 0 and not violations,
        cases_checked=len(cases),
        positive_authorised_exceptions_verified=positive_exceptions,
        safety_progression_attempts=len(safety_attempts),
        safety_progression_blocked=sum(1 for a in safety_attempts if a["blocked"]),
        controlled_progressions_with_unresolved_safety=safety_breaches,
        consent_work_start_attempts=len(consent_attempts),
        consent_work_start_blocked=sum(1 for a in consent_attempts if a["blocked"]),
        work_started_without_agreement_or_exception=consent_breaches,
        violations=violations,
    )


def _run_learning_bundles_suite() -> dict[str, Any]:
    effort = {comp: 5.0 for comp in learning_test_bundles.COMPONENTS}
    bundle_checks: tuple[tuple[str, str | None, str], ...] = (
        ("story-once", None, "authority_or_consent_breaches"),
        ("pre-visit-pack", None, "offers_misread_as_commitments"),
        ("change-impact", "change-impact", "approvals_wrongly_carried_over"),
    )
    violations: list[dict[str, Any]] = []
    consent_breaches = 0
    stop_triggers_verified = 0

    for bundle_key, o16_owner, zero_measure in bundle_checks:
        bundle = learning_test_bundles.BUNDLES[bundle_key]
        clean_counts = {m: 0 for m in bundle.zero_measures}
        clean_run = dict(
            bundle=bundle_key,
            o16_counted_under=o16_owner,
            representative_data_retained=False,
            cases=[
                dict(
                    case=f"LB-{bundle_key}-1",
                    arms=dict(
                        comparator=dict(effort=dict(effort), counts=dict(clean_counts)),
                        workflow=dict(effort=dict(effort), counts=dict(clean_counts)),
                    ),
                )
            ],
        )
        clean_report = learning_test_bundles.run_report(clean_run)
        if clean_report["stop"] is not False or clean_report["breaches"] != []:
            consent_breaches += 1
            violations.append(
                dict(
                    bundle=bundle_key,
                    check=f"{bundle_key}:clean_zero_breaches",
                    gate="resident",
                    rule_id=CONSENT_GATE_RULE_ID,
                    detail="Clean learning bundle run unexpectedly reported breaches.",
                )
            )

        breach_counts = dict(clean_counts)
        breach_counts[zero_measure] = 1
        breach_run = dict(
            bundle=bundle_key,
            o16_counted_under=o16_owner,
            representative_data_retained=False,
            cases=[
                dict(
                    case=f"LB-{bundle_key}-BREACH",
                    arms=dict(
                        comparator=dict(effort=dict(effort), counts=dict(clean_counts)),
                        workflow=dict(effort=dict(effort), counts=breach_counts),
                    ),
                )
            ],
        )
        breach_report = learning_test_bundles.run_report(breach_run)
        if breach_report["stop"] is True and breach_report["breaches"]:
            stop_triggers_verified += 1
        else:
            consent_breaches += 1
            violations.append(
                dict(
                    bundle=bundle_key,
                    check=f"{bundle_key}:stop_on_{zero_measure}",
                    gate="resident",
                    rule_id=CONSENT_GATE_RULE_ID,
                    detail=f"Learning bundle failed to stop when {zero_measure}=1.",
                )
            )

    return dict(
        suite="learning_bundles",
        passed=consent_breaches == 0 and not violations,
        bundles_checked=len(bundle_checks),
        stop_triggers_verified=stop_triggers_verified,
        safety_progression_attempts=0,
        safety_progression_blocked=0,
        controlled_progressions_with_unresolved_safety=0,
        consent_work_start_attempts=len(bundle_checks),
        consent_work_start_blocked=stop_triggers_verified,
        work_started_without_agreement_or_exception=consent_breaches,
        violations=violations,
    )


def verify_exercise_safety_and_consent_gates(
    *,
    as_of: str = DEFAULT_AS_OF,
    use_sql: bool = False,
    extra_stores: Sequence[tuple[str, Store]] = (),
) -> dict[str, Any]:
    """Run deterministic #81 safety and resident consent gate verification across all suites."""
    as_of_day, as_of_utc = _normalize_as_of(as_of)
    suites = [
        _run_constructed_workbench_suite(as_of_day=as_of_day, use_sql=use_sql),
        _run_resident_preview_suite(as_of_day=as_of_day, use_sql=use_sql),
        _run_sensor_retrofit_suite(as_of_day=as_of_day, use_sql=use_sql),
        _run_scale_matrix_suite(as_of_day=as_of_day, use_sql=use_sql),
        _run_authorised_exception_suite(
            as_of_day=as_of_day,
            as_of_utc=as_of_utc,
            use_sql=use_sql,
        ),
        _run_learning_bundles_suite(),
    ]
    for custom_name, custom_store in extra_stores:
        custom_res = verify_store_safety_and_consent_invariants(
            custom_store,
            suite_name=custom_name,
            as_of=as_of_day,
        )
        suites.append({k: v for k, v in custom_res.items() if k != "attempts"})

    total_safety_attempts = sum(int(s["safety_progression_attempts"]) for s in suites)
    total_safety_blocked = sum(int(s["safety_progression_blocked"]) for s in suites)
    total_safety_breaches = sum(
        int(s["controlled_progressions_with_unresolved_safety"]) for s in suites
    )
    total_consent_attempts = sum(int(s["consent_work_start_attempts"]) for s in suites)
    total_consent_blocked = sum(int(s["consent_work_start_blocked"]) for s in suites)
    total_consent_breaches = sum(
        int(s["work_started_without_agreement_or_exception"]) for s in suites
    )
    all_violations = [v for s in suites for v in s["violations"]]

    return dict(
        as_of=as_of_day,
        backend="sqlite" if use_sql else "json",
        qualification=EXERCISE_QUALIFICATION,
        rules=dict(
            safety=SAFETY_GATE_RULE_ID,
            consent=CONSENT_GATE_RULE_ID,
            authorised_exception=AUTHORISED_EXCEPTION_RULE_ID,
        ),
        passed=(
            total_safety_breaches == 0
            and total_consent_breaches == 0
            and not all_violations
            and all(bool(s["passed"]) for s in suites)
        ),
        suites_checked=len(suites),
        suite_names=[str(s["suite"]) for s in suites],
        safety_progression_attempts=total_safety_attempts,
        safety_progression_blocked=total_safety_blocked,
        controlled_progressions_with_unresolved_safety=total_safety_breaches,
        consent_work_start_attempts=total_consent_attempts,
        consent_work_start_blocked=total_consent_blocked,
        work_started_without_agreement_or_exception=total_consent_breaches,
        suites=suites,
        violations=all_violations,
    )
