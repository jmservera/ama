"""Case store: loading, views, actions, gates and the hash-chained audit log."""
import csv
import hashlib
import io
import json
import os
import re
import threading
import uuid
from datetime import datetime

from . import ai_tasks, buildings, insights, ledger, projection, ranking
from .finance import FinanceMixin
from .continuity import ContinuityMixin
from .governance import GovernanceMixin
from .grants import GrantMixin, grant_summary
from .resident_decisions import ResidentDecisionMixin, measure_decision_view
from .signoffs import SignoffMixin, missing_items, technical_gate
from zava_forward.core.ai import Ai
from .chatthreads import ChatMixin
from .doc_controls import DocControlsMixin, open_scanner
from .documents import ACCEPTED, MAX_BYTES, DocumentStoreError, open_document_store
from .procurement import ProcurementMixin
from .quality import QualityMixin
from .workflows import MANAGER_ROLES, WorkflowMixin, handoff_view, hazard_view

DECISIONS = ("Not yet asked", "Waiting", "Accepted", "Declined")
READY_STAGE = "Final checks before ordering"
BOOKED_STAGE = "Install booked"


class GateError(Exception):
    def __init__(self, reasons):
        super().__init__("; ".join(reasons))
        self.reasons = reasons


class ConflictError(Exception):
    """Another writer changed the same record first, so this write was refused."""


