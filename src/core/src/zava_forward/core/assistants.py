"""Five proposal-only assistants. SQL owns claims, liability and review, not inference.

Exercise rules deliberately describe gaps, not company approvals. All captured
fields are safe for every reader of a capability. No domain write is available
to the provider or this service.
"""
import hashlib
import json
import logging
import math
import os
import threading
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone

from . import assistant_release as rel
from . import continuity, projection, quality, ranking
from zava_forward.core.ai import FORBIDDEN, Ai
from .store import ConflictError

LOG = logging.getLogger(__name__)

PM = "Retrofit Programme Manager"
RC = "Retrofit Coordinator"
VERSION = "1.0.0"
SCHEMA_VERSION = "evidence-proposal-v1"
RULE_VERSION = "synthetic-gaps-2026-10-13-v1"
PURPOSE = "service:retrofit-evidence-proposals"
REGISTRY = {
    "stock-prioritisation": dict(roles=(RC, PM), categories=("home", "survey", "ranking"),
                               purpose="Explain stock facts and prepare a data-owner query"),
    "assessment-preparation": dict(roles=(RC, PM), categories=("home", "survey", "measures", "technical", "documents"),
                                  purpose="Prepare a survey/design evidence checklist"),
    "funding-evidence": dict(roles=("Grants and Evidence Officer", PM),
                            categories=("home", "measures", "funding", "finance", "grants", "documents"),
                            purpose="Prepare application/claim evidence gaps"),
    "works-resident-coordination": dict(roles=(RC, "Resident Liaison Officer", PM),
                                       categories=("home", "measures", "preferences", "appointments", "handoff", "capacity", "requests"),
                                       purpose="Draft an update or committed-capacity option"),
    "quality-evidence": dict(roles=("Quality Inspector", PM),
                            categories=("home", "measures", "quality", "checklists", "documents"),
                            purpose="Assemble per-measure quality evidence discrepancies"),
}
RULES = {
    "stock-prioritisation": "Missing/unknown home.epc, home.type or home.built; supplied survey.epc/type/built conflicts with home.",
    "assessment-preparation": "Missing Survey/Design metadata/content hash or technical.design_version; relevant permitted source signature changes.",
    "funding-evidence": "Missing measures, funding.route/reference, grants or budget amount; incomplete supplied invoice ref/lines/milestone inputs; claim-phase grant lacks sourced history or hashed Funding evidence metadata; relevant permitted terms/evidence signature changes.",
    "works-resident-coordination": "handoff.state=Offered/Received/Escalated; past appointment.date with missing/Booked/Planned/No access/Missed outcome; past open service_request.next_update.",
    "quality-evidence": "Missing measures; not exactly one quality record per measure; missing/conflicting checklist item evidence or checklist version mismatch; relevant permitted signature changes.",
}
OUTPUT_SCHEMA = dict(required=("summary", "findings", "unknowns"), summary_chars=1200,
                     findings_count=12, finding_chars=800, citations_per_finding=8,
                     unknowns_count=80, unknown_chars=240, absolute_output_chars=16000,
                     citations="captured source IDs only; non-empty on every finding")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def proposal_identity(capability):
    return dict(capability=capability, purpose=REGISTRY[capability]["purpose"])


def pick(value, keys):
    value = value if isinstance(value, dict) else {}
    result = {}
    for key in keys:
        item = value.get(key)
        result[key] = item if (item is None or type(item) in (str, int, bool) or
                               (type(item) is float and math.isfinite(item))) else None
    return result


def measures(c):
    value = c.get("measures")
    values = value if isinstance(value, list) else value.split(",") if isinstance(value, str) else []
    return [m.strip() for m in values if isinstance(m, str) and m.strip()]


