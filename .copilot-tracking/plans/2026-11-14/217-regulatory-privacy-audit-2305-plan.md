<!-- markdownlint-disable-file -->
# RPI Plan: Issue #217 Regulatory Assistant Security, Privacy, and Audit Controls

## Task Metadata

* Task ID: 217-regulatory-privacy-audit-2305
* Task slug: 217-regulatory-privacy-audit-2305
* Planning status: implementation-ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md
* Plan critique: .copilot-tracking/critiques/2026-11-14/217-regulatory-privacy-audit-2305-critique.md

## Executive Summary

This plan delivers the four locally verifiable `src/core` engineering controls for Issue #217 ("Security, privacy and audit for the regulatory assistant") across `regulatory_privacy.py`, `regulatory_usage.py`, `regulatory_chat.py`, and `rule_engine.py`, backed by a dedicated strict-typed unit test suite (`test_regulatory_privacy_audit_217.py`) and updated `src/core/README.md` documentation. Specifically, it enforces question-scoped Foundry query minimisation and special-category purpose gates, canonical Entra three-role separation (`ZavaForward.RuleAuthor`, `ZavaForward.RuleOwner`, `ZavaForward.RegulatoryChat`) with alias-proof separation of duties, an append-only UK GDPR Articles 22A to 22C propose/flag and retained named-human decision guard on `LawStore`, and closed-schema chat and check metering and cost records governed by shared role-scoped access, retention, and metadata-only audit controls.

### User Decisions and Requirements Highlights

* Deliver the four locally verifiable Issue #217 objectives in `src/core` on branch `feat/ai-217-regulatory-privacy-audit-2305` (target `feat/demo-164-chat-grounding-provenance-0900`).
* Write all four `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`) dated `2026-11-14`, run only the targeted `mypy`, `ruff`, and `-p 'test_*217*.py'` command in `src/core`, and commit cleanly with the Copilot trailer without pushing.

### What You May Not Know

