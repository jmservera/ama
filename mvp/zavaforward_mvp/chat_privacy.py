"""Privacy controls for per-user chat and memory (ADR 0004, GitHub #163). Built, but inactive.

No chat feature exists yet. This module holds what the DPIA needs to be testable
before any real use, and nothing in it decides a legal question:

* DATA_MAP: every place chat and memory content can land (messages, memory
  items, prompts sent to the model, logs) with its retention status.
* Decision record: lawful basis, staff notice and DPIA are references recorded
  by the DPO and Legal (CHAT_DPIA_REF, CHAT_LAWFUL_BASIS_REF, CHAT_NOTICE_REF).
  A bare yes is not a reference. Until all three exist, storing is refused.
* Retention: no period is set until CHAT_RETENTION_REF and CHAT_RETENTION_DAYS
  are both present. Without them nothing expires and the value is Unknown.
* Storage: threads and messages live in the #160 chat repository (chatthreads.py),
  keyed by its owner column. Only chat_memory is added here, in the same dialect
  hooks, so the same code runs on SQLite and Azure SQL.
* Rights: locate, export and erase a user's threads, messages and memory by
  server-derived user key. The erase counts are returned for the audit ledger,
  which holds metadata only.
* Redaction: free text is masked for obvious identifiers and special-category
  cues before storage. It is best effort, not a guarantee, so the warning stays.
* Logging: diagnostic output may carry counts and ids, never content.

Tests use labelled synthetic values only. Open items stay with the DPO and Legal
in docs/reference/research/chat-memory-dpia.md.
"""
import os
import re
import uuid
from datetime import datetime, timedelta, timezone

from .chatthreads import MAX_CONTENT, user_key

WARNING = ("Do not type health, disability, safeguarding, religion, ethnicity, sexual orientation, trade union, criminal, "
           "financial hardship or other special-category details, and do not paste resident contact details. Use the case record "
           "instead. Matching text is masked before it is saved, but masking can miss things.")
REDACTION_VERSION = "draft-1"

