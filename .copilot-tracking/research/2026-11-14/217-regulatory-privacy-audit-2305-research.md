<!-- markdownlint-disable-file -->

# Task Research: 217-regulatory-privacy-audit-2305

| Field              | Value                                                                             |
|--------------------|-----------------------------------------------------------------------------------|
| Date               | 2026-11-14                                                                        |
| Researcher / agent | rpi-research (RPI Agent)                                                          |
| Status             | Complete                                                                          |
| Artifact path      | .copilot-tracking/research/2026-11-14/217-regulatory-privacy-audit-2305-research.md |

## Research Brief

* What to research: Current coverage and engineering gaps in `src/core` for the four locally verifiable acceptance criteria of Issue #217 ("Security, privacy and audit for the regulatory assistant"):
  1. Foundry queries exclude fields not needed for the question; special-category data follows existing purpose controls.
  2. Authors, approvers, and chat users are separate Entra roles.
  3. UK GDPR Art 22A to 22C guard: system proposes and flags; consequential decisions require and retain a named human with recorded reasons.
  4. Tokenomics: Metering and cost records for chat and checks hold identifiers, counts, and versions only, with no raw case, chat, or retrieved source content, and follow the same role-scoped access, retention, and audit controls.
* Why it matters: ADR 0005, PRD FR-060/AC-106/FR-061/NFR-017, BRD FR-051/NFR-003/CON-003/CON-008/NFR-012/FR-052, the chat/memory DPIA draft, and the AI Tokenomics baseline require deterministic, fail-closed `src/core` controls so regulatory assistance never leaks unneeded case or special-category data to Foundry, never conflates authoring, approval, and chat roles, never takes consequential decisions without retained named-human reasons, and never exposes raw case, chat, or source text in metering or cost records.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` for local `src/core` delivery on branch `feat/ai-217-regulatory-privacy-audit-2305` (target `feat/demo-164-chat-grounding-provenance-0900`).
* Scope: `src/core/src/zava_forward/core/{regulatory_privacy,regulatory_usage,regulatory_chat,rule_engine}.py`, `src/core/tests/test_regulatory_privacy_audit_217.py`, `src/core/README.md`, and read-only contract alignment checks across `rulecards.py`, `lawstore.py`, `identity.py`, `data_protection.py`, `projection.py`, `chat_privacy.py`, `controls.py`, `src/api/src/zava_forward/api/{auth,server}.py`, `infra/entra/app-registration.json`, and `docs/`.
* Non-goals: Claiming DPO DPIA sign-off (`dpo_reviewed` must stay `False`), recording a live Legal applicability decision (#224), live Azure Entra tenant role-assignment verification (#358), live Foundry network calls, running untargeted `unittest discover -s tests` without `-p`, or pushing to remote (`git push` prohibited).
* Criteria: All four engineering objectives enforced deterministically in `src/core` with full backwards compatibility for existing `src/core` and `src/api` callers; strict `mypy`, `ruff check .`, `ruff format --check .`, and `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*217*.py' -v` pass cleanly.
* Requested outputs: Dated primary research artifact with converged implementation recommendation for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                            |
|--------------------------------------|------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1-Q5 below covering Foundry query minimisation/purpose gates, Entra 3-role separation, Art 22A-22C persistence, chat+check tokenomics/cost governance, and strict typing/test constraints |
| Codebase scope                       | `src/core/`, `src/api/` (read-only alignment), `src/agents/` (read-only alignment), `infra/entra/`, `docs/`       |
| External scope                       | none (codebase and committed regulatory/DPIA/ADR synthesis task)                                                 |
| Initial internal candidate areas     | `src/core/src/zava_forward/core/{regulatory_privacy,regulatory_usage,regulatory_chat,rulecards,rule_engine,identity,data_protection,projection,chat_privacy,controls,lawstore}.py` |
| Initial external candidate areas     | none                                                                                                             |
| Research posture                     | focused                                                                                                          |
| Posture provenance                   | caller-specified bounded `src/core` objective, named target branch, and explicit targeted validation command      |
| Explicit limits / deadline           | Run only targeted `-p 'test_*217*.py'` tests (never untargeted discovery); do not push; clean working tree       |
| Posture-specific completion basis    | focused scope and materiality: every touched module, caller contract, test assertion, and spec trace inspected   |
| Edits allowed during research?       | no, research-only                                                                                                |
| Resolved evidence root               | `.copilot-tracking/`                                                                                             |
| Known constraints / excluded sources | Keep `dpo_reviewed=False`; use `Refs #217` (human DPO/Legal/live tenant gates remain open); no `.copilot-tracking/` citations in code/docs/commit messages |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                      | Match and provenance                            | Scoped authority or output contract          | Selected / skipped reason                                                       |
|---------------------|--------------------------------|-------------------------------------------------|----------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | Repository custom instructions | `applyTo: "**"` across repository               | Legal/regulatory honesty, focused tier, style | Selected: governs non-inference rules, `Refs #217`, and `src/core` tests        |
| Skill               | `rpi-research`                 | Explicit RPI loop phase 1                       | Read-only three-wave primary artifact        | Selected: active phase skill                                                    |
| Skill               | `privacy-standards`            | Privacy/UK GDPR domain                          | General privacy guidance                     | Skipped: repository DPIA, UK GDPR review pack, and `data_protection.py` already define exact enforced contracts |
| Research specialist | `hve-core-all:rpi-researcher`  | Host-registered delegated research worker       | Subagent lane artifact                       | Skipped (inline): tightly coupled `src/core` module cluster inspected directly  |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                               | Answers / unanswered                     | Resulting decision or selected further research                                 |
|------------------|-------------------------------------------------------------------------------------|------------------------------------------|---------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI execution with explicit Issue #217 criteria, branch, and test command | Unasked (non-interactive; unambiguous)   | Proceed in focused convergence mode                                             |
| Convergence      | All module contracts, typing rules, and caller expectations verified in `src/core` and `src/api` | Unasked (non-interactive)                | Converge on extending `regulatory_privacy.py`, `regulatory_usage.py`, `regulatory_chat.py`, `rule_engine.py`, `test_regulatory_privacy_audit_217.py`, and `src/core/README.md` |

