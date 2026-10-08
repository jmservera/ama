"""Case store: loading, views, actions, gates and the hash-chained audit log."""
import csv
import hashlib
import io
import json
import os
import re
import threading
from datetime import datetime

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
        src = self.live_path if os.path.exists(self.live_path) else data_path
        with open(src, encoding="utf-8") as f:
            self.data = json.load(f)
        self.cases = {c["id"]: c for c in self.data["cases"]}
        self.staff = {s["email"].lower(): s for s in self.data["staff"]}
        self.last_hash = self._tail_hash()

    def _tail_hash(self):
        h = "0" * 64
        if os.path.exists(self.audit_path):
            with open(self.audit_path, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        h = json.loads(line)["hash"]
        return h

    def save(self):
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
                    last_contact=last, next_visit=nxt["date"] if nxt else None,
                    hazard=any(not h["released"] for h in c["hazards"]),
                    support=c["resident"]["priority_support"] or c["resident"]["adjustment"] != "None",
                    closed=c["closed"])

    def list_cases(self, user, view="mine", q=""):
        with self.lock:
            rows = [c for c in self.cases.values() if not c["closed"]]
            if view == "mine" or user["role"] not in MANAGER_ROLES:
                rows = [c for c in rows if c["owner_code"] == user["code"]]
            if q:
                ql = q.lower()
                rows = [c for c in rows if ql in " ".join([c["resident"]["name"], c["home"]["address"],
                                                           c["home"]["postcode"], c["id"]]).lower()]
            out = [self.summary(c) for c in rows]
        out.sort(key=lambda s: (not s["hazard"], -s["days"]))
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