class Store(ChatMixin, WorkflowMixin, QualityMixin, ProcurementMixin, FinanceMixin, GrantMixin, SignoffMixin, ResidentDecisionMixin, GovernanceMixin, ContinuityMixin, DocControlsMixin):
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
        self.digest_dir = os.environ.get("ZF_DIGEST_DIR") or os.path.join(base, "digests")
        self.docs_dir = os.path.join(os.path.dirname(self.live_path), "docs")
        self.docstore = open_document_store(self.docs_dir)
        self.scanner = open_scanner(self.docstore)
        self.ai = Ai()
        self.ai.gate = lambda task, deployment=None: self.continuity_block(task)
        self.version = 0
        self._briefings = {}
        self._ranks = None
        self.data.setdefault("recommendations", [])
        self.as_of = self.data.setdefault("as_of", os.environ.get("ZF_AS_OF") or datetime.now().date().isoformat())

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

    def verify_ledger_by_year(self):
        return ledger.verify_years(self.audit_entries(), ledger.read_year_digests(self.digest_dir))

    def write_year_digests(self):
        """Seal every year before the current one. Sealed years are written once and never overwritten."""
        with self.lock:
            return [ledger.write_year_digest(self.digest_dir, d)
                    for d in ledger.year_digests(list(self.audit_entries()), before=datetime.now().year)]

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
        why = []
        if c["decision"]["status"] != "Accepted":
            why.append(f"The resident has not confirmed they want the works. Owner: {c['owner']}. Next action: ask the resident and save their answer.")
        if not c["funding_ok"]:
            why.append(f"Funding has not been confirmed. Owner: {c['owner']}. Next action: check the funding and record it.")
        open_h = [h for h in c["hazards"] if not h["released"]]
        if open_h:
            why.append(f"Home retrofit work is stopped for safety review. Owner: {open_h[0]['owner']} (referral follow-up). Next action: obtain external service evidence and an independent decision to restart retrofit work.")
        return why + technical_gate(c)

    @staticmethod
    def status_line(c):
        if c["closed"]:
            return "Completed"
        open_h = [h for h in c["hazards"] if not h["released"]]
        if open_h:
            return f"Stopped until {open_h[0]['owner']} obtains evidence and an independent decision to restart retrofit work"
        if c["stage"] == READY_STAGE and not Store.gate_reasons(c):
            return "Ready"
        return f"Waiting on {c['waiting_on']} {c['reason']}"

    def summary(self, c):
        last = c["contacts"][-1]["at"] if c["contacts"] else None
        nxt = next((a for a in c["appointments"] if a["outcome"] == "Booked"), None)
        status = self.status_line(c)
        if status == "Ready" and buildings.blockers(self.data, self.cases, c):
            status = "Waiting on shared building review"
        return dict(id=c["id"], resident=c["resident"]["name"], address=c["home"]["address"],
                    town=c["home"]["town"], postcode=c["home"]["postcode"], phone=c["resident"]["phone"],
                    stage=c["stage"], status=status, owner=c["owner"], days=c["days_in_stage"],
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
            d["hazards"] = [hazard_view(h, case_id) for h in c["hazards"]]
            if c.get("handoff"):
                d["handoff"] = handoff_view(c)
            d["status"] = self.status_line(c)
            d["gate"] = self.gate_reasons(c) + buildings.blockers(self.data, self.cases, c)
            if d["status"] == "Ready" and d["gate"]:
                d["status"] = "Waiting on shared building review"
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

    def building_view(self, user, building_id):
        with self.lock:
            return buildings.view(self.data, self.cases, building_id, user)

    def require_building_clear(self, c, package_id=None):
        reasons = buildings.blockers(self.data, self.cases, c, package_id)
        if reasons:
            raise GateError(reasons)

    def require_safety_clear(self, c):
        active = next((h for h in c["hazards"] if not h["released"]), None)
        if active:
            raise GateError([f"Home retrofit work is stopped for safety review. Owner: {active['owner']} (referral follow-up). Next action: obtain external evidence and an independent decision to restart retrofit work."])

    def log_call(self, user, case_id, outcome, note, channel="Phone"):
        outcome = (outcome or "").strip()[:80]
        if not outcome:
            raise ValueError("Say how the call went.")
        with self.lock:
            c = self._case(case_id)
            self.guard_case_event(c)
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
            self.guard_case_event(c)
            c["decision"] = dict(status=status, by=user["name"], at=datetime.now().date().isoformat())
            self.audit(user["email"], "resident_decision", case_id, f"{status} {note}".strip())
            self.save()

    def hand_over(self, user, case_id, to_email, note=""):
        """Legacy entry point: offer responsibility, never bypass receiver acceptance."""
        return self.offer_handoff(user, case_id, to_email, note)

    def advance(self, user, case_id):
        with self.lock:
            c = self._case(case_id)
            self.guard_case_event(c)
            if c["stage"] != READY_STAGE:
                raise ValueError("This case is not at the final checks.")
            why = self.gate_reasons(c)
            why += buildings.blockers(self.data, self.cases, c)
            if why:
                raise GateError(why)
            self.require_safety_clear(c)
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
                    f"Kind regards,\n{c['owner']}\nZava North Homes")
        else:
            body = (f"Dear {who},\n\nA quick update on the work to {c['home']['address']}: it is currently at "
                    f"'{c['stage'].lower()}'. {c['owner']} is your contact and will be in touch with the next "
                    f"step.\n\nKind regards,\n{c['owner']}\nZava North Homes")
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
            try:
                scan = self.scan_new_document(case_id, did, name, data, mime)
            except ValueError as e:
                self.audit(user["email"], "upload_document_rejected", case_id, f"{did}: {kind}: {e}")
                raise
            doc = dict(id=did, name=name, kind=kind, at=datetime.now().date().isoformat(), by=user["name"],
                       generated=False, mime=mime, summary="", content_sha256=hashlib.sha256(data).hexdigest(), version=1, scan=scan)
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
            self.ensure_scanned(case_id, doc, user["email"] if user else "system")
            self.require_clean(doc)
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
            self.ensure_scanned(case_id, doc, user["email"] if user else "system")
            self.require_clean(doc)
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
                f"Recent contacts: " + "; ".join(f"{k['at'][:10]} {k['outcome'] if reason_ok else k['channel']}" for k in c["contacts"][-4:]))

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
        return dict(r, label=("AI suggestion, not approved" if r["source"] == "ai" else "Template draft, not approved")
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
        out = dict(r, label=("AI suggestion, not approved" if r["source"] == "ai" else "Summary by rules")
                   + ("" if r["verified"] else ". Unverified: its sources do not match the case record"))
        with self.lock:
            if self.version - ver <= 1:  # only our own comparison record was saved meanwhile
                self._briefings[(user["code"], off)] = (self.version, out)
        return out

    # ---- AI priority recommendation: advice beside the deterministic order, never part of it
    REC_LABEL = "AI suggestion, not approved"
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
        return dict(r, label="AI suggestion, not approved: nothing is submitted until a person approves and submits it"
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
            f = c["funding"]
            if action == "save_draft":
                f["draft"] = (text or "")[:6000]
            elif action == "approve":
                if f["status"] != "Draft ready" or not f["draft"].strip():
                    raise ValueError("Write or generate a draft first.")
                missing = [x["kind"] for x in self.checklist(c) if not x["present"]]
                if missing:
                    raise GateError([f"Evidence is missing: {', '.join(missing)}. Owner: {c['owner']}. Next action: add it to the case."])
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
