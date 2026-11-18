<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #93 Deterministic No-Automated-Finance-Authority Invariant

## Metadata

* Task ID: issue-93-finance-no-auto-path
* Task slug: finance-93-no-auto-path
* Related plan: .copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/finance-93-no-auto-path-research.md, docs/brds/agentic-retrofit-programme-brd.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Core Deterministic No-Automated-Finance-Authority Guard and Verifier | Ready | P01, P01-T01, P01-T02 |
| P02 | End-to-End Invariant Test Suite, Documentation, and Focused Validation | Ready | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Core Deterministic No-Automated-Finance-Authority Guard and Verifier

### Context

Research (`C2`-`C18` in `.copilot-tracking/research/2026-11-15/finance-93-no-auto-path-research.md`) confirmed that `FinanceMixin._finance_operation` is shared by `FinanceMixin.finance_action`, `GrantMixin.grant_action`, and `Store.funding_step`, while `form_review.action` governs form-assisted funding/claim pack review. Hardening these boundaries in `src/core` closes automated, agent, worker, orchestrator, system, unauthenticated, non-human, and AI proposal-apply paths across both direct Python calls and HTTP routes in `src/api/src/zava_forward/api/server.py`.

### Intent

Introduce a structured `AutomatedFinanceAuthorityRefusedError(ValueError)` exception, deterministic guard `guard_no_automated_finance_authority`, operation classifier, SQL writer revalidation, and end-to-end invariant verifier `verify_no_automated_finance_authority` without disturbing existing `PermissionError` / `AuthorityGateError` behavior for human staff RBAC, independence, and stored grant-designation checks.

### Boundaries

* Included: `src/core/src/zava_forward/core/finance.py`, `src/core/src/zava_forward/core/grants.py`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/form_review.py`, and `src/api/src/zava_forward/api/server.py` (one-line `body=body` forwarding on `/api/cases/{cid}/funding`).
* Excluded: Creating non-existent `funding_packs.py` or `routers/finance_grants.py` shims; importing `zava_forward.{api,agents,orchestrator,importer}` inside `src/core`; changing web UI templates or `infra/`.

### Likely Targets

* `src/core/src/zava_forward/core/finance.py`: Fully type-annotated core error type, operation map, actor/payload guard, `finance_action`-scoped SQL stored-human revalidation, and AST + disposable-fixture `verify_no_automated_finance_authority`.
* `src/core/src/zava_forward/core/grants.py`: Read-only operation-specific guard call (`self.cases.get`) at `grant_action` entry before `refuse_bulk` / `_finance_operation`.
* `src/core/src/zava_forward/core/store.py`: Operation-specific guard call at `funding_step` entry (`approve` -> `approve_match_funding`, `submit` -> `submit_bid`, `confirm` -> `record_cash`, or automated shortcut actions), accepting optional `body=None`.
* `src/core/src/zava_forward/core/form_review.py`: Guard call at `action` entry rejecting automated/non-human/unauthenticated callers, proposal-apply payloads, and prohibited pack-submission/certification actions (`submit_bid`, `certify_claim`, `approve_match_funding`, `record_cash`, `submit`, `approve`, `certify`).
* `src/api/src/zava_forward/api/server.py`: Forward `body=body` in `s.funding_step(u, cid, body.get("action"), body.get("text", ""), body=body)` while preserving `"s.funding_step("`.

### Dependencies

* None.

### Validation Expectations

* `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `python3 -m mypy` in `src/core` (and `python3 -m ruff check` + `PYTHONPATH=../core/src:../agents/src python3 -m mypy` in `src/api`) pass with zero errors.
* Existing `test_dependency_rule.py`, `#93`, `#94`, `#95`, and `#104` unit tests continue passing with zero regressions.

### Completion Evidence

* `AutomatedFinanceAuthorityRefusedError`, `PROTECTED_FINANCE_OPERATIONS`, `guard_no_automated_finance_authority`, and `verify_no_automated_finance_authority` are importable from `zava_forward.core.finance` and enforced across all four modules.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement `AutomatedFinanceAuthorityRefusedError`, `guard_no_automated_finance_authority`, and `verify_no_automated_finance_authority` in `finance.py`

