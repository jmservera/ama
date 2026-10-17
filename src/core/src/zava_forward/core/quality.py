"""Quality acceptance per measure (FR-017, AC-019, AC-039).

One active record per measure on a case, retaining superseded evidence. It moves
through a fixed list of states, one
step at a time, by a named person, and every step is audited. The system never
accepts work itself: a person with the right role accepts it, and that person
must be someone other than whoever submitted the evidence, recorded it, or
fixed a defect on it. A provider's submission is kept as evidence only.
"""
import json
import logging
import os
import re
from contextlib import contextmanager
from copy import deepcopy

from .stock import decision_scope
from .workflows import MANAGER_ROLES, _now
from .resident_decisions import require_context

QUALITY_ROLES = ("Quality Inspector",) + MANAGER_ROLES
SOURCES = ("Installer", "Contractor", "Provider submission", "Our own inspection")
SUBMITTED, ACCEPTED, RETURNED = "Submitted", "Accepted", "Returned"
FIXED, HANDED = "Fixed, awaiting reinspection", "Handed over"
SUPERSEDED = "Superseded"
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
    if text is not None and not isinstance(text, str):
        raise ValueError("Enter text for this quality field.")
    return (text or "").strip()[:n]


def _identity(user):
    return {key: user.get(key) for key in ("name", "email", "code", "oid")}


def _norm(value):
    return (value or "").strip().lower()


class QualityOutcomeError(RuntimeError):
    """A quality decision committed, but the refreshed view is unavailable."""


