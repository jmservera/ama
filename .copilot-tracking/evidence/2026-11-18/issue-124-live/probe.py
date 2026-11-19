"""Issue 124 evidence probe: contract behaviour plus synthetic demo data coverage. No secrets, no network."""

import csv
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src/core/src"))
from zava_forward.core import discovery_contract as dc  # noqa: E402
from zava_forward.core import discovery_register as dr  # noqa: E402

DATA = ROOT / "docs/reference/research/retrofit-synthetic-data"
out: dict[str, object] = {"module_path": dc.__file__}


def attempt(fn):
    try:
        return {"ok": True, "value": str(fn())[:200]}
    except Exception as exc:  # recorded as evidence
        return {"ok": False, "error": f"{type(exc).__name__}: {str(exc)[:200]}"}


# Criterion 1: owner nomination and endpoint
unset = dc.NominatedDiscoveryOwner()
out["owner_default_status"] = unset.status()
out["agent_as_owner"] = attempt(
    lambda: dc.nominate_discovery_owner(
        nominated_by="Sponsor A", nominated_by_role="Executive sponsor",
        owner="AI agent", owner_role="Discovery owner", nominated_on=date(2026, 11, 18))
)
out["same_person"] = attempt(
    lambda: dc.nominate_discovery_owner(
        nominated_by="Sam Person", nominated_by_role="Sponsor",
        owner="sam person", owner_role="Owner", nominated_on=date(2026, 11, 18))
)
nominated = dc.nominate_discovery_owner(
    nominated_by="Placeholder Sponsor", nominated_by_role="Executive sponsor",
    owner="Placeholder Owner", owner_role="Discovery owner", nominated_on=date(2026, 11, 18))
out["nominated_status"] = nominated.status()
out["wrong_endpoint"] = attempt(
    lambda: dc.agree_discovery_endpoint(
        nominated, endpoint="installation", agreed_by="Placeholder Sponsor",
        agreed_role="Executive sponsor", agreed_on=date(2026, 11, 18))
)
agreed = dc.agree_discovery_endpoint(
    nominated, endpoint="accepted handover", agreed_by="Placeholder Sponsor",
    agreed_role="Executive sponsor", agreed_on=date(2026, 11, 18))
out["agreed_status"] = agreed.status()
out["note_owner"] = "Placeholder names exercise the rule only; they are not nominations."

# Criterion 2: dictionary
dictionary = dc.build_default_lifecycle_dictionary()
rep = dc.summarize_lifecycle_dictionary(dictionary)
out["dictionary"] = {
    "stages": rep.stage_count, "events": rep.event_count, "timestamps": rep.timestamp_spec_count,
    "wait_states": rep.wait_state_count, "return_loops": rep.return_loop_count,
    "gaps_open": len(rep.gaps), "gaps_sample": list(rep.gaps[:3]),
    "owner_validated": rep.owner_validated, "finding_status": rep.finding_status,
}
out["validate_dictionary_no_owner"] = attempt(
    lambda: dc.validate_lifecycle_report(
        rep, unset, dictionary, by="Placeholder Owner", on=date(2026, 11, 18), note="x")
)
out["validate_dictionary_agent"] = attempt(
    lambda: dc.validate_lifecycle_report(
        rep, agreed, dictionary, by="AI agent", on=date(2026, 11, 18), note="x")
)