## Scope and Success Criteria

* Scope: Deterministic `src/core` enforcement, persistence, role-scoped governance, audit logging, unit tests (`test_*217*.py`), and component documentation (`src/core/README.md`) for Issue #217.
* Assumptions:
  * Existing `test_regulatory_privacy.py`, `test_regulatory_usage.py`, `test_regulatory_chat.py`, `test_rulecards.py`, `test_rule_engine.py`, and `src/api/tests/test_regulatory_chat_api.py` contracts must remain 100% backwards-compatible. (Verified by reading their exact assertions.)
  * Human DPO review of the chat/memory DPIA and Legal decision on UK GDPR Articles 22A-22C remain pending human actions and must never be fabricated in code or docs. (Verified in `docs/reference/research/chat-memory-dpia.md` and `docs/reference/regulatory/reviewed-updates/2026-11-01-adm-ai-act-applicability-review.md`.)
* Success criteria:
  * Every question Q1-Q5 is answered with workspace-relative `path:line` citations (`C1`-`C12`).
  * Three waves (`Wider`, `Deeper`, `Contrarian`) are executed and reflected in order.
  * Alternatives are compared and one cohesive `src/core` design is selected.

## Task Research Requests

* Explicit requests: Run full RPI loop (`research`, `plan`, `implement`, `review`) for Issue #217; deliver the four engineering objectives in `src/core`; write all 4 `.copilot-tracking/` artifacts dated `2026-11-14`; run only `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*217*.py' -v`; commit cleanly on `feat/ai-217-regulatory-privacy-audit-2305` without pushing.
* Inferred research questions: What partial helpers already exist in `regulatory_privacy.py` and `regulatory_usage.py`, why Issue #217 remains open on closure audit, where `src/core` lacks enforcement vs `src/api`, and how `pyproject.toml` strict typing governs interactions with legacy untyped modules.
* Caller constraints and non-goals: Never run untargeted `unittest discover -s tests`; never push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                        | Source / checkpoint  | Effect on active brief, evidence, or revalidation                               |
|----------------------------------------------------------|------------------------------------------------------------------------------|----------------------|---------------------------------------------------------------------------------|
| narrow                                                   | Implement locally verifiable Issue #217 engineering controls in `src/core`   | User prompt (intake) | Keeps changes inside `src/core` while preserving `src/api` caller compatibility |
| narrow                                                   | Run only targeted `-p 'test_*217*.py'` unit discovery alongside `mypy`/`ruff`| User prompt (intake) | Requires a dedicated `test_regulatory_privacy_audit_217.py` matching `test_*217*.py` |
| exclude                                                  | Do not push to remote; working tree must be clean after commit               | User prompt (intake) | Local commit only with `Refs #217` and Copilot trailer                          |

