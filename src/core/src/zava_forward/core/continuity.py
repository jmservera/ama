"""Service continuity, versioned change and supplier-independent export (BRD NFR-002, NFR-004, NFR-006, NFR-007; issue #122).

This records what named people decide and enforces it on the server. It never
decides, approves or restarts for anyone, and an AI assistant has no part in it.

* Suspension: a manager, quality inspector or building safety liaison suspends
  one AI task or the whole release, naming the incident owner, containment and
  the communication owner and audience. Every AI invoke, scan, claim, dispatch,
  completion, review and list/detail view rechecks the persisted state, so a
  disabled button is never the control. Manual case work and hazard response
  are not routed through it and continue.
* Epoch: each suspend and restart increments one counter. A provider call that
  started under an older epoch may finish and stays charged, but its result is
  quarantined: kept for reconstruction, never actionable, never a proposal.
* Restart: a proposer records corrective evidence; a different manager with an
  authority reference decides. A replayed, stale, self-approved or
  unauthorised restart fails. Communication templates are records only; nothing
  is sent to anyone. A witnessed authorised drill is an owner activity and is
  not claimed here.
* Change register: records declared model, rule or configuration versions and
  evaluation evidence. A reversal is another record, not a serving-configuration
  switch. Task-bound release admission is the separate serving control.
* Export: a self-describing bundle with its own digest and ledger chain, so
  evidence stays readable and verifiable with no AI supplier or live service.
"""
import hashlib
import json
import math
import re
import uuid

from . import controls as k

MANAGER_ROLES = ("Retrofit Programme Manager", "Programme Support Officer")
SUSPEND_ROLES = MANAGER_ROLES + ("Quality Inspector", "Building Safety Liaison")
KINDS = ("model", "rule", "configuration")
EVALUATIONS = ("pass", "fail")
EXPORT_FORMAT = "zf-evidence-export/1"
ALL = "all"
MANUAL_NOTE = ("Manual case work, resident challenge and hazard response continue outside any suspension; "
               "emergency and statutory hazard duties are never paused.")
COMMS_NOTE = "Constructed communication record only: nothing is sent and no resident is contacted automatically."


def blank():
    return dict(epoch=0, suspensions=[], changes=[])


def load(raw):
    """A persisted document or an empty one; shared by the Store and the independent assistant connection."""
    doc = json.loads(raw) if raw else blank()
    for key, value in blank().items():
        doc.setdefault(key, value)
    return doc


def active(doc, task):
    """The open suspension that covers this task, or None."""
    for s in doc["suspensions"]:
        if s["status"] == "Suspended" and s["scope"] in (ALL, task):
            return s
    return None


def sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()


def reason_text(s):
    return f"Suspended ({s['id']}): use the manual route. {MANUAL_NOTE}"


def epoch_current(record, epoch):
    recorded = record.get("continuity_epoch", record.get("claim_epoch"))
    return type(recorded) is int and recorded == epoch


def effective_versions(doc):
    """Latest applied, unreversed change per kind and subject."""
    out = {}
    for c in doc["changes"]:
        if c["status"] == "Applied":
            out[f"{c['kind']}:{c['subject']}"] = dict(version=c["to_version"], change=c["id"])
    return out


