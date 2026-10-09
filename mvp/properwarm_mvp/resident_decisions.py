"""Resident decision per measure and a separate service/complaint route (FR-014, AC-017, AC-037, SA-008).

The decision is a resident-owned field. It starts as "Not recorded" for every
measure and changes only when a person records what the resident said, with how
they said it. It is never worked out from calls, visits, access or other
measures, and one measure's pause or withdrawal does not touch another's.
Service and complaint requests have their own route, desired outcome and a
named redress owner. Contact needs are held as short coded entries so only the
minimum necessary is shown.
"""
from . import controls as k

DECISION_STATUSES = ("Waiting", "Accepted", "Declined", "Paused", "Withdrawn")
ANSWERED_BY = ("The resident", "Their representative")
ROUTES = ("Service request", "Complaint", "Repair", "Defect", "Hazard")
REQUEST_STATUSES = ("Open", "In progress", "Resolved")
ACCESS_CODES = ("None", "Unknown", "Large print", "Phone only", "Plain language", "Interpreter", "Representative contact", "Safe route needed")
RESIDENT_ACTIONS = ("decision_record", "service_open", "service_update", "service_close")
NOT_RECORDED = "Not recorded"


def case_measures(c):
    m = c["measures"]
    parts = m if isinstance(m, list) else [p.strip() for p in str(m).replace(";", ",").split(",")]
    return [p for p in parts if p]


def measure_decision_view(c):
    """Every measure with its latest recorded answer, or 'Not recorded'. Nothing is filled in."""
    recorded = c.get("measure_decisions") or {}
    return [dict(measure=m, status=(recorded[m][-1]["status"] if recorded.get(m) else NOT_RECORDED), versions=recorded.get(m, []))
            for m in case_measures(c)]


class ResidentDecisionMixin:
    def resident_action(self, user, case_id, body):
        k.refuse_bulk(body)
        action = body.get("action")
        if action not in RESIDENT_ACTIONS:
            raise ValueError("Unknown step.")
        k.require_role(user, k.RESIDENT_ROLES, "the Resident Liaison Officer, coordinator or a manager")
        with self.lock:
            c = self._case(case_id)
            detail = getattr(self, "_res_" + action)(user, c, body)
            self.audit(user["email"], f"resident_{action}", case_id, detail)
            self.save()

    def _res_decision_record(self, user, c, body):
        measure = body.get("measure")
        if measure not in case_measures(c):
            raise ValueError("Choose one of this home's measures.")
        status = k.choice(body.get("status"), DECISION_STATUSES, "what the resident said")
        by = k.choice(body.get("answered_by"), ANSWERED_BY, "who gave the answer")
        note = k.text(body.get("note"), "what they said, in their words" if status in ("Paused", "Withdrawn", "Declined") else "", 300,
                      required=status in ("Paused", "Withdrawn", "Declined"))
        rep = k.text(body.get("representative_ref"), "the reference for their representative", 80, required=by == ANSWERED_BY[1])
        versions = c.setdefault("measure_decisions", {}).setdefault(measure, [])
        versions.append(dict(version=len(versions) + 1, status=status, answered_by=by, representative_ref=rep, note=note,
                             next_update=k.text(body.get("next_update"), "", 10, False), recorded_by=user["name"], at=k.now()))
        return f"{measure}: {status} v{len(versions)} (told to staff by {by.lower()})"

    def _res_service_open(self, user, c, body):
        route = k.choice(body.get("route"), ROUTES, "the route")
        owners = []
        for key, label in (("service_owner", "who deals with it"), ("redress_owner", "who owns the redress")):
            s = self.staff.get((body.get(key) or "").lower())
            if not s or s["role"] == "Contractor":
                raise ValueError(f"Choose {label} from the staff list.")
            owners.append(s)
        if route == "Complaint" and owners[0]["email"].lower() == owners[1]["email"].lower():
            raise ValueError("A complaint needs a redress owner who is not the person dealing with it.")
        codes = body.get("accessibility") or ["Unknown"]
        if not isinstance(codes, list) or not codes or any(x not in ACCESS_CODES for x in codes):
            raise ValueError("Choose contact needs from the list.")
        reqs = c.setdefault("service_requests", [])
        req = dict(id=k.next_id(reqs, "SR"), route=route, summary=k.text(body.get("summary"), "a short summary", 200),
                   desired_outcome=k.text(body.get("desired_outcome"), "the outcome the resident wants", 300),
                   service_owner=owners[0]["name"], service_owner_email=owners[0]["email"], redress_owner=owners[1]["name"],
                   redress_owner_email=owners[1]["email"], accessibility=codes, representative_ref=k.text(body.get("representative_ref"), "", 80, False) or "Unknown",
                   status="Open", next_update=k.text(body.get("next_update"), "the date of the next update", 10), opened_by=user["name"], opened_at=k.now(),
                   history=[])
        reqs.append(req)
        return f"{req['id']} {route} opened"

    def _res_service_update(self, user, c, body):
        req = k.find(c.get("service_requests", []), body.get("id"), "request")
        if req["status"] == "Closed":
            raise ValueError("This request is closed.")
        req["status"] = k.choice(body.get("status"), REQUEST_STATUSES, "the status")
        req["next_update"] = k.text(body.get("next_update"), "the date of the next update", 10)
        req["history"].append(dict(status=req["status"], by=user["name"], at=k.now(), note=k.text(body.get("note"), "a note", 300, False)))
        return f"{req['id']} {req['status']}"

    def _res_service_close(self, user, c, body):
        req = k.find(c.get("service_requests", []), body.get("id"), "request")
        if req["status"] != "Resolved":
            raise ValueError("Mark it resolved before closing it.")
        if req["route"] == "Complaint":
            if user["email"].lower() != req["redress_owner_email"].lower():
                raise PermissionError("Only the redress owner can close a complaint.")
            k.different_person(user, req["service_owner_email"], "close a complaint")
        elif user["email"].lower() not in (req["service_owner_email"].lower(), req["redress_owner_email"].lower()):
            raise PermissionError("Only the person dealing with it or the redress owner can close this.")
        req.update(status="Closed", closed_by=user["name"], closed_at=k.now(), outcome=k.text(body.get("note"), "the outcome for the resident", 300))
        return f"{req['id']} closed"
