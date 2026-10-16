"""Resident decision per measure and a separate service/complaint route (FR-014, AC-017, AC-037, SA-008).

The decision is a resident-owned field. It starts as "Not recorded" for every
measure and changes only when a person records what the resident said, with how
they said it. It is never worked out from calls, visits, access or other
measures, and one measure's pause or withdrawal does not touch another's.
Service and complaint requests have their own route, desired outcome and a
named redress owner. Contact needs are held as short coded entries so only the
minimum necessary is shown.
"""
from copy import deepcopy
from datetime import date

from . import controls as k

DECISION_STATUSES = ("Waiting", "Accepted", "Declined", "Paused", "Withdrawn")
ANSWERED_BY = ("The resident", "Their representative")
ROUTES = ("Service request", "Complaint", "Independent review", "Repair", "Defect", "Hazard")
REQUEST_STATUSES = ("Open", "In progress", "Resolved")
ACCESS_CODES = ("None", "Unknown", "Large print", "Phone only", "Plain language", "Interpreter", "Representative contact", "Safe route needed")
RESIDENT_ACTIONS = ("scope_record", "safe_contact_record", "representative_record", "disclosure_check",
                    "decision_record", "service_open", "service_update", "service_close")
NOT_RECORDED = "Not recorded"
AUTHORITY_TASKS = ("Receive information", "Communicate", "Attend", "Works decision")
AUTHORITY_STATUSES = ("Confirmed", "Unclear", "Disputed", "Revoked")
RESIDENT_RETENTION_YEARS = 5
RESIDENT_RETENTION_ID = "resident-decisions"
RESIDENT_FIELDS = ("resident_scopes", "measure_decisions", "representative_authorities",
                   "resident_safe_contact", "resident_contact_history", "resident_reviews")


def first_contact(c, today=None):
    """Only actual contact evidence can establish the resident's first interaction."""
    today = date.fromisoformat(today or k.today())
    deleted = c.get("resident_retention_deleted_at")
    tombstone = c.get("resident_retention_tombstone")
    offset = tombstone["contacts_before_deletion"] if tombstone else 0
    legacy = bool(deleted and not tombstone)
    candidates = [((c.get("resident") or {}).get("first_contact_at"), legacy)]
    candidates += [(r.get("at"), legacy) for r in c.get("contacts", [])[offset:]]
    candidates += [(r.get("at"), False) for r in c.get("resident_contact_history", [])]
    days = []
    for raw, legacy_contact in candidates:
        try:
            day = date.fromisoformat(str(raw)[:10])
        except ValueError:
            continue
        if deleted and (day.isoformat() < deleted or
                        (legacy_contact and day.isoformat() == deleted)):
            continue
        if day <= today:
            days.append(day)
    return min(days) if days else None


def remember_first_contact(c):
    day = first_contact(c)
    if day:
        c["resident"]["first_contact_at"] = day.isoformat()


def retention_schedule(c, today=None):
    today = today or k.today()
    start = first_contact(c, today)
    due = None
    if start:
        try:
            due = start.replace(year=start.year + RESIDENT_RETENTION_YEARS)
        except ValueError:
            due = start.replace(year=start.year + RESIDENT_RETENTION_YEARS, day=28)
    return dict(years=RESIDENT_RETENTION_YEARS, trigger="First recorded resident contact",
                first_contact=start.isoformat() if start else None,
                due=due.isoformat() if due else None,
                expired=bool(due and due.isoformat() <= today),
                status="Known" if start else "Unknown: first recorded contact needs evidence")


def current_context(c, measure):
    versions = c.get("resident_scopes", {}).get(measure, [])
    context = versions[-1] if versions else None
    design = (c.get("technical") or {}).get("design_version")
    return context if context and context["design_version"] == design else None


def require_context(c, body):
    measure = body.get("measure")
    if not isinstance(measure, str) or measure not in case_measures(c):
        raise ValueError("Choose one of this home's measures.")
    context = current_context(c, measure)
    revision = body.get("context_revision")
    if (not context or type(revision) is not int
            or revision != context["revision"]):
        raise ValueError("Confirm the current measure scope and design before recording this step.")
    return measure, context