#### Context

`finance.py` owns `_finance_operation`, `validate_sql`, and `FinanceMixin.finance_action`. Today `_actor(self, user)` raises `AttributeError` when `user` is `None` or a string, and `_fin_budget_approve`, `_fin_commit_approve`, `_fin_disposition`, and `_fin_payment_status` do not reject automated caller markers, AI proposal-apply keys, or stored `financial_authority.human is False`.

#### Intent

Define the canonical `#93` / `RULE-010` error contract, operation classifier, pre-execution guard, SQL writer revalidation hook, and self-contained invariant verifier in `src/core/src/zava_forward/core/finance.py`.

#### Boundaries

* Included:
  * `PROTECTED_FINANCE_OPERATIONS = ("submit_bid", "approve_match_funding", "certify_claim", "record_cash")`.
  * `AutomatedFinanceAuthorityRefusedError(ValueError)` with `operation: str`, `actor_kind: str`, `reason: str`, `rule: str = "RULE-010"`, `code: str = "automated_finance_authority_refused"`, informative `ValueError` message, and `as_record() -> dict[str, str]`.
  * `classify_finance_operation(surface: str, action: object = None, body: object = None) -> str` mapping:
    * `funding_step`: `submit` / `submit_bid` / `auto_submit` -> `submit_bid`; `approve` / `approve_match_funding` / `auto_approve` -> `approve_match_funding`; `confirm` / `record_cash` / `auto_record_cash` -> `record_cash`; `certify` / `certify_claim` / `auto_certify` -> `certify_claim`.
    * `finance_action`: `budget_propose` / `budget_approve` / `commit_raise` / `commit_approve` / `approve_match_funding` / `auto_approve` -> `approve_match_funding`; `payment_status` / `disposition` / `record_cash` / `auto_record_cash` -> `record_cash`; `submit_bid` / `certify_claim` -> matching operation; other finance steps (`invoice_receive`, `invoice_match`, `hold_place`, `hold_release`) -> `approve_match_funding` / `finance_authority` guarded against automated actors.
    * `grant_action`: `to == "Cash received"` or `record_cash` -> `record_cash`; `grant_open` or `to == "Opportunity"` or `submit_bid` -> `submit_bid`; `to == "Award"` or `approve_match_funding` -> `approve_match_funding`; `grant_eligibility` or `to in ("Claimable", "Submitted", "Accepted")` or `certify_claim` -> `certify_claim`; when `grant_approve` has no `to` in `body`, resolve pending target read-only via `cases.get(case_id)` when available or default deterministically to `certify_claim`.
    * `form_review`: `submit` / `submit_bid` -> `submit_bid`; `approve` / `approve_match_funding` -> `approve_match_funding`; `record_cash` -> `record_cash`; `certify` / `certify_claim` / `review` / `open` / `diagnose` -> `certify_claim`.
  * Complete PEP 484 parameter and return type annotations on `PROTECTED_FINANCE_OPERATIONS`, `AutomatedFinanceAuthorityRefusedError` (`__init__`, `as_record`), `classify_finance_operation`, `guard_no_automated_finance_authority`, and `verify_no_automated_finance_authority` so strict-`mypy` test callers never trigger `disallow_untyped_calls` (`PC-003`).
  * `guard_no_automated_finance_authority(user: object, *, operation: str = "finance_authority", body: object = None, store: Any = None, check_stored_human: bool = False) -> None` checking:
    1. `user is None` or `not isinstance(user, dict)` (`actor_kind="unauthenticated"` or `"non_dict_caller"`).
    2. Blank/unauthenticated dict where both `email` and `code` are missing/blank (`actor_kind="unauthenticated"`).
    3. Explicit non-human/automated flags on `user`: `user.get("human") is False`, truthy `automated`, `is_automated`, `is_agent`, `is_system`, `worker`, `is_worker`, `service_principal`, `managed_identity`, `ai_generated`, or `isinstance(user.get("financial_authority"), dict) and user["financial_authority"].get("human") is False`.
    4. Automated principal metadata on `user`: `actor_type`, `kind`, `principal_type`, `identity_source`, `auth_provider`, `caller_type`, or `source` matching `{"automated", "automation", "system", "agent", "worker", "orchestrator", "bot", "service", "service_principal", "managed_identity", "daemon", "cron", "job", "scheduler", "ai", "assistant", "model", "llm", "unauthenticated", "anonymous", "webhook", "pipeline"}` (explicitly preserving human Entra/proxy values such as `"entra"` and `"trusted-proxy"`).
    5. Automated `role` values (`{"agent", "worker", "system", "orchestrator", "assistant", "automation", "bot", "service", "service_principal", "managed_identity", "background_worker"}`) or automated `email`/`code` prefixes (`system@`, `agent@`, `worker@`, `orchestrator@`, `bot@`, `noreply@`, `automation@`, `service-principal`, `managed-identity`, `auto-`, `bot-`, `sys-`, `agent-`, `worker-`, `orch-`).
    6. Proposal-apply / automated execution keys in `user` or `body` (when `isinstance(body, dict)`): `proposal_id`, `recommendation_id`, `assistant_task_id`, `ai_proposal`, `from_proposal`, `apply_proposal`, `auto_apply`, `envelope`, truthy `automated` / `ai_apply` / `approved`, `actor_type` in automated set, or `isinstance(body.get("source"), str) and body["source"].strip().lower() in {"ai", "ai_proposal", "assistant", "agent", "automated"}` (preserving human text citations like `source="SYN"`).
    7. Direct automated shortcut action names (`submit_bid`, `approve_match_funding`, `certify_claim`, `record_cash`, `auto_submit`, `auto_approve`, `auto_certify`, `auto_record_cash`).
    8. When `check_stored_human=True` and `store is not None` (enabled strictly in `finance_action` and recorded as `context["check_stored_human"] = True` in `_finance_operation(..., check_stored_human=False)` for `validate_sql` so `grant_action` keeps `AuthorityGateError(PermissionError)` in `#95` tests), inspect the stored `staff` row's `financial_authority` if present and reject `human is False` or stored automated flags with `AutomatedFinanceAuthorityRefusedError`.
  * `verify_no_automated_finance_authority(store: Any = None) -> dict[str, Any]`:
    1. Audits `bounded_ai.audit_registered_capabilities({})` and verifies `funding-evidence` and `funding_draft` exist, are `propose_only=True`, and forbid controlled approval/execution keys via `bounded_ai.enforce_proposal_only`, raising `AutomatedFinanceAuthorityRefusedError` on any violation.
    2. Performs pure AST source inspection (`ast.parse`, zero `import` of non-`core` packages, honoring `test_dependency_rule.py` and standalone `src-core` CI `deps=""`) across `zava_forward.core` automation modules (`ai.py`, `ai_consumption.py`, `ai_prompts.py`, `ai_registry.py`, `ai_tasks.py`, `assistants.py`, `chat_case_answers.py`, `chat_isolation.py`, `chat_panel.py`, `coordinator.py`, `resident_assistant.py`, `workflows.py`) plus sibling `src/agents/src` and `src/orchestrator/src` `.py` files when present in the repository layout, confirming none reference `finance_action`, `grant_action`, `funding_step`, or `_financial_authority`.
    3. If `store is not None`, takes a read-only before-snapshot of `store.cases` (calling `store._sync()` under `store.lock` if `hasattr(store, "_sync")`) and `len(store.audit_entries())` solely to assert after probing that the caller's `Store` or `SqlStore` was completely untouched; builds a fresh self-contained disposable synthetic `Store` in `TemporaryDirectory` with prepared budget, commitment, matched invoice, grant, funding draft, and form-pack fixtures, and executes live automated/agent/worker/orchestrator/system/unauthenticated/non-human/proposal-apply probes across all four `PROTECTED_FINANCE_OPERATIONS` (`submit_bid`, `approve_match_funding`, `certify_claim`, `record_cash`), verifying every probe raises `AutomatedFinanceAuthorityRefusedError` with matching `.operation` and leaves disposable store state and audit chain untouched.
    4. Returns a deterministic summary dict (`ok=True`, `rule="RULE-010"`, `operations=list(PROTECTED_FINANCE_OPERATIONS)`, `actors_checked`, `ai_capabilities_checked`, `module_boundaries_checked`, `probes_executed`).
