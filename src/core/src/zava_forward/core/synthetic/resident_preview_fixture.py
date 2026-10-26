"""Build the disposable synthetic dataset and grant fixture for the resident preview.

Everything here is invented. The builder drives the existing domain store with explicit
synthetic inputs (never a generator backfill), then writes a private dataset and a separate
grant fixture into a fresh directory. It reads no environment-selected data and no real file.
"""

import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

from .. import store as _store
from .. import workflows as _workflows

Store: Any = _store.Store
_today: Any = _workflows._today

FIXTURE_ID = "SYN-RESIDENT-PREVIEW-444"
MEASURES = ("Loft insulation", "Cavity wall")
CANARY = "SYN-CANARY"
LIMITATIONS = [
    "Invented people, homes and cases only; no real resident, address, roster or staff data.",
    "Read-only: no messaging, upload, download, consent, AI or action is available.",
    "Identity is the subject this server process was started with; there is no sign-in.",
    "Loopback only. Not enrolment, not a live service, not an approved resident design.",
]


def _case(cid: str, name: str, stage: str, owner: str, town: str) -> dict[str, Any]:
    return dict(
        id=cid,
        wave="Wave 1",
        closed=False,
        stage=stage,
        stage_since="2026-01-01",
        days_in_stage=10,
        waiting_on=f"{CANARY}-WAITING-{cid}",
        reason=f"{CANARY}-REASON-{cid}",
        owner_code="RLO-01",
        owner=owner,
        owner_role="Resident Liaison Officer",
        resident=dict(
            title="Ms",
            name=name,
            formal=name,
            phone=f"{CANARY}-PHONE-{cid}",
            email="",
            preferred="Phone",
            adjustment=f"{CANARY}-VULNERABILITY-{cid}",
            priority_support=True,
            unavailable="",
            representative=None,
        ),
        home=dict(
            address=f"{cid[-1]} Synthetic Row",
            town=town,
            postcode="ZZ1 1ZZ",
            area="Synthetic",
            type="Mid terrace",
            built=1950,
            epc="D",
            tenure="Social rent",
            lat=0,
            lon=0,
        ),
        measures=list(MEASURES),
        notes=f"{CANARY}-STAFF-NOTE-{cid}",
        contractor=dict(
            name="Synthetic Build Ltd",
            phone=f"{CANARY}-CONTRACTOR-PHONE",
            scope="x",
            contact=f"{CANARY}-CONTRACTOR-{cid}",
        ),
        decision=dict(status="Waiting", by=None, at=None),
        funding_ok=False,
        funding=dict(
            route=f"{CANARY}-FUNDING-ROUTE",
            status="Not started",
            reference=f"{CANARY}-FUNDING-REF",
            draft=f"{CANARY}-FUNDING-DRAFT",
            approved_by=None,
        ),
        contacts=[dict(at="2026-01-02T10:00", channel="Phone", outcome=f"{CANARY}-CONTACT-{cid}")],
        appointments=[f"{CANARY}-LEGACY-APPOINTMENT-{cid}"],
        hazards=[
            dict(
                category="Damp",
                priority="P1",
                noticed="2026-01-01",
                referred=None,
                repaired=None,
                released=False,
                job=f"{CANARY}-SAFEGUARDING-{cid}",
                owner=f"{CANARY}-HAZARD-OWNER",
            )
        ]
        if cid == "SYN-C3"
        else [],
        safeguarding=dict(note=f"{CANARY}-SAFEGUARDING-NOTE-{cid}"),
        history=[f"{CANARY}-HISTORY-{cid}"],
        chat=[dict(text=f"{CANARY}-CHAT-{cid}")],
        memory=[dict(text=f"{CANARY}-MEMORY-{cid}")],
    )


def _dataset() -> dict[str, Any]:
    return dict(
        staff=[
            dict(
                code="RLO-01",
                name=f"{CANARY}-STAFF-SAM",
                email="sam@example.test",
                role="Resident Liaison Officer",
            ),
            dict(
                code="PM-01",
                name=f"{CANARY}-STAFF-PAM",
                email="pam@example.test",
                role="Retrofit Programme Manager",
            ),
        ],
        cases=[
            _case("SYN-C1", "Alex Synthetic", "Install booked", f"{CANARY}-OWNER-1", "Exampleton"),
            _case(
                "SYN-C2",
                "Blake Synthetic",
                "Survey being booked",
                f"{CANARY}-OWNER-2",
                "Exampleton",
            ),
            _case(
                "SYN-C3", "Casey Unrelated", "Works under way", f"{CANARY}-OWNER-3", "Otherville"
            ),
        ],
        as_of="2026-10-24",
    )


