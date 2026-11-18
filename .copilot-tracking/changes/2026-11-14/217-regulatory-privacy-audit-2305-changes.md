<!-- markdownlint-disable-file -->
# RPI Changes: Issue #217 Regulatory Assistant Security, Privacy, and Audit Controls

## Metadata

* Task ID: 217-regulatory-privacy-audit-2305
* Related plan: .copilot-tracking/plans/2026-11-14/217-regulatory-privacy-audit-2305-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`–`P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P01-T03`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`
* All remaining active-plan markers: none
* Status basis: All planned tasks `P01`–`P03` completed in `src/core` and verified with targeted `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*217*.py' -v` exiting 0.

## Execution Summary

Delivered all four locally verifiable Issue #217 engineering acceptance criteria in `src/core`: question-scoped Foundry query minimisation and special-category purpose controls (`regulatory_privacy.py`, `regulatory_chat.py`), separate mutually non-implying Entra capabilities for authors, approvers, and chat users plus separation of duties (`regulatory_privacy.py`, `regulatory_chat.py`, `rule_engine.py`), append-only UK GDPR Articles 22A-22C propose/flag and retained named-human decision guard (`ConsequentialDecisionGuard`), and closed-schema identifier/count/version-only chat and check metering and cost records under shared role-scoped access, retention, and audit controls (`regulatory_privacy.py`, `regulatory_usage.py`), backed by 14 strict-typed unit tests in `src/core/tests/test_regulatory_privacy_audit_217.py` and updated `src/core/README.md`.

## Completed Work

### Foundry Query Minimisation, Entra Role Separation, and UK GDPR Art 22A-22C Guard (`P01`, `P01-T01`, `P01-T02`, `P01-T03`)

* Updated `src/core/src/zava_forward/core/regulatory_privacy.py` with question-scoped `QUESTION_QUERY_FIELDS`, `SPECIAL_CATEGORY_FIELDS`, `check_special_category_purpose`, `build_foundry_query`, scalar/cue-safe `minimise_query`, Entra three-role separation (`ENTRA_REGULATORY_ROLES`, `resolve_entra_regulatory_roles`, `require_regulatory_role`, `enforce_separation_of_duties`), hardened `record_human_decision`, and append-only `LawStore`-backed `ConsequentialDecisionGuard`.
* Updated `src/core/src/zava_forward/core/regulatory_chat.py` so `admit()` verifies Entra principals, rejects `view_only`, enforces `ZavaForward.RegulatoryChat` (`regulatory_chat`) on `trusted-proxy` callers without erasing Entra claims, and added `foundry_query(user, cid, question)` with metadata-only `chat.regulatory.foundry_query` audit logging.
* Updated `src/core/src/zava_forward/core/rule_engine.py` so `disposition()` enforces `require_regulatory_role(user, "alert_disposition", require_entra=False)`.

### Chat and Check Tokenomics Metering and Cost Governance (`P02`, `P02-T01`, `P02-T02`)

* Added `COST_FIELDS`, `cost_record`, and `retention_alignment` in `src/core/src/zava_forward/core/regulatory_privacy.py` while keeping `METERING_FIELDS` and `metering_record` (`<= 64` `_ID_CHARS`) intact.
* Updated `src/core/src/zava_forward/core/regulatory_usage.py` with `check_usage_metering`, `chat_cost_record`, `check_cost_record`, `summarize_checks`, and role-scoped, retention-aligned, audited `governed_metering_and_cost`.

### Targeted Test Suite, Documentation, and Verification (`P03`, `P03-T01`, `P03-T02`)

* Created `src/core/tests/test_regulatory_privacy_audit_217.py` (14 strict-typed test methods, within the `<= 16` locked plan cap, 0 removals) proving question-scoped Foundry query minimisation, special-category purpose controls and canary exclusion, three-role Entra separation and forged-claim rejection, separation of duties across same-OID dual-role principals, UK GDPR Art 22A-22C non-binding propose/flag enforcement, named-human decision retention with SQLite `BEFORE UPDATE`/`BEFORE DELETE` abort triggers and metadata-only audit logging, closed-schema chat and check metering/cost records (`cost="Unknown"` when unpriced), role-scoped/retention-filtered/audited `governed_metering_and_cost`, and backward-compatibility invariants.
* Updated `src/core/README.md` to document the delivered #217 controls and targeted test command while keeping `dpo_reviewed=False` and open Legal/DPO/live-tenant gates explicit.
* Verified `python3 -m mypy` (0 issues across 328 source files), `python3 -m ruff check .` (`All checks passed!`), `python3 -m ruff format --check .` (`275 files already formatted`), and `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*217*.py' -v` (`Ran 14 tests ... OK`).

## Implementation-Time Plan and Detail Updates

* Classification: Immediately relevant current-state update (`P02-T01`). Formatted `check_usage_metering`'s `rule_card_version` identifier as `f"{card_id}:v{card_version}"` instead of `f"{card_id}@v{card_version}"` so it conforms directly to `regulatory_privacy._ID_CHARS` (`:` is permitted while `@` is excluded) without relaxing `metering_record`'s existing closed identifier charset. Synchronized in `plan.md` and `phase-details.md`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy` | `src/core` | Passed | `Success: no issues found in 328 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` | Passed | `275 files already formatted` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*217*.py' -v` | `src/core/tests/test_regulatory_privacy_audit_217.py` | Passed | `Ran 14 tests in 8.609s — OK` |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`–`P03` and `P01-T01`–`P03-T02` all checked; `f"{card_id}:v{card_version}"` reflected in `plan.md` and `phase-details.md`)
* Completed-work evidence and handoff prose: reconciled
* Validation, blockers, remaining work, and follow-up items: reconciled (`0` blockers, `0` remaining active tasks)
* Review readiness: ready

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/217-regulatory-privacy-audit-2305-plan.md, `## Follow-Up Items`
* Human DPO review and sign-off of `docs/reference/research/chat-memory-dpia.md` and Legal applicability decision on UK GDPR Articles 22A to 22C (#217, #224): outside local `src/core` scope; owned by named DPO/Legal owner.
* Live Azure Entra role-assignment and Foundry runtime verification (#217, #358): outside offline `src/core` unit scope; owned by project owner during live tenant preflight.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P01-T03`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`; remaining: none
* Validation coverage: targeted `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*217*.py' -v` all passed in `src/core`
* Blockers: none
* Current plan and detail updates: `rule_card_version` colon delimiter (`f"{card_id}:v{card_version}"`) synchronized across `plan.md` and `phase-details.md`
* Planning and critique state: implementation-ready (`PC-001`–`PC-005` satisfied)
* Follow-up items: DPO/Legal sign-off (#217, #224) and live Entra/Foundry verification (#217, #358)
* Review readiness or no-handoff reason: ready for single post-implementation `rpi-review`
* Continuation owner: parent confirmed automatic RPI Agent
