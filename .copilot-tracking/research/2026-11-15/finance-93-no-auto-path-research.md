---
description: "Primary evidence artifact for issue #93 finance no-automated-path invariant research"
---
<!-- markdownlint-disable-file -->

# Task Research: finance-93-no-auto-path

| Field              | Value                                                                    |
|--------------------|--------------------------------------------------------------------------|
| Date               | 2026-11-15                                                               |
| Researcher / agent | RPI Agent (`rpi-research`)                                               |
| Status             | Complete                                                                 |
| Artifact path      | .copilot-tracking/research/2026-11-15/finance-93-no-auto-path-research.md |

## Research Brief

* What to research: How `src/core/src/zava_forward/core/finance.py`, `grants.py`, `funding_packs.py`, `src/agents/`, `src/orchestrator/`, and `src/api/src/zava_forward/api/routers/finance_grants.py` currently model and guard the four protected financial/grant operations (`submit_bid`, `approve_match_funding`, `certify_claim`, `record_cash`), what actor/proposal/orchestrator call paths exist, and how to enforce and verify a deterministic `AutomatedFinanceAuthorityRefusedError` (`ValueError` subclass) and `verify_no_automated_finance_authority` invariant.
* Why it matters: Issue `#93` ("Epic: Finance, grants and form-assisted funding evidence") has an unticked engineering acceptance criterion: `No automated path submits a bid, approves match funding, certifies a claim or records cash` grounded in BRD `BG-007`, `BG-008`, `FR-018`, `FR-019`, `RULE-009` to `RULE-012`, `CON-005`, `CON-006` and PRD `FR-018`, `FR-019`, `FR-038` to `FR-043`.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` in this confirmed automatic RPI session, plus PR reviewers on parent branch `feat/demo-164-chat-grounding-provenance-0900`.
* Scope: `src/core/` (`finance.py`, `grants.py`, `funding_packs.py`, proposal/apply/actor helpers, README, tests), `src/agents/`, `src/orchestrator/`, `src/api/src/zava_forward/api/routers/finance_grants.py`, and BRD/PRD references for `#93`.
* Non-goals: Closing epic `#93` itself (stabilization checkpoint `#440` and child-feature closure remain separate), pushing to remote, modifying unrelated web UI or Azure infrastructure.
* Criteria: Every protected operation and automated/proposal/orchestrator entry path mapped with `path:line` `C#` evidence; contrarian bypass paths tested in analysis; focused validation command set verified.
* Requested outputs: Convergence recommendation for deterministic core guard, structured refusal error, invariant verifier, end-to-end invariant test `src/core/tests/test_finance_no_automated_path_93.py`, and `src/core/README.md` documentation.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                   |
|----------------------------------|-------------------------------------------------------------------------|
| Research question(s)             | Q1-Q5 covering protected operations, actor/identity contracts, agent/proposal apply & orchestrator paths, bypass vectors, and documentation/test conventions |
| Codebase scope                   | `src/core/`, `src/agents/`, `src/orchestrator/`, `src/api/`, `docs/brds/`, `docs/prds/` |
| External scope                   | none (codebase and local BRD/PRD governance specifications)             |
| Initial internal candidate areas | `src/core/src/zava_forward/core/finance.py`, `grants.py`, `funding_packs.py`, `src/agents/`, `src/orchestrator/`, `src/api/src/zava_forward/api/routers/finance_grants.py`, `src/core/README.md` |
| Initial external candidate areas | none                                                                    |
| Research posture                 | focused                                                                 |
| Posture provenance               | caller-specified (bounded internal engineering task with named targets and focused validation tier) |
| Explicit limits / deadline       | Focused validation tier; do not push; leave clean frozen HEAD           |
| Posture-specific completion basis | focused scope and materiality across all four operations and automated/agent/orchestrator paths |
| Edits allowed during research?   | no, research-only                                                       |
| Resolved evidence root           | .copilot-tracking/                                                      |
| Known constraints / excluded sources | Never read private datasets; preserve existing human-approved behavior and API contracts |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches repository root and `src/` | Repository structure, focused tier validation, mypy/ruff/unittest rules, branch/commit conventions | Selected: mandatory repo instructions |
| Skill               | `python-foundational`            | Python library/typing/testing topic match         | Optional general Python guidance             | Skipped: existing `src/core` conventions and strict `mypy`/`ruff` config provide exact local contracts |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered general RPI research subagent     | Delegated independent lane artifact          | Skipped (inline fallback): bounded internal 6-file trace is tightly coupled across `core`, `agents`, `orchestrator`, and `api` |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive session with complete caller brief, named files, error class (`AutomatedFinanceAuthorityRefusedError` / `ValueError`), verifier (`verify_no_automated_finance_authority`), and test file path. | No interaction available or needed | Proceed in focused convergence mode across all named targets |
| Direction change | `funding_packs.py` and `routers/finance_grants.py` do not exist; mapped responsibilities to `forms.py`, `form_review.py`, `form_export.py`, `store.py`, and `api/server.py`. | n/a | Keep scope tightly aligned to actual module layout without inventing placeholder modules |
| Convergence      | All 4 `#93` / `RULE-010` operations, actor checks, proposal-apply boundaries, and contrarian bypass vectors verified across `core`, `agents`, `orchestrator`, and `api`. | n/a | Converge on deterministic guard + `AutomatedFinanceAuthorityRefusedError(ValueError)` + `verify_no_automated_finance_authority` in `finance.py` |