class ContinuityMixin:
    def _cont(self):
        c = self.data.setdefault("continuity", blank())
        for key, value in blank().items():
            c.setdefault(key, value)
        return c

    def continuity_epoch(self):
        with self.lock:
            return self._cont()["epoch"]

    def ai_epoch_current(self, record):
        return epoch_current(record, self.continuity_epoch())

    def continuity_fence(self):
        """Make the existing optimistic SQL writer validate the observed continuity document."""
        if hasattr(self, "assistant_connection"):
            self._cont()["publication_fence"] = uuid.uuid4().hex

    def continuity_publish(self, task, epoch, source, publish):
        """Retry only a known rolled-back local publication, never a provider call."""
        from .store import ConflictError
        for attempt in range(2):
            try:
                with self.lock:
                    late = source == "ai" and (
                        type(epoch) is not int or epoch != self._cont()["epoch"]
                        or bool(active(self._cont(), task)))
                    if source == "ai":
                        self.continuity_fence()
                    return publish(late)
            except ConflictError as error:
                if error.args != ("continuity",) or attempt:
                    raise

    def continuity_suspension(self, task):
        return active(self._cont(), task)

    def continuity_block(self, task):
        """Reason an AI task must not run now, or None."""
        s = self.continuity_suspension(task)
        return reason_text(s) if s else None

    # ---- suspension and restart
    def suspend(self, user, body, assistant_affected=None):
        k.refuse_bulk(body)
        k.require_role(user, SUSPEND_ROLES, "a manager, quality inspector or building safety liaison can suspend AI work")
        from . import ai_registry
        scope = body.get("scope")
        if scope != ALL and ai_registry.get(scope) is None:
            raise ValueError("Choose all AI work or one registered task.")
        rec = dict(scope=scope, scope_kind="release" if scope == ALL else "task", reason=k.text(body.get("reason"), "why work is suspended", 400),
                   incident_owner=k.text(body.get("incident_owner"), "the incident owner", 120),
                   containment=k.text(body.get("containment"), "the containment", 400),
                   communication=dict(owner=k.text(body.get("comms_owner"), "the communication owner", 120),
                                      audience=k.text(body.get("comms_audience"), "the communication audience", 200),
                                      sent=False, note=COMMS_NOTE),
                   recorded_by=user["email"], recorded_at=k.now(), status="Suspended", restart=None,
                   in_flight_note="A provider call already in flight may complete and stay charged or unknown; its result is quarantined. "
                                  "Remote cancellation and exactly-once billing are not claimed.",
                   synthetic=bool(body.get("synthetic")))
        with self.lock:
            doc = self._cont()
            if active(doc, scope) and active(doc, scope)["scope"] == scope:
                raise ValueError("This scope is already suspended.")
            rec["id"] = k.next_id(doc["suspensions"], "SUS")
            rec["epoch"] = doc["epoch"] + 1
            rec["affected"] = [dict(id=r["id"], task=r["task"], version=(r.get("envelope") or {}).get("task_version"), state=r["status"])
                               for r in self.data["recommendations"]
                               if r.get("kind") == "ai_task" and scope in (ALL, r["task"]) and r["status"] == "Not reviewed"]
            rec["affected_assistant_tasks"] = list(assistant_affected or [])
            rec["affected_assistant_total"] = getattr(assistant_affected, "total", len(rec["affected_assistant_tasks"]))
            rec["affected_assistant_truncated"] = bool(getattr(assistant_affected, "truncated", False))
            doc["epoch"] = rec["epoch"]
            doc["suspensions"].append(rec)
            self.audit(user["email"], "ai_suspend", "-", f"{rec['id']} {scope} epoch={rec['epoch']}")
            self.save()
            return control_record(user, rec)

    def _suspension(self, body):
        s = next((x for x in self._cont()["suspensions"] if x["id"] == body.get("id")), None)
        if not s:
            raise ValueError("Choose one of the suspensions.")
        return s

    def restart_propose(self, user, body):
        k.refuse_bulk(body)
        k.require_role(user, MANAGER_ROLES, "a manager can propose a restart")
        with self.lock:
            s = self._suspension(body)
            if s["status"] != "Suspended":
                raise ValueError("This suspension is not open.")
            s["proposal"] = dict(by=user["email"], at=k.now(), epoch=self._cont()["epoch"],
                                 corrective_evidence=k.text(body.get("corrective_evidence"), "the corrective evidence", 600))
            self.audit(user["email"], "ai_restart_propose", "-", s["id"])
            self.save()
            return control_record(user, s)

    def restart_decide(self, user, body):
        k.refuse_bulk(body)
        k.require_role(user, MANAGER_ROLES, "a manager can decide a restart")
        with self.lock:
            doc = self._cont()
            s = self._suspension(body)
            if s["status"] != "Suspended":
                raise ValueError("This suspension is not open; a replayed restart is refused.")
            p = s.get("proposal")
            if not p:
                raise PermissionError("Restart needs corrective evidence proposed first. Owner: programme manager.")
            if body.get("epoch") != doc["epoch"] or p["epoch"] != doc["epoch"]:
                raise PermissionError("This restart decision is stale: the suspension epoch has changed.")
            k.different_person(user, s["recorded_by"], "decide the restart")
            k.different_person(user, p["by"], "decide the restart")
            decision = k.choice(body.get("decision"), ("Restart", "Keep suspended"), "the decision")
            rec = dict(decision=decision, by=user["email"], at=k.now(), epoch=doc["epoch"], proposal=p,
                       authority_ref=k.text(body.get("authority_ref"), "the named restart authority reference", 200),
                       note="Operator identity alone is not authority; the reference is recorded, not verified here.")
            if decision == "Keep suspended":
                s.setdefault("decisions", []).append(rec)
                s.pop("proposal", None)
            else:
                s["restart"] = rec
                s["status"] = "Restarted"
                doc["epoch"] += 1
                rec["new_epoch"] = doc["epoch"]
            self.audit(user["email"], "ai_restart_decide", "-", f"{s['id']} {decision}")
            self.save()
            return control_record(user, s)

    # ---- change register
    def change_record(self, user, body):
        k.refuse_bulk(body)
        k.require_role(user, MANAGER_ROLES, "a manager can record a model, rule or configuration change")
        kind = k.choice(body.get("kind"), KINDS, "model, rule or configuration")
        evaluation = k.choice(body.get("evaluation"), EVALUATIONS, "the evaluation result")
        rec = dict(kind=kind, subject=k.text(body.get("subject"), "what changes", 120), from_version=k.text(body.get("from_version"), "the current version", 80),
                   to_version=k.text(body.get("to_version"), "the new version", 80), reason=k.text(body.get("reason"), "why", 300),
                   evaluation=dict(result=evaluation, reference=k.text(body.get("evaluation_ref"), "the evaluation reference", 200)),
                   recorded_by=user["email"], recorded_at=k.now(), reverses=None, synthetic=bool(body.get("synthetic")),
                   status="Applied" if evaluation == "pass" else "Blocked")
        if rec["from_version"] == rec["to_version"]:
            raise ValueError("The new version must differ from the current one.")
        with self.lock:
            doc = self._cont()
            now = effective_versions(doc).get(f"{kind}:{rec['subject']}")
            if now and now["version"] != rec["from_version"]:
                raise ValueError(f"The current version of this {kind} is {now['version']}, not {rec['from_version']}.")
            rec["id"] = k.next_id(doc["changes"], "CHG")
            doc["changes"].append(rec)
            self.audit(user["email"], "change_record", "-", f"{rec['id']} {kind} {rec['subject']} {rec['status']}")
            self.save()
            return control_record(user, rec)

    def change_reverse(self, user, body):
        k.refuse_bulk(body)
        k.require_role(user, MANAGER_ROLES, "a manager can reverse a change")
        with self.lock:
            doc = self._cont()
            c = k.find(doc["changes"], body.get("id"), "change")
            if c["status"] != "Applied":
                raise ValueError("Only an applied change can be reversed.")
            current = effective_versions(doc).get(f"{c['kind']}:{c['subject']}")
            if not current or current["change"] != c["id"]:
                raise ValueError("A later change supersedes this one; reverse that first.")
            rev = dict(kind=c["kind"], subject=c["subject"], from_version=c["to_version"], to_version=c["from_version"],
                       reason=k.text(body.get("reason"), "why", 300), evaluation=dict(result="pass", reference=f"restores {c['id']} prior version"),
                       recorded_by=user["email"], recorded_at=k.now(), reverses=c["id"], status="Applied", synthetic=c.get("synthetic", False))
            rev["id"] = k.next_id(doc["changes"], "CHG")
            c["status"] = "Reversed"
            c["superseded_by"] = rev["id"]
            doc["changes"].append(rev)
            self.audit(user["email"], "change_reverse", "-", f"{rev['id']} reverses {c['id']}")
            self.save()
            return control_record(user, rev)

    def continuity_view(self, user):
        k.require_role(user, SUSPEND_ROLES, "a manager, quality inspector or building safety liaison can see the continuity register")
        from . import projection
        doc = self._cont()
        suspensions = [control_record(user, s) for s in doc["suspensions"]]
        return dict(epoch=doc["epoch"], suspensions=suspensions,
                    changes=[control_record(user, c) for c in doc["changes"]],
                    effective=effective_versions(doc) if projection.can_see_reason(user) else {},
                    suspended=[{key: s[key] for key in ("id", "scope") if key in s}
                               for s in suspensions if s["status"] == "Suspended"], note=MANUAL_NOTE)

    # ---- supplier-independent export
    def continuity_export(self, user, assistants=None):
        """Build the bundle. It says whether it is complete and never presents a truncated or unsupported part as whole."""
        k.require_role(user, MANAGER_ROLES, "a manager can export evidence")
        from . import ai_registry, ledger, projection
        source = assistants if isinstance(assistants, dict) else {}
        with self.lock:
            head_count, head_hash = self.ledger_head()
            from .resident_decisions import priority_challenge_state
            recs = [dict(r, **priority_challenge_state(self, r)) for r in self.data["recommendations"]]
            gov = self._gov()
            ledger_rows = list(self.audit_entries())
            report = self.verify_ledger()
            digests = ledger.read_digests(self.digest_dir)
            reasons = [] if isinstance(assistants, dict) else ["assistant source missing or malformed"]
            if len(ledger_rows) != head_count or (ledger_rows and ledger_rows[-1]["hash"] != head_hash):
                reasons.append("ledger changed or could not be read in full during export")
            epoch = self._cont()["epoch"]
            raw = source.get("proposals")
            proposals = [dict(p) if isinstance(p, dict) else p for p in raw] if isinstance(raw, list) else raw
            metadata = dict(supported=source.get("supported"), total=source.get("total"),
                            exported=len(raw) if isinstance(raw, list) else None,
                            truncated=source.get("truncated"), source_status=source.get("source_status"),
                            note=source.get("note"))
            if metadata["truncated"] is True:
                reasons.append("assistant proposal evidence truncated")
            reasons.extend(proposal_problems(dict(assistant_proposals=proposals, assistants=metadata)))
            if isinstance(proposals, list):
                for p in proposals:
                    if isinstance(p, dict) and (
                            not epoch_current(p, epoch) or active(self._cont(), p.get("capability"))):
                        p.update(relied_on=False, actionable=False, epoch_current=False)
            task_releases = source.get("task_releases")
            if "task_releases" not in source and metadata["supported"] is False and not reasons:
                task_releases = dict(
                    supported=False, records=[], total=0, exported=0, truncated=False,
                    note="Explicit unsupported durable task-release source: JSON store has no assistant release storage.")
            bundle = dict(
                format=EXPORT_FORMAT, generated_by=user["email"], generated_at=k.now(), as_of=self.as_of,
                independence="Plain JSON with its own digest and ledger chain. Provider, deployment and model appear only as recorded data; "
                             "reading, verifying or re-importing it needs no AI supplier or live service.",
                registry=ai_registry.registry(),
                ai_records=[self._export_record(r) for r in recs],
                assistant_proposals=proposals, task_releases=task_releases,
                assistants=metadata,
                complete=not reasons, incomplete_reasons=reasons,
                versions=dict(effective=effective_versions(self._cont()), changes=self._cont()["changes"]),
                continuity=dict(epoch=self._cont()["epoch"], suspensions=self._cont()["suspensions"]),
                approvals=dict(protocol_versions=gov["protocol_versions"], releases=gov["releases"], breaches=gov["breaches"]),
                ledger=dict(entries=ledger_rows, report=report, head=dict(count=head_count, hash=head_hash), digests=digests))
            reasons.extend(release_problems(bundle))
            bundle["complete"] = not reasons
            bundle["audience"] = dict(scope="full", full_ledger_proof=True)
            if not projection.can_see_reason(user):
                bundle = limited_export(bundle)
        bundle["digest"] = sha({k_: v for k_, v in bundle.items() if k_ != "digest"})
        self.audit(user["email"], "evidence_export", "-", f"digest={bundle['digest'][:16]} records={len(bundle['ai_records'])}")
        self.save()
        return bundle

    def _export_record(self, r):
        keep = ("id", "kind", "task", "case_ids", "created", "status", "mode", "source", "model", "prompt_version", "envelope", "provenance",
                "citations", "unresolved", "verified", "fallback_reason", "ai_output", "workflow_output", "shown_output", "reviewer_action",
                "reviewer_reason", "override_text", "resolved_by", "resolved_at", "review_evidence", "quarantine", "continuity_epoch", "user", "release")
        result = {key: r[key] for key in keep if key in r} if r.get("kind") == "ai_task" else dict(r, kind=r.get("kind", "priority"))
        task = r.get("task", "priority")
        current = r.get("source") != "ai" or (
            epoch_current(r, self._cont()["epoch"]) and not active(self._cont(), task)
            and not r.get("quarantine") and self.release_current(task, r.get("release"), r.get("model")))
        current = current and not r.get("stale", False)
        result.update(epoch_current=r.get("source") != "ai" or epoch_current(r, self._cont()["epoch"]),
                      actionable=current and r["status"] in ("Not reviewed", "Proposed"),
                      relied_on=current and r["status"] in ("Accepted", "Edited"))
        return result