* Existing `test_regulatory_privacy.py` asserts exact `set(QUERY_FIELDS) == {"rule_lookup", "check_explain", "alert_triage"}`, so question-scoped narrowing (`build_foundry_query` and `RegulatoryChat.foundry_query`) layers cleanly atop `QUERY_FIELDS` without altering its key set.
* Human DPO review of the chat/memory DPIA (`dpo_reviewed=False`), the named Legal decision on UK GDPR Articles 22A to 22C (#224), and live Azure Entra role-assignment verification (#358) remain open human/hosted gates, so code and documentation preserve fail-closed `dpo_reviewed=False` and `cost="Unknown"` (OD-51) semantics and the commit uses `Refs #217`.

### Unresolved Decisions or Blockers

* None for local `src/core` implementation. Human DPO/Legal sign-off and live Entra/Foundry verification remain tracked outside this local engineering slice.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) for Issue #217 on branch `feat/ai-217-regulatory-privacy-audit-2305` in `/home/azureuser/source/ama-demo-wt/feat-217-regulatory-privacy-audit-2305` targeting `feat/demo-164-chat-grounding-provenance-0900` (caller prompt).
* Foundry queries exclude fields not needed for the question; special-category data follows existing purpose controls (caller prompt; Issue #217; ADR 0005; PRD FR-060, NFR-017; `docs/reference/research/chat-memory-dpia.md`).
* Authors, approvers, and chat users are separate Entra roles (caller prompt; Issue #217; BRD CON-008; `infra/entra/app-registration.json`; `src/api/src/zava_forward/api/auth.py`).
* UK GDPR Art 22A to 22C guard: system proposes and flags; consequential decisions require and retain a named human with recorded reasons (caller prompt; Issue #217; PRD AC-106; BRD CON-003; `docs/reference/regulatory/reviewed-updates/2026-11-01-adm-ai-act-applicability-review.md`).
* Tokenomics: Metering and cost records for chat and checks hold identifiers, counts, and versions only, with no raw case, chat, or retrieved source content, and follow the same role-scoped access, retention, and audit controls (caller prompt; Issue #217; PRD FR-061; BRD FR-052; `docs/reference/resources/ai-tokenomics.md` OD-51).
* Write all 4 `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`) dated `2026-11-14`, run ONLY `cd /home/azureuser/source/ama-demo-wt/feat-217-regulatory-privacy-audit-2305/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*217*.py' -v` (never untargeted `unittest discover -s tests`), and commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (caller prompt).

## Goals

* Enforce question-scoped Foundry query minimisation and existing repository special-category purpose controls (`projection.can_see_reason`, `data_protection.dispatch_hold`, `chat_privacy.redact`, `dpo_reviewed=False`) across standalone queries and `RegulatoryChat`.
* Establish canonical Entra three-role isolation (`rule_author`, `rule_owner`, `regulatory_chat`) and alias-proof separation of duties (`identity.verified`, `identity.distinct`) directly in `src/core`.
* Replace the stateless Art 22A-22C dictionary helper gap with an append-only `LawStore`-backed proposal-and-human-decision guard (`ConsequentialDecisionGuard`) that restricts the system to non-binding flagged proposals and retains named-human decisions with recorded non-memory reasons.
* Provide closed-schema metering and cost records (`cost="Unknown"` when unpriced per OD-51) for both regulatory chat and rule-engine checks under shared role-scoped access, retention-window alignment, and metadata-only audit logging.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/regulatory_privacy.py`: scalar/cue-safe `minimise_query`, question-scoped `QUESTION_QUERY_FIELDS` + `build_foundry_query`, `check_special_category_purpose`, `retention_alignment`, canonical Entra 3-role mapping (`ENTRA_REGULATORY_ROLES`, `resolve_entra_regulatory_roles`, `require_regulatory_role`, `enforce_separation_of_duties`), hardened `record_human_decision` + append-only `ConsequentialDecisionGuard` with `(proposal_id, proposal_version)` uniqueness, preserved `<= 64` `_ID_CHARS` `metering_record`, and closed-schema `COST_FIELDS` + `cost_record`.
* `src/core/src/zava_forward/core/regulatory_usage.py`: check metering projection (`check_usage_metering` over `reg_check.body["usage"]`), chat and check cost record builders (`chat_cost_record`, `check_cost_record`), `summarize_checks`, and unified role-scoped (`audience`/`decision_owner` for checks; caller-owned `chat.regulatory.turn` audit rows for chat), retention-enforced, audited `governed_metering_and_cost`.
* `src/core/src/zava_forward/core/regulatory_chat.py`: `trusted-proxy` (`auth_provider` or `auth_mode`) + Entra `identity.verified` + `"regulatory_chat"` capability enforcement and Entra claim preservation inside `admit()`, and `admit`-gated `foundry_query(user, cid, question)` integration.
* `src/core/src/zava_forward/core/rule_engine.py`: `trusted-proxy` (`auth_provider` or `auth_mode`), Entra `identity.verified`, `"rule_owner"` Entra role verification, and `view_only` denial in `RuleEngine.disposition()`.
* `src/core/tests/test_regulatory_privacy_audit_217.py` and `src/core/README.md`: targeted strict-typed tests (with typed `Callable`/`Any` bindings for untyped sibling modules) matching `test_*217*.py` and concise documentation update.

### Non-Goals

* Modifying `QUERY_FIELDS` keys or breaking existing `src/core` / `src/api` callers.
* Altering seed card `automated-decision-safeguard` provision text before human DPO review (#211, #224), marking `dpo_reviewed=True`, making live Azure/Entra/Foundry calls, running untargeted test discovery, or pushing to remote.

## Functional Requirements

* FR-1: Question-scoped Foundry query minimisation and special-category purpose controls.
  * Observable acceptance criteria: `minimise_query` and `build_foundry_query` reject malformed/nested/overlong values, redact or refuse free-text special-category cues (`chat_privacy.SENSITIVE`), exclude fields not needed for the specific question (provision lookup vs hazard vs automated-decision home question), enforce `projection.can_see_reason` and `data_protection.dispatch_hold` for special-category purposes while refusing external Foundry transmission of `SPECIAL_CATEGORY` fields while `dpo_reviewed=False`, and `RegulatoryChat.foundry_query` never includes `PRIVATE-HEALTH-CANARY`, `PRIVATE-REPORT-CANARY`, resident PII, or unneeded case fields.
* FR-2: Separate Entra roles for authors, approvers, and chat users in `src/core`.
  * Observable acceptance criteria: `resolve_entra_regulatory_roles` maps only `ZavaForward.RuleAuthor -> rule_author`, `ZavaForward.RuleOwner -> rule_owner`, and `ZavaForward.RegulatoryChat -> regulatory_chat` (ignoring `ApplicationAdmin`, `AIRestart`, and business roles); `require_regulatory_role` enforces strict mutual non-implication across authoring, approval, and chat, rejects unverified/password principals for Entra-gated checks and `view_only` administrators, `enforce_separation_of_duties` blocks self-approval across `oid`/`tid` aliases (`identity.distinct`), and `RegulatoryChat.admit()` plus `RuleEngine.disposition()` enforce verified Entra capabilities on `trusted-proxy` callers.
* FR-3: UK GDPR Articles 22A to 22C propose/flag and retained named-human decision guard.
  * Observable acceptance criteria: `ConsequentialDecisionGuard.propose` emits only non-binding flagged proposals (`status="proposed"`, `decided_by_system=False`, `requires_named_human=True`, `"uk-gdpr-art-22a-human-required"` flag) and rejects system-decided statuses; `authorize_consequential_action` fails closed until `decide` records and retains an append-only row in `LawStore` (`reg_consequential_decision`, protected by SQLite/MSSQL update/delete abort triggers) with a named human approver (`rule_owner`), distinct identity from any human proposer, non-empty non-memory reasons (`controls.is_memory_reference` rejected), and metadata-only audit logging.
* FR-4: Closed-schema chat and check metering and cost records under shared access, retention, and audit controls.
  * Observable acceptance criteria: `metering_record` and `cost_record` accept identifiers, counts, and versions only (rejecting raw case/chat/source keys and prose/multiline smuggling inside string fields, with `cost="Unknown"` and `cost_minor_units=None` when `price_version == "unpriced"` per OD-51); `regulatory_usage` projects both `chat` turns and `reg_check` rows into metering and cost records; and `governed_metering_and_cost` enforces role-scoped access (caller-owned chat isolation + staff/Entra capability gates), retention-window filtering (`retention_alignment` with `dpo_reviewed=False`), and metadata-only `store.audit` events on both permitted and denied reads.

## Non-Functional Requirements

* NFR-1: Strict static typing, style compliance, and deterministic targeted execution in `src/core`.
  * Objective threshold or evaluation condition: Zero `mypy` errors (`strict = true`), zero `ruff check .` diagnostics, zero `ruff format --check .` diffs, and 100% pass rate on `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*217*.py' -v` with zero network calls and without editing `pyproject.toml` ignore lists.
  * Operating condition or verification approach, if needed: Run exact caller validation command in `src/core` and verify clean git status after commit.
  * Observable acceptance criteria: Targeted validation command exits 0 and `git status --short` is empty after commit.

## Acceptance Criteria

* Foundry queries built via `minimise_query`, `build_foundry_query`, and `RegulatoryChat.foundry_query` exclude fields not needed for the question and enforce existing repository purpose controls on special-category fields and cues.
* Authors (`ZavaForward.RuleAuthor` / `rule_author`), approvers (`ZavaForward.RuleOwner` / `rule_owner`), and chat users (`ZavaForward.RegulatoryChat` / `regulatory_chat`) are enforced as separate, mutually non-implying Entra capabilities across `regulatory_privacy`, `RegulatoryChat.admit`, `RuleEngine.disposition`, and separation-of-duties checks.
* `ConsequentialDecisionGuard` limits system output to non-binding flagged proposals, blocks consequential execution without an approved human decision, and durably retains named-human decisions with recorded non-memory reasons in append-only storage with metadata-only audit entries.
* Metering and cost records for both `chat` and `check` surfaces contain only identifiers, counts, and versions (`cost="Unknown"` when unpriced), strip/refuse raw case, chat, and source content, and enforce the same role-scoped access, retention-window filtering, and audit logging.
* Targeted `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*217*.py' -v` succeed in `src/core`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/217-regulatory-privacy-audit-2305-plan.md                                                             |
| Phase details                    | .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md                                                  |
| Latest critique                  | .copilot-tracking/critiques/2026-11-14/217-regulatory-privacy-audit-2305-critique.md (`Revise` resolved directly via PC-001..PC-005)     |
| Relevant research                | .copilot-tracking/research/2026-11-14/217-regulatory-privacy-audit-2305-research.md                                                      |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/217-regulatory-privacy-audit-2305-changes.md is created by implementation as its evidence record    |
| Planning execution and readiness | Complete; implementation-ready after applying single-pass critique findings PC-001..PC-005                                               |
| Continuation context             | Confirmed automatic RPI Agent transitions directly to `rpi-implement`                                                                    |

## Sources

* .copilot-tracking/research/2026-11-14/217-regulatory-privacy-audit-2305-research.md: Primary codebase synthesis (`C1`-`C12`).
* src/core/src/zava_forward/core/regulatory_privacy.py and src/core/src/zava_forward/core/regulatory_usage.py: Primary `src/core` modules under extension.
* src/core/src/zava_forward/core/regulatory_chat.py and src/core/src/zava_forward/core/rule_engine.py: Chat admission, Foundry query seam, check usage source, and alert disposition seam.
* infra/entra/app-registration.json and src/api/src/zava_forward/api/auth.py: Canonical Entra `capabilityRoles` definitions.
* docs/adrs/0005-regulatory-compliance-assistant.md, docs/reference/research/chat-memory-dpia.md, docs/reference/resources/ai-tokenomics.md, and docs/reference/regulatory/reviewed-updates/2026-11-01-adm-ai-act-applicability-review.md: Governing privacy, UK GDPR Art 22A-22C, and OD-51 tokenomics constraints.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Foundry query minimisation, Entra three-role separation, and UK GDPR Art 22A-22C guard

* Intent: Deliver deterministic `src/core` enforcement for Objectives 1, 2, and 3 across `regulatory_privacy.py`, `regulatory_chat.py`, and `rule_engine.py`.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement question-scoped Foundry query minimisation and special-category purpose controls

* Requirement and evidence: FR-1, NFR-1; Research `C1`, `C3`, `C7`, `C12`.
* Expected result: `minimise_query` enforces scalar/length/cue safety while preserving `QUERY_FIELDS`; `check_special_category_purpose` and `build_foundry_query` exclude fields not needed for the question and enforce `projection.can_see_reason` + `data_protection.dispatch_hold` + external special-category refusal while `dpo_reviewed=False`; `RegulatoryChat.foundry_query(user, cid, question)` produces canary-free question-scoped payloads with metadata-only audit logging.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Implement Entra three-role separation and separation-of-duties guards in `src/core`

* Requirement and evidence: FR-2, NFR-1; Research `C3`, `C4`, `C5`, `C6`, `C8`, `C10`.
* Expected result: `regulatory_privacy.py` defines `ENTRA_REGULATORY_ROLES`, `resolve_entra_regulatory_roles`, `require_regulatory_role`, and `enforce_separation_of_duties`; `RegulatoryChat.admit()` requires `"regulatory_chat"` for `trusted-proxy` principals; `RuleEngine.disposition()` enforces `identity.verified` and `not view_only` for `trusted-proxy` principals.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Implement append-only UK GDPR Art 22A-22C propose/flag and retained human-decision guard

* Requirement and evidence: FR-3, NFR-1; Research `C1`, `C4`, `C6`, `C9`, `C12`.
* Expected result: `record_human_decision` rejects bot/placeholder deciders and chat-memory citations while supporting `"approver"` and `"rule_owner"`; `ConsequentialDecisionGuard` persists append-only `reg_consequential_proposal` and `reg_consequential_decision` rows in `LawStore` with update/delete abort triggers, blocks system-decided actions, enforces separation of duties and recorded reasons, and writes metadata-only audit logs.
* Detail section: P01-T03 in .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Chat and check tokenomics metering and cost governance

* Intent: Deliver Objective 4 across `regulatory_privacy.py` and `regulatory_usage.py` so chat and check metering and cost records hold only identifiers, counts, and versions under shared role-scoped access, retention, and audit controls.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add closed-schema `cost_record`, `retention_alignment`, and `reg_check` usage/cost projection

* Requirement and evidence: FR-4, NFR-1; Research `C1`, `C2`, `C5`, `C7`; Critique `PC-001`.
* Expected result: `metering_record` preserves its `<= 64` `_ID_CHARS` closed schema intact; `COST_FIELDS` and `cost_record` validate identifier/count/version-only cost records (`cost="Unknown"` and `cost_minor_units=None` when `price_version == "unpriced"`); `retention_alignment` validates synthetic `SYNTH-` retention windows with `dpo_reviewed=False`; `regulatory_usage.py` adds `check_usage_metering`, `chat_cost_record`, `check_cost_record`, and `summarize_checks` over `reg_check.body["usage"]` without touching raw case, chat, or source text.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Implement role-scoped, retention-aligned, audited `governed_metering_and_cost` reader

* Requirement and evidence: FR-4, NFR-1; Research `C2`, `C3`, `C5`, `C6`, `C12`; Critique `PC-001`.
* Expected result: `governed_metering_and_cost` reads `chat.regulatory.turn` audit entries (caller-owned `who == user_key(user)` and matching `role`) and `reg_check` rows (scoped to `user["role"] in check["audience"] or user["email"] == check["decision_owner"]`), enforces staff/Entra capability gates, applies `retention_alignment` cutoff filtering (`dpo_reviewed=False`), and emits metadata-only `store.audit` records on permitted and denied access.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Targeted `test_*217*.py` test suite, component documentation, and verification

* Intent: Prove all four Issue #217 acceptance criteria under strict typing and targeted unit discovery, and document the delivered controls accurately in `src/core/README.md`.
* Dependencies: P01, P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Create `src/core/tests/test_regulatory_privacy_audit_217.py` and update `src/core/README.md`

* Requirement and evidence: FR-1..FR-4, NFR-1; Research `C7`, `C11`, `C12`.
* Expected result: Canonical new test file `src/core/tests/test_regulatory_privacy_audit_217.py` (0 test removals, <= 16 focused semantic and regression test methods) covers all four Issue #217 acceptance criteria and negative/edge cases; `src/core/README.md` documents the new controls while keeping `dpo_reviewed=False` and live/human gates explicit.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Execute targeted `mypy`, `ruff`, and `test_*217*.py` validation in `src/core`

* Requirement and evidence: NFR-1; caller prompt; Research `C11`.
* Expected result: Exact command `cd /home/azureuser/source/ama-demo-wt/feat-217-regulatory-privacy-audit-2305/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*217*.py' -v` exits 0 cleanly.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md

## Dependencies

* `src/core` editable Python environment with `mypy` (`strict = true`), `ruff`, and `sqlite3`: present in worktree.
* Existing `LawStore`, `Store`/`SqlStore`, `ChatIsolation`, `identity`, `data_protection`, `projection`, `chat_privacy`, and `controls` contracts in `src/core`: read and verified in Research (`C1`-`C12`).

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique (`Revise`) — PC-001 [High] | Applied directly | Kept `metering_record` (`METERING_FIELDS`, `_ID_CHARS`, `1 <= len <= 64`) unchanged; defined `retention_alignment` in `regulatory_privacy.py`; switched check metering/cost reads to `reg_check.body["usage"]` (formatting `card_version` as `f"{card_id}:v{card_version}"` within `_ID_CHARS`) scoped by `audience`/`decision_owner`, and chat reads to `audit` `chat.regulatory.turn` rows scoped by `user_key(user)` and `role`. |
| Single-pass critique (`Revise`) — PC-002 [High] | Applied directly | Updated P01-T02 so `RegulatoryChat.admit()` and `RuleEngine.disposition()` recognize `auth_provider == "trusted-proxy"` and `auth_mode == "trusted-proxy"`, reject `view_only`, verify Entra principals via `identity.verified`, derive Entra capabilities from `app_roles`/`entra_roles` (preventing forged `rule_roles`), and preserve Entra claims across both SQL and JSON branches. |
| Single-pass critique (`Revise`) — PC-003 [Medium] | Applied directly | Defined `QUESTION_QUERY_FIELDS` in P01-T01 for question-topic subsets (`provision_lookup`, `hazard-awareness-clock`, `automated-decision-safeguard`) disjoint from `SPECIAL_CATEGORY`/`SPECIAL_CATEGORY_FIELDS` while keeping `minimise_query` over `QUERY_FIELDS` intact, and required `RegulatoryChat.foundry_query` to run `self.admit(user)` and question redaction/refusal before `self.store.detail`. |
| Single-pass critique (`Revise`) — PC-004 [Medium] | Applied directly | Specified `with self.law.rules.transaction():` wrapping across `sqlite` and `mssql` DDL/mutations in `ConsequentialDecisionGuard` and a `PRIMARY KEY (proposal_id, proposal_version)` uniqueness/conflict check on `reg_consequential_decision` so recorded decisions cannot be overwritten via duplicate `INSERT`. |
| Single-pass critique (`Revise`) — PC-005 [Medium] | Applied directly | Added explicit `typing.cast(Callable[...], ...)` / `Any` adapter bindings for untyped sibling callables (`projection`, `chat_privacy`, `controls`, `chatthreads`) and test fixture helpers so `mypy --strict` passes without modifying `pyproject.toml`, and included legacy compatibility checks inside `test_regulatory_privacy_audit_217.py` (`<= 16` methods). |

## Follow-Up Items

* Human DPO review and sign-off of `docs/reference/research/chat-memory-dpia.md` and Legal applicability decision on UK GDPR Articles 22A to 22C (#217, #224): outside local `src/core` scope; owned by named DPO/Legal owner.
* Live Azure Entra role-assignment and Foundry runtime verification (#217, #358): outside offline `src/core` unit scope; owned by project owner during live tenant preflight.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/217-regulatory-privacy-audit-2305-changes.md
* Ready phase or task: `P01-T01` (plan finalized as `implementation-ready`)
* Remaining provisional question or blocker: none
