"""Case store: loading, views, actions, gates and the hash-chained audit log."""
import csv
import io
import json
import os
import re
import threading
import uuid
from copy import deepcopy
from hashlib import sha256
from decimal import Decimal, InvalidOperation
from datetime import date, datetime

from . import ai_tasks, insights, ledger, projection, ranking
from .finance import FinanceMixin
from .grants import GrantMixin, grant_summary
from .resident_decisions import ResidentDecisionMixin, measure_decision_view
from .signoffs import SignoffMixin, missing_items, technical_gate
from .ai import Ai
from .documents import ACCEPTED, MAX_BYTES, DocumentStoreError, open_document_store
from .procurement import ProcurementMixin
from .quality import QualityMixin
from .workflows import MANAGER_ROLES, WorkflowMixin

DECISIONS = ("Not yet asked", "Waiting", "Accepted", "Declined")
READY_STAGE = "Final checks before ordering"
BOOKED_STAGE = "Install booked"


class GateError(Exception):
    def __init__(self, reasons):
        super().__init__("; ".join(reasons))
        self.reasons = reasons


class ConflictError(Exception):
    """Another writer changed the same record first, so this write was refused."""


class Store(WorkflowMixin, QualityMixin, ProcurementMixin, FinanceMixin, GrantMixin, SignoffMixin, ResidentDecisionMixin):
    def __init__(self, data_path, live_path=None, audit_path=None):
        self.lock = threading.RLock()
        base = os.path.dirname(data_path)
        self.live_path = live_path or os.path.join(base, "live.json")
        self.audit_path = audit_path or os.path.join(base, "audit.jsonl")
        os.makedirs(os.path.dirname(self.live_path) or ".", exist_ok=True)
        os.makedirs(os.path.dirname(self.audit_path) or ".", exist_ok=True)
        src = self.live_path if os.path.exists(self.live_path) else data_path
        with open(src, encoding="utf-8") as f:
            self.data = json.load(f)
        for c in self.data["cases"]:
            c.setdefault("documents", [])
            c.setdefault("funding", dict(route="Not decided", status="Not started", reference="", draft="", approved_by=None))
        self.cases = {c["id"]: c for c in self.data["cases"]}
        self.staff = {s["email"].lower(): s for s in self.data["staff"]}
        self.last_hash = self._tail_hash()
        self.digest_dir = os.environ.get("PW_DIGEST_DIR") or os.path.join(base, "digests")
        self.docs_dir = os.path.join(os.path.dirname(self.live_path), "docs")
        self.docstore = open_document_store(self.docs_dir)
        self.ai = Ai()
        self.version = 0
        self._briefings = {}
        self._ranks = None
        self.data.setdefault("recommendations", [])
        self.as_of = self.data.setdefault("as_of", os.environ.get("PW_AS_OF") or datetime.now().date().isoformat())

    def _tail_hash(self):
        h = ledger.GENESIS
        for e in self.audit_entries():
            h = e["hash"]
        return h

    def save(self):
        self.version += 1
        tmp = self.live_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.data, f)
        os.replace(tmp, self.live_path)

    def audit(self, who, action, case_id, detail):
        entry = ledger.make_entry(who, action, case_id, detail, self.last_hash)
        with open(self.audit_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        self.last_hash = entry["hash"]

    def audit_entries(self):
        if os.path.exists(self.audit_path):
            with open(self.audit_path, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        yield json.loads(line)

    def verify_audit(self):
        return self.verify_ledger()["intact"]

    def verify_ledger(self):
        """Verify the chain and, when digests exist, that each digest still matches it."""
        return ledger.verify_entries(self.audit_entries(), ledger.read_digests(self.digest_dir))

    def ledger_head(self):
        count, head = 0, ledger.GENESIS
        for e in self.audit_entries():
            count, head = count + 1, e["hash"]
        return count, head

    def write_digest(self):
        """Write the current head as a digest file. In Azure this is uploaded to an immutable container."""
        with self.lock:
            count, head = self.ledger_head()
            return ledger.write_digest(self.digest_dir, ledger.make_digest(count, head))

    def ready(self):
        return True

    def _touch(self, case_id):
        """Hook for stores that track which cases a request changed."""

    @staticmethod
    def gate_reasons(c):
        if c.get("exercise"):
            return Store.exercise_readiness(c)
        why = []
        if c["decision"]["status"] != "Accepted":
            why.append("The resident has not confirmed they want the works.")
        if not c["funding_ok"]:
            why.append("Funding has not been confirmed.")
        if any(not h["released"] for h in c["hazards"]):
            why.append("A safety issue is still open.")
        return why + technical_gate(c)

    @staticmethod
    def exercise_readiness(c: dict) -> list[str]:
        """Return deterministic same-home exercise blockers, never approvals."""
        why = []
        if not c.get("technical"):
            why.append("Record a design and independent technical reviews.")
        why.extend(technical_gate(c))
        version = (c.get("technical") or {}).get("design_version")
        for row in measure_decision_view(c):
            latest = row["versions"][-1] if row["versions"] else {}
            if row["status"] != "Accepted" or latest.get("design_version") != version:
                why.append(f"Resident choice for {row['measure']} needs this design version.")
        if not c["funding_ok"]:
            why.append("Record separate evidenced award and approved budget.")
        if c["home"]["epc"] == "Unknown":
            why.append("Resolve authoritative same-home EPC source conflict.")
        if any(not h["released"] for h in c["hazards"]):
            why.append("An external safety hold remains open.")
        if any(not ref["released"] for ref in c["exercise"].get("hazard_references", [])):
            why.append("Supplied external safety reference retains a hold.")
        review_dates = [(f"Source {s['id']}", s.get("at"), 30) for s in c["exercise"].get("evidence", [])
                        if s["authority"] == "survey" or s["id"].endswith("-IDENTITY")]
        if c.get("technical"):
            review_dates.append(("Assessment/design", c["technical"].get("design_at"), 180))
        for row in measure_decision_view(c):
            if row["versions"]:
                review_dates.append((f"Resident choice {row['measure']}", row["versions"][-1].get("at"), 30))
        review_dates.extend(("Funding evidence", e.get("at"), 7) for e in c["exercise"].get("fund_events", [])
                            if e["event"] == "award" and not e.get("stale"))
        review_dates.extend(("External safety reference", r.get("at"), 1)
                            for r in c["exercise"].get("hazard_references", []))
        for label, observed, days in review_dates:
            if not Store.exercise_current(observed, days):
                why.append(f"{label} requires human freshness review ({days} day internal trigger, not legal expiry).")
        return why

    @staticmethod
    def exercise_current(observed: str | None, days: int) -> bool:
        """Apply the declared internal trigger; missing/future dates fail closed."""
        try:
            elapsed = (date.today() - date.fromisoformat(observed[:10])).days
        except (TypeError, ValueError):
            return False
        return 0 <= elapsed <= days

    def exercise_status(self, user: dict) -> dict:
        """Return navigation and analytical snapshots without granting a role."""
        from . import exercise, forecast
        from .decision import InferenceConfig, inference_guard
        with self.lock:
            if not any(c.get("exercise") for c in self.cases.values()):
                raise ValueError("Exercise mode is not active.")
            public = exercise.manifest()
            programme_mode = os.environ.get("PW_PROGRAMME") == "1"
            if programme_mode:
                lead = next((c["id"] for c in self.cases.values() if not c["closed"]), next(iter(self.cases)))
                for profile in public["profiles"]:
                    profile["script"]["case"] = lead
                    profile["script"]["next_action"] = "Open the generated programme case; keep existing history and independent review."
                    actor = next((s for s in self.staff.values() if s["role"] == profile["role"]), None)
                    profile["actor"] = actor["code"] if actor else "No existing matching staff identity"
            for workflow in public["workflows"]:
                workflow["status"] = "Local controls and workflow navigation available; full workflow acceptance Not run."
            for profile in public["profiles"]:
                if profile["id"] == "safety":
                    profile["script"]["blocker"] = "Supplied external authority/reference required; no local safety judgement."
                if profile["id"] == "operator":
                    profile["script"]["blocker"] = "Scheduled RPO/operator reconciliation and real inference remain unaccepted; focused interruption/restore probes are not production recovery."
            stories = []
            for c in self.cases.values():
                if c.get("exercise", {}).get("population") != "story":
                    continue
                if projection.is_contractor(user) and not projection.own_case(user, c):
                    continue
                stories.append(dict(id=c["id"], lifecycle=c["exercise"]["lifecycle"],
                                    owner=c["owner"], blockers=self.exercise_readiness(c),
                                    next_action="Open the same-home workbench; use separate authorized identities."))
                if programme_mode and len(stories) == 10:
                    break
            guard = inference_guard("summary", "generative-drafting",
                                    permissions=("evidence.read", "drafts.assist"),
                                    source_kinds=("case_facts",), source_count=1, text_chars=1, field="narrative")
            live = guard.allowed and self.ai.configured and not ai_tasks.workflow_only()
            return dict(fictional=True, fixture_version=exercise.FIXTURE_VERSION,
                        profiles=public["profiles"], workflows=public["workflows"], stories=stories,
                        forecast={} if programme_mode else {name: forecast.forecast(exercise.forecast_input(name))
                                  for name in public["forecast_scenarios"]},
                        analytical=(dict(cohort="Existing generated programme", cases=len(self.cases),
                                         closed_records=sum(bool(c["closed"]) for c in self.cases.values()),
                                         note="Generated existing records, not verified handover or company outcomes; see portfolio overview.")
                                    if programme_mode else dict(cohort="EX-ANALYTICAL-24", source_version="analytical-snapshot-1",
                                        as_of=exercise.AS_OF, accepted_handovers="Suppressed",
                                        not_accepted="Suppressed", unknown="Suppressed",
                                        denominator="Suppressed (complementary totals)",
                                        note="Separate constructed stakeholder snapshot; all cells/totals suppressed.")),
                        inference=("Live AI configured for reviewed tasks; each request still requires source/spend checks and human review."
                                   if live else f"AI unavailable or disabled ({guard.reason}); templates/manual work are not model success."),
                        validation="Local integration and focused browser fixtures executed. Full nine-workflow and human acceptance remain incomplete; real provider success is recorded per output.",
                        budget=("Owner removed the prior budget cap for this rebuild; model usage and reservations remain recorded. No real payments."
                                if not InferenceConfig.from_env().spend_cap_enforced
                                else "USD 450/month cap; unknown price blocks inference; no purchases or real payments."))

    @staticmethod
    def _exercise_form_role(user: dict, form_type: str) -> None:
        roles = projection.FINANCE_VIEW if form_type != "technical" else (
            "Retrofit Coordinator", *projection.FINANCE_VIEW)
        if user.get("role") not in roles:
            raise PermissionError("This identity cannot access this form or its evidence.")

    @staticmethod
    def _exercise_sources(c: dict, form_type: str) -> list[dict]:
        from . import forms
        fields = forms.SCHEMAS[form_type]["fields"]
        sources = []
        for raw in c["exercise"]["evidence"]:
            allowed = [key for key in raw["field_ids"] if key in fields]
            if not allowed:
                continue
            source = {key: deepcopy(raw[key]) for key in ("id", "version", "authority", "media_type")}
            source.update(case_id=c["id"], authorized=True, field_ids=allowed,
                          hash=sha256(raw["raw_text"].encode()).hexdigest())
            if raw["authority"] == "funding":
                source.update(scheme_id=forms.SCHEME_ID,
                              routes=["competitive", "allocation", "award_return", "claim"])
            sources.append(source)
        return sources

    def exercise_case(self, user: dict, case_id: str) -> dict:
        """Read authorized forms and server-owned same-home source bytes."""
        from . import forms
        with self.lock:
            c = self._case(case_id)
            if not c.get("exercise") or c["exercise"]["population"] != "story":
                raise ValueError("Choose one of the two fictional story homes.")
            allowed = []
            for kind in forms.SCHEMAS:
                try:
                    self._exercise_form_role(user, kind)
                except PermissionError:
                    continue
                allowed.append(kind)
            ids = {s["id"] for kind in allowed for s in self._exercise_sources(c, kind)}
            evidence = [deepcopy(s) for s in c["exercise"]["evidence"] if s["id"] in ids]
            if user["role"] not in projection.FINANCE_VIEW:
                evidence = [s for s in evidence if s["authority"] not in ("funding", "finance", "human")]
            detail = self.detail(case_id, user)
            if user["role"] == "Retrofit Coordinator":
                visible_ids = {key for key, draft in c.get("forms", {}).items() if draft["form_type"] == "technical"}
                for kind in ("narratives", "assistance"):
                    detail["exercise"][kind] = [deepcopy(r) for r in c["exercise"].get(kind, [])
                                               if r.get("form_id") in visible_ids]
            return dict(case=detail, allowed_forms=allowed,
                        forms={key: deepcopy(value) for key, value in c.get("forms", {}).items()
                               if value["form_type"] in allowed},
                        validations={key: forms.validate_draft(value) for key, value in c.get("forms", {}).items()
                                     if value["form_type"] in allowed},
                        sources=evidence, blockers=self.exercise_readiness(c),
                        events=deepcopy(c["exercise"].get("fund_events", []))
                        if user["role"] in projection.FINANCE_VIEW else [],
                        lifecycle=c["exercise"]["lifecycle"],
                        building_id=c["exercise"]["building_id"])

    def exercise_building(self, user: dict, building_id: str) -> dict:
        """Project linked home gates independently; shared identity grants no approval."""
        if not projection.allowed(user, "exercise"):
            raise PermissionError("This identity cannot view exercise building context.")
        with self.lock:
            linked = [c for c in self.cases.values()
                      if c.get("exercise", {}).get("population") == "story"
                      and c["exercise"].get("building_id") == building_id]
            if not linked:
                raise ValueError("Choose a building linked to a fictional story home.")
            homes = []
            for c in linked:
                if projection.is_contractor(user) and not projection.own_case(user, c):
                    continue
                projected = self.exercise_case(user, c["id"])
                homes.append(dict(id=c["id"], lifecycle=projected["lifecycle"],
                                  case=projected["case"], blockers=projected["blockers"],
                                  package_id=c["exercise"].get("package_id", "Unknown"),
                                  applicability=c["exercise"].get("package_applicability", "Unknown")))
            if not homes:
                raise PermissionError("No linked home is assigned to this contractor.")
            return dict(id=building_id, fictional=True, as_of=self.as_of,
                        shared_systems="Unknown: no supplied shared-system evidence",
                        shared_works="Unknown: package identity alone is not reviewed applicability",
                        shared_dependencies="Unknown: no approved shared dependency scope",
                        shared_holds="Unknown: home holds below are not a building-wide decision",
                        shared_cost="Unknown: home costs are not an approved building total",
                        homes=homes,
                        note="Each home retains its own evidence, resident choice, funding, quality and closure. Navigation is read-only.")

    def _exercise_data_authority(self, user: dict) -> dict:
        """Resolve data-edit authority exclusively from the persisted staff roster."""
        staff = self.staff.get(str(user.get("email", "")).lower())
        if staff is None or staff["role"] not in MANAGER_ROLES:
            raise PermissionError("Programme Manager or Programme Support must preview and commit coordination data.")
        if staff["role"] != user.get("role"):
            raise PermissionError("Signed-in role does not match the server-owned staff authority.")
        return staff

    def exercise_data_export(self, user: dict, population: str = "all") -> dict:
        """Export permitted exercise cases/history without AI or privileged raw data."""
        from . import exercise
        from .controls import now
        staff = self.staff.get(str(user.get("email", "")).lower())
        if staff is None or staff.get("role") != user.get("role"):
            raise PermissionError("Export requires the server-owned signed-in staff role and scope.")
        user = staff
        if not projection.allowed(user, "exercise"):
            raise PermissionError("Your role cannot export exercise data.")
        if population not in ("all", "story", "forecast", "scale"):
            raise ValueError("Choose all, story, forecast or scale population explicitly.")
        with self.lock:
            rows = []
            for cid in sorted(self.cases):
                c = self._case(cid)
                metadata = c.get("exercise", {})
                if not metadata or (population != "all" and metadata.get("population") != population):
                    continue
                if projection.is_contractor(user) and not projection.own_case(user, c):
                    continue
                if metadata.get("population") == "story" and not projection.is_contractor(user):
                    authorized = self.exercise_case(user, cid)
                    detail = authorized["case"]
                    sources = authorized["sources"]
                else:
                    detail = self.detail(cid, user)
                    sources = []
                detail.get("exercise", {}).pop("data_previews", None)
                if projection.is_contractor(user):
                    row = dict(case=detail, events=deepcopy(detail.get("appointments", [])),
                               decisions=[], evidence_references=[], sources=[], reviews=[],
                               version=exercise.data_fingerprint(detail))
                else:
                    detail["contacts"] = deepcopy(c["contacts"])
                    projected = detail.get("exercise", {})
                    row = dict(
                        case=detail, version=exercise.data_fingerprint(detail),
                        events={key: deepcopy(detail.get(key, [])) for key in
                                ("history", "contacts", "appointments", "handoffs", "quality")},
                        decisions={key: deepcopy(detail.get(key, [])) for key in
                                   ("decision", "measure_decisions", "technical")},
                        evidence_references=deepcopy(detail.get("documents", [])),
                        sources=deepcopy(sources),
                        reviews={key: deepcopy(projected.get(key, [])) for key in
                                 ("source_history", "fund_events", "hazard_references",
                                  "hazard_reference_history", "data_history")},
                    )
                    row["events"]["data_changes"] = deepcopy(projected.get("data_history", []))
                rows.append(row)
            result = dict(
                metadata=dict(contract_version=exercise.DATA_VERSION, fixture_version=exercise.FIXTURE_VERSION,
                              exported_at=now(), as_of=self.as_of, population=population,
                              scope="own contractor scope" if projection.is_contractor(user) else "permitted exercise cases",
                              count=len(rows), role=user["role"], fictional=True,
                              status="Read-only snapshot; not approval, submission or authoritative stock update."),
                cases=rows,
            )
            self.audit(user.get("email", user["role"]), "exercise_data_export", "-",
                       json.dumps(result["metadata"], sort_keys=True))
            self.save()
            return result

    def exercise_data_action(self, user: dict, body: dict, workbook: bytes | None = None) -> dict:
        """Persist a reviewed preview or explicitly commit unchanged per-case snapshots."""
        from . import exercise
        from .controls import now, text
        actor = self._exercise_data_authority(user)
        if not isinstance(body, dict):
            raise ValueError("Data action requires a JSON object.")
        action = body.get("action")
        with self.lock:
            if action == "commit":
                return self._exercise_data_commit(actor, body)
            if action not in ("import-preview", "bulk-preview"):
                raise ValueError("Choose import-preview, bulk-preview or commit.")
            reason = text(body.get("reason"), "coordination change reason", 300)
            if action == "import-preview":
                if set(body) - {"action", "reason", "filename", "workbook_base64", "fields"}:
                    raise ValueError("Import accepts only the frozen workbook contract, not authority or approval metadata.")
                if not isinstance(body.get("filename"), str) or not body["filename"].lower().endswith(".xlsx"):
                    raise ValueError("Select a .xlsx Case updates workbook.")
                fields = body.get("fields")
                if (not isinstance(fields, list) or not fields or not all(isinstance(field, str) for field in fields)
                        or len(fields) != len(set(fields))
                        or any(field not in exercise.DATA_FIELDS for field in fields)):
                    raise ValueError("Choose coordination_note and/or task_due_date explicitly; owner is immutable.")
                source = exercise.read_case_updates(workbook)
                requested = [dict(row=row["row"], case_id=row["case_id"],
                                  changes={field: row["values"].get(field, "") for field in fields},
                                  errors=list(row["errors"])) for row in source["rows"]]
                lineage = {key: source[key] for key in
                           ("source_sha256", "sheet", "mapping", "parser_version", "source_unchanged")}
            else:
                if set(body) - {"action", "reason", "case_ids", "changes"}:
                    raise ValueError("Bulk coordination data cannot contain controlled actions or authority metadata.")
                ids, changes = body.get("case_ids"), body.get("changes")
                if not isinstance(ids, list) or not 1 <= len(ids) <= 25:
                    raise ValueError("Select between 1 and 25 exact case IDs.")
                if not isinstance(changes, dict):
                    raise ValueError("Supply explicit coordination field changes.")
                requested = [dict(row=index, case_id=cid, changes=deepcopy(changes), errors=[])
                             for index, cid in enumerate(ids, 1)]
                lineage = dict(parser_version=exercise.DATA_VERSION, source="explicit bulk input")
            rows = []
            ids = [row["case_id"] for row in requested]
            for row in requested:
                cid = row["case_id"]
                errors = row["errors"] + exercise.validate_data_changes(row["changes"])
                if not isinstance(cid, str) or not cid:
                    errors.append("case_id: required exact case mapping.")
                    c = None
                else:
                    c = self.cases.get(cid)
                    if ids.count(cid) > 1:
                        errors.append("Duplicate/conflicting case rows; repair every duplicate and preview again.")
                if c is None or not c.get("exercise"):
                    errors.append("Unknown or non-exercise case ID; no cross-case mapping or stock updates.")
                    c = None
                before = {field: deepcopy(c["exercise"].get(field)) for field in row["changes"]
                          if field in exercise.DATA_FIELDS} if c else {}
                rows.append(dict(row=row["row"], case_id=cid, errors=errors, before=before,
                                 changes=row["changes"], status="error" if errors else "ready",
                                 expected_fingerprint=exercise.data_fingerprint(c) if c else None))
            input_hash = sha256(json.dumps(dict(rows=rows, lineage=lineage, reason=reason),
                                           sort_keys=True).encode()).hexdigest()
            preview = dict(token=uuid.uuid4().hex, actor=actor["email"], action=action,
                           created_at=now(), reason=reason, input_hash=input_hash, lineage=lineage,
                           rows=rows, status="Preview only; unverified coordination metadata.",
                           committed=False)
            anchor = next((self.cases[row["case_id"]] for row in rows
                           if isinstance(row["case_id"], str) and row["case_id"] in self.cases
                           and self.cases[row["case_id"]].get("exercise")), None)
            if anchor is None:
                preview["token"] = None
                self.audit(actor["email"], "exercise_data_preview_rejected", "-",
                           json.dumps(dict(input_hash=input_hash, rows=rows), sort_keys=True))
                self.save()
                return preview
            self._touch(anchor["id"])
            previews = anchor["exercise"].setdefault("data_previews", [])
            previews.append(deepcopy(preview))
            previews[:] = previews[-20:]
            self.audit(actor["email"], "exercise_data_preview", anchor["id"], input_hash)
            self.save()
            return preview

    def _exercise_data_commit(self, actor: dict, body: dict) -> dict:
        """Apply only a server-stored preview; report every error/stale row."""
        from . import exercise
        from .controls import now
        if set(body) != {"action", "token", "input_hash", "expected_fingerprints"}:
            raise ValueError("Commit requires token, input_hash and exact expected_fingerprints only.")
        preview = None
        anchor = None
        for c in self.cases.values():
            for candidate in c.get("exercise", {}).get("data_previews", []):
                if candidate["token"] == body["token"]:
                    anchor, preview = c, candidate
                    break
        if preview is None or preview["actor"] != actor["email"]:
            raise PermissionError("Preview is missing, expired or belongs to another staff identity.")
        expected = {str(row["row"]): row["expected_fingerprint"] for row in preview["rows"]}
        if body["input_hash"] != preview["input_hash"] or body["expected_fingerprints"] != expected:
            raise ValueError("Commit inputs differ from the exact reviewed preview.")
        if preview["committed"]:
            return deepcopy(preview["result"])
        outcomes = []
        # Validate all snapshots before changing the anchor or any target case.
        for row in preview["rows"]:
            c = self.cases.get(row["case_id"]) if isinstance(row["case_id"], str) else None
            errors = list(row["errors"])
            if not errors and (c is None or exercise.data_fingerprint(c) != row["expected_fingerprint"]):
                errors.append("Stale case version; preview the current data again before committing.")
            outcomes.append(dict(row=row["row"], case_id=row["case_id"], errors=errors,
                                 status="error" if errors else "committed"))
        at = now()
        for row, outcome in zip(preview["rows"], outcomes):
            if outcome["errors"]:
                continue
            c = self._case(row["case_id"])
            self._touch(c["id"])
            record = dict(token=preview["token"], row=row["row"], actor=actor["email"], at=at,
                          reason=preview["reason"], before=deepcopy(row["before"]),
                          changes=deepcopy(row["changes"]), lineage=deepcopy(preview["lineage"]),
                          input_hash=preview["input_hash"], prior_fingerprint=row["expected_fingerprint"],
                          status="Unverified coordination metadata; not source-of-record stock or approval.")
            c["exercise"].update(row["changes"])
            c["exercise"].setdefault("data_history", []).append(record)
            self.audit(actor["email"], "exercise_data_commit", c["id"], json.dumps(record, sort_keys=True))
        result = dict(token=preview["token"], input_hash=preview["input_hash"], outcomes=outcomes,
                      committed=sum(row["status"] == "committed" for row in outcomes),
                      errors=sum(row["status"] == "error" for row in outcomes),
                      lineage=deepcopy(preview["lineage"]), status="Every row disposition reported.")
        self._touch(anchor["id"])
        preview.update(committed=True, result=deepcopy(result))
        self.audit(actor["email"], "exercise_data_batch_result", anchor["id"], json.dumps(result, sort_keys=True))
        self.save()
        return result

    def exercise_action(self, user: dict, case_id: str, body: dict) -> dict:
        """Apply one attributed exercise action atomically on its owning case."""
        from . import forms
        from .controls import refuse_bulk, text, now
        refuse_bulk(body)
        with self.lock:
            original = self._case(case_id)
            if not original.get("exercise") or original["exercise"]["population"] != "story":
                raise ValueError("Choose a fictional story home, not an analytical fixture.")
            c = deepcopy(original)
            state = c["exercise"]
            action = body.get("action")
            if action == "source-correct":
                self._exercise_correct_source(user, c, body)
            elif action == "funding-event":
                self._exercise_funding_event(user, c, body)
            elif action == "external-hazard-reference":
                if user["role"] != "Building Safety Liaison":
                    raise PermissionError("Building Safety records supplied external references only.")
                ref = {key: text(body.get(key), key, 300) for key in ("authority", "version", "evidence", "reference")}
                if type(body.get("released")) is not bool:
                    raise ValueError("Supply the external authority's explicit released flag.")
                ref.update(released=body["released"], by=user["email"], at=now(),
                           note="Supplied fictional external decision; no local sufficiency judgement.")
                refs = state.setdefault("hazard_references", [])
                state.setdefault("hazard_reference_history", []).extend(
                    deepcopy(r) for r in refs if r["reference"] == ref["reference"])
                refs[:] = [r for r in refs if r["reference"] != ref["reference"]]
                refs.append(ref)
                if body.get("hazard_index") is not None:
                    hazard = self._hazard(c, body["hazard_index"])
                    if not hazard.get("referred"):
                        raise ValueError("Refer the hazard before recording the supplied external response.")
                    hazard.update(released=ref["released"], external_reference=deepcopy(ref))
            elif action == "hazard-followup":
                if user["role"] != "Building Safety Liaison":
                    raise PermissionError("Building Safety records separately supplied referral evidence.")
                hazard = self._hazard(c, body.get("hazard_index"))
                if not hazard.get("referred"):
                    raise ValueError("Record the sent referral before receipt, acceptance or chase evidence.")
                step = body.get("step")
                history = hazard.setdefault("external_history", [])
                if step not in ("received", "accepted", "chased"):
                    raise ValueError("Choose received, accepted or chased; no hazard clock/classification/closure action.")
                if step == "accepted" and not any(e["step"] == "received" for e in history):
                    raise ValueError("External receipt and acceptance need separate supplied evidence.")
                event = dict(step=step, by=user["email"], recorded_at=now(),
                             authority=text(body.get("authority"), "external authority", 80),
                             actor=text(body.get("external_actor"), "supplied external actor or Unknown", 80),
                             reference=text(body.get("reference"), "external action reference", 80),
                             evidence=text(body.get("evidence"), "external action evidence", 300),
                             followup=text(body.get("followup"), "owned follow-up", 300))
                if any(e["reference"] == event["reference"] for e in history):
                    raise ValueError("Receipt, acceptance and chase require distinct external action references; do not duplicate supplied evidence.")
                observed = text(body.get("observed_at"), "supplied external action timestamp", 80)
                if datetime.fromisoformat(observed.replace("Z", "+00:00")).tzinfo is None:
                    raise ValueError("Supply an external event timestamp with an explicit timezone.")
                event["observed_at"] = observed
                history.append(event)
                if step == "received":
                    hazard.update(received_reference=deepcopy(event))
                elif step == "accepted":
                    hazard.update(accepted_reference=deepcopy(event))
                hazard["followup_owner"] = user["email"]
                hazard["followup"] = event["followup"]
            elif action == "milestone":
                if user["role"] not in MANAGER_ROLES:
                    raise PermissionError("Independent Programme reviewer records accepted milestone evidence.")
                wid = body.get("work_order")
                order = self._work_order(wid)
                if order["case_id"] != case_id:
                    raise PermissionError("Milestone belongs to a different home.")
                milestone = body.get("milestone")
                amounts = {"mobilisation": 3600, "installation": 12600, "handover": 1800}
                if milestone not in amounts:
                    raise ValueError("Choose one fictional contract milestone.")
                if user["name"] == order["versions"][-1]["issued_by"]:
                    raise PermissionError("Milestone reviewer must differ from work-order issuer.")
                if milestone == "mobilisation" and order["state"] != "Appointed":
                    raise ValueError("Verified booked mobilisation evidence is required; no advance payment.")
                if milestone == "installation" and not all(
                    any(r["measure"] == measure and r["state"] in ("Accepted", "Handed over")
                        for r in c.get("quality", [])) for measure in self._measures(c)):
                    raise ValueError("Independent quality acceptance is required for installation milestone.")
                if milestone == "handover" and state["lifecycle"] != "Handover":
                    raise ValueError("Resident handover is required for retention milestone.")
                evidence = text(body.get("evidence"), "accepted milestone evidence", 300)
                ref = f"{wid}:{milestone}"
                if ref in state.get("milestones", {}):
                    state.setdefault("milestone_history", []).append(dict(reference=ref, **deepcopy(state["milestones"][ref])))
                state.setdefault("milestones", {})[ref] = dict(work_order=wid, amount=amounts[milestone],
                                                               by=user["email"], at=now(), evidence=evidence)
            elif action == "lifecycle":
                self._exercise_lifecycle(user, c, body)
            elif action == "handoff":
                self._exercise_handoff(user, c, body)
            elif action == "return":
                from .controls import text
                if user["role"] not in MANAGER_ROLES:
                    raise PermissionError("An authorized Programme reviewer returns or reopens exercise work.")
                stages = ("Intake", "Assessment", "Funding", "Ready", "Installation", "Provider completed",
                          "Independent QA", "Handover", "Financial closure")
                old, target = state["lifecycle"], body.get("target")
                if target not in stages or stages.index(target) >= stages.index(old):
                    raise ValueError("Return to an earlier exercise stage; no forward approval shortcut.")
                receiver = self._staff_person(body.get("receiver"))
                returns = state.setdefault("returns", [])
                entry = dict(id=f"RETURN-{len(returns)+1:03d}", version=len(returns)+1,
                             from_stage=old, to_stage=target, reason=text(body.get("reason"), "return reason", 300),
                             source=text(body.get("evidence"), "return source", 300),
                             by=user["email"], at=now(), receiver=receiver["email"],
                             next_action=text(body.get("next_action"), "owned next action", 300))
                from .signoffs import SIGNOFFS
                signoffs = body.get("affected_signoffs", [])
                fields = body.get("affected_form_fields", {})
                milestones = body.get("affected_milestones", [])
                if (not isinstance(signoffs, list) or any(not isinstance(key, str) or key not in SIGNOFFS for key in signoffs)
                        or len(signoffs) != len(set(signoffs))):
                    raise ValueError("Name each affected technical sign-off once, or supply an empty list.")
                if not isinstance(fields, dict):
                    raise ValueError("Affected form fields must map same-home form IDs to explicit field lists.")
                if (not isinstance(milestones, list)
                        or any(not isinstance(ref, str) or ref not in state.get("milestones", {}) for ref in milestones)
                        or len(milestones) != len(set(milestones))):
                    raise ValueError("Name each existing same-home milestone reference once, or supply an empty list.")
                for fid, keys in fields.items():
                    draft = c.get("forms", {}).get(fid)
                    if (draft is None or not isinstance(keys, list) or not keys
                            or any(not isinstance(key, str) or key not in draft["fields"] for key in keys)
                            or len(keys) != len(set(keys))):
                        raise ValueError("Name known fields once on each existing same-home form; no other home or guessed scope.")
                for key in signoffs:
                    self._tech_signoff_return(user, c, dict(type=key, reason=entry["reason"]))
                entry["affected_signoffs"] = list(signoffs)
                entry["affected_form_fields"] = deepcopy(fields)
                entry["affected_milestones"] = list(milestones)
                entry["invalidation"] = {}
                for ref in milestones:
                    milestone = state["milestones"][ref]
                    state.setdefault("milestone_history", []).append(dict(reference=ref, **deepcopy(milestone)))
                    milestone.update(stale=True, return_id=entry["id"], reassessment_reason=entry["reason"],
                                     reassessment_source=entry["source"])
                for fid, keys in fields.items():
                    draft = c["forms"][fid]
                    updated = forms.update_versions(draft, input_versions={
                        key: draft["fields"][key]["input_version"]+1 for key in keys})
                    c["forms"][fid] = updated
                    entry["invalidation"][fid] = deepcopy(updated["last_invalidation"])
                returns.append(entry)
                state["lifecycle"] = target
                stage_labels = {
                    "Intake": "Contacting resident", "Assessment": "Design in progress",
                    "Funding": "Funding check", "Ready": READY_STAGE,
                    "Installation": "Works under way", "Provider completed": "Quality check",
                    "Independent QA": "Quality check", "Handover": "Handover to arrange",
                }
                c.update(closed=False, waiting_on=receiver["name"], stage=stage_labels[target],
                         reason=entry["next_action"])
                self._exercise_reconcile_dependents(c)
            elif action == "resident-update":
                self._exercise_resident_update(user, c, body)
            else:
                drafts = c.setdefault("forms", {})
                if action == "create-form":
                    kind = body.get("form_type")
                    if kind not in forms.SCHEMAS:
                        raise ValueError("Select an approved exercise template.")
                    if body.get("schema_version", forms.SCHEMA_VERSION) != forms.SCHEMA_VERSION:
                        raise ValueError("Unapproved schema version.")
                    self._exercise_form_role(user, kind)
                    sources = self._exercise_sources(c, kind)
                    route = None
                    if forms.SCHEMAS[kind]["funding"]:
                        funding_source = next((s for s in sources if s["id"] == f"{case_id}-FUND"), None)
                        if funding_source is None:
                            raise ValueError("Record a same-home funding-route source before preparing a funding form.")
                        route = dict(scheme_id=forms.SCHEME_ID, route=kind, version=funding_source["version"],
                                     source_id=f"{case_id}-FUND")
                    if "route" in body and body["route"] != route:
                        raise ValueError("Client-supplied route does not match the server-owned same-home scheme evidence.")
                    draft = forms.create_draft(case_id, kind, sources=sources, route=route)
                    fid = f"FORM-{len(drafts) + 1:03d}"
                    drafts[fid] = draft
                else:
                    fid = body.get("form_id")
                    if fid not in drafts:
                        raise ValueError("Choose a form on this home.")
                    draft = drafts[fid]
                    self._exercise_form_role(user, draft["form_type"])
                    field = body.get("field")
                    if action == "extract":
                        source = next((s for s in self._exercise_sources(c, draft["form_type"])
                                       if s["id"] == body.get("source_id")), None)
                        if source is None:
                            raise PermissionError("Source is unavailable on this home and template.")
                        raw = next(s for s in state["evidence"] if s["id"] == source["id"])
                        draft = forms.extract_candidates(draft, source, raw["raw_text"].encode())
                    elif action == "select":
                        draft = forms.select_candidate(draft, field, body.get("candidate_id"))
                    elif action == "review":
                        if field == "completed" and state["lifecycle"] not in ("Handover", "Financial closure"):
                            raise ValueError("The constructed completion source is not accepted completion; actual QA/handover must exist.")
                        draft = forms.review_field(draft, field, body.get("review_action"), user,
                            value=body.get("value"), unit=body.get("unit"), currency=body.get("currency"),
                            evidence=body.get("evidence", []), reason=body.get("reason"),
                            unresolved=body.get("unresolved", False))
                    elif action == "human-field":
                        if field == "match_budget_approved" and (
                                c.get("finance", {}).get("budget") or {}).get("status") != "Approved":
                            raise ValueError("Independent budget approval must exist first.")
                        draft = forms.human_field_action(draft, field, user, value=body.get("value"),
                            evidence=body.get("evidence", []), reason=body.get("reason"))
                    elif action == "calculate":
                        draft = forms.recalculate(draft)
                    elif action == "attachments":
                        draft = forms.set_attachments(draft, body.get("evidence", []))
                    elif action == "review-pack":
                        if draft["form_type"] == "claim" and state["lifecycle"] not in ("Handover", "Financial closure"):
                            raise ValueError("Claim review requires actual accepted resident handover.")
                        draft = forms.review_pack(draft, user, evidence=body.get("evidence", []),
                                                  reason=body.get("reason"))
                    elif action == "export":
                        draft = forms.export_pack(draft)
                    elif action in ("assist", "support"):
                        proposal = self._exercise_assist(c, draft, field,
                            task="evidence_support" if action == "support" else "form_candidate_selection",
                            claim=body.get("claim"))
                        state.setdefault("assistance", []).append(dict(proposal, form_id=fid, stale=False))
                    elif action == "versions":
                        if user["role"] not in MANAGER_ROLES:
                            raise PermissionError("A template owner records explicit schema/rule version changes.")
                        text(body.get("reason"), "version change reason", 300)
                        draft = forms.update_versions(draft, schema_version=body.get("schema_version"),
                                                      rule_version=body.get("rule_version"))
                    elif action == "narrative":
                        result = self.ai.source_narrative(case_id, draft)
                        result = ai_tasks.finish(self, user, "source_bound_narrative", [case_id], result,
                            "Manual source-bound narrative; no external action.",
                            {case_id: result.get("citable_facts", [])},
                            record_cites=result.get("citations", []), persist=False)
                        state.setdefault("narratives", []).append(dict(result, form_id=fid, stale=False,
                                                                     by=user["email"], at=now()))
                        record = next(r for r in self.data["recommendations"] if r["id"] == result["record_id"])
                        record.update(form_id=fid, input_version=draft["input_version"],
                                      source_refs=result.get("source_refs", []))
                    elif action == "review-narrative":
                        result = next((r for r in state.get("narratives", [])
                                       if r.get("record_id") == body.get("record_id") and r["form_id"] == fid), None)
                        if result is None or result["stale"] or result["input_version"] != draft["input_version"]:
                            raise ValueError("Choose a current same-home narrative; stale output cannot be reviewed.")
                        reviewed = ai_tasks.review(self, user, result["record_id"], body.get("review_action"),
                                                   body.get("reason", ""), body.get("text"), persist=False)
                        result["approval"] = reviewed["status"]
                        result["reviewer_reason"] = reviewed["reviewer_reason"]
                        if reviewed["override_text"] is not None:
                            result["text"] = reviewed["override_text"]
                    else:
                        raise ValueError("Unknown exercise action.")
                    drafts[fid] = draft
                for record in [*state.get("assistance", []), *state.get("narratives", [])]:
                    if record.get("form_id") == fid and str(record.get("input_version", record.get("case_version"))) != str(draft["input_version"]):
                        record["stale"] = True
                self._exercise_reconcile_dependents(c)
            self.audit(user["email"], f"exercise_{action}", case_id,
                       json.dumps(dict(action=action, form_id=body.get("form_id"), source_id=body.get("source_id"),
                                       reason=body.get("reason")), sort_keys=True))
            original.clear()
            original.update(c)
            self.save()
            return self.exercise_case(user, case_id)

    def _exercise_correct_source(self, user: dict, c: dict, body: dict) -> None:
        from . import forms
        from .controls import text, now
        source = next((s for s in c["exercise"]["evidence"] if s["id"] == body.get("source_id")), None)
        if source is None:
            raise PermissionError("Source is not on this home.")
        roles = projection.FINANCE_VIEW if source["authority"] in ("finance", "funding", "human") else (
            "Retrofit Coordinator", *MANAGER_ROLES)
        if user["role"] not in roles:
            raise PermissionError("Ask the source's authorized domain owner to correct it.")
        reason = text(body.get("reason"), "correction reason", 300)
        raw = text(body.get("raw_text"), "replacement source bytes", 12000)
        c["exercise"].setdefault("source_history", []).append(dict(deepcopy(source), reason=reason))
        source.update(raw_text=raw, version=f"{source['version']}.r{len(c['exercise']['source_history'])}",
                      by=user["email"], at=now(), reason=reason)
        for draft in c.get("forms", {}).values():
            metadata = next((s for s in self._exercise_sources(c, draft["form_type"])
                             if s["id"] == source["id"]), None)
            if metadata and source["id"] in draft["sources"]:
                updated = forms.update_source(draft, metadata)
                draft.clear()
                draft.update(updated)
        if source["authority"] == "survey":
            values = {s["raw_text"].strip() for s in c["exercise"]["evidence"] if s["authority"] == "survey"}
            match = re.fullmatch(r"epc_band:\s*([A-G])", next(iter(values))) if len(values) == 1 else None
            c["home"]["epc"] = match.group(1) if match else "Unknown"
        self._exercise_reconcile_dependents(c)
        for record in [*c["exercise"].get("assistance", []), *c["exercise"].get("narratives", [])]:
            refs = record.get("source_refs", record.get("sources", []))
            if any(ref["id"] == source["id"] and (
                    ref["version"] != source["version"] or ref["hash"] != sha256(raw.encode()).hexdigest())
                   for ref in refs):
                record["stale"] = True

    @staticmethod
    def _exercise_reconcile_dependents(c: dict) -> None:
        """Suspend exactly the external events bound to changed reviewed packs."""
        from . import forms
        events = c["exercise"].get("fund_events", [])
        by_id = {event["id"]: event for event in events}
        for event in events:
            try:
                current = forms.export_pack(c["forms"][event["form_id"]])["exports"][-1]
                stale = current["finance_review"]["digest"] != event["digest"]
            except ValueError:
                stale = True
            if stale:
                event["stale"] = True
        # Predecessors are recorded before descendants; historical staleness is irreversible.
        for event in events:
            previous = event.get("previous_event")
            if previous and (previous not in by_id or by_id[previous].get("stale")):
                event["stale"] = True
        awards = [event for event in events if event["event"] == "award"]
        if awards:
            current_award = awards[-1]
            c["funding_ok"] = not current_award.get("stale") and (
                c.get("finance", {}).get("budget") or {}).get("status") == "Approved"
            c["exercise"]["funding_reassessment"] = (
                "Current reviewed external award and independently approved budget."
                if c["funding_ok"] else
                "Reviewed evidence changed; historical external award retained, readiness suspended.")

    def _exercise_handoff(self, user: dict, c: dict, body: dict) -> None:
        from .controls import text, now
        step = body.get("step")
        h = c.get("handoff")
        reason = text(body.get("reason"), "handoff reason", 300)
        evidence = text(body.get("evidence"), "separately supplied handoff evidence", 300)
        if step == "sent":
            if user["code"] != c["owner_code"] and user["role"] not in MANAGER_ROLES:
                raise PermissionError("Only the current owner or Programme team sends a handoff.")
            if h and h.get("phase") not in ("Returned", "Completed", None):
                raise ValueError("Resolve the existing handoff before sending another.")
            receiver = self._staff_person(body.get("receiver"))
            if receiver["code"] == c["owner_code"]:
                raise ValueError("A handoff needs a different receiver.")
            due = text(body.get("due"), "handoff due date or Unknown", 80)
            if due != "Unknown":
                date.fromisoformat(due)
            urgency = body.get("urgency")
            if urgency not in ("Routine", "Urgent", "Unknown"):
                raise ValueError("Supply Routine, Urgent or Unknown urgency.")
            h = dict(state="Offered", phase="Sent", from_code=c["owner_code"], from_name=c["owner"],
                     to_code=receiver["code"], to_name=receiver["name"], destination=receiver["role"],
                     proposed_receiver=receiver["email"], confirmed_receiver=None, chase_owner=c["owner"],
                     offered_by=user["name"], offered_at=now(), note=reason, answered_at=None, answer_note="",
                     due=due, urgency=urgency,
                     next_action=text(body.get("next_action"), "handoff next action", 300), history=[])
            c["handoff"] = h
        else:
            if not h or "phase" not in h:
                raise ValueError("Record a separately evidenced sent handoff first.")
            if step in ("received", "accepted", "returned", "completed") and user["code"] != h["to_code"]:
                raise PermissionError("Only the named receiver records this handoff disposition.")
            if step == "received" and h["phase"] in ("Sent", "Escalated"):
                h.update(phase="Received", received_at=now(), received_by=user["email"])
            elif step == "accepted" and h["phase"] == "Received":
                h.update(phase="Accepted", state="Accepted", answered_at=now(),
                         confirmed_receiver=user["email"], chase_owner=user["name"])
                c.update(owner=user["name"], owner_code=user["code"], owner_role=user["role"],
                         waiting_on=user["name"])
            elif step == "returned" and h["phase"] in ("Sent", "Received", "Escalated"):
                h.update(phase="Returned", state="Declined", answered_at=now(), answer_note=reason)
            elif step == "completed" and h["phase"] == "Accepted":
                h.update(phase="Completed", completed_at=now())
            elif step == "escalated" and h["phase"] in ("Sent", "Received"):
                if user["code"] != h["from_code"] and user["role"] not in MANAGER_ROLES:
                    raise PermissionError("Only the sender/chase owner or Programme reviewer escalates.")
                h.update(phase="Escalated", escalation_owner=text(body.get("escalation_owner"), "escalation owner", 80))
            else:
                raise ValueError("Invalid handoff transition; receipt never implies acceptance.")
        h["history"].append(dict(step=step, by=user["email"], at=now(), reason=reason, evidence=evidence,
                                 owner=c["owner"], chase_owner=h["chase_owner"]))
        c.setdefault("handoff_log", []).append(deepcopy(h))

    def _exercise_resident_update(self, user: dict, c: dict, body: dict) -> None:
        from .controls import text, now
        if user["role"] not in ("Resident Liaison Officer", *MANAGER_ROLES):
            raise PermissionError("Resident liaison or the named case team records update commitments.")
        updates = c["exercise"].setdefault("resident_updates", [])
        step = body.get("step", "create")
        if step == "create":
            due = text(body.get("due", "Unknown"), "update due date or Unknown", 80)
            if due != "Unknown":
                date.fromisoformat(due)
            record = dict(id=f"UPDATE-{len(updates)+1:03d}", owner=user["email"], at=now(),
                          purpose=text(body.get("purpose", body.get("next_update")), "purpose/linked issue", 300),
                          channel=text(body.get("channel"), "safe channel", 80),
                          evidence=text(body.get("evidence"), "commitment evidence", 300),
                          next_update=text(body.get("next_update"), "next update commitment", 80),
                          due=due, due_basis=text(body.get("due_basis", "Unknown"), "due-date basis", 300),
                          adjustment_reference=text(body.get("adjustment_reference", "Unknown"), "safe adjustment reference", 80),
                          status="Outstanding", history=[])
            updates.append(record)
        else:
            record = next((r for r in updates if r["id"] == body.get("update_id")), None)
            if record is None:
                raise ValueError("Choose an existing independently owned update commitment.")
            if user["email"] != record["owner"] and user["role"] not in MANAGER_ROLES:
                raise PermissionError("Only the update owner or authorized Programme team can change it.")
            evidence = text(body.get("evidence"), "update action evidence", 300)
            reason = text(body.get("reason"), "update action reason", 300)
            if step == "reassign" and record["status"] != "Sent":
                receiver = self._staff_person(body.get("receiver"))
                if receiver["role"] not in ("Resident Liaison Officer", *MANAGER_ROLES):
                    raise PermissionError("Choose an authorized resident-update owner.")
                record["history"].append(dict(owner=record["owner"], status=record["status"],
                                              by=user["email"], at=now(), evidence=evidence, reason=reason))
                record["owner"] = receiver["email"]
            elif step in ("proposed", "sent") and record["status"] in ("Outstanding", "Proposed"):
                record["status"] = "Proposed" if step == "proposed" else "Sent"
                record["history"].append(dict(step=step, by=user["email"], at=now(), evidence=evidence, reason=reason))
                if step == "sent":
                    record.update(sent_at=now(), sent_evidence=evidence,
                                  receipt="Unknown", understanding="Unknown")
            else:
                raise ValueError("Invalid commitment transition; sending is not resident receipt.")

    def _exercise_assist(self, c: dict, draft: dict, field: str, *,
                         task: str = "form_candidate_selection", claim: str | None = None) -> dict:
        from .decision import DecisionClient, DecisionConfig, InferenceConfig
        if field not in draft["fields"]:
            raise ValueError("Choose an approved field.")
        sources, candidates = [], []
        for candidate in draft["fields"][field]["candidates"]:
            if not candidate["stale"]:
                candidates.append(dict(id=candidate["id"], source_id=candidate["source_id"], text=candidate["raw_value"]))
        source_ids = {candidate["source_id"] for candidate in candidates}
        for sid, source in draft["sources"].items():
            if sid not in source_ids or not source["authorized"] or field not in source["field_ids"]:
                continue
            raw = next(s for s in c["exercise"]["evidence"] if s["id"] == sid)
            excerpt = "\n".join(line for line in raw["raw_text"].splitlines()
                                if line.split(":", 1)[0].strip() == field)
            if not excerpt:
                raise ValueError("Current candidate source lacks its authorized labelled field excerpt.")
            sources.append(dict(id=sid, case_id=c["id"], version=source["version"], hash=source["hash"],
                                locator=f"supplied labelled field {field}; hash binds full source bytes",
                                kind="form_evidence", text=excerpt))
        if "_decision_client" not in self.__dict__:
            config = DecisionConfig(
                endpoint=os.environ.get("PW_DECISION_ENDPOINT", ""),
                deployment=os.environ.get("PW_DECISION_DEPLOYMENT", ""),
                metadata_reviewed=os.environ.get("PW_DECISION_METADATA_REVIEWED") == "true",
                metadata_endpoint=os.environ.get("PW_DECISION_METADATA_ENDPOINT", ""),
                metadata_deployment=os.environ.get("PW_DECISION_METADATA_DEPLOYMENT", ""),
                metadata_model=os.environ.get("PW_DECISION_METADATA_MODEL", ""),
                metadata_model_version=os.environ.get("PW_DECISION_METADATA_MODEL_VERSION", ""),
                deployment_type=os.environ.get("PW_DECISION_DEPLOYMENT_TYPE", ""),
                region=os.environ.get("PW_DECISION_REGION", ""),
            )
            self._decision_client = DecisionClient(config)
        client = DecisionClient(inference=InferenceConfig()) if ai_tasks.workflow_only() else self._decision_client
        return client.propose(task, case_id=c["id"],
            case_version=str(draft["input_version"]), sources=sources, field=field,
            workflow="technical-forms" if draft["form_type"] == "technical" else
                     "invoice-forms" if draft["form_type"] == "invoice" else "funding-forms",
            permissions=("evidence.read", "forms.assist"),
            candidates=candidates if task == "form_candidate_selection" else (),
            claim=claim if task == "evidence_support" else None)

    def _exercise_funding_event(self, user: dict, c: dict, body: dict) -> None:
        from . import forms
        from .controls import text, now
        if user["role"] not in projection.FINANCE_VIEW:
            raise PermissionError("Only Finance identities record external financial evidence.")
        kind = body.get("event")
        prerequisites = {"application-submitted": None, "application-disposition": "application-submitted",
                         "award": "application-disposition", "claimable": "award",
                         "claim-submitted": "claimable", "claim-disposition": "claim-submitted",
                         "cash": "claim-disposition"}
        if kind not in prerequisites:
            raise ValueError("Choose a separate application, award, claim or cash evidence event.")
        fid = body.get("form_id")
        draft = c.get("forms", {}).get(fid)
        if draft is None:
            raise ValueError("Anchor this event to a same-home reviewed form export.")
        current = forms.export_pack(draft)["exports"][-1]
        exported = next((e for e in draft["exports"] if e["id"] == body.get("export_id")), None)
        if exported is None or exported["finance_review"]["digest"] != current["finance_review"]["digest"]:
            raise ValueError("Supply the exact current reviewed export ID; export is not submission.")
        expected = "claim" if kind.startswith("claim") or kind == "cash" else ("competitive", "allocation", "award_return")
        if draft["form_type"] not in (expected if isinstance(expected, tuple) else (expected,)):
            raise ValueError("Wrong template for this financial event.")
        events = c["exercise"].setdefault("fund_events", [])
        previous = next((e for e in reversed(events) if e["event"] == prerequisites[kind]
                         and (prerequisites[kind] == "award" or e["form_id"] == fid)
                         and (body.get("previous_event") is None or e["id"] == body["previous_event"])), None)
        retry = next((e for e in reversed(events) if e["event"] == kind), None)
        if kind in ("application-submitted", "claim-submitted") and retry:
            rejection = next((e for e in events if e["event"] == (
                "application-disposition" if kind == "application-submitted" else "claim-disposition")
                and e["previous_event"] == retry["id"] and e["disposition"] == "Rejected"), None)
            if not rejection and not retry.get("stale"):
                raise ValueError("A resubmission requires its exact rejected disposition reference.")
            if rejection:
                if body.get("retry_of") != rejection["id"]:
                    raise ValueError("A resubmission requires its exact rejected disposition reference.")
                prior_export = next(e for e in c["forms"][retry["form_id"]]["exports"]
                                    if e["id"] == retry["export_id"])
                if (exported["finance_review"]["digest"] == retry["digest"]
                        or (fid == retry["form_id"] and exported["finance_review"]["id"]
                            == prior_export["finance_review"]["id"])):
                    raise ValueError("Re-review and export a corrected pack before resubmitting.")
        if prerequisites[kind] and not previous:
            raise ValueError("Record the preceding external evidence event separately.")
        if previous and previous.get("stale"):
            raise ValueError("Preceding external event depends on stale reviewed evidence; obtain a fresh review and external response.")
        if body.get("previous_event") is not None and (
                previous is None or previous["id"] != body["previous_event"]):
            raise ValueError("The supplied preceding event ID does not match this home and financial state.")
        if kind != "cash" and any(e["event"] == kind and not e.get("stale")
                                 and e["form_id"] == fid and e["export_id"] == exported["id"] for e in events):
            raise ValueError("This external state is already evidenced; do not duplicate it.")
        if kind in ("application-disposition", "claim-disposition") and previous["by"] == user["email"]:
            raise PermissionError("Disposition reviewer must differ from the submission recorder.")
        if kind in ("application-disposition", "award") and previous and previous["form_id"] != fid:
            raise ValueError("Application disposition/award must reference the submitted application's exact form.")
        if previous and prerequisites[kind] != "award" and (
                previous["export_id"] != exported["id"]
                or previous["digest"] != exported["finance_review"]["digest"]):
            raise ValueError("Use the exact preceding reviewed export and digest; changed packs require resubmission.")
        if previous and previous.get("disposition") == "Rejected":
            raise ValueError("Rejected external disposition blocks downstream events.")
        if kind in ("claimable", "claim-submitted", "claim-disposition", "cash") and c["exercise"]["lifecycle"] != "Handover":
            raise ValueError("Accepted same-home handover is required before claim/cash evidence.")
        evidence = text(body.get("evidence"), "fictional external evidence reference", 300)
        amount = None
        if kind in ("award", "claimable", "claim-submitted", "claim-disposition", "cash"):
            try:
                amount = Decimal(str(body.get("amount")))
            except InvalidOperation as error:
                raise ValueError("Supply an explicit finite GBP amount.") from error
            if not amount.is_finite() or amount < 0 or amount > 7500:
                raise ValueError("Exercise amounts must be finite, non-negative and no more than GBP 7500.")
            ceiling = Decimal(str(previous["amount"])) if previous and previous.get("amount") is not None else Decimal("7500")
            reviewed_amount = draft["fields"].get("claim_amount" if draft["form_type"] == "claim" else "grant_amount", {}).get("value")
            if reviewed_amount is not None:
                ceiling = min(ceiling, Decimal(str(reviewed_amount)))
            if amount > ceiling:
                raise ValueError("Amount exceeds the separately evidenced preceding state.")
            if kind == "cash":
                # All receipts belong to this home's single fictional funding opportunity.
                # Staling a claim never reverses externally evidenced cash.
                received = sum(Decimal(e["amount"]) for e in events if e["event"] == "cash")
                if received + amount > ceiling:
                    raise ValueError("Cumulative cash exceeds the accepted claim.")
                if any(e["event"] == "cash" and e["evidence"] == evidence for e in events):
                    raise ValueError("This external receipt reference is already recorded.")
        disposition = body.get("disposition")
        if kind.endswith("disposition") and disposition not in ("Accepted", "Rejected"):
            raise ValueError("Record the supplied external disposition explicitly.")
        events.append(dict(id=f"EVENT-{len(events)+1:03d}", event=kind, form_id=fid,
                           export_id=exported["id"], digest=exported["finance_review"]["digest"],
                           scheme_id=draft["funding"]["scheme_id"], route=draft["funding"]["route"],
                           scheme_version=draft["funding"]["version"], input_version=draft["input_version"],
                           review_id=exported["finance_review"]["id"],
                           by=user["email"], at=now(), evidence=evidence,
                           amount=str(amount) if amount is not None else None, disposition=disposition,
                           previous_event=previous["id"] if previous else None, stale=False,
                           retry_of=body.get("retry_of"),
                           fictional=True, note="Record only; no submission/payment performed."))
        if kind == "award":
            c["funding_ok"] = (c.get("finance", {}).get("budget") or {}).get("status") == "Approved"

    def _exercise_lifecycle(self, user: dict, c: dict, body: dict) -> None:
        if user["role"] not in MANAGER_ROLES:
            raise PermissionError("The Programme team records lifecycle transitions.")
        stages = ("Intake", "Assessment", "Funding", "Ready", "Installation", "Provider completed",
                  "Independent QA", "Handover", "Financial closure")
        current, target = c["exercise"]["lifecycle"], body.get("target")
        if current not in stages or stages.index(current) + 1 >= len(stages) or target != stages[stages.index(current)+1]:
            raise ValueError("Record only the next lifecycle step; approvals cannot be skipped.")
        why = []
        if target == "Funding" and (not c.get("technical") or c["home"]["epc"] == "Unknown"):
            why.append("A versioned design and resolved EPC source are required.")
        if target in ("Ready", "Installation"):
            why += self.exercise_readiness(c)
        orders = [w for w in self._proc()["work_orders"] if w["case_id"] == c["id"]]
        if target == "Installation" and not any(w["state"] in ("Issued", "Appointed") for w in orders):
            why.append("Capacity-backed work order is missing.")
        if target == "Provider completed" and not any(w["state"] == "Completed" for w in orders):
            why.append("Separately recorded provider completion is missing.")
        records = c.get("quality", [])
        if target == "Independent QA" and not records:
            why.append("Provider quality pack is missing.")
        if target == "Handover":
            why += self.exercise_readiness(c)
            if any(not any(r["measure"] == m and r["state"] == "Handed over" for r in records)
                   for m in self._measures(c)):
                why.append("Every measure needs independent QA acceptance and resident handover.")
        if target == "Financial closure":
            from .finance import match_invoice
            why += self.exercise_readiness(c)
            events = c["exercise"].get("fund_events", [])
            claims = [e for e in events if e["event"] == "claim-disposition"
                      and e["disposition"] == "Accepted" and not e.get("stale")]
            cash = sum(Decimal(e["amount"]) for e in events if e["event"] == "cash")
            invoices = c.get("finance", {}).get("invoices", [])
            if not claims or cash != Decimal(claims[-1]["amount"]):
                why.append("Accepted claim and separately received cash must reconcile exactly.")
            if not invoices or any(i["payment_status"] != "Paid outside this system" for i in invoices):
                why.append("Every provider invoice needs independent disposition and external payment evidence.")
            if any(match_invoice(c, invoice) for invoice in invoices):
                why.append("Current invoice/commitment/milestone evidence must still reconcile after re-review.")
            if sum(Decimal(str(ln["amount"])) for i in invoices for ln in i["lines"]) != Decimal("18000"):
                why.append("Provider invoices must reconcile to the fictional GBP 18000 contract.")
        if why:
            raise GateError(why)
        c["exercise"]["lifecycle"] = target
        if target == "Ready":
            c["stage"] = READY_STAGE
        if target == "Financial closure":
            c.update(closed=True, stage="Completed")

    @staticmethod
    def status_line(c):
        if c["closed"]:
            return "Completed"
        open_h = [h for h in c["hazards"] if not h["released"]]
        if open_h:
            return f"Stopped until {open_h[0]['owner']} confirms the safety issue is resolved"
        if c["stage"] == READY_STAGE and not Store.gate_reasons(c):
            return "Ready"
        return f"Waiting on {c['waiting_on']} {c['reason']}"

    def summary(self, c):
        last = c["contacts"][-1]["at"] if c["contacts"] else None
        nxt = next((a for a in c["appointments"] if a["outcome"] == "Booked"), None)
        return dict(id=c["id"], resident=c["resident"]["name"], address=c["home"]["address"],
                    town=c["home"]["town"], postcode=c["home"]["postcode"], phone=c["resident"]["phone"],
                    stage=c["stage"], status=self.status_line(c), owner=c["owner"], days=c["days_in_stage"],
                    last_contact=last, next_visit=nxt["date"] if nxt else None, area=c["home"]["area"],
                    wave=c["wave"], funding=c["funding"]["status"], owner_code=c["owner_code"],
                    hazard=any(not h["released"] for h in c["hazards"]),
                    support=c["resident"]["priority_support"] or c["resident"]["adjustment"] != "None",
                    closed=c["closed"])

    def _ranking(self):
        """Ranking of all open cases for the current policy, rebuilt only when case data changes."""
        if self._ranks is None or self._ranks[0] != self.version:
            entries = ranking.rank([c for c in self.cases.values() if not c["closed"]], ranking.CURRENT)
            self._ranks = (self.version, {e["id"]: e for e in entries})
        return self._ranks[1]

    def ranking_policy(self):
        return ranking.describe(ranking.CURRENT)

    def ranking_snapshot(self, user, policy=None):
        """Snapshot of the open-case ranking under a policy version, stored beside the data when it changes. Managers only."""
        if user["role"] not in MANAGER_ROLES:
            raise PermissionError("Only a manager can see the ranking snapshot.")
        pol = ranking.POLICIES.get(policy or ranking.CURRENT["version"])
        if pol is None:
            raise ValueError(f"Unknown ranking policy version. Known: {', '.join(sorted(ranking.POLICIES))}")
        with self.lock:
            cache = self.__dict__.setdefault("_snapcache", {})
            hit = cache.get(pol["version"])
            if hit and hit[0] == self.version:
                return hit[1]
            snap = ranking.snapshot([c for c in self.cases.values() if not c["closed"]], pol, self.as_of)
            cache.clear()
            cache[pol["version"]] = (self.version, snap)
            path = os.path.join(os.path.dirname(getattr(self, "live_path", None) or self.db_path) or ".", f"ranking-snapshot-{pol['version']}.json")
            text = ranking.canonical(snap)
            try:
                with open(path, encoding="utf-8") as f:
                    same = f.read() == text
            except OSError:
                same = False
            if not same:
                with open(path + ".tmp", "w", encoding="utf-8") as f:
                    f.write(text)
                os.replace(path + ".tmp", path)
            return snap

    def _filtered(self, user, view, q, f):
        if view == "closed":
            if user["role"] not in MANAGER_ROLES:
                raise PermissionError("Only a manager can see closed cases.")
            return sorted((c for c in self.cases.values() if c["closed"] and insights.matches(c, f)), key=lambda c: c["id"])
        rows = [c for c in self.cases.values() if not c["closed"] and insights.matches(c, f)]
        if projection.is_contractor(user):
            rows = [c for c in rows if projection.own_case(user, c)]
        elif view == "mine":
            rows = [c for c in rows if c["owner_code"] == user["code"]]
        if q:
            ql = q.lower()
            # a contractor cannot search on the resident's name: that would reveal who lives where
            fields = (lambda c: [c["home"]["address"], c["home"]["postcode"], c["id"]]) if projection.is_contractor(user) \
                else (lambda c: [c["resident"]["name"], c["home"]["address"], c["home"]["postcode"], c["id"]])
            rows = [c for c in rows if ql in " ".join(fields(c)).lower()]
        return rows

    def page_cases(self, user, view="mine", q="", filters=None, sort="urgent", limit=None, offset=0, after=None):
        """One page of the filtered, sorted list plus the total. limit None returns everything."""
        with self.lock:
            ranks = self._ranking()
            rows = self._filtered(user, view, q, filters or {})
            total = len(rows)
            if view == "closed":
                page = rows if limit is None else rows[offset:offset + limit]
                return dict(items=[self.summary(c) for c in page], total=total, limit=limit, offset=offset, sort="id",
                            policy_version=ranking.CURRENT["version"], policy_hash=ranking.CURRENT["content_hash"], as_of=self.as_of, ranked_total=len(ranks))
            if sort in ("urgent", "", None) or sort not in insights.SORTS:
                rows.sort(key=lambda c: ranks[c["id"]]["rank"])
                if after:
                    rows = [c for c in rows if ranking.sql_key(c) > after]
                    offset = 0
                page = rows if limit is None else rows[offset:offset + limit]
                out = [self.summary(c) for c in page]
            else:
                out = [self.summary(c) for c in rows]
                for r in out:
                    r["rank"] = ranks[r["id"]]["rank"]
                out.sort(key=lambda r: (insights.sort_key(sort)(r), r["rank"]))
                page = None
                if limit is not None:
                    out = out[offset:offset + limit]
                by_id = self.cases
                page = [by_id[r["id"]] for r in out]
            for i, (r, c) in enumerate(zip(out, page)):
                e = ranks[c["id"]]
                r["rank"], r["reasons"] = e["rank"], e["reasons"]
                if projection.is_contractor(user):
                    r.pop("reasons")
                    out[i] = projection.contractor_summary(c, r)
                elif view == "mine":
                    r["focus"] = self.focus(c, user["role"], projection.can_see_reason(user))
            nxt = ranking.sql_key(page[-1]) if limit is not None and page and (sort in ("urgent", "", None) or sort not in insights.SORTS) and len(page) == limit else None
            return dict(items=out, total=total, limit=limit, offset=offset, sort=sort,
                        policy_version=ranking.CURRENT["version"], policy_hash=ranking.CURRENT["content_hash"], as_of=self.as_of, ranked_total=len(ranks), next_cursor=nxt)

    def list_cases(self, user, view="mine", q="", filters=None, sort="urgent"):
        return self.page_cases(user, view, q, filters, sort)["items"]

    def focus(self, c, role, reason_ok=True):
        """Role-specific facts for the card, as label/value pairs."""
        nxt = next((a for a in c["appointments"] if a["outcome"] == "Booked"), None)
        open_h = [h for h in c["hazards"] if not h["released"]]
        ev = {d["kind"] for d in c["documents"]}
        missing = [k for k in self.EVIDENCE if k not in ev]
        rs = c["resident"]
        if role == "Resident Liaison Officer":
            return [("Resident prefers", rs["preferred"]),
                    ("Extra support", "Yes" if rs["priority_support"] else (rs["adjustment"] if rs["adjustment"] != "None" else "None recorded")),
                    ("Decision on works", c["decision"]["status"]),
                    ("Next visit", nxt["date"] if nxt else "None booked")]
        if role == "Retrofit Coordinator":
            return [("Contractor", c["contractor"]["name"]), ("Works", c["measures"]),
                    ("Next visit", nxt["date"] if nxt else "None booked")]
        if role == "Building Safety Liaison":
            return [("Open safety issues", "; ".join(f"{h['category']} ({h['owner']})" for h in open_h) or "None"),
                    ("Works", c["measures"])]
        if role == "Grants and Evidence Officer":
            return [("Funding", f"{c['funding']['route']}, {c['funding']['status']}"),
                    ("Evidence missing", ", ".join(missing) or "Nothing missing")]
        if role == "Quality Inspector":
            return [("Works", c["measures"]), ("Contractor", c["contractor"]["name"]),
                    ("Stage", c["stage"])]
        return [("Wave", c["wave"]), ("Funding", c["funding"]["status"]),
                ("Decision on works", c["decision"]["status"]), ("Contractor", c["contractor"]["name"])]

    def counts(self, user):
        with self.lock:
            mine = [c for c in self.cases.values() if not c["closed"] and c["owner_code"] == user["code"]]
            return dict(mine=len(mine), hazards=sum(any(not h["released"] for h in c["hazards"]) for c in mine),
                        open=sum(not c["closed"] for c in self.cases.values()))

    def detail(self, case_id, user=None):
        """Case card. Pass the signed-in user so the role's projection is applied; None returns everything (internal use)."""
        with self.lock:
            c = self.cases.get(case_id)
            if not c or (user is not None and projection.is_contractor(user) and not projection.own_case(user, c)):
                return None
            d = json.loads(json.dumps(c))
            d["status"] = self.status_line(c)
            d["gate"] = self.gate_reasons(c)
        d["can_advance"] = c["stage"] == READY_STAGE
        d["suggestions"] = insights.recommend_handover(c, list(self.cases.values()), self.data["staff"])
        d["checklist"] = self.checklist(c)
        d["technical_missing"] = missing_items(c)
        d["measure_decisions"] = measure_decision_view(c)
        d["contacts"] = list(reversed(d["contacts"]))[:40]
        if user is None:
            return d
        if projection.is_contractor(user):
            return projection.contractor_detail(c, d)
        return projection.redact_staff_detail(user, d)

    def log_call(self, user, case_id, outcome, note, channel="Phone"):
        outcome = (outcome or "").strip()[:80]
        if not outcome:
            raise ValueError("Say how the call went.")
        with self.lock:
            c = self._case(case_id)
            c["contacts"].append(dict(at=datetime.now().isoformat(timespec="minutes"), purpose="Update",
                                      channel=channel, direction="Outbound", outcome=outcome,
                                      note=(note or "")[:500], by=user["name"]))
            self.audit(user["email"], "log_contact", case_id, outcome)
            self.save()

    def set_decision(self, user, case_id, status, note=""):
        if status not in DECISIONS:
            raise ValueError("Choose one of the listed answers.")
        with self.lock:
            c = self._case(case_id)
            c["decision"] = dict(status=status, by=user["name"], at=datetime.now().date().isoformat())
            if c.get("exercise"):
                c["decision"]["note"] = "Legacy whole-home record only; never satisfies scoped exercise readiness."
            self.audit(user["email"], "resident_decision", case_id, f"{status} {note}".strip())
            self.save()

    def hand_over(self, user, case_id, to_email, note=""):
        to = self.staff.get((to_email or "").lower())
        if not to:
            raise ValueError("Choose who is taking this over.")
        with self.lock:
            c = self._case(case_id)
            if c.get("exercise"):
                raise PermissionError("Offer a handoff and wait for receiver acceptance.")
            c.update(owner=to["name"], owner_code=to["code"], owner_role=to["role"], waiting_on=to["name"])
            self.audit(user["email"], "hand_over", case_id, f"to {to['name']} {note}".strip())
            self.save()

    def advance(self, user, case_id):
        with self.lock:
            c = self._case(case_id)
            if c.get("exercise"):
                raise PermissionError("Use capacity-backed exercise lifecycle transitions.")
            if c["stage"] != READY_STAGE:
                raise ValueError("This case is not at the final checks.")
            why = self.gate_reasons(c)
            if why:
                raise GateError(why)
            c.update(stage=BOOKED_STAGE, reason="to book the installation", waiting_on=c["contractor"]["contact"])
            self.audit(user["email"], "advance", case_id, BOOKED_STAGE)
            self.save()

    def draft(self, case_id, kind):
        with self.lock:
            c = self._case(case_id)
        r = c["resident"]
        who = r["representative"]["name"] if r["representative"] else r["formal"]
        if kind == "visit":
            avoid = f", outside {r['unavailable']}" if r["unavailable"] else ""
            body = (f"Dear {who},\n\nWe would like to arrange a visit to {c['home']['address']} to talk through "
                    f"improvements to your home. Please let us know a day and time that suits you{avoid}.\n\n"
                    f"Kind regards,\n{c['owner']}\nProper North Homes")
        else:
            body = (f"Dear {who},\n\nA quick update on the work to {c['home']['address']}: it is currently at "
                    f"'{c['stage'].lower()}'. {c['owner']} is your contact and will be in touch with the next "
                    f"step.\n\nKind regards,\n{c['owner']}\nProper North Homes")
        return dict(text=body, note="Draft for you to read and change. Nothing is sent until you send it.")

    # ---- insight views
    def facets(self):
        with self.lock:
            return insights.facets(list(self.cases.values()))

    def stats(self):
        with self.lock:
            return insights.stats(list(self.cases.values()), self.data["staff"])

    def map_points(self, f):
        with self.lock:
            return insights.map_points(list(self.cases.values()), f)

    def map_view(self, f, bbox=None, zoom=None):
        with self.lock:
            return insights.map_view(self.cases.values(), f, bbox, zoom)

    def visits(self, user, view="mine"):
        with self.lock:
            own = None if view == "all" else user["code"]
            return insights.visits(list(self.cases.values()), own)

    # ---- documents
    EVIDENCE = ("EPC", "Survey", "Design", "Consent")
    EXT = ACCEPTED
    KINDS = ("EPC", "Survey", "Design", "Consent", "Funding evidence", "Photo", "Other")
    MAX_BYTES = MAX_BYTES

    @staticmethod
    def checklist(c):
        have = {d["kind"] for d in c["documents"]}
        return [dict(kind=k, present=k in have) for k in Store.EVIDENCE]

    def _doc_role(self, user, what):
        if user is not None and user.get("role") not in projection.STAFF_ROLES:
            raise PermissionError(f"Your role cannot {what} documents.")

    def add_document(self, user, case_id, name, kind, data):
        self._doc_role(user, "add")
        name = os.path.basename((name or "").strip())[:120]
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
        if ext not in self.EXT:
            raise ValueError("That file type is not accepted. Use pdf, png, jpg, docx, xlsx, csv or txt.")
        if not data or len(data) > self.MAX_BYTES:
            raise ValueError("Files must be between 1 byte and 5 MB.")
        kind = kind if kind in self.KINDS else "Other"
        mime = self.EXT[ext]
        with self.lock:
            c = self._case(case_id)
            did = uuid.uuid4().hex[:12]
            try:
                self.docstore.put(case_id, did, data, mime)
            except DocumentStoreError as e:
                self.audit(user["email"], "upload_document_failed", case_id, f"{kind}: {name}: {e}")
                raise
            doc = dict(id=did, name=name, kind=kind, at=datetime.now().date().isoformat(), by=user["name"],
                       generated=False, mime=mime, summary="")
            c["documents"].append(doc)
            self.audit(user["email"], "upload_document", case_id, f"{kind}: {name}")
            try:
                self.save()
            except BaseException:
                try:
                    self.docstore.delete(case_id, did)
                except DocumentStoreError:
                    pass
                raise
        return doc

    def read_document(self, user, case_id, doc_id, mode=None):
        self._doc_role(user, "read")
        with self.lock:
            c = self._case(case_id)
            doc = next((d for d in c["documents"] if d["id"] == doc_id and not d["generated"]), None)
            if not doc:
                raise KeyError(doc_id)
            data = self.docstore.get(case_id, doc_id)
        self.audit(user["email"], "ai_run_start", case_id, f"read_document {doc['name']}")
        r = ai_tasks.run_document(self, user, case_id, doc, data, mode)
        with self.lock:
            doc = next(d for d in self._case(case_id)["documents"] if d["id"] == doc_id)
            doc["summary"] = r["text"]
            self.audit(user["email"], "ai_run_end", case_id, f"read_document source={r['source']} model={r['model']}")
            self.save()
        return r

    def get_document(self, case_id, doc_id, user=None):
        """Bytes of one document. Pass the signed-in user so the role is checked and the download is audited."""
        self._doc_role(user, "download")
        with self.lock:
            c = self._case(case_id)
            doc = next((d for d in c["documents"] if d["id"] == doc_id), None)
            if not doc:
                raise KeyError(doc_id)
            if doc["generated"]:
                text = (f"{doc['name']}\nCase {c['id']}: {c['home']['address']}, {c['home']['postcode']}\n"
                        f"Filed {doc['at']} by {doc['by']}\nType: {doc['kind']}\n")
                return doc["name"].rsplit(".", 1)[0] + ".txt", "text/plain", text.encode()
            data = self.docstore.get(case_id, doc_id)
            if user is not None:
                self.audit(user["email"], "download_document", case_id, f"{doc['kind']}: {doc['name']}")
            return doc["name"], doc["mime"], data

    # ---- AI drafting (always a draft for a person)
    def _facts(self, c, reason_ok=False):
        r = c["resident"]
        adjust = r["adjustment"] if reason_ok else ("extra support needed" if projection.needs_notice(c) else "None")
        return (f"Case {c['id']}. Resident: {r['name']}. Home: {c['home']['address']}, {c['home']['town']}. "
                f"Stage: {c['stage']} for {c['days_in_stage']} days. Waiting on {c['waiting_on']} {c['reason']}. "
                f"Resident adjustments: {adjust}. Resident prefers: {r['preferred']}. "
                f"Resident decision: {c['decision']['status']}. Funding: {c['funding']['route']} ({c['funding']['status']}). "
                f"Open safety issues: {sum(not h['released'] for h in c['hazards'])}. "
                f"Recent contacts: " + "; ".join(f"{k['at'][:10]} {k['outcome']}" for k in c["contacts"][-4:]))

    def ai_run(self, user, case_id, task, mode=None):
        with self.lock:
            c = self._case(case_id)
            facts = self._facts(c, projection.can_see_reason(user))
            fallback = self.draft(case_id, "visit" if task == "message" else "update")["text"]
            summary = self.status_line(c)
            owner, who = c["owner"], c["resident"]["name"]
            case = c
            tcites = ai_tasks.cites_for(c, "Stage:", "Preferred contact:", "Unavailable:", reason_ok=projection.can_see_reason(user)) if task == "message" else \
                ai_tasks.cites_for(c, "Stage:", "Waiting on:", "Open safety issues:")
        sysmsg = ("You assist a UK housing association retrofit team. Use only the facts given. Never invent dates, amounts, "
                  "names or promises. Never say anything has been sent. Plain English, short, warm, no jargon.")
        prompts = {
            "message": ("Draft a short letter or email from " + owner + " to the resident offering to arrange a visit or giving an "
                        "update, respecting their adjustments and preferred contact. Sign off with the officer's name.", fallback, False),
            "summary": ("Catch up a colleague taking over this case in at most 5 short bullets: where it is, what is stuck, "
                        "what to do next, anything about the resident they must know.", summary, False),
        }
        if task not in prompts:
            raise ValueError("Unknown request.")
        instr, tmpl, strong = prompts[task]
        self.audit(user["email"], "ai_run_start", case_id, task)
        r = ai_tasks.run_text_task(self, user, task, [case], sysmsg, instr + "\n\nFacts:\n" + facts, tmpl, tcites, strong, mode=mode,
                                   bullets=task == "summary")
        self.audit(user["email"], "ai_run_end", case_id, f"{task} source={r['source']} model={r['model']} validated={r['validated']} verified={r['verified']}")
        return dict(r, label=("AI-drafted, for you to check" if r["source"] == "ai" else "Template draft, for you to check")
                    + ("" if r["verified"] else ". Unverified: its sources do not match the case record"))

    def briefing(self, user, mode=None):
        off = ai_tasks.workflow_only(mode)
        with self.lock:
            hit = self._briefings.get((user["code"], off))
            if hit and hit[0] == self.version:
                return hit[1]
            ver = self.version
            mine = [c for c in self.cases.values() if not c["closed"] and c["owner_code"] == user["code"]]
            ranks = self._ranking()
            mine.sort(key=lambda c: ranks[c["id"]]["rank"])
            top = mine[:8]
            facts = "\n".join(f"{c['id']} {c['resident']['name']}: {c['stage']}, {c['days_in_stage']} days. {self.status_line(c)}" for c in top)
            tmpl = "Start with: " + "; ".join(f"{c['resident']['name']} ({c['stage'].lower()}, {c['days_in_stage']} days)" for c in top[:3]) if top else "No open cases."
        r = ai_tasks.run_text_task(self, user, "briefing", top, "You write a friendly three-sentence morning briefing for a housing officer. "
                                   "Use only the facts. Safety issues first, then longest waits. No invented facts.", facts, tmpl,
                                   [x for c in top[:3] for x in [f"{c['id']}: Stage: {c['stage']}", f"{c['id']}: Days in stage: {c['days_in_stage']}"]],
                                   mode=mode)
        self.audit(user["email"], "ai_run", "-", f"briefing source={r['source']} model={r['model']} verified={r['verified']}")
        out = dict(r, label=("AI-drafted" if r["source"] == "ai" else "Summary by rules")
                   + ("" if r["verified"] else ". Unverified: its sources do not match the case record"))
        with self.lock:
            if self.version - ver <= 1:  # only our own comparison record was saved meanwhile
                self._briefings[(user["code"], off)] = (self.version, out)
        return out

    # ---- AI priority recommendation: advice beside the deterministic order, never part of it
    REC_LABEL = "AI-drafted, human-approved"
    REC_ACTIONS = {"accept": "Accepted", "edit": "Edited", "reject": "Rejected"}

    def _rec_view(self, rec):
        ranks = self._ranking()
        def row(cid, reason=None, cites=None):
            c = self.cases[cid]
            r = dict(case_id=cid, resident=c["resident"]["name"], address=c["home"]["address"], stage=c["stage"],
                     rank=ranks[cid]["rank"] if cid in ranks else None)
            if reason is not None:
                r["reason"] = reason
                r["cites"] = cites or []
            return r
        return dict(rec, label=self.REC_LABEL,
                    items=[row(i["case_id"], i["reason"], i.get("cites")) for i in rec["items"]],
                    final_items=[row(i["case_id"], i["reason"], i.get("cites")) for i in rec["final_items"]] if rec.get("final_items") is not None else None,
                    deterministic=[row(cid) for cid in rec["deterministic"]])

    def ai_priority(self, user, n=5, mode=None):
        n = max(1, min(10, int(n)))
        with self.lock:
            ranks = self._ranking()
            mine = sorted((c for c in self.cases.values() if not c["closed"] and c["owner_code"] == user["code"]),
                          key=lambda c: ranks[c["id"]]["rank"])
            if not mine:
                raise ValueError("You have no open cases to prioritise.")
            det = [c["id"] for c in mine[:n]]
            cand = mine[:40]
            ids = {c["id"] for c in cand}
            ok = projection.can_see_reason(user)
            facts = "\n".join(f"{c['id']}: {self._facts(c, ok)}" for c in cand)
            sources = {c["id"]: ai_tasks.source_labels(c, ok) for c in cand}
            hazard_ids = [c["id"] for c in cand if any(not h["released"] for h in c["hazards"])]
            tmpl_items = self._heuristic_priority(cand, n, ok)
            policy_version = ranking.CURRENT["version"]
        tmpl = json.dumps(tmpl_items)
        sysmsg = ("You advise a UK housing association retrofit officer which of their cases to work on first today. You only "
                  "recommend; a person decides. Use only the facts given and only the case ids listed. Never invent facts. "
                  f"Reply with JSON only: a list of exactly {n} objects with keys case_id and reason (one short plain sentence "
                  "citing a fact such as an open safety issue, extra support need, days waiting or a missing resident decision) and "
                  "cites, a list of the facts it relies on copied exactly from that case's citable facts. Always include every case "
                  "with an open safety issue.")

        def valid(text):
            items, _, err = ai_tasks.priority_items(text, n, sources)
            return err is None and not ai_tasks.critical_misses([i["case_id"] for i in items], hazard_ids, n)
        self.audit(user["email"], "ai_run_start", "-", f"priority_recommendation n={n}")
        r = self.ai.run("priority", sysmsg, f"Pick the top {n}.\n\nCases:\n{facts}", tmpl, True, check=valid,
                        off=ai_tasks.workflow_only(mode))
        items, dropped = None, 0
        if r["source"] == "ai":
            items, dropped, _ = ai_tasks.priority_items(r["text"], n, sources)
        if items is None:
            items = tmpl_items
        with self.lock:
            rec = dict(id=uuid.uuid4().hex[:12], user=user["email"], created=datetime.now().isoformat(timespec="seconds"),
                       status="Proposed", source=r["source"], model=r["model"], validated=r["validated"], n=n,
                       items=items, deterministic=det, policy_version=policy_version, final_items=None,
                       resolved_by=None, resolved_at=None, reason="", workflow_items=tmpl_items, ai_output=r.get("ai_text") or (r["text"] if r["source"] == "ai" else None),
                       fallback_reason=r.get("reason"), latency_ms=r.get("latency_ms"), prompt_version=ai_tasks.PROMPT_VERSION,
                       mode="workflow-only" if r.get("reason") == "workflow-only mode selected" else "ai", dropped_uncited=dropped,
                       case_ids=[c["id"] for c in cand], hazard_ids=hazard_ids,
                       overlap=len({i["case_id"] for i in items} & set(det)))
            self.data["recommendations"].append(rec)
            self.audit(user["email"], "ai_run_end", "-", f"priority_recommendation {rec['id']} source={r['source']} model={r['model']} validated={r['validated']}")
            self.save()
            return self._rec_view(rec)

    def _heuristic_priority(self, cand, n, ok=False):
        """Template used when no model is available: a different, simpler view from the ranking policy."""
        def score(c):
            s = 0
            s += 100 if any(not h["released"] for h in c["hazards"]) else 0
            s += 30 if c["resident"]["priority_support"] or c["resident"]["adjustment"] != "None" else 0
            s += 20 if c["decision"]["status"] in ("Not yet asked", "Waiting") else 0
            return s + min(c["days_in_stage"], 120) / 4
        out = []
        for c in sorted(cand, key=lambda c: (-score(c), c["id"]))[:n]:
            why = []
            if any(not h["released"] for h in c["hazards"]):
                why.append("an open safety issue")
            if c["resident"]["priority_support"] or c["resident"]["adjustment"] != "None":
                why.append("the resident needs extra support")
            if c["decision"]["status"] in ("Not yet asked", "Waiting"):
                why.append("no resident decision yet")
            why.append(f"{c['days_in_stage']} days at '{c['stage'].lower()}'")
            out.append(dict(case_id=c["id"], reason="Because of " + ", ".join(why) + ".",
                            cites=ai_tasks.cites_for(c, "Open safety issues:", "Extra support:", "Resident decision:", "Days in stage:", "Stage:", reason_ok=ok)))
        return out

    def latest_priority(self, user):
        with self.lock:
            mine = [r for r in self.data["recommendations"] if r["user"] == user["email"] and r.get("kind") != "ai_task"]
            return self._rec_view(mine[-1]) if mine else None

    def resolve_priority(self, user, rec_id, action, reason="", items=None):
        if action not in self.REC_ACTIONS:
            raise ValueError("Choose accept, edit or reject.")
        reason = (reason or "").strip()[:300]
        if action in ("edit", "reject") and not reason:
            raise ValueError("Say why.")
        with self.lock:
            rec = next((r for r in self.data["recommendations"] if r["id"] == rec_id and r.get("kind") != "ai_task"), None)
            if not rec:
                raise KeyError(rec_id)
            if rec["user"] != user["email"]:
                raise PermissionError("This suggestion was made for someone else.")
            if rec["status"] != "Proposed":
                raise ValueError("This suggestion has already been answered.")
            final = None
            if action == "accept":
                final = rec["items"]
            elif action == "edit":
                mine = {c["id"] for c in self.cases.values() if not c["closed"] and c["owner_code"] == user["code"]}
                final = []
                for i in items or []:
                    cid = i.get("case_id") if isinstance(i, dict) else None
                    if cid not in mine or any(f["case_id"] == cid for f in final):
                        raise ValueError("Choose each of your own open cases at most once.")
                    final.append(dict(case_id=cid, reason=str(i.get("reason", ""))[:300]))
                if not final or len(final) > 10:
                    raise ValueError("Keep between 1 and 10 cases.")
            rec.update(status=self.REC_ACTIONS[action], final_items=final, reason=reason,
                       resolved_by=user["email"], resolved_at=datetime.now().isoformat(timespec="seconds"))
            ids = ",".join(i["case_id"] for i in final) if final else "-"
            self.audit(user["email"], f"ai_priority_{action}", "-", f"{rec_id} {reason} cases={ids}".strip())
            self.save()
            return self._rec_view(rec)

    # ---- funding: a person approves and submits; the system never does
    FUND_FLOW = ("Not started", "To prepare", "Draft ready", "Approved", "Submitted", "Confirmed")
    FUND_ROLES = ("Grants and Evidence Officer",) + MANAGER_ROLES

    def funding_list(self, user):
        with self.lock:
            out = []
            for c in self.cases.values():
                if c["closed"] or c["funding"]["status"] == "Confirmed":
                    continue
                cl = self.checklist(c)
                out.append(dict(id=c["id"], resident=c["resident"]["name"], address=c["home"]["address"], area=c["home"]["area"],
                                route=c["funding"]["route"], status=c["funding"]["status"], owner=c["owner"],
                                have=sum(x["present"] for x in cl), need=len(cl), days=c["days_in_stage"],
                                grants=grant_summary(c)))
        order = {s: i for i, s in enumerate(self.FUND_FLOW)}
        out.sort(key=lambda x: (order[x["status"]] == 0, -x["days"]))
        return out

    def funding_draft(self, user, case_id, mode=None):
        with self.lock:
            c = self._case(case_id)
            missing = [x["kind"] for x in self.checklist(c) if not x["present"]]
            facts = self._facts(c, projection.can_see_reason(user)) + f" Built: {c['home']['built']}. Type: {c['home']['type']}. EPC band: {c['home']['epc']}. " \
                f"Measures: {', '.join(c['measures']) if isinstance(c['measures'], list) else c['measures']}."
            route = c["funding"]["route"]
            case = c
            tcites = ai_tasks.cites_for(c, "Address:", "Home type:", "EPC band:", "Built:", "Measures:", "Funding route:")
            tmpl = (f"Funding application draft for {c['home']['address']} ({route})\n\nProperty: {c['home']['type']}, built "
                    f"{c['home']['built']}, EPC {c['home']['epc']}.\nProposed measures: {c['measures']}.\n\n"
                    + "\n".join(f"Needs: {m} document" for m in missing) + "\nNeeds: costs from the contractor\nNeeds: eligibility check by the Grants Officer")
        sysmsg = ("You draft the narrative part of a social housing retrofit funding application. Use only the facts given. Do not invent "
                  "costs, eligibility results or evidence. Where something is missing write 'Needs: ...'. Headings: Property, Proposed work, "
                  "Evidence held, Evidence still needed. Under 250 words.")
        self.audit(user["email"], "ai_run_start", case_id, "funding_draft")
        r = ai_tasks.run_text_task(self, user, "funding_draft", [case], sysmsg,
                                   f"Route: {route}\n{facts}\nMissing documents: {', '.join(missing) or 'none'}", tmpl, tcites, True,
                                   check=lambda t: all(m.lower() in t.lower() for m in missing) or "needs" in t.lower(), mode=mode)
        with self.lock:
            c = self._case(case_id)
            c["funding"]["draft"] = r["text"]
            if c["funding"]["status"] in ("Not started", "To prepare"):
                c["funding"]["status"] = "Draft ready"
            self.audit(user["email"], "ai_run_end", case_id, f"funding_draft source={r['source']} model={r['model']}")
            self.save()
        return dict(r, label="AI-drafted, human-approved: nothing is submitted until a person approves and submits it"
                    + ("" if r["verified"] else ". Unverified: its sources do not match the case record"))

    # ---- review of any AI output, the comparison records and the live report
    def review_ai(self, user, rec_id, action, reason="", text=None):
        return ai_tasks.review(self, user, rec_id, action, reason, text)

    def ai_live_report(self):
        return ai_tasks.live_report(self)

    def funding_step(self, user, case_id, action, text=""):
        if user["role"] not in self.FUND_ROLES:
            raise PermissionError("Only the Grants and Evidence Officer or a manager can do this.")
        with self.lock:
            c = self._case(case_id)
            if c.get("exercise"):
                raise PermissionError("Use separate reviewed forms and external financial evidence events.")
            f = c["funding"]
            if action == "save_draft":
                f["draft"] = (text or "")[:6000]
            elif action == "approve":
                if f["status"] != "Draft ready" or not f["draft"].strip():
                    raise ValueError("Write or generate a draft first.")
                missing = [x["kind"] for x in self.checklist(c) if not x["present"]]
                if missing:
                    raise GateError([f"Missing evidence: {', '.join(missing)}"])
                f.update(status="Approved", approved_by=user["name"])
            elif action == "submit":
                if f["status"] != "Approved":
                    raise ValueError("Approve the draft first.")
                ref = (text or "").strip()[:60]
                if not ref:
                    raise ValueError("Enter the reference the funder gave you.")
                f.update(status="Submitted", reference=ref)
            elif action == "confirm":
                if f["status"] != "Submitted":
                    raise ValueError("Record the submission first.")
                f["status"] = "Confirmed"
                c["funding_ok"] = True
            else:
                raise ValueError("Unknown step.")
            self.audit(user["email"], f"funding_{action}", case_id, f["status"])
            self.save()

    def _case(self, case_id):
        c = self.cases.get(case_id)
        if not c:
            raise KeyError(case_id)
        self._touch(case_id)
        return c

    def export_csv(self, rows):
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["Reference", "Resident", "Address", "Town", "Postcode", "Phone", "Stage", "Status",
                    "Owner", "Days in stage", "Last contact", "Next visit"])
        for s in rows:
            w.writerow([s["id"], s["resident"], s["address"], s["town"], s["postcode"], s["phone"], s["stage"],
                        s["status"], s["owner"], s["days"], s["last_contact"] or "", s["next_visit"] or ""])
        return buf.getvalue()

    def import_check(self, text):
        """Forgiving check of any spreadsheet export: map columns, report rows to fix, change nothing."""
        rows = list(csv.reader(io.StringIO(text)))
        if not rows:
            raise ValueError("The file is empty.")
        head = [h.strip() for h in rows[0]]
        guess = {"name": r"name|resident|tenant", "address": r"address|street|property",
                 "postcode": r"post ?code|postal", "phone": r"phone|mobile|tel"}
        mapping = {k: next((i for i, h in enumerate(head) if re.search(p, h, re.I)), None) for k, p in guess.items()}
        known = {c["home"]["postcode"].replace(" ", "").upper() for c in self.cases.values()}
        good, fix, matched = 0, [], 0
        for n, r in enumerate(rows[1:], start=2):
            def cell(k):
                i = mapping[k]
                return r[i].strip() if i is not None and i < len(r) else ""
            problems = [k for k in ("name", "address", "postcode") if not cell(k)]
            pc = cell("postcode")
            if pc and not re.fullmatch(r"[A-Za-z]{1,2}\d[A-Za-z\d]? ?\d[A-Za-z]{2}", pc):
                problems.append("postcode looks wrong")
            if pc.replace(" ", "").upper() in known:
                matched += 1
            if problems:
                fix.append(dict(row=n, problem="Check " + ", ".join(problems)))
            else:
                good += 1
        found = {k: (head[i] if i is not None else None) for k, i in mapping.items()}
        return dict(columns=found, ready=good, to_fix=fix[:50], matched_existing=matched,
                    message="Your file has not been changed.")