def authority_for(c, ref, task, measure, context, version=None):
    if retention_schedule(c)["expired"]:
        raise ValueError("Resident records are past retention. Obtain current human-reviewed evidence.")
    versions = c.get("representative_authorities", {}).get(ref, []) if isinstance(ref, str) else []
    a = versions[-1] if versions else None
    if not a or (version is not None and a["version"] != version):
        raise ValueError("Representative authority needs human confirmation through the safe contact route.")
    if (a["status"] != "Confirmed" or task not in a["tasks"]
            or a["measure"] != measure or a["context_revision"] != context["revision"]
            or a["safe_contact_ref"] != c.get("resident_safe_contact")
            or a["safe_contact_revision"] != len(c.get("resident_contact_history", []))
            or not a["authority_date"] <= k.today() < a["review_date"]):
        raise ValueError("Representative authority needs human confirmation through the safe contact route.")
    return a


def resident_gate(c, bindings=None):
    """Case advance checks all measures; scoped work checks only explicit bindings."""
    if retention_schedule(c)["expired"]:
        return ["Resident records are past retention. Owner: Resident Liaison Officer. Next action: obtain current human-reviewed evidence."]
    if bindings is None:
        bindings = [dict(measure=m, context_revision=(current_context(c, m) or {}).get("revision"))
                    for m in case_measures(c)]
    if not isinstance(bindings, list) or not bindings:
        return ["Resident scope is unknown. Owner: Resident Liaison Officer. Next action: bind the work to its measure and current scope."]
    why, seen = [], set()
    for binding in bindings:
        try:
            if not isinstance(binding, dict):
                raise ValueError("Invalid resident scope binding.")
            measure, context = require_context(c, binding)
            if measure in seen:
                raise ValueError("Choose each measure once.")
            seen.add(measure)
            versions = c.get("measure_decisions", {}).get(measure, [])
            answer = versions[-1] if versions else {}
            if answer.get("context_revision") != context["revision"] or answer.get("status") != "Accepted":
                raise ValueError("A current supplied resident acceptance is needed.")
            if c.get("resident_reviews", {}).get(measure, {}).get("status") == "Needs human review":
                raise ValueError("Human review is needed.")
            if answer.get("answered_by") == ANSWERED_BY[1]:
                authority_for(c, answer.get("representative_ref"), "Works decision", measure, context,
                              answer.get("authority_version"))
        except ValueError:
            why.append("Resident decision or authority needs confirmation. Owner: Resident Liaison Officer. "
                       "Next action: review the affected measure's current scope, supplied answer and authority.")
    return why


def resident_status(c):
    """Conservative list/prompt status; a legacy case-wide answer is not scoped evidence."""
    if not resident_gate(c):
        return "Accepted"
    measures = case_measures(c)
    if measures and all(current_context(c, m) and c.get("measure_decisions", {}).get(m)
                        and c["measure_decisions"][m][-1].get("context_revision") == current_context(c, m)["revision"]
                        and c["measure_decisions"][m][-1]["status"] == "Declined" for m in measures):
        return "Declined"
    return NOT_RECORDED


def case_measures(c):
    m = c.get("measures", [])
    parts = m if isinstance(m, list) else [p.strip() for p in str(m).replace(";", ",").split(",")]
    return [p for p in parts if p]


def measure_decision_view(c):
    """Every measure with its latest recorded answer, or 'Not recorded'. Nothing is filled in."""
    recorded = c.get("measure_decisions") or {}
    out = []
    for measure in case_measures(c):
        context = current_context(c, measure)
        versions = recorded.get(measure, [])
        answer = versions[-1] if versions else {}
        status = answer.get("status", NOT_RECORDED) if context and answer.get("context_revision") == context["revision"] else NOT_RECORDED
        out.append(dict(measure=measure, status=status, context=deepcopy(context),
                        versions=deepcopy(versions), readiness="Needs human review" if resident_gate(c, [
                            dict(measure=measure, context_revision=(context or {}).get("revision"))]) else "Resident decision current",
                        review=deepcopy(c.get("resident_reviews", {}).get(measure))))
    return out


