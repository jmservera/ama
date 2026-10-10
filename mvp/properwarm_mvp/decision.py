"""Optional, source-bound Decision 1 proposals, with no workflow write authority.

Public guide checked 2026-10-10 (updated 2026-10-09):
https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision
POST /providers/microsoft/v1/systemone accepts model (deployment), state and
named questions. Answers are named choice/noul objects; response model is the
underlying model, not the deployment. No generated rationale is supplied.

The guide does not publish a complete response schema, probability rounding
tolerance, usage-counter schema or response model-version field. The strict
fixture contract below accepts choice/probabilities mappings, normalized to
within 1e-6 without repair, and flat nonnegative integer usage counters.
These conservative constraints still need an authorized synthetic provider
probe. Fake transport tests do not establish live provider conformance.

The shared guard is callable by Ai before *any* scoring/generation transport.
It does not modify Ai itself. Caller-supplied permissions/source kinds must
come from service authorization, not browser data. Shared spend accounting
must include reserved, accrued and unbilled liabilities across all clients.
"""

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from hashlib import sha256
import json
import math
import os
import sqlite3
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
import uuid
from pathlib import Path
import re
from threading import Lock
from time import perf_counter
import urllib.error
import urllib.parse
import urllib.request

REGISTRY_PATH = Path(__file__).resolve().parents[1] / "evals" / "decision_tasks.json"
API_PATH = "/providers/microsoft/v1/systemone"
TOKEN_SCOPE = "https://cognitiveservices.azure.com"
NO_MATCH = "__no_match__"
PROTECTED_FIELDS = frozenset({
    "declaration", "signature", "certification", "consent", "resident_decision",
    "eligibility", "approval", "payment", "submission", "quality_acceptance",
    "hazard", "hazard_release", "complaint", "withdrawal", "ranking",
})
_ID = re.compile(r"^[A-Za-z0-9_.:-]{1,100}$")
_HASH = re.compile(r"^[a-f0-9]{64}$")
JsonObject = dict[str, object]
Transport = Callable[[urllib.request.Request, float], object]


def load_registry() -> JsonObject:
    """Read the versioned local task definitions without enabling inference."""
    with REGISTRY_PATH.open(encoding="utf-8") as stream:
        return json.load(stream)


def _finite(value: object, *, positive: bool = False) -> bool:
    if type(value) not in (float, int):
        return False
    try:
        return math.isfinite(value) and (value > 0 if positive else value >= 0)
    except OverflowError:
        return False


@dataclass(frozen=True)
class InferenceConfig:
    """Operator-reviewed activation and liability ceiling, disabled by default.

    max_call_charge_usd is a reviewed upper bound, not an inferred model price.
    accrued_usd includes existing technology spend and unbilled liabilities.
    A caller sharing multiple clients must reserve spend atomically upstream.
    """

    authorized: bool = False
    access_reviewed: bool = False
    terms_reviewed: bool = False
    cost_reviewed: bool = False
    quota_reviewed: bool = False
    price_known: bool = False
    spend_paused: bool = True
    enabled_tasks: tuple[str, ...] = ()
    monthly_cap_usd: float = 450.0
    pause_at_usd: float = 405.0
    accrued_usd: float | None = None
    max_call_charge_usd: float | None = None
    spend_cap_enforced: bool = True

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "InferenceConfig":
        """Parse PW flags explicitly; AI_ENDPOINT never grants authorization."""
        env = os.environ if environ is None else environ

        def flag(name: str) -> bool:
            return env.get(name, "").strip().lower() == "true"

        def amount(name: str, default: float | None = None) -> float | None:
            try:
                return float(env[name]) if name in env else default
            except (TypeError, ValueError):
                return None

        return cls(
            authorized=flag("PW_INFERENCE_AUTHORIZED"),
            access_reviewed=flag("PW_INFERENCE_ACCESS_REVIEWED"),
            terms_reviewed=flag("PW_INFERENCE_TERMS_REVIEWED"),
            cost_reviewed=flag("PW_INFERENCE_COST_REVIEWED"),
            quota_reviewed=flag("PW_INFERENCE_QUOTA_REVIEWED"),
            price_known=flag("PW_INFERENCE_PRICE_KNOWN"),
            spend_paused=not (env.get("PW_INFERENCE_SPEND_PAUSED", "").lower() == "false"),
            enabled_tasks=tuple(x.strip() for x in env.get("PW_INFERENCE_TASKS", "").split(",") if x.strip()),
            monthly_cap_usd=amount("PW_INFERENCE_CAP_USD", 450.0),
            pause_at_usd=amount("PW_INFERENCE_PAUSE_AT_USD", 405.0),
            accrued_usd=amount("PW_INFERENCE_ACCRUED_USD"),
            max_call_charge_usd=amount("PW_INFERENCE_MAX_CALL_CHARGE_USD"),
            spend_cap_enforced=env.get("PW_INFERENCE_ENFORCE_CAP", "").lower() != "false",
        )