def _drive(store: Any) -> None:
    """Record scopes, answers, one confirmed appointment, one offer and representative authority."""
    pam, sam = store.staff["pam@example.test"], store.staff["sam@example.test"]
    for cid in ("SYN-C1", "SYN-C2"):
        store.technical_action(pam, cid, dict(action="design_submit", note="SYN"))
        for measure in MEASURES:
            store.resident_action(
                sam,
                cid,
                dict(
                    action="scope_record",
                    measure=measure,
                    design_version=1,
                    scope="SYN-SCOPE",
                    source="SYN",
                ),
            )
            store.resident_action(
                sam,
                cid,
                dict(
                    action="decision_record",
                    measure=measure,
                    context_revision=1,
                    status="Accepted",
                    answered_by="The resident",
                    source="SYN-SOURCE",
                    note="SYN-NOTE",
                ),
            )
    pid = store.create_package(
        pam, "SYN-444", "2026-01-01", "2099-01-01", "SYN-SCOPE", "SYN-CONTRACT", "SYN-1"
    )
    content = b"SYNTHETIC ONLY: accepted one-home-order package quota; no real instruction."
    with store.lock:
        package = store._package(pid)
        package["contract_version"] = "SYN-1"
        actor = store.staff[pam["email"]]
        actor.setdefault("contract_authorities", []).append(
            dict(
                reference="SYN-DELEGATION",
                version="1",
                contract_ref=package["contract_ref"],
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
                suppliers=["Synthetic Build Ltd"],
                scope_versions=[1, 2],
            )
        )
        ids = [
            c for c, v in store.cases.items() if v["contractor"]["name"] == "Synthetic Build Ltd"
        ]
        source = store._case(ids[0])
        doc = dict(
            id="SYN-COMMITMENT",
            name="synthetic-commitment.txt",
            kind="Other",
            version="1",
            content_sha256=hashlib.sha256(content).hexdigest(),
            at=_today(),
            scan=dict(status="clean", scanner="Synthetic fixture"),
        )
        source["documents"] = [d for d in source["documents"] if d["id"] != doc["id"]] + [doc]
        store.docstore.put(source["id"], doc["id"], content, "text/plain")
        store.save()
        details = dict(
            source_case_id=source["id"],
            document_id=doc["id"],
            source_version="1",
            source_date=_today(),
            reviewed_on=_today(),
            valid_from=package["period_from"],
            valid_to=package["period_to"],
            unit="home-work-order",
            case_ids=ids,
            status="Committed",
        )
    store.set_capacity(pam, pid, "Synthetic Build Ltd", 5, 5, "SYN-CAPACITY", details)
    bindings = [dict(measure=MEASURES[0], context_revision=1)]
    orders = {
        cid: store.issue_work_order(pam, pid, cid, resident_bindings=bindings)
        for cid in ("SYN-C1", "SYN-C2")
    }
    for cid, when, confirm in (("SYN-C1", "2098-01-01", True), ("SYN-C2", "2098-02-01", False)):
        wid = orders[cid]
        case = store.cases[cid]
        store.resident_action(
            pam,
            cid,
            dict(
                action="update_record",
                expected_version=0,
                owner=pam["email"],
                purpose="SYN appointment update",
                due_at="2099-01-01T10:00:00+00:00",
                basis="SYN manual arrangement",
                status="Outstanding",
            ),
        )
        ref = f"SYN-offer-{wid}"
        store.appointment_control(
            pam,
            wid,
            dict(
                action="offer",
                event_ref=ref,
                date=when,
                period="Morning",
                expected_offer_id=None,
                options=["Morning", "Different day", "Pause"],
                constraints="SYN morning only",
                instructions="SYN",
                paused=False,
                deferred=False,
                bundle=False,
            ),
        )
        if confirm:
            for kind, person in (
                ("resident", case["resident"]["name"]),
                ("staff", pam["name"]),
                ("capacity", "SYN supplier authorized contact"),
            ):
                store.appointment_control(
                    pam,
                    wid,
                    dict(
                        action="confirm",
                        event_ref=f"{ref}-{kind}",
                        offer_id=ref,
                        kind=kind,
                        person=person,
                        source="SYN explicit recorded agreement " + kind,
                        channel="Phone, manually recorded",
                    ),
                )
    store.resident_action(
        sam,
        "SYN-C2",
        dict(action="safe_contact_record", safe_contact_ref="SYN-SAFE-B", source="SYN"),
    )
    for ref, tasks in (
        ("SYN-REP-B", ["Receive information", "Attend"]),
        ("SYN-REP-WRONG-REF", ["Receive information"]),
    ):
        store.resident_action(
            sam,
            "SYN-C2",
            dict(
                action="representative_record",
                measure=MEASURES[0],
                context_revision=1,
                representative_ref=ref,
                status="Confirmed",
                tasks=tasks,
                source="SYN-AUTH",
                authority_date="2026-01-01",
                review_date="2099-01-01",
                resident_wishes="SYN",
                safe_contact_ref="SYN-SAFE-B",
            ),
        )


