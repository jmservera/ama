<!-- markdownlint-disable-file -->
# Review: Issue #217 Regulatory Assistant Security, Privacy, and Audit Controls

## Scope and Evidence

* Task ID: 217-regulatory-privacy-audit-2305
* Review date: 2026-11-14
* Review scope: Full task (`P01` through `P03`, tasks `P01-T01` through `P03-T02`)
* Assessed boundary: Locally verifiable `src/core` engineering controls for Issue #217 (`regulatory_privacy.py`, `regulatory_chat.py`, `rule_engine.py`, `regulatory_usage.py`, `test_regulatory_privacy_audit_217.py`, and `src/core/README.md`) covering question-scoped Foundry query minimisation and special-category purpose gates, separate Entra roles for authors/approvers/chat users with alias-proof separation of duties, UK GDPR Articles 22A to 22C propose/flag and retained named-human decision guard, and closed-schema chat and check metering and cost governance.
* Plan: .copilot-tracking/plans/2026-11-14/217-regulatory-privacy-audit-2305-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md
* Plan critique: .copilot-tracking/critiques/2026-11-14/217-regulatory-privacy-audit-2305-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/217-regulatory-privacy-audit-2305-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/217-regulatory-privacy-audit-2305-research.md, `git diff` across `src/core`, and targeted `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*217*.py' -v` execution results.

## Opening Review State