@dataclass(frozen=True)
class InferenceGuard:
    """A pre-transport decision; denial always preserves manual handling."""

    allowed: bool
    reason: str
    reviewer: str | None = None


def reserve_inference_charge(task_id: str, config: InferenceConfig, state_dir: str) -> dict:
    """Reserve a conservative upper liability across scoring/generation processes.

    Failed or timed-out calls keep their reservation. No automatic refund or
    monthly rollover can discard an unresolved charge; reconciliation is human-owned.
    """
    state = Path(state_dir)
    if not state_dir or not state.is_absolute() or not state.is_dir() or state.is_symlink():
        raise ValueError("An explicit existing absolute inference state directory is required.")
    path = state / "inference-liabilities.sqlite"
    if path.is_symlink():
        raise ValueError("Inference liability database must not be a symlink.")
    if not _finite(config.accrued_usd) or not _finite(config.max_call_charge_usd, positive=True):
        raise ValueError("Reviewed accrued spend and maximum call charge are required.")
    def units(value):
        return int((Decimal(str(value)) * 1_000_000).to_integral_value(rounding=ROUND_CEILING))
    base, charge = units(config.accrued_usd), units(config.max_call_charge_usd)
    pause = (min(units(config.pause_at_usd), units(config.monthly_cap_usd), 405_000_000)
             if config.spend_cap_enforced else None)
    if os.environ.get("PW_EXERCISE") == "1" and os.environ.get("PW_STORE") == "mssql":
        return _reserve_sql_charge(task_id, base, charge, pause)
    with sqlite3.connect(path, timeout=5) as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS liability_base (id INTEGER PRIMARY KEY CHECK(id=1), amount INTEGER NOT NULL)")
        connection.execute("CREATE TABLE IF NOT EXISTS reservations (id TEXT PRIMARY KEY, task TEXT NOT NULL, amount INTEGER NOT NULL, at TEXT NOT NULL)")
        connection.execute("BEGIN IMMEDIATE")
        previous = connection.execute("SELECT amount FROM liability_base WHERE id=1").fetchone()
        base = max(base, previous[0] if previous else 0)
        connection.execute("INSERT OR REPLACE INTO liability_base(id,amount) VALUES(1,?)", (base,))
        reserved = connection.execute("SELECT COALESCE(SUM(amount),0) FROM reservations").fetchone()[0]
        projected = base + reserved + charge
        if pause is not None and projected >= pause:
            connection.commit()
            return dict(allowed=False, reason="shared_liability_pause", projected_usd=projected / 1_000_000)
        reference = uuid.uuid4().hex
        connection.execute("INSERT INTO reservations VALUES(?,?,?,datetime('now'))", (reference, task_id, charge))
        connection.commit()
    return dict(allowed=True, reason="reserved_budget_override" if pause is None else
                "review_spend" if projected >= 360_000_000 else "reserved",
                reservation_id=reference, projected_usd=projected / 1_000_000,
                reserved_upper_charge_usd=charge / 1_000_000)


