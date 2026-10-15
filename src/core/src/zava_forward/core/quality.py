"""Quality acceptance per measure (FR-017, AC-019, AC-039).

One record per measure on a case. It moves through a fixed list of states, one
step at a time, by a named person, and every step is audited. The system never
accepts work itself: a person with the right role accepts it, and that person
must be someone other than whoever submitted the evidence, recorded it, or
fixed a defect on it. A provider's submission is kept as evidence only.
"""
from .workflows import MANAGER_ROLES, _now

QUALITY_ROLES = ("Quality Inspector",) + MANAGER_ROLES
SOURCES = ("Installer", "Contractor", "Provider submission", "Our own inspection")
SUBMITTED, ACCEPTED, RETURNED = "Submitted", "Accepted", "Returned"
FIXED, HANDED = "Fixed, awaiting reinspection", "Handed over"
TRANSITIONS = {SUBMITTED: (ACCEPTED, RETURNED), RETURNED: (FIXED,), FIXED: (ACCEPTED, RETURNED), ACCEPTED: (HANDED,), HANDED: ()}

CHECKLISTS = {
    "Loft insulation": dict(version="QC-LOFT v1", items=["Depth measured and photo taken", "Ventilation at the eaves kept clear",
                                                         "Hatch insulated and sealed", "Pipes and tanks protected", "Cables and lights checked"]),
    "Wall insulation": dict(version="QC-WALL v1", items=["Wall surface checked before fitting", "Fixings and thickness match the design",
                                                         "Vents, meters and sills finished", "Finish clean and sealed", "Guarantee issued"]),
    "Heat pump": dict(version="QC-HP v1", items=["Commissioning record present", "Flow temperatures and settings recorded",
                                                 "Controls shown and working", "Noise and position checked", "Guarantee issued"]),
    "Solar panels": dict(version="QC-PV v1", items=["Electrical certificate present", "Roof fixings and sealing checked",
                                                    "Inverter and display working", "Guarantee issued"]),
    "General": dict(version="QC-GEN v1", items=["Work matches the agreed scope", "Area left clean and safe",
                                                "Photos of finished work", "Guarantee or certificate issued"]),
}
_KEYWORDS = (("loft", "Loft insulation"), ("wall", "Wall insulation"), ("heat pump", "Heat pump"), ("solar", "Solar panels"))


def checklist_for(measure):
    low = (measure or "").lower()
    key = next((name for word, name in _KEYWORDS if word in low), "General")
    return dict(CHECKLISTS[key], name=key)


def _clean(text, n=300):
    return (text or "").strip()[:n]