* Excluded: Changing `AuthorityGateError(PermissionError)` behavior for human staff in `grants.require_authority`.

#### Likely Targets

* `src/core/src/zava_forward/core/finance.py`: Add exception, guard, classifier, `validate_sql` check, `finance_action` / `_finance_operation` calls, and `verify_no_automated_finance_authority`.

#### Dependencies

* `zava_forward.core.bounded_ai` and `zava_forward.core.ai_registry`.

#### Validation Expectations

* Guard rejects every automated/non-human/unauthenticated/proposal-apply probe with `AutomatedFinanceAuthorityRefusedError`; human `grant_open(source="SYN")` and human `PermissionError` tests remain green.

#### Completion Evidence

* `finance.py` changes pass `ruff check`, `mypy`, and unit tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Wire operation-aware automated-authority guards into `grants.py`, `store.py`, `form_review.py`, and `api/server.py`

#### Context

* `GrantMixin.grant_action` (`grants.py:114`) checks `action not in GRANT_ACTIONS` before entering `_finance_operation`, so calling `grant_action` with an automated actor and `action="certify_claim"` or `body={"action": "grant_approve", "proposal_id": "..."}` needs `guard_no_automated_finance_authority` right at entry, resolving `pending["to"]` read-only via `self.cases.get(case_id)` (after `self._sync()` under `self.lock` if `hasattr(self, "_sync")`, never calling `self._case(case_id)` or `self._touch(case_id)`) so `.operation` on `AutomatedFinanceAuthorityRefusedError` is exact without mutating `SqlStore` thread-local state.
* `Store.funding_step` (`store.py:2125`) checks `action not in ("approve", "submit", "confirm")` before entering `_finance_operation`, and `src/api/src/zava_forward/api/server.py:1871` calls `s.funding_step(u, cid, body.get("action"), body.get("text", ""))`. Extending `funding_step(self, user, case_id, action, text="", *, body=None, **extra)` and forwarding `body=body` at `server.py:1871` ensures automated actors, `submit_bid` shortcut actions, and HTTP/Python proposal-apply keys immediately raise `AutomatedFinanceAuthorityRefusedError` with the exact operation (`submit_bid`, `approve_match_funding`, `record_cash`).
* `form_review.action` (`form_review.py:478`) checks `kind not in ("open", "review", "diagnose")` after `controlled(...)`, so calling `guard_no_automated_finance_authority` at the top of `form_review.action` ensures automated callers, proposal-apply payloads, or automated pack submission/certification attempts (`kind in ("submit", "submit_bid", "approve", "approve_match_funding", "certify", "certify_claim", "record_cash")`) raise `AutomatedFinanceAuthorityRefusedError` while arbitrary unknown human kinds keep `ValueError("Unknown form review action.")`.