def _reserve_sql_charge(task_id: str, base: int, charge: int, pause: int | None) -> dict:
    """Use the exercise database's transaction lock and ledger-backed metadata."""
    from datetime import datetime, timezone
    from .mssqlstore import _Conn, connection_string
    import mssql_python

    connection = None
    try:
        connection = _Conn(connection_string(), os.environ.get("PW_SQL_TOKEN"))
        connection.execute("BEGIN IMMEDIATE")
        try:
            previous = connection.execute(
                "SELECT value FROM meta WHERE [key]=?", ("inference_liability_base",)).fetchone()
            base = max(base, int(previous[0]) if previous else 0)
            if previous:
                connection.execute("UPDATE meta SET value=? WHERE [key]=?",
                                   (str(base), "inference_liability_base"))
            else:
                connection.execute("INSERT INTO meta ([key],value) VALUES (?,?)",
                                   ("inference_liability_base", str(base)))
            rows = connection.execute(
                "SELECT value FROM meta WHERE [key] LIKE 'inference_reservation:%'").fetchall()
            reserved = sum(json.loads(row[0])["amount_micro_usd"] for row in rows)
            projected = base + reserved + charge
            if pause is not None and projected >= pause:
                connection.execute("COMMIT")
                return dict(allowed=False, reason="shared_liability_pause", projected_usd=projected / 1_000_000)
            reference = uuid.uuid4().hex
            record = dict(task=task_id, amount_micro_usd=charge, at=datetime.now(timezone.utc).isoformat())
            connection.execute("INSERT INTO meta ([key],value) VALUES (?,?)",
                               ("inference_reservation:" + reference, json.dumps(record)))
            connection.execute("COMMIT")
        except BaseException:
            connection.execute("ROLLBACK")
            raise
    except mssql_python.Error as error:
        raise ValueError("Azure SQL inference liability reservation failed.") from error
    finally:
        if connection is not None and connection.raw is not None:
            connection.raw.close()
    return dict(allowed=True, reason="reserved_budget_override" if pause is None else
                "review_spend" if projected >= 360_000_000 else "reserved",
                reservation_id=reference, projected_usd=projected / 1_000_000,
                reserved_upper_charge_usd=charge / 1_000_000)


def _valid_task(task: Mapping[str, object]) -> bool:
    for key in ("version", "question_version", "instructions", "reviewer", "fallback", "capability"):
        if not isinstance(task.get(key), str) or not task[key].strip():
            return False
    for key in ("permissions", "source_kinds", "field_scope", "workflow_scope"):
        values = task.get(key)
        if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v for v in values):
            return False
    for key in ("max_sources", "max_text_chars"):
        if type(task.get(key)) is not int or task[key] <= 0:
            return False
    if type(task.get("enabled")) is not bool:
        return False
    if task["capability"] == "decision-scoring":
        if (task.get("question_type") not in ("choice", "noul")
                or not isinstance(task.get("question_name"), str)
                or not _ID.fullmatch(task["question_name"])):
            return False
        for key in ("probability_threshold", "margin_threshold"):
            if not _finite(task.get(key), positive=True) or task[key] > 1:
                return False
    return task["capability"] in ("decision-scoring", "generative-drafting")