## Scope and Success Criteria

* Scope: Inspect `finance.py`, `grants.py`, `funding_packs.py`, `src/agents/`, `src/orchestrator/`, `finance_grants.py`, and related proposal/audit/actor modules in `src/core`.
* Assumptions:
  * All four operations exist or map cleanly onto domain functions in `finance.py`, `grants.py`, and/or `funding_packs.py`.
  * Automated actors, system/worker identities, unauthenticated/blank actors, and AI proposal apply paths have identifiable representations in `src/core`, `src/agents`, `src/orchestrator`, and `src/api`.
* Success criteria:
  * Every research question is answered with `C#` `path:line` evidence.
  * Contrarian bypass vectors (spoofed actor strings, whitespace/case variants, system/service principals, proposal apply, background worker dispatch, direct function calls) are evaluated.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect `finance.py`, `grants.py`, `funding_packs.py`, `src/agents/`, `src/orchestrator/`, and `finance_grants.py`; design deterministic guard + `verify_no_automated_finance_authority` + `AutomatedFinanceAuthorityRefusedError(ValueError)`; design end-to-end invariant test `test_finance_no_automated_path_93.py` and `src/core/README.md` update.
* Inferred research questions: Exact function signatures, caller expectations in `src/api` and existing tests, proposal/apply mechanics, orchestrator task types, and actor/role validation conventions in `src/core`.
* Caller constraints and non-goals: Focused validation tier (`ruff check`, `mypy`, `unittest`), no `git push`, preserve existing legitimate human workflows.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Focused validation tier; target `#93` no-automated-path criterion without closing epic `#93` or pushing | Caller intake | Bound research to finance/grants/funding authority and automated/agent/orchestrator paths |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status   |
|---:|------------------|------------------------------------------|-----------|----------|
| Q1 | Which exact functions and endpoints implement submitting a bid, approving match funding, certifying a claim, and recording cash across `finance.py`, `grants.py`, `funding_packs.py`, and `finance_grants.py`? | straightforward | H | answered |
| Q2 | How are human vs automated/system/agent/worker/unauthenticated callers represented and validated across `src/core`, `src/api`, `src/agents`, and `src/orchestrator`? | depth | H | answered |
| Q3 | Can AI agent outputs, proposal apply paths, or orchestrator workers reach or mutate bid submission, match-funding approval, claim certification, or cash recording states? | breadth | H | answered |
| Q4 | What contrarian bypass vectors exist (e.g., direct core calls with agent/worker/system actor names, empty/None actors, role-less dicts, proposal payload injection, funding pack export/stage mutations, or status-update shortcuts)? | depth | H | answered |
| Q5 | What existing tests, `ValueError` / HTTP error mappings in `finance_grants.py`, and `src/core/README.md` sections must remain compatible or be updated? | straightforward | M | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, GitHub issue `#93`.
* Reused (verified) findings: Grant & Funding Agent is L3 ("drafts, finance submits") in Case Study 48; Addendum confirms automatic proposal generation is not automatic case action and no model receives cost/contract authority; Issue `#93` specifies budget, invoice, grant, and claim states remain separate, record-only, and human-approved.
* Superseded / stale: Legacy `mvp/` path mentioned in issue `#93` body was retired at cut-over (`v0.21.0`) in favor of `src/core`, `src/agents`, `src/api`, `src/orchestrator`.

