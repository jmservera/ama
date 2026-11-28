"""Case store: loading, views, actions, gates and the hash-chained audit log."""

import contextlib
import csv
import errno
import hashlib
import io
import json
import logging
import os
import re
import threading
import time
import uuid
from copy import deepcopy
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from . import (
    challenges,
    ai_tasks,
    ai_prompts,
    buildings,
    change_provenance,
    controls,
    export_fields,
    gates,
    identity,
    insights,
    ledger,
    projection,
    ranking,
    ranking_archive_blob,
    ranking_publication,
    stock,
    taskqueues,
    tokenomics,
)
from .finance import FinanceMixin
from .list_export import safe_cell
from .continuity import ContinuityMixin
from .governance import GovernanceMixin
from .grants import GrantMixin, grant_summary
from .resident_decisions import (
    ResidentDecisionMixin,
    measure_decision_view,
    redress_route_view,
    remember_first_contact,
    retention_schedule,
    resident_gate,
    resident_status,
)
from .signoffs import SignoffMixin, missing_items, technical_gate
from zava_forward.core.ai import Ai
from .chatthreads import ChatMixin
from .doc_controls import DocControlsMixin, is_available_case_document, open_scanner
from .exception_register import ExceptionRegisterMixin
from .import_refusals import ImportRefusalsMixin
from .documents import ACCEPTED, MAX_BYTES, open_document_store
from .procurement import ProcurementMixin
from .quality import QualityMixin, handover_blockers, quality_evidence_gate
from .workflows import MANAGER_ROLES, WorkflowMixin, handoff_view, hazard_view

if TYPE_CHECKING:
    from .complaints_route import ComplaintsReceiver

DECISIONS = ("Not yet asked", "Waiting", "Accepted", "Declined")
READY_STAGE = "Final checks before ordering"
BOOKED_STAGE = "Install booked"


def _handoff_clock():
    """Wall clock shared with the handoff queues, so a card and the waiting list judge one wait alike."""
    return datetime.now(UTC).isoformat(timespec="minutes")


class GateError(Exception):
    def __init__(self, reasons, rules=()):
        super().__init__("; ".join(reasons))
        self.reasons = reasons
        self.rules = [r.as_record() if isinstance(r, gates.GateRule) else r for r in rules]


class ConflictError(Exception):
    """Another writer changed the same record first, so this write was refused."""