#### Intent

Ensure exact operation attribution (`submit_bid`, `approve_match_funding`, `certify_claim`, `record_cash`) on `AutomatedFinanceAuthorityRefusedError` across `grants.py`, `store.py`, `form_review.py`, and `api/server.py`.

#### Boundaries

* Included: `src/core/src/zava_forward/core/grants.py`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/form_review.py`, and `src/api/src/zava_forward/api/server.py`.
* Excluded: Changing valid human workflows in `funding_step`, `grant_action`, or `form_review.action`.

#### Likely Targets

* `src/core/src/zava_forward/core/grants.py`: Read-only `pending["to"]` lookup via `self.cases.get(case_id)` + `guard_no_automated_finance_authority` at `grant_action` entry.
* `src/core/src/zava_forward/core/store.py`: `guard_no_automated_finance_authority` at `funding_step` entry with optional `body=None` and `**extra`.
* `src/core/src/zava_forward/core/form_review.py`: `guard_no_automated_finance_authority` at `action` entry.
* `src/api/src/zava_forward/api/server.py`: Pass `body=body` into `s.funding_step(...)`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Existing `test_form_review.py`, `test_grant_lifecycle_controls.py`, and `test_funding_automation_boundary.py` pass 100%.

#### Completion Evidence

* Automated calls to `grant_action`, `funding_step`, and `form_review.action` raise `AutomatedFinanceAuthorityRefusedError` with exact `.operation` in `PROTECTED_FINANCE_OPERATIONS`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: End-to-End Invariant Test Suite, Documentation, and Focused Validation

### Context

Requirement 3 and Requirement 4 require a comprehensive end-to-end invariant test `src/core/tests/test_finance_no_automated_path_93.py` covering all four protected operations across core, agent/proposal apply, and orchestrator/automated actors, plus documenting the `#93` invariant in `src/core/README.md` and running `ruff check`, `mypy`, and `unittest`.

