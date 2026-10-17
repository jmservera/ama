"""Assessment and technical stage: separate competent sign-offs, design version and re-approval (FR-013, AC-016).

Each sign-off belongs to a role the data defines and is given by a named
person. A changed design version marks only the affected downstream sign-offs
"Needs reassessment" so a person looks again; it never re-signs or clears
anything for them. The role mapping is a proposal for the programme to confirm.
"""
from . import controls as k, stock

SIGNOFFS = {
    "assessment": dict(label="Retrofit assessment", roles=("Quality Inspector",), design_dependent=False),
    "design": dict(label="Design", roles=("Retrofit Coordinator",), design_dependent=True),
    "building": dict(label="Building and safety dependency", roles=("Building Safety Liaison",), design_dependent=True),
    "coordination": dict(label="Coordination", roles=("Retrofit Programme Manager", "Programme Support Officer"), design_dependent=True),
}
DESIGN_ROLES = ("Retrofit Coordinator", "Retrofit Programme Manager", "Programme Support Officer")
TECH_ACTIONS = ("design_submit", "design_change", "signoff_give", "signoff_return")
EVIDENCE_OWNER = "Grants and Evidence Officer"


def _missing_evidence(c):
    from .store import Store
    return [x["kind"] for x in Store.checklist(c) if not x["present"]]


def missing_items(c):
    """What stops the technical stage passing, each item assigned to a competent role."""
    t = c.get("technical")
    queries = [dict(item=reason, assigned_to="Stock query owner") for reason in stock.blockers(c)]
    if not t:
        return queries
    out = queries
    for key, spec in SIGNOFFS.items():
        s = t["signoffs"].get(key)
        if not s or s["status"] != "Signed off":
            state = s["status"] if s else "Not given"
            out.append(dict(item=f"{spec['label']} sign-off ({state.lower()})", assigned_to=spec["roles"][0]))
    out += [dict(item=f"Evidence: {kind}", assigned_to=EVIDENCE_OWNER) for kind in _missing_evidence(c)]
    return out


def technical_gate(c):
    return [f"Technical stage: {m['item']}. Owner: {m['assigned_to']}. Next action: complete it and record it." for m in missing_items(c)]


class SignoffMixin:
    def technical_action(self, user, case_id, body):
        k.refuse_bulk(body)
        action = body.get("action")
        if action not in TECH_ACTIONS:
            raise ValueError("Unknown step.")
        if "note" in body and not isinstance(body["note"], str):
            raise ValueError("Enter the technical note as text.")
        with stock.decision_scope(self, user, case_id) as (c, actor):
            detail = getattr(self, "_tech_" + action)(actor, c, body)
            self.audit(actor["email"], f"technical_{action}", case_id, detail)
            self.save()

    @staticmethod
    def _sign_type(body):
        key = body.get("type")
        if key not in SIGNOFFS:
            raise ValueError("Choose which sign-off this is.")
        return key

    def _tech_design_submit(self, user, c, body):
        k.require_role(user, DESIGN_ROLES, "the coordinator or a manager")
        if c.get("technical"):
            raise ValueError("A design is already recorded. Record a change instead.")
        c["technical"] = dict(design_version=1, design_by=user["email"], design_name=user["name"], design_at=k.now(),
                              versions=[dict(version=1, by=user["name"], by_email=user["email"], role=user["role"], at=k.now(), note=k.text(body.get("note"), "what the design covers", 300))],
                              signoffs={})
        return "design version 1 recorded"

    def _tech_design_change(self, user, c, body):
        k.require_role(user, DESIGN_ROLES, "the coordinator or a manager")
        t = c.get("technical")
        if not t:
            raise ValueError("Record the design first.")
        note = k.text(body.get("note"), "what changed in the design", 300)
        down = [key for key, spec in SIGNOFFS.items() if spec["design_dependent"]]
        affects = body.get("affects", down)
        if not isinstance(affects, list) or not affects or any(a not in down for a in affects) or len(affects) != len(set(affects)):
            raise ValueError("Only design, building and coordination sign-offs can be affected by a design change.")
        t["design_version"] += 1
        t.update(design_by=user["email"], design_name=user["name"], design_at=k.now())
        t["versions"].append(dict(version=t["design_version"], by=user["name"], by_email=user["email"], role=user["role"], at=k.now(), note=note, affects=list(affects)))
        for key in affects:
            s = t["signoffs"].get(key)
            if s and s["status"] == "Signed off":
                s.update(status="Needs reassessment", reason=f"Design changed to version {t['design_version']}: {note}")
                s["history"].append(dict(status="Needs reassessment", by=user["name"], by_email=user["email"], role=user["role"], at=k.now(), note=note, version=t["design_version"]))
        return f"design version {t['design_version']} affects {','.join(affects)}"

    def _tech_signoff_give(self, user, c, body):
        self.require_safety_clear(c)
        self.require_stock_clear(c)
        t = c.get("technical")
        if not t:
            raise ValueError("Record the design first.")
        key = self._sign_type(body)
        spec = SIGNOFFS[key]
        k.require_role(user, spec["roles"], f"the {spec['roles'][0]}" + (" or a manager" if len(spec["roles"]) > 1 else ""))
        if key in ("building", "coordination"):
            self.require_building_clear(c)
        k.different_person(user, t["design_by"], "give this sign-off")
        for other, s in t["signoffs"].items():
            if other != key and s["status"] == "Signed off" and (s.get("by_email") or "").lower() == user["email"].lower():
                raise PermissionError("Each sign-off needs a different person.")
        if key == "coordination":
            why = [f"{v['label']} sign-off is not in place. Owner: {v['roles'][0]}. Next action: give the sign-off." for o, v in SIGNOFFS.items() if o != key
                   and (t["signoffs"].get(o) or {}).get("status") != "Signed off"]
            why += [f"Evidence is missing: {kind}. Owner: {EVIDENCE_OWNER}. Next action: add it to the case." for kind in _missing_evidence(c)]
            if why:
                from .store import GateError
                raise GateError(why)
        note = k.text(body.get("note"), "a note", 300, False)
        s = t["signoffs"].setdefault(key, dict(status="Not given", history=[]))
        again = s["status"] in ("Returned", "Needs reassessment")
        s.update(status="Signed off", version=t["design_version"], by=user["name"], by_email=user["email"], at=k.now(),
                 note=note, role=user["role"], reason="")
        s["history"].append(dict(status="Re-approved" if again else "Signed off", by=user["name"], by_email=user["email"], role=user["role"], at=k.now(), version=t["design_version"]))
        return f"{key} signed off on version {t['design_version']}" + (" (re-approval)" if again else "")

    def _tech_signoff_return(self, user, c, body):
        t = c.get("technical")
        if not t:
            raise ValueError("Record the design first.")
        key = self._sign_type(body)
        spec = SIGNOFFS[key]
        k.require_role(user, spec["roles"] + k.FINANCE_APPROVERS, "the competent role or a manager")
        reason = k.text(body.get("reason"), "why it is being returned", 300)
        s = t["signoffs"].setdefault(key, dict(status="Not given", history=[]))
        s.update(status="Returned", reason=reason)
        s["history"].append(dict(status="Returned", by=user["name"], by_email=user["email"], role=user["role"], at=k.now(), note=reason, version=t["design_version"]))
        return f"{key} returned: {reason}"