## Research Cycle Log

### Cycle 1

* Active direction controls: Focused intake scope; map prompt filenames (`funding_packs.py`, `routers/finance_grants.py`) to actual repository modules (`forms.py`, `form_review.py`, `form_export.py`, `store.py`, `api/server.py`).
* Active research posture and completion basis: focused; focused scope and materiality across all four `#93` / `RULE-010` operations and automated/agent/orchestrator paths.
* Explicit limits or deadline effect: none on read-only codebase inspection.

#### Wave 1: Wider (Inline)

* Investigated module inventory across `src/core/src/zava_forward/core/`, `src/agents/src/zava_forward/agents/`, `src/orchestrator/src/zava_forward/orchestrator/`, `src/api/src/zava_forward/api/`, and `docs/brds/agentic-retrofit-programme-brd.md` (`C1`-`C8`).
* Confirmed `funding_packs.py` does not exist; form-assisted funding/claim pack preparation and export live in `forms.py`, `form_review.py`, `form_export.py`, and `store.py` (`funding_draft`, `funding_step`) (`C4`-`C7`).
* Confirmed `src/api/src/zava_forward/api/routers/finance_grants.py` does not exist; HTTP endpoints for `/api/cases/{cid}/finance`, `/api/cases/{cid}/grant`, `/api/cases/{cid}/funding`, and `/api/cases/{cid}/funding-draft` live in `src/api/src/zava_forward/api/server.py` (`C8`).
* Anchored requirement in BRD `RULE-010` and `AC-035`: no automated path submits a bid, approves match funding, certifies a claim, or records cash (`C1`).

#### Wave 2: Deeper (Inline)

* Traced all four protected operations to exact core methods (`C2`, `C3`, `C6`, `C7`):
  1. **Submit bid**: `Store.funding_step(..., action="submit")` (`application:submit`), `GrantMixin.grant_action(..., {"action": "grant_propose"|"grant_approve", "to": "Submitted"|"Opportunity"})`, and form export/pack submission holds in `form_review.action` / `form_export.draft_export`.
  2. **Approve match funding**: `FinanceMixin.finance_action(..., {"action": "budget_approve"|"commit_approve"|"disposition"})` and `Store.funding_step(..., action="approve")` (`application:approve`), plus `GrantMixin.grant_action(..., {"to": "Award"})`.
  3. **Certify claim**: `GrantMixin.grant_action(..., {"action": "grant_eligibility"})`, `GrantMixin.grant_action` proposing/approving `Claimable`, `Submitted`, or `Accepted`, and `form_review.action` blocking `HUMAN_ONLY = ("declaration", "signature", "attestation", "consent", "approval")` categories (`C4`, `C5`).
  4. **Record cash**: `GrantMixin.grant_action` proposing/approving `Cash received` (`grant:Cash received`), `FinanceMixin.finance_action(..., {"action": "payment_status"})`, and `Store.funding_step(..., action="confirm")` (`application:confirm`).
* Confirmed `FinanceMixin._finance_operation(self, user, case_id)` (`finance.py:155`) is the shared transactional choke point entered by `finance_action`, `grant_action`, and `funding_step` (`C2`, `C3`, `C7`).
* Verified `bounded_ai.py`, `assistants.py`, and `ai_tasks.py` enforce `propose-only` envelopes (`funding-evidence`, `funding_draft`); accepting an AI proposal via `ai_tasks.review` or `Assistants.review` updates only recommendation/assistant review metadata (`effect="Not an instruction; records the review only..."`) and never calls finance, grant, or funding mutations (`C10`, `C11`, `C12`).
* Verified `src/agents` (`worker.py`, `dispatch.py`) only executes bounded assistant proposals (`C13`) and `src/orchestrator` (`__main__.py`, `document_rescan.py`, `ranking_publish.py`, `source_monitor.py`, `rebuild.py`, `rebuild_azure.py`) only runs document virus/rescan sweeps, ranking publication, regulatory source discovery, and synthetic Azure resource/consumption-budget rehearsals (`C14`, `C15`).