### Intent

Deliver complete executable proof of `#93` / `RULE-010` across JSON `Store`, `SqlStore`, AI proposal generation and acceptance (`funding_draft`, `funding-evidence`), `form_review` / `form_export`, `src/agents` and `src/orchestrator` actors/modules, and HTTP API endpoints, documented in `src/core/README.md`.

### Boundaries

* Included: `src/core/tests/test_finance_no_automated_path_93.py` and `src/core/README.md`.
* Excluded: Unrelated test files or web documentation.

### Likely Targets

* `src/core/tests/test_finance_no_automated_path_93.py`: New strict-`mypy`-clean test suite.
* `src/core/README.md`: New concise section documenting the `#93` no-automated-finance-authority guard and invariant verifier.

### Dependencies

* P01.

### Validation Expectations

* `cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy && PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` exits `0`.
* `cd src/api && python3 -m ruff check . && PYTHONPATH=../core/src:../agents/src python3 -m mypy` exits `0`.
* `PYTHONPATH=src/api/src:src/api/tests:src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/orchestrator/src python3 -m unittest src/api/tests/test_finance_match_api.py src/api/tests/test_grant_lifecycle_api.py -q` exits `0`.

### Completion Evidence

* Passing test output, zero `ruff` and `mypy` diagnostics, and updated `src/core/README.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Author `src/core/tests/test_finance_no_automated_path_93.py`

#### Context

`src/core/pyproject.toml` runs `mypy` with `strict = true` on `tests/`. Following the pattern in `test_epic104_bounded_ai_invariants.py`, type all test methods and helper fixtures explicitly (`-> None`, `Any` wrappers around untyped legacy modules).

#### Intent

Prove across both `Store` and `SqlStore` that no automated path can perform any of the four `#93` protected operations (`submit_bid`, `approve_match_funding`, `certify_claim`, `record_cash`), while designated independent human staff still complete legitimate workflows.

#### Boundaries