def inference_guard(
    task_id: str, capability: str, *,
    config: InferenceConfig | None = None,
    registry: Mapping[str, object] | None = None,
    permissions: Iterable[str] = (),
    source_kinds: Iterable[str] = (),
    source_count: int = 0,
    text_chars: int = 0,
    field: str = "",
    workflow: str = "",
) -> InferenceGuard:
    """Fail closed for task, capability, evidence, authorization and spend.

    This is reusable for legacy narrative tasks. Endpoint configuration is
    deliberately not an argument and cannot turn on inference.
    """
    cfg = config if config is not None else InferenceConfig.from_env()
    reg = registry if registry is not None else load_registry()
    tasks = reg.get("tasks")
    task = tasks.get(task_id) if isinstance(tasks, Mapping) else None
    if not isinstance(task, Mapping) or task.get("approved") is not True:
        return InferenceGuard(False, "unregistered_or_unapproved_task")
    reviewer = task.get("reviewer")

    def deny(reason: str) -> InferenceGuard:
        return InferenceGuard(False, reason, reviewer if isinstance(reviewer, str) else None)

    if not isinstance(reg.get("version"), str) or not reg["version"] or not _valid_task(task):
        return deny("invalid_registry")
    if task.get("capability") != capability:
        return deny("wrong_capability")
    if field in PROTECTED_FIELDS or (field and field not in task.get("field_scope", [])):
        return deny("prohibited_field")
    if workflow and workflow not in task.get("workflow_scope", []):
        return deny("wrong_workflow")
    if not set(task.get("permissions", [])).issubset(set(permissions)):
        return deny("source_permission_denied")
    kinds = tuple(source_kinds)
    if (type(source_count) is not int or not 0 < source_count <= task.get("max_sources", 0)
            or len(kinds) != source_count
            or not set(kinds).issubset(set(task.get("source_kinds", [])))
            or type(text_chars) is not int or not 0 < text_chars <= task.get("max_text_chars", 0)):
        return deny("source_scope_denied")
    if cfg.authorized is not True:
        return deny("operator_authorization_required")
    if any(value is not True for value in (
        cfg.access_reviewed, cfg.terms_reviewed, cfg.cost_reviewed, cfg.quota_reviewed,
    )):
        return deny("access_terms_cost_quota_review_required")
    if task.get("enabled") is not True and task_id not in cfg.enabled_tasks:
        return deny("task_disabled")
    if cfg.spend_paused is not False:
        return deny("spend_paused")
    if cfg.price_known is not True or not _finite(cfg.max_call_charge_usd, positive=True):
        return deny("unknown_price_or_charge")
    if not _finite(cfg.accrued_usd):
        return deny("invalid_cap_or_liability")
    if cfg.spend_cap_enforced and (not _finite(cfg.monthly_cap_usd, positive=True) or cfg.monthly_cap_usd > 450
            or not _finite(cfg.pause_at_usd, positive=True)
            or cfg.pause_at_usd > min(405, cfg.monthly_cap_usd)
            or not _finite(cfg.accrued_usd)):
        return deny("invalid_cap_or_liability")
    projected = cfg.accrued_usd + cfg.max_call_charge_usd
    if cfg.spend_cap_enforced and (projected >= cfg.pause_at_usd or projected > cfg.monthly_cap_usd):
        return deny("spend_limit")
    return InferenceGuard(True, "authorized", reviewer)


def inference_allowed(task_id: str, capability: str, **kwargs: object) -> bool:
    """Boolean convenience wrapper for the shared fail-closed guard."""
    return inference_guard(task_id, capability, **kwargs).allowed


@dataclass(frozen=True)
class DecisionConfig:
    """Endpoint and externally reviewed deployment metadata expectations.

    Returned model identity is checked separately from request deployment.
    Model version comes from reviewed deployment metadata, not the response.
    """

    endpoint: str = ""
    deployment: str = ""
    expected_model: str = "microsoft-decision-1"
    expected_model_version: str = "1"
    metadata_reviewed: bool = False
    metadata_endpoint: str = ""
    metadata_deployment: str = ""
    metadata_model: str = ""
    metadata_model_version: str = ""
    deployment_type: str = ""
    region: str = ""
    timeout_seconds: float = 30.0


class DecisionContractError(ValueError):
    """Safe response/request rejection with no provider body attached."""


def _hash(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True, allow_nan=False).encode()).hexdigest()