## Research Questions

|  # | Sub-question                                                                                                    | Type (depth / breadth / straightforward) | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|----------|
| Q1 | What Foundry query minimisation and special-category purpose controls exist today, and what gaps remain?        | depth                                    | H        | answered |
| Q2 | How are Entra roles (`RuleAuthor`, `RuleOwner`, `RegulatoryChat`) separated across `infra`, `api`, and `core`?  | breadth                                  | H        | answered |
| Q3 | Why is `record_human_decision` insufficient for the UK GDPR Art 22A-22C propose/flag and retention criterion?   | depth                                    | H        | answered |
| Q4 | How do chat and check metering/cost records currently work, and what access, retention, and audit gaps exist?   | depth                                    | H        | answered |
| Q5 | What typing (`mypy --strict`), formatting (`ruff`), and backwards-compatibility invariants apply in `src/core`? | straightforward                          | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: GitHub Issue #217 and closure-audit comments, `docs/adrs/0005-regulatory-compliance-assistant.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/resources/ai-tokenomics.md`, and `docs/reference/regulatory/reviewed-updates/2026-11-01-adm-ai-act-applicability-review.md`.
* Reused (verified) findings: PRs #781 and #1155 introduced initial pure dictionary helpers in `regulatory_privacy.py` (`privacy_readiness`, `retention_alignment`, `minimise_query`, `record_human_decision`, `metering_record`) and `regulatory_usage.py` (`offline_usage`, `usage_metering`, `economics`, `summarize`), plus `RULE_ROLES` in `src/api/src/zava_forward/api/auth.py`.
* Superseded / incomplete elements identified: `src/core/README.md:4706` explicitly documents that `record_human_decision` "is a pure builder and is not wired to storage or an approval flow"; `minimise_query` performs only static flat-dict key filtering without question-specific field selection, scalar/cue bounds, or `data_protection`/`projection` purpose enforcement; `src/core` has no canonical Entra 3-role separation contract and `RegulatoryChat.admit()` omits checking `"regulatory_chat"` for `trusted-proxy` users; and `regulatory_usage` neither builds closed-schema cost records nor governs `reg_check` + `chat` metering/cost reads under unified role-scoped access, retention expiry, and metadata-only audit logging.

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow to `src/core` and `-p 'test_*217*.py'`; exclude `git push`.
* Active research posture and completion basis: `focused`; all relevant `src/core`, `src/api`, `src/agents`, `infra/entra`, and `docs/` sources read directly.
* Explicit limits or deadline effect: none blocking complete local evidence.

#### Wave 1: Wider

* Plan and independent lanes: Inline breadth survey across `docs/adrs/0005-regulatory-compliance-assistant.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/brds/agentic-retrofit-programme-brd.md`, `docs/reference/resources/ai-tokenomics.md`, `docs/reference/research/chat-memory-dpia.md`, `infra/entra/app-registration.json`, `src/api/src/zava_forward/api/{auth,server}.py`, and `src/core/src/zava_forward/core/`.
* Worker evidence relationships or inline fallback: Inline (bounded repository cluster): Q1-Q4 -> `regulatory_privacy.py`, `regulatory_usage.py`, `regulatory_chat.py`, `rulecards.py`, `rule_engine.py`, `identity.py`, `data_protection.py`, `projection.py`, `chat_privacy.py`, `controls.py`, `lawstore.py`.
* Reflection: All four Issue #217 objectives converge on `regulatory_privacy.py` and `regulatory_usage.py` with targeted integration seams in `regulatory_chat.py` and `rule_engine.py`.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Line-by-line inspection of existing implementations, SQLite/MSSQL append-only ledger conventions in `lawstore.py`, existing unit tests, and `src/core/pyproject.toml` strict typing configuration.
* Plan and independent lanes: Inline verification of invariants:
  1. `test_regulatory_privacy.py:143` asserts `set(QUERY_FIELDS) == {"rule_lookup", "check_explain", "alert_triage"}` (`C7`), so `QUERY_FIELDS` keys must stay unchanged while question-specific selection (`build_foundry_query`) and `RegulatoryChat.foundry_query` layer cleanly on top.
  2. `RegulatoryChat.admit()` (`regulatory_chat.py:114-129`, `C3`) checks `identity.verified(user)` for `trusted-proxy` principals and checks `"regulatory_chat"` in `_owner()` (`regulatory_chat.py:163`), yet omits requiring `"regulatory_chat"` in `admit()` itself (relying only on `src/api/server.py:1671`).
  3. `LawStore` (`lawstore.py:146-156`, `C9`) enforces append-only tables via `BEFORE UPDATE` and `BEFORE DELETE` SQLite `RAISE(ABORT, ...)` triggers and MSSQL `LEDGER = ON (APPEND_ONLY = ON)` / `INSTEAD OF UPDATE, DELETE` triggers, providing the exact repository pattern for retaining UK GDPR Art 22A-22C proposals and named-human decisions.
  4. `RuleEngine.evaluate` (`rule_engine.py:420-427`, `C5`) already stores `usage_json` (`offline_usage("regulatory-check", ...)`) on every `reg_check` row, while `regulatory_usage.py` (`C2`) only projects and summarises `chat` turns without cost records, check projection, role-scoped read guards, retention cutoff enforcement, or audit events.
  5. `src/core/pyproject.toml:35-105` (`C11`) runs `mypy` with `strict = true`, where `regulatory_privacy.py`, `regulatory_usage.py`, and any new test file `test_regulatory_privacy_audit_217.py` are NOT in `disallow_untyped_calls = false` or `ignore_errors = true`; all untyped legacy boundaries (`LawStore`, `Store`, `projection`, `chat_privacy`, `controls`) must be typed cleanly via `Protocol` or typed adapters.
