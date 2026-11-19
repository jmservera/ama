---
title: "Meaningful Human-Review Effectiveness Gate and Automation-Bias Harness in Core (#223)"
description: "Primary RPI research artifact for delivering Issue #223 locally verifiable engineering criteria in src/core"
ms.date: 2026-11-14
---

## Research Brief

* Topic: Meaningful human-review effectiveness gate, workflow-only comparator harness, and automation-bias evaluation in `src/core` for GitHub Issue #223.
* Purpose: Establish exact specification, `src/core` integration seams, strict typing constraints, and privacy/provenance boundaries before planning and implementing Issue #223 in `src/core`.
* Audience and use: Automatic RPI session (`task_id`: `223-human-review-effectiveness-2305`, `task_slug`: `human-review-effectiveness-223-2305`) targeting branch `feat/ai-223-human-review-effectiveness-2305` (parent branch `feat/demo-164-chat-grounding-provenance-0900`).
* Output mode: `convergence` (supports planning handoff).
* Research posture: `focused` (bounded internal engineering slice with named target package `src/core`, explicit acceptance criteria, and specified validation commands).
* Explicit limits and non-goals:
  * Deliver locally verifiable engineering criteria in `src/core` without modifying `pyproject.toml`, workflow YAML, or `src/agents`.
  * Validate strictly with `mypy`, `ruff check .`, `ruff format --check .`, and `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*223*.py' -v` (never run full unfiltered `unittest discover -s tests`).
  * Keep real human reviewer trials, measured participant effort, owner-approved oversight thresholds, and `OQ-017` authority appointments explicitly open (`Refs #223`, never `Closes #223`).
* No-interaction rationale: Running in non-interactive automatic RPI mode with complete caller scope and repository evidence.

## Extension and Instruction Provenance

* Selected instructions:
  * `.github/copilot-instructions.md` (`applyTo: "**"`): governs problem specification boundaries, `OQ-017` human-authority non-fabrication, `Refs #223` issue-linking semantics, Markdown style, and branch/commit rules.
* Selected skills:
  * `rpi-research`: governs three-wave research execution (Wider, Deeper, Contrarian), `C#` evidence mapping, and read-only boundary.
* Skipped skills and specialists:
  * Web/UI design skills (`design-taste-frontend`, `web-design-guidelines`, `accessibility`): skipped because this slice is pure `src/core` Python domain/gate logic with zero web UI edits.
  * Delegated `RPI Researcher` subagents: skipped in favour of inline investigation because all target files reside in `src/core`, `src/agents`, and `docs/` and fit within direct reads.

## Candidate Questions

1. Q1: What exact requirements do Issue #223, `AC-070`, `FR-026`, `FR-027`, `NFR-009`, `OQ-017`, and the Responsible AI release position place on human-review effectiveness?
2. Q2: What already exists in `src/core` versus `src/agents`, and how do `Store.ai_run`, `Store.review_ai`, `gates.GateResult`, `rai_release`, and `controls` interact?
3. Q3: What contrarian failure modes, bypasses, strict-typing traps, or synthetic-data privacy checks could break `src/core` or allow defective proposals to satisfy a controlled gate?

## Cycle 1 Execution

### Wave 1: Wider

* Reviewed Issue #223, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, and `docs/reference/research/rai/project-rai-review.md` (`C1`, `C2`).
* Surveyed `src/core/src/zava_forward/core/` modules (`ai_tasks.py`, `store.py`, `gates.py`, `rai_release.py`, `controls.py`, `cohort_eval.py`, `paired_equity.py`) and `src/agents/src/zava_forward/agents/review_effectiveness.py` (`C3`–`C6`).
* Confirmed that while `src/agents` contains an offline script (`review_effectiveness.py`) and golden JSON (`src/agents/evals/review_effectiveness_golden.json`), `src/core` currently has no `human_review_effectiveness` gate module and zero `*223*` tests (`C6`).

### Wave 2: Deeper