PATTERNS = (
    ("email", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")),
    ("phone", re.compile(r"(?<!\w)(?:\+44\s?|0)\d(?:[\s-]?\d){8,10}(?!\w)")),
    ("ni_number", re.compile(r"\b[A-CEGHJ-PR-TW-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D]\b", re.I)),
    ("postcode", re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b", re.I)),
    ("special_category", re.compile(r"\b(?:diagnos\w*|disabilit\w*|dementia|cancer|asthma|copd|mental health|depress\w*|safeguard\w*|"
                                    r"vulnerab\w*|pregnan\w*|religio\w*|muslim|christian|jewish|hindu|sikh|ethnic\w*|sexual orientation|"
                                    r"trade union|criminal\w*|convict\w*|benefits claimant)\b", re.I)),
)

DATA_MAP = (
    dict(id="message", data="Chat messages typed by staff and assistant replies", subjects="Staff; residents named in case text",
         location="Azure SQL chat_message via chat_thread owner, uksouth", sensitivity="Personal data; may hold resident data typed in free text",
         retention="Unknown until DPO approval", rights="Locate, export, erase by user key"),
    dict(id="thread", data="Thread header: owner, case, task, time", subjects="Staff", location="Azure SQL chat_thread (owner column), uksouth",
         sensitivity="Personal data", retention="Unknown until DPO approval", rights="Locate, export, erase by user key"),
    dict(id="memory", data="Opt-in memory items (off by default)", subjects="Staff", location="Azure SQL chat_memory, uksouth, owner-filtered",
         sensitivity="Personal data; never special-category or consent data", retention="Unknown until DPO approval; expiry required",
         rights="Locate, export, edit, erase by user key"),
    dict(id="prompt", data="Prompt assembled per turn: own thread, own memory, projected case data", subjects="Staff; residents in case text",
         location="Sent to the Azure OpenAI deployment in uksouth; not stored by Zava", sensitivity="Personal data in transit",
         retention="Not stored by Zava. Provider abuse-monitoring and retention terms Unknown, to be recorded by the DPO",
         rights="Nothing held by Zava to erase; provider terms are an open item"),
    dict(id="diagnostic_log", data="Application diagnostics", subjects="Staff", location="Process output and Azure Monitor",
         sensitivity="Must hold no chat or memory content", retention="Per platform log policy", rights="Not applicable: no content held"),
    dict(id="audit_ledger", data="Event metadata: who, what, when, counts", subjects="Staff", location="Append-only audit ledger",
         sensitivity="Metadata only, no content, so erasure does not break tamper evidence", retention="Per ledger policy",
         rights="Metadata retained; DPO to confirm"),
)

MODEL_PROVIDER_POSITION = dict(
    provider="Azure OpenAI through the existing Foundry deployments (ADR 0001 to ADR 0003)", region="uksouth (owner decision 2026-10-15)",
    zava_stores_prompts=False, foundry_agent_memory=False,
    open_items=("Provider data processing terms, abuse-monitoring retention and any opt-out must be retrieved and recorded by the DPO "
                "from current Microsoft terms; not verified here.",
                "International transfer position, if any, stays Unknown until the DPO records it."))

DIAGNOSTIC_FIELDS = frozenset({"thread_id", "user_key", "case_id", "task", "role", "count", "status", "at", "event", "latency_ms"})
def redact(text):
    """Return (masked text, sorted kinds found). Masking is best effort."""
    kinds = set()
    for kind, rx in PATTERNS:
        text, n = rx.subn(f"[{kind} removed]", text)
        if n:
            kinds.add(kind)
    return text, sorted(kinds)


def diagnostic_safe(fields):
    """Drop everything except ids, counts and status from a diagnostic record. Content is never logged."""
    return {k: v for k, v in fields.items() if k in DIAGNOSTIC_FIELDS}


class ChatNotApproved(PermissionError):
    pass


class ChatPrivacy:
    """Privacy rules over the Store's chat repository (chatthreads.py, #160). Threads and messages are owned by the
    `owner` column there; only chat_memory is new. No tables or connections are created here."""

    def __init__(self, store, env=None):
        if not hasattr(store, "chat_repo"):
            raise TypeError("ChatPrivacy needs a Store with the chat repository.")
        self.store = store
        self.env = os.environ if env is None else env

    def _ref(self, key):
        return (self.env.get(key) or "").strip()

    def decision(self):
        """The recorded DPO and Legal decision. Storage stays refused until all three references exist."""
        refs = dict(dpia_ref=self._ref("CHAT_DPIA_REF"), lawful_basis_ref=self._ref("CHAT_LAWFUL_BASIS_REF"), notice_ref=self._ref("CHAT_NOTICE_REF"))
        missing = [k for k, v in refs.items() if not v]
        days = self._ref("CHAT_RETENTION_DAYS")
        retention_set = bool(self._ref("CHAT_RETENTION_REF")) and days.isdigit() and int(days) > 0
        return dict(refs=refs, approved=not missing, missing=missing, retention_days=int(days) if retention_set else None,
                    retention="Unknown: no period set until CHAT_RETENTION_REF and CHAT_RETENTION_DAYS are recorded" if not retention_set else f"{int(days)} days",
                    owner="Juan Manuel Servera (DPO, Legal and Compliance, 2026-10-15)",
                    performance_use="Prohibited: chat and memory content is excluded from performance measurement without a separate decision (RULE-026)")

    def _require(self):
        d = self.decision()
        if not d["approved"]:
            raise ChatNotApproved("Chat and memory storage is refused until the DPIA, lawful basis and staff notice references are recorded: "
                                  + ", ".join(d["missing"]))
        return d

    @staticmethod
    def _now():
        return datetime.now(timezone.utc).isoformat(timespec="milliseconds")

    def _expiry(self, d):
        if not d["retention_days"]:
            return None
        return (datetime.now(timezone.utc) + timedelta(days=d["retention_days"])).isoformat(timespec="milliseconds")

    def start_thread(self, user, case_id="", task=""):
        self._require()
        return self.store.chat_create_thread(user, case_id=case_id, task=task)["id"]

    def add_message(self, user, thread_id, role, content):
        """Store a redacted message in the caller's own thread. Returns the redaction kinds found, for the warning."""
        self._require()
        text, kinds = redact(str(content)[:MAX_CONTENT])
        self.store.chat_add_message(user, thread_id, role, text)
        return kinds

    def add_memory(self, user, content):
        """Opt-in memory. Refused outright if the text looks special-category, rather than stored masked."""
        d = self._require()
        owner = user_key(user)
        text, kinds = redact(str(content)[:1000])
        if "special_category" in kinds:
            raise ValueError("Memory must not hold special-category data. " + WARNING)
        m = dict(id="CM-" + uuid.uuid4().hex[:16], owner=owner, owner_role=str(user.get("role") or ""), content=text,
                 redactions=",".join(kinds), created_at=self._now(), expires_at=self._expiry(d))
        repo = self.store.chat_repo
        with repo.txn():
            repo.insert_memory(m)
            repo.commit()
        return m["id"]

    def _held(self, owner):
        repo = self.store.chat_repo
        return repo.list(owner, None), repo.memories(owner)

    def locate(self, user):
        """Rights request: counts and ids of everything held for this user key. Reads need no approval."""
        threads, memory = self._held(user_key(user))
        return dict(threads=[t["id"] for t in threads], messages=sum(t["message_count"] for t in threads), memory=[m["id"] for m in memory])

    def export(self, user):
        """Rights request (access): the user's own content, nobody else's."""
        owner, repo = user_key(user), self.store.chat_repo
        threads, memory = self._held(owner)
        msgs = [dict(thread_id=t["id"], role=m["role"], content=m["content"], at=m["created_at"])
                for t in sorted(threads, key=lambda t: t["created_at"]) for m in repo.messages(t["id"])]
        return dict(messages=msgs, memory=[dict(id=m["id"], content=m["content"], at=m["created_at"], expires_at=m["expires_at"]) for m in memory])

    def erase(self, user):
        """Rights request (erasure): delete the user's threads, messages and memory. Returns counts for a metadata-only audit event."""
        owner, repo = user_key(user), self.store.chat_repo
        with repo.txn():
            threads, memory = self._held(owner)
            for t in threads:
                repo.delete(t["id"])
            repo.delete_memories(owner)
            repo.commit()
        return dict(threads=len(threads), messages=sum(t["message_count"] for t in threads), memory=len(memory))

    def purge_expired(self, now=None):
        """Delete memory past its expiry. Nothing expires while no retention period is approved."""
        repo = self.store.chat_repo
        with repo.txn():
            n = repo.purge_memory(now or self._now())
            repo.commit()
        return n