# Synthetic data coverage against dictionary event vocabulary
events = list(csv.DictReader((DATA / "lifecycle-events.csv").open()))
types = Counter(e["event_type"] for e in events)
cands = list(csv.DictReader((DATA / "candidate-lifecycle.csv").open()))
mapping = {
    "candidate selection": ["CANDIDATE_IDENTIFIED"],
    "retrofit assessment completed": ["ASSESSMENT_COMPLETED"],
    "design approved": ["DESIGN_APPROVED"],
    "resident works decision recorded": ["RESIDENT_WORKS_DECISION"],
    "ready to install": [],
    "work release": ["WORK_ORDER_ISSUED"],
    "appointment": [],
    "installation": ["INSTALL_STARTED", "INSTALL_COMPLETE"],
    "practical completion": ["INSTALL_COMPLETE"],
    "invoice": [],
    "documentary completion": [],
    "physical acceptance": ["QA_PASSED"],
    "evidence acceptance": ["EVIDENCE_ACCEPTED"],
    "resident handover": ["RESIDENT_HANDOVER"],
    "accepted handover": ["ACCEPTED_HANDOVER"],
}
out["event_coverage"] = {
    k: {"mapped_types": v, "rows": sum(types[t] for t in v)} for k, v in mapping.items()
}
out["event_coverage_unmapped_contract_events"] = [k for k, v in mapping.items() if not v]
out["population"] = {
    "candidates": len(cands),
    "event_rows": len(events),
    "distinct_candidates_in_events": len({e["candidate_id"] for e in events}),
    "distinct_properties": len({c["property_ref"] for c in cands}),
    "event_date_iso_rows": sum(1 for e in events if e["event_date"][:4].isdigit()),
    "event_date_dmy_rows": sum(1 for e in events if e["event_date"][2:3] == "/"),
    "event_date_iso_min": min(e["event_date"] for e in events if e["event_date"][:4].isdigit()),
    "event_date_iso_max": max(e["event_date"] for e in events if e["event_date"][:4].isdigit()),
    "accepted_handover_candidates": len({e["candidate_id"] for e in events if e["event_type"] == "ACCEPTED_HANDOVER"}),
    "all_rows_synthetic": all(e["is_synthetic"] == "true" for e in events) and all(c["is_synthetic"] == "true" for c in cands),
}
loops = Counter(e["event_type"] for e in events if e["event_type"] in
                {"DESIGN_RETURNED", "CASE_REOPENED", "INSTALL_ABORTED", "DESIGN_RESCOPED", "DESIGN_VARIATION_REQUESTED"})
out["return_loop_signals"] = dict(loops)
delay = Counter(c["delay_code"] for c in cands if c["delay_code"])
out["delay_codes_on_candidates"] = dict(delay.most_common(8))
out["delay_free_text_rows"] = sum(1 for c in cands if c["delay_notes"])

# Criterion 3: register
reg = dc.build_seed_constraint_register()
out["register"] = [
    {"rank": h.rank, "code": h.code, "supporting": len(h.supporting_evidence),
     "contradicting": len(h.contradicting_evidence),
     "gaps": dc.constraint_evidence_gaps(h), "owner_validated": h.owner_validated,
     "finding_status": h.finding_status}
    for h in reg.hypotheses
]
h1 = reg.hypotheses[0]
sup = dc.EvidenceRecord(
    statement="Synthetic: delay code share", source_ref="retrofit-synthetic-data/candidate-lifecycle.csv",
    direction="supports", recorded_by="Placeholder Analyst")
con = dc.EvidenceRecord(
    statement="Synthetic: waits recorded with no capacity reason", source_ref="retrofit-synthetic-data/lifecycle-events.csv",
    direction="contradicts", recorded_by="Placeholder Analyst")
h_s = dc.record_supporting_evidence(h1, sup)
out["one_sided_gaps"] = dc.constraint_evidence_gaps(h_s)
h_b = dc.record_contradicting_evidence(h_s, con)
out["two_sided_gaps"] = dc.constraint_evidence_gaps(h_b)

# Governance: candidate-only default pack
pack = dc.build_default_phase0_pack(
    window_start=date(2025, 7, 1), window_end=date(2026, 6, 30), as_of=date(2026, 11, 18))
out["default_pack"] = {
    "owner_status": pack.discovery_owner.status(),
    "flow_owner_validated": pack.flow_report.owner_validated,
    "flow_finding_status": pack.flow_report.finding_status,
    "population": getattr(pack.flow_report, "candidate_count", None),
}
out["validate_pack_without_owner"] = attempt(
    lambda: dc.validate_discovery_pack(pack, by="Placeholder Owner", on=date(2026, 11, 18), note="x")
)
print(json.dumps(out, indent=1, default=str))