* Inspected `Store.ai_run` (`src/core/src/zava_forward/core/store.py:861-895`) and `ai_tasks.finish` / `ai_tasks.review` (`src/core/src/zava_forward/core/ai_tasks.py:58-135,335-465`) (`C3`, `C4`):
  * `Store.ai_run(user, case_id, task, mode="workflow")` produces the deterministic workflow-only comparator (`mode == "workflow"`) with exact case `source_labels`, `source_hashes`, and `statement_sources` verification (`verified: bool`).
  * `Store.review_ai(user, rec_id, disposition, text=..., reason=...)` records `status`, `resolved_by`, `reviewer_reason`, `final_text`, and structured `review_evidence` (`reviewer`, `disposition`, `reason`, `compared` with `ai_text` vs `workflow_text`, `source_hashes` snapshot, `case_version`, and `effect`), and already detects post-draft case mutations when `source_hashes` change (`stale_sources`).
  * Crucially, `Store.review_ai` only checks basic input presence (`accept` needs no `reason`; `verified=True` only checks that `[[...]]` tokens match `source_labels` keys, not whether the prose states the opposite of the cited source, omits safety/adjustment facts, cites an older superseded note while ignoring a newer case state, or adds unsupported promises).
* Inspected `gates.py` (`src/core/src/zava_forward/core/gates.py:1-130`), `rai_release.py` (`src/core/src/zava_forward/core/rai_release.py:21-75`), and `controls.py` (`src/core/src/zava_forward/core/controls.py:49-60`) (`C5`):
  * `GateResult(gate, status, reasons, missing_authority)` with `PASS`, `FAIL`, `UNKNOWN` and `transition_allowed(...)` is the canonical `src/core` gate contract.
  * `rai_release.named_human(...)` rejects blank, placeholder (`TBD`, `pending`, `unassigned`), and system/agent (`assistant`, `copilot`, `system`, `bot`, `agent`, `workflow`, `automation`, `model`, `ai`) identities.
  * `controls.is_memory_reference(...)` detects unverified chat/assistant memory references (`"earlier in chat"`, `"the assistant said"`, etc.) that must never count as authoritative case source checks.

### Wave 3: Contrarian

* Contrarian check 1 — Public JSON dataset registration trap (`C7`):
  * `src/core/src/zava_forward/core/synthetic/privacy.py:175-215` and `src/core/tests/test_synthetic_provenance.py:333-345` enforce that every JSON/CSV file placed under `src/*/evals/` must be registered in `provenance-register.json` and pass synthetic label and email-pattern checks, AND `src/core/pyproject.toml:85-86` only packages `policies/*.json`, `law/*.json`, and `resident-demo.json` into built wheels.
  * Counter-design: Keep the canonical synthetic multi-scenario specification immutable in Python dataclasses/mappings inside `zava_forward.core.human_review_effectiveness` (matching `paired_equity.py` and `cohort_eval.py`), while supporting JSON export/import for blank human worksheets and completed human answer sheets in caller-supplied paths (`tempfile` in tests). This avoids unregistered `evals/` drift, works identically in wheels and editable checkouts, and requires zero `pyproject.toml` or `provenance-register.json` edits.
* Contrarian check 2 — Strict `mypy` boundary with legacy untyped `Store` and `ai_tasks` (`C8`):
  * `src/core/pyproject.toml:25-65` runs `mypy` with `strict = true` across `src` and `tests`, exempting legacy `zava_forward.core.store` and `zava_forward.core.ai_tasks` via overrides. Calling untyped functions from a new strictly typed module raises `[no-untyped-call]`.
  * Counter-design: Encapsulate the narrow `Store` and `ai_tasks.source_labels` calls behind a small typed adapter boundary (`Store: Any = UntypedStore` / typed wrapper helpers, matching `src/core/tests/test_ai_consumption_safety.py:19-22`), keeping 100% strict type annotations across every public and private function in `human_review_effectiveness.py` and `test_human_review_effectiveness_223.py` without touching `pyproject.toml`.
