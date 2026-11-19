<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #217 Regulatory Assistant Security, Privacy, and Audit Controls

## Metadata

* Task ID: 217-regulatory-privacy-audit-2305
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/217-regulatory-privacy-audit-2305-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver the four locally verifiable Issue #217 engineering acceptance criteria in src/core (Foundry query minimisation and special-category purpose controls; separate Entra roles for authors, approvers, and chat users; UK GDPR Articles 22A to 22C propose/flag and retained named-human decision guard with recorded reasons; closed-schema identifier/count/version-only chat and check metering and cost records governed by shared role-scoped access, retention, and audit controls) and validate exclusively with `cd /home/azureuser/source/ama-demo-wt/feat-217-regulatory-privacy-audit-2305/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*217*.py' -v`.
* Research and evidence considered: .copilot-tracking/research/2026-11-14/217-regulatory-privacy-audit-2305-research.md, .copilot-tracking/plans/2026-11-14/217-regulatory-privacy-audit-2305-plan.md, .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md, src/core/src/zava_forward/core/regulatory_privacy.py, src/core/src/zava_forward/core/regulatory_usage.py, src/core/src/zava_forward/core/regulatory_chat.py, src/core/src/zava_forward/core/rule_engine.py, src/core/src/zava_forward/core/rulecards.py, src/core/tests/test_regulatory_privacy.py, src/core/tests/test_regulatory_usage.py, and src/core/pyproject.toml.
* Decisions, dependencies, and acceptance criteria considered: Option A in-place extension of regulatory_privacy.py and regulatory_usage.py wired to regulatory_chat.py, rule_engine.py, and LawStore; fail-closed `dpo_reviewed=False` and OD-51 `cost="Unknown"` when unpriced; strict `mypy` and `ruff` compliance without modifying src/core/pyproject.toml; zero untargeted unit test discovery.
* Assessment boundary: Evaluates completeness, codebase contract accuracy, security/privacy fail-closed guarantees, backwards compatibility with supplied tests, and strict static-typing feasibility within src/core. Does not inspect unsupplied modules (`identity.py`, `data_protection.py`, `projection.py`, `chat_privacy.py`, `controls.py`, `lawstore.py`, `src/api/auth.py`) directly beyond their call sites in the supplied source files and research citations, and does not assess external human DPO/Legal sign-offs or live Azure Entra/Foundry runtime state.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1 / Q1 / P01-T01 | Partial | Covers scalar/cue checks and purpose gates, but `QUERY_FIELDS` lacks the planned count fields (`hazard_count`, `active_hold_count`, `automated_decision_count`) and `RegulatoryChat.foundry_query` does not explicitly invoke `self.admit(user)` before `store.detail` (PC-003). |
| FR-2 / Q2 / P01-T02 | Partial | Covers 3-role mapping and `identity.distinct`, but misstates `RegulatoryChat.admit()` current behavior: `admit()` never calls `identity.verified`, keys off `auth_provider == "trusted-proxy"` rather than `auth_mode`, skips `current_user` in SQL mode, and strips `oid`, `tid`, `auth_mode`, `entra_roles`, and `view_only` when merging `person` (PC-002). |
| FR-3 / Q3 / P01-T03 | Partial | Covers append-only `LawStore` DDL triggers and non-memory human reasons, but omits a uniqueness/conflict guard per `(proposal_id, proposal_version)` against overwrite-by-`INSERT` and explicit `law.rules.transaction()` mutation wrapping (PC-004). |
| FR-4 / Q4 / P02-T01 | Partial | Covers OD-51 `cost_record`, but proposes widening `metering_record` ID length to 128 and adding `actor_role`, which breaks `test_regulatory_privacy.py:208,215`, and assumes a nonexistent `reg_check.usage_json` SQL column and chat turn metadata field (PC-001). |
| FR-4 / Q4 / P02-T02 | Partial | Covers unified reader intent, but depends on a nonexistent `retention_alignment` function in `regulatory_privacy.py` and omits `reg_check` parent audience/decision-owner scoping (`check["audience"]` / `check["decision_owner"]`) (PC-001). |
| NFR-1 / Q5 / P03-T01, P03-T02 | Partial | Locks targeted `-p 'test_*217*.py'` command and test cap (`<= 16`), but omits typed-callable/constructor bindings needed to pass `mypy` `disallow_untyped_calls = true` when calling untyped sibling modules and constructing untyped stores in `test_regulatory_privacy_audit_217.py` without editing `pyproject.toml` (PC-005). |

## Verdict