class QualityMixin:
    def _quality(self, c):
        return c.setdefault("quality", [])

    def _qrec(self, c, idx):
        try:
            return self._quality(c)[int(idx)]
        except (IndexError, ValueError, TypeError):
            raise ValueError("Choose one of this case's quality records.")

    def _measures(self, c):
        m = c["measures"]
        return [x.strip() for x in (m if isinstance(m, list) else str(m).split(",")) if x.strip()]

    def _need_quality_role(self, user, what):
        if user["role"] not in QUALITY_ROLES:
            raise PermissionError(f"Only a Quality Inspector or a manager can {what}.")

    def _qmove(self, rec, to, user, note):
        if to not in TRANSITIONS.get(rec["state"], ()):
            raise ValueError(f"This work is '{rec['state']}'. It cannot go to '{to}' from there.")
        rec.setdefault("history", []).append(dict(at=_now(), by=user["name"], from_state=rec["state"], to_state=to, note=note))
        rec["state"] = to

    def _independent(self, rec, user, what):
        """The person accepting must not be anyone who put the work forward or fixed it."""
        involved = {rec.get("submitted_by"), rec.get("recorded_by"), rec.get("fixed_by"), rec.get("fixed_recorded_by")}
        if user["name"].strip().lower() in {(x or "").strip().lower() for x in involved} or user["code"] in (rec.get("recorded_by_code"), rec.get("fixed_by_code")):
            raise PermissionError(f"Someone independent must {what}: it cannot be the person who submitted, recorded or fixed this work.")

    def submit_quality(self, user, case_id, measure, submitted_by, source, items):
        submitted_by, source = _clean(submitted_by, 80), _clean(source, 40)
        if not submitted_by:
            raise ValueError("Say who carried out or submitted the work.")
        if source not in SOURCES:
            raise ValueError("Choose where this evidence came from.")
        with self.lock:
            c = self._case(case_id)
            if c["closed"]:
                raise ValueError("This case is closed.")
            if measure not in self._measures(c):
                raise ValueError("Choose one of this case's measures.")
            if any(r["measure"] == measure and r["state"] != HANDED for r in self._quality(c)):
                raise ValueError("This measure already has a quality record in progress.")
            cl = checklist_for(measure)
            items = items if isinstance(items, dict) else {}
            missing = [lab for lab in cl["items"] if not _clean(items.get(lab), 200)]
            if missing:
                raise ValueError("Each check needs a note of what was seen. Missing: " + "; ".join(missing))
            rec = dict(measure=measure, state=SUBMITTED, checklist=cl["name"], checklist_version=cl["version"],
                       items=[dict(label=lab, evidence=_clean(items[lab], 200)) for lab in cl["items"]],
                       submitted_by=submitted_by, source=source, recorded_by=user["name"], recorded_by_code=user["code"], recorded_at=_now(),
                       history=[dict(at=_now(), by=user["name"], from_state=None, to_state=SUBMITTED, note=f"{source}: {submitted_by}")],
                       defect=None, defects=[], handover=None, aftercare=[])
            self._quality(c).append(rec)
            self.audit(user["email"], "quality_submitted", case_id, f"{measure} {cl['version']} from {source} ({submitted_by})")
            self.save()
            return len(c["quality"]) - 1

    def accept_quality(self, user, case_id, idx, note=""):
        self._need_quality_role(user, "accept work")
        with self.lock:
            c = self._case(case_id)
            self.require_safety_clear(c)
            rec = self._qrec(c, idx)
            if rec["state"] not in (SUBMITTED, FIXED):
                raise ValueError(f"This work is '{rec['state']}'. It can only be accepted after it is submitted or reinspected.")
            self._independent(rec, user, "accept this work")
            self._qmove(rec, ACCEPTED, user, _clean(note))
            rec.update(accepted_by=user["name"], accepted_at=_now())
            self.audit(user["email"], "quality_accepted", case_id, f"{rec['measure']} {rec['checklist_version']} {_clean(note)}".strip())
            self.save()

    def return_quality(self, user, case_id, idx, reason, defect, owner):
        self._need_quality_role(user, "return work")
        reason, defect, owner = _clean(reason), _clean(defect), _clean(owner, 80)
        if not reason or not defect or not owner:
            raise ValueError("Say why it is returned, what the defect is and who will put it right.")
        with self.lock:
            c = self._case(case_id)
            rec = self._qrec(c, idx)
            self._qmove(rec, RETURNED, user, reason)
            rec["defect"] = dict(reason=reason, description=defect, owner=owner, raised_by=user["name"], raised_at=_now())
            rec["defects"].append(dict(rec["defect"]))
            self.audit(user["email"], "quality_returned", case_id, f"{rec['measure']}: {reason}. Defect owner {owner}")
            self.save()

    def record_fix(self, user, case_id, idx, fixed_by, note=""):
        fixed_by = _clean(fixed_by, 80)
        if not fixed_by:
            raise ValueError("Say who put the defect right.")
        with self.lock:
            c = self._case(case_id)
            rec = self._qrec(c, idx)
            self._qmove(rec, FIXED, user, _clean(note))
            rec.update(fixed_by=fixed_by, fixed_recorded_by=user["name"], fixed_by_code=user["code"], fixed_at=_now())
            rec["defect"].update(fixed_by=fixed_by, fixed_at=rec["fixed_at"])
            rec["defects"][-1].update(fixed_by=fixed_by, fixed_at=rec["fixed_at"])
            self.audit(user["email"], "quality_fixed", case_id, f"{rec['measure']} fixed by {fixed_by}. Reinspection needed")
            self.save()

    def reinspect_quality(self, user, case_id, idx, result, note=""):
        """Reinspection ends in acceptance or a return. Acceptance has the same independence rule."""
        if result == "pass":
            return self.accept_quality(user, case_id, idx, note or "Reinspected")
        if result != "fail":
            raise ValueError("Say whether the reinspection passed or failed.")
        with self.lock:
            rec = self._qrec(self._case(case_id), idx)
            if rec["state"] != FIXED:
                raise ValueError("Only fixed work waiting for reinspection can be reinspected.")
            d = rec["defect"]
        self.return_quality(user, case_id, idx, _clean(note) or "Reinspection failed", d["description"], d["owner"])

    def hand_over_quality(self, user, case_id, idx, note, told):
        note = _clean(note)
        if not told or not note:
            raise ValueError("Confirm the resident was told and note what they were given, such as guarantees and how to use it.")
        with self.lock:
            c = self._case(case_id)
            self.require_safety_clear(c)
            rec = self._qrec(c, idx)
            self._qmove(rec, HANDED, user, note)
            rec["handover"] = dict(by=user["name"], at=_now(), note=note, resident_told=True)
            self.audit(user["email"], "quality_handover", case_id, f"{rec['measure']} handed over to resident. {note}")
            self.save()

    def add_aftercare(self, user, case_id, idx, note):
        note = _clean(note)
        if not note:
            raise ValueError("Say what the resident reported or what was done.")
        with self.lock:
            rec = self._qrec(self._case(case_id), idx)
            if rec["state"] != HANDED:
                raise ValueError("Aftercare can be recorded once the work has been handed over.")
            rec["aftercare"].append(dict(at=_now(), by=user["name"], note=note))
            self.audit(user["email"], "quality_aftercare", case_id, f"{rec['measure']}: {note}")
            self.save()