* Contrarian check 3 — Superficial gate gaming & multi-task coverage:
  * A gate that only checks `disposition in ("edit", "reject")` could be bypassed by:
    1. Editing text cosmetically while leaving the wrong/unsupported claim intact or omitting a required hazard/accessibility fact (`ineffective_edit`).
    2. Rejecting or editing with a vague reason that cites no resolving case `source_labels` key, cites an unrelated source key not tied to the discrepancy, or cites chat memory (`controls.is_memory_reference`).
    3. Using an unauthorised staff role, a task-scope mismatch (e.g., reviewer authorised for `message` signing off `summary`), or an agent/system reviewer string.
    4. Mutating the underlying case after `ai_run` so `review_evidence.source_hashes` diverges from current case state (`stale_case_sources`).
    5. Passing `live=True` with provisional `OQ-017` authority lacking named-human `approved_by` and `approved_on`.
  * Also, testing only `summary` on one case leaves `message` untested; including workflow-paired scenarios across both `summary` and `message` tasks strengthens workflow-only comparator fidelity.

## Evidence Register

* `C1`: `docs/prds/zava-forward-retrofit-programme-demonstrator.md:489-490,1401-1403,1520-1523,2166,2941` — Defines `FR-026`, `FR-027`, `FR-028`, `NFR-009`, `AC-070`, and `OQ-017` for human-review dispositions, source citations, workflow-only comparators, review-effort capture, seeded defect classes (`wrong`, `stale`, `unsupported`, `incomplete` plus valid controls), and competent-review authority sign-off.
* `C2`: `docs/case_study_48_addendum.md:1005-1013` and `docs/reference/research/rai/project-rai-review.md:107-120` — Responsible AI Release Position (`F08`/`B06`): citation/schema validity is necessary but does not mitigate automation bias; default acceptance cannot satisfy controlled gates; human reviewer trials remain a pre-live governance blocker under `OQ-017`.
* `C3`: `src/core/src/zava_forward/core/store.py:50-85,861-895,1207-1209` — `Store` initialization, `Store.ai_run(user, case_id, task, mode=...)` supporting `"summary"` and `"message"` plus `mode="workflow"`, `Store.review_ai`, and `Store.verify_audit()`.
* `C4`: `src/core/src/zava_forward/core/ai_tasks.py:58-135,335-465` — `source_labels`, `source_hashes`, `statement_sources` (`verified: bool`), `finish`, and `review` stamping `review_evidence` (`reviewer`, `disposition`, `reason`, `compared`, `source_hashes`, `case_version`, `effect`).
* `C5`: `src/core/src/zava_forward/core/gates.py:1-130`, `src/core/src/zava_forward/core/rai_release.py:21-75`, and `src/core/src/zava_forward/core/controls.py:49-60` — `GateRule`, `GateResult` (`PASS`, `FAIL`, `UNKNOWN`), `transition_allowed`, `AUTHORITY_GAP`, `named_human`, and `is_memory_reference`.
* `C6`: `src/agents/src/zava_forward/agents/review_effectiveness.py:1-260` — Existing `src/agents` offline evaluation script for `#223`; confirms conceptual vocabulary (`wrong`, `stale`, `unsupported`, `incomplete`, `none`, reviewer panels, blank worksheet, session pooling) while showing `src/core` lacks an enforceable `GateResult` gate and core harness.
* `C7`: `src/core/src/zava_forward/core/synthetic/privacy.py:175-215` and `src/core/tests/test_synthetic_provenance.py:333-345` — Public `src/*/evals/` files must be registered in `provenance-register.json`; pure-Python embedded synthetic fixtures (`paired_equity.py:1-80`, `cohort_eval.py:1-80`) avoid unregistered dataset drift and wheel-packaging gaps.
* `C8`: `src/core/pyproject.toml:25-65` and `src/core/tests/test_ai_consumption_safety.py:19-22` — `mypy` runs with `strict = true` on `src` and `tests`; narrow typed wrappers around `UntypedStore` and `ai_tasks` satisfy strict typing without modifying `pyproject.toml`.

## Parent Synthesis and Decisions