def control_record(user, record):
    """Project control responses without changing the canonical retained record."""
    from . import ai_registry, projection
    if projection.can_see_reason(user):
        return record
    held = projection.NOTE_HELD
    result = dict(detail=held)
    for key in ("id", "reverses", "superseded_by"):
        value = record.get(key)
        if isinstance(value, str) and re.fullmatch(r"(SUS|CHG)-[0-9]+", value):
            result[key] = value
    for key, choices in (
            ("status", ("Suspended", "Restarted", "Applied", "Blocked", "Reversed")),
            ("kind", KINDS), ("scope_kind", ("release", "task"))):
        if record.get(key) in choices:
            result[key] = record[key]
    scope = record.get("scope")
    if isinstance(scope, str) and (scope == ALL or ai_registry.get(scope)):
        result["scope"] = scope
    for key in ("epoch", "affected_assistant_total"):
        if type(record.get(key)) is int:
            result[key] = record[key]
    if type(record.get("affected_assistant_truncated")) is bool:
        result["affected_assistant_truncated"] = record["affected_assistant_truncated"]
    if isinstance(record.get("affected"), list):
        result["affected_total"] = len(record["affected"])
    if "communication" in record:
        result["communication"] = dict(sent=False, owner=held, audience=held, note=COMMS_NOTE)
    for key in ("reason", "incident_owner", "containment", "subject", "from_version", "to_version"):
        if key in record:
            result[key] = held

    def decision_summary(value):
        summary = dict(detail=held)
        for key in ("epoch", "new_epoch"):
            if type(value.get(key)) is int:
                summary[key] = value[key]
        if value.get("decision") in ("Restart", "Keep suspended"):
            summary["decision"] = value["decision"]
        return summary

    for key in ("proposal", "restart"):
        if isinstance(record.get(key), dict):
            result[key] = decision_summary(record[key])
    if isinstance(record.get("decisions"), list):
        result["decisions"] = [decision_summary(d) for d in record["decisions"] if isinstance(d, dict)]
    return result