class ResidentDecisionMixin:
    def resident_recorder(self, user, service=False):
        roles = k.RESIDENT_VIEW_ROLES if service else k.RESIDENT_ROLES
        k.require_role(user, roles, "authorised resident-workflow staff")
        actor = self.staff.get(user.get("email", "").lower())
        if not actor or any(actor.get(key) != user.get(key) for key in ("role", "name", "code")):
            raise PermissionError("Resident records require a registered named human staff identity.")
        return actor

    def delete_resident_records(self, user, case_id, today=None):
        self._manager(user, "approve resident record deletion")
        with self.lock:
            c = self._case(case_id)
            if (c.get("legal_hold") or {}).get("active"):
                raise PermissionError("A legal hold blocks deletion on this case.")
            if not retention_schedule(c, today)["expired"]:
                raise ValueError("Resident records are not past their first-contact retention period.")
            c["resident"].pop("first_contact_at", None)
            # Contacts have a separate purpose; count their retained prefix without copying content.
            c["resident_retention_tombstone"] = dict(contacts_before_deletion=len(c.get("contacts", [])))
            for key in RESIDENT_FIELDS:
                c.pop(key, None)
            c["decision"] = dict(status=NOT_RECORDED, by=None, at=None)
            c["resident"]["representative"] = None
            for request in c.get("service_requests", []):
                request.pop("representative_ref", None)
            c["resident_retention_deleted_at"] = today or k.today()
            self.audit(user["email"], "resident_retention_deleted", case_id, "resident decision payload removed")
            self.save()

    def resident_action(self, user, case_id, body):
        k.refuse_bulk(body)
        action = body.get("action")
        if action not in RESIDENT_ACTIONS:
            raise ValueError("Unknown step.")
        with self.lock:
            self.resident_recorder(user, service=action in ("service_open", "service_update", "service_close"))
            c = self._case(case_id)
            detail = getattr(self, "_res_" + action)(user, c, body)
            self.audit(user["email"], f"resident_{action}", case_id, detail)
            self.save()

    def _res_scope_record(self, user, c, body):
        measure = body.get("measure")
        if not isinstance(measure, str) or measure not in case_measures(c):
            raise ValueError("Choose one of this home's measures.")
        design = body.get("design_version")
        if type(design) is not int or design < 1 or design != (c.get("technical") or {}).get("design_version"):
            raise ValueError("Use the current recorded technical design version.")
        scope = k.text(body.get("scope"), "the measure scope reference", 100)
        source = k.text(body.get("source"), "the supplied scope source reference", 100)
        versions = c.get("resident_scopes", {}).get(measure, [])
        rec = dict(revision=len(versions) + 1, case_id=c["id"], measure=measure, scope=scope,
                   design_version=design, source=source, recorded_by=user["email"], at=k.now())
        c.setdefault("resident_scopes", {}).setdefault(measure, []).append(rec)
        return f"scope revision {rec['revision']} recorded"

    def _res_safe_contact_record(self, user, c, body):
        ref = k.text(body.get("safe_contact_ref"), "the resident-confirmed safe contact reference", 80)
        source = k.text(body.get("source"), "the supplied contact confirmation source", 100)
        c["resident_safe_contact"] = ref
        c.setdefault("resident_contact_history", []).append(
            dict(reference=ref, source=source, recorded_by=user["email"], at=k.now()))
        remember_first_contact(c)
        return f"safe contact revision {len(c['resident_contact_history'])} recorded"

    def _res_representative_record(self, user, c, body):
        measure, context = require_context(c, body)
        ref = k.text(body.get("representative_ref"), "the representative reference", 80)
        status = k.choice(body.get("status"), AUTHORITY_STATUSES, "the authority status")
        tasks = body.get("tasks")
        if not isinstance(tasks, list) or not tasks or any(t not in AUTHORITY_TASKS for t in tasks):
            raise ValueError("Choose the representative's evidenced tasks.")
        try:
            start = date.fromisoformat(body.get("authority_date", "")).isoformat()
            review = date.fromisoformat(body.get("review_date", "")).isoformat()
        except (TypeError, ValueError):
            raise ValueError("Enter the authority and review dates as YYYY-MM-DD.")
        if start > k.today() or review <= start:
            raise ValueError("Authority cannot start in the future and review must follow its source date.")
        safe = k.text(body.get("safe_contact_ref"), "the resident-confirmed safe contact reference", 80)
        if safe != c.get("resident_safe_contact"):
            raise ValueError("Confirm the resident's current safe contact route first.")
        source = k.text(body.get("source"), "the authority evidence reference", 100)
        wishes = k.text(body.get("resident_wishes"), "the resident's own stated wishes", 300)
        versions = c.get("representative_authorities", {}).get(ref, [])
        rec = dict(version=len(versions) + 1, representative_ref=ref, status=status, tasks=list(tasks),
                   case_id=c["id"], measure=measure, scope=context["scope"], design_version=context["design_version"],
                   context_revision=context["revision"], authority_date=start, review_date=review,
                   safe_contact_ref=safe, safe_contact_revision=len(c.get("resident_contact_history", [])),
                   source=source, resident_wishes=wishes,
                   recorded_by=user["email"], at=k.now())
        c.setdefault("representative_authorities", {}).setdefault(ref, []).append(rec)
        return f"representative authority version {rec['version']} recorded"

    def _res_disclosure_check(self, user, c, body):
        measure, context = require_context(c, body)
        task = k.choice(body.get("task"), AUTHORITY_TASKS, "the representative task")
        authority_for(c, body.get("representative_ref"), task, measure, context)
        return "representative task checked; nothing sent"

    def _res_decision_record(self, user, c, body):
        measure, context = require_context(c, body)
        status = k.choice(body.get("status"), DECISION_STATUSES, "what the resident said")
        by = k.choice(body.get("answered_by"), ANSWERED_BY, "who gave the answer")
        note = k.text(body.get("note"), "what they said, in their words" if status in ("Paused", "Withdrawn", "Declined") else "", 300,
                      required=status in ("Paused", "Withdrawn", "Declined"))
        rep = k.text(body.get("representative_ref"), "the reference for their representative", 80, required=by == ANSWERED_BY[1])
        authority = authority_for(c, rep, "Works decision", measure, context) if by == ANSWERED_BY[1] else None
        source = k.text(body.get("source"), "the supplied resident answer source reference", 100)
        review = c.get("resident_reviews", {}).get(measure)
        review_ref = k.text(body.get("review_ref"), "the human review evidence reference", 100,
                            required=status == "Accepted" and bool(review and review["status"] == "Needs human review"))
        versions = c.setdefault("measure_decisions", {}).setdefault(measure, [])
        versions.append(dict(version=len(versions) + 1, case_id=c["id"], measure=measure,
                             scope=context["scope"], design_version=context["design_version"],
                             context_revision=context["revision"], source=source,
                             authority_version=authority["version"] if authority else None,
                             status=status, answered_by=by, representative_ref=rep if authority else "", note=note,
                             recorded_by_email=user["email"], review_ref=review_ref,
                             next_update=k.text(body.get("next_update"), "", 10, False), recorded_by=user["name"], at=k.now()))
        if status in ("Paused", "Withdrawn", "Declined"):
            c.setdefault("resident_reviews", {})[measure] = dict(status="Needs human review", decision_version=len(versions),
                                                                context_revision=context["revision"], owner=c["owner"],
                                                                recorded_by=user["email"], at=k.now())
        elif status == "Accepted" and review:
            review.update(status="Reviewed with supplied acceptance", review_ref=review_ref,
                          reviewed_by=user["email"], at=k.now())
        return f"scope revision {context['revision']}: {status} decision v{len(versions)}"

    def _res_service_open(self, user, c, body):
        route = k.choice(body.get("route"), ROUTES, "the route")
        owners = []
        for key, label in (("service_owner", "who deals with it"), ("redress_owner", "who owns the redress")):
            s = self.staff.get((body.get(key) or "").lower())
            if not s or s["role"] == "Contractor":
                raise ValueError(f"Choose {label} from the staff list.")
            owners.append(s)
        if route in ("Complaint", "Independent review") and owners[0]["email"].lower() == owners[1]["email"].lower():
            raise ValueError("A complaint or independent review needs a different redress owner.")
        subject = None
        if route == "Independent review":
            review_measure = body.get("review_measure")
            if not isinstance(review_measure, str) or review_measure not in case_measures(c):
                raise ValueError("Choose the recorded measure decision to review.")
            decisions = c.get("measure_decisions", {}).get(review_measure, [])
            version = body.get("review_decision_version")
            if type(version) is not int or not 1 <= version <= len(decisions):
                raise ValueError("Choose the recorded measure decision version to review.")
            subject = decisions[version - 1].get("recorded_by_email")
            if not subject or subject.lower() == owners[1]["email"].lower():
                raise ValueError("Choose a reviewer who did not make the contested decision.")
        review_reference = k.text(body.get("review_reference"), "the contested decision reference", 100,
                                  required=route == "Independent review")
        codes = body.get("accessibility") or ["Unknown"]
        if not isinstance(codes, list) or not codes or any(x not in ACCESS_CODES for x in codes):
            raise ValueError("Choose contact needs from the list.")
        reqs = c.get("service_requests", [])
        req = dict(id=k.next_id(reqs, "SR"), route=route, summary=k.text(body.get("summary"), "a short summary", 200),
                   desired_outcome=k.text(body.get("desired_outcome"), "the outcome the resident wants", 300),
                   service_owner=owners[0]["name"], service_owner_email=owners[0]["email"], redress_owner=owners[1]["name"],
                   redress_owner_email=owners[1]["email"], accessibility=codes, representative_ref=k.text(body.get("representative_ref"), "", 80, False) or "Unknown",
                   status="Open", next_update=k.text(body.get("next_update"), "the date of the next update", 10), opened_by=user["name"], opened_at=k.now(),
                   reviewed_actor=subject, review_reference=review_reference,
                   review_measure=body.get("review_measure") if route == "Independent review" else None,
                   review_decision_version=body.get("review_decision_version") if route == "Independent review" else None,
                   history=[])
        c.setdefault("service_requests", []).append(req)
        return f"{req['id']} {route} opened"

    def _res_service_update(self, user, c, body):
        req = k.find(c.get("service_requests", []), body.get("id"), "request")
        if req["status"] == "Closed":
            raise ValueError("This request is closed.")
        if req["route"] == "Independent review" and user["email"].lower() != req["redress_owner_email"].lower():
            raise PermissionError("Only the named independent reviewer can update this review.")
        status = k.choice(body.get("status"), REQUEST_STATUSES, "the status")
        next_update = k.text(body.get("next_update"), "the date of the next update", 10)
        req.update(status=status, next_update=next_update)
        req["history"].append(dict(status=req["status"], by=user["name"], at=k.now(), note=k.text(body.get("note"), "a note", 300, False)))
        return f"{req['id']} {req['status']}"

    def _res_service_close(self, user, c, body):
        req = k.find(c.get("service_requests", []), body.get("id"), "request")
        if req["status"] != "Resolved":
            raise ValueError("Mark it resolved before closing it.")
        if req["route"] in ("Complaint", "Independent review"):
            if user["email"].lower() != req["redress_owner_email"].lower():
                raise PermissionError("Only the redress owner can close a complaint.")
            k.different_person(user, req["service_owner_email"], "close a complaint")
        elif user["email"].lower() not in (req["service_owner_email"].lower(), req["redress_owner_email"].lower()):
            raise PermissionError("Only the person dealing with it or the redress owner can close this.")
        req.update(status="Closed", closed_by=user["name"], closed_at=k.now(), outcome=k.text(body.get("note"), "the outcome for the resident", 300))
        return f"{req['id']} closed"