* Worker evidence relationships or inline fallback: Inline: Q1-Q5 -> `C1`-`C12`.
* Reflection: Exact caller invariants and typing constraints are clear; no changes to `pyproject.toml` are needed if protocols/adapters are used cleanly.

#### Wave 3: Contrarian

* Plan and independent lanes: Challenge each proposed change for hidden regressions, over-claiming of regulatory/DPO compliance, or side effects on `src/api` and existing `src/core` tests.
* Worker evidence relationships or inline fallback: Inline contrarian checks:
  1. *Could enforcing `"regulatory_chat"` inside `RegulatoryChat.admit()` break `src/api/tests/test_regulatory_chat_api.py` or `src/core/tests/test_regulatory_chat.py`?* Checked `test_regulatory_chat.py` and `test_regulatory_chat_api.py:203-240` (`C10`): synthetic local fixtures do not set `auth_mode="trusted-proxy"` (only `auth_provider="trusted-proxy"` in one test where `rule_roles=["regulatory_chat"]` is already present), whereas real Entra principals produced by `src/api/src/zava_forward/api/auth.py:90` (`C8`) set `auth_mode="trusted-proxy"` and populate `rule_roles` exclusively from `ZavaForward.RuleAuthor`, `ZavaForward.RuleOwner`, and `ZavaForward.RegulatoryChat`. Checking `auth_mode == "trusted-proxy"` in `admit()` preserves every synthetic fixture test while closing the `src/core` Entra bypass.
  2. *Could adding fields to `QUERY_FIELDS` or `METERING_FIELDS` break existing equality tests?* Yes, `test_regulatory_privacy.py:143` (`C7`) asserts exact `set(QUERY_FIELDS)`. Keeping `QUERY_FIELDS` and `METERING_FIELDS` stable while introducing `COST_FIELDS`, `cost_record`, `build_foundry_query`, and tightening scalar/identifier content bounds preserves 100% compatibility.
  3. *Could special-category purpose controls accidentally claim Article 9 / DPO clearance for external Foundry dispatch?* Contrarian check against `chat-memory-dpia.md` (`C12`): DPO review is incomplete (`dpo_reviewed=False`). Therefore, existing purpose controls (`projection.can_see_reason` + `data_protection.dispatch_hold`) govern internal staff eligibility and lawful-basis/DPIA/notice readiness, while external Foundry queries must STILL strip or redact special-category fields/cues and refuse raw external special-category transmission while `dpo_reviewed` is `False`.
  4. *Could cost records violate OD-51 ("Unknown when price source is missing")?* Contrarian check against `ai-tokenomics.md`: cost records must never invent unit rates; when `price_version == "unpriced"` (default offline/unconfigured state), `cost` must be `"Unknown"` and `cost_minor_units` must be `None`, accepting integer minor-unit cost counts only when an explicit versioned price schedule is provided.