class QualityMixin:
    @contextmanager
    def _quality_operation(self, user, case_id):
        with self.lock:
            sql = hasattr(self, "db")
            prior = list(self.local.pending) if sql else None
            before = None
            committed = False
            audit_size = None if sql else (os.path.getsize(self.audit_path) if os.path.exists(self.audit_path) else 0)
            audit_head = None if sql else self.last_hash
            try:
                with decision_scope(self, user, case_id) as (c, actor):
                    before = deepcopy(c) if not sql else None
                    snapshot = self._snap.get(case_id) if sql else None
                    try:
                        yield c, actor
                    except BaseException:
                        # Own snapshots advance after COMMIT; check before recovery can reload another writer.
                        committed = sql and self._snap.get(case_id) != snapshot
                        raise
            except BaseException as error:
                if sql:
                    if committed:
                        if isinstance(error, QualityOutcomeError):
                            raise
                        logging.getLogger(__name__).exception("Quality decision committed; refreshed view unavailable")
                        raise QualityOutcomeError(
                            "The quality decision was committed, but the current view could not refresh. "
                            "Reload the case and check its history before retrying."
                        ) from error
                    # The shared decision scope quarantines failed writes before recovery I/O.
                    self.local.pending[:] = prior
                elif before is not None:
                    c.clear()
                    c.update(before)
                    try:
                        if os.path.exists(self.audit_path):
                            with open(self.audit_path, "r+b") as audit:
                                audit.truncate(audit_size)
                        self.last_hash = audit_head
                        from .store import Store
                        Store.save(self)
                    except Exception as recovery_error:
                        error.add_note("Quality state restoration failed; the durable outcome may be unknown. Reload before retrying.")
                        logging.getLogger(__name__).exception("Quality JSON recovery failed")
                        raise RuntimeError("Quality state restoration failed; the durable outcome may be unknown. Reload before retrying.") from recovery_error
                raise

    def _quality(self, c):
        return c.setdefault("quality", [])

    def _qrec(self, c, idx):
        if type(idx) is not int and not (isinstance(idx, str) and re.fullmatch(r"0|[1-9][0-9]*", idx)):
            raise ValueError("Choose one of this case's quality records.")
        try:
            if int(idx) < 0:
                raise ValueError
            rec = self._quality(c)[int(idx)]
        except (IndexError, ValueError, TypeError):
            raise ValueError("Choose one of this case's quality records.")
        if rec["state"] == SUPERSEDED:
            raise ValueError("This evidence was superseded. Use the current quality record.")
        return rec

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
        involved.update(d.get("fixed_by") for d in rec.get("defects", []))
        recorders = [(rec.get("recorded_by"), rec.get("recorded_by_code"))]
        recorders.extend((h.get("by"), None) for h in rec.get("history", []) if h.get("to_state") == FIXED)
        involved.update(name for name, _ in recorders)
        identities = list(rec.get("participants", []))
        codes = {rec.get("recorded_by_code"), rec.get("fixed_by_code")} - {None, ""}
        for person in self._quality_staff():
            if person.get("code") in codes or _norm(person.get("name")) in {_norm(x) for x in involved if x}:
                identities.append(_identity(person))
        for name, code in recorders:
            if not any((code and _norm(other.get("code")) == _norm(code))
                       or (name and _norm(other.get("name")) == _norm(name)) for other in identities):
                raise PermissionError("A contributor's identity is unknown. Ask the quality owner to resolve it before acceptance.")
        if (_norm(user["name"]) in {_norm(x) for x in involved if x}
                or any(_norm(user.get(key)) and _norm(user.get(key)) == _norm(other.get(key))
                       for other in identities for key in ("name", "email", "code", "oid"))):
            raise PermissionError(f"Someone independent must {what}: it cannot be the person who submitted, recorded or fixed this work.")

    def _quality_staff(self):
        if hasattr(self, "db"):
            with self.dblock:
                return [json.loads(row[0]) for row in self.db.execute("SELECT body FROM staff").fetchall()]
        return list(self.staff.values())

    def _quality_participants(self, rec, actor, supplied_name):
        people = [_identity(actor), dict(name=supplied_name)]
        people.extend(_identity(p) for p in self._quality_staff() if _norm(p.get("name")) == _norm(supplied_name))
        rec.setdefault("participants", []).extend(deepcopy(people))

    def submit_quality(self, user, case_id, measure, submitted_by, source, items, context_revision=None):
        submitted_by, source = _clean(submitted_by, 80), _clean(source, 40)
        if not submitted_by:
            raise ValueError("Say who carried out or submitted the work.")
        if source not in SOURCES:
            raise ValueError("Choose where this evidence came from.")
        with self._quality_operation(user, case_id) as (c, user):
            if c["closed"]:
                raise ValueError("This case is closed.")
            if measure not in self._measures(c):
                raise ValueError("Choose one of this case's measures.")
            previous = [(i, r) for i, r in enumerate(self._quality(c)) if r["measure"] == measure]
            if any(r["state"] not in (ACCEPTED, HANDED, SUPERSEDED) for _, r in previous):
                raise ValueError("This measure already has a quality record in progress.")
            cl = checklist_for(measure)
            items = items if isinstance(items, dict) else {}
            missing = [lab for lab in cl["items"] if not _clean(items.get(lab), 200)]
            if missing:
                raise ValueError("Each check needs a note of what was seen. Missing: " + "; ".join(missing))
            binding = None
            if context_revision is not None:
                require_context(c, dict(measure=measure, context_revision=context_revision))
                binding = dict(measure=measure, context_revision=context_revision)
            idx = len(self._quality(c))
            supersedes = [i for i, r in previous if r["state"] != SUPERSEDED]
            if supersedes and binding is None:
                raise ValueError("Bind replacement evidence to the current measure scope revision.")
            rec = dict(measure=measure, state=SUBMITTED, checklist=cl["name"], checklist_version=cl["version"],
                       evidence_version=max((r.get("evidence_version", 1) for _, r in previous), default=0) + 1,
                       supersedes=supersedes,
                       resident_binding=binding,
                       items=[dict(label=lab, evidence=_clean(items[lab], 200)) for lab in cl["items"]],
                       submitted_by=submitted_by, source=source, recorded_by=user["name"], recorded_by_code=user["code"], recorded_at=_now(),
                       history=[dict(at=_now(), by=user["name"], from_state=None, to_state=SUBMITTED, note=f"{source}: {submitted_by}")],
                       defect=None, defects=[], handover=None, aftercare=[])
            self._quality_participants(rec, user, submitted_by)
            for old_idx in supersedes:
                old = self._quality(c)[old_idx]
                old["prior_acceptance"] = {k: deepcopy(old.get(k)) for k in
                                           ("accepted_by", "accepted_at", "accepted_identity", "handover")}
                old.update(superseded_by=idx, superseded_at=_now(), handover=None)
                old.setdefault("history", []).append(dict(at=_now(), by=user["name"], from_state=old["state"],
                                                          to_state=SUPERSEDED, note=f"Replaced by evidence record {idx}"))
                old["state"] = SUPERSEDED
                for key in ("accepted_by", "accepted_at", "accepted_identity"):
                    old.pop(key, None)
            self._quality(c).append(rec)
            self.audit(user["email"], "quality_submitted", case_id, f"{measure} {cl['version']} from {source} ({submitted_by})")
            self.save()
            return len(c["quality"]) - 1

    def accept_quality(self, user, case_id, idx, note=""):
        with self._quality_operation(user, case_id) as (c, user):
            self._need_quality_role(user, "accept work")
            self.require_safety_clear(c)
            rec = self._qrec(c, idx)
            self.require_resident_clear(c, [rec["resident_binding"]] if rec.get("resident_binding") else [])
            if rec["state"] not in (SUBMITTED, FIXED):
                raise ValueError(f"This work is '{rec['state']}'. It can only be accepted after it is submitted or reinspected.")
            self._independent(rec, user, "accept this work")
            if rec["state"] == FIXED and not _clean((rec.get("defect") or {}).get("remediation_evidence")):
                raise ValueError("Remediation evidence is missing. Record the correction evidence before independent reinspection.")
            self._qmove(rec, ACCEPTED, user, _clean(note))
            rec.update(accepted_by=user["name"], accepted_at=_now(), accepted_identity=_identity(user))
            self.audit(user["email"], "quality_accepted", case_id, f"{rec['measure']} {rec['checklist_version']} {_clean(note)}".strip())
            self.save()

    def return_quality(self, user, case_id, idx, reason, defect, owner):
        reason, defect, owner = _clean(reason), _clean(defect), _clean(owner, 80)
        if not reason or not defect or not owner:
            raise ValueError("Say why it is returned, what the defect is and who will put it right.")
        with self._quality_operation(user, case_id) as (c, user):
            self._need_quality_role(user, "return work")
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
        with self._quality_operation(user, case_id) as (c, user):
            note = _clean(note)
            if not note:
                raise ValueError("Record the remediation evidence: what was corrected and the photo, document or inspection reference.")
            rec = self._qrec(c, idx)
            self._qmove(rec, FIXED, user, _clean(note))
            rec.update(fixed_by=fixed_by, fixed_recorded_by=user["name"], fixed_by_code=user["code"], fixed_at=_now())
            self._quality_participants(rec, user, fixed_by)
            rec["defect"].update(fixed_by=fixed_by, fixed_at=rec["fixed_at"], remediation_evidence=note)
            rec["defects"][-1].update(fixed_by=fixed_by, fixed_at=rec["fixed_at"], remediation_evidence=note)
            self.audit(user["email"], "quality_fixed", case_id, f"{rec['measure']} fixed by {fixed_by}. Reinspection needed")
            self.save()

    def reinspect_quality(self, user, case_id, idx, result, note=""):
        """Reinspection ends in acceptance or a return. Acceptance has the same independence rule."""
        if result not in ("pass", "fail"):
            raise ValueError("Say whether the reinspection passed or failed.")
        with self._quality_operation(user, case_id) as (c, user):
            self._need_quality_role(user, "reinspect work")
            rec = self._qrec(c, idx)
            if rec["state"] != FIXED:
                raise ValueError("Only fixed work waiting for reinspection can be reinspected.")
            if result == "pass":
                return self.accept_quality(user, case_id, idx, note or "Reinspected")
            d = rec["defect"]
            self.return_quality(user, case_id, idx, _clean(note) or "Reinspection failed", d["description"], d["owner"])

    def hand_over_quality(self, user, case_id, idx, note, told):
        note = _clean(note)
        if told is not True or not note:
            raise ValueError("Confirm the resident was told and note what they were given, such as guarantees and how to use it.")
        with self._quality_operation(user, case_id) as (c, user):
            self.require_safety_clear(c)
            rec = self._qrec(c, idx)
            self.require_resident_clear(c, [rec["resident_binding"]] if rec.get("resident_binding") else [])
            self._qmove(rec, HANDED, user, note)
            rec["handover"] = dict(by=user["name"], at=_now(), note=note, resident_told=True)
            self.audit(user["email"], "quality_handover", case_id, f"{rec['measure']} handed over to resident. {note}")
            self.save()

    def add_aftercare(self, user, case_id, idx, note):
        note = _clean(note)
        if not note:
            raise ValueError("Say what the resident reported or what was done.")
        with self._quality_operation(user, case_id) as (c, user):
            rec = self._qrec(c, idx)
            if rec["state"] != HANDED:
                raise ValueError("Aftercare can be recorded once the work has been handed over.")
            rec["aftercare"].append(dict(at=_now(), by=user["name"], note=note))
            self.audit(user["email"], "quality_aftercare", case_id, f"{rec['measure']}: {note}")
            self.save()