def _public_transport(request: urllib.request.Request, timeout: float) -> object:
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read(1_000_001)
    if len(raw) > 1_000_000:
        raise DecisionContractError("response_too_large")
    def unique_keys(pairs: list[tuple[str, object]]) -> JsonObject:
        result: JsonObject = {}
        for key, value in pairs:
            if key in result:
                raise DecisionContractError("duplicate_response_key")
            result[key] = value
        return result

    return json.loads(raw, object_pairs_hook=unique_keys)


def _managed_identity_token() -> str:
    endpoint = os.environ.get("IDENTITY_ENDPOINT")
    if endpoint:
        query = urllib.parse.urlencode({"resource": TOKEN_SCOPE, "api-version": "2019-08-01"})
        request = urllib.request.Request(
            f"{endpoint}?{query}", headers={"X-IDENTITY-HEADER": os.environ.get("IDENTITY_HEADER", "")},
        )
    else:
        query = urllib.parse.urlencode({"resource": TOKEN_SCOPE, "api-version": "2018-02-01"})
        request = urllib.request.Request(
            f"http://169.254.169.254/metadata/identity/oauth2/token?{query}", headers={"Metadata": "true"},
        )
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.load(response)["access_token"]


class DecisionClient:
    """Read-only proposal client; transport/token are injectable for fake tests."""

    def __init__(
        self, config: DecisionConfig | None = None, *,
        inference: InferenceConfig | None = None,
        registry: Mapping[str, object] | None = None,
        transport: Transport | None = None,
        token: Callable[[], str] | None = None,
        clock: Callable[[], float] = perf_counter,
    ) -> None:
        self.config = config or DecisionConfig()
        self.inference = inference if inference is not None else InferenceConfig.from_env()
        self.registry = json.loads(json.dumps(registry if registry is not None else load_registry()))
        self.transport = transport or _public_transport
        self.token = token or _managed_identity_token
        self.clock = clock
        self._reserved_usd = 0.0
        self._lock = Lock()

    def _configuration_error(self) -> str | None:
        cfg = self.config
        if any(not isinstance(value, str) for value in
               (cfg.endpoint, cfg.deployment, cfg.expected_model, cfg.expected_model_version,
                cfg.metadata_endpoint, cfg.metadata_deployment, cfg.metadata_model,
                cfg.metadata_model_version, cfg.deployment_type, cfg.region)):
            return "deployment_metadata_unverified"
        if not cfg.endpoint or not cfg.deployment:
            return "unconfigured"
        endpoint = urllib.parse.urlsplit(cfg.endpoint)
        if (endpoint.scheme != "https" or not endpoint.hostname or endpoint.username
                or endpoint.password or endpoint.query or endpoint.fragment
                or endpoint.path not in ("", "/") or endpoint.port not in (None, 443)
                or not endpoint.hostname.endswith((".services.ai.azure.com", ".cognitiveservices.azure.com",
                                                   ".openai.azure.com"))
                or not _ID.fullmatch(cfg.deployment)
                or not _finite(cfg.timeout_seconds, positive=True) or cfg.timeout_seconds > 120):
            return "invalid_endpoint_or_timeout"
        if (cfg.metadata_reviewed is not True
                or cfg.endpoint.rstrip("/") != cfg.metadata_endpoint.rstrip("/")
                or cfg.deployment != cfg.metadata_deployment
                or cfg.expected_model.casefold() != cfg.metadata_model.casefold()
                or cfg.expected_model_version != cfg.metadata_model_version
                or cfg.expected_model.casefold() != "microsoft-decision-1"
                or cfg.expected_model_version != "1"
                or cfg.deployment_type not in ("DataZoneStandard", "GlobalStandard")
                or not cfg.region):
            return "deployment_metadata_unverified"
        return None

    def propose(
        self, task_id: str, *, case_id: str, case_version: str,
        sources: Sequence[Mapping[str, object]],
        field: str, workflow: str,
        permissions: Iterable[str] = (),
        candidates: Sequence[Mapping[str, str]] = (),
        claim: str | None = None,
    ) -> JsonObject:
        """Return an unreviewed proposal or explicit manual/failure envelope.

        Source objects have id, case_id, version, hash, locator, kind and text.
        Candidates have id, source_id and text (an exact source substring).
        No source text, token, provider rationale or response body is returned.
        Inputs are snapshots: integration must recheck current versions before
        human review/application. This method never mutates those snapshots.
        """
        start = self.clock()
        task = self.registry.get("tasks", {}).get(task_id, {})
        envelope: JsonObject = {
            "task": task_id, "task_version": task.get("version"),
            "registry_version": self.registry.get("version"), "case_id": case_id,
            "case_version": case_version, "field": field, "workflow": workflow,
            "sources": [], "question_version": task.get("question_version"),
            "prompt_version": task.get("question_version"), "input_hash": None,
            "request_hash": None,
            "prompt_hash": None, "question_hash": None, "source_hash": None,
            "status": "disabled", "validated": False, "approval": "Not reviewed",
            "reviewer": task.get("reviewer"), "manual_route": task.get("fallback", "Manual review"),
            "selected_candidate": None, "supported": None, "probabilities": None,
            "probability": None, "margin": None,
            "probability_threshold": task.get("probability_threshold"),
            "margin_threshold": task.get("margin_threshold"),
            "provider": "microsoft", "deployment": self.config.deployment or None,
            "model": None, "model_version": None, "returned_model_version": None,
            "model_version_source": None, "usage": None, "latency_ms": 0.0,
            "reserved_upper_charge_usd": None, "actual_charge_usd": None,
            "error_class": None, "http_status": None, "reason": None,
            "explanation": "No model proposal; use the independent manual route.",
        }

        def finish(status: str, reason: str) -> JsonObject:
            envelope.update(status=status, reason=reason,
                            latency_ms=round(max(0, self.clock() - start) * 1000, 3))
            return envelope

        try:
            state, question, references = self._inputs(
                task, case_id, case_version, sources, candidates, claim, field,
            )
        except (DecisionContractError, TypeError, ValueError, KeyError):
            return finish("failed", "invalid_source_or_candidate_snapshot")
        envelope.update(
            sources=references, source_hash=_hash(references),
            question_hash=_hash(question), prompt_hash=_hash(task.get("instructions")),
        )
        with self._lock:
            cfg = self.inference
            if _finite(cfg.accrued_usd):
                cfg = replace(cfg, accrued_usd=cfg.accrued_usd + self._reserved_usd)
            guard = inference_guard(
                task_id, "decision-scoring", config=cfg, registry=self.registry,
                permissions=permissions, source_kinds=[s["kind"] for s in sources],
                source_count=len(sources), text_chars=len(json.dumps(state)),
                field=field, workflow=workflow,
            )
            if not guard.allowed:
                return finish("disabled", guard.reason)
            try:
                problem = self._configuration_error()
            except (TypeError, ValueError):
                problem = "invalid_endpoint_or_timeout"
            if problem:
                return finish("unconfigured" if problem == "unconfigured" else "failed", problem)
            if os.environ.get("PW_EXERCISE") == "1":
                try:
                    reservation = reserve_inference_charge(task_id, self.inference, os.environ.get("PW_STATE", ""))
                except (OSError, sqlite3.Error, ValueError):
                    return finish("disabled", "shared_liability_ledger_unavailable")
                if not reservation["allowed"]:
                    return finish("disabled", reservation["reason"])
                envelope["liability_reservation"] = reservation
            else:
                # Fake/client-only use outside the exercise retains its local upper bound.
                self._reserved_usd += cfg.max_call_charge_usd
            envelope["reserved_upper_charge_usd"] = cfg.max_call_charge_usd
        body = {"model": self.config.deployment, "state": state,
                "questions": {task["question_name"]: question}}
        envelope["request_hash"] = _hash(body)
        envelope["input_hash"] = _hash({
            "request": body, "sources": references, "case_id": case_id,
            "case_version": case_version, "registry_version": envelope["registry_version"],
            "task_version": envelope["task_version"], "question_version": envelope["question_version"],
        })
        try:
            access_token = self.token()
            if not isinstance(access_token, str) or not access_token.strip():
                raise PermissionError("missing_token")
            request = urllib.request.Request(
                self.config.endpoint.rstrip("/") + API_PATH,
                data=json.dumps(body, allow_nan=False).encode(),
                headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json",
                         "Accept": "application/json"},
                method="POST",
            )
            payload = self.transport(request, self.config.timeout_seconds)
            answer, model, usage = self._response(payload, task, question)
        except urllib.error.HTTPError as exc:
            envelope.update(http_status=exc.code, error_class="HTTPError")
            reason = "authentication" if exc.code in (401, 403) else "rate_limited" if exc.code == 429 else "provider_http"
            return finish("failed", reason)
        except (TimeoutError, urllib.error.URLError) as exc:
            timeout = isinstance(exc, TimeoutError) or isinstance(getattr(exc, "reason", None), TimeoutError)
            envelope["error_class"] = "TimeoutError" if timeout else "URLError"
            return finish("failed", "timeout" if timeout else "transport_unavailable")
        except PermissionError:
            envelope["error_class"] = "PermissionError"
            return finish("failed", "authentication")
        except (DecisionContractError, ValueError, TypeError, KeyError, UnicodeError):
            envelope["error_class"] = "DecisionContractError"
            return finish("failed", "malformed_response")
        except Exception:
            # Provider/token boundary: preserve safe class only, never exception text/body.
            envelope["error_class"] = "ProviderError"
            return finish("failed", "provider_failure")
        envelope.update(
            model=model, usage=usage, model_version=self.config.metadata_model_version,
            model_version_source="reviewed_deployment_metadata", region=self.config.region,
            deployment_type=self.config.deployment_type, validated=True,
        )
        if question["type"] == "choice":
            probabilities = answer["probabilities"]
            choice = answer["choice"]
            probability = probabilities[choice]
            runner_up = max(p for option, p in probabilities.items() if option != choice)
            margin = probability - runner_up
            eligible = (choice != NO_MATCH and probability >= task["probability_threshold"]
                        and margin >= task["margin_threshold"])
            envelope.update(probabilities=probabilities, probability=probability, margin=margin,
                            selected_candidate=choice if eligible else None)
        else:
            probability = answer["probability"]
            margin = probability - (1 - probability)
            eligible = probability >= task["probability_threshold"] and margin >= task["margin_threshold"]
            envelope.update(probability=probability, margin=margin, supported=True if eligible else None)
        envelope["explanation"] = (
            "Application threshold checks allow a source-bound suggestion for human review; not a model rationale."
            if eligible else "No permitted suggestion meets application thresholds; manual review remains required."
        )
        return finish("proposed" if eligible else "no_match", "thresholds_met" if eligible else "abstained")

    def _inputs(
        self, task: Mapping[str, object], case_id: str, case_version: str,
        sources: Sequence[Mapping[str, object]], candidates: Sequence[Mapping[str, str]],
        claim: str | None, field: str,
    ) -> tuple[JsonObject, JsonObject, list[JsonObject]]:
        if not isinstance(case_id, str) or not _ID.fullmatch(case_id) or not isinstance(case_version, str) or not case_version:
            raise DecisionContractError("invalid_case")
        references: list[JsonObject] = []
        evidence: list[JsonObject] = []
        source_map: dict[str, str] = {}
        keys = {"id", "case_id", "version", "hash", "locator", "kind", "text"}
        if not sources:
            raise DecisionContractError("missing_sources")
        for source in sources:
            if (not isinstance(source, Mapping) or set(source) != keys
                    or any(not isinstance(v, str) or not v.strip() for v in source.values())
                    or source["case_id"] != case_id or not _ID.fullmatch(source["id"])
                    or not _HASH.fullmatch(source["hash"]) or source["id"] in source_map):
                raise DecisionContractError("invalid_source")
            source_map[source["id"]] = source["text"]
            references.append({k: source[k] for k in sorted(keys - {"text"})})
            evidence.append({"source_id": source["id"], "text": source["text"]})
        state: JsonObject = {"field": field, "evidence": evidence}
        question: JsonObject = {"type": task.get("question_type"), "instructions": task.get("instructions")}
        if task.get("question_type") == "choice":
            if claim is not None or not 0 < len(candidates) <= task.get("max_candidates", 0):
                raise DecisionContractError("invalid_candidates")
            criteria = {NO_MATCH: "No candidate is supported, evidence conflicts or context is insufficient"}
            bindings: list[JsonObject] = []
            for candidate in candidates:
                if (set(candidate) != {"id", "source_id", "text"}
                        or any(not isinstance(v, str) or not v.strip() for v in candidate.values())
                        or not _ID.fullmatch(candidate["id"]) or candidate["id"] in criteria
                        or candidate["source_id"] not in source_map
                        or candidate["text"] not in source_map[candidate["source_id"]]):
                    raise DecisionContractError("unbound_candidate")
                criteria[candidate["id"]] = candidate["text"]
                bindings.append(dict(candidate))
            state["candidates"] = bindings
            question["criteria"] = criteria
        elif task.get("question_type") == "noul":
            if candidates or not isinstance(claim, str) or not claim.strip():
                raise DecisionContractError("missing_claim")
            state["claim"] = claim
            question["criteria"] = dict(task["criteria"])
        return state, question, references

    def _response(
        self, payload: object, task: Mapping[str, object], question: Mapping[str, object],
    ) -> tuple[JsonObject, str, JsonObject]:
        if not isinstance(payload, dict) or set(payload) != {"answers", "model", "usage"}:
            raise DecisionContractError("unexpected_response_keys")
        if payload["model"] != self.config.expected_model:
            raise DecisionContractError("unexpected_model")
        usage = payload["usage"]
        if (not isinstance(usage, dict) or not usage or len(usage) > 16
                or any(not isinstance(k, str) or not _ID.fullmatch(k)
                       or type(v) is not int or not _finite(v) for k, v in usage.items())):
            raise DecisionContractError("invalid_usage")
        answers = payload["answers"]
        if not isinstance(answers, dict) or set(answers) != {task["question_name"]}:
            raise DecisionContractError("unexpected_questions")
        answer = answers[task["question_name"]]
        if not isinstance(answer, dict) or answer.get("type") != question["type"]:
            raise DecisionContractError("unexpected_answer_type")
        if question["type"] == "choice":
            if set(answer) not in ({"type", "choice", "probabilities"},
                                  {"type", "choice", "probabilities", "confidence"}):
                raise DecisionContractError("unexpected_choice_keys")
            if "confidence" in answer and (not _finite(answer["confidence"]) or answer["confidence"] > 1):
                raise DecisionContractError("invalid_choice_confidence")
            probabilities = answer["probabilities"]
            if (not isinstance(probabilities, dict) or set(probabilities) != set(question["criteria"])
                    or not all(_finite(p) and p <= 1 for p in probabilities.values())
                    or not math.isclose(math.fsum(probabilities.values()), 1, rel_tol=0, abs_tol=1e-6)):
                raise DecisionContractError("invalid_probability_vector")
            choice = answer["choice"]
            if (not isinstance(choice, str) or choice not in probabilities
                    or probabilities[choice] != max(probabilities.values())):
                raise DecisionContractError("choice_not_allowed_argmax")
        elif question["type"] == "noul":
            if (set(answer) != {"type", "probability"}
                    or not _finite(answer["probability"]) or answer["probability"] > 1):
                raise DecisionContractError("invalid_noul")
        else:
            raise DecisionContractError("unsupported_question_type")
        return json.loads(json.dumps(answer)), payload["model"], dict(usage)