* Reflection: Contrarian checks strengthened all four designs and prevented two potential compatibility regressions (`QUERY_FIELDS` key set and `trusted-proxy` `auth_mode` check) plus two governance pitfalls (DPO non-inference and OD-51 `Unknown` cost).

### Cycle 1 Parent Synthesis

* Accepted findings: `C1`-`C12` below.
* Rejected or deferred items: Modifying seed card `automated-decision-safeguard` citation text in `rulecards.py` is explicitly deferred per `2026-11-01-adm-ai-act-applicability-review.md` RI-3 until the human DPO decides #224/#211; modifying `pyproject.toml` ignore lists is rejected in favour of strict typing in all new/edited code.
* Re-entry decision: No second cycle required; all questions Q1-Q5 are answered with primary codebase evidence and zero unresolved blockers within `src/core` scope.

## Evidence Log

### Codebase Evidence

| ID  | Path and lines                                                                 | Tool category | Claim supported                                                                                                                                         | Confidence | Provenance / notes |
|-----|--------------------------------------------------------------------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|------------|--------------------|
| C1  | `src/core/src/zava_forward/core/regulatory_privacy.py:1-214`                   | Code search   | Defines `QUERY_FIELDS`, `SPECIAL_CATEGORY`, `METERING_FIELDS`, `privacy_readiness`, `retention_alignment`, `minimise_query`, `record_human_decision`, and `metering_record`, with `dpo_reviewed=False` and pure dict-only `record_human_decision` | High       | Direct read        |
| C2  | `src/core/src/zava_forward/core/regulatory_usage.py:1-128`                     | Code search   | Defines `offline_usage`, `usage_metering`, `economics` (`cost="Unknown"`), and `summarize` for `regulatory-home-chat` only; lacks `reg_check` projection, `cost_record`, role-scoped read gate, retention expiry filtering, and audit logging | High       | Direct read        |
| C3  | `src/core/src/zava_forward/core/regulatory_chat.py:92-270`                     | Code search   | `RegulatoryChat.admit()` enforces `identity.verified` on `trusted-proxy` and `projection.allowed(user, "chat")`, but omits checking `"regulatory_chat" in user.get("rule_roles", [])` in `admit()` and has no Foundry query builder | High       | Direct read        |
| C4  | `src/core/src/zava_forward/core/rulecards.py:1-259`                            | Code search   | Uses `AUTHOR = "rule_author"` and `OWNER = "rule_owner"`, enforces `author != actor` string comparison on `approve()`, and defines seed card `automated-decision-safeguard` | High       | Direct read        |
| C5  | `src/core/src/zava_forward/core/rule_engine.py:390-487`                        | Code search   | Persists `offline_usage("regulatory-check", ...)` in `reg_check.usage_json` and checks `"rule_owner" in actor.get("rule_roles", [])` in `disposition()` without verifying `trusted-proxy` identity claims or `view_only` | High       | Direct read        |
| C6  | `src/core/src/zava_forward/core/identity.py:1-63`                              | Code search   | Provides fully typed `verified(user)`, `same_owner(owner, user)`, and `distinct(first, second)` comparing Entra `oid`/`tid` across email aliases         | High       | Direct read        |
| C7  | `src/core/tests/test_regulatory_privacy.py:1-230`                              | Code search   | Asserts exact `set(QUERY_FIELDS) == {"rule_lookup", "check_explain", "alert_triage"}` and existing signatures/exceptions for `minimise_query`, `record_human_decision`, and `metering_record` | High       | Direct read        |
| C8  | `src/api/src/zava_forward/api/auth.py:18-100` & `infra/entra/app-registration.json:25-31` | Code search | Declares the three separate Entra `capabilityRoles` (`ZavaForward.RuleAuthor -> rule_author`, `ZavaForward.RuleOwner -> rule_owner`, `ZavaForward.RegulatoryChat -> regulatory_chat`) and `ApplicationAdmin` `view_only` isolation | High       | Direct read        |
| C9  | `src/core/src/zava_forward/core/lawstore.py:141-215`                           | Code search   | Establishes SQLite `BEFORE UPDATE`/`BEFORE DELETE` `RAISE(ABORT, ...)` triggers and MSSQL append-only ledger/trigger pattern for immutable regulatory records | High       | Direct read        |
| C10 | `src/api/tests/test_regulatory_chat_api.py:203-245`                            | Code search   | Confirms HTTP tests expect `"RegulatoryChat capability"` denial when `rule_roles` only has `["rule_author", "rule_owner"]` and 200 when `["regulatory_chat"]` is assigned | High       | Direct read        |
| C11 | `src/core/pyproject.toml:35-108`                                               | Code search   | Enforces `mypy` `strict = true` and `ruff` line-length 100 (`E`, `F`, `I`, `B`, `UP`) on `regulatory_privacy.py`, `regulatory_usage.py`, and non-excluded test modules | High       | Direct read        |
| C12 | `docs/reference/research/chat-memory-dpia.md:1-120` & `src/core/src/zava_forward/core/{data_protection,projection,chat_privacy,controls}.py` | Code search | Defines existing special-category purpose controls (`projection.can_see_reason`, `HAZARD_ROLES`, `data_protection.dispatch_hold`, `chat_privacy.redact` `SENSITIVE` cues, `controls.is_memory_reference`, and `dpo_reviewed=False`) | High       | Direct read        |