def limited_export(bundle):
    """Closed summaries, not rewritten ledger rows or filtered arbitrary free text."""
    from . import projection
    held = projection.NOTE_HELD

    def summary(record):
        result = {key: value for key in ("continuity_epoch", "claim_epoch", "epoch_current", "actionable", "relied_on", "revision")
                  if type(value := record.get(key)) in (int, bool)}
        for key in ("status", "state"):
            value = record.get(key)
            if value in ("Not reviewed", "Proposed", "Accepted", "Edited", "Rejected", "Quarantined",
                         "pending", "leased", "ready", "accepted", "rejected", "quarantined",
                         "Suspended", "Restarted"):
                result[key] = value
        return dict(result, detail=held)

    reason = "Audience-limited export: protected evidence is held; the full canonical ledger cannot be verified from this bundle."
    # Do not traverse unknown evidence fields: any free-text field can contain a reason.
    result = {key: bundle[key] for key in ("format", "generated_by", "generated_at", "as_of", "registry")}
    result.update(
        independence="Plain JSON audience-limited evidence summary; not a complete ledger or task-release proof.",
        audience=dict(scope="limited", full_ledger_proof=False, note=held),
        complete=False, incomplete_reasons=[reason, *bundle["incomplete_reasons"]],
        ai_records=[summary(r) for r in bundle["ai_records"]],
        assistant_proposals=[summary(p) for p in (bundle["assistant_proposals"] or [])
                             if isinstance(p, dict)] if isinstance(bundle["assistant_proposals"], list) else [],
        assistants={**{key: bundle["assistants"][key] for key in ("supported", "total", "exported", "truncated")},
                    "source_status": bundle["assistants"]["source_status"] if bundle["assistants"]["source_status"] in
                    ("available", "unsupported", "unavailable") else "unavailable",
                    "note": held},
        task_releases=dict(supported=False, records=[],
                           total=bundle["task_releases"].get("total") if isinstance(bundle["task_releases"], dict) else None,
                           exported=0, truncated=True, note=held),
        versions=dict(effective={}, changes=[], held_count=len(bundle["versions"]["changes"]), note=held),
        continuity=dict(epoch=bundle["continuity"]["epoch"],
                        suspensions=[summary(s) for s in bundle["continuity"]["suspensions"]], note=held),
        approvals={key: [] for key in ("protocol_versions", "releases", "breaches")},
        ledger=dict(entries=[], head=dict(bundle["ledger"]["head"]), digests=[],
                    report=dict(intact=False, problem=reason), full_proof=False, note=held))
    return result


