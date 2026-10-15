"""Deterministic synthetic queue fixtures; never approval, certification or payment."""
from collections import Counter
from datetime import date, timedelta

from zavaforward_mvp import insights, quality
import zf_names as names

NOTE = "Synthetic exercise fixture; evidence unverified, not an operational approval."


def enrich(data, as_of, source_orders):
    people = {p["code"]: p for p in data["staff"]}
    pm, geo = people["PM-01"], people["GEO-01"]
    stamp = as_of.isoformat() + "T09:00"
    cases = sorted(data["cases"], key=lambda c: c["id"])
    open_cases = [c for c in cases if not c["closed"]]
    candidates = [c for c in open_cases if not insights.has_hazard(c)
                  and not c["resident"]["unavailable"]
                  and not any(a["outcome"] == "Booked" for a in c["appointments"])]
    if len(candidates) < 9:
        raise ValueError("Synthetic coverage needs nine available open cases without safety holds or existing bookings.")
    for c, offset in zip(candidates[:6], (0, 1, 2, 3, 6, 7)):
        day = as_of + timedelta(days=offset)
        c["appointments"].append(dict(type="Assessment", date=day.isoformat(), slot="AM",
                                      outcome="Booked", note=NOTE, who=names.contractor("SUP-RA")["name"],
                                      person=names.operative(data["seed"], "SUP-RA", c["id"]),
                                      is_synthetic=True, fixture="forward-visit"))
    for c, outcome in zip(candidates[6:9], ("Attended", "No access", "Cancelled")):
        c["appointments"].append(dict(type="Assessment", date=(as_of - timedelta(days=2)).isoformat(),
                                      slot="PM", outcome=outcome, note=NOTE,
                                      who=names.contractor("SUP-RA")["name"],
                                      person=names.operative(data["seed"], "SUP-RA", c["id"]),
                                      is_synthetic=True, fixture="historical-visit"))

    scope = "Synthetic source-issued retrofit orders; current release evidence must be independently checked."
    package = dict(id="PKG-SYN-001", name="Synthetic year-one delivery",
                   period_from=min((d for d, _, _, _ in source_orders), default=as_of.isoformat()),
                   period_to=(as_of + timedelta(days=30)).isoformat(), contract_ref="SYNTHETIC-SOURCE-ONLY",
                   scope=scope, scope_version=1, scope_history=[dict(version=1, scope=scope, by=pm["name"],
                   at=stamp, reason=NOTE)], capacity={}, created_by=pm["name"], created_at=stamp, is_synthetic=True)
    by_id = {c["id"]: c for c in cases}
    orders = []
    for i, (day, cid, supplier, completed) in enumerate(source_orders):
        if cid not in by_id:
            raise ValueError("Source work order refers to an unknown case.")
        contractor = names.contractor(supplier)["name"]
        orders.append(dict(id=f"WO-SYN-{i + 1:04d}", package=package["id"], case_id=cid,
                           contractor=contractor, state="Completed" if completed else "Issued", is_synthetic=True,
                           versions=[dict(version=1, scope=scope, scope_version=1, issued_by=pm["name"],
                                          issued_at=day, reason="Imported WORK_ORDER_ISSUED simulation fact; not live authorization.")],
                           appointments=[], corrections=[], history=[dict(at=day, by="Synthetic source export",
                           from_state=None, to_state="Issued", note="Source simulation issuance; acceptance not inferred.")]))
        if completed:
            orders[-1]["history"].append(dict(at=completed, by="Synthetic source export", from_state="Issued",
                to_state="Completed", note="Source physical installation completion; not independent quality acceptance."))
    for contractor, used in sorted(Counter(w["contractor"] for w in orders).items()):
        package["capacity"][contractor] = dict(offered=used + 5, committed=used,
            evidence="SYNTHETIC simulation issued-order allocation; not a verified contract.",
            by=pm["name"], at=stamp, history=[], is_synthetic=True)
    data["procurement"] = dict(packages=[package], work_orders=orders)

    for i, c in enumerate(open_cases[:12]):
        measure = c["measures"][0] if isinstance(c["measures"], list) and c["measures"] else (
            c["measures"].split(",")[0].strip() if isinstance(c["measures"], str) else "")
        c["finance"] = dict(budget=dict(amount=10000 + i * 100, status="Proposed", proposed_by=geo["email"],
            proposed_name=geo["name"], at=stamp, note=NOTE, approved_by=None), commitments=[], invoices=[])
        invoice = dict(id="INV-SYN-001", kind="Invoice", supplier=c["contractor"]["name"],
            work_order=next((w["id"] for w in orders if w["case_id"] == c["id"]), "UNKNOWN-SOURCE-ORDER"),
            ref=f"SYNTHETIC-{c['id']}", lines=[dict(measure=measure or "Unknown measure", quantity=1,
            amount=500, milestone_ref="")], status="Received", exceptions=[], commitment=None,
            hold=None, disposition=None, disposition_by=None, payment_status="Not payable yet",
            payment_note=NOTE, received_by=geo["email"], received_name=geo["name"], received_at=stamp,
            is_synthetic=True)
        if i % 2:
            invoice.update(status="Exceptions", exceptions=[
                dict(line=None, code="no_budget", message="No approved budget; synthetic evidence remains unknown."),
                dict(line=0, code="no_milestone", message="Accepted milestone evidence is missing.")],
                hold=dict(reason=NOTE, by=geo["name"], at=stamp))
        c["finance"]["invoices"].append(invoice)
        c["grants"] = [dict(id="GR-SYN-001", scheme="Zava Forward Exercise Fund", state="Not recorded",
            pending=dict(to="Opportunity", source=NOTE, amount=None, by=geo["email"], name=geo["name"], at=stamp),
            history=[], is_synthetic=True)]
        if measure:
            checklist = quality.checklist_for(measure)
            c["quality"] = [dict(measure=measure, state="Submitted", checklist=checklist["name"],
                checklist_version=checklist["version"], items=[dict(label=label, evidence="Missing/unverified synthetic evidence")
                for label in checklist["items"]], submitted_by=c["contractor"]["name"], source="Provider submission",
                recorded_by=geo["name"], recorded_by_code=geo["code"], recorded_at=stamp, history=[],
                defect=None, defects=[], handover=None, aftercare=[], is_synthetic=True)]
        recipient = people["RC-01"] if c["owner_code"] != "RC-01" else people["RC-02"]
        if i < 4:
            c["handoff"] = dict(state="Offered", from_code=c["owner_code"], from_name=c["owner"],
                to_code=recipient["code"], to_name=recipient["name"], offered_by=pm["name"], offered_at=stamp,
                note=NOTE, answered_at=None, answer_note="", is_synthetic=True)
            c["handoff_log"] = []
        liaison = people["RLO-01"]
        c["service_requests"] = [dict(id="SR-SYN-001", route="Complaint" if i % 2 else "Service request",
            summary="Synthetic request for a clear next-visit update", desired_outcome="Confirm the next update without booking works",
            service_owner=liaison["name"], service_owner_email=liaison["email"], redress_owner=pm["name"],
            redress_owner_email=pm["email"], accessibility=["Unknown"], representative_ref="Unknown",
            status="Open", next_update=(as_of + timedelta(days=i % 3 - 1)).isoformat(),
            opened_by=liaison["name"], opened_at=stamp, history=[], is_synthetic=True)]


    for j, c in enumerate(open_cases[12:14]):
        measure = c["measures"][0] if isinstance(c["measures"], list) and c["measures"] else ""
        c["finance"] = dict(budget=dict(amount=12000 + j * 100, status="Proposed", proposed_by=geo["email"],
            proposed_name=geo["name"], at=stamp, note=NOTE, approved_by=None), commitments=[], invoices=[])
        if j == 0:
            c["finance"]["commitments"].append(dict(id="COM-SYN-001", supplier=c["contractor"]["name"],
                contract="SYNTHETIC-SOURCE-ONLY", measure=measure or "Unknown measure", amount=5000, quantity=1,
                work_order=next((w["id"] for w in orders if w["case_id"] == c["id"]), "UNKNOWN-SOURCE-ORDER"),
                status="Raised", raised_by=geo["email"], raised_name=geo["name"], at=stamp, approved_by=None,
                is_synthetic=True))
        else:
            c["finance"]["invoices"].append(dict(id="INV-SYN-002", kind="Valuation", supplier=c["contractor"]["name"],
                work_order=next((w["id"] for w in orders if w["case_id"] == c["id"]), "UNKNOWN-SOURCE-ORDER"),
                ref=f"SYNTHETIC-{c['id']}", lines=[dict(measure=measure or "Unknown measure", quantity=1, amount=500,
                milestone_ref="")], status="Received", exceptions=[], commitment=None, hold=None, disposition=None,
                disposition_by=None, payment_status="Not payable yet", payment_note=NOTE, received_by=geo["email"],
                received_name=geo["name"], received_at=stamp, is_synthetic=True))