### External Evidence

| ID | Source title | URL | Retrieval date | Version / date | Claim supported | Confidence |
|----|--------------|-----|----------------|----------------|-----------------|------------|

## Findings Mapped to Questions and Evidence

* **Q1 (Foundry query minimisation & special-category purpose controls)** (`C1`, `C3`, `C7`, `C12`):
  * Fact: `minimise_query` currently filters flat keys against `QUERY_FIELDS` and `SPECIAL_CATEGORY`, but does not enforce scalar/length bounds, does not exclude optional fields unneeded for a specific question (for example, provision-only vs hazard vs automated-decision home questions), does not redact/block special-category free-text cues (`chat_privacy.SENSITIVE`), and does not verify `projection` (`allowed(user, "chat")`, `can_see_reason(user)`, `HAZARD_ROLES`) or `data_protection.dispatch_hold` purpose controls.
  * Finding: Retaining `QUERY_FIELDS` unchanged (`C7`) while hardening `minimise_query` scalar/cue validation, adding `check_special_category_purpose` + question-scoped `build_foundry_query`, and exposing `RegulatoryChat.foundry_query(user, cid, question)` guarantees Foundry queries exclude every field not needed for the question and enforce existing special-category purpose controls.
* **Q2 (Separate Entra roles for authors, approvers, and chat users)** (`C3`, `C4`, `C5`, `C6`, `C8`, `C10`):
  * Fact: Entra role mapping (`ZavaForward.RuleAuthor`, `ZavaForward.RuleOwner`, `ZavaForward.RegulatoryChat`) previously lived only in `src/api/auth.py` and `infra/entra/app-registration.json`, leaving `src/core` without a canonical Entra role-separation verifier and leaving `RegulatoryChat.admit()` and `RuleEngine.disposition()` with incomplete `trusted-proxy` role/identity enforcement.
  * Finding: Defining canonical Entra role mapping, capability isolation (`rule_author`, `rule_owner`, `regulatory_chat` mutually non-implying; `ApplicationAdmin` / `view_only` granting none; unverified/password principals denied Entra capabilities), and alias-proof `identity.distinct` separation-of-duties in `regulatory_privacy.py`—and enforcing it in `RegulatoryChat.admit()`, `RuleEngine.disposition()`, and `ConsequentialDecisionGuard`—delivers full Entra 3-role separation in `src/core`.
* **Q3 (UK GDPR Art 22A-22C guard: propose/flag + retained named human with reasons)** (`C1`, `C4`, `C6`, `C9`, `C12`):
  * Fact: `record_human_decision` (`C1`) is a stateless dict builder not wired to storage, proposal flagging, separation of duties, or memory-citation refusal (`src/core/README.md:4706`).
  * Finding: Hardening `record_human_decision` (blocking bot/placeholder deciders and `controls.is_memory_reference` reasons while supporting `"approver"` and `"rule_owner"`) and introducing `ConsequentialDecisionGuard` backed by append-only `LawStore` tables (`reg_consequential_proposal`, `reg_consequential_decision` with update/delete abort triggers per `C9`) plus metadata-only `store.audit` records ensures the system can only propose and flag while consequential actions require and durably retain a named, verified human approver with recorded reasons.