def proposal_problems(bundle):
    """Validate serialized collection completeness independently of producer flags."""
    problems = []
    proposals, metadata = bundle.get("assistant_proposals"), bundle.get("assistants")
    if not isinstance(proposals, list) or any(not isinstance(p, dict) for p in proposals):
        problems.append("missing or malformed assistant_proposals collection")
    if not isinstance(metadata, dict):
        return problems + ["missing or malformed assistants source metadata"]
    supported, truncated = metadata.get("supported"), metadata.get("truncated")
    total, exported = metadata.get("total"), metadata.get("exported")
    if type(supported) is not bool or type(truncated) is not bool:
        problems.append("assistant source support/truncation flags must be booleans")
    counts_valid = all(type(v) is int and v >= 0 for v in (total, exported))
    if not counts_valid:
        problems.append("assistant proposal counts must be nonnegative integers")
    elif not isinstance(proposals, list) or exported != len(proposals) or exported != total:
        problems.append("assistant proposal collection missing or counts inconsistent")
    if truncated is not False:
        problems.append("assistant proposal evidence truncated or truncation unavailable")
    status = metadata.get("source_status")
    if supported is True:
        if status != "available":
            problems.append("required assistant proposal source unavailable")
    elif supported is False:
        note = metadata.get("note")
        if status != "unsupported" or not isinstance(note, str) or not note.strip():
            problems.append("assistant source unavailable or unsupported status unexplained")
        if not counts_valid or total != 0 or exported != 0 or proposals != []:
            problems.append("unsupported assistant source cannot contain or omit known proposals")
    return problems