# Lifecycle states that would record a person's or a funder's outcome are deferred, never invented.
DEFERRED = {
    "work order": ("Appointed", "Withdrawn"),
    "budget": ("Approved",),
    "commitment": ("Approved",),
    "invoice": ("Matched", "Accepted for payment", "Rejected and returned"),
    "payment": ("Awaiting payment run", "Paid outside this system"),
    "grant": ("Opportunity", "Award", "Claimable", "Submitted", "Accepted", "Rejected", "Cash received"),
    "quality": ("Accepted", "Returned", "Fixed, awaiting reinspection", "Handed over"),
    "resident decision": ("Waiting", "Accepted", "Declined", "Paused", "Withdrawn"),
}


def lifecycle(data):
    cases = data["cases"]
    invoices = [i for c in cases for i in c.get("finance", {}).get("invoices", [])]
    commitments = [x for c in cases for x in c.get("finance", {}).get("commitments", [])]
    budgets = [c["finance"]["budget"] for c in cases if c.get("finance", {}).get("budget")]
    orders = data["procurement"]["work_orders"]
    seeded = {
        "work order": Counter(w["state"] for w in orders),
        "budget": Counter(b["status"] for b in budgets),
        "commitment": Counter(x["status"] for x in commitments),
        "invoice": Counter(f"{i['kind']}: {i['status']}" for i in invoices),
        "payment": Counter(i["payment_status"] for i in invoices),
        "grant": Counter(g["state"] for c in cases for g in c.get("grants", [])),
        "quality": Counter(q["state"] for c in cases for q in c.get("quality", [])),
        "resident decision": Counter(v[-1]["status"] for c in cases for v in c.get("measure_decisions", {}).values() if v),
        "safety hold": Counter("Open" if not h["released"] else "Released" for c in cases for h in c["hazards"]),
    }
    return dict(seeded={k: dict(v) for k, v in seeded.items()}, deferred={k: list(v) for k, v in DEFERRED.items()})