* Selected approach (Accepted):
  1. Implement `src/core/src/zava_forward/core/human_review_effectiveness.py` with full `mypy --strict` typing and `gates.GateResult` integration (`GATE_ID = "human_review_effectiveness"`):
     * `AuthorityPolicy` and `PROVISIONAL_AUTHORITY` (`provisional=True`, `OQ-017` boundary, `approved_by=None`, `approved_on=None`; fails closed when `live=True` unless approved by a named human).
     * Canonical synthetic scenario pack covering all four `AC-070` critical defect classes (`wrong` / plausible-but-wrong, `stale`, `unsupported`, `incomplete`) plus hedged and confident valid controls (`none`) across both `summary` and `message` tasks on constructed synthetic cases, paired 1-to-1 against `Store.ai_run(..., mode="workflow")`.
     * `human_review_gate(...) -> GateResult` enforcing: reviewed status (`UNKNOWN` when unreviewed or missing authority policy), `live=True` `OQ-017` block (`FAIL` + `missing_authority`), named-human reviewer identity (`rai_release.named_human`), authorised reviewer role and task scope, current `source_hashes` match against live case (`stale_case_sources`), non-memory substantive `reviewer_reason` citing a resolving case `source_labels` key relevant to the scenario/discrepancy, explicit prohibition on relying on `verified=True` citation validity or default `accept` when critical discrepancies exist, and semantic verification of edited `final_text` (rejecting edits that retain wrong/stale/unsupported claims, omit required safety/accessibility facts, or introduce new unsupported promises).
     * Workflow-only comparison and automation-bias harness (`run_automation_bias_harness`, `evaluate_panel`, `blank_worksheet`, `score_human_session`, `pool_human_sessions`) testing `competent`, `default_accept`, `automation_bias` (accepting confident + citation-valid defective proposals while checking hedged proposals), `citation_only`, and `unauthorised_competent` panels against the exact same workflow-only scenarios (`Store.ai_run(..., mode="workflow")`), reporting overall and per-class detection, corrections, rejections, false rejects, retained `reviewer`/`source`/`reason` audit completeness (`Store.verify_audit()`), workflow effort, AI review effort, and effort delta, with `automation_bias_exposed=True` and `evidence_class="synthetic_harness_not_human_oversight_evidence"`.
  2. Add targeted unit test suite `src/core/tests/test_human_review_effectiveness_223.py` (matched by `-p 'test_*223*.py'`) covering every acceptance criterion, bypass attempt, staleness check, live `OQ-017` fail-closed gate, blank worksheet / human session scoring / duplicate session rejection, and `Store.verify_audit()` integrity.
  3. Document the core gate, automation-bias harness, and `OQ-017` human-trial boundary in `src/core/README.md`.
* Rejected alternatives:
  * Adding an unregistered JSON file under `src/core/evals/`: rejected because `privacy.public_issues` requires `provenance-register.json` registration (`C7`) and `pyproject.toml` excludes `evals/` from wheel package data.
  * Adding `[[tool.mypy.overrides]]` in `src/core/pyproject.toml`: rejected because typed boundary helpers satisfy `mypy --strict` cleanly while leaving manifest/gate configuration untouched (`C8`).
  * Relying on `rec["verified"]` or `disposition != "accept"` alone: rejected because citation-valid wrong/stale/incomplete proposals have `verified == True` and superficial edits can preserve the underlying defect (`C2`, `C4`).

## Risks and Unresolved Governance Items

* `OQ-017` remains open: reviewer role rules and 30-character minimum reason thresholds are provisional engineering defaults, not Sponsor/Programme/Safety/DPO/Assurance sign-off (`C1`, `C2`).
* Real human reviewer effectiveness and real human review effort cannot be claimed from scripted profiles; `evidence_class` and `human_trial_complete=False` explicitly prevent synthetic harness passes from masquerading as live `AC-070` closure.

## Readiness and Handoff

* Research execution status: Complete (Cycle 1 Wider, Deeper, and Contrarian waves finished; zero material evidence gaps remain for `src/core` planning).
* Research disposition: `executed`
* Planning Readiness: `Ready`
