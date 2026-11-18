<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #217 Regulatory Assistant Security, Privacy, and Audit Controls

## Metadata

* Task ID: 217-regulatory-privacy-audit-2305
* Task slug: 217-regulatory-privacy-audit-2305
* Related plan: .copilot-tracking/plans/2026-11-14/217-regulatory-privacy-audit-2305-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/217-regulatory-privacy-audit-2305-research.md

## Phase Index

| Phase ID | Name                                                                                       | Status | Detail sections                   |
|----------|--------------------------------------------------------------------------------------------|--------|-----------------------------------|
| P01      | Foundry query minimisation, Entra three-role separation, and UK GDPR Art 22A-22C guard     | ready  | P01, P01-T01, P01-T02, P01-T03    |
| P02      | Chat and check tokenomics metering and cost governance                                     | ready  | P02, P02-T01, P02-T02             |
| P03      | Targeted `test_*217*.py` test suite, component documentation, and verification             | ready  | P03, P03-T01, P03-T02             |

<!-- rpi:phase id=P01 -->
## P01: Foundry query minimisation, Entra three-role separation, and UK GDPR Art 22A-22C guard

### Context

Research (`C1`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C12`) showed that `regulatory_privacy.py` currently holds only stateless dictionary builders (`minimise_query`, `record_human_decision`, `metering_record`), `src/core` lacks a canonical Entra three-role contract (`ZavaForward.RuleAuthor`, `ZavaForward.RuleOwner`, `ZavaForward.RegulatoryChat`), `RegulatoryChat.admit()` omits checking `"regulatory_chat"` for `trusted-proxy` principals, and `record_human_decision` is not wired to append-only `LawStore` persistence or proposal flagging.

### Intent

Enforce question-scoped Foundry query minimisation with existing repository special-category purpose gates, canonical Entra three-role isolation and separation of duties, and an append-only UK GDPR Articles 22A-22C propose/flag and retained human-decision guard in `src/core`.

### Boundaries

* Included: `regulatory_privacy.py`, `regulatory_chat.py`, and `rule_engine.py`.
* Excluded: Changing `QUERY_FIELDS` keys (`C7`), editing `rulecards.py` seed-card provision text before DPO approval, or modifying `pyproject.toml`.

### Likely Targets

* `src/core/src/zava_forward/core/regulatory_privacy.py`: Foundry query, Entra role, and Art 22A-22C contracts.
* `src/core/src/zava_forward/core/regulatory_chat.py`: `trusted-proxy` `regulatory_chat` admission check and `foundry_query` method.
* `src/core/src/zava_forward/core/rule_engine.py`: `trusted-proxy` `identity.verified` and `view_only` check in `disposition()`.

### Dependencies

* None.

### Validation Expectations

* `mypy` (`strict = true`) and `ruff` pass on all modified modules; semantic unit tests in P03 verify positive and fail-closed negative paths.

### Completion Evidence

* Updated `regulatory_privacy.py`, `regulatory_chat.py`, and `rule_engine.py` passing static checks and P03 unit tests.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement question-scoped Foundry query minimisation and special-category purpose controls

#### Context

`minimise_query` (`C1`) currently copies any value under `QUERY_FIELDS[purpose]` without checking scalar types, length bounds, free-text special-category cues (`chat_privacy.SENSITIVE`), question-specific necessity, or `projection` / `data_protection` purpose controls (`C12`), while `test_regulatory_privacy.py` (`C7`) pins `set(QUERY_FIELDS) == {"rule_lookup", "check_explain", "alert_triage"}`.

#### Intent

Exclude all fields not needed for the specific question from Foundry queries and enforce existing repository purpose controls on special-category fields and cues.

#### Boundaries

* Included: Scalar/bounds/cue hardening in `minimise_query` (keeping `QUERY_FIELDS` unchanged); `SPECIAL_CATEGORY_FIELDS` (extending outbound checks to `adjustment`, `medical`, `biometric`, `genetic`, `sexual_orientation`, `trade_union` while keeping `SPECIAL_CATEGORY` intact); explicit `QUESTION_QUERY_FIELDS` subsets (`provision_lookup`, `hazard-awareness-clock`, `automated-decision-safeguard`) disjoint from `SPECIAL_CATEGORY_FIELDS` so `build_foundry_query` keeps question-needed count fields (`hazard_count`, `active_hold_count` vs `automated_decision_count`) without changing `QUERY_FIELDS`; `check_special_category_purpose(user, purpose, *, env=None)`; typed `Callable`/`Any` adapters for `projection`, `chat_privacy`, and `controls` (`PC-005`); and `RegulatoryChat.foundry_query(user, cid, question)` running `user = self.admit(user)` plus question redaction/refusal before reading `self.store.detail(cid, user)` (`PC-003`).
* Excluded: Network calls to Azure AI Foundry or changing `QUERY_FIELDS` keys.

#### Likely Targets

* `src/core/src/zava_forward/core/regulatory_privacy.py`: `minimise_query`, `check_special_category_purpose`, `build_foundry_query`.
* `src/core/src/zava_forward/core/regulatory_chat.py`: `RegulatoryChat.foundry_query`.

#### Dependencies

* None.

#### Validation Expectations

* Provision-only questions exclude home/case counts; hazard home questions include only needed non-identifying hazard counts (`hazard_count`, `active_hold_count`) and exclude `automated_decision_count`, `resident`, `address`, `PRIVATE-HEALTH-CANARY`, and `PRIVATE-REPORT-CANARY`; automated-decision home questions include `automated_decision_count` and exclude hazard counts; special-category fields/cues are stripped/redacted and explicit external special-category transmission raises `PermissionError` while `dpo_reviewed=False` or when `projection.can_see_reason` / `data_protection.dispatch_hold` denies the caller.

#### Completion Evidence

* `minimise_query`, `check_special_category_purpose`, `build_foundry_query`, and `RegulatoryChat.foundry_query` implemented with full strict type annotations.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Implement Entra three-role separation and separation-of-duties guards in `src/core`

#### Context

`infra/entra/app-registration.json` and `src/api/src/zava_forward/api/auth.py` (`C8`) map `ZavaForward.RuleAuthor -> rule_author`, `ZavaForward.RuleOwner -> rule_owner`, and `ZavaForward.RegulatoryChat -> regulatory_chat`, whereas `src/core` lacked this canonical separation validator and `RegulatoryChat.admit()` (`C3`) plus `RuleEngine.disposition()` (`C5`) had incomplete `trusted-proxy` verification.

#### Intent

Enforce separate Entra roles for authors (`rule_author`), approvers (`rule_owner`), and chat users (`regulatory_chat`) with verified Entra claim checks and alias-proof separation of duties in `src/core`.

#### Boundaries

* Included: `ENTRA_REGULATORY_ROLES`, `ACTION_CAPABILITIES`, `resolve_entra_regulatory_roles` (reading Entra app roles from `app_roles` and `entra_roles`), `require_regulatory_role`, and `enforce_separation_of_duties` in `regulatory_privacy.py`; updating `RegulatoryChat.admit()` across both SQL and JSON branches (`PC-002`) to recognize `auth_provider == "trusted-proxy"` and `auth_mode == "trusted-proxy"`, reject `view_only`, verify Entra principals via `identity.verified`, derive authoritative capabilities from `app_roles`/`entra_roles` when present (blocking forged `rule_roles` while preserving non-Entra synthetic fixture `rule_roles`), require `"regulatory_chat"` on trusted-proxy principals, and preserve Entra claims (`oid`, `tid`, `identity_source`, `bound`, `derived_code`, `derived_email`, `app_roles`, `entra_roles`, `auth_mode`, `auth_provider`, `rule_roles`, `view_only`); and enforcing the matching `trusted-proxy` + `not view_only` + `identity.verified` + `"rule_owner"` check in `RuleEngine.disposition()`.
* Excluded: Modifying `src/api` routes or `infra/` scripts.

#### Likely Targets

* `src/core/src/zava_forward/core/regulatory_privacy.py`: Entra role constants and guard functions.
* `src/core/src/zava_forward/core/regulatory_chat.py`: `RegulatoryChat.admit()`.
* `src/core/src/zava_forward/core/rule_engine.py`: `RuleEngine.disposition()`.

#### Dependencies

* None.

#### Validation Expectations

* Each of `ZavaForward.RuleAuthor`, `ZavaForward.RuleOwner`, and `ZavaForward.RegulatoryChat` grants only its own capability and denies the other two; `ZavaForward.ApplicationAdmin`, `ZavaForward.AIRestart`, business roles, `view_only`, and unverified/password principals cannot satisfy Entra capability checks; `enforce_separation_of_duties` blocks the same Entra `oid`/`tid` even across different email aliases (`identity.distinct`).

#### Completion Evidence

* Entra role separation helpers and `RegulatoryChat.admit` / `RuleEngine.disposition` guards active and tested.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Implement append-only UK GDPR Art 22A-22C propose/flag and retained human-decision guard

#### Context

`src/core/README.md:4706` (`C1`) notes that `record_human_decision` is a pure builder not wired to storage or an approval flow. `LawStore` (`C9`) provides SQLite and MSSQL append-only table patterns with `BEFORE UPDATE` and `BEFORE DELETE` abort triggers.

#### Intent

Ensure the system only proposes and flags consequential actions while consequential execution requires and durably retains a named human approver with recorded non-memory reasons in append-only `LawStore` tables with metadata-only audit logging.

#### Boundaries

* Included: Hardening `record_human_decision` (rejecting bot/placeholder names and `controls.is_memory_reference` reasons, accepting `"approver"` and `"rule_owner"`, preserving existing return schema); adding `ConsequentialDecisionGuard(law, *, store=None, audit=None)` wrapping DDL and mutations in `with self.law.rules.transaction():` across both `sqlite` and `mssql` dialects (`PC-004`), enforcing `PRIMARY KEY (proposal_id, proposal_version)` uniqueness plus an explicit conflict check on `reg_consequential_decision` so a rejected/recorded decision cannot be overwritten via duplicate `INSERT`, plus append-only `BEFORE UPDATE`/`BEFORE DELETE` abort triggers (and MSSQL ledger/triggers), `propose()`, `decide()`, `authorize_consequential_action()`, and role-scoped `history()`.
* Excluded: Claiming a completed Legal applicability decision under #224.

#### Likely Targets

* `src/core/src/zava_forward/core/regulatory_privacy.py`: `record_human_decision` and `ConsequentialDecisionGuard`.

#### Dependencies

* P01-T02 (`require_regulatory_role` and `enforce_separation_of_duties`).

#### Validation Expectations

* System proposals carry `status="proposed"`, `effect="non_binding_proposal"`, `decided_by_system=False`, `requires_named_human=True`, and `"uk-gdpr-art-22a-human-required"`; `authorize_consequential_action` raises `PermissionError` before human approval or after rejection/deferral; `decide` rejects system/AI/placeholder names, `rule_author`/`regulatory_chat` roles, self-approval (`identity.distinct`), blank or chat-memory reasons, and persists rows whose SQL `UPDATE`/`DELETE` triggers abort.

#### Completion Evidence

* `ConsequentialDecisionGuard` and hardened `record_human_decision` implemented and verified against `LawStore` SQLite triggers.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Chat and check tokenomics metering and cost governance

### Context

`metering_record` (`C1`) lacks lexical prose-smuggling bounds and has no companion `cost_record`; `regulatory_usage.py` (`C2`) handles only `chat` turns, ignoring `reg_check` usage (`C5`), and lacks a unified role-scoped, retention-aligned, audited reader across chat and checks.

### Intent

Provide closed-schema identifier/count/version-only metering and cost records (`cost="Unknown"` when unpriced per OD-51) for both regulatory chat and rule-engine checks, governed by the same role-scoped access, retention-window filtering, and metadata-only audit controls.

### Boundaries

* Included: `regulatory_privacy.py` (`metering_record` lexical bounds, `COST_FIELDS`, `cost_record`) and `regulatory_usage.py` (`check_usage_metering`, `chat_cost_record`, `check_cost_record`, `summarize_checks`, `governed_metering_and_cost`).
* Excluded: Inventing live Azure token prices (OD-51 requires `"Unknown"` when unpriced).

### Likely Targets

* `src/core/src/zava_forward/core/regulatory_privacy.py`: `metering_record`, `COST_FIELDS`, `cost_record`.
* `src/core/src/zava_forward/core/regulatory_usage.py`: check metering/cost projections and `governed_metering_and_cost`.

### Dependencies

* P01 (`require_regulatory_role`, `retention_alignment`).

### Validation Expectations

* Both chat and check metering/cost records reject raw content keys and whitespace/multiline prose smuggling inside identifier/version fields, report `cost="Unknown"` when unpriced, enforce caller-owned chat isolation and staff/Entra role checks, filter expired records past `retention_days`, and emit metadata-only `store.audit` logs without reading chat message bodies or source quotes.

### Completion Evidence

* Updated `regulatory_privacy.py` and `regulatory_usage.py` passing `mypy`, `ruff`, and P03 tests.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add closed-schema `cost_record`, `retention_alignment`, and `reg_check` usage/cost projection

#### Context

`RuleEngine.run` (`C5`, `PC-001`) stores `offline_usage("regulatory-check", ...)` at `json.loads(body)["usage"]` in `reg_check` `(id, case_id, at, check_seq, body)`, and `RegulatoryChat.ask` (`C3`, `PC-001`) stores `offline_usage("regulatory-home-chat", ...)` inside `audit` (`action == "chat.regulatory.turn"`). `metering_record` already enforces `METERING_FIELDS`, `_ID_CHARS`, and `1 <= len <= 64`. Both surfaces need validated closed-schema metering and cost projections holding identifiers, counts, and versions only, plus `retention_alignment` in `regulatory_privacy.py`.

#### Intent

Preserve `metering_record` compatibility while adding `COST_FIELDS`, `cost_record`, `retention_alignment`, and `reg_check` metering/cost projections for both `chat` and `check` surfaces.

#### Boundaries

* Included: Preserving `metering_record` (`METERING_FIELDS`, `_ID_CHARS`, `1 <= len <= 64`) unchanged (`PC-001`); adding `COST_FIELDS` and `cost_record` in `regulatory_privacy.py` (`<= 64` `_ID_CHARS` IDs/versions, bounded non-negative int counts, `cost == "Unknown"` and `cost_minor_units is None` when `price_version == "unpriced"`); adding `retention_alignment(env, now, *, retention_days=None)` in `regulatory_privacy.py` preserving `SYNTH-` validation and `dpo_reviewed=False`; and adding `check_usage_metering` (formatting `rule_card_version=f"{card_id}:v{card_version}"` within `_ID_CHARS`), `chat_cost_record`, `check_cost_record`, and `summarize_checks` in `regulatory_usage.py`.
* Excluded: Altering `METERING_FIELDS` key names or `<= 64` bounds (`C7`, `PC-001`).

#### Likely Targets

* `src/core/src/zava_forward/core/regulatory_privacy.py`
* `src/core/src/zava_forward/core/regulatory_usage.py`

#### Dependencies

* None.

#### Validation Expectations

* Existing `metering_record` calls and `<= 64` bounds succeed unchanged; smuggling raw quotes, case JSON, or multiline text inside `record_id`, `rule_card_version`, or `price_version` raises `ValueError`; `cost_record` enforces `cost == "Unknown"` and `cost_minor_units is None` when `price_version == "unpriced"`, and integer `cost_minor_units >= 0` when a versioned price table is explicitly supplied.

#### Completion Evidence

* Closed-schema metering, cost, and retention-alignment helpers for chat and checks verified under strict typing.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Implement role-scoped, retention-aligned, audited `governed_metering_and_cost` reader

#### Context

Issue #217 Criterion 4 requires metering and cost records for chat and checks to "follow the same role-scoped access, retention, and audit controls".

#### Intent

Provide a unified governed inspection entrypoint in `regulatory_usage.py` that reads `chat.regulatory.turn` audit entries (SQL `audit` or JSONL `audit_path`, scoped to `who == user_key(user)` and `record["role"] == user["role"]`) and `LawStore` `reg_check` rows (`SELECT id, at, body FROM reg_check`, extracting only `id`, `at`, `card_id`, `card_version`, `audience`, `decision_owner`, and `usage`, scoped to `user["role"] in check["audience"] or user["email"] == check["decision_owner"]`, per `PC-001`) under identical role-scoped access checks, `retention_alignment` cutoff filtering, and metadata-only `store.audit` logging.

#### Boundaries

* Included: `governed_metering_and_cost(store, user, *, law=None, surface="all", env=None, as_of=None, retention_days=None, price_schedule=None)` in `regulatory_usage.py`.
* Excluded: Reading chat message transcripts (`chat_message` table) or provision bodies (`reg_provision`).

#### Likely Targets

* `src/core/src/zava_forward/core/regulatory_usage.py`

#### Dependencies

* P01-T02, P02-T01.

#### Validation Expectations

* Denies `Contractor`, unauthenticated/unknown roles, `view_only` where unpermitted, unverified `trusted-proxy` principals, and Entra principals lacking `"regulatory_chat"` (for chat) or staff/`"rule_owner"`/`"regulatory_chat"` eligibility (for checks), logging `regulatory_metering_denied`; filters out records older than the retention window (`CHAT_RETENTION_DAYS` / `AUDIT_RETENTION_DAYS`) with `retention_alignment` (`dpo_reviewed=False`) attached; logs metadata-only `regulatory_metering_read` on permitted reads; never touches message text or source quotes.

#### Completion Evidence

* `governed_metering_and_cost` implemented and verified against `Fixture` (`Store` and `SqlStore` + `LawStore`).

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Targeted `test_*217*.py` test suite, component documentation, and verification

### Context

The caller specifies exact validation: `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*217*.py' -v` (never untargeted discovery). No existing test file matches `test_*217*.py`.

### Intent

Create `src/core/tests/test_regulatory_privacy_audit_217.py` covering all four Issue #217 acceptance criteria and regression invariants, update `src/core/README.md`, and pass all targeted checks cleanly.

### Boundaries

* Included:Test ownership locked:
  * Canonical new test file: `src/core/tests/test_regulatory_privacy_audit_217.py`
  * Exact test removals: `none`
  * Maximum test method additions: `16` focused test methods across Foundry query minimisation/purpose gates, Entra 3-role separation & separation of duties, UK GDPR Art 22A-22C propose/flag + append-only human decision retention, chat+check metering/cost closed schemas + role/retention/audit parity, and backwards compatibility of `QUERY_FIELDS`, `minimise_query`, `record_human_decision`, and `metering_record`.
  * Documentation target: `src/core/README.md` (`#217` and `#208` notes).
* Excluded: Running untargeted `unittest discover -s tests` without `-p`.

### Likely Targets

* `src/core/tests/test_regulatory_privacy_audit_217.py`
* `src/core/README.md`

### Dependencies

* P01, P02.

### Validation Expectations

* `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*217*.py' -v` all exit 0.

### Completion Evidence

* Passing command output recorded in `.copilot-tracking/changes/2026-11-14/217-regulatory-privacy-audit-2305-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Create `src/core/tests/test_regulatory_privacy_audit_217.py` and update `src/core/README.md`

#### Context

`test_regulatory_privacy_audit_217.py` is matched by `-p 'test_*217*.py'` and checked by `mypy --strict` and `ruff` (`C11`). `src/core/README.md` lines 4700-4785 document `#217` and `#208`.

#### Intent

Author focused, high-signal semantic and negative-case tests for Objectives 1-4 plus backwards-compatibility assertions, and update `src/core/README.md` concisely without `.copilot-tracking/` references or false compliance claims.

#### Boundaries

* Included: `src/core/tests/test_regulatory_privacy_audit_217.py` (<= 16 test methods, 0 removals, using typed `Callable`/`Any` bindings for untyped sibling modules/constructors so `mypy --strict` passes without editing `pyproject.toml`, and including compatibility checks for `metering_record` `<= 64` bounds, `record_human_decision(..., role="approver")`, `QUERY_FIELDS` non-overlap with `SPECIAL_CATEGORY`, and `summarize` plain-language error wrapping per `PC-005`) and `src/core/README.md`.
* Excluded: Modifying existing test files unless needed (none planned).

#### Likely Targets

* `src/core/tests/test_regulatory_privacy_audit_217.py`
* `src/core/README.md`

#### Dependencies

* P01, P02.

#### Validation Expectations

* Every test fails if its corresponding control is removed and verifies canary absence (`PRIVATE-HEALTH-CANARY`, `PRIVATE-REPORT-CANARY`, `QUOTE`), SQLite append-only trigger enforcement, Entra 3-role isolation, and metadata-only audit entries.

#### Completion Evidence

* File created, formatted, strict-type-clean, and README updated.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Execute targeted `mypy`, `ruff`, and `test_*217*.py` validation in `src/core`

#### Context

Caller requirement 2 mandates running only the exact targeted command in `src/core`.

#### Intent

Verify static typing, lint, formatting, and all `test_*217*.py` tests pass with exit code 0.

#### Boundaries

* Included: Running the exact `mypy` + `ruff check` + `ruff format --check` + `unittest discover -s tests -p 'test_*217*.py' -v` pipeline.
* Excluded: Running untargeted `unittest discover -s tests`.

#### Likely Targets

* `src/core/` validation execution.

#### Dependencies

* P03-T01.

#### Validation Expectations

* Exit code 0 across all four checks.

#### Completion Evidence

* Recorded command output in the changes artifact.

#### Unresolved Items

* None.