def receipt(data):
    as_of = date.fromisoformat(data["as_of"])
    week = as_of - timedelta(days=as_of.weekday())
    visits = insights.visits(data["cases"])
    appointments = [a for c in data["cases"] for a in c["appointments"]]
    return dict(is_synthetic=True, seed=data["seed"], as_of=data["as_of"], generator_version=data["generator_version"],
        generator_revision=data["generator_revision"],
        stock_register_rows=data["stock_register_rows"], programme_cases=len(data["cases"]),
        distinct_stock_anchors=len({c["synthetic_stock_anchor_id"] for c in data["cases"]}),
        open_cases=sum(not c["closed"] for c in data["cases"]),
        appointments=len(appointments), outcomes=dict(Counter(a["outcome"] for a in appointments)),
        visible_booked_visits=len(visits),
        current_week_visits=sum(week.isoformat() <= v["date"] <= (week + timedelta(days=6)).isoformat() for v in visits),
        designated_forward_visits=sum(a.get("fixture") == "forward-visit" for a in appointments),
        packages=len(data["procurement"]["packages"]), work_orders=len(data["procurement"]["work_orders"]),
        invoices=sum(len(c.get("finance", {}).get("invoices", [])) for c in data["cases"]),
        quality_records=sum(len(c.get("quality", [])) for c in data["cases"]),
        pending_grants=sum(len(c.get("grants", [])) for c in data["cases"]),
        offered_handoffs=sum(c.get("handoff", {}).get("state") == "Offered" for c in data["cases"]),
        service_requests=sum(len(c.get("service_requests", [])) for c in data["cases"]),
        lifecycle=lifecycle(data))
