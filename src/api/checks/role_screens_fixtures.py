"""One explicitly constructed home reused across independent screen checks."""

from __future__ import annotations

import copy
import runpy
from typing import Any

from checks.design_system_browser_check import ROOT
from checks.workbench_browser_check import synthetic_data as workbench_data


def synthetic_data() -> dict[str, Any]:
    data = workbench_data()
    c = data["cases"][0]
    supplied = runpy.run_path(str(ROOT / "src/core/tests/dataset.py"))
    supplied["supplied_resident_fixture"](c)
    owner = data["staff"][0]
    c["measure_decisions"]["Loft insulation"][0].update(
        status="Paused", note="SYN resident requested time", source="SYN-CHOICE-232"
    )
    c["resident_update"] = dict(
        purpose="SYN-REQUEST-232 accessible update", owner_identity=owner,
        due_at="2026-10-28T10:00:00Z", basis="SYN supplied date, not SLA",
        safe_contact_ref="SYN-SAFE-232", status="Outstanding", version=1,
        at="2026-10-27T10:00:00Z", opened_at="2026-10-27T10:00:00Z"
    )
    c["service_requests"] = [dict(
        id="SYN-REQUEST-232", route="Service request", summary="SYN large-print explanation",
        desired_outcome="Accessible explanation before a decision", status="Open",
        service_owner=owner["name"], redress_owner=owner["name"],
        accessibility=["Large print"], next_update="2026-10-28",
        status_owner=owner, version=1, opened_at="2026-10-27T09:00:00Z",
        status_at="2026-10-27T09:00:00Z", history=[]
    )]
    c["hazards"] = [copy.deepcopy(data["cases"][1]["hazards"][0])]
    c["hazards"][0].update(
        source="SYN-REPORT-227", aware_at="2026-10-27T08:00:00Z",
        sent_at="2026-10-27T08:05:00Z", sent_evidence="SYN-SENT-227",
        received_at=None, accepted_at=None, destination=data["staff"][3],
        sender=owner, referred="SYN-REFERRAL-227", referral_version=1, response_due_at=None
    )
    c["returns"] = [dict(
        at="2026-10-27T09:00:00Z", from_stage="Design in progress",
        to_stage="Survey write-up", by="SYN sender", reason="SYN missing roof reference",
        source="SYN-RETURN-230", receiving_owner=owner, next_action="Obtain roof reference"
    )]
    c["finance"] = dict(
        budget=dict(amount=8750, status="Proposed"),
        commitments=[dict(id="SYN-COM-225", supplier="Test Ltd", work_order="SYN-WO-225",
                          measure="Loft insulation", amount=1700, quantity=1, status="Raised")],
        invoices=[dict(id="SYN-INV-225", ref="SYN-REF-225", supplier="Test Ltd",
                       work_order="SYN-WO-225", status="Not checked",
                       payment_status="Not payable yet", disposition=None, hold=None,
                       lines=[dict(measure="Loft insulation", quantity=2, amount=1950,
                                   milestone_ref="")],
                       exceptions=[dict(line=0, message="SYN quantity requires review")])]
    )
    c["stock_reconciliation"] = [dict(
        id="SQ-1", field="epc", version=1, query_owner=owner,
        left=dict(value="D", source_id="SYN-STOCK-A", date="2026-09-10", version="1",
                  validation_state="Unverified"),
        right=dict(value="C", source_id="SYN-STOCK-B", date="2026-10-10", version="2",
                   validation_state="Unverified"),
        authority="Unknown", resolution="Unknown", eligibility="Unknown"
    )]
    c["stock_reconciliation_events"] = []
    c["technical"]["signoffs"]["design"] = dict(
        status="Needs reassessment", version=0, reason="SYN-MISSING-DESIGN-231"
    )
    c["documents"].append(dict(
        id="SYN-MISSING-DESIGN-231", kind="Survey", name="SYN survey",
        version=2, at="2026-10-27", scan=dict(status="clean")
    ))
    c["quality"] = [dict(
        measure="Loft insulation", state="Returned", evidence_version=1,
        checklist_version="SYN-QA-231-v1", source="Provider submission",
        submitted_by="SYN Provider", items=[dict(label="SYN depth", evidence="SYN-PHOTO-231")],
        defect=dict(description="SYN missing edge photo", reason="SYN incomplete evidence",
                    owner="SYN Contractor"), defects=[], handover=None, aftercare=[]
    )]
    return data