* Included:
  1. **Matrix across all 4 operations x automated actor classes (`Store` and `SqlStore`)**:
     * Actors: `None`, non-dict string (`"agent-worker"`), empty unauthenticated dict (`{}`), agent worker actor (`actor_type="agent"`, `code="AGENT-1"`), orchestrator job actor (`actor_type="orchestrator"`, `code="ORCH-1"`), system/service-principal actor (`actor_type="service_principal"`, `service_principal=True`), background assistant actor (`role="assistant"`, `automated=True`), and spoofed human-role dict with `human=False` (plus stored staff row with `financial_authority.human=False` on `finance_action`).
     * Operations (aligned 1-to-1 with `classify_finance_operation`):
       * `submit_bid`: `funding_step(..., "submit", "Bid ref")`, `grant_action(..., grant_open / grant_propose / grant_approve to="Opportunity")`, `grant_action(..., action="submit_bid")`, `form_review.action(..., "submit_bid")`.
       * `approve_match_funding`: `finance_action(..., budget_approve)`, `finance_action(..., commit_approve)`, `funding_step(..., "approve", "Match note")`, `grant_action(..., grant_propose / grant_approve to="Award")`.
       * `certify_claim`: `grant_action(..., grant_eligibility)`, `grant_action(..., grant_propose / grant_approve to="Claimable" / "Submitted" / "Accepted")`, `form_review.action(..., "certify_claim")` and `form_export.draft_export` remaining `Held` / `Not submitted`.
       * `record_cash`: `grant_action(..., grant_propose / grant_approve to="Cash received")`, `finance_action(..., payment_status="Paid outside this system")`, `finance_action(..., disposition="Accept for payment")`, `funding_step(..., "confirm", "Confirmation ref")`.
     * Assert `AutomatedFinanceAuthorityRefusedError` (and `isinstance(err, ValueError)`), structured `.as_record()` fields (`rule == "RULE-010"`, `code == "automated_finance_authority_refused"`, exact `operation`), zero state change on case `funding`/`grants`/`finance`, unchanged audit log length, and `store.verify_audit() is True`.
  2. **AI proposal generation, review, and proposal-apply refusal**:
     * Generate `funding_draft` proposal (`Store.funding_draft`) and accept it via `Store.review_ai(..., action="accept")`; generate `funding-evidence` proposal (`Assistants.request` + `execute`) and verify + accept it via `Assistants.review`; prove neither generation nor human proposal acceptance submits a bid, approves match funding, certifies a claim, or records cash, and attempting to pass proposal payloads (`proposal_id`, `recommendation_id`, `assistant_task_id`, `ai_proposal`, `apply_proposal`, `envelope`) into `finance_action`, `grant_action`, `funding_step(..., body=...)`, or `form_review.action` raises `AutomatedFinanceAuthorityRefusedError`.
  3. **Orchestrator and Agent Worker AST boundary checks (`ALLOWED = {"core"}`)**:
     * Without importing any `zava_forward.{api,agents,orchestrator,importer}` module, AST-parse `src/agents/src` and `src/orchestrator/src` when present in the repository layout (and verify `verify_no_automated_finance_authority` performs the same AST boundary check) to prove neither background worker dispatch nor orchestrator CLI jobs (`document-rescan`, `ranking-publish`, `source_monitor`) expose or invoke bid submission, match-funding approval, claim certification, or cash recording.
  4. **Invariant verifier & positive human control**:
     * Assert `verify_no_automated_finance_authority()` and `verify_no_automated_finance_authority(self.store)` (for both `Store` and `SqlStore`) return `ok=True` covering all 4 operations without mutating `self.store`, fail closed with `AutomatedFinanceAuthorityRefusedError` when an AI funding capability's `mode` is monkeypatched away from `propose-only`, and verify two independent designated humans (`self.a`, `self.b`) can still execute the legitimate two-person human path.
* Excluded: Importing `zava_forward.{api,agents,orchestrator,importer}` inside `src/core/tests/test_finance_no_automated_path_93.py` or modifying `src/api` test files.

#### Likely Targets

* `src/core/tests/test_finance_no_automated_path_93.py`.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `PYTHONPATH=src:tests python3 -m unittest tests/test_finance_no_automated_path_93.py -v` passes on both JSON `Store` and `SqlStore`, and `python3 -m mypy` + `python3 -m ruff check` pass cleanly.

#### Completion Evidence

* All tests in `test_finance_no_automated_path_93.py` pass under `unittest`, `mypy`, and `ruff`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Document `#93` invariant check in `src/core/README.md` and run focused validation

#### Context

`src/core/README.md` documents core controls and bounded-AI (`#104`) verification commands. Issue `#93` step 4 requires documenting the `#93` invariant check in `src/core/README.md`, and step 5 requires running `ruff check`, `mypy`, and `unittest` in `src/core`.

#### Intent

Add concise documentation of `AutomatedFinanceAuthorityRefusedError`, `PROTECTED_FINANCE_OPERATIONS`, `verify_no_automated_finance_authority`, and the `#93` test command to `src/core/README.md` (with zero `.copilot-tracking/` paths), then run full `src/core` lint, typecheck, and unit tests plus targeted `src/api` finance/grant tests.

#### Boundaries

* Included: `src/core/README.md` and local validation execution.
* Excluded: Unrelated READMEs.

#### Likely Targets

* `src/core/README.md`.

#### Dependencies

* P02-T01.

#### Validation Expectations

* `ruff check`, `mypy`, and `unittest discover` in `src/core` exit `0`.
* Targeted `src/api` finance/grant tests exit `0`.

#### Completion Evidence

* Updated `src/core/README.md` and clean validation command outputs recorded in `.copilot-tracking/changes/2026-11-15/finance-93-no-auto-path-changes.md`.

#### Unresolved Items

* None.