#### Wave 3: Contrarian (Inline)

* Tested adversarial bypass vectors against `_finance_operation`, `finance_action`, `grant_action`, `funding_step`, and `form_review.action` (`C2`, `C3`, `C5`, `C9`, `C16`, `C17`):
  1. **Non-dict / `None` / string callers**: `_actor(store, user)` (`change_provenance.py:16`) calls `user.get("email")` directly, raising `AttributeError` on `None` or string callers (e.g., `"system"`, `"agent-worker"`) rather than a structured refusal error (`C9`).
  2. **Automated / system / agent / worker / orchestrator / non-human actor dicts and seeded service accounts**: `_fin_budget_approve`, `_fin_commit_approve`, `_fin_disposition`, and `_fin_payment_status` in `finance.py:217-322` check staff role and `_independent(...)` without calling `require_authority` (`C2`). An actor dict carrying automated/non-human markers (`human=False`, `automated=True`, `actor_type="agent"|"system"|"worker"|"orchestrator"|"service"`, `service_principal=True`, automated email/code/role tokens) or a seeded staff row with `financial_authority.human=False` is not explicitly intercepted by a deterministic `AutomatedFinanceAuthorityRefusedError(ValueError)` guard in `finance.py`.
  3. **AI proposal-apply payload injection**: Passing proposal-apply fields (`proposal_id`, `recommendation_id`, `assistant_task_id`, `ai_proposal`, `apply_proposal`, `from_proposal`, `auto_apply`, `envelope`) or canonical shortcut actions (`submit_bid`, `approve_match_funding`, `certify_claim`, `record_cash`) into `finance_action`, `grant_action`, `funding_step`, or `form_review.action` lacks a structured `AutomatedFinanceAuthorityRefusedError` refusal explaining `RULE-010`.
  4. **Existing `#94` and `#95` test compatibility**: Inspected `test_grant_lifecycle_controls.py`, `test_finance_match_controls.py`, `test_funding_automation_boundary.py`, `test_finance_match_api.py`, and `test_grant_lifecycle_api.py` (`C16`, `C17`, `C18`). Human-shaped staff denial tests (`person("FAKE", ...)`, forged `oid`/`name`, `self.plain` without designation, non-independent alias, and `self.b` when stored `staff` `financial_authority.human` is mutated to `False` in `test_grant_lifecycle_controls.py:165`) assert `PermissionError` (HTTP `403`). Meanwhile, `server.py:1875-1879` maps `ValueError` (including `AutomatedFinanceAuthorityRefusedError(ValueError)`) to HTTP `400` (`{"error": str(e)}`) (`C8`). Therefore, caller-level automated/system/agent/worker/orchestrator/unauthenticated/non-human callers, proposal-apply payloads, direct automated action names, and stored non-human authority on `finance_action` must raise `AutomatedFinanceAuthorityRefusedError(ValueError)` before `_actor`, while preserving `PermissionError` / `AuthorityGateError` for registered/unregistered human-shaped staff RBAC, independence, and stored grant-designation checks.
  5. **Strict typing & lint checks**: `src/core/pyproject.toml` sets `mypy` `strict = true` globally while `zava_forward.core.finance` and `zava_forward.core.grants` have legacy `ignore_errors = true` (`C19`). Any new test file `src/core/tests/test_finance_no_automated_path_93.py` is type-checked under strict `mypy` and checked by `ruff check` (`E,F,I,B,UP`, line-length 100).

* Cycle re-entry check: All five research questions (`Q1`-`Q5`) are answered with `C#` codebase citations; contrarian bypass paths and compatibility constraints are resolved; no further cycle is required.

## Evidence Log