* Verdict: Revise
* Rationale: The 3-phase architecture is sound and well-scoped to `src/core`, but five concrete discrepancies between the plan/research assumptions and the actual `src/core` source files (`PC-001` through `PC-005`) would cause runtime SQL/schema failures, Entra claim stripping or bypasses in `RegulatoryChat.admit()`, existing contract regressions on `metering_record`, append-by-`INSERT` decision overrides, and `mypy --strict` `[no-untyped-call]` errors unless corrected in the plan and phase details before implementation. All five findings are direct planner corrections requiring no user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Tokenomics tasks rely on nonexistent storage columns/helpers, weaken `metering_record` bounds, and omit per-check audience scoping

* Related IDs: FR-4, Q4, P02, P02-T01, P02-T02
* Evidence: src/core/src/zava_forward/core/regulatory_privacy.py:23-74,204-248; src/core/src/zava_forward/core/regulatory_usage.py:45-58; src/core/src/zava_forward/core/regulatory_chat.py:137-172,274-331; src/core/src/zava_forward/core/rule_engine.py:28-29,345-391,424,480-484; src/core/tests/test_regulatory_privacy.py:206-223; .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md:174-244
* Concern: Four concrete mismatches exist in P02:
  1. `P02-T01` proposes changing `metering_record` lexical bounds to `[A-Za-z0-9._:@+/-]{1,128}` and adding `actor_role`. In `regulatory_privacy.py:217,241`, `metering_record` already enforces `1 <= len(value) <= 64` over `_ID_CHARS` (`[A-Za-z0-9._:-]`), and `test_regulatory_privacy.py:208,215` explicitly asserts that unknown fields and `prompt_version="x" * 65` raise `ValueError`.
  2. `P02-T01` and `P02-T02` state that `reg_check` has a `usage_json` column and `RegulatoryChat.ask` writes `usage` into turn metadata. In fact, `reg_check` (`rule_engine.py:28-29,379-390`) has columns `(id, case_id, at, check_seq, body)` with `usage` stored at `json.loads(body)["usage"]` and `card_version` stored as `int` (which must be formatted as a short string ID such as `f"{card_id}@v{card_version}"` for `metering_record`/`cost_record`), while `RegulatoryChat.ask` (`regulatory_chat.py:137-172,289-325`) records content-free chat `usage` only in the `audit` ledger (`SELECT ... FROM audit` on `SqlStore` and `store.audit_path` JSONL on `Store` for `action == "chat.regulatory.turn"`).
  3. `P02` and `P02-T02` depend on `retention_alignment` from `regulatory_privacy.py`, which does not exist (only `retention_report` and `readiness_report` exist in `regulatory_privacy.py:23-140`, and P01 never defines `retention_alignment`).
  4. `P02-T02` checks staff/role eligibility for `reg_check` reads globally without filtering each check by `user["role"] in check["audience"] or user["email"].strip().lower() == check["decision_owner"].strip().lower()`, unlike parent check/alert access in `RuleEngine.alerts()` (`rule_engine.py:424,480-484`) and `CLASSES["usage"]` ("inherits parent record access, retention and audit review").