class LedgerRelianceError(RuntimeError):
    """Audit ledger or sealed digest verification failed before reliance."""

    def __init__(self, message: str, report: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.report: dict[str, Any] = dict(report) if isinstance(report, dict) else {}
        self.problems: list[dict[str, Any]] = list(self.report.get("problems", []))


class Store(
    ChatMixin,
    WorkflowMixin,
    QualityMixin,
    ProcurementMixin,
    FinanceMixin,
    GrantMixin,
    SignoffMixin,
    ResidentDecisionMixin,
    GovernanceMixin,
    ContinuityMixin,
    DocControlsMixin,
    ExceptionRegisterMixin,
    ImportRefusalsMixin,
):
    if TYPE_CHECKING:
        # Injection point for tests and a future approved receiver; absent means the configured default.
        complaints_receiver: ComplaintsReceiver | None

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
            c.setdefault(
                "funding",
                dict(
                    route="Not decided",
                    status="Not started",
                    reference="",
                    draft="",
                    approved_by=None,
                ),
            )
        self.cases = {c["id"]: c for c in self.data["cases"]}
        self.staff = {s["email"].lower(): s for s in self.data["staff"]}
        self.last_hash = self._tail_hash()
        self.digest_dir = os.environ.get("ZF_DIGEST_DIR") or os.path.join(base, "digests")
        self.docs_dir = os.path.join(os.path.dirname(self.live_path), "docs")
        self.docstore = open_document_store(self.docs_dir)
        self.scanner = open_scanner(self.docstore)
        self.ai = Ai()
        self.ai.gate = lambda task, deployment=None: (
            self.continuity_block(task) or self.release_block(task, deployment)
        )
        self.version = 0
        self._briefings = {}
        self._briefing_busy: dict = {}
        self._ranks = None
        self.data.setdefault("recommendations", [])
        self.as_of = self.data.setdefault(
            "as_of", os.environ.get("ZF_AS_OF") or datetime.now().date().isoformat()
        )

    def release_denial(self, task, deployment=None):
        """Why a configured provider may not be called for task now, or None; a pure read that records nothing."""
        if not self.ai.configured:
            return None
        from . import assistant_release as rel

        return rel.denial(
            "durable SQL release records are required", ["SQL-owned release record"], task
        )["reason"]

    def release_block(self, task, deployment=None):
        reason = self.release_denial(task, deployment)
        if reason:
            self.audit("system", "ai_release_denied", "-", reason)
        return reason

    def release_context(self, task, deployment=None):
        return None

    def release_current(self, task, release, deployment=None):
        """Exact per-invocation reference; a replacement never authorizes an old output."""
        from .ai_registry import LEGACY, legacy_deployment

        if (
            task not in LEGACY
            or not isinstance(release, dict)
            or not all(
                isinstance(release.get(key), str) and release[key].strip()
                for key in ("id", "version", "digest")
            )
        ):
            return False
        current = legacy_deployment(task, self.ai)
        if deployment is not None and deployment != current:
            return False
        selected = self.release_context(task, current)
        return bool(selected) and release == selected

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

    def write_year_digests(self, *, before=None):
        """Seal every year before the current one. Sealed years are written once and never overwritten."""
        cutoff = (
            f"{datetime.now().year:04d}"
            if before is None
            else (f"{before:04d}" if type(before) is int else str(before))
        )
        with self.lock:
            return [
                ledger.write_year_digest(self.digest_dir, d)
                for d in ledger.year_digests(list(self.audit_entries()), before=cutoff)
            ]

    def _reliance_lock(self):
        return self.lock

    def _reliance_db_errors(self) -> tuple[type[BaseException], ...]:
        try:
            err = getattr(self, "dberror", None)
        except ImportError:
            return ()
        if isinstance(err, type) and issubclass(err, BaseException):
            return (err,)
        if isinstance(err, tuple) and all(
            isinstance(item, type) and issubclass(item, BaseException) for item in err
        ):
            return err
        return ()

    @staticmethod
    def _validate_audit_entry_shape(entry: Any, index: int) -> dict[str, Any] | None:
        if not isinstance(entry, dict):
            return dict(
                code="audit_entry_malformed",
                entry=index,
                year=None,
                reason="audit entry is not a mapping",
            )
        if not all(
            isinstance(entry.get(k), str)
            for k in ("at", "who", "action", "case", "detail", "prev", "hash")
        ):
            return dict(
                code="audit_entry_malformed",
                entry=index,
                year=None,
                reason="audit entry is missing required string fields",
            )
        year = entry["at"][:4]
        if not ledger.ASCII_YEAR_RE.fullmatch(year):
            return dict(
                code="audit_entry_malformed",
                entry=index,
                year=None,
                reason="audit entry timestamp lacks a four-digit ASCII year",
            )
        if not (
            ledger.HEX64_RE.fullmatch(entry["prev"])
            and ledger.HEX64_RE.fullmatch(entry["hash"])
        ):
            return dict(
                code="audit_entry_malformed",
                entry=index,
                year=year,
                reason="audit entry hash link is malformed",
            )
        return None

    def _reliance_audit_snapshot(self) -> tuple[list[dict[str, Any]], bool, list[dict[str, Any]]]:
        entries = list(self.audit_entries())
        for idx, entry in enumerate(entries, start=1):
            bad = self._validate_audit_entry_shape(entry, idx)
            if bad is not None:
                return [], False, [bad]
        actual_head = entries[-1]["hash"] if entries else ledger.GENESIS
        recorded_head = getattr(self, "last_hash", None)
        if isinstance(recorded_head, str) and actual_head != recorded_head:
            return (
                entries,
                False,
                [
                    dict(
                        code="audit_head_mismatch",
                        year=None,
                        reason="the chain differs from the recorded ledger head",
                    )
                ],
            )
        return entries, True, []

    def _invoke_write_year_digests(self, year_cutoff: str) -> list[str]:
        try:
            return list(self.write_year_digests(before=year_cutoff))
        except TypeError:
            return list(self.write_year_digests())

    @staticmethod
    def _clean_problem_year(raw: Any) -> str | None:
        if isinstance(raw, str):
            if ledger.ASCII_YEAR_RE.fullmatch(raw):
                return raw
            ym = ledger.YEAR_DIGEST_FILE_RE.fullmatch(raw)
            if ym and ledger.ASCII_YEAR_RE.fullmatch(ym.group(1)):
                return ym.group(1)
        return None

    @staticmethod
    def _dedupe_problems(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen: set[str] = set()
        out: list[dict[str, Any]] = []
        for item in items:
            key = json.dumps(item, sort_keys=True)
            if key not in seen:
                seen.add(key)
                out.append(item)
        return out

    def verify_ledger_before_reliance(
        self,
        *,
        require_sealed_past_years: bool = True,
        current_year: int | None = None,
        seal_past_years: bool = True,
    ) -> dict[str, Any]:
        """Seal intact past years and verify per-year chains, anchors, and heads before reliance."""
        if not isinstance(require_sealed_past_years, bool):
            raise ValueError("require_sealed_past_years must be a bool")
        if not isinstance(seal_past_years, bool):
            raise ValueError("seal_past_years must be a bool")
        if current_year is not None and (
            isinstance(current_year, bool)
            or not isinstance(current_year, int)
            or not 1 <= current_year <= 9999
        ):
            raise ValueError("current_year must be an integer between 1 and 9999")
        effective_year = datetime.now().year if current_year is None else current_year
        year_cutoff = f"{effective_year:04d}"
        recoverable = self._reliance_db_errors() + (
            OSError,
            ValueError,
            TypeError,
            KeyError,
            RuntimeError,
        )
        try:
            with self._reliance_lock():
                problems: list[dict[str, Any]] = []
                try:
                    entries, head_ok, snap_problems = self._reliance_audit_snapshot()
                except recoverable:
                    return dict(
                        reliance_allowed=False,
                        intact=False,
                        current_year=year_cutoff,
                        require_sealed_past_years=require_sealed_past_years,
                        entries=0,
                        head=ledger.GENESIS,
                        audit_head_matches=False,
                        digests_checked=0,
                        digest_mismatches=[],
                        years={},
                        sealed_years=[],
                        missing_years=[],
                        bad_digests=[],
                        sealed_digest_files=[],
                        problems=[
                            dict(
                                code="audit_unreadable",
                                year=None,
                                reason="audit entries could not be read",
                            )
                        ],
                    )
                problems.extend(snap_problems)
                if any(
                    p["code"] in ("audit_unreadable", "audit_entry_malformed")
                    for p in snap_problems
                ):
                    return dict(
                        reliance_allowed=False,
                        intact=False,
                        current_year=year_cutoff,
                        require_sealed_past_years=require_sealed_past_years,
                        entries=0,
                        head=ledger.GENESIS,
                        audit_head_matches=False,
                        digests_checked=0,
                        digest_mismatches=[],
                        years={},
                        sealed_years=[],
                        missing_years=[],
                        bad_digests=[],
                        sealed_digest_files=[],
                        problems=self._dedupe_problems(problems),
                    )

                root_digests, pre_year_digests, dir_problems = ledger.inspect_digest_directory(
                    self.digest_dir
                )
                problems.extend(dir_problems)
                chain_rep = ledger.verify_entries(entries, root_digests)
                if chain_rep["problem"] is not None:
                    cprob = chain_rep["problem"]
                    idx = int(cprob["entry"])
                    pyear = entries[idx - 1]["at"][:4] if 1 <= idx <= len(entries) else None
                    problems.append(
                        dict(
                            code="chain_tampered",
                            entry=idx,
                            year=pyear,
                            reason=str(cprob["reason"]),
                        )
                    )
                for mismatch in chain_rep["digest_mismatches"]:
                    problems.append(
                        dict(
                            code="root_digest_mismatch",
                            digest_count=int(mismatch["digest_count"]),
                            year=None,
                            reason=str(mismatch["reason"]),
                        )
                    )

                pre_year_rep = ledger.verify_years(entries, pre_year_digests)
                pre_year_intact = bool(pre_year_rep.get("intact"))
                written_files: list[str] = []
                if seal_past_years and not problems and pre_year_intact:
                    try:
                        written_files = [
                            os.path.basename(str(p))
                            for p in self._invoke_write_year_digests(year_cutoff)
                        ]
                    except recoverable:
                        problems.append(
                            dict(
                                code="year_digest_seal_failed",
                                year=None,
                                reason="completed past year digests could not be written",
                            )
                        )

                _, post_year_digests, post_dir_problems = ledger.inspect_digest_directory(
                    self.digest_dir
                )
                problems.extend(post_dir_problems)
                year_rep = ledger.verify_years(entries, post_year_digests)
                try:
                    hook_year_rep = self.verify_ledger_by_year()
                except recoverable:
                    problems.append(
                        dict(
                            code="year_verification_failed",
                            year=None,
                            reason="per-year ledger verification could not complete",
                        )
                    )
                else:
                    if not hook_year_rep.get("intact", False) and year_rep.get("intact", False):
                        year_rep = hook_year_rep

                for bad in year_rep.get("bad_digests", []):
                    byear = self._clean_problem_year(bad)
                    if not any(
                        p["code"] == "corrupt_year_digest" and p.get("year") == byear
                        for p in problems
                    ):
                        problems.append(
                            dict(
                                code="corrupt_year_digest",
                                year=byear,
                                reason="sealed year digest is unreadable, malformed, or duplicated",
                            )
                        )
                for missing_year in year_rep.get("missing_years", []):
                    problems.append(
                        dict(
                            code="missing_audit_year",
                            year=self._clean_problem_year(str(missing_year)),
                            reason="audit entries for a sealed year are missing",
                        )
                    )
                sealed_set = set(year_rep.get("sealed_years", []))
                for year, info in sorted(year_rep.get("years", {}).items()):
                    for reason in info.get("problems", []):
                        code = (
                            "year_digest_mismatch"
                            if "sealed digest" in reason
                            else (
                                "year_link_broken"
                                if "previous year" in reason
                                else "year_chain_tampered"
                            )
                        )
                        problems.append(dict(code=code, year=year, reason=str(reason)))
                    if (
                        require_sealed_past_years
                        and year < year_cutoff
                        and (not info.get("sealed") or year not in sealed_set)
                    ):
                        problems.append(
                            dict(
                                code="unsealed_past_year",
                                year=year,
                                reason="past year with audit entries has no sealed digest",
                            )
                        )

                deduped = self._dedupe_problems(problems)
                reliance_allowed = (
                    not deduped
                    and head_ok
                    and bool(chain_rep.get("intact"))
                    and bool(year_rep.get("intact"))
                )
                if not reliance_allowed and not deduped:
                    deduped.append(
                        dict(
                            code="ledger_verification_failed",
                            year=None,
                            reason="ledger verification did not pass",
                        )
                    )
                sanitized_bad = [
                    self._clean_problem_year(b) or "unreadable"
                    for b in year_rep.get("bad_digests", [])
                ]
                return dict(
                    reliance_allowed=reliance_allowed,
                    intact=reliance_allowed,
                    current_year=year_cutoff,
                    require_sealed_past_years=require_sealed_past_years,
                    entries=int(chain_rep["entries"]),
                    head=str(chain_rep["head"]),
                    audit_head_matches=head_ok,
                    digests_checked=int(chain_rep["digests_checked"]),
                    digest_mismatches=list(chain_rep["digest_mismatches"]),
                    years=dict(year_rep.get("years", {})),
                    sealed_years=list(year_rep.get("sealed_years", [])),
                    missing_years=list(year_rep.get("missing_years", [])),
                    bad_digests=sanitized_bad,
                    sealed_digest_files=written_files,
                    problems=deduped,
                )
        except recoverable:
            return dict(
                reliance_allowed=False,
                intact=False,
                current_year=year_cutoff,
                require_sealed_past_years=require_sealed_past_years,
                entries=0,
                head=ledger.GENESIS,
                audit_head_matches=False,
                digests_checked=0,
                digest_mismatches=[],
                years={},
                sealed_years=[],
                missing_years=[],
                bad_digests=[],
                sealed_digest_files=[],
                problems=[
                    dict(
                        code="audit_unreadable",
                        year=None,
                        reason="ledger state could not be read or verified",
                    )
                ],
            )

    def require_verified_ledger_for_reliance(
        self,
        *,
        require_sealed_past_years: bool = True,
        current_year: int | None = None,
        seal_past_years: bool = True,
    ) -> dict[str, Any]:
        """Verify ledger and sealed past-year digests before reliance, or raise `LedgerRelianceError`."""
        report = self.verify_ledger_before_reliance(
            require_sealed_past_years=require_sealed_past_years,
            current_year=current_year,
            seal_past_years=seal_past_years,
        )
        if not report["reliance_allowed"]:
            codes = ", ".join(
                sorted({str(p.get("code", "ledger_verification_failed")) for p in report["problems"]})
            ) or "ledger_verification_failed"
            raise LedgerRelianceError(
                f"Ledger verification failed before reliance ({codes}).",
                report,
            )
        return report

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
    def _open_safety_items(c, staff=None):
        unverified = [("Unverified safety evidence", "Building Safety Liaison")]
        if not isinstance(c, dict) or "hazards" not in c:
            return unverified
        hazards = c.get("hazards")
        if not isinstance(hazards, list):
            return unverified
        for h in hazards:
            if not isinstance(h, dict):
                return unverified
            rel = h.get("released")
            if rel is not None and type(rel) is not bool:
                return unverified
        if "safeguarding_items" in c:
            sg_items = c.get("safeguarding_items")
            if not isinstance(sg_items, list):
                return unverified
            for sg in sg_items:
                if gates._safeguarding_item_closed(sg) is None:
                    return unverified
        if "safeguarding" in c and c.get("safeguarding") is not None:
            legacy = c.get("safeguarding")
            if isinstance(legacy, list):
                for sg in legacy:
                    if gates._safeguarding_item_closed(sg) is None:
                        return unverified
            elif isinstance(legacy, dict):
                if (
                    set(legacy.keys()) & taskqueues.SAFEGUARDING_ITEM_KEYS
                    and gates._safeguarding_item_closed(legacy) is None
                ):
                    return unverified
            else:
                return unverified
        entries = []
        for h in hazards:
            if h.get("released") is not True:
                projected = taskqueues.project_safety_clock_and_owner(
                    h, case=c, staff=staff, default_kind="hazard"
                )
                entries.append(
                    (
                        h.get("category") or projected["category"],
                        projected["named_owner"],
                    )
                )
        for sg in taskqueues.raw_safeguarding_items(c):
            if gates._safeguarding_item_closed(sg) is not True:
                entries.append(
                    (sg.get("category") or "Safeguarding", taskqueues.ESCALATION_OWNER)
                )
        return entries

    @staticmethod
    def gate_reasons(c):
        why = []
        if c.get("funding_ok") is not True:
            why.append(
                f"Funding has not been confirmed. Owner: {c['owner']}. Next action: check the funding and record it."
            )
        open_h = Store._open_safety_items(c)
        if open_h:
            why.append(
                f"Home retrofit work is stopped for safety review. Owner: {open_h[0][1]} (referral follow-up). Next action: obtain external service evidence and an independent decision to restart retrofit work."
            )
        return why + resident_gate(c) + technical_gate(c)

    @staticmethod
    def _transition_rules(c):
        """Rules behind the pre-booking reasons, so a refusal names what it enforced."""
        rules = []
        if c.get("funding_ok") is not True:
            rules.append(gates.BOOKING_RULES["funding"])
        if Store._open_safety_items(c):
            rules.append(gates.BOOKING_RULES["safety"])
        if resident_gate(c):
            rules.append(gates.BOOKING_RULES["resident"])
        if technical_gate(c):
            rules.append(gates.TECHNICAL_RULE)
        return rules

    @staticmethod
    def status_line(c):
        if c["closed"]:
            return "Completed"
        open_h = Store._open_safety_items(c)
        if open_h:
            return f"Stopped until {open_h[0][1]} obtains evidence and an independent decision to restart retrofit work"
        if c["stage"] == READY_STAGE and not Store.gate_reasons(c):
            return "Ready"
        return f"Waiting on {c['waiting_on']} {c['reason']}"

    def summary(self, c):
        last = c["contacts"][-1]["at"] if c["contacts"] else None
        nxt = next(
            (a for a in c["appointments"] if isinstance(a, dict) and a.get("outcome") == "Booked"),
            None,
        )
        status = self.status_line(c)
        if status == "Ready" and buildings.blockers(self.data, self.cases, c):
            status = "Waiting on shared building review"
        return dict(
            id=c["id"],
            resident=c["resident"]["name"],
            address=c["home"]["address"],
            town=c["home"]["town"],
            postcode=c["home"]["postcode"],
            phone=c["resident"]["phone"],
            stage=c["stage"],
            status=status,
            owner=c["owner"],
            days=c["days_in_stage"],
            last_contact=last,
            next_visit=nxt["date"] if nxt else None,
            area=c["home"]["area"],
            wave=c["wave"],
            funding=c["funding"]["status"],
            owner_code=c["owner_code"],
            hazard=insights.has_hazard(c),
            safeguarding=taskqueues.has_open_safeguarding(c),
            support=stock.support_status(c["resident"]) == "Yes",
            support_status=stock.support_status(c["resident"]),
            support_coverage=stock.support_coverage(c["resident"]),
            closed=c["closed"],
        )

    def _ranking(self):
        """Ranking of all open cases for the current policy, rebuilt only when case data changes."""
        if self._ranks is None or self._ranks[0] != self.version:
            entries = ranking.rank(
                [c for c in self.cases.values() if not c["closed"]], ranking.CURRENT
            )
            self._ranks = (self.version, {e["id"]: e for e in entries})
        return self._ranks[1]

    def ranking_policy(self):
        return ranking.describe(ranking.CURRENT)

    def ranking_snapshot(self, user, policy=None):
        """Snapshot of the open-case ranking under a policy version, stored beside the data when it changes. Managers only."""
        if user["role"] not in MANAGER_ROLES:
            raise PermissionError(
                "Only a manager can see the saved ranking record. Owner: your manager. Next action: ask a manager to open it."
            )
        pol = ranking.POLICIES.get(policy or ranking.CURRENT["version"])
        if pol is None:
            raise ValueError(
                f"Unknown ranking policy version. Known: {', '.join(sorted(ranking.POLICIES))}"
            )
        with self.lock:
            cache = self.__dict__.setdefault("_snapcache", {})
            hit = cache.get(pol["version"])
            if hit and hit[0] == self.version:
                return hit[1]
            snap = ranking.snapshot(
                [c for c in self.cases.values() if not c["closed"]], pol, self.as_of
            )
            cache.clear()
            cache[pol["version"]] = (self.version, snap)
            path = os.path.join(
                os.path.dirname(getattr(self, "live_path", None) or self.db_path) or ".",
                f"ranking-snapshot-{pol['version']}.json",
            )
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

    def _ranking_archive(self):
        """The ranking archive: Azure Blob when ZF_RANKING_ARCHIVE=azure-blob (owner decision,
        issue 1258), else a local folder. The folder is a dev/test adapter only; its fsync is
        not evidence that a container persists a record. Blob selection never falls back."""
        blob = ranking_archive_blob.from_environment()
        if blob is not None:
            return blob
        return os.path.join(
            os.path.dirname(getattr(self, "live_path", None) or self.db_path) or ".",
            "ranking-archive",
        )

    def ranking_publication_status(self, user):
        """Retained-snapshot check for managers: count, problems, latest date, overdue flag and the stated schedule."""
        if user["role"] not in MANAGER_ROLES:
            raise PermissionError(
                "Only a manager can see the ranking publication record. Owner: your manager. Next action: ask a manager to open it."
            )
        try:
            archive = self._ranking_archive()
            out = ranking_publication.verify(archive)
        except ranking_archive_blob.BlobArchiveError as e:
            out = {
                "count": 0,
                "latest": None,
                "problems": [
                    f"The ranking archive cannot be read: {e}. "
                    "Owner: your operator. Next action: ask them to check the Blob archive configuration and access."
                ],
            }
        except OSError as e:
            out = {
                "count": 0,
                "latest": None,
                "problems": [
                    f"The archive folder cannot be read: {type(e).__name__}: {e.strerror or e}. "
                    "Owner: your manager. Next action: check the archive location and permissions."
                ],
            }
        out["overdue"] = out["latest"] is None or out["latest"] < controls.today()
        out["schedule"] = ranking_publication.SCHEDULE
        out["policy_signed"] = ranking.is_signed(ranking.CURRENT)
        out["signoff_problems"] = ranking.signoff_problems(ranking.CURRENT)
        return out

    @staticmethod
    def _log_retained_stage(error):
        retained = getattr(error, "stage_retained", None)
        if retained:
            logging.getLogger(__name__).warning(
                "Ranking archive temporary file %s was not removed", retained
            )
        return retained

    def publish_ranking_snapshot(self, user):
        """Archive today's snapshot under the current policy; a manager action, idempotent, audited, never rewrites an archived file."""
        if user["role"] not in MANAGER_ROLES:
            raise PermissionError(
                "Only a manager can publish the ranking record. Owner: your manager. Next action: ask a manager to publish it."
            )
        with self.lock:
            snap = self.ranking_snapshot(user)
            try:
                res = ranking_publication.publish(snap, self._ranking_archive(), controls.today())
            except ranking_publication.PublicationError as e:
                self._log_retained_stage(e)
                raise ValueError(str(e)) from e
            except ranking_publication.DurabilityUnconfirmedError as e:
                self._log_retained_stage(e)
                signed = ranking.is_signed(ranking.CURRENT)
                try:
                    self.audit(
                        user["email"],
                        "ranking_snapshot_publication_unconfirmed",
                        "-",
                        f"policy {snap['policy_version']} ({'signed' if signed else 'unsigned'}); as of {snap['as_of']}; hash {snap['snapshot_hash'][:12]}; "
                        + (
                            "Blob write outcome unconfirmed; the record may or may not be stored, nothing rolled back"
                            if isinstance(e, ranking_publication.ArchiveWriteUncertainError)
                            else "record written, archive folder sync unconfirmed"
                        ),
                    )
                except OSError:
                    logging.getLogger(__name__).exception(
                        "Ranking record written, directory sync unconfirmed and its audit entry failed"
                    )
                    raise
                raise e
            except ranking_archive_blob.BlobArchiveError as e:
                logging.getLogger(__name__).error("Ranking archive could not be written: %s", e)
                raise ranking_publication.ArchiveStorageError(
                    f"The ranking archive cannot be written ({e}). Publication could not be confirmed; "
                    "a record already archived is reported as already published on retry. "
                    "Owner: your operator. Next action: ask them to check the Blob archive configuration and access."
                ) from None
            except OSError as e:
                logging.getLogger(__name__).error("Ranking archive could not be written: %s", e)
                retained = self._log_retained_stage(e)
                leftover = (
                    " A temporary file could not be removed; the operator log names it."
                    if retained
                    else ""
                )
                raise ranking_publication.ArchiveStorageError(
                    f"The ranking archive cannot be written ({type(e).__name__}, {errno.errorcode.get(e.errno or 0, 'unknown')}). "
                    "It must be a local folder that supports hard links and is writable. Publication could not be confirmed; "
                    "a record already archived is reported as already published on retry."
                    + leftover
                    + " "
                    "Owner: your operator. Next action: ask them to check the archive location."
                ) from e
            signed = ranking.is_signed(ranking.CURRENT)
            self.audit(
                user["email"],
                "ranking_snapshot_published"
                if res["written"]
                else "ranking_snapshot_already_published",
                "-",
                f"policy {snap['policy_version']} ({'signed' if signed else 'unsigned'}); as of {snap['as_of']}; hash {snap['snapshot_hash'][:12]}",
            )
            body = {
                "written": res["written"],
                "published_on": res["published_on"],
                "policy_version": snap["policy_version"],
                "policy_signed": signed,
                "as_of": snap["as_of"],
                "snapshot_hash": snap["snapshot_hash"],
            }
            if res.get("stage_retained"):
                logging.getLogger(__name__).warning(
                    "Ranking archive temporary file %s was not removed", res["stage_retained"]
                )
                body["warning"] = (
                    "The record is archived, but a temporary file could not be removed. "
                    "Owner: your operator. Next action: ask them to check the archive permissions."
                )
            return body

    def _queue_candidates(self, queue):
        """Index IDs, never viewer-projected context; called under the store lock."""
        key = (
            self.version,
            self.as_of,
            controls.today(),
            json.dumps(ranking.CURRENT, sort_keys=True),
            json.dumps(self.data.get("handoff_policy"), sort_keys=True),
        )
        cached = getattr(self, "_queue_index", None)
        if cached is None or cached[0] != key:
            members = {name: [] for name, _, _ in taskqueues.DEFINITIONS}
            for c in self.cases.values():
                if not c["closed"]:
                    for name in self.work_context(c, None)["queues"]:
                        members[name].append(c["id"])
            self._queue_index = (key, members)
        return (self.cases[cid] for cid in self._queue_index[1][queue])

    def _filtered(self, user, view, q, f):
        taskqueues.validate_queue(f.get("queue", ""))
        if f.get("queue") and projection.is_contractor(user):
            raise PermissionError("Staff work queues are not available to contractors.")
        if view == "closed":
            if user["role"] not in MANAGER_ROLES:
                raise PermissionError("Only a manager can see closed cases.")
            return sorted(
                (c for c in self.cases.values() if c["closed"] and insights.matches(c, f)),
                key=lambda c: c["id"],
            )
        candidates = self._queue_candidates(f["queue"]) if f.get("queue") else self.cases.values()
        rows = [c for c in candidates if not c["closed"] and insights.matches(c, f)]
        if projection.is_contractor(user):
            rows = [c for c in rows if projection.own_case(user, c)]
        elif view == "mine":
            rows = [c for c in rows if c["owner_code"] == user["code"]]
        if q:
            ql = q.lower()
            # a contractor cannot search on the resident's name: that would reveal who lives where
            fields = (
                (lambda c: [c["home"]["address"], c["home"]["postcode"], c["id"]])
                if projection.is_contractor(user)
                else (
                    lambda c: [
                        c["resident"]["name"],
                        c["home"]["address"],
                        c["home"]["postcode"],
                        c["id"],
                    ]
                )
            )
            rows = [c for c in rows if ql in " ".join(fields(c)).lower()]
        return rows

    def page_cases(
        self, user, view="mine", q="", filters=None, sort="urgent", limit=None, offset=0, after=None
    ):
        """One page of the filtered, sorted list plus the total. limit None returns everything."""
        with self.lock:
            rows = self._filtered(user, view, q, filters or {})
            ranks = self._ranking()
            total = len(rows)
            if view == "closed":
                page = rows if limit is None else rows[offset : offset + limit]
                return dict(
                    items=[self.summary(c) for c in page],
                    total=total,
                    limit=limit,
                    offset=offset,
                    sort="id",
                    policy_version=ranking.CURRENT["version"],
                    policy_hash=ranking.CURRENT["content_hash"],
                    as_of=self.as_of,
                    ranked_total=len(ranks),
                )
            if sort in ("urgent", "", None) or sort not in insights.SORTS:
                rows.sort(key=lambda c: ranks[c["id"]]["rank"])
                if after:
                    rows = [c for c in rows if ranking.sql_key(c) > after]
                    offset = 0
                page = rows if limit is None else rows[offset : offset + limit]
                out = [self.summary(c) for c in page]
            else:
                out = [self.summary(c) for c in rows]
                for r in out:
                    r["rank"] = ranks[r["id"]]["rank"]
                out.sort(key=lambda r: (insights.sort_key(sort)(r), r["rank"]))
                page = None
                if limit is not None:
                    out = out[offset : offset + limit]
                by_id = self.cases
                page = [by_id[r["id"]] for r in out]
            for i, (r, c) in enumerate(zip(out, page)):
                e = ranks[c["id"]]
                r["rank"], r["reasons"] = e["rank"], e["reasons"]
                if projection.is_contractor(user):
                    r.pop("reasons")
                    out[i] = projection.contractor_summary(c, r)
                else:
                    r["work"] = self.work_context(c, user)
                    if not projection.can_see_reason(user) and r["status"].startswith(
                        "Waiting on "
                    ):
                        r["status"] = "Waiting for the recorded next step"
                    if view == "mine":
                        r["focus"] = self.focus(c, user["role"], projection.can_see_reason(user))
            nxt = (
                ranking.sql_key(page[-1])
                if limit is not None
                and page
                and (sort in ("urgent", "", None) or sort not in insights.SORTS)
                and len(page) == limit
                else None
            )
            return dict(
                items=out,
                total=total,
                limit=limit,
                offset=offset,
                sort=sort,
                policy_version=ranking.CURRENT["version"],
                policy_hash=ranking.CURRENT["content_hash"],
                as_of=self.as_of,
                ranked_total=len(ranks),
                next_cursor=nxt,
            )

    def list_cases(self, user, view="mine", q="", filters=None, sort="urgent"):
        return self.page_cases(user, view, q, filters, sort)["items"]

    def work_context(self, c, user):
        return self._work_context(c, user, self.data, self.cases)

    def _work_context(self, c, user, data, cases):
        """Evaluate against either the live copy or a transaction-local SQL snapshot."""
        staff_list = data.get("staff") or list(self.staff.values())
        return taskqueues.context(
            c,
            as_of=self.as_of,
            reason_ok=user is None or projection.can_see_reason(user),
            policy=ranking.CURRENT,
            stock_queries=[
                q
                for q in c.get("stock_reconciliation", [])
                if stock.query_status(c, q["id"]) == "Unresolved"
            ],
            building_reasons=buildings.blockers(data, cases, c),
            resident_reasons=resident_gate(c),
            technical_missing=missing_items(c),
            handoff=handoff_view(
                c, as_of=_handoff_clock(), policy=data.get("handoff_policy"), staff=data.get("staff")
            ),
            staff=staff_list,
        )

    def focus(self, c, role, reason_ok=True):
        """Role-specific facts for the card, as label/value pairs."""
        nxt = next((a for a in c["appointments"] if a["outcome"] == "Booked"), None)
        staff_list = self.data.get("staff") or list(self.staff.values())
        open_h = self._open_safety_items(c, staff=staff_list)
        ev = {d["kind"] for d in c["documents"] if is_available_case_document(d)}
        missing = [k for k in self.EVIDENCE if k not in ev]
        rs = c["resident"]
        if role == "Resident Liaison Officer":
            return [
                ("Resident prefers", rs["preferred"]),
                ("Extra support", stock.support_status(rs)),
                ("Decision on works", resident_status(c)),
                ("Next visit", nxt["date"] if nxt else "None booked"),
            ]
        if role == "Retrofit Coordinator":
            return [
                ("Contractor", c["contractor"]["name"]),
                ("Works", c["measures"]),
                ("Next visit", nxt["date"] if nxt else "None booked"),
            ]
        if role == "Building Safety Liaison":
            return [
                (
                    "Open safety issues",
                    "; ".join(
                        f"{taskqueues.safe_category(cat, reason_ok)} ({own})" for cat, own in open_h
                    ) or "None",
                ),
                ("Works", c["measures"]),
            ]
        if role == "Grants and Evidence Officer":
            return [
                ("Funding", f"{c['funding']['route']}, {c['funding']['status']}"),
                ("Evidence missing", ", ".join(missing) or "Nothing missing"),
            ]
        if role == "Quality Inspector":
            return [
                ("Works", c["measures"]),
                ("Contractor", c["contractor"]["name"]),
                ("Stage", c["stage"]),
            ]
        return [
            ("Wave", c["wave"]),
            ("Funding", c["funding"]["status"]),
            ("Decision on works", resident_status(c)),
            ("Contractor", c["contractor"]["name"]),
        ]

    def counts(self, user):
        with self.lock:
            mine = [
                c
                for c in self.cases.values()
                if not c["closed"] and c["owner_code"] == user["code"]
            ]
            return dict(
                mine=len(mine),
                hazards=sum(taskqueues.has_open_safety(c) for c in mine),
                open=sum(not c["closed"] for c in self.cases.values()),
            )

    def detail(self, case_id, user=None):
        """Case card. Pass the signed-in user so the role's projection is applied; None returns everything (internal use)."""
        with self.lock:
            c = self.cases.get(case_id)
            if not c or (
                user is not None
                and projection.is_contractor(user)
                and not projection.own_case(user, c)
            ):
                return None
            d = json.loads(json.dumps(c))
            d["checklist"] = self.checklist(c)
            d["technical_missing"] = missing_items(c, usable_only=True)
            d["quality_handover_blockers"] = handover_blockers(c)
            from . import nomination_route
            from .resident_decisions import (
                INTAKE_FIELDS,
                _priority_includes_case,
                challenge_catalog,
                challenge_references_visible,
                followup_view,
                nomination_permissions,
            )
            visible = True if user is None else challenge_references_visible(self, user)
            reason_ok = True if user is None else projection.can_see_reason(user)
            case_recs = [
                r for r in self.data.get("recommendations", ())
                if r.get("kind") != "ai_task" and _priority_includes_case(r, case_id)
            ]
            followup_view(
                d,
                recommendations=case_recs,
                can_view_intake=visible,
                can_view_reason=reason_ok,
            )
            if visible and "affected_challenges" in d:
                d["affected_challenges"] = nomination_route.scrub_nomination_restricted_fields(
                    d["affected_challenges"]
                )
                for ch in d["affected_challenges"]:
                    expl = nomination_route.filter_explanation_for_viewer(
                        nomination_route.challenge_explanation(
                            ch,
                            can_view_intake=visible,
                            can_view_reason=reason_ok,
                        ),
                        can_view_intake=visible,
                        can_view_reason=reason_ok,
                    )
                    if expl is not None:
                        ch["plain_language_explanation"] = expl
            if user is not None and visible:
                d["challenge_targets"] = challenge_catalog(
                    self,
                    case_id,
                    can_view_intake=visible,
                    can_view_reason=reason_ok,
                )
                d["challenge_guarantees"] = list(challenges.GUARANTEES)
                d["challenge_assurance"] = challenges.assurance()
                d["nomination_permissions"] = nomination_permissions(self, user, d)
            elif user is not None:
                for field in INTAKE_FIELDS:
                    d.pop(field, None)
                d.pop("affected_challenges", None)
                d.pop("challenge_targets", None)
                d.pop("challenge_guarantees", None)
                d.pop("challenge_assurance", None)
                d.pop("nomination_permissions", None)
            d.pop("form_staging", None)
            d.pop("form_reviews", None)
            d.pop("finance_decision_holds", None)
            if user is not None:
                d.pop("safeguarding_items", None)  # Only the allowlisted work.safeguarding_clocks leaves the store.
            d["support_status"] = stock.support_status(c["resident"])
            d["support_coverage"] = stock.support_coverage(c["resident"])
            d["resident"].setdefault("priority_support", None)
            if not d["resident"].get("adjustment"):
                d["resident"]["adjustment"] = "Unknown"
            d.setdefault("stock_reconciliation", [])
            d.setdefault("stock_reconciliation_events", [])
            for row in d["stock_reconciliation"]:
                row["status"] = stock.query_status(c, row["id"])
            staff_list = self.data.get("staff") or list(self.staff.values())
            d["hazards"] = [
                hazard_view(h, case_id, case=c, as_of=self.as_of, staff=staff_list)
                for h in c["hazards"]
            ]
            if user is None or not projection.is_contractor(user):
                d["work"] = self.work_context(c, user)
            if c.get("handoff"):
                d["handoff"] = handoff_view(
                    c,
                    as_of=_handoff_clock(),
                    policy=self.data.get("handoff_policy"),
                    staff=self.data.get("staff"),
                )
            d["redress_route"] = redress_route_view(c)
            d["status"] = self.status_line(c)
            d["gate"] = self.gate_reasons(c) + buildings.blockers(self.data, self.cases, c)
            if d["status"] == "Ready" and d["gate"]:
                d["status"] = "Waiting on shared building review"
        d["can_advance"] = c["stage"] == READY_STAGE
        d["suggestions"] = insights.recommend_handover(
            c, list(self.cases.values()), self.data["staff"] + identity.people(self)
        )
        d["measure_decisions"] = measure_decision_view(c)
        d["resident_retention"] = retention_schedule(c)
        d["can_record_resident"] = bool(
            user and user.get("role") in projection.RESIDENT_RECORD_ROLES
        )
        d["contacts"] = list(reversed(d["contacts"]))[:40]
        if user is None:
            return d
        if projection.is_contractor(user):
            return projection.contractor_detail(c, d)
        return projection.redact_staff_detail(user, d)

    def building_view(self, user, building_id):
        with self.lock:
            return buildings.view(self.data, self.cases, building_id, user)

    def home_case_view(self, user, case_id):
        from . import home_case

        return home_case.view(self, user, case_id)

    def home_case_record_version(self, user, case_id, metadata):
        from . import home_case

        return home_case.record_version(self, user, case_id, metadata)

    def bulk_edit_preview(self, user, body):
        from . import bulk_edits

        return bulk_edits.preview(self, user, body)

    def bulk_edit_apply(self, user, body):
        from . import bulk_edits

        return bulk_edits.apply(self, user, body)

    def stock_queue(self, user):
        """Open stock conflicts across homes for managers. Read-only, not an investment priority."""
        if user["role"] not in MANAGER_ROLES:
            raise PermissionError("Only a manager can see the stock conflict queue.")
        with self.lock:
            return stock.queue_rows(self.cases.values())

    RESIDENT_CHOICE_QUEUE_ROLES = (
        "Resident Liaison Officer",
        "Retrofit Coordinator",
        "Retrofit Programme Manager",
        "Programme Support Officer",
    )

    def resident_choice_queue(self, user, limit=50, offset=0):
        """Measure choices and update commitments across open homes, role-projected. Read-only, no resident contact."""
        if user.get("role") not in self.RESIDENT_CHOICE_QUEUE_ROLES:
            raise PermissionError("Your role does not include the resident choice queue.")
        with self.lock:
            ids = sorted(cid for cid, c in self.cases.items() if not c["closed"])
            items = []
            for cid in ids[offset : offset + limit]:
                d = self.detail(cid, user)
                if d is None:
                    continue
                items.append(
                    dict(
                        id=cid,
                        address=d["home"]["address"],
                        town=d["home"]["town"],
                        measure_decisions=d.get("measure_decisions", []),
                        resident_update=d.get("resident_update"),
                    )
                )
            return dict(items=items, total=len(ids), limit=limit, offset=offset)

    def stock_reconcile(self, user, case_id, body):
        from . import controls

        controls.refuse_bulk(body)
        with stock.decision_scope(self, user, case_id) as (c, actor):
            if actor["role"] not in MANAGER_ROLES and actor["code"] != c["owner_code"]:
                raise PermissionError(
                    "Only the case owner or a programme manager can open a stock query."
                )
            query = stock.comparison(body)
            owner = self._staff_person(query["query_owner"])
            rows = c.get("stock_reconciliation", [])
            query.update(
                id=f"SQ-{len(rows) + 1}",
                version=len(rows) + 1,
                query_owner={key: owner[key] for key in ("email", "code", "name", "role")},
                recorded_by={key: actor[key] for key in ("email", "code", "name", "role")},
                at=controls.now(),
            )
            c.setdefault("stock_reconciliation", []).append(query)
            self.audit(
                actor["email"],
                "stock_comparison",
                case_id,
                f"{query['id']} {query['field']}; owner {owner['code']}; unresolved",
            )
            self.save()

    def stock_query_event(self, user, case_id, body):
        from . import controls

        controls.refuse_bulk(body)
        with stock.decision_scope(self, user, case_id) as (c, actor):
            event = stock.query_event(body)
            query = next(
                (q for q in c.get("stock_reconciliation", []) if q["id"] == event["query_id"]), None
            )
            if query is None:
                raise ValueError("Choose a stock query on this case.")
            manager = actor["role"] in MANAGER_ROLES
            if event["action"] == "resolve" and not manager:
                raise PermissionError(
                    "Only a named human programme manager can record reconciliation."
                )
            if (
                event["action"] == "withdraw"
                and not manager
                and actor["email"].lower() != query["recorded_by"]["email"].lower()
            ):
                raise PermissionError(
                    "Only the query raiser or a programme manager can withdraw it."
                )
            if stock.query_status(c, query["id"]) != "Unresolved":
                raise ValueError(
                    "This stock query already has a terminal disposition. Open a new query if needed."
                )
            events = c.get("stock_reconciliation_events", [])
            event.update(
                id=f"SQE-{len(events) + 1}",
                at=controls.now(),
                recorded_by={key: actor[key] for key in ("email", "code", "name", "role")},
            )
            c.setdefault("stock_reconciliation_events", []).append(event)
            self.audit(
                actor["email"],
                f"stock_query_{event['action']}",
                case_id,
                f"{event['id']} {query['id']}: {event['status']}; {event['reason']}; evidence {event.get('evidence', 'Not supplied')}",
            )
            self.save()

    def require_stock_clear(self, c):
        reasons = stock.blockers(c)
        if reasons:
            raise GateError(reasons, [gates.STOCK_RULE])

    def require_building_clear(self, c, package_id=None):
        reasons = buildings.blockers(self.data, self.cases, c, package_id)
        if reasons:
            raise GateError(reasons, [gates.BUILDING_RULE])

    def require_safety_clear(self, c):
        staff_list = self.data.get("staff") or list(self.staff.values())
        active = self._open_safety_items(c, staff=staff_list)
        if active:
            raise GateError(
                [
                    f"Home retrofit work is stopped for safety review. Owner: {active[0][1]} (referral follow-up). Next action: obtain external evidence and an independent decision to restart retrofit work."
                ],
                [gates.BOOKING_RULES["safety"]],
            )

    def require_resident_clear(self, c, bindings=None):
        reasons = resident_gate(c, bindings)
        if reasons:
            raise GateError(reasons, [gates.BOOKING_RULES["resident"]])

    @staticmethod
    def _evidence_missing(c: dict[str, Any]) -> list[str] | None:
        try:
            return [x["kind"] for x in Store.checklist(c) if not x["present"]]
        except (KeyError, TypeError):
            return None

    def require_booking_gates(self, c):
        """Fail closed: only an explicit pass on every booking gate lets the case advance."""
        results = gates.booking_gates(c, resident_gate(c))
        results.append(
            gates.evidence_gate(self._evidence_missing(c), "Grants and Evidence Officer")
        )
        if not gates.transition_allowed(results):
            unmet = gates.unmet(results)
            raise GateError([f"{r.reason} Owner: {r.owner}. Next action: {r.correction}" for r in unmet], [r.rule for r in unmet if r.rule])

    def require_quality_evidence(self, rec):
        """Fail closed: acceptance and handover need an explicit pass on the stored checklist evidence."""
        result = quality_evidence_gate(rec)
        if not result.passed:
            raise GateError([f"{result.reason} Owner: {result.owner}. Next action: {result.correction}"], [result.rule] if result.rule else [])

    def log_call(self, user, case_id, outcome, note, channel="Phone"):
        outcome = (outcome or "").strip()[:80]
        if not outcome:
            raise ValueError("Say how the call went.")
        with self.lock:
            c = self._case(case_id)
            self.guard_case_event(c)
            c["contacts"].append(
                dict(
                    at=datetime.now().isoformat(timespec="minutes"),
                    purpose="Update",
                    channel=channel,
                    direction="Outbound",
                    outcome=outcome,
                    note=(note or "")[:500],
                    by=user["name"],
                )
            )
            remember_first_contact(c)
            self.audit(user["email"], "log_contact", case_id, outcome)
            self.save()

    def set_decision(self, user, case_id, status, note=""):
        if status not in DECISIONS:
            raise ValueError("Choose one of the listed answers.")
        with self.lock:
            c = self._case(case_id)
            self.guard_case_event(c)
            self.resident_recorder(user)
            c["decision"] = dict(
                status=status, by=user["name"], at=datetime.now().date().isoformat()
            )
            self.audit(user["email"], "resident_decision", case_id, status)
            self.save()

    def hand_over(self, user, case_id, to_email, note="", metadata=None):
        """Legacy entry point: offer responsibility, never bypass receiver acceptance."""
        return self.offer_handoff(user, case_id, to_email, note, metadata=metadata)

    def advance(self, user, case_id):
        with change_provenance.controlled(self, user, case_id) as (c, user):
            self.guard_case_event(c)
            if c["stage"] != READY_STAGE:
                raise ValueError(
                    f"This case is not at the final checks. It may have changed since you opened it. Case owner: {c['owner']}. Next action: copy any unsaved notes, then reload the case and check its current stage before taking further action."
                )
            why = self.gate_reasons(c)
            rules = self._transition_rules(c) if why else []
            building = buildings.blockers(self.data, self.cases, c)
            if building:
                why += building
                rules.append(gates.BUILDING_RULE)
            if why:
                raise GateError(why, rules)
            self.require_safety_clear(c)
            self.require_resident_clear(c)
            self.require_booking_gates(c)
            self.require_booked_capacity(c)
            was = c["stage"]
            c.update(
                stage=BOOKED_STAGE,
                reason="to book the installation",
                waiting_on=c["contractor"]["contact"],
            )
            orders = [
                w
                for w in self._proc()["work_orders"]
                if w["case_id"] == case_id and w["state"] == "Appointed"
            ]
            change_provenance.append_event(
                c,
                "returns",
                user,
                "advance",
                "controlled/advance",
                from_stage=was,
                to_stage=BOOKED_STAGE,
                reopened=False,
                work_order_versions=[
                    dict(id=w["id"], version=w["versions"][-1]["version"]) for w in orders
                ],
            )
            if hasattr(self, "db"):
                self.audit(user["email"], "advance", case_id, BOOKED_STAGE)
                self.save()
            else:
                self.save()
                self.audit(user["email"], "advance", case_id, BOOKED_STAGE)

    def draft(self, case_id, kind, user=None):
        with self.lock:
            c = self._case(case_id)
        r = c["resident"]
        if r["representative"]:
            raise ValueError(
                "Representative disclosure needs a current scoped authority check. Nothing has been sent."
            )
        who = r["formal"]
        reason_ok = True if user is None else projection.can_see_reason(user)
        if kind == "visit":
            avoid = f", outside {r['unavailable']}" if reason_ok and r["unavailable"] else ""
            body = (
                f"Dear {who},\n\nWe would like to arrange a visit to {c['home']['address']} to talk through "
                f"improvements to your home. Please let us know a day and time that suits you{avoid}.\n\n"
                f"Kind regards,\n{c['owner']}\nZava North Homes"
            )
        else:
            body = (
                f"Dear {who},\n\nA quick update on the work to {c['home']['address']}: it is currently at "
                f"'{c['stage'].lower()}'. {c['owner']} is your contact and will be in touch with the next "
                f"step.\n\nKind regards,\n{c['owner']}\nZava North Homes"
            )
        return dict(
            text=body,
            note="Template draft, not approved, not an instruction. Nothing is sent by the system.",
        )

    # ---- insight views
    def facets(self):
        with self.lock:
            return insights.facets(list(self.cases.values()))

    def ai_consumption_economics(self, **kwargs):
        return tokenomics.store_ai_consumption_economics(self, **kwargs)

    def stats(self):
        with self.lock:
            cases = list(self.cases.values())
            staff = list(self.data["staff"])
        econ = self.ai_consumption_economics()
        return insights.stats(cases, staff, ai_consumption_economics=econ)

    def progress_report(self, user, *, as_of, start=None, view="mine", filters=None, scenario=None):
        from . import progress

        if user.get("role") not in projection.STAFF_ROLES:
            raise PermissionError("Only authorised staff can read progress evidence.")
        if view not in ("mine", "all", "closed"):
            raise ValueError("Choose mine, all or closed for the cohort.")
        filters = filters or {}
        if set(filters) - {"stage", "area", "wave", "owner", "contractor", "flag", "queue"}:
            raise ValueError("Unknown cohort filter.")
        if filters.get("flag") not in (
            None,
            "",
            "hazard",
            "support",
            "long",
            "nodecision",
            "fundingprog",
            "funding",
        ):
            raise ValueError("Unknown cohort flag.")
        progress.timestamp(as_of, "As-of")
        if start is not None:
            progress.timestamp(start, "Period start")
        with self.lock:
            baseline = self._filtered(user, view, "", {})
            selected = self._filtered(user, view, "", filters)
            try:
                audit_intact = self.verify_ledger()["intact"]
            except (OSError, ValueError, TypeError, KeyError, AttributeError):
                logging.getLogger(__name__).exception(
                    "Progress report audit verification unavailable"
                )
                audit_intact = None
            cohort = dict(
                view=view,
                filters=dict(filters),
                selection_basis="Current authorized records",
                baseline_cases=len(baseline),
                selected_cases=len(selected),
                excluded_by_filters=len(baseline) - len(selected),
                case_ids=sorted(c["id"] for c in selected),
            )
            return progress.report(
                selected,
                as_of=as_of,
                start=start,
                cohort=cohort,
                scenario=scenario,
                audit_intact=audit_intact,
                ai_consumption_economics=self.ai_consumption_economics(
                    start=start,
                    as_of=as_of,
                ),
            )

    def map_points(self, f):
        with self.lock:
            return insights.map_points(list(self.cases.values()), f)

    def map_view(self, f, bbox=None, zoom=None, sensors=None):
        with self.lock:
            view = insights.map_view(self.cases.values(), f, bbox, zoom)
        return insights.attach_sensors(view, sensors)

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
    def checklist(c: Any) -> list[dict[str, Any]]:
        have = {k for d in c["documents"] for k in (d["kind"],) if is_available_case_document(d)}
        return [dict(kind=k, present=k in have) for k in Store.EVIDENCE]

    def _doc_role(self, user, what):
        if user is not None and user.get("role") not in projection.STAFF_ROLES:
            raise PermissionError(f"Your role cannot {what} documents.")

    @staticmethod
    def _clean_doc_ai_metadata(metadata):
        if not isinstance(metadata, dict):
            return {}
        extra = {}
        raw_deriv = metadata.get("ai_derivative", metadata.get("derivative"))
        if raw_deriv is not None:
            if not isinstance(raw_deriv, str) or len(raw_deriv.strip()) > 60:
                raise ValueError("Document derivative status must be a bounded text label.")
            extra["ai_derivative"] = raw_deriv.strip()
        if "requires_derivative" in metadata and metadata["requires_derivative"] is not None:
            if not isinstance(metadata["requires_derivative"], bool):
                raise ValueError("requires_derivative must be true or false.")
            extra["requires_derivative"] = metadata["requires_derivative"]
        if "derivative_text" in metadata and metadata["derivative_text"] is not None:
            if (
                not isinstance(metadata["derivative_text"], str)
                or len(metadata["derivative_text"]) > 20_000
            ):
                raise ValueError(
                    "Approved derivative text must be bounded text up to 20,000 characters."
                )
            extra["derivative_text"] = metadata["derivative_text"]
        if "necessity_exception" in metadata and metadata["necessity_exception"] is not None:
            exc = metadata["necessity_exception"]
            if not isinstance(exc, dict) or len(exc) > 12:
                raise ValueError("Necessity exception metadata must be a bounded object.")
            cleaned_exc = {}
            for k, v in exc.items():
                if not isinstance(k, str) or len(k) > 40 or not isinstance(v, str) or len(v) > 300:
                    raise ValueError("Necessity exception fields must be bounded strings.")
                cleaned_exc[k] = v.strip()
            extra["necessity_exception"] = cleaned_exc
        return extra

    def add_document(self, user, case_id, name, kind, data, metadata=None):
        from . import change_provenance

        self._doc_role(user, "add")
        name = os.path.basename((name or "").strip())[:120]
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
        if ext not in self.EXT:
            raise ValueError(
                "That file type is not accepted. Use pdf, png, jpg, docx, xlsx, csv or txt."
            )
        if not data or len(data) > self.MAX_BYTES:
            raise ValueError("Files must be between 1 byte and 5 MB.")
        doc_ai_meta = self._clean_doc_ai_metadata(metadata)
        kind = kind if kind in self.KINDS else "Other"
        mime = self.EXT[ext]
        did, uploaded = uuid.uuid4().hex[:12], False
        try:
            with change_provenance.operation(
                self, user, case_id, "upload_document", metadata, "document_history"
            ) as (c, event):
                old = change_provenance.document_refs(c)
                self.docstore.put(case_id, did, data, mime)
                uploaded = True
                scan = self.scan_new_document(case_id, did, name, data, mime)
                doc = dict(
                    id=did,
                    name=name,
                    kind=kind,
                    at=datetime.now().date().isoformat(),
                    by=user["name"],
                    generated=False,
                    mime=mime,
                    summary="",
                    content_sha256=hashlib.sha256(data).hexdigest(),
                    version=1,
                    scan=scan,
                )
                doc.update({key: event[key] for key in ("source", "source_version", "reason")})
                doc.update(doc_ai_meta)
                c = self._case(case_id)
                c["documents"].append(doc)
                event["changes"] = dict(
                    documents=dict(old=old, new=change_provenance.document_refs(c))
                )
            out = deepcopy(doc)
            out.pop("derivative_text", None)
            if isinstance(out.get("necessity_exception"), dict) and not projection.can_see_reason(
                user
            ):
                out["necessity_exception"] = dict(
                    out["necessity_exception"], reason=projection.NOTE_HELD
                )
            return out
        except Exception as error:
            if uploaded and not any(d["id"] == did for d in self.cases[case_id]["documents"]):
                try:
                    self.docstore.delete(case_id, did)
                except Exception:
                    error.add_note("Uploaded object cleanup failed; check storage before retrying.")
                    logging.getLogger(__name__).exception("Failed upload object cleanup failed")
            raise

    def read_document(
        self,
        user,
        case_id,
        doc_id,
        mode=None,
        *,
        derivative=None,
        derivative_text=None,
        necessity_exception=None,
    ):
        self._doc_role(user, "read")
        call_meta = self._clean_doc_ai_metadata(
            {
                k: v
                for k, v in (
                    ("ai_derivative", derivative),
                    ("derivative_text", derivative_text),
                    ("necessity_exception", necessity_exception),
                )
                if v is not None
            }
        )
        with self.lock:
            if self.detail(case_id, user) is None:
                raise PermissionError("You do not have access to this case.")
            c = self._case(case_id)
            doc = next(
                (d for d in c["documents"] if d["id"] == doc_id and not d.get("generated")), None
            )
            if not doc:
                raise KeyError(doc_id)
            export_fields.scalars(doc, ("name", "mime"))
            self.ensure_scanned(case_id, doc, user["email"] if user else "system")
            self.require_clean(doc)
            data = self.docstore.get(case_id, doc_id)
            resident = c.get("resident") or {}
            consent = (
                resident.get("ai_data_use_consent") if "ai_data_use_consent" in resident else None
            )
            eff_deriv = call_meta.get("ai_derivative", doc.get("ai_derivative"))
            eff_exc = call_meta.get("necessity_exception", doc.get("necessity_exception"))
            eff_text = call_meta.get("derivative_text", doc.get("derivative_text"))
            doc_snap = deepcopy(doc)
        dispatch_data = data
        dispatch_mime = doc_snap["mime"]
        if eff_deriv == "reviewed_redacted" and isinstance(eff_text, str) and eff_text.strip():
            dispatch_data = eff_text.encode("utf-8")
            dispatch_mime = "text/plain"
        self.audit(user["email"], "ai_run_start", case_id, f"read_document {doc_snap['name']}")
        r = ai_tasks.run_document(
            self,
            user,
            case_id,
            doc_snap,
            dispatch_data,
            mode,
            derivative=eff_deriv,
            necessity_exception=eff_exc,
            resident_consent=consent,
            dispatch_mime=dispatch_mime,
        )
        used_exception = (
            r["source"] == "ai"
            and eff_deriv not in ("reviewed_redacted", "synthetic_safe")
            and eff_exc is not None
        )
        with self.lock:
            doc = next(d for d in self._case(case_id)["documents"] if d["id"] == doc_id)
            if r["source"] == "ai" or not doc.get("summary"):
                doc["summary"] = r["text"]
                if r["source"] == "ai":
                    doc["summary_from_exception"] = used_exception
                    if used_exception and isinstance(eff_exc, dict):
                        doc["necessity_exception"] = deepcopy(eff_exc)
            self.audit(
                user["email"],
                "ai_run_end",
                case_id,
                f"read_document source={r['source']} model={r['model']}",
            )
            self.save()
        return dict(r, manual_available=True)

    def get_document(self, case_id, doc_id, user=None):
        """Bytes of one document. Pass the signed-in user so the role is checked and the download is audited."""
        self._doc_role(user, "download")
        with self.lock:
            c = self._case(case_id)
            doc = next((d for d in c["documents"] if d["id"] == doc_id), None)
            if not doc:
                raise KeyError(doc_id)
            if doc.get("generated"):
                text = (
                    f"{doc['name']}\nCase {c['id']}: {c['home']['address']}, {c['home']['postcode']}\n"
                    f"Filed {doc['at']} by {doc['by']}\nType: {doc['kind']}\n"
                )
                return doc["name"].rsplit(".", 1)[0] + ".txt", "text/plain", text.encode()
            self.ensure_scanned(case_id, doc, user["email"] if user else "system")
            self.require_clean(doc)
            data = self.docstore.get(case_id, doc_id)
            if user is not None:
                self.audit(
                    user["email"], "download_document", case_id, f"{doc['kind']}: {doc['name']}"
                )
            return doc["name"], doc["mime"], data

    # ---- AI drafting (always a draft for a person)
    def _facts(self, c, reason_ok=False):
        export_fields.prompt_case(c)
        r = c["resident"]
        adjust = (
            (r.get("adjustment") or "Unknown")
            if reason_ok
            else (
                "extra support needed"
                if projection.needs_notice(c)
                else "Unknown"
                if stock.support_status(r) == "Unknown"
                else "None"
            )
        )
        return (
            f"Case {c['id']}. Resident: {r['name']}. Home: {c['home']['address']}, {c['home']['town']}. "
            f"Stage: {c['stage']} for {c['days_in_stage']} days. Waiting on {c['waiting_on']} {c['reason']}. "
            f"Resident adjustments: {adjust}. Resident prefers: {r['preferred']}. "
            f"Resident decision: {resident_status(c)}. Funding: {c['funding']['route']} ({c['funding']['status']}). "
            f"Open safety issues: {sum(not h['released'] for h in c['hazards'])}. "
            f"Recent contacts: "
            + "; ".join(
                f"{k['at'][:10]} {k['outcome'] if reason_ok else k['channel']}"
                for k in c["contacts"][-4:]
            )
        )

    def ai_run(self, user, case_id, task, mode=None):
        with self.lock:
            c = self._case(case_id)
            reason_ok = projection.can_see_reason(user)
            facts = self._facts(c, reason_ok)
            raw_status = self.status_line(c)
            safe_status = (
                "Waiting for the recorded next step"
                if not reason_ok and raw_status.startswith("Waiting on ")
                else raw_status
            )
            fallback = (
                (
                    "Staff proposal only. Confirm the safe recipient and current authority before "
                    "using this update: " + safe_status
                )
                if c["resident"]["representative"]
                else self.draft(case_id, "visit" if task == "message" else "update", user=user)[
                    "text"
                ]
            )
            summary = safe_status
            owner, who = c["owner"], c["resident"]["name"]
            case = c
            tcites = (
                ai_tasks.cites_for(
                    c, "Stage:", "Preferred contact:", "Unavailable:", reason_ok=reason_ok
                )
                if task == "message"
                else ai_tasks.cites_for(c, "Stage:", "Waiting on:", "Open safety issues:")
            )
        if task not in ("message", "summary"):
            raise ValueError("Unknown request.")
        sysmsg, prompt = ai_prompts.render(task, owner=owner, facts=facts)
        tmpl, strong = (fallback if task == "message" else summary), False
        self.audit(user["email"], "ai_run_start", case_id, task)
        r = ai_tasks.run_text_task(
            self,
            user,
            task,
            [case],
            sysmsg,
            prompt,
            tmpl,
            tcites,
            strong,
            mode=mode,
            bullets=task == "summary",
        )
        self.audit(
            user["email"],
            "ai_run_end",
            case_id,
            f"{task} source={r['source']} model={r['model']} validated={r['validated']} verified={r['verified']}",
        )
        return dict(
            r,
            label=(
                "AI suggestion, not approved"
                if r["source"] == "ai"
                else "Template draft, not approved"
            )
            + ("" if r["verified"] else ". Unverified: its sources do not match the case record"),
        )

    def _briefing_denial_unchanged(self, cached):
        """A template briefing held by a release denial stays valid while that same denial holds.

        Without this every GET re-ran the held dispatch, which wrote an audit entry, a comparison record and a
        second audit entry under the SQL write lock (issue #2320)."""
        if cached["source"] == "ai" or cached.get("release") is not None:
            return False
        reason = cached.get("reason")
        return bool(reason) and reason == self.release_denial("briefing")

    BRIEFING_WRITE_WAIT_MS = 2000

    def write_wait(self, ms):
        """Cap the wait for the write lock in this thread; the SQLite store has no shared lock to wait for."""
        return contextlib.nullcontext()

    BRIEFING_BUSY = (
        "The briefing could not be saved to the record just now because the record is busy. "
        "It is shown without being saved; refresh in a moment."
    )

    BRIEFING_BUSY_TTL_S = 10

    def _briefing_unrecorded(self, key, hit, programme, candidates, top, tmpl):
        out = self._briefing_unrecorded_answer(key, hit, programme, candidates, top, tmpl)
        # Without this every GET in a busy period repeated the capped lock wait while holding store.lock.
        now = time.monotonic()
        with self.lock:
            for k in [k for k, v in self._briefing_busy.items() if v[0] <= now]:
                del self._briefing_busy[k]
            self._briefing_busy[key] = (now + self.BRIEFING_BUSY_TTL_S, out)
        return out

    def _briefing_unrecorded_answer(self, key, hit, programme, candidates, top, tmpl):
        stale = hit or self._briefings.get(key)
        if stale:
            return dict(stale[1], reason=self.BRIEFING_BUSY, recorded=False)
        cites = [
            f"{c['id']}: {part}"
            for c in top[:3]
            for part in (f"Stage: {c['stage']}", f"Days in stage: {c['days_in_stage']}")
        ]
        return dict(
            text=tmpl,
            source="template",
            model=None,
            validated=True,
            verified=bool(cites),
            approval="Not reviewed",
            task="briefing",
            release=None,
            reason=self.BRIEFING_BUSY,
            recorded=False,
            citations=cites,
            scope="programme" if programme else "assigned",
            scope_label="All programme cases" if programme else "My assigned cases",
            case_count=len(candidates),
            summary_count=len(top[:3]),
            label="Summary by rules",
        )

    def briefing(self, user, mode=None):
        if not projection.allowed(user, "briefing"):
            raise PermissionError("Your role does not include this.")
        off = ai_tasks.workflow_only(mode)
        programme = user["role"] in MANAGER_ROLES
        with self.lock:
            candidates = self._filtered(user, "all" if programme else "mine", "", {})
            ranks = self._ranking()
            candidates.sort(key=lambda c: ranks[c["id"]]["rank"])
            key = (
                user["code"],
                user["email"],
                user["role"],
                user.get("tid"),
                user.get("oid"),
                projection.can_see_reason(user),
                tuple(c["id"] for c in candidates),
                off,
            )
            hit = self._briefings.get(key)
            busy = self._briefing_busy.get(key)
            if busy and busy[0] > time.monotonic():
                return busy[1]
            if (
                hit
                and hit[0] == self.version
                and (hit[1]["source"] != "ai" or self.ai_epoch_current(hit[1]))
                and not self.continuity_suspension("briefing")
                and (
                    (hit[1]["source"] != "ai" and (off or not self.ai.configured))
                    or self.release_current("briefing", hit[1].get("release"), hit[1].get("model"))
                    or self._briefing_denial_unchanged(hit[1])
                )
            ):
                return hit[1]
            ver = self.version
            top = [deepcopy(self._case(c["id"])) for c in candidates[:8]]
            for c in top:
                export_fields.prompt_case(c)
            rows = [self.summary(c) for c in top]
            if not projection.can_see_reason(user):
                for row in rows:
                    if row["status"].startswith("Waiting on "):
                        row["status"] = "Waiting for the recorded next step"
            facts = "\n".join(
                f"{c['id']} {c['resident']['name']}: {c['stage']}, {c['days_in_stage']} days. {row['status']}"
                for c, row in zip(top, rows)
            )
            empty = (
                "No permitted open programme cases are available."
                if programme
                else "No open cases are assigned to you. This does not mean the programme has no work."
            )
            tmpl = (
                "Start with: "
                + "; ".join(
                    f"{c['resident']['name']} ({c['stage'].lower()}, {c['days_in_stage']} days)"
                    for c in top[:3]
                )
                if top
                else empty
            )
        sysmsg, prompt = ai_prompts.render("briefing", facts=facts)
        try:
            with self.write_wait(self.BRIEFING_WRITE_WAIT_MS):
                r = ai_tasks.run_text_task(
                    self,
                    user,
                    "briefing",
                    top,
                    sysmsg,
                    prompt,
                    tmpl,
                    [
                        x
                        for c in top[:3]
                        for x in [
                            f"{c['id']}: Stage: {c['stage']}",
                            f"{c['id']}: Days in stage: {c['days_in_stage']}",
                        ]
                    ],
                    mode=mode,
                )
                self.audit(
                    user["email"],
                    "ai_run",
                    "-",
                    f"briefing source={r['source']} model={r['model']} verified={r['verified']}",
                )
        except Exception as exc:
            from .mssqlstore import is_write_lock_busy

            if not is_write_lock_busy(exc):
                raise
            # A GET must not answer 503 because other clients hold the SQL write lock (issue #2320):
            # show the last answer or a rules summary, say it was not recorded, and let the next GET record it.
            return self._briefing_unrecorded(key, hit, programme, candidates, top, tmpl)
        out = dict(
            r,
            scope="programme" if programme else "assigned",
            scope_label="All programme cases" if programme else "My assigned cases",
            case_count=len(candidates),
            summary_count=len(top) if r["source"] == "ai" else len(top[:3]),
            label=("AI suggestion, not approved" if r["source"] == "ai" else "Summary by rules")
            + ("" if r["verified"] else ". Unverified: its sources do not match the case record"),
        )
        if r["source"] != "ai" and r["approval"] != "Quarantined" and top:
            out["statements"] = [
                dict(
                    text=f"{c['resident']['name']} "
                    f"({c['stage'].lower()}, {c['days_in_stage']} days)",
                    citations=[
                        f"{c['id']}: Stage: {c['stage']}",
                        f"{c['id']}: Days in stage: {c['days_in_stage']}",
                    ],
                    unresolved=[],
                )
                for c in top[:3]
            ]
        with self.lock:
            self._briefing_busy.pop(key, None)
            if self.version - ver <= 1:  # only our own comparison record was saved meanwhile
                for old in [k for k, v in self._briefings.items() if v[0] != self.version]:
                    del self._briefings[old]
                self._briefings[key] = (self.version, out)
        return out

    # ---- AI priority recommendation: advice beside the deterministic order, never part of it
    REC_LABEL = "AI suggestion, not approved"
    REC_ACTIONS = {"accept": "Accepted", "edit": "Edited", "reject": "Rejected"}

    def _rec_view(self, rec, user=None):
        from .resident_decisions import priority_challenge_state, challenge_references_visible

        challenge = priority_challenge_state(self, rec)
        if not challenge_references_visible(self, user):
            challenge["challenge_ids"] = []
        ranks = self._ranking()
        reason_ok = True if user is None else projection.can_see_reason(user)

        def _visible_cid(cid):
            c = self.cases.get(cid)
            if c is None:
                return False
            if user is None:
                return True
            if projection.is_contractor(user):
                return projection.own_case(user, c)
            return user.get("role") in projection.STAFF_ROLES

        def row(cid, reason=None, cites=None):
            c = self.cases[cid]
            r = dict(
                case_id=cid,
                resident=c["resident"]["name"],
                address=c["home"]["address"],
                stage=c["stage"],
                rank=ranks[cid]["rank"] if cid in ranks else None,
            )
            if reason is not None:
                withheld = (
                    frozenset()
                    if user is None
                    else projection.withheld_scope_values(self, user, [cid])
                )
                safe_cites = [
                    ct
                    for ct in (cites or [])
                    if (reason_ok or not str(ct).strip().casefold().startswith("support reason:"))
                    and not projection.contains_withheld_value(ct, withheld)
                ]
                safe_reason = (
                    projection.NOTE_HELD
                    if projection.contains_withheld_value(reason, withheld)
                    else reason
                )
                r["reason"] = safe_reason
                r["cites"] = safe_cites
                r["reason_origin"] = origin
            return r

        origin = ai_tasks.origin_of(rec["source"])
        denied = rec["source"] == "ai" and not self.release_current(
            "priority", rec.get("release"), rec.get("model")
        )
        current = rec["source"] != "ai" or (
            self.ai_epoch_current(rec) and not self.continuity_suspension("priority")
        )
        scope_withheld = (
            frozenset()
            if user is None
            else projection.withheld_scope_values(
                self, user, rec.get("case_ids") or [i["case_id"] for i in rec.get("items", [])]
            )
        )
        base = dict(rec)
        if user is not None:
            if not reason_ok and base.get("reason"):
                base["reason"] = projection.NOTE_HELD
            if base.get("ai_output") and (
                ai_tasks.FORBIDDEN.search(str(base["ai_output"]))
                or projection.contains_withheld_value(base["ai_output"], scope_withheld)
            ):
                base["ai_output"] = projection.NOTE_HELD
        view = dict(
            base,
            label=self.REC_LABEL,
            origin=origin,
            ordering_origin=ai_tasks.DECISION_RULE,
            actionable=current and not denied and not challenge["stale"],
            release_denied=denied,
            **challenge,
            epoch_current=current,
            relied_on=current
            and not denied
            and not challenge["stale"]
            and rec["status"] in ("Accepted", "Edited"),
            items=[
                row(i["case_id"], i["reason"], i.get("cites"))
                for i in rec["items"]
                if _visible_cid(i["case_id"])
            ],
            final_items=[
                row(i["case_id"], i["reason"], i.get("cites"))
                for i in rec["final_items"]
                if _visible_cid(i["case_id"])
            ]
            if rec.get("final_items") is not None
            else None,
            deterministic=[
                dict(row(cid), origin=ai_tasks.DECISION_RULE)
                for cid in rec["deterministic"]
                if _visible_cid(cid)
            ],
        )
        if self._order_unresolved(rec):
            view.update(
                order_confirmed=False, actionable=False, relied_on=False, order_note=self.ORDER_NOTE
            )
        return view

    ORDER_NOTE = (
        "After a database upgrade the order of this record could not be proven, so it may not be your newest. "
        "The named data owner must confirm it before it is acted on. You can still reject it or use the "
        "ordinary case controls."
    )

    def _order_unresolved(self, rec):
        """The employee's newest eligible record whose creation order the upgrade could not prove (#1292)."""
        if rec.get("kind") == "ai_task" or not self.rec_order_unresolved(rec["id"]):
            return False
        mine = [
            r
            for r in self.data["recommendations"]
            if r["user"] == rec["user"] and r.get("kind") != "ai_task"
        ]
        return bool(mine) and mine[-1]["id"] == rec["id"]

    def ai_priority(self, user, n=5, mode=None):
        n = max(1, min(10, int(n)))
        with self.lock:
            ranks = self._ranking()
            mine = sorted(
                (
                    c
                    for c in self.cases.values()
                    if not c["closed"] and c["owner_code"] == user["code"]
                ),
                key=lambda c: ranks[c["id"]]["rank"],
            )
            if not mine:
                raise ValueError("You have no open cases to prioritise.")
            det = [c["id"] for c in mine[:n]]
            cand = mine[:40]
            ids = {c["id"] for c in cand}
            ok = projection.can_see_reason(user)
            facts = "\n".join(f"{c['id']}: {self._facts(c, ok)}" for c in cand)
            sources = {c["id"]: ai_tasks.source_labels(c, ok) for c in cand}
            captured_sources = ai_tasks.source_snapshot_hashes(sources)
            hazard_ids = [c["id"] for c in cand if any(not h["released"] for h in c["hazards"])]
            tmpl_items = self._heuristic_priority(cand, n, ok)
            policy_version = ranking.CURRENT["version"]
            withheld_by_cid = {
                c["id"]: projection.withheld_scope_values(self, user, [c["id"]]) for c in cand
            }
            all_withheld = (
                frozenset().union(*withheld_by_cid.values()) if withheld_by_cid else frozenset()
            )
        tmpl = json.dumps(tmpl_items)
        sysmsg, prompt = ai_prompts.render("priority", n=n, facts=facts)

        def valid(text):
            items, _, err = ai_tasks.priority_items(text, n, sources)
            if err is not None or ai_tasks.critical_misses(
                [i["case_id"] for i in items], hazard_ids, n
            ):
                return False
            for i in items:
                cw = withheld_by_cid.get(i["case_id"], all_withheld)
                if projection.contains_withheld_value(i.get("reason"), cw) or any(
                    projection.contains_withheld_value(ct, cw) for ct in i.get("cites", [])
                ):
                    return False
            return True

        self.audit(user["email"], "ai_run_start", "-", f"priority_recommendation n={n}")
        epoch0 = self.continuity_epoch()
        r = self.ai.run(
            "priority", sysmsg, prompt, tmpl, True, check=valid, off=ai_tasks.workflow_only(mode)
        )
        items, dropped = None, 0
        if r["source"] == "ai":
            items, dropped, _ = ai_tasks.priority_items(r["text"], n, sources)
        if items is None:
            items = tmpl_items
        raw_ai = r.get("ai_text") or (r["text"] if r["source"] == "ai" else None)
        safe_ai = (
            None
            if raw_ai
            and (
                ai_tasks.FORBIDDEN.search(str(raw_ai))
                or projection.contains_withheld_value(raw_ai, all_withheld)
            )
            else raw_ai
        )

        def publish(late):
            rec = dict(
                id=uuid.uuid4().hex[:12],
                user=user["email"],
                created=datetime.now().isoformat(timespec="seconds"),
                status="Proposed",
                source=r["source"],
                model=r["model"],
                validated=r["validated"],
                n=n,
                items=items,
                deterministic=det,
                policy_version=policy_version,
                final_items=None,
                resolved_by=None,
                resolved_at=None,
                reason="",
                workflow_items=tmpl_items,
                ai_output=safe_ai,
                fallback_reason=r.get("reason"),
                latency_ms=r.get("latency_ms"),
                prompt_version=ai_prompts.version("priority"),
                release=r.get("release"),
                continuity_epoch=epoch0,
                meter_root=r.get("meter_root"),
                usage=r.get("usage"),
                meter_id=r.get("meter_id"),
                quarantine=dict(reason="Late priority result after epoch change") if late else None,
                mode="workflow-only" if r.get("reason") == "workflow-only mode selected" else "ai",
                dropped_uncited=dropped,
                case_ids=list(captured_sources),
                source_versions=captured_sources,
                hazard_ids=hazard_ids,
                overlap=len({i["case_id"] for i in items} & set(det)),
            )
            if late:
                rec.update(
                    status="Quarantined",
                    items=tmpl_items,
                    fallback_reason="Late priority result quarantined; use the manual route.",
                )
            self.data["recommendations"].append(rec)
            self.audit(
                user["email"],
                "ai_run_end",
                "-",
                f"priority_recommendation {rec['id']} source={r['source']} model={r['model']} validated={r['validated']}",
            )
            self.save()
            if r.get("meter_root"):
                held = self.ai.consumption.publish_output(
                    r["meter_root"],
                    rec["id"],
                    eligible=not late and r["source"] == "ai" and r["validated"],
                )
                if held:
                    rec.update(
                        source="template",
                        model=None,
                        mode="workflow-only",
                        items=tmpl_items,
                        fallback_reason=f"Financial attribution held ({held['reason']}); use the manual route.",
                        financial_attribution=held,
                        overlap=len({i["case_id"] for i in tmpl_items} & set(det)),
                    )
                    self.save()
            return self._rec_view(rec, user)

        return self.continuity_publish("priority", epoch0, r["source"], publish)

    def _heuristic_priority(self, cand, n, ok=False):
        """Template used when no model is available: a different, simpler view from the ranking policy."""

        def score(c):
            s = 0
            s += 100 if any(not h["released"] for h in c["hazards"]) else 0
            s += 30 if stock.support_status(c["resident"]) == "Yes" else 0
            s += 20 if resident_status(c) not in ("Accepted", "Declined") else 0
            return s + min(c["days_in_stage"], 120) / 4

        out = []
        for c in sorted(cand, key=lambda c: (-score(c), c["id"]))[:n]:
            why = []
            if any(not h["released"] for h in c["hazards"]):
                why.append("an open safety issue")
            if stock.support_status(c["resident"]) == "Yes":
                why.append("the resident needs extra support")
            if resident_status(c) not in ("Accepted", "Declined"):
                why.append("no resident decision yet")
            why.append(f"{c['days_in_stage']} days at '{c['stage'].lower()}'")
            out.append(
                dict(
                    case_id=c["id"],
                    reason="Because of " + ", ".join(why) + ".",
                    cites=ai_tasks.cites_for(
                        c,
                        "Open safety issues:",
                        "Extra support:",
                        "Resident decision:",
                        "Days in stage:",
                        "Stage:",
                        reason_ok=ok,
                    ),
                )
            )
        return out

    def rec_order_unresolved(self, rec_id):
        return False

    def latest_priority(self, user):
        with self.lock:
            mine = [
                r
                for r in self.data["recommendations"]
                if r["user"] == user["email"] and r.get("kind") != "ai_task"
            ]
            if not mine:
                return None
            return self._rec_view(mine[-1], user)

    def resolve_priority(self, user, rec_id, action, reason="", items=None):
        if action not in self.REC_ACTIONS:
            raise ValueError("Choose accept, edit or reject.")
        reason = (reason or "").strip()[:300]
        if action in ("edit", "reject") and not reason:
            raise ValueError("Say why.")
        from .resident_decisions import priority_review, mark_priority_committed, _actor

        with self.lock:
            _actor(self, user)
            rec = next(
                (
                    r
                    for r in self.data["recommendations"]
                    if r["id"] == rec_id and r.get("kind") != "ai_task"
                ),
                None,
            )
            if not rec:
                raise KeyError(rec_id)
            if rec["user"] != user["email"]:
                raise PermissionError("This suggestion was made for someone else.")
            if action != "reject" and rec["status"] == "Proposed" and self._order_unresolved(rec):
                raise PermissionError(self.ORDER_NOTE)
            if rec["status"] != "Proposed":
                repaired = self._repair_ai_review(rec, action, self.REC_ACTIONS[action])
                if repaired is not None:
                    return self._rec_view(repaired, user)
                raise ValueError("This suggestion has already been answered.")
            if action != "reject" and rec["source"] == "ai":
                if not self.ai_epoch_current(rec) or self.continuity_suspension("priority"):
                    raise PermissionError(
                        "AI output epoch changed or is suspended; use fresh work or the manual route."
                    )
                self.continuity_fence()
            if (
                action != "reject"
                and rec["source"] == "ai"
                and not self.release_current("priority", rec.get("release"), rec.get("model"))
            ):
                self.audit(
                    user["email"],
                    "ai_release_denied",
                    "-",
                    f"priority {rec_id}; use the manual route",
                )
                raise PermissionError("Release changed; use the ordinary case controls.")
            with priority_review(self, user, rec_id, action):
                final = None
                if action == "accept":
                    final = rec["items"]
                elif action == "edit":
                    mine = {
                        c["id"]
                        for c in self.cases.values()
                        if not c["closed"] and c["owner_code"] == user["code"]
                    }
                    final = []
                    for i in items or []:
                        cid = i.get("case_id") if isinstance(i, dict) else None
                        if cid not in mine or any(f["case_id"] == cid for f in final):
                            raise ValueError("Choose each of your own open cases at most once.")
                        final.append(dict(case_id=cid, reason=str(i.get("reason", ""))[:300]))
                    if not final or len(final) > 10:
                        raise ValueError("Keep between 1 and 10 cases.")
                metered = bool(rec.get("meter_root"))
                disposition = "edit-accept" if action == "edit" else action
                intent = (
                    self.ai.consumption.review_intent(rec_id, disposition, root=rec["meter_root"])
                    if metered
                    else None
                )
                rec.update(
                    status=self.REC_ACTIONS[action],
                    final_items=final,
                    reason=reason,
                    resolved_by=user["email"],
                    resolved_at=datetime.now().isoformat(timespec="seconds"),
                )
                ids = ",".join(i["case_id"] for i in final) if final else "-"
                self.audit(
                    user["email"],
                    f"ai_priority_{action}",
                    "-",
                    f"{rec_id} {reason} cases={ids}".strip(),
                )
                self.save()
                mark_priority_committed(self)
                if metered:
                    self.ai.consumption.review(rec_id, disposition, intent=intent)
                return self._rec_view(rec, user)

    def _repair_ai_review(self, rec, action, status):
        """Repair only financial attribution confirmed by the persisted human disposition."""
        root = rec.get("meter_root") or rec.get("envelope", {}).get("meter_root")
        if not root or rec["status"] != status:
            return None
        if hasattr(self, "db"):
            with self.dblock:
                row = self.db.execute(
                    "SELECT body FROM recommendations WHERE id=?", (rec["id"],)
                ).fetchone()
            saved = json.loads(row[0]) if row else None
        else:
            with open(self.live_path, encoding="utf-8") as source:
                saved = next(
                    (r for r in json.load(source)["recommendations"] if r["id"] == rec["id"]), None
                )
        if not saved or saved["status"] != status or saved["user"] != rec["user"]:
            return None
        saved_root = saved.get("meter_root") or saved.get("envelope", {}).get("meter_root")
        if saved_root != root or (
            saved.get("kind") == "ai_task" and saved.get("reviewer_action") != action
        ):
            return None
        disposition = "edit-accept" if action == "edit" else action
        intent = self.ai.consumption.pending_review(rec["id"], disposition)
        if intent is None:
            return None
        self.ai.consumption.review(rec["id"], disposition, intent=intent)
        return saved

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
                out.append(
                    dict(
                        id=c["id"],
                        resident=c["resident"]["name"],
                        address=c["home"]["address"],
                        area=c["home"]["area"],
                        route=c["funding"]["route"],
                        status=c["funding"]["status"],
                        owner=c["owner"],
                        have=sum(x["present"] for x in cl),
                        need=len(cl),
                        days=c["days_in_stage"],
                        grants=grant_summary(c),
                    )
                )
        order = {s: i for i, s in enumerate(self.FUND_FLOW)}
        out.sort(key=lambda x: (order[x["status"]] == 0, -x["days"]))
        return out

    def funding_draft(self, user, case_id, mode=None):
        with self.lock:
            c = self._case(case_id)
            missing = [x["kind"] for x in self.checklist(c) if not x["present"]]
            facts = (
                self._facts(c, False)
                + f" Built: {c['home']['built']}. Type: {c['home']['type']}. EPC band: {c['home']['epc']}. "
                f"Measures: {', '.join(c['measures']) if isinstance(c['measures'], list) else c['measures']}."
            )
            route = c["funding"]["route"]
            case = c
            tcites = ai_tasks.cites_for(
                c, "Address:", "Home type:", "EPC band:", "Built:", "Measures:", "Funding route:"
            )
            tmpl = (
                f"Funding application draft for {c['home']['address']} ({route})\n\nProperty: {c['home']['type']}, built "
                f"{c['home']['built']}, EPC {c['home']['epc']}.\nProposed measures: {c['measures']}.\n\n"
                + "\n".join(f"Needs: {m} document" for m in missing)
                + "\nNeeds: costs from the contractor\nNeeds: eligibility check by the Grants Officer"
            )
        sysmsg, prompt = ai_prompts.render(
            "funding_draft", route=route, facts=facts, missing=", ".join(missing) or "none"
        )
        self.audit(user["email"], "ai_run_start", case_id, "funding_draft")
        r = ai_tasks.run_text_task(
            self,
            user,
            "funding_draft",
            [case],
            sysmsg,
            prompt,
            tmpl,
            tcites,
            True,
            check=lambda t: all(m.lower() in t.lower() for m in missing) or "needs" in t.lower(),
            mode=mode,
        )
        with self.lock:
            c = self._case(case_id)
            c["funding"]["draft"] = r["text"]
            if c["funding"]["status"] in ("Not started", "To prepare"):
                c["funding"]["status"] = "Draft ready"
            self.audit(
                user["email"],
                "ai_run_end",
                case_id,
                f"funding_draft source={r['source']} model={r['model']}",
            )
            self.save()
        return dict(
            r,
            label="AI suggestion, not approved: nothing is submitted until a person approves and submits it"
            + ("" if r["verified"] else ". Unverified: its sources do not match the case record"),
        )

    # ---- review of any AI output, the comparison records and the live report
    def review_ai(self, user, rec_id, action, reason="", text=None):
        return ai_tasks.review(self, user, rec_id, action, reason, text)

    def ai_live_report(self, user=None, *, start=None, end=None, as_of=None, assistants_service=None):
        return ai_tasks.live_report(
            self,
            user=user,
            start=start,
            end=end,
            as_of=as_of,
            assistants_service=assistants_service,
        )

    def rai_readiness_report(self, user=None, *, assistants_service=None):
        from . import rai_control_plane

        if user is not None and user.get("role") not in MANAGER_ROLES:
            raise PermissionError("Only a manager can read the RAI readiness report.")
        return rai_control_plane.exercise_acceptance_report(
            self,
            user=user,
            assistants_service=assistants_service,
        )

    def activate_ai_task_live(
        self,
        user,
        task_id,
        approval=None,
        *,
        approved_by=None,
        named_approval_id=None,
        assistants_service=None,
        release_body=None,
    ):
        from . import rai_control_plane

        return rai_control_plane.activate_live_task(
            self,
            task_id,
            approval,
            approved_by=approved_by,
            named_approval_id=named_approval_id,
            actor=user,
            assistants_service=assistants_service,
            release_body=release_body,
        )

    def funding_step(self, user, case_id, action, text="", *, body=None, **extra):
        from .finance import _identity, classify_finance_operation, guard_no_automated_finance_authority

        payload = dict(body) if isinstance(body, dict) else {}
        if extra:
            payload.update(extra)
        payload.setdefault("action", action)
        op = classify_finance_operation("funding_step", action, payload)
        guard_no_automated_finance_authority(user, operation=op, body=payload)

        with self._finance_operation(user, case_id, operation=op) as (user, c):
            f = c["funding"]
            authority = None
            if action in ("approve", "submit", "confirm"):
                authority = self._financial_authority(
                    user, "application:" + action, case_id, f["route"]
                )
                if not isinstance(text, str) or not text.strip() or len(text) > 200:
                    raise ValueError(
                        "Enter the evidence reference for this application event, from 1 to 200 characters."
                    )
            if action == "save_draft":
                f["draft"] = (text or "")[:6000]
            elif action == "approve":
                if f["status"] != "Draft ready" or not f["draft"].strip():
                    raise ValueError("Write or generate a draft first.")
                missing = [x["kind"] for x in self.checklist(c) if not x["present"]]
                if missing:
                    raise GateError(
                        [
                            f"Evidence is missing: {', '.join(missing)}. Owner: {c['owner']}. Next action: add it to the case."
                        ]
                    )
                f.update(status="Approved", approved_by=user["name"])
            elif action == "submit":
                if f["status"] != "Approved":
                    raise ValueError("Approve the draft first.")
                ref = text.strip()
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
            if authority is not None:
                f.setdefault("history", []).append(
                    dict(
                        action=action,
                        at=datetime.now().isoformat(),
                        case_id=case_id,
                        route=f["route"],
                        source=text.strip(),
                        actor=_identity(user),
                        authority=authority,
                        source_status="Supplied, unverified",
                    )
                )
            self.audit(user["email"], f"funding_{action}", case_id, f["status"])

    def _case(self, case_id):
        c = self.cases.get(case_id)
        if not c:
            raise KeyError(case_id)
        self._touch(case_id)
        return c

    def export_csv(self, rows):
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(
            [
                "Reference",
                "Resident",
                "Address",
                "Town",
                "Postcode",
                "Phone",
                "Stage",
                "Status",
                "Owner",
                "Days in stage",
                "Last contact",
                "Next visit",
            ]
        )
        for s in rows:
            w.writerow(
                [
                    safe_cell(v)
                    for v in (
                        s["id"],
                        s["resident"],
                        s["address"],
                        s["town"],
                        s["postcode"],
                        s["phone"],
                        s["stage"],
                        s["status"],
                        s["owner"],
                        s["days"],
                        s["last_contact"] or "",
                        s["next_visit"] or "",
                    )
                ]
            )
        return buf.getvalue()

    def import_check(self, text):
        """Forgiving check of any spreadsheet export: map columns, report rows to fix, change nothing."""
        rows = list(csv.reader(io.StringIO(text)))
        if not rows:
            raise ValueError("The file is empty.")
        head = [h.strip() for h in rows[0]]
        guess = {
            "name": r"name|resident|tenant",
            "address": r"address|street|property",
            "postcode": r"post ?code|postal",
            "phone": r"phone|mobile|tel",
        }
        mapping = {
            k: next((i for i, h in enumerate(head) if re.search(p, h, re.I)), None)
            for k, p in guess.items()
        }
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
        return dict(
            columns=found,
            ready=good,
            to_fix=fix[:50],
            matched_existing=matched,
            message="Your file has not been changed.",
        )

    def import_check_workbook(self, name, data):
        """Row-level preview of an .xlsx case list: mapping, conflicts and rows; change nothing."""
        from .import_preview import preview_bytes
        from .xlsx import WorkbookError

        try:
            prev = preview_bytes(str(name or "workbook.xlsx")[:120], data)
        except WorkbookError as error:
            raise ValueError(f"We could not read that workbook: {error}.") from error
        known = {c["home"]["postcode"].replace(" ", "").upper() for c in self.cases.values()}
        rows = [
            dict(row=r.row, values=r.values, problems=r.problems, ready=not r.problems)
            for r in prev.rows
        ]
        return dict(
            kind="workbook",
            source_name=prev.source_name,
            source_sha256=prev.source_sha256,
            sheet=prev.sheet,
            columns=[dict(field=c.field, header=c.header, how=c.how) for c in prev.columns],
            unmapped_headers=prev.unmapped_headers,
            conflicts=prev.conflicts[:50],
            ready=prev.ready,
            to_fix_count=len(prev.to_fix),
            matched_existing=sum(
                1
                for r in prev.rows
                if r.values.get("postcode", "").replace(" ", "").upper() in known
            ),
            rows=rows[:200],
            rows_total=len(rows),
            message=prev.message,
        )