| ID  | Source (`path:line`) | Summary of verified evidence |
|-----|----------------------|------------------------------|
| C1  | `docs/brds/agentic-retrofit-programme-brd.md:274` | `RULE-009`..`RULE-012` and `AC-035` (`:556`) require that no automated path submits a bid, approves match funding, certifies a claim, or records cash. |
| C2  | `src/core/src/zava_forward/core/finance.py:139` | `FinanceMixin.finance_action` (`:139`), `_finance_operation` (`:155`), `_fin_budget_approve` (`:224`), `_fin_commit_approve` (`:260`), `_fin_disposition` (`:296`), `_fin_payment_status` (`:309`), and `FINANCE_ACTIONS` (`:357`) implement record-only budget, commitment, invoice disposition, and external payment-status controls. |
| C3  | `src/core/src/zava_forward/core/grants.py:21` | `AuthorityGateError(PermissionError)` (`:25`), `require_authority` (`:31`), `GRANT_FLOW` (`:15`), and `GrantMixin.grant_action` (`:114`) govern `Opportunity`, `Award`, `Claimable`, `Submitted`, `Accepted`, `Cash received`, and `grant_eligibility`. |
| C4  | `src/core/src/zava_forward/core/forms.py:25` | `HUMAN_ONLY = ("declaration", "signature", "attestation", "consent", "approval")` prevents candidate auto-staging of human-only sign-off fields. |
| C5  | `src/core/src/zava_forward/core/form_review.py:478` | `form_review.action` permits only `("open", "review", "diagnose")` under `controlled(store, user, case_id)` and holds approvals/submissions via `HOLD_DEFINITIONS`. |
| C6  | `src/core/src/zava_forward/core/form_export.py:25` | `draft_export` emits `status="Held"`, `reviewed=False`, `submission="Not submitted"` draft packs only. |
| C7  | `src/core/src/zava_forward/core/store.py:2063` | `Store.funding_draft` (`:2063`) generates unapproved AI/template draft proposals (`approval="Not reviewed"`), while `Store.funding_step` (`:2125`) enters `_finance_operation` and `require_authority` for `approve`, `submit`, and `confirm`. |
| C8  | `src/api/src/zava_forward/api/server.py:1856` | `POST /api/cases/{cid}/{act}` routes `finance`, `grant`, `funding`, and `funding-draft`, mapping `PermissionError` to `403` and `ValueError` to `400` (`:1875-1879`). |
| C9  | `src/core/src/zava_forward/core/change_provenance.py:16` | `_actor(store, user)` assumes `user` is a `dict` (`user.get("email")`) and checks active named staff membership without structured automated-actor classification. |
| C10 | `src/core/src/zava_forward/core/bounded_ai.py:29` | `EXPECTED_CAPABILITIES` (`funding-evidence`, `funding_draft`, etc.) and `enforce_proposal_only` (`:93`) reject `approved=True`, controlled statuses, and forbidden execution keys. |
| C11 | `src/core/src/zava_forward/core/assistants.py:3334` | `Assistants.review` (`:3334`) and `_worker` (`:3464`) update only `assistant_tasks` proposal state and never invoke `finance_action`, `grant_action`, or `funding_step`. |
| C12 | `src/core/src/zava_forward/core/ai_tasks.py:496` | `ai_tasks.review` records `effect="Not an instruction; records the review only; any task or draft is created separately by the person"` (`:549`). |
| C13 | `src/agents/src/zava_forward/agents/dispatch.py:1` | Agent worker/dispatch modules execute bounded assistant tasks only and import no finance/grant/funding mutation entrypoints. |
| C14 | `src/orchestrator/src/zava_forward/orchestrator/__main__.py:1` | Orchestrator CLI exposes only `document-rescan` and `ranking-publish` (`source_monitor.py` and `rebuild.py` are standalone bounded offline/rehearsal scripts). |
| C15 | `src/orchestrator/src/zava_forward/orchestrator/rebuild.py:100` | Mentions of `budgets` and `grants` in `rebuild.py` / `rebuild_azure.py` refer solely to Azure `Microsoft.Consumption/budgets` and Entra RBAC roster checks, never case finance or grant claims. |
| C16 | `src/core/tests/test_funding_automation_boundary.py:1` | Tests `#93` draft separation (`funding_draft` does not advance funding/grants/finance), `require_authority` exercise gates, and separate ledger surfaces. |
| C17 | `src/core/tests/test_grant_lifecycle_controls.py:141` | Asserts `PermissionError` for unregistered human-shaped staff (`FAKE`), forged `oid`/`name`, un-designated `self.plain`, same-OID alias, and stored `financial_authority` with `human=False` (`:165`). |
| C18 | `src/core/tests/test_finance_match_controls.py:85` | Asserts `PermissionError` for non-independent human approvers (`self.a`, `self.alias`, `self.same_code`) and unknown legacy preparer on `finance_action`. |
| C19 | `src/core/pyproject.toml:25` | Configures `ruff` (`line-length = 100`, `select = ["E", "F", "I", "B", "UP"]`) and `mypy` (`strict = true` for new test files). |
| C20 | `src/core/README.md:1` | Documents `zava-forward-core` controls, bounded-AI `#104` invariants, and exact `unittest`, `ruff`, and `mypy` commands. |