* Impact: Querying `usage_json` or importing `retention_alignment` fails immediately at runtime; widening `metering_record` to 128 chars or adding `actor_role` breaks existing `test_regulatory_privacy.py` assertions; and returning unscoped `reg_check` metering/cost rows across unauthorized staff roles violates Criterion 4 role-scoped access parity.
* Smallest useful change: Update P02, P02-T01, and P02-T02 so that: (a) `metering_record` keeps `METERING_FIELDS`, `_ID_CHARS`, and `1 <= len <= 64` intact while `COST_FIELDS`/`cost_record` uses the same closed identifier/count/version discipline (`cost="Unknown"` and `cost_minor_units=None` when `price_version == "unpriced"`); (b) check metering/cost reads `SELECT id, at, body FROM reg_check` extracting only `id`, `at`, `card_id`, `card_version` (formatted as string), `audience`, `decision_owner`, and `usage`, and chat metering/cost reads `chat.regulatory.turn` entries from `store` SQL `audit` / `audit_path` (matching `RegulatoryChat.usage_status`); (c) `regulatory_privacy.py` explicitly defines `retention_alignment` (preserving `retention_report`'s `SYNTH-` validation, `status="unknown"` when unconfigured unless an explicit synthetic window is supplied, `dpo_reviewed=False`, and `deletion_enabled=False`); and (d) `governed_metering_and_cost` filters `reg_check` rows to `user["role"] in check["audience"] or user["email"] == check["decision_owner"]` and chat rows to `who == user_key(user)` and `record["role"] == user["role"]`.
* Action owner: planning_parent
* Exact resolving evidence: Revised P02, P02-T01, and P02-T02 sections in `.copilot-tracking/plans/2026-11-14/217-regulatory-privacy-audit-2305-plan.md` and `.copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md` naming `reg_check.body["usage"]`, `audit` `chat.regulatory.turn` entries, `<= 64` `_ID_CHARS` retention in `metering_record`, explicit `retention_alignment` creation, and `audience`/`decision_owner` check scoping.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: `RegulatoryChat.admit()` neither calls `identity.verified` nor preserves Entra claims across SQL/JSON branches, and uses `auth_provider` rather than `auth_mode`

* Related IDs: FR-2, Q2, P01-T02
* Evidence: src/core/src/zava_forward/core/regulatory_chat.py:53-112,343-346; src/core/src/zava_forward/core/rule_engine.py:517-542; .copilot-tracking/research/2026-11-14/217-regulatory-privacy-audit-2305-research.md:107,118; .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md:99-128
* Concern: P01-T02 assumes `RegulatoryChat.admit()` already enforces `identity.verified` on `trusted-proxy` principals and proposes gating `"regulatory_chat"` on `auth_mode == "trusted-proxy"`. Direct inspection of `regulatory_chat.py:53-112` shows: (1) `identity.verified` is never imported or called anywhere in `regulatory_chat.py` (in the SQL branch `hasattr(self.store, "assistant_connection")`, `admit()` skips `self.iso.current_user(user)` altogether); (2) lines 75, 103, and 343 check `user.get("auth_provider") == "trusted-proxy"`, so an Entra caller setting only `auth_mode == "trusted-proxy"` falls into `else person` on line 76 and loses `rule_roles` completely, whereas a caller setting `auth_provider == "trusted-proxy"` without `auth_mode` would bypass an `auth_mode`-only `"regulatory_chat"` check; and (3) both branches reconstruct `user`/`current` from `person` keeping only `role`, `auth_provider`, and `rule_roles`, stripping `oid`, `tid`, `auth_mode`, `entra_roles`, and `view_only` needed by downstream Entra role and `identity.distinct` checks.
* Impact: Entra principals with `auth_mode="trusted-proxy"` fail or lose `rule_roles` in `RegulatoryChat.admit()`, SQL-backed `RegulatoryChat` omits `identity.verified` and `view_only` rejection, and downstream callers of `admit()` lose `oid`/`tid` claims required for alias-proof separation of duties.
* Smallest useful change: Specify in P01-T02 that `RegulatoryChat.admit()` treats a caller as `trusted-proxy` whenever `user.get("auth_mode") == "trusted-proxy" or user.get("auth_provider") == "trusted-proxy"`, rejects `bool(user.get("view_only"))` in all modes, enforces `identity.verified(user)` when `auth_mode == "trusted-proxy"` (or when Entra `oid`/`tid` claims are supplied on a trusted-proxy principal so legacy synthetic fixtures with `auth_provider="trusted-proxy"` and `rule_roles=["regulatory_chat"]` stay compatible if they omit `oid`/`tid`), resolves `rule_roles` from `entra_roles` union explicit `rule_roles` and requires `"regulatory_chat"`, and preserves `oid`, `tid`, `auth_mode`, `auth_provider`, `entra_roles`, `rule_roles`, and `view_only` on the returned principal dict; apply the same `trusted-proxy` (`auth_mode` or `auth_provider`) + `not view_only` + `identity.verified` rule in `RuleEngine.disposition()`.
* Action owner: planning_parent
* Exact resolving evidence: Updated P01-T02 specification in `.copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md` covering both `auth_mode` and `auth_provider` `"trusted-proxy"` branches, `view_only` denial, `identity.verified` enforcement, and Entra claim preservation in `RegulatoryChat.admit()` and `RuleEngine.disposition()`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `build_foundry_query` question-scoped count fields conflict with unchanged `QUERY_FIELDS` tuples, and `RegulatoryChat.foundry_query` omits admission gating

* Related IDs: FR-1, Q1, P01-T01
* Evidence: src/core/src/zava_forward/core/regulatory_privacy.py:143-165; src/core/src/zava_forward/core/regulatory_chat.py:114-121,194-263; src/core/tests/test_regulatory_privacy.py:139-160; .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md:64-97
* Concern: `P01-T01` expects `build_foundry_query` and `RegulatoryChat.foundry_query(user, cid, question)` to layer atop `QUERY_FIELDS` while retaining `hazard_count` and `active_hold_count` for hazard home questions and `automated_decision_count` for automated-decision home questions. However, `QUERY_FIELDS` (`regulatory_privacy.py:143-147`) contains none of those count keys (`check_explain` allows only `card_id`, `card_version`, `check_kind`, `outcome`, `as_of`, `case_id`; `rule_lookup` allows `card_id`, `card_version`, `provision_id`, `source_id`, `version`, `as_of`), so passing candidate fields through `minimise_query` first drops all three count keys. In addition, `RegulatoryChat.bundle(user, cid, question)` (`regulatory_chat.py:194`) assumes its caller already ran `self.admit(user)`, whereas `RegulatoryChat.foundry_query(user, cid, question)` is a public entrypoint taking `(user, cid, question)` directly without a thread lookup.
* Impact: Either question-specific count fields are silently dropped so hazard and automated-decision Foundry queries become indistinguishable, or an unadmitted caller (such as `Contractor`, `view_only`, or a `trusted-proxy` principal lacking `regulatory_chat`) can invoke `RegulatoryChat.foundry_query` directly without passing `self.admit(user)`.
* Smallest useful change: Clarify in P01-T01 how `build_foundry_query` composes with `QUERY_FIELDS` (for example, keeping `minimise_query(purpose, fields)` unchanged against `QUERY_FIELDS` for existing callers while defining explicit question-topic field subsets in `QUESTION_QUERY_FIELDS` for `provision_lookup`, `hazard-awareness-clock`, and `automated-decision-safeguard` disjoint from `SPECIAL_CATEGORY`/`SPECIAL_CATEGORY_FIELDS`, or extending `QUERY_FIELDS["check_explain"]` only if existing `test_regulatory_privacy.py:140-159` assertions remain satisfied), and require `RegulatoryChat.foundry_query(user, cid, question)` to call `user = self.admit(user)` and redact/refuse `question` before reading `self.store.detail(cid, user)`.
* Action owner: planning_parent
* Exact resolving evidence: Updated P01-T01 detail in `.copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md` specifying the exact per-question allowlist composition with `QUERY_FIELDS` and mandatory `self.admit(user)` entry check in `RegulatoryChat.foundry_query`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Append-only `ConsequentialDecisionGuard` DDL triggers do not prevent decision overwrite via duplicate `INSERT`

* Related IDs: FR-3, Q3, P01-T03
* Evidence: src/core/src/zava_forward/core/rule_engine.py:259-283,551-555; src/core/src/zava_forward/core/rulecards.py:109-140; .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md:130-166
* Concern: `P01-T03` relies on SQLite `BEFORE UPDATE`/`BEFORE DELETE` `RAISE(ABORT, ...)` triggers (and MSSQL append-only ledger/triggers) on `reg_consequential_proposal` and `reg_consequential_decision` to retain human decisions immutably, and states that `authorize_consequential_action` fails closed after rejection or deferral. Update/delete triggers alone do not prevent inserting a second row for the same `(proposal_id, proposal_version)` with `outcome="accepted"` after a `"rejected"` row has already been recorded.
* Impact: Without a primary-key/uniqueness constraint per `(proposal_id, proposal_version)` (or explicit conflict rejection inside `with self.law.rules.transaction():` matching `RuleEngine.disposition()` at `rule_engine.py:551-555`), a rejected consequential proposal could be overridden via a subsequent `INSERT` without triggering `BEFORE UPDATE` or `BEFORE DELETE`.
* Smallest useful change: Specify in P01-T03 that `ConsequentialDecisionGuard` wraps DDL and writes in `with self.law.rules.transaction():` (supporting both `sqlite` and `mssql` dialects on `law.sql`) and enforces one immutable recorded decision per `(proposal_id, proposal_version)` via SQL `PRIMARY KEY`/`UNIQUE` constraint and explicit pre-insert check so a new proposal version is required after rejection or change.
* Action owner: planning_parent
* Exact resolving evidence: Updated P01-T03 specification in `.copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md` defining `(proposal_id, proposal_version)` uniqueness/conflict rejection and `law.rules.transaction()` wrapping across `sqlite` and `mssql` DDL.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: `mypy --strict` `disallow_untyped_calls` will fail on direct calls to untyped `src/core` sibling modules and test fixture constructors unless typed adapters are planned

* Related IDs: NFR-1, Q5, P01-T01, P01-T03, P02-T02, P03-T01, P03-T02
* Evidence: src/core/pyproject.toml:35-156; .copilot-tracking/plans/2026-11-14/217-regulatory-privacy-audit-2305-plan.md:83-88; .copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md:247-314
* Concern: `src/core/pyproject.toml:35-41` enables `strict = true` (`disallow_untyped_calls = true`) across `src` and `tests`, while `projection`, `chat_privacy`, `controls`, `lawstore`, `rulecards`, `store`, `sqlstore`, `chat_isolation`, and `tests.regulatory_fixture` are untyped (`ignore_errors = true` or `disallow_untyped_calls = false` overrides). Neither `regulatory_privacy.py`, `regulatory_usage.py`, nor the new `tests/test_regulatory_privacy_audit_217.py` appears in `disallow_untyped_calls = false`, and NFR-1 forbids editing `pyproject.toml`. Defining `Protocol` types for function parameters does not suppress `[no-untyped-call]` when `regulatory_privacy.py` calls `projection.can_see_reason`, `chat_privacy.redact`, or `controls.is_memory_reference`, or when `test_regulatory_privacy_audit_217.py` constructs `LawStore(...)`, `Store(...)`, `SqlStore(...)`, `RuleCardStore(...)`, or `ChatIsolation(...)`. Furthermore, because the caller's validation command runs only `-p 'test_*217*.py'`, regressions against existing `test_regulatory_privacy.py` and `test_regulatory_usage.py` invariants are checked only if `test_regulatory_privacy_audit_217.py` pins them directly.
* Impact: Direct calls to untyped module functions or test fixture constructors cause `python3 -m mypy` to exit non-zero in P03-T02, and unexercised legacy assertions could drift unnoticed under `-p 'test_*217*.py'`.
* Smallest useful change: Note in P01/P02/P03-T01 that untyped sibling callables and test fixture constructors imported into `regulatory_privacy.py`, `regulatory_usage.py`, and `test_regulatory_privacy_audit_217.py` must be bound through `typing.cast(Callable[...], ...)` or `Any`-typed module aliases so `mypy --strict` passes with zero edits to `pyproject.toml`, and ensure `test_regulatory_privacy_audit_217.py` (within its `<= 16` test method cap) includes compatibility assertions for `metering_record` `<= 64` length bounds, `record_human_decision(..., role="approver")`, `QUERY_FIELDS` non-overlap with `SPECIAL_CATEGORY`, and `summarize` plain-language error wrapping.
* Action owner: planning_parent
* Exact resolving evidence: Updated P03-T01 (and typing note in P01/P02) in `.copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md` specifying typed `Callable`/`Any` import bindings for untyped sibling modules/constructors and explicit compatibility assertions inside `test_regulatory_privacy_audit_217.py`.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Strong alignment with repository governance and honesty rules: the plan preserves `dpo_reviewed=False`, OD-51 `cost="Unknown"` when unpriced, deferred human Legal review on seed card `automated-decision-safeguard` (#211, #224), and `Refs #217` non-closure discipline.
* Cohesive module placement: keeping controls in `regulatory_privacy.py` and `regulatory_usage.py` with targeted integration seams in `regulatory_chat.py` and `rule_engine.py` avoids unnecessary module sprawl and addresses the documented pure-builder gap.
* Locked validation discipline: P03-T01 and P03-T02 honor the caller's exact targeted `mypy`, `ruff`, and `-p 'test_*217*.py'` command and set a clear test-ownership boundary (`0` removals, `<= 16` methods).
* Accepted residual risk: Human DPO review of the chat/memory DPIA, the named Legal decision on UK GDPR Articles 22A to 22C, and live Azure Entra/Foundry runtime verification remain outside offline `src/core` scope and are explicitly left fail-closed (`dpo_reviewed=False`).

## Questions or Blocking Evidence Gaps

* None. Every finding is resolvable directly from the supplied `src/core` contracts without user input or further research.

## Limitations

* This critique evaluated only the caller-supplied tracking artifacts and primary `src/core` files (`regulatory_privacy.py`, `regulatory_usage.py`, `regulatory_chat.py`, `rule_engine.py`, `rulecards.py`, `test_regulatory_privacy.py`, `test_regulatory_usage.py`, `pyproject.toml`). Sibling modules referenced by research (`identity.py`, `data_protection.py`, `projection.py`, `chat_privacy.py`, `controls.py`, `lawstore.py`, `src/api/auth.py`) were assessed through their usage in the supplied files and `pyproject.toml` typing rules without additional file reads or test execution.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply direct planner revisions for PC-001 through PC-005 across `.copilot-tracking/plans/2026-11-14/217-regulatory-privacy-audit-2305-plan.md` and `.copilot-tracking/details/2026-11-14/217-regulatory-privacy-audit-2305-phase-details.md`, record their Critique Disposition entries, and finalize the plan for `rpi-implement` without running another critique pass.
* User response required: no