def _grant(grant_id: str, subject: str, case_id: str, **extra: Any) -> dict[str, Any]:
    kind = extra.pop("kind", "resident")
    body: dict[str, Any] = dict(
        grant_id=grant_id,
        subject=subject,
        case_id=case_id,
        kind=kind,
        fields=["home", "measures", "progress", "next_step", "appointments", "help"],
        actions=[],
        valid_from="2026-01-01T00:00:00+00:00",
        valid_to="2099-01-01T00:00:00+00:00",
        revoked=False,
    )
    body.update(extra)
    return body


def _grants() -> dict[str, Any]:
    rep = dict(
        kind="representative",
        measure=MEASURES[0],
        fields=["measures", "progress", "next_step", "appointments"],
    )
    return dict(
        fixture=dict(
            id=FIXTURE_ID,
            synthetic=True,
            disposable=True,
            lineage="Built by resident_preview_fixture from invented inputs; no real source.",
            limitations=LIMITATIONS,
        ),
        subjects=[
            dict(subject=s)
            for s in (
                "SYN-RES-A",
                "SYN-RES-B",
                "SYN-REP-B",
                "SYN-REP-WRONG",
                "SYN-RES-EXPIRED",
                "SYN-RES-REVOKED",
                "SYN-RES-AMBIG",
                "SYN-RES-NOGRANT",
            )
        ],
        grants=[
            _grant("G-A", "SYN-RES-A", "SYN-C1"),
            _grant("G-B", "SYN-RES-B", "SYN-C2"),
            _grant(
                "G-REP-B",
                "SYN-REP-B",
                "SYN-C2",
                representative_ref="SYN-REP-B",
                tasks=["Receive information", "Attend"],
                **rep,
            ),
            _grant(
                "G-REP-WRONG",
                "SYN-REP-WRONG",
                "SYN-C2",
                representative_ref="SYN-REP-WRONG-REF",
                tasks=["Receive information", "Attend"],
                **rep,
            ),
            _grant("G-EXPIRED", "SYN-RES-EXPIRED", "SYN-C1", valid_to="2026-01-02T00:00:00+00:00"),
            _grant("G-REVOKED", "SYN-RES-REVOKED", "SYN-C1", revoked=True),
            _grant("G-AMBIG-1", "SYN-RES-AMBIG", "SYN-C1"),
            _grant("G-AMBIG-2", "SYN-RES-AMBIG", "SYN-C2"),
        ],
    )


def build(out_dir: str | Path) -> tuple[Path, Path]:
    """Create a new directory holding the dataset and grant fixture. Refuses an existing one."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False, mode=0o700)
    with tempfile.TemporaryDirectory(prefix="ama444-build-") as work:
        base = Path(work) / "base.json"
        base.write_text(json.dumps(_dataset()), encoding="utf-8")
        store = Store(str(base), str(Path(work) / "live.json"), str(Path(work) / "audit.jsonl"))
        _drive(store)
        data = store.data
        shutil.copytree(Path(work) / "docs", out / "docs")
    data["synthetic_preview"] = dict(disposable=True, fixture_id=FIXTURE_ID)
    dataset, fixture = out / "dataset.json", out / "grants.json"
    dataset.write_text(json.dumps(data, indent=1), encoding="utf-8")
    fixture.write_text(json.dumps(_grants(), indent=1), encoding="utf-8")
    return dataset, fixture