## Synthesis and Convergence Recommendation

### Synthesized Answers to Research Questions

* **Q1 (Protected operations & actual modules)**: `funding_packs.py` and `routers/finance_grants.py` do not exist; the four `#93` / `RULE-010` operations map to `Store.funding_step` (`approve`, `submit`, `confirm` in `store.py`), `FinanceMixin.finance_action` (`budget_approve`, `commit_approve`, `disposition`, `payment_status` in `finance.py`), `GrantMixin.grant_action` (`grant_open`, `grant_propose`, `grant_approve`, `grant_eligibility` across `Opportunity`, `Award`, `Claimable`, `Submitted`, `Accepted`, `Cash received` in `grants.py`), `form_review.action` / `form_export.draft_export`, and `POST /api/cases/{cid}/{finance|grant|funding|funding-draft}` in `api/server.py` (`C2`-`C8`).
* **Q2 (Caller representation)**: Legitimate callers are authenticated registered named human staff dictionaries (`email`, `code`, `name`, `role` in `STAFF_ROLES`, optional `oid`, and human `financial_authority` designation where required) (`C3`, `C9`). Automated/non-human callers appear as `None`, non-dict values, blank/unauthenticated dicts, dicts with `human=False` / `automated=True` / automated `actor_type` (`agent`, `system`, `worker`, `orchestrator`, `service`, `bot`, `ai`, `assistant`, `service_principal`, `managed_identity`) / automated role-email-code prefixes, or stored non-human `financial_authority`.
* **Q3 (Agent, proposal-apply, and orchestrator isolation)**: `funding_draft` and `funding-evidence` are strictly `propose-only`; accepting a proposal in `ai_tasks.review` or `Assistants.review` writes review metadata only (`C10`-`C12`). Neither `src/agents` nor `src/orchestrator` calls `finance_action`, `grant_action`, or `funding_step` (`C13`-`C15`).
* **Q4 (Contrarian gaps to close)**: Adding a deterministic pre-execution guard in `finance.py` (`guard_no_automated_finance_authority`) invoked at `_finance_operation`, `finance_action`, `grant_action`, `funding_step`, and `form_review.action` closes `None`/non-dict `AttributeError`s, blank/unauthenticated dicts, automated/system/agent/worker/orchestrator actor dicts, stored non-human `financial_authority` on finance approvals/cash statuses, AI proposal-apply payload injection (`proposal_id`, `recommendation_id`, `assistant_task_id`, `ai_proposal`, `apply_proposal`, `from_proposal`, `auto_apply`, `envelope`), and canonical automated action names (`submit_bid`, `approve_match_funding`, `certify_claim`, `record_cash`), raising `AutomatedFinanceAuthorityRefusedError(ValueError)`.
* **Q5 (Compatibility & documentation)**: Preserving `PermissionError` / `AuthorityGateError` for human-shaped unregistered/un-designated/non-independent staff keeps all `#94`/`#95` core and API tests passing while `AutomatedFinanceAuthorityRefusedError(ValueError)` deterministically rejects automated/non-human/proposal-apply paths (and maps cleanly to HTTP `400` in `api/server.py`) (`C8`, `C16`-`C18`).