* **Q4 (Tokenomics: chat and check metering and cost records)** (`C1`, `C2`, `C5`, `C7`, `C12`):
  * Fact: `metering_record` (`C1`) allows arbitrary-length whitespace prose inside string fields and has no companion closed-schema `cost_record`; `regulatory_usage.py` (`C2`) handles only `chat` turns, not `reg_check` (`C5`), and lacks unified role-scoped access checks, retention-window filtering, and metadata-only audit logging across chat and checks.
  * Finding: Tightening identifier/version lexical bounds in `metering_record`, adding closed-schema `COST_FIELDS` + `cost_record` (`cost="Unknown"` when unpriced per OD-51), projecting both `chat` turns and `reg_check` rows into identifier/count/version-only metering and cost records, and governing reads/writes through a role-scoped, retention-aligned, audited `governed_usage_records` / `RegulatoryMeteringService` in `regulatory_usage.py` satisfies every element of Criterion 4.
* **Q5 (Typing, linting, and targeted validation)** (`C7`, `C11`):
  * Fact: `mypy` runs in strict mode across `src` and `tests`, `ruff` enforces 100-char lines and `E/F/I/B/UP`, and the required test command discovers `-p 'test_*217*.py'`.
  * Finding: All new and modified code in `regulatory_privacy.py`, `regulatory_usage.py`, `regulatory_chat.py`, `rule_engine.py`, and `tests/test_regulatory_privacy_audit_217.py` will use complete strict type annotations and typed `Protocol` boundaries without modifying `pyproject.toml`.

## Key Discoveries

* `test_regulatory_privacy.py:143` pins `set(QUERY_FIELDS) == {"rule_lookup", "check_explain", "alert_triage"}` (`C7`); preserving `QUERY_FIELDS` keys while adding question-scoped narrowing prevents regressions in existing suites.
* `RegulatoryChat.admit()` (`C3`) verified Entra claims (`identity.verified`) for `trusted-proxy` principals on chat entry, whereas only `_owner()` and `src/api/server.py` checked `"regulatory_chat" in user.get("rule_roles", [])`.
* `metering_record` (`C1`) validated `isinstance(value, str) and value.strip()` on identifier fields without rejecting multiline or whitespace-laden prose, meaning raw chat/source sentences could previously be smuggled inside `record_id` or `source_version` unless lexical identifier bounds are enforced.
* `RuleEngine.evaluate` (`C5`) already writes `offline_usage("regulatory-check", ...)` into `reg_check.usage_json`, providing an existing deterministic SQL source for check metering and cost projection alongside chat turn metadata.

## Alternatives and Decision State

### Option A: Extend `regulatory_privacy.py` and `regulatory_usage.py` in place and wire `regulatory_chat.py` and `rule_engine.py` (Selected)

* Summary: Keep regulatory privacy, Entra 3-role separation, Art 22A-22C append-only proposal/decision retention, and closed-schema metering/cost contracts in `regulatory_privacy.py` and `regulatory_usage.py`, and wire `RegulatoryChat` (`admit` + `foundry_query`) and `RuleEngine.disposition` to use them.
* Benefits: Preserves existing module boundaries documented in `src/core/README.md`, maintains 100% backwards compatibility with existing imports, avoids module sprawl, and keeps all new surfaces under strict `mypy` and `ruff` checks (`C1`, `C2`, `C11`).
* Trade-offs: Requires typed `Protocol` definitions in `regulatory_privacy.py` / `regulatory_usage.py` so calls into untyped `LawStore`, `Store`, `projection`, `chat_privacy`, and `controls` pass `mypy --strict` cleanly.
* Supporting evidence: `C1`, `C2`, `C3`, `C5`, `C9`, `C11`.

### Option B: Create separate standalone subpackages without wiring `RegulatoryChat`, `LawStore`, or `RuleEngine`

* Summary: Add isolated helper classes in new modules without integrating `LawStore` append-only SQL triggers, `RegulatoryChat`, or `reg_check` usage records.
* Benefits: Slightly smaller diff in existing files.
* Trade-offs: Repeats the exact gap flagged in `src/core/README.md:4706` ("pure builder and is not wired to storage or an approval flow") and leaves `RegulatoryChat.admit()` and `reg_check` metering unconnected.
* Why not selected: Fails completeness and leaves real `src/core` seams unguarded.

## Open Questions, Risks, and Residual Uncertainty