def release_problems(bundle):
    """Check retained task-release relationships without a provider or store.

    These checks detect missing/contradictory evidence, not wholesale rewriting of
    unanchored release history. The application ledger does not bind these events.
    """
    from . import ai_registry, rai_release
    problems, references = proposal_problems(bundle), []
    proposals = bundle.get("assistant_proposals")
    if not isinstance(proposals, list) or any(not isinstance(p, dict) for p in proposals):
        return problems
    def retain_reference(reference, task):
        if not isinstance(reference, dict) or not isinstance(reference.get("id"), str) or not reference["id"]:
            problems.append("malformed task-release reference")
        else:
            references.append((reference, task))

    def envelope_reference(envelope, reference, task):
        if envelope is None:
            return
        if not isinstance(envelope, dict):
            problems.append("malformed release evidence envelope")
            return
        if envelope.get("release") is not None:
            retain_reference(envelope["release"], task)
            if envelope["release"] != reference:
                problems.append("envelope task-release reference mismatch")

    for p in proposals:
        reference = p.get("release")
        if reference is not None:
            retain_reference(reference, p.get("capability"))
        elif isinstance(p.get("envelope"), dict) and p["envelope"].get("source") == "ai":
            problems.append("AI proposal has no retained task-release reference")
        envelope_reference(p.get("envelope"), reference, p.get("capability"))
        events = p.get("provenance", [])
        if not isinstance(events, list) or any(not isinstance(e, dict) for e in events):
            problems.append("malformed proposal provenance collection")
            continue
        for event in events:
            envelope_reference(event.get("envelope"), reference, p.get("capability"))
            if event.get("release") is not None:
                retain_reference(event["release"], p.get("capability"))
    records = bundle.get("ai_records")
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        problems.append("missing or malformed AI record collection")
        records = []
    for r in records:
        task = r.get("task", "priority")
        if not isinstance(task, str):
            problems.append("malformed legacy task")
            continue
        task = "legacy:" + task
        if r.get("release") is not None:
            retain_reference(r["release"], task)
        elif r.get("source") == "ai":
            problems.append("Legacy AI record has no retained task-release reference")
        envelope_reference(r.get("envelope"), r.get("release"), task)
    evidence = bundle.get("task_releases")
    if not isinstance(evidence, dict):
        return problems + ["missing or malformed task-release source"]
    records = evidence.get("records")
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        return problems + ["missing or malformed task-release collection"]
    total, exported = evidence.get("total"), evidence.get("exported")
    if any(type(n) is not int or n < 0 for n in (total, exported)) or total != exported or exported != len(records) or evidence.get("truncated") is not False:
        problems.append("task-release evidence truncated or inconsistent")
    supported = evidence.get("supported")
    if supported is not True:
        metadata = bundle.get("assistants")
        metadata = metadata if isinstance(metadata, dict) else {}
        note = evidence.get("note")
        if (supported is not False or records or total != 0 or exported != 0 or references
                or metadata.get("supported") is not False or metadata.get("source_status") != "unsupported"
                or not isinstance(note, str) or not note.strip()):
            problems.append("task-release source unavailable or contradictory unsupported evidence")
    found = {}
    for record in records:
        rid = record.get("id")
        task, snapshot = record.get("task"), record.get("snapshot")
        if not isinstance(rid, str) or not rid:
            problems.append("malformed task-release identity")
            continue
        if rid in found:
            problems.append("duplicate task-release evidence")
        found[rid] = record
        if (not isinstance(task, str) or ai_registry.get(task.removeprefix("legacy:")) is None
                or not isinstance(snapshot, dict) or snapshot.get("id") != rid
                or snapshot.get("task") != task or snapshot.get("status") != "active"
                or not isinstance(snapshot.get("release_version"), str) or not snapshot["release_version"]):
            problems.append("malformed or contradictory task-release snapshot")
        problems.extend(lifecycle_problems(record))
    for reference, task in references:
        record = found.get(reference.get("id"))
        if record is None:
            problems.append("missing task-release evidence")
            continue
        snapshot = record.get("snapshot")
        if not isinstance(snapshot, dict) or not {"id", "release_version"} <= snapshot.keys() or snapshot.get("id") != record["id"] or snapshot.get("task") != task or record.get("task") != task or snapshot.get("status") != "active" or rai_release.reference(snapshot) != reference:
            problems.append("task-release reference digest/version/task mismatch")
    return list(dict.fromkeys(problems))