### Alternatives Considered

| Option | Summary | Disposition | Rationale |
|--------|---------|-------------|-----------|
| Option A: Selected | Add `AutomatedFinanceAuthorityRefusedError(ValueError)`, `guard_no_automated_finance_authority`, and `verify_no_automated_finance_authority` in `finance.py`; wire guard into `_finance_operation`, `finance_action`, `grant_action`, `funding_step`, and `form_review.action`; add `test_finance_no_automated_path_93.py` and `src/core/README.md` documentation. | Accepted | Covers every entry point (JSON `Store`, `SqlStore`, proposal-apply injection, agent/orchestrator actors, form review, and HTTP API) through the shared core boundary without breaking `#94`/`#95` `PermissionError` contracts. |
| Option B | Inherit `AutomatedFinanceAuthorityRefusedError` only from `PermissionError` instead of `ValueError`. | Rejected | Conflicts with the explicit prompt contract (`AutomatedFinanceAuthorityRefusedError` / `ValueError`) and core invariant convention (`FinanceGateError(ValueError)`). |
| Option C | Guard only inside HTTP `api/server.py` or create a new `routers/finance_grants.py` shim. | Rejected | Would leave direct core/worker/orchestrator Python call paths unguarded and introduce dead router duplication outside `server.py`. |

### Current & Unresolved Decisions, Risks, and Further Research

* **Confirmed design decisions**:
  1. Define `PROTECTED_FINANCE_OPERATIONS = ("submit_bid", "approve_match_funding", "certify_claim", "record_cash")` and `AutomatedFinanceAuthorityRefusedError(ValueError)` with structured attributes (`operation`, `actor_kind`, `reason`, `rule="RULE-010"`, `code="automated_finance_authority_refused"`) and `.as_record()` in `src/core/src/zava_forward/core/finance.py`.
  2. Enforce `guard_no_automated_finance_authority` across `finance.py` (`_finance_operation`, `finance_action`, plus stored `financial_authority.human is False` check on finance approvals/payment status), `grants.py` (`grant_action`), `store.py` (`funding_step`), and `form_review.py` (`action`).
  3. Implement `verify_no_automated_finance_authority(store=None)` in `finance.py` that deterministically verifies: (a) AI capability registry keeps funding capabilities (`funding-evidence`, `funding_draft`) `propose-only`, (b) `src/agents` and `src/orchestrator` expose no automated bid/match/claim/cash authority dispatchers, and (c) live probes across all four protected operations on an isolated disposable synthetic store (or supplied synthetic store copy without mutating caller state) reject automated, agent, worker, orchestrator, system, unauthenticated, non-human, and AI proposal-apply callers with `AutomatedFinanceAuthorityRefusedError` while leaving records and audit state unmutated by prohibited executions.
* **Unresolved decisions or blockers**: None.
* **Risks**: Over-broad actor classification could misclassify synthetic human test fixtures (`FAKE`, `PM-A`, `GEO-1`, `missing@example.test`) as automated rather than human `PermissionError`; mitigated by matching explicit non-human/unauthenticated/automated markers and automated principal tokens only.
* **Potential further research**: None needed for `#93` engineering criterion; Epic `#93` overall closure awaits stabilization checkpoint `#440` and child-issue review verification.

## Readiness and Handoff

* **Research execution status**: Complete (1 complete 3-wave cycle executed inline)
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Research-only constraint check**: Passed (no production, test, or README files modified during Research)
* **Artifact self-check**:
  * Brief, parameters, extension registry, participation, direction controls, questions, prior-knowledge gate recorded: Pass
  * Wider, Deeper, and Contrarian waves executed in order and logged: Pass
  * Every question (`Q1`-`Q5`) answered with `C1`-`C20` `path:line` evidence: Pass
  * Convergence recommendation and rejected alternatives documented: Pass
  * Continuation: Active confirmed automatic RPI Agent continues to `Plan` (`rpi-plan`).