def capture(capability, c, procurement=None):
    """Closed field allowlists, never whole records, notes, vulnerability or AI summaries."""
    source = {"home": pick(c.get("home"), ("address", "town", "postcode", "type", "built", "epc", "tenure"))}
    # Role-independent so the source signature is stable: outcomes only when every role of the assistant has a recorded need.
    need_ok = all(projection.can_see_reason(dict(role=r)) for r in REGISTRY[capability]["roles"])
    if "measures" in REGISTRY[capability]["categories"]:
        source["measures"] = measures(c)
    if capability in ("stock-prioritisation", "assessment-preparation"):
        source["survey"] = pick(c.get("survey"), ("epc", "type", "built", "version", "status", "evidence_hash"))
    if capability == "stock-prioritisation":
        # Only the public portion of the deterministic reasons crosses this audience.
        policy = ranking.describe()
        policy.pop("versions", None)
        public = pick(dict(stage=c.get("stage"), waiting_days=c.get("days_in_stage")), ("stage", "waiting_days"))
        reasons = []
        if type(public["waiting_days"]) in (int, float):
            reasons.append(dict(code="waiting_days", text=f"Waiting {public['waiting_days']} days in this stage"))
        if public["stage"]:
            reasons.append(dict(code="stage_order", text=f"At '{public['stage']}'"))
        source["ranking"] = dict(policy=policy, **public, reasons=reasons,
                               disclosure="Resident support and safety ranking inputs are not disclosed to this audience.")
    if capability == "assessment-preparation":
        source["technical"] = pick(c.get("technical"), ("design_version",))
    if capability in ("assessment-preparation", "funding-evidence", "quality-evidence"):
        kinds = {"assessment-preparation": ("EPC", "Survey", "Design"),
                 "funding-evidence": ("EPC", "Survey", "Design", "Funding evidence"),
                 "quality-evidence": ("Photo", "Design", "Other")}[capability]
        source["documents"] = sorted(
            [pick(d, ("id", "kind", "version", "content_sha256", "at"))
             for d in c.get("documents", []) if d.get("kind") in kinds],
            key=lambda d: str(d.get("id")))
    if capability == "funding-evidence":
        source["funding"] = pick(c.get("funding"), ("route", "status", "reference", "terms_version", "terms_hash"))
        fx = c.get("finance") or {}
        source["finance"] = {
            "budget": pick(fx.get("budget"), ("amount", "status")),
            "commitments": [pick(x, ("id", "supplier", "contract", "work_order", "measure", "amount", "quantity", "status"))
                            for x in fx.get("commitments", [])],
            "invoices": [dict(pick(x, ("id", "kind", "supplier", "work_order", "ref", "status", "version", "evidence_hash")),
                              lines=[pick(line, ("measure", "quantity", "amount", "milestone_ref"))
                                     for line in x.get("lines", [])]) for x in fx.get("invoices", [])],
        }
        source["grants"] = [dict(pick(g, ("id", "scheme", "state")), evidence=[
            pick(x, ("state", "source", "amount", "at")) for x in g.get("history", [])])
                            for g in c.get("grants", [])]
    if capability == "works-resident-coordination":
        source["preferences"] = pick(c.get("resident"), ("preferred", "unavailable"))
        source["appointments"] = [dict(pick(a, ("type", "date", "slot", "outcome")), **(
            {} if need_ok else {"outcome": projection.status_only(a.get("outcome"))})) for a in c.get("appointments", [])]
        source["handoff"] = pick(c.get("handoff"), ("state", "to_code", "at"))
        source["requests"] = [pick(r, ("id", "status", "next_update")) for r in c.get("service_requests", [])]
        name = (c.get("contractor") or {}).get("name")
        source["capacity"] = []
        for p in (procurement or {}).get("packages", []):
            cap = (p.get("capacity") or {}).get(name)
            if cap:
                source["capacity"].append(dict(package=p.get("id"), period_from=p.get("period_from"),
                                               period_to=p.get("period_to"), contractor=name,
                                               **pick(cap, ("committed", "evidence"))))
    if capability == "quality-evidence":
        source["quality"] = [dict(pick(q, ("measure", "state", "checklist_version")),
                                 items=[pick(i, ("label", "evidence")) for i in q.get("items", [])])
                             for q in c.get("quality", [])]
        source["checklists"] = {m: quality.checklist_for(m) for m in measures(c)}
    unknowns = []

    def missing(value, path):
        if value is None or value == "" or value == []:
            unknowns.append(path)
        elif isinstance(value, dict):
            for key, child in value.items():
                missing(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                missing(child, f"{path}.{index}")
    missing(source, "source")
    citations = {f"source:{key}": dict(locator=f"case:{c['id']}/{key}", content_hash=digest(value))
                 for key, value in source.items()}
    return dict(sources=source, citations=citations, unknowns=unknowns,
                schema=SCHEMA_VERSION, rules=RULE_VERSION, registry=VERSION,
                registry_hash=digest(dict(version=VERSION, capability=capability, contract=REGISTRY[capability])),
                schema_hash=digest(dict(version=SCHEMA_VERSION, schema=OUTPUT_SCHEMA)),
                rule_hash=digest(dict(version=RULE_VERSION, predicate=RULES[capability])),
                exercise_predicate=RULES[capability],
                exercise_rule="Selected synthetic gap predicates, not approved company rules.")


def eligible(capability, snapshot, now_date, changed=False):
    s = snapshot["sources"]
    if capability == "stock-prioritisation":
        h, survey = s["home"], s["survey"]
        return any(h.get(k) in (None, "", "Unknown") for k in ("epc", "type", "built")) or any(
            survey.get(k) not in (None, "") and survey[k] != h.get(k) for k in ("epc", "type", "built"))
    if capability == "assessment-preparation":
        kinds = {d["kind"] for d in s["documents"]}
        return changed or not {"Survey", "Design"} <= kinds or not s["technical"]["design_version"] or any(
            not d["content_sha256"] for d in s["documents"])
    if capability == "funding-evidence":
        f = s["funding"]
        basic = (not s["measures"] or f["route"] in (None, "", "Not decided") or not f["reference"] or
                 not s["grants"] or not s["finance"]["budget"]["amount"])
        invoices_missing = any(not inv["ref"] or not inv["lines"] or any(
            any(line.get(k) in (None, "") for k in ("measure", "quantity", "amount", "milestone_ref"))
            for line in inv["lines"]) for inv in s["finance"]["invoices"])
        claim_missing = any(g["state"] in ("Claimable", "Submitted", "Accepted", "Cash received") and (
            not any(e.get("source") for e in g["evidence"]) or not any(
                d["kind"] == "Funding evidence" and d["content_sha256"] for d in s["documents"])) for g in s["grants"])
        return changed or basic or invoices_missing or claim_missing
    if capability == "works-resident-coordination":
        return s["handoff"]["state"] in ("Offered", "Received", "Escalated") or any(
            a["date"] and a["date"] < now_date and a["outcome"] in (None, "", "Booked", "Planned", "No access", "Missed")
            for a in s["appointments"]) or any(
            r["next_update"] and r["next_update"] < now_date and r["status"] not in ("Closed", "Resolved")
            for r in s["requests"])
    if not s["measures"]:
        return True
    for m in s["measures"]:
        records = [q for q in s["quality"] if q["measure"] == m]
        if len(records) != 1:
            return True
        q = records[0]
        labels = s["checklists"][m]["items"]
        if q["checklist_version"] != s["checklists"][m]["version"]:
            return True
        if any(not any(i["label"] == label and i["evidence"] for i in q["items"]) for label in labels):
            return True
        if any(len({i["evidence"] for i in q["items"] if i["label"] == label}) > 1 for label in labels):
            return True
    return changed


def validate_output(value, snapshot, max_chars):
    if not isinstance(value, dict) or set(value) != {"summary", "findings", "unknowns"}:
        raise ValueError("Expected summary, findings and unknowns.")
    if len(canonical(value)) > max_chars or not isinstance(value["summary"], str) or not value["summary"].strip() or not 1 <= len(value["summary"]) <= 1200:
        raise ValueError("Summary/output bounds exceeded.")
    if not isinstance(value["findings"], list) or not 1 <= len(value["findings"]) <= 12:
        raise ValueError("Cited findings required.")
    if not isinstance(value["unknowns"], list) or len(value["unknowns"]) > 80 or any(
            not isinstance(x, str) or len(x) > 240 for x in value["unknowns"]):
        raise ValueError("Unknowns must be bounded strings.")
    for item in value["findings"]:
        if not isinstance(item, dict) or set(item) != {"text", "citations"} or not isinstance(item["text"], str) or not 1 <= len(item["text"]) <= 800:
            raise ValueError("Invalid finding.")
        if not isinstance(item["citations"], list) or not 1 <= len(item["citations"]) <= 8 or any(
                not isinstance(x, str) or x not in snapshot["citations"] for x in item["citations"]):
            raise ValueError("Missing/unsupported citation.")
    # Deterministic unknowns cannot disappear merely because a model omitted them.
    value["unknowns"] = sorted(set(value["unknowns"] + snapshot["unknowns"]))
    if len(value["unknowns"]) > 80 or len(canonical(value)) > max_chars or FORBIDDEN.search(canonical(value)):
        raise ValueError("Output bounds exceeded after unknown reconciliation.")
    return value


class Limits:
    DEFAULTS = dict(scan_interval=60, scan_size=20, input_chars=12000, output_chars=8000,
                    output_tokens=600, timeout=20, active_calls=2, attempts=2, backoff=30, lease=60)

    def __init__(self, env=None):
        env = os.environ if env is None else env
        self.authority = env.get("ZF_ASSIST_AUTHORITY", "")
        self.proactive = env.get("ZF_ASSIST_PROACTIVE", "0") == "1"
        self.expiry = None
        self.valid = False
        self.error = "Operator authority, finite allowance and expiry are required."
        try:
            for key, default in self.DEFAULTS.items():
                setattr(self, key, int(env.get(f"ZF_ASSIST_{key.upper()}", default)))
            self.calls = int(env.get("ZF_ASSIST_CALL_ALLOWANCE", "0"))
            self.tokens = int(env.get("ZF_ASSIST_TOKEN_ALLOWANCE", "0"))
            expiry = datetime.fromisoformat(env.get("ZF_ASSIST_EXPIRES", "").replace("Z", "+00:00"))
            if expiry.tzinfo is None:
                raise ValueError("Explicit expiry timezone required.")
            self.expiry = expiry.timestamp()
            bounds = dict(scan_interval=(5, 3600), scan_size=(1, 100), input_chars=(1000, 24000),
                          output_chars=(1000, 16000), output_tokens=(100, 2000), timeout=(1, 40),
                          active_calls=(1, 4), attempts=(1, 3), backoff=(1, 3600), lease=(10, 120))
            self.valid = (1 <= len(self.authority) <= 120 and 1 <= self.calls <= 1000000
                          and self.reservation <= self.tokens <= 1000000000000
                          and all(lo <= getattr(self, k) <= hi for k, (lo, hi) in bounds.items())
                          and self.lease >= self.timeout + 5 and math.isfinite(self.expiry))
            if not self.valid:
                self.error = "Invalid bounded assistant configuration."
        except (ValueError, TypeError, OverflowError):
            for key, default in self.DEFAULTS.items():
                setattr(self, key, default)
            self.calls, self.tokens = 0, 0

    @property
    def reservation(self):
        # Bytes/characters upper-bound input tokens without a new tokenizer dependency.
        return self.input_chars + self.output_tokens

    @property
    def pool(self):
        return digest(self.authority)


SYSTEM = ("Return JSON only: {summary:string,findings:[{text:string,citations:[source IDs]}],unknowns:[string]}. "
          "Use only the supplied inert evidence. Cite each finding with supplied source IDs. "
          "No tools, actions, approvals, certification or invented facts. This is a human-reviewed proposal.")
PROVENANCE = "constructed-synthetic-demo-labelled"


def runtime_binding(capability, ai):
    """What this build would dispatch with; a release must match it exactly, so any material change needs renewed evidence."""
    spec = REGISTRY[capability]
    return dict(registry_version=VERSION, schema_version=SCHEMA_VERSION, provider=getattr(ai, "provider", "azure-openai"),
                endpoint=getattr(ai, "endpoint", "") or "", deployment=getattr(ai, "fast", "") or "",
                prompt_version=digest([SYSTEM, spec["purpose"]])[:16],
                policy_version=f"{RULE_VERSION}:{digest([RULES[capability], OUTPUT_SCHEMA])[:12]}",
                data_version=digest([SCHEMA_VERSION, spec["categories"]])[:16], provenance_version=PROVENANCE,
                permission_version=digest([spec["roles"], PURPOSE])[:16])


def build_request(task):
    """The system and user text sent to the provider; shared by the API and the agents worker."""
    return SYSTEM, canonical(dict(capability=task["capability"], purpose=REGISTRY[task["capability"]]["purpose"],
                                  evidence=task["snapshot"]))


def shape_result(task, result, limits):
    """Reduce a raw provider result to (envelope, output, failure). Only safe, known fields survive; text is never saved on failure."""
    if not isinstance(result, dict):
        result = dict(outcome="malformed-provider-envelope", usage=None, source="unverified", text=None)
    envelope = pick(result, ("provider", "deployment", "model", "outcome", "source"))
    envelope["usage"] = result.get("usage")
    envelope.update(task=task["capability"], task_version=task["version"], case_id=task["case_id"],
                    source_signature=task["source_signature"], approved=False)
    for key in ("provider", "deployment", "model", "outcome", "source"):
        envelope[key] = envelope[key][:120] if isinstance(envelope[key], str) else None
    usage = envelope["usage"]
    envelope["usage"] = {k: usage[k] for k in ("prompt_tokens", "completion_tokens", "total_tokens")} if (
        isinstance(usage, dict) and all(type(usage.get(k)) is int and usage[k] >= 0
                                       for k in ("prompt_tokens", "completion_tokens", "total_tokens")) and
        usage["prompt_tokens"] > 0 and usage["total_tokens"] == usage["prompt_tokens"] + usage["completion_tokens"]) else None
    output, failure = None, None
    try:
        if result.get("source") != "ai" or result.get("outcome") != "returned":
            raise ValueError("AI unavailable/unverified; use the manual route.")
        text = result.get("text")
        if not isinstance(text, str) or len(text) > limits.output_chars:
            raise ValueError("Output exceeds bounds.")
        output = validate_output(json.loads(text), task["snapshot"], limits.output_chars)
    except (ValueError, TypeError, KeyError):
        failure = "Failed or malformed evidence proposal; human/manual work required."
        envelope["source"] = "unverified"
    return envelope, output, failure


SQLITE_DDL = (
    "CREATE TABLE IF NOT EXISTS assistant_tasks (id TEXT PRIMARY KEY, capability TEXT NOT NULL, case_id TEXT NOT NULL, signature TEXT NOT NULL, body TEXT NOT NULL, state TEXT NOT NULL, fence INTEGER NOT NULL, owner TEXT NOT NULL, lease_until REAL NOT NULL, attempts INTEGER NOT NULL, not_before REAL NOT NULL, revision INTEGER NOT NULL)",
    "CREATE TABLE IF NOT EXISTS assistant_allowance (id TEXT PRIMARY KEY, calls INTEGER NOT NULL, tokens INTEGER NOT NULL, expires REAL NOT NULL, used_calls INTEGER NOT NULL, reserved_tokens INTEGER NOT NULL)",
    "CREATE TABLE IF NOT EXISTS assistant_attempts (id TEXT PRIMARY KEY, task_id TEXT NOT NULL, fence INTEGER NOT NULL, pool TEXT NOT NULL, reserved INTEGER NOT NULL, actual INTEGER, outcome TEXT NOT NULL, active_until REAL NOT NULL DEFAULT 0)",
    "CREATE TABLE IF NOT EXISTS assistant_events (id TEXT PRIMARY KEY, task_id TEXT NOT NULL, at REAL NOT NULL, body TEXT NOT NULL)",
    "CREATE INDEX IF NOT EXISTS ix_assistant_pending ON assistant_tasks (state, not_before, lease_until)",
) + rel.SQLITE_DDL
MSSQL_DDL = (
    "CREATE TABLE assistant_tasks (id VARCHAR(64) PRIMARY KEY, capability VARCHAR(64) NOT NULL, case_id NVARCHAR(64) NOT NULL, signature VARCHAR(64) NOT NULL, body NVARCHAR(MAX) NOT NULL, state VARCHAR(24) NOT NULL, fence BIGINT NOT NULL, owner VARCHAR(64) NOT NULL, lease_until FLOAT NOT NULL, attempts INT NOT NULL, not_before FLOAT NOT NULL, revision BIGINT NOT NULL)",
    "CREATE TABLE assistant_allowance (id VARCHAR(64) PRIMARY KEY, calls BIGINT NOT NULL, tokens BIGINT NOT NULL, expires FLOAT NOT NULL, used_calls BIGINT NOT NULL, reserved_tokens BIGINT NOT NULL)",
    "CREATE TABLE assistant_attempts (id VARCHAR(100) PRIMARY KEY, task_id VARCHAR(64) NOT NULL, fence BIGINT NOT NULL, pool VARCHAR(64) NOT NULL, reserved BIGINT NOT NULL, actual BIGINT NULL, outcome VARCHAR(40) NOT NULL, active_until FLOAT NOT NULL DEFAULT 0)",
    "CREATE TABLE assistant_events (id VARCHAR(64) PRIMARY KEY, task_id VARCHAR(64) NOT NULL, at FLOAT NOT NULL, body NVARCHAR(MAX) NOT NULL)",
) + rel.MSSQL_DDL


class Affected(list):
    """Affected proposals with the full count, so a capped list is never mistaken for the whole set."""

    def __init__(self, items=(), total=None):
        super().__init__(items)
        self.total = len(self) if total is None else total
        self.truncated = self.total > len(self)


class Assistants:
    def __init__(self, store, env=None, provider=None):
        self.store, self.limits = store, Limits(env)
        # The provider port: (system, prompt, max_tokens, timeout) -> raw envelope. The default late-binds to the store's AI client.
        self.provider = provider or (lambda *args: self.store.ai.evidence(*args))
        self.sql = hasattr(store, "assistant_connection")
        self.mssql = hasattr(store, "_env")
        self.stop_event = threading.Event()
        self.dispatch_lock = threading.Lock()
        self.threads = []
        self.scan_lock = threading.Lock()
        self.call_slots = threading.BoundedSemaphore(self.limits.active_calls if self.limits.valid else 1)
        self.scan_cursor = ""
        self.approvers = {x.strip().lower() for x in (env or os.environ).get("ZF_ASSIST_RELEASE_APPROVERS", "").split(",") if x.strip()}
        self.schema_error = None
        if self.sql:
            try:
                self.migrate()
            except Exception:
                self.sql = False
                self.schema_error = "Assistant schema unavailable; operator migration required. Continue ordinary case work manually."

    def migrate(self):
        with self.transaction() as db:
            if self.mssql:
                ledger = bool(db.execute("SELECT is_ledger_on FROM sys.databases WHERE name=DB_NAME()").fetchone()[0])
                for ddl in MSSQL_DDL:
                    name = ddl.split()[2]
                    if ledger and name == "assistant_events":
                        ddl += " WITH (LEDGER = ON (APPEND_ONLY = ON))"
                    db.execute(f"IF OBJECT_ID(N'{name}', N'U') IS NULL {ddl}")
                db.execute("IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name='ix_assistant_pending' AND object_id=OBJECT_ID(N'assistant_tasks')) CREATE INDEX ix_assistant_pending ON assistant_tasks (state, not_before, lease_until)")
                if ledger:
                    kind = db.execute("SELECT ledger_type_desc FROM sys.tables WHERE name=N'assistant_events'").fetchone()[0]
                    if kind != "APPEND_ONLY_LEDGER_TABLE":
                        raise ValueError("Assistant events must be an append-only ledger table; operator schema repair required.")
                else:
                    db.execute("IF OBJECT_ID(N'assistant_events_immutable', N'TR') IS NULL EXEC(N'CREATE TRIGGER assistant_events_immutable ON assistant_events INSTEAD OF UPDATE, DELETE AS THROW 50001, ''assistant evidence is append-only'', 1')")
            else:
                for ddl in SQLITE_DDL:
                    db.execute(ddl)
                for action in ("UPDATE", "DELETE"):
                    db.execute(f"CREATE TRIGGER IF NOT EXISTS assistant_events_no_{action.lower()} BEFORE {action} ON assistant_events BEGIN SELECT RAISE(ABORT, 'assistant evidence is append-only'); END")

    @contextmanager
    def transaction(self):
        db = self.store.assistant_connection()
        try:
            if self.mssql:
                db.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.execute("COMMIT")
        except BaseException:
            db.execute("ROLLBACK")
            raise
        finally:
            try:
                if self.mssql:
                    db.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")
            finally:
                db.close()

    def now(self, db):
        query = ("SELECT DATEDIFF_BIG(MILLISECOND, CONVERT(datetime2,'1970-01-01'), SYSUTCDATETIME()) / 1000.0"
                 if self.mssql else "SELECT (julianday('now')-2440587.5)*86400.0")
        return float(db.execute(query).fetchone()[0])

    def event(self, db, tid, **body):
        db.execute("INSERT INTO assistant_events (id, task_id, at, body) VALUES (?,?,?,?)",
                   (uuid.uuid4().hex, tid, self.now(db), canonical(body)))

    def authorize(self, db, user, capability, case_id=None):
        if capability not in REGISTRY:
            raise ValueError("Unknown assistant.")
        if user.get("role") not in REGISTRY[capability]["roles"]:
            raise PermissionError("This assistant belongs to a different role. Use the manual owner route.")
        row = db.execute("SELECT body FROM staff WHERE email=?", (user.get("email", "").lower(),)).fetchone()
        current = json.loads(row[0]) if row else None
        if not current or current.get("role") != user.get("role") or current.get("disabled") or current.get("active") is False or (
                current.get("email", "").lower() != user.get("email", "").lower()):
            raise PermissionError("Current staff role has changed or been revoked.")
        for field in ("case_ids", "areas"):
            values = current.get(field)
            if values is not None and (not isinstance(values, list) or len(values) > 1000 or
                                       any(not isinstance(x, str) or not 1 <= len(x) <= 128 for x in values)):
                raise PermissionError("Current staff scope is malformed; resolve it manually.")
        if case_id is not None:
            ids = current.get("case_ids")
            if ids is not None and case_id not in ids:
                raise PermissionError("Case is outside your current scope.")
            row = db.execute("SELECT body FROM cases WHERE id=?", (case_id,)).fetchone()
            if row is None:
                raise KeyError(case_id)
            c = json.loads(row[0])
            areas = current.get("areas")
            if areas is not None and c.get("home", {}).get("area") not in areas:
                raise PermissionError("Case area is outside your current scope.")
            return c
        return current

    def snapshot(self, db, capability, c):
        proc = {}
        if capability == "works-resident-coordination":
            row = db.execute("SELECT value FROM meta WHERE key='procurement'").fetchone()
            proc = json.loads(row[0]) if row else {}
        return capture(capability, c, proc)

    def continuity(self, db):
        """The persisted suspension state, read on the caller's own SQL connection so no process caches it."""
        row = db.execute("SELECT value FROM meta WHERE key='continuity'").fetchone()
        return continuity.load(row[0] if row else None)

    def suspended(self, db, capability):
        s = continuity.active(self.continuity(db), capability)
        return continuity.reason_text(s) if s else None

    def admission(self, db, capability):
        """The retained denial for this task, or None when a matching release is in force. Read on the caller's connection."""
        ai = self.store.ai
        return rel.admission(db, capability, runtime_binding(capability, ai), self.now(db), live=isinstance(ai, Ai))

    def record_release(self, user, body):
        if not self.sql:
            raise ValueError(self.disabled())
        with self.transaction() as db:
            self.authorize(db, user, "funding-evidence")
            from .ai_registry import LEGACY
            rid = rel.record(db, self.now(db), user, body, self.approvers, set(REGISTRY) | {f"legacy:{t}" for t in LEGACY})
        return dict(id=rid, status="active", note="Permits bounded proposals only; no approval, domain write or live-use authority.")

    def change_release(self, user, rid, status, reason):
        if not self.sql:
            raise ValueError(self.disabled())
        with self.transaction() as db:
            self.authorize(db, user, "funding-evidence")
            rel.change(db, self.now(db), user, rid, status, reason)
        return dict(id=rid, status=status)

    def affected(self, scope, limit=500):
        """Queued, leased and ready proposals a suspension of this scope covers; `.truncated` says whether the limit cut the list."""
        if not self.sql:
            return Affected()
        with self.transaction() as db:
            rows = db.execute("SELECT id,capability,state,body FROM assistant_tasks WHERE state IN ('pending','leased','ready') ORDER BY id").fetchall()
        found = [dict(id=i, task=c, version=json.loads(b).get("version"), state=s) for i, c, s, b in rows
                 if scope in (continuity.ALL, c)]
        return Affected(found[:limit], total=len(found))

    def export(self, limit=5000):
        """Proposals with append-only provenance for the supplier-independent export, and whether the limit cut them off."""
        if not self.sql:
            return dict(proposals=[], total=0, truncated=False, supported=False,
                        note="Assistant proposals are durable SQL only; this JSON store holds none, so none are exported.")
        with self.transaction() as db:
            ids = [r[0] for r in db.execute("SELECT id FROM assistant_tasks ORDER BY id").fetchall()]
            out = []
            for tid in ids[:limit]:
                body = self._row(db, tid)
                events = [json.loads(r[0]) for r in db.execute("SELECT body FROM assistant_events WHERE task_id=? ORDER BY at,id", (tid,)).fetchall()]
                s = continuity.active(self.continuity(db), body["capability"])
                out.append(dict(body, provenance=events, relied_on=body["state"] == "accepted" and not s and not self.admission(db, body["capability"]),
                                suspension=s["id"] if s else None))
            return dict(proposals=out, total=len(ids), truncated=len(ids) > limit, supported=True, limit=limit)

    def disabled(self, db=None, capability=None):
        l = self.limits
        if self.schema_error:
            return self.schema_error
        if not self.sql:
            return "Durable SQL is required; use the ordinary case/manual route."
        if not l.valid:
            return l.error
        if db is not None and (held := self.suspended(db, capability)):
            return held
        if db is not None and capability and (denied := self.admission(db, capability)):
            return denied["reason"]
        if db is not None and self.now(db) >= l.expiry:
            return "Operator authority/allowance has expired."
        if not self.store.ai.configured:
            return "AI is not configured; use the manual owner route."
        if db is not None:
            pool = db.execute("SELECT calls,tokens,expires,used_calls,reserved_tokens FROM assistant_allowance WHERE id=?", (l.pool,)).fetchone()
            if pool and (pool[2] <= self.now(db) or pool[3] >= min(pool[0], l.calls) or
                         pool[4] + l.reservation > min(pool[1], l.tokens)):
                return "Shared durable allowance exhausted/expired; use the manual owner route."
        return None

    def registry(self, user):
        if user.get("role") not in projection.STAFF_ROLES:
            raise PermissionError("Staff assistance only.")
        if not self.sql:
            return dict(assistants=[dict(id=k, version=VERSION, **v) for k, v in REGISTRY.items()
                                    if user.get("role") in v["roles"]], disabled=self.disabled(),
                        proactive=False, manual="Use the ordinary case controls.")
        with self.transaction() as db:
            result = []
            for k, v in REGISTRY.items():
                if user.get("role") in v["roles"]:
                    self.authorize(db, user, k)
                    denied = self.admission(db, k)
                    result.append(dict(id=k, version=VERSION, release="in force" if not denied else denied,
                                       binding=runtime_binding(k, self.store.ai), **v))
            return dict(assistants=result, disabled=self.disabled(db), proactive=self.limits.proactive,
                        principal=PURPOSE, rule=RULE_VERSION, limits=Limits.DEFAULTS if not self.limits.valid else
                        {k: getattr(self.limits, k) for k in Limits.DEFAULTS},
                        manual="Use the ordinary case controls; proposals never approve or change the case.")

    def _enqueue(self, db, capability, c, mode, actor):
        snapshot = self.snapshot(db, capability, c)
        signature = digest(snapshot)
        identity = proposal_identity(capability)
        tid = digest([capability, VERSION, c["id"], signature, identity])
        row = db.execute("SELECT body FROM assistant_tasks WHERE id=?", (tid,)).fetchone()
        if row is None:
            reason = self.disabled(db, capability)
            body = dict(id=tid, capability=capability, version=VERSION, case_id=c["id"], proposal_identity=identity,
                        source_signature=signature, snapshot=snapshot, output=None, verification=None, review=None, envelope=None,
                        manual=f"Review the ordinary case with {', '.join(REGISTRY[capability]['roles'])}.",
                        reason=reason, created_at=self.now(db))
            state = "disabled" if reason else "pending"
            if self.limits.valid and len(canonical(snapshot)) > self.limits.input_chars - 1500:
                state, body["reason"] = "failed", "Source capture exceeds bounded input. Review manually."
            db.execute("INSERT INTO assistant_tasks (id,capability,case_id,signature,body,state,fence,owner,lease_until,attempts,not_before,revision) VALUES (?,?,?,?,?,?,0,'',0,0,0,1)",
                       (tid, capability, c["id"], signature, canonical(body), state))
        elif not self.disabled(db, capability):
            task = self._row(db, tid)
            if task["state"] == "disabled" and task["attempts"] < self.limits.attempts:
                task["reason"] = None
                db.execute("UPDATE assistant_tasks SET state='pending',body=?,revision=revision+1 WHERE id=?",
                           (canonical(task), tid))
        self.event(db, tid, kind="invocation", mode=mode, actor=actor, purpose=PURPOSE if mode == "proactive" else None,
                   rules=RULE_VERSION)
        return tid

    def invoke(self, user, capability, case_id):
        if not isinstance(case_id, str) or not 1 <= len(case_id) <= 64:
            raise ValueError("Choose a bounded case ID.")
        if not self.sql:
            raise ValueError(self.disabled())
        with self.transaction() as db:
            c = self.authorize(db, user, capability, case_id)
            tid = self._enqueue(db, capability, c, "reactive", user["email"])
        return self.detail(user, tid)

    def _row(self, db, tid):
        row = db.execute("SELECT body,state,fence,owner,lease_until,attempts,not_before,revision FROM assistant_tasks WHERE id=?", (tid,)).fetchone()
        if row is None:
            raise KeyError(tid)
        body = json.loads(row[0])
        body.update(state=row[1], fence=row[2], owner=row[3], lease_until=row[4],
                    attempts=row[5], not_before=row[6], revision=row[7])
        return body

    def _view(self, db, user, tid, history_offset=0):
        body = self._row(db, tid)
        c = self.authorize(db, user, body["capability"], body["case_id"])
        body["stale"] = digest(self.snapshot(db, body["capability"], c)) != body["source_signature"]
        history_limit = 50
        query = "SELECT body FROM assistant_events WHERE task_id=? ORDER BY at DESC,id DESC"
        query += " OFFSET ? ROWS FETCH NEXT ? ROWS ONLY" if self.mssql else " LIMIT ? OFFSET ?"
        args = (tid, history_offset, history_limit) if self.mssql else (tid, history_limit, history_offset)
        body["provenance"] = list(reversed([json.loads(r[0]) for r in db.execute(query, args).fetchall()]))
        total = db.execute("SELECT COUNT(*) FROM assistant_events WHERE task_id=?", (tid,)).fetchone()[0]
        body["history_next_offset"] = history_offset + history_limit if total > history_offset + history_limit else None
        body["history_count"] = total
        body["display_state"] = "stale" if body["stale"] else body["state"]
        held = continuity.active(self.continuity(db), body["capability"])
        body["release_denial"] = self.admission(db, body["capability"])
        body["actionable"] = held is None and body["state"] not in ("quarantined", "disabled") and not body["release_denial"]
        body["suspension"] = held["id"] if held else None
        if held:
            body["display_state"] = "suspended"
        elif body["release_denial"]:
            body["display_state"] = "release-denied"
        return body

    def detail(self, user, tid, history_offset=0):
        if not self.sql:
            raise ValueError(self.disabled())
        if type(history_offset) is not int or not 0 <= history_offset <= 1000000:
            raise ValueError("Invalid bounded history offset.")
        with self.transaction() as db:
            return self._view(db, user, tid, history_offset)

    def listing(self, user, case_id=None, after=""):
        if case_id is not None and (not isinstance(case_id, str) or not 1 <= len(case_id) <= 64):
            raise ValueError("Choose a bounded case ID.")
        if not isinstance(after, str) or (after and (len(after) != 64 or any(c not in "0123456789abcdef" for c in after))):
            raise ValueError("Invalid proposal cursor.")
        if user.get("role") not in projection.STAFF_ROLES:
            raise PermissionError("Staff assistance only.")
        if not self.sql:
            return dict(proposals=[], disabled=self.disabled())
        with self.transaction() as db:
            permitted = [k for k, v in REGISTRY.items() if user.get("role") in v["roles"]]
            current = None
            for cap in permitted:
                current = self.authorize(db, user, cap)
            if not permitted:
                return dict(proposals=[], disabled="No assistant belongs to this role.")
            where = "WHERE capability IN (" + ",".join("?" for _ in permitted) + ")"
            args = tuple(permitted)
            if case_id:
                where += " AND case_id=?"
                args += (case_id,)
            for field in ("case_ids", "areas"):
                values = current.get(field)
                if values is not None:
                    if not values:
                        return dict(proposals=[], disabled=self.disabled(db), next_after=None)
                    if field == "case_ids":
                        where += " AND case_id IN (" + ",".join("?" for _ in values) + ")"
                    else:
                        where += " AND case_id IN (SELECT id FROM cases WHERE area IN (" + ",".join("?" for _ in values) + "))"
                    args += tuple(values)
            if after:
                where += " AND id>?"
                args += (after,)
            query = f"SELECT id,capability FROM assistant_tasks {where} ORDER BY id"
            if self.mssql:
                query += " OFFSET 0 ROWS FETCH NEXT 50 ROWS ONLY"
            else:
                query += " LIMIT 50"
            results = []
            rows = db.execute(query, args).fetchall()
            for tid, cap in rows:
                if cap in permitted:
                    try:
                        results.append(self._view(db, user, tid))
                    except PermissionError:
                        continue
            return dict(proposals=results, disabled=self.disabled(db), manual="Open the case for ordinary human work.",
                        next_after=rows[-1][0] if len(rows) == 50 else None)

    def scan(self):
        if not self.sql or not self.limits.proactive:
            return dict(enqueued=[], disabled="Proactive assistance is off.")
        if not self.scan_lock.acquire(blocking=False):
            return dict(enqueued=[], disabled="Scan already in progress.")
        try:
            with self.transaction() as db:
                reason = self.disabled(db)
                if reason:
                    return dict(enqueued=[], disabled=reason)
                query = "SELECT id,body FROM cases WHERE id>? AND closed=0 ORDER BY id"
                query += " OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY" if self.mssql else " LIMIT ?"
                rows = db.execute(query, (self.scan_cursor, self.limits.scan_size)).fetchall()
                self.scan_cursor = rows[-1][0] if len(rows) == self.limits.scan_size else ""
                today = datetime.fromtimestamp(self.now(db), timezone.utc).date().isoformat()
                result = []
                for cid, raw in rows:
                    c = json.loads(raw)
                    for cap in REGISTRY:
                        if self.suspended(db, cap):
                            continue
                        s = self.snapshot(db, cap, c)
                        signatures = db.execute("SELECT signature FROM assistant_tasks WHERE capability=? AND case_id=?",
                                                (cap, cid)).fetchall()
                        changed = bool(signatures) and digest(s) not in {r[0] for r in signatures}
                        if eligible(cap, s, today, changed):
                            result.append(self._enqueue(db, cap, c, "proactive", PURPOSE))
                return dict(enqueued=result, disabled=None)
        finally:
            self.scan_lock.release()

    def claim(self, tid, owner):
        with self.transaction() as db:
            task, now, l = self._row(db, tid), self.now(db), self.limits
            if task["state"] not in ("pending", "leased") or task["not_before"] > now or (task["state"] == "leased" and task["lease_until"] > now):
                return None
            if task["attempts"] >= l.attempts:
                task["reason"] = "Attempts exhausted; use the manual owner route."
                db.execute("UPDATE assistant_tasks SET state='failed',body=?,revision=revision+1 WHERE id=?", (canonical(task), tid))
                self.event(db, tid, kind="exhausted", outcome="attempts-exhausted")
                return None
            reason = self.disabled(db, task["capability"])
            if reason:
                task["reason"] = reason
                db.execute("UPDATE assistant_tasks SET state='disabled',body=?,revision=revision+1 WHERE id=?", (canonical(task), tid))
                self.event(db, tid, kind="disabled", reason=reason)
                return None
            row = db.execute("SELECT body FROM cases WHERE id=?", (task["case_id"],)).fetchone()
            if row is None or digest(self.snapshot(db, task["capability"], json.loads(row[0]))) != task["source_signature"]:
                task["reason"] = "Permitted source changed; request a new proposal or work manually."
                db.execute("UPDATE assistant_tasks SET state='stale',body=?,revision=revision+1 WHERE id=?", (canonical(task), tid))
                self.event(db, tid, kind="stale", reason=task["reason"])
                return None
            active = db.execute("SELECT COUNT(*) FROM assistant_attempts WHERE active_until>?", (now,)).fetchone()[0]
            if active >= l.active_calls:
                reason = "Waiting for a shared active-call slot; ordinary manual case work remains available."
                if task["reason"] != reason:
                    task["reason"] = reason
                    db.execute("UPDATE assistant_tasks SET body=?,revision=revision+1 WHERE id=?", (canonical(task), tid))
                    self.event(db, tid, kind="throttled", reason=reason)
                return None
            pool = db.execute("SELECT calls,tokens,expires,used_calls,reserved_tokens FROM assistant_allowance WHERE id=?", (l.pool,)).fetchone()
            if pool is None:
                db.execute("INSERT INTO assistant_allowance (id,calls,tokens,expires,used_calls,reserved_tokens) VALUES (?,?,?,?,0,0)",
                           (l.pool, l.calls, l.tokens, l.expiry))
                pool = (l.calls, l.tokens, l.expiry, 0, 0)
            # Same authority cannot extend expiry or increase allowance by restarting/config changes.
            calls, tokens, expiry = min(pool[0], l.calls), min(pool[1], l.tokens), min(pool[2], l.expiry)
            db.execute("UPDATE assistant_allowance SET calls=?,tokens=?,expires=? WHERE id=?", (calls, tokens, expiry, l.pool))
            if expiry <= now or pool[3] >= calls or pool[4] + l.reservation > tokens:
                task["reason"] = "Shared durable allowance exhausted/expired; use manual route."
                db.execute("UPDATE assistant_tasks SET state='disabled',body=?,revision=revision+1 WHERE id=?", (canonical(task), tid))
                self.event(db, tid, kind="disabled", reason="Shared durable allowance exhausted/expired; use manual route.")
                return None
            fence = task["fence"] + 1
            task["reason"] = None
            task["claim_epoch"] = self.continuity(db)["epoch"]
            task["claim_binding"] = digest(runtime_binding(task["capability"], self.store.ai))
            result = db.execute("UPDATE assistant_tasks SET state='leased',body=?,owner=?,fence=?,lease_until=?,attempts=attempts+1,revision=revision+1 WHERE id=? AND fence=? AND revision=?",
                                (canonical(task), owner, fence, now + l.lease, tid, task["fence"], task["revision"]))
            if result.rowcount != 1:
                raise ConflictError(tid)
            db.execute("UPDATE assistant_allowance SET used_calls=used_calls+1,reserved_tokens=reserved_tokens+? WHERE id=?", (l.reservation, l.pool))
            db.execute("INSERT INTO assistant_attempts (id,task_id,fence,pool,reserved,actual,outcome,active_until) VALUES (?,?,?,?,?,NULL,'reserved',?)",
                       (f"{tid}:{fence}", tid, fence, l.pool, l.reservation, now + l.lease))
            self.event(db, tid, kind="claimed", owner=owner, fence=fence, reservation=l.reservation,
                       authority_reference=l.authority)
            return self._row(db, tid)

    def renew(self, tid, owner, fence):
        with self.transaction() as db:
            now = self.now(db)
            renewed = db.execute("UPDATE assistant_tasks SET lease_until=? WHERE id=? AND owner=? AND fence=? AND state='leased' AND lease_until>?",
                                 (now + self.limits.lease, tid, owner, fence, now)).rowcount == 1
            if renewed:
                db.execute("UPDATE assistant_attempts SET active_until=? WHERE id=?", (now + self.limits.lease, f"{tid}:{fence}"))
            return renewed

    def complete(self, task, envelope, output, failure=None):
        if output is not None:
            try:
                if envelope.get("source") != "ai" or envelope.get("outcome") != "returned":
                    raise ValueError("Unverified provider outcome.")
                output = validate_output(output, task["snapshot"], self.limits.output_chars)
            except (ValueError, TypeError, KeyError):
                output, failure = None, "Invalid/unverified proposal; use manual work."
        with self.transaction() as db:
            current, now = self._row(db, task["id"]), self.now(db)
            if current["state"] != "leased" or current["owner"] != task["owner"] or current["fence"] != task["fence"] or current["lease_until"] <= now:
                return False
            epoch = self.continuity(db)["epoch"]
            denied = self.admission(db, current["capability"])
            binding = digest(runtime_binding(current["capability"], self.store.ai))
            quarantined = epoch != current.get("claim_epoch", epoch) or bool(self.suspended(db, current["capability"])) or bool(
                denied) or binding != current.get("claim_binding", binding)
            if not quarantined and envelope.get("outcome") == "returned":
                # A deployment alias is not immutable. This only compares the model name the provider returned with the released one;
                # it is a returned-model check, not authoritative attestation of what served the call.
                released = [r for r in rel.releases(db, current["capability"]) if r["status"] == "active"]
                if not any(r.get("serving_model") == envelope.get("model") for r in released):
                    quarantined = True
                    for r in released:
                        rel.change(db, now, None, r["id"], "suspended",
                                   "Returned model name differs from the released one (returned-model check, not attestation); results quarantined.", system=True)
                    current["serving_attestation"] = dict(returned=envelope.get("model"), outcome="mismatch")
            held_output = output
            if quarantined:
                # The call may have been charged; its result is kept as a digest only and never becomes a proposal.
                output = None
                failure = failure or "Late result quarantined after a suspension, restart, release change or serving-version mismatch; use manual work."
                current["quarantine"] = dict(epoch=epoch, claim_epoch=current.get("claim_epoch"),
                                             output_digest=digest(held_output) if held_output is not None else None)
            current.update(envelope=envelope, output=output, reason=failure,
                           verification=None, review=None)
            state = "quarantined" if quarantined else "ready" if output is not None and not failure else (
                "pending" if envelope.get("outcome") in ("timeout", "provider-unavailable") and current["attempts"] < self.limits.attempts else "failed")
            delay = self.limits.backoff * current["attempts"] if state == "pending" else 0
            result = db.execute("UPDATE assistant_tasks SET body=?,state=?,not_before=?,lease_until=0,revision=revision+1 WHERE id=? AND owner=? AND fence=? AND state='leased' AND lease_until>?",
                                (canonical(current), state, now + delay, task["id"], task["owner"], task["fence"], now))
            if result.rowcount != 1:
                return False
            usage = envelope.get("usage")
            actual = usage.get("total_tokens") if isinstance(usage, dict) else None
            attempt = db.execute("SELECT pool,reserved FROM assistant_attempts WHERE id=?", (f"{task['id']}:{task['fence']}",)).fetchone()
            if type(actual) is int and 0 <= actual <= attempt[1]:
                db.execute("UPDATE assistant_allowance SET reserved_tokens=reserved_tokens-? WHERE id=?",
                           (attempt[1] - actual, attempt[0]))
            else:
                actual = None
            db.execute("UPDATE assistant_attempts SET actual=?,outcome=? WHERE id=?",
                       (actual, str(envelope.get("outcome", "unknown"))[:40], f"{task['id']}:{task['fence']}"))
            if envelope.get("outcome") not in ("timeout", "provider-unavailable"):
                db.execute("UPDATE assistant_attempts SET active_until=0 WHERE id=?", (f"{task['id']}:{task['fence']}",))
            self.event(db, task["id"], kind="completed", state=state, fence=task["fence"], envelope=envelope,
                       actual_tokens=actual, reservation_liability=attempt[1] if actual is None else actual,
                       output=output, source_signature=task["source_signature"],
                       capability=task["capability"], version=task["version"])
            return True

    def execute(self, tid):
        if self.stop_event.is_set():
            return False
        if not self.call_slots.acquire(blocking=False):
            return False
        owner = uuid.uuid4().hex
        try:
            try:
                task = self.claim(tid, owner)
            except Exception:
                # Lookup, never replay a possibly acknowledged reservation.
                with self.transaction() as db:
                    task = self._row(db, tid)
                    if task["owner"] != owner or task["state"] != "leased" or task["lease_until"] <= self.now(db):
                        raise
        except BaseException:
            self.call_slots.release()
            raise
        if task is None:
            self.call_slots.release()
            return False
        system, prompt = build_request(task)
        if len(system) + len(prompt) > self.limits.input_chars:
            self.call_slots.release()
            return self.complete(task, dict(outcome="input-too-large", usage=None, source="unverified"),
                                 None, "Input exceeds limit; manual review required.")
        started = time.perf_counter()
        returned, values = threading.Event(), []

        def call():
            try:
                values.append(self.provider(system, prompt, self.limits.output_tokens, self.limits.timeout))
            except Exception:
                values.append(dict(outcome="provider-unavailable", usage=None, source="unverified", text=None))
            finally:
                # A timed-out physical call continues owning its local slot until it returns.
                self.call_slots.release()
                returned.set()
        with self.transaction() as db:
            held = self.suspended(db, task["capability"]) or (self.admission(db, task["capability"]) or {}).get("reason")
        if held:
            self.call_slots.release()
            return self.complete(task, dict(outcome="suspended-before-dispatch", usage=None, source="unverified"), None, held)
        try:
            with self.dispatch_lock:
                stopped = self.stop_event.is_set()
                if not stopped:
                    threading.Thread(target=call, daemon=True, name="retrofit-provider").start()
        except RuntimeError:
            self.call_slots.release()
            return self.complete(task, dict(outcome="provider-unavailable", usage=None, source="unverified"),
                                 None, "Provider dispatch unavailable; use manual work.")
        if stopped:
            self.call_slots.release()
            return self.complete(task, dict(outcome="shutdown", usage=None, source="unverified"),
                                 None, "Assistance stopped before dispatch; use manual work.")
        while not returned.wait(0.1):
            if self.stop_event.is_set() or time.perf_counter() - started >= self.limits.timeout:
                break
        result = values[0] if returned.is_set() and time.perf_counter() - started <= self.limits.timeout else dict(
            outcome="timeout", usage=None, source="unverified", text=None)
        envelope, output, failure = shape_result(task, result, self.limits)
        try:
            return self.complete(task, envelope, output, failure)
        except Exception:
            # Completion acknowledgement may have been lost. Never dispatch the provider again here.
            with self.transaction() as db:
                current = self._row(db, tid)
                return current["fence"] == task["fence"] and current["state"] in ("ready", "failed", "pending")

    def review(self, user, tid, action, revision, note="", output=None, source_verified=False):
        if not self.sql:
            raise ValueError(self.disabled())
        if action not in ("verify", "accept", "edit-accept", "reject"):
            raise ValueError("Choose verify, accept, edit-accept or reject.")
        if not isinstance(note, str) or not 1 <= len(note.strip()) <= 1000:
            raise ValueError("Record a bounded source verification/review note.")
        with self.transaction() as db:
            task = self._view(db, user, tid)
            if type(revision) is not int or revision != task["revision"]:
                raise ConflictError(tid)
            if action != "reject":
                if task["suspension"]:
                    raise PermissionError(self.suspended(db, task["capability"]))
                if task["release_denial"]:
                    raise PermissionError(task["release_denial"]["reason"])
                if task["stale"] or task["state"] != "ready" or task["output"] is None or task["envelope"].get("source") != "ai":
                    raise ValueError("Only current, valid AI proposals can be verified/accepted. Use manual work or reject.")
                validate_output(task["output"], task["snapshot"], self.limits.output_chars)
                c = self.authorize(db, user, task["capability"], task["case_id"])
                if task["capability"] == "quality-evidence":
                    current_actor = self.authorize(db, user, task["capability"])
                    for rec in c.get("quality", []):
                        self.store._independent(rec, current_actor, "review quality evidence")
                if action == "verify":
                    if source_verified is not True:
                        raise ValueError("Explicit human source verification is required.")
                    task["verification"] = dict(by=user["email"], signature=task["source_signature"], note=note, at=self.now(db))
                else:
                    verification = task.get("verification")
                    if not verification or verification["by"] != user["email"] or verification["signature"] != task["source_signature"]:
                        raise ValueError("Record your human source verification before accept/edit.")
                    if action == "edit-accept":
                        task["output"] = validate_output(output, task["snapshot"], self.limits.output_chars)
                    task["review"] = dict(action=action, by=user["email"], note=note, at=self.now(db))
            else:
                task["review"] = dict(action=action, by=user["email"], note=note, at=self.now(db))
            state = task["state"] if action == "verify" else ("rejected" if action == "reject" else "accepted")
            task.pop("provenance", None)
            for key in ("history_next_offset", "history_count", "display_state", "stale", "actionable", "suspension", "release_denial"):
                task.pop(key, None)
            res = db.execute("UPDATE assistant_tasks SET body=?,state=?,revision=revision+1 WHERE id=? AND revision=?",
                             (canonical(task), state, tid, revision))
            if res.rowcount != 1:
                raise ConflictError(tid)
            self.event(db, tid, kind="review", action=action, reviewer=user["email"], note=note,
                       source_verified=action == "verify", source_signature=task["source_signature"],
                       edited_output=task["output"] if action == "edit-accept" else None)
        return self.detail(user, tid)

    def _worker(self):
        while not self.stop_event.is_set():
            delay = 1
            try:
                with self.transaction() as db:
                    now = self.now(db)
                    query = "SELECT id FROM assistant_tasks WHERE (state='pending' AND not_before<=?) OR (state='leased' AND lease_until<=?) ORDER BY id"
                    query += " OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY" if self.mssql else " LIMIT 1"
                    row = db.execute(query, (now, now)).fetchone()
                if row:
                    if self.execute(row[0]):
                        continue
            except Exception:
                LOG.warning("Retrofit assistant worker failed; manual work remains available; bounded retry pending.")
                delay = self.limits.backoff
            self.stop_event.wait(delay)

    def _scanner(self):
        while not self.stop_event.is_set():
            try:
                self.scan()
            except Exception:
                LOG.warning("Retrofit assistant scan failed; manual work remains available; next bounded scan pending.")
            self.stop_event.wait(self.limits.scan_interval)

    def start(self):
        if self.threads or not self.sql or not self.limits.valid:
            return
        self.stop_event.clear()
        for target in [self._worker] * self.limits.active_calls + ([self._scanner] if self.limits.proactive else []):
            t = threading.Thread(target=target, daemon=True, name="retrofit-assistant")
            self.threads.append(t)
            t.start()

    def stop(self):
        with self.dispatch_lock:
            self.stop_event.set()
        for t in self.threads:
            t.join(timeout=0.2)
        # A bounded network call may still finish; SQL fencing/expiry owns correctness.