* Interpreted review goal: Verify once with direct source, test, documentation, and artifact evidence whether the `src/core` implementation satisfies all four Issue #217 local engineering acceptance criteria, preserves critique dispositions `PC-001` through `PC-005` and repository governance boundaries (`dpo_reviewed=False`, OD-51 `cost="Unknown"`, zero `.copilot-tracking/` leaks in `src/`), and passes the declared targeted validation suite.
* Review scope: Full task (`P01` through `P03`)
* Evidence readiness: Ready; research, plan, phase details, single-pass critique, reconciled changes record, source/test/documentation diffs, and targeted validation outputs are complete and internally consistent.
* Acceptance basis: Caller prompt objectives and validation constraints, Plan `FR-1` through `FR-4` and `NFR-1`, single-pass critique dispositions `PC-001` through `PC-005`, and AMA repository conventions.
* First comparison boundary: Reconcile plan checklist markers (`P01` through `P03`), phase details, and changes record against the `src/core` Git diff before assessing implementation-time updates, critique coverage, validation, and follow-up routing.
* Active read-only boundaries: Create only `.copilot-tracking/reviews/2026-11-14/217-regulatory-privacy-audit-2305-review.md` during Review without mutating research, plan, phase details, critique, changes record, or `src/` files.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single post-implementation review on 2026-11-14 across the full declared `src/core` task boundary (`P01` through `P03`), comparing `.copilot-tracking/plans/2026-11-14/217-regulatory-privacy-audit-2305-plan.md`, `.copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md`, `.copilot-tracking/critiques/2026-11-14/217-regulatory-privacy-audit-2305-critique.md`, `.copilot-tracking/changes/2026-11-14/217-regulatory-privacy-audit-2305-changes.md`, `.copilot-tracking/research/2026-11-14/217-regulatory-privacy-audit-2305-research.md`, and the exact `src/core` diff.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`, `P01-T03`) | Foundry Query Minimisation, Entra Role Separation, and UK GDPR Art 22A-22C Guard | Reconciled | All three tasks checked `[x]` in `plan.md` with matching source evidence in `regulatory_privacy.py`, `regulatory_chat.py`, and `rule_engine.py`. |
| `P02` (`P02-T01`, `P02-T02`) | Chat and Check Tokenomics Metering and Cost Governance | Reconciled | Both tasks checked `[x]` in `plan.md` with matching source evidence in `regulatory_privacy.py` and `regulatory_usage.py`, including synchronized `f"{card_id}:v{card_version}"` identifier delimiter. |
| `P03` (`P03-T01`, `P03-T02`) | Targeted Test Suite, Documentation, and Verification | Reconciled | Both tasks checked `[x]` in `plan.md` with `test_regulatory_privacy_audit_217.py` (14 tests `<= 16` cap), updated `src/core/README.md`, and passing targeted validation checks. |
| `## Follow-Up Items` | Human DPO/Legal sign-off (#217, #224) and live Azure Entra/Foundry verification (#217, #358) | Reconciled | Kept outside active `Pxx`/`Pxx-Txx` scope and mirrored identically between `plan.md` and `changes.md`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/regulatory_privacy.py`, `src/core/src/zava_forward/core/regulatory_chat.py` | Hardened `minimise_query` for scalar/length/cue safety while keeping `QUERY_FIELDS` intact; added `QUESTION_QUERY_FIELDS`, `SPECIAL_CATEGORY_FIELDS`, `check_special_category_purpose`, `build_foundry_query`, and `RegulatoryChat.foundry_query` with admission, projection, canary exclusion, and metadata-only `chat.regulatory.foundry_query` audit logging. | Source diff + tests for provision-only vs hazard vs automated-decision narrowing, role-based `can_see_reason` and `dispatch_hold` gates, and canary exclusion. | Passed (`mypy`, `ruff`, `test_regulatory_privacy_audit_217.py`) | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/regulatory_privacy.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/src/zava_forward/core/rule_engine.py` | Added `ENTRA_REGULATORY_ROLES`, `resolve_entra_regulatory_roles`, `require_regulatory_role`, and `enforce_separation_of_duties`; hardened `RegulatoryChat.admit()` and `RuleEngine.disposition()` to reject `view_only`, verify Entra principals, prevent forged `rule_roles`, and enforce distinct capability roles. | Source diff + mutual non-implication matrix, forged-claim rejection, view-only denial, and same-OID dual-role separation-of-duties unit tests. | Passed (`mypy`, `ruff`, `test_regulatory_privacy_audit_217.py`) | Reconciled |
| `P01-T03` | `src/core/src/zava_forward/core/regulatory_privacy.py` | Hardened `record_human_decision` (rejecting bot/placeholder deciders and chat-memory citations, accepting `"approver"` and `"rule_owner"`) and added append-only `LawStore`-backed `ConsequentialDecisionGuard` (`reg_consequential_proposal`, `reg_consequential_decision`, SQLite/MSSQL abort triggers, fail-closed `authorize_consequential_action`, and metadata-only audit events). | Source diff + unit tests proving non-binding `proposed` output, rejection of system-decided statuses/bots/memory citations, separation of duties, SQLite `UPDATE`/`DELETE` trigger aborts, and metadata-only audit entries. | Passed (`mypy`, `ruff`, `test_regulatory_privacy_audit_217.py`) | Reconciled |
| `P02-T01` | `src/core/src/zava_forward/core/regulatory_privacy.py`, `src/core/src/zava_forward/core/regulatory_usage.py` | Added `retention_alignment` and closed-schema `COST_FIELDS`/`cost_record` (`cost="Unknown"` and `cost_minor_units=None` when unpriced per OD-51) while keeping `metering_record` unchanged; added `check_usage_metering`, `chat_cost_record`, `check_cost_record`, and `summarize_checks`. | Source diff + unit tests proving closed identifier/count/version schemas, smuggling rejection, `cost="Unknown"` unpriced invariant, and deterministic priced minor-unit calculation. | Passed (`mypy`, `ruff`, `test_regulatory_privacy_audit_217.py`) | Reconciled |
| `P02-T02` | `src/core/src/zava_forward/core/regulatory_usage.py` | Implemented `governed_metering_and_cost` across both SQLite and JSON stores with caller-owned chat isolation, `audience`/`decision_owner` check visibility, `retention_alignment` cutoff filtering (`dpo_reviewed=False`), and metadata-only `regulatory.metering.read`/`regulatory.metering.denied` audit events. | Source diff + unit tests proving role-scoped chat/check filtering, cross-user/unscoped exclusion, retention window filtering, and permitted/denied audit logging with zero raw case/chat/source leakage. | Passed (`mypy`, `ruff`, `test_regulatory_privacy_audit_217.py`) | Reconciled |
| `P03-T01`, `P03-T02` | `src/core/tests/test_regulatory_privacy_audit_217.py`, `src/core/README.md` | Added 14 strict-typed unit tests (`<= 16` cap, 0 removals) and updated `src/core/README.md` `#217` and `#208` subsections with accurate architectural status and targeted test command while keeping `dpo_reviewed=False` explicit and zero `.copilot-tracking/` references in `src/`. | `test_regulatory_privacy_audit_217.py`, `src/core/README.md` diff, grep check across `src/`, and clean targeted command run. | Passed (`mypy` across 328 files, `ruff check .`, `ruff format --check .`, 14/14 unit tests) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P02-T01` (`check_usage_metering`) | Changed `rule_card_version` format from `f"{card_id}@v{card_version}"` to `f"{card_id}:v{card_version}"` because `regulatory_privacy._ID_CHARS` permits `:` and excludes `@`, preserving `metering_record`'s existing closed identifier charset without relaxation. | Direct `regulatory_privacy._ID_CHARS` inspection during `P02-T01`; no user decision needed (ordinary local identifier delimiter alignment). | Updated `plan.md` (`Critique Disposition PC-001`), `phase-details.md` (`P02-T01`), and `changes.md` (`Implementation-Time Plan and Detail Updates`). | Not needed; preserves `PC-001` ("do not relax `metering_record`") more strictly. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five single-pass critique findings (`PC-001` through `PC-005` in `.copilot-tracking/critiques/2026-11-14/217-regulatory-privacy-audit-2305-critique.md`) were directly applied in the finalized plan and honored in implementation (`metering_record` preserved intact, `retention_alignment` implemented, `reg_check.body["usage"]` and `audit` `chat.regulatory.turn` used with proper scoping, `auth_mode`/`auth_provider` + `identity.verified` + claim preservation enforced in `RegulatoryChat.admit()` and `RuleEngine.disposition()`, `QUESTION_QUERY_FIELDS` layered cleanly atop `QUERY_FIELDS`, `with self.law.rules.transaction():` and `(proposal_id, proposal_version)` primary-key uniqueness enforced in `ConsequentialDecisionGuard`, and strict `mypy` passed across 328 files without modifying `pyproject.toml`).
* Material revisions: None occurred during implementation; only the non-material `:` delimiter alignment in `P02-T01` was recorded and synchronized.
* Dependent-work pause assessment: No dependent-work pause was triggered or bypassed.
* Justification assessment: Fully supported by repository code and test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Human DPO review and sign-off of `docs/reference/research/chat-memory-dpia.md` and Legal applicability decision on UK GDPR Articles 22A to 22C (#217, #224) | Requires named human DPO and Legal governance authority (`dpo_reviewed=False` must remain fail-closed until signed). | Named DPO and Legal counsel / project owner. | Open non-blocking governance gate; routed as distinct follow-up item (`Refs #217`). |
| Live Azure Entra role-assignment and Foundry runtime verification (#217, #358) | Requires live Azure tenant credentials and hosted Foundry runtime outside offline `src/core` unit scope. | Project owner during live tenant preflight. | Open non-blocking hosted verification gate; routed as distinct follow-up item (`Refs #217`). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Harden `ConsequentialDecisionGuard.history` reason visibility against un-normalized Entra `rule_roles`

* Related scope: `P01-T03`
* Evidence: `src/core/src/zava_forward/core/regulatory_privacy.py` (`ConsequentialDecisionGuard.history`) computes `show_reasons` using `resolve_entra_regulatory_roles(user) | set(user.get("rule_roles") or ())`. When callers pass a principal already normalized by `RegulatoryChat.admit()` or `require_regulatory_role()`, forged `rule_roles` are already stripped; however, a future direct caller passing an un-normalized Entra user dictionary with forged `rule_roles=["rule_owner"]` could unmask decision `reasons` for a staff role where `projection.can_see_reason(user)` is `False`.
* Impact: Non-blocking defense-in-depth hardening for future `src/api` endpoint wiring (`propose`, `decide`, `authorize_consequential_action`, `admit`, and `require_regulatory_role` already overwrite forged `rule_roles` from verified Entra claims).
* Destination: distinct follow-up (`src/api` integration / hardening slice)
* Smallest useful next action: When exposing `ConsequentialDecisionGuard.history` via `src/api` (or in a follow-up `src/core` hardening slice), derive `rule_owner` reason visibility solely from `resolve_entra_regulatory_roles(verified)` whenever Entra markers (`oid`, `tid`, `app_roles`, `entra_roles`, or `trusted-proxy`) are present.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` [Low] | distinct follow-up | Future `src/api` / `src/core` hardening slice: restrict `ConsequentialDecisionGuard.history` Entra reason-unmasking to verified `resolve_entra_regulatory_roles` claims when Entra markers are present. | Non-blocking defense-in-depth hardening outside current accepted `P01`–`P03` acceptance defects. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Wire `RegulatoryChat.foundry_query`, `ConsequentialDecisionGuard`, and `governed_metering_and_cost` into `src/api` HTTP endpoints while restricting `ConsequentialDecisionGuard.history` Entra reason visibility to verified Entra claims (`RV-001`).
* Complete human DPO review/sign-off of `docs/reference/research/chat-memory-dpia.md` and named Legal applicability sign-off on UK GDPR Articles 22A to 22C (#217, #224).
* Execute live Azure Entra three-role assignment and Foundry runtime verification (#217, #358).

## Blockers and Remaining Work

* Blockers: none for the declared `src/core` engineering scope.
* Remaining active work: none (`P01` through `P03` and `P01-T01` through `P03-T02` are complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy` | `src/core` (328 source files, `strict = true`) | Passed | `Success: no issues found in 328 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` | Passed | `275 files already formatted` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*217*.py' -v` | `src/core/tests/test_regulatory_privacy_audit_217.py` | Passed | `Ran 14 tests in 8.609s — OK` |
| Untargeted `unittest discover -s tests` | `src/core/tests` | Skipped | Explicitly prohibited by caller instructions (`NEVER run full unittest discover -s tests without -p`). |

## Outcome

* Outcome: Conformant
* Outcome rationale: All four Issue #217 locally verifiable `src/core` acceptance criteria (`FR-1` through `FR-4`), strict static typing and formatting (`NFR-1`), and single-pass critique dispositions (`PC-001` through `PC-005`) are implemented, reconciled across plan/details/changes artifacts, free of `.copilot-tracking/` leaks in `src/`, and verified by passing `mypy`, `ruff check .`, `ruff format --check .`, and 14 targeted `test_*217*.py` tests. Zero defects or open material findings remain; `RV-001` [Low] and external human/live gates are routed cleanly as distinct follow-up work (`Refs #217`).

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Harden `ConsequentialDecisionGuard.history` un-normalized Entra claim handling when wiring `src/api` (`RV-001`); complete human DPO/Legal sign-off (#217, #224) and live Entra/Foundry verification (#217, #358). |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Targeted `src/core` `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*217*.py' -v` (14 tests) all passed; untargeted discovery skipped per explicit caller rule.