def lifecycle_problems(record):
    """Check every retained history; equal timestamps establish no UUID ordering."""
    events, revision = record.get("events"), record.get("revision")
    if (not isinstance(events, list) or not events or record.get("truncated") is not False
            or type(record.get("event_total")) is not int or record["event_total"] != len(events)
            or type(revision) is not int or revision != len(events)):
        return ["task-release lifecycle missing or truncated"]
    ids, times = set(), {"release-recorded": [], "release-suspended": [], "release-revoked": []}
    for event in events:
        if not isinstance(event, dict):
            return ["invalid task-release event envelope"]
        eid, at, body = event.get("id"), event.get("at"), event.get("body")
        try:
            finite_at = type(at) in (int, float) and math.isfinite(at)
        except OverflowError:
            finite_at = False
        if (not isinstance(eid, str) or not eid or eid in ids
                or event.get("release_id") != record["id"]
                or not finite_at or not isinstance(body, dict)):
            return ["invalid task-release event envelope"]
        ids.add(eid)
        kind = body.get("kind")
        if not isinstance(kind, str) or kind not in times or (kind == "release-recorded" and body.get("task") != record.get("task")):
            return ["invalid task-release event"]
        times[kind].append(at)
    initial, suspended, revoked = (times[k] for k in ("release-recorded", "release-suspended", "release-revoked"))
    if len(initial) != 1 or any(at < initial[0] for at in suspended + revoked):
        return ["contradictory task-release initial event"]
    status = record.get("current_status")
    if ((status == "active" and revision == 1)
            or (status == "suspended" and suspended and not revoked)
            or (status == "revoked" and len(revoked) == 1
                and all(at <= revoked[0] for at in suspended))):
        return []
    return ["contradictory task-release lifecycle status"]