* Open external/human items (outside `src/core` local scope, preserved honestly):
  * Human DPO review and sign-off of `docs/reference/research/chat-memory-dpia.md` (`dpo_reviewed` remains `False`).
  * Named Legal/DPO applicability decision on UK GDPR Articles 22A-22C in `docs/reference/regulatory/reviewed-updates/2026-11-01-adm-ai-act-applicability-review.md` (#224) and seed-card citation update (#211).
  * Live Azure Entra tenant role-assignment and Foundry runtime verification (#217, #358).
* Engineering risks mitigated in plan:
  * Strict `mypy` `disallow_untyped_calls` across legacy untyped `src/core` helpers -> mitigated via explicit `typing.Protocol` interfaces and typed wrappers.
  * SQLite append-only immutability -> verified directly via `UPDATE`/`DELETE` trigger tests in `test_regulatory_privacy_audit_217.py`.

## Current Decisions

| Decision                                                                                                         | Status    | Owner / source | Rationale                                                                                  | Evidence          | Implications                                                                                  |
|------------------------------------------------------------------------------------------------------------------|-----------|----------------|--------------------------------------------------------------------------------------------|-------------------|-----------------------------------------------------------------------------------------------|
| Select Option A: in-place hardening of `regulatory_privacy.py` and `regulatory_usage.py` wired to `regulatory_chat.py`, `rule_engine.py`, and `LawStore` | confirmed | evidence       | Delivers complete, durable, end-to-end `src/core` controls without module sprawl           | C1, C2, C3, C5, C9 | `rpi-plan` structures 4 cohesive implementation phases + tests + `src/core/README.md` update |
| Preserve `QUERY_FIELDS` and `METERING_FIELDS` existing key sets while adding `build_foundry_query`, lexical identifier bounds, and `COST_FIELDS`/`cost_record` | confirmed | evidence       | Protects backwards compatibility with `test_regulatory_privacy.py` while closing smuggling gaps | C1, C7            | Zero regressions for existing callers in `src/core` and `src/api`                             |
| Keep `dpo_reviewed=False`, `cost="Unknown"` when unpriced (OD-51), and commit reference as `Refs #217`          | confirmed | constraint     | Repository honesty and regulatory/tokenomics non-inference rules                           | C1, C2, C12       | Code, README, and commit accurately distinguish delivered local controls from human/live gates |

## Unresolved Decisions

| Decision                                                       | Smallest missing evidence or answer                     | Owner            | Impact                                           | Blocking? |
|----------------------------------------------------------------|---------------------------------------------------------|------------------|--------------------------------------------------|-----------|
| Human DPO DPIA approval and Art 22A-22C Legal decision (#224)  | Signed Legal/DPO review record                          | Named DPO/Legal  | Required before live personal-data processing    | No (out of local `src/core` scope; guarded fail-closed) |

## Potential Next Research

| # | Area                                              | Priority | Expected value                                                | Trigger to pursue                             | Selected |
|---|---------------------------------------------------|----------|---------------------------------------------------------------|-----------------------------------------------|----------|
| 1 | Live Entra app-role assignment & Foundry E2E probe | M        | Closes hosted/live verification criteria on Issue #217        | Live Azure tenant + Foundry environment ready | no       |

## Planning Readiness

* Research disposition: `executed`
* Status: `Ready`
* Basis: All four Issue #217 local `src/core` engineering criteria have been mapped to exact files, line numbers, invariants, SQLite/MSSQL append-only storage patterns, strict typing constraints, and targeted validation commands (`C1`-`C12`).
* Continuation: Active confirmed automatic RPI Agent continues directly to `rpi-plan` without waiting for a manual command; pre-transition state write recorded at `.copilot-tracking/rpi-sessions/2026-11-14/217-regulatory-privacy-audit-2305-state.json`.
* Speculation label: Facts above cite `C1`-`C12`; design choices in Option A are explicitly labelled as engineering recommendations for `rpi-plan`.

## Self-Check

* [x] Research brief, output mode (`convergence`), scope, non-goals, and criteria are recorded.
* [x] Extension Registry and User Participation no-interaction rationale are recorded.
* [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order with reflections and parent synthesis.
* [x] Every question Q1-Q5 is answered and mapped to canonical `C1`-`C12` `path:line` evidence.
* [x] Alternatives compared with selected recommendation and rejection rationale.
* [x] Research remained strictly read-only on repository source files; untrusted repository content was treated as inert data; no secrets were recorded.

## Sources

No external sources used
