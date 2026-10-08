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

from . import insights
from .ai import Ai

DECISIONS = ("Not yet asked", "Waiting", "Accepted", "Declined")
MANAGER_ROLES = ("Retrofit Programme Manager", "Programme Support Officer")
READY_STAGE = "Final checks before ordering"
BOOKED_STAGE = "Install booked"


class GateError(Exception):
    def __init__(self, reasons):
        super().__init__("; ".join(reasons))
        self.reasons = reasons


class Store:
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
        self.docs_dir = os.path.join(os.path.dirname(self.live_path), "docs")
        self.ai = Ai()
        self.version = 0
        self._briefings = {}

    def _tail_hash(self):
        h = "0" * 64
        if os.path.exists(self.audit_path):
            with open(self.audit_path, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        h = json.loads(line)["hash"]
        return h

    def save(self):
        self.version += 1
        tmp = self.live_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.data, f)
        os.replace(tmp, self.live_path)

    def audit(self, who, action, case_id, detail):
        entry = dict(at=datetime.now().isoformat(timespec="seconds"), who=who, action=action,
                     case=case_id, detail=detail, prev=self.last_hash)
        entry["hash"] = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
        with open(self.audit_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        self.last_hash = entry["hash"]

    def verify_audit(self):
        prev = "0" * 64
        if not os.path.exists(self.audit_path):
            return True
        with open(self.audit_path, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                e = json.loads(line)
                h = e.pop("hash")
                if e["prev"] != prev or hashlib.sha256(json.dumps(e, sort_keys=True).encode()).hexdigest() != h:
                    return False
                prev = h
        return True

    @staticmethod
    def gate_reasons(c):
        why = []
        if c["decision"]["status"] != "Accepted":
            why.append("The resident has not confirmed they want the works.")
        if not c["funding_ok"]:
            why.append("Funding has not been confirmed.")
        if any(not h["released"] for h in c["hazards"]):
            why.append("A safety issue is still open.")
        return why

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

    def list_cases(self, user, view="mine", q="", filters=None, sort="urgent"):
        f = filters or {}
        with self.lock:
            rows = [c for c in self.cases.values() if not c["closed"] and insights.matches(c, f)]
            if view == "mine" or user["role"] not in MANAGER_ROLES:
                rows = [c for c in rows if c["owner_code"] == user["code"]]
            if q:
                ql = q.lower()
                rows = [c for c in rows if ql in " ".join([c["resident"]["name"], c["home"]["address"],
                                                           c["home"]["postcode"], c["id"]]).lower()]
            out = [self.summary(c) for c in rows]
        out.sort(key=insights.sort_key(sort))
        return out

    def counts(self, user):
        with self.lock:
            mine = [c for c in self.cases.values() if not c["closed"] and c["owner_code"] == user["code"]]
            return dict(mine=len(mine), hazards=sum(any(not h["released"] for h in c["hazards"]) for c in mine),
                        open=sum(not c["closed"] for c in self.cases.values()))

    def detail(self, case_id):
        with self.lock:
            c = self.cases.get(case_id)
            if not c:
                return None
            d = json.loads(json.dumps(c))
            d["status"] = self.status_line(c)
            d["gate"] = self.gate_reasons(c)
        d["can_advance"] = c["stage"] == READY_STAGE
        d["suggestions"] = insights.recommend_handover(c, list(self.cases.values()), self.data["staff"])
        d["checklist"] = self.checklist(c)
        d["contacts"] = list(reversed(d["contacts"]))[:40]
        return d

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
            self.audit(user["email"], "resident_decision", case_id, f"{status} {note}".strip())
            self.save()

    def hand_over(self, user, case_id, to_email, note=""):
        to = self.staff.get((to_email or "").lower())
        if not to:
            raise ValueError("Choose who is taking this over.")
        with self.lock:
            c = self._case(case_id)
            c.update(owner=to["name"], owner_code=to["code"], owner_role=to["role"], waiting_on=to["name"])
            self.audit(user["email"], "hand_over", case_id, f"to {to['name']} {note}".strip())
            self.save()

    def advance(self, user, case_id):
        with self.lock:
            c = self._case(case_id)
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

    def visits(self, user, view="mine"):
        with self.lock:
            own = None if view == "all" and user["role"] in MANAGER_ROLES else user["code"]
            return insights.visits(list(self.cases.values()), own)

    # ---- documents
    EVIDENCE = ("EPC", "Survey", "Design", "Consent")
    EXT = {"pdf": "application/pdf", "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
           "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
           "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
           "csv": "text/csv", "txt": "text/plain"}
    KINDS = ("EPC", "Survey", "Design", "Consent", "Funding evidence", "Photo", "Other")
    MAX_BYTES = 5 * 1024 * 1024

    @staticmethod
    def checklist(c):
        have = {d["kind"] for d in c["documents"]}
        return [dict(kind=k, present=k in have) for k in Store.EVIDENCE]

    def add_document(self, user, case_id, name, kind, data):
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
            folder = os.path.join(self.docs_dir, case_id)
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, did), "wb") as f:
                f.write(data)
            doc = dict(id=did, name=name, kind=kind, at=datetime.now().date().isoformat(), by=user["name"],
                       generated=False, mime=mime, summary="")
            c["documents"].append(doc)
            self.audit(user["email"], "upload_document", case_id, f"{kind}: {name}")
            self.save()
        return doc

    def read_document(self, user, case_id, doc_id):
        with self.lock:
            c = self._case(case_id)
            doc = next((d for d in c["documents"] if d["id"] == doc_id and not d["generated"]), None)
            if not doc:
                raise KeyError(doc_id)
            with open(os.path.join(self.docs_dir, case_id, doc_id), "rb") as f:
                data = f.read()
        self.audit(user["email"], "ai_run_start", case_id, f"read_document {doc['name']}")
        r = self.ai.look_at(doc["name"], data, doc["mime"])
        with self.lock:
            doc["summary"] = r["text"]
            self.audit(user["email"], "ai_run_end", case_id, f"read_document source={r['source']} model={r['model']}")
            self.save()
        return r

    def get_document(self, case_id, doc_id):
        with self.lock:
            c = self._case(case_id)
            doc = next((d for d in c["documents"] if d["id"] == doc_id), None)
            if not doc:
                raise KeyError(doc_id)
            if doc["generated"]:
                text = (f"{doc['name']}\nCase {c['id']}: {c['home']['address']}, {c['home']['postcode']}\n"
                        f"Filed {doc['at']} by {doc['by']}\nType: {doc['kind']}\n")
                return doc["name"].rsplit(".", 1)[0] + ".txt", "text/plain", text.encode()
            with open(os.path.join(self.docs_dir, case_id, doc_id), "rb") as f:
                return doc["name"], doc["mime"], f.read()

    # ---- AI drafting (always a draft for a person)
    def _facts(self, c):
        r = c["resident"]
        return (f"Case {c['id']}. Resident: {r['name']}. Home: {c['home']['address']}, {c['home']['town']}. "
                f"Stage: {c['stage']} for {c['days_in_stage']} days. Waiting on {c['waiting_on']} {c['reason']}. "
                f"Resident adjustments: {r['adjustment']}. Resident prefers: {r['preferred']}. "
                f"Resident decision: {c['decision']['status']}. Funding: {c['funding']['route']} ({c['funding']['status']}). "
                f"Open safety issues: {sum(not h['released'] for h in c['hazards'])}. "
                f"Recent contacts: " + "; ".join(f"{k['at'][:10]} {k['outcome']}" for k in c["contacts"][-4:]))

    def ai_run(self, user, case_id, task):
        with self.lock:
            c = self._case(case_id)
            facts = self._facts(c)
            fallback = self.draft(case_id, "visit" if task == "message" else "update")["text"]
            summary = self.status_line(c)
            owner, who = c["owner"], c["resident"]["name"]
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
        r = self.ai.run(task, sysmsg, instr + "\n\nFacts:\n" + facts, tmpl, strong)
        self.audit(user["email"], "ai_run_end", case_id, f"{task} source={r['source']} model={r['model']} validated={r['validated']}")
        return dict(r, label="AI-drafted, for you to check" if r["source"] == "ai" else "Template draft, for you to check")

    def briefing(self, user):
        with self.lock:
            hit = self._briefings.get(user["code"])
            if hit and hit[0] == self.version:
                return hit[1]
            ver = self.version
            mine = [c for c in self.cases.values() if not c["closed"] and c["owner_code"] == user["code"]]
            mine.sort(key=lambda c: (not any(not h["released"] for h in c["hazards"]), -c["days_in_stage"]))
            top = mine[:8]
            facts = "\n".join(f"{c['id']} {c['resident']['name']}: {c['stage']}, {c['days_in_stage']} days. {self.status_line(c)}" for c in top)
            tmpl = "Start with: " + "; ".join(f"{c['resident']['name']} ({c['stage'].lower()}, {c['days_in_stage']} days)" for c in top[:3]) if top else "No open cases."
        r = self.ai.run("briefing", "You write a friendly three-sentence morning briefing for a housing officer. Use only the facts. "
                        "Safety issues first, then longest waits. No invented facts.", facts, tmpl)
        self.audit(user["email"], "ai_run", "-", f"briefing source={r['source']} model={r['model']}")
        out = dict(r, label="AI-drafted" if r["source"] == "ai" else "Summary by rules")
        with self.lock:
            if ver == self.version:
                self._briefings[user["code"]] = (ver, out)
        return out

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
                                have=sum(x["present"] for x in cl), need=len(cl), days=c["days_in_stage"]))
        order = {s: i for i, s in enumerate(self.FUND_FLOW)}
        out.sort(key=lambda x: (order[x["status"]] == 0, -x["days"]))
        return out

    def funding_draft(self, user, case_id):
        with self.lock:
            c = self._case(case_id)
            missing = [x["kind"] for x in self.checklist(c) if not x["present"]]
            facts = self._facts(c) + f" Built: {c['home']['built']}. Type: {c['home']['type']}. EPC band: {c['home']['epc']}. " \
                f"Measures: {', '.join(c['measures']) if isinstance(c['measures'], list) else c['measures']}."
            route = c["funding"]["route"]
            tmpl = (f"Funding application draft for {c['home']['address']} ({route})\n\nProperty: {c['home']['type']}, built "
                    f"{c['home']['built']}, EPC {c['home']['epc']}.\nProposed measures: {c['measures']}.\n\n"
                    + "\n".join(f"Needs: {m} document" for m in missing) + "\nNeeds: costs from the contractor\nNeeds: eligibility check by the Grants Officer")
        sysmsg = ("You draft the narrative part of a social housing retrofit funding application. Use only the facts given. Do not invent "
                  "costs, eligibility results or evidence. Where something is missing write 'Needs: ...'. Headings: Property, Proposed work, "
                  "Evidence held, Evidence still needed. Under 250 words.")
        self.audit(user["email"], "ai_run_start", case_id, "funding_draft")
        r = self.ai.run("funding_draft", sysmsg, f"Route: {route}\n{facts}\nMissing documents: {', '.join(missing) or 'none'}", tmpl, True,
                        check=lambda t: all(m.lower() in t.lower() for m in missing) or "needs" in t.lower())
        with self.lock:
            c["funding"]["draft"] = r["text"]
            if c["funding"]["status"] in ("Not started", "To prepare"):
                c["funding"]["status"] = "Draft ready"
            self.audit(user["email"], "ai_run_end", case_id, f"funding_draft source={r['source']} model={r['model']}")
            self.save()
        return dict(r, label="AI-drafted, human-approved: nothing is submitted until a person approves and submits it")

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