def verify_export(bundle, expected_head=None):
    """Offline check of an export: digest, ledger chain, recorded ledger head and completeness, using only the bundle.

    The head recorded inside the bundle catches a tail cut that leaves the chain valid, but whoever rebuilds the bundle can
    rewrite it too. Pass expected_head=dict(count, hash) from a copy held outside the application (an immutable
    digest) to detect that. A bundle marked incomplete is never reported valid."""
    from . import ledger
    problems = []
    body = {k_: v for k_, v in bundle.items() if k_ != "digest"}
    if bundle.get("format") != EXPORT_FORMAT:
        problems.append("unknown format")
    if sha(body) != bundle.get("digest"):
        problems.append("digest mismatch")
    limited = bundle.get("audience", {}).get("scope") == "limited" or bundle.get("ledger", {}).get("full_proof") is False
    if limited:
        problems.append("audience-limited evidence cannot verify the full canonical ledger")
    problems.extend(release_problems(bundle))
    for need in ("registry", "ai_records", "versions", "continuity", "approvals", "ledger", "complete"):
        if need not in bundle:
            problems.append(f"missing {need}")
    if "ledger" in bundle:
        led = bundle["ledger"]
        entries = led.get("entries", [])
        if not ledger.verify_entries(iter(entries), led.get("digests", []))["intact"]:
            problems.append("ledger chain broken or shorter than a recorded digest")
        head = led.get("head")
        tail = entries[-1]["hash"] if entries else ledger.GENESIS
        if not head:
            problems.append("missing recorded ledger head")
        elif head.get("count") != len(entries) or head.get("hash") != tail:
            problems.append("ledger tail truncated: entries do not reach the recorded head")
        if expected_head and (expected_head.get("count") != len(entries) or expected_head.get("hash") != tail):
            problems.append("ledger does not match the externally held head")
    if bundle.get("complete") is not True:
        problems.append("bundle is incomplete: " + "; ".join(bundle.get("incomplete_reasons") or ["not marked complete"]))
    return dict(valid=not problems, problems=problems, complete=bundle.get("complete") is True and not problems)
