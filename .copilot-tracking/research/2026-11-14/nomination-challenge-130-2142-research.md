---
title: "Task Research: nomination-challenge-130-2142"
description: "Three-wave RPI research for Issue 130 locally verifiable nomination, acknowledgement, challenge, dependent re-review, and immediate hazard intake controls in src/core"
ms.date: 2026-11-14
---

## Research Brief

* Topic: Deliver the remaining locally verifiable acceptance criteria of Issue #130 (Nomination, self-referral, acknowledgement and challenge route; `FR-037`, `AC-065`, `RULE-005`) in `src/core` on branch `feat/safety-130-nomination-challenge-2142`.
* Purpose: Establish exact codebase evidence, contrarian edge cases, store parity (`Store` and `SqlStore`), and verification constraints before planning and implementing changes in `src/core`.
* Audience: RPI planning, implementation, and post-implementation review phases, plus independent PR review.
* Output mode: `convergence`.

## Research Parameters

* Posture: `focused` (bounded internal task in `src/core` with explicit acceptance criteria, named verification command, and pre-existing uncommitted draft edits in the worktree).
* Provenance: User prompt specifying all four target acceptance criteria, full four-phase RPI execution, bare `mypy`/`ruff`/`unittest discover` verification in `src/core`, and local commit without push.
* Resolved evidence root: `.copilot-tracking/research/2026-11-14/nomination-challenge-130-2142-research.md`.

## Extension Registry and Provenance

* Repository instructions (`.github/copilot-instructions.md`): selected; governs problem specification boundaries, human-approval and non-inference controls, Markdown style, validation tiering, privacy-safe Git identity, and `Refs #130` issue linking.
* `rpi-research`: selected; enforces read-only investigation, three-wave research cycle (`Wider`, `Deeper`, `Contrarian`), `C#` `path:line` citations, and planning readiness gating.
* Web UI skills (`design-taste-frontend`, `web-design-guidelines`, `redesign-existing-projects`): skipped; task scope is strictly backend domain logic and tests in `src/core`.
* Delegated `RPI Researcher` subagents: skipped inline fallback; bounded five-file `src/core` trace fits direct inspection with zero context pressure.

## User Participation and Research Decisions

* Non-interactive autonomous CLI run explicitly instructing automatic execution of Research, Plan, Implement, and Review in order. No blocking `vscode_askQuestions` prompt is available or needed because scope, target directory (`src/core`), verification command, and commit boundary are unambiguous.

## Scope and Success Criteria

* In scope (`src/core` locally verifiable criteria for Issue #130):
  1. Each referral has an acknowledged route and a named owner before review.
  2. A resident or representative can raise a challenge or correction; competing evidence, reviewer, and outcome are retained.
  3. A correction triggers re-review of dependent decisions without automatic acceptance or sanction.
  4. Emergency or hazard concerns route to the independent hazard intake (#85) immediately, not through this queue.
* Out of scope (remain open on Issue #130, requiring `Refs #130` rather than a closing keyword):
  * Owner/governance ratification of `OD-41` and `OD-42`.
  * Live UI authoring screens in `src/api` and human representative comprehension testing.

## Task Research Requests

* Audit existing Issue #130 slices on `HEAD` (`e9c595e8b` / PR #1710 and earlier slices) alongside uncommitted worktree drafts in `nomination_route.py`, `resident_decisions.py`, `test_nomination_route.py`, and `test_resident_decisions.py`.
* Verify how `Store` (JSON) and `SqlStore` (SQLite) persist and project `nomination_records`, `affected_challenges`, `representative_authorities`, `recommendations`, and `hazards`.
* Diagnose why the mandatory bare verification selector `python3 -m unittest discover -s tests -p 'test_*nomination*.py' -v` fails in this worktree and identify a clean, strict-typed, worktree-isolated fix.

## Direction Controls

* Preserve existing `Store` and `SqlStore` schemas (`cases.body` JSON document) without altering SQL DDL or migrations in `sqlstore.py` or `mssqlstore.py`.
* Do not modify shared user-site Python packages (`/home/azureuser/.local/lib/python3.12/site-packages`), which are shared across concurrent worktrees.
* Preserve all existing resident decision invariants (`test_resident_decisions.py`, `test_challenges.py`, `test_hazard_referral.py`, `test_taskqueues.py`).

## Research Questions

* Q1: How are pre-review prerequisites (named owner, staff-recorded acknowledgement, staffed non-digital route) currently enforced and surfaced, and can an unacknowledged/legacy referral complete those prerequisites before review?
* Q2: Can both a resident and a confirmed representative (`Communicate` authority) raise both a nomination correction and a formal challenge, while retaining competing evidence, challenged reviewer, and review outcome?
* Q3: How does a correction trigger human re-review across both nomination reviews and transitive dependent decisions (`ChallengeRegister`) while preserving prior versions, leaving unrelated decisions untouched, and preventing automatic acceptance or sanction?
* Q4: Do all nomination and challenge actions route emergency or unknown (`None` or non-`False`) hazard concerns immediately to the independent hazard intake (#85) without creating queue items or mutating state?
* Q5: Why does bare `python3 -m unittest discover -s tests -p 'test_*nomination*.py' -v` fail, and how can `test_*nomination*.py` exercise both pure domain helpers and `Store`/`SqlStore` end-to-end under strict `mypy` and `ruff`?

## Prior Knowledge Gate

* Reviewed `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/memory.md`, BRD (`FR-037`, `AC-065`, `RULE-005`, `OD-41`, `OD-42`), PRD (`FR-037`, `FR-043`, `FR-052`, `AC-071`), Customer Journey Atlas (`O01`, `O02`), Issue #130, Issue #85, and `.copilot-tracking/research/2026-11-14-issue-130-challenge-route-research.md`.

## Research Cycle Log

### Cycle 1

* Wider wave: Mapped nomination, challenge, hazard, queue, and SQL persistence touchpoints across `nomination_route.py`, `resident_decisions.py`, `challenges.py`, `taskqueues.py`, `store.py`, `sqlstore.py`, `projection.py`, and `ai_tasks.py`.
* Deeper wave: Traced exact field validation, exception types, projection boundaries, `authority_for` representative checks, `ChallengeRegister.dependents`, and `pyproject.toml` strict `mypy`/`ruff` rules.
* Contrarian wave: Tested pre-existing worktree drafts against adversarial inputs and bare `unittest discover`, uncovering five concrete defects and coverage gaps (`D1` through `D5` below).
* Re-entry check: All five questions have verified file-and-line evidence; no further research cycle is needed.

## Evidence Log

### Codebase Evidence

* `C1` (`src/core/src/zava_forward/core/nomination_route.py:31-51`): Uncommitted draft defines `missing_before_review` and `require_ready_for_review`, checking `owner.get("name")`, `ack.get("reference")`, and `record.get("non_digital_route")`, but uses raw truthiness so whitespace-only strings (`"   "`) or role-label-only owners pass erroneously.
* `C2` (`src/core/src/zava_forward/core/resident_decisions.py:514-563`): `nomination_follow_up` duplicates missing-prerequisite logic inline instead of delegating to `nomination_route.missing_before_review`, risking read/write readiness drift.
* `C3` (`src/core/src/zava_forward/core/resident_decisions.py:1219-1312`): `_res_nomination_record` records `owner`, `acknowledgement`, and `non_digital_route` on creation and `_res_nomination_review` gates review via `nomination_route.require_ready_for_review(record)`, but there is no `nomination_acknowledge` action to attach a named owner and acknowledged route to an unready/imported referral before review, and `_res_nomination_review` does not verify `_identity_status(record.get("owner")) == "Known"`.
* `C4` (`src/core/src/zava_forward/core/resident_decisions.py:240-255` and `src/core/src/zava_forward/core/nomination_route.py:22-28`): `HazardRouted` and hazard route metadata are duplicated across `resident_decisions.py` and `nomination_route.py`. Worse, `_refuse_hazard` (`resident_decisions.py:252-255`) checks `if flag is not None and flag is not False`, so an explicit `hazard_concern=None` (unknown) passed to `nomination_correct` or `challenge_open` silently bypasses `#85` routing, contradicting `nomination_route.hazard_routing(None)` (`nomination_route.py:54-60`).
* `C5` (`src/core/src/zava_forward/core/resident_decisions.py:1281-1312`): `_res_nomination_review` does not split optional `hazard_concern`, so a hazard spotted at review time raises a generic field-set `ValueError` instead of routing immediately via `HazardRouted` to `#85`.
* `C6` (`src/core/src/zava_forward/core/resident_decisions.py:257-270` and `1020-1035`): `_raiser` validates `Resident`, `Representative`, and `Officer` for `nomination_correct`, but looks up `c["representative_authorities"][ref]` before stripping whitespace on `ref`, and checks only `versions[-1]` rather than searching the representative's latest authority per case measure when multiple measures exist.
* `C7` (`src/core/src/zava_forward/core/resident_decisions.py:1590-1625`): `_res_challenge_open` only splits optional `("hazard_concern",)` and rejects `raised_by` and `representative_ref`, preventing a resident or confirmed representative from being explicitly recorded as the raiser on `challenge_open`.
* `C8` (`src/core/src/zava_forward/core/nomination_route.py:63-95` and `src/core/src/zava_forward/core/challenges.py:143-155`): `ChallengeRegister.dependents` computes transitive dependents via BFS without mutating unrelated nodes. `nomination_route.challenge_trail` omits `representative_ref`, `channel`, and `challenged_review` on `competing_evidence` and `rationale`/`evidence_ref` on `reviews`; `nomination_route.re_review_set` collects `record_version` without bounding to `<= corrected_version` and is not connected to optional `dependencies` in `_res_nomination_correct`.
* `C9` (`src/core/tests/test_resident_decisions.py:293-296` and `381-389`): Existing regression tests assert that `_res_nomination_correct` mutates no case fields outside `nomination_records` and that `correction["re_review"]` equals `{"required": True, "automatic_acceptance": False, "automatic_sanction": False, "dependent_review_versions": [1]}` when no graph dependencies are passed.
* `C10` (`src/core/src/zava_forward/core/workflows.py:18-45` and `src/core/src/zava_forward/core/taskqueues.py:155-182`): Independent hazard intake (#85) runs through `store.raise_hazard`, immediately recording a hazard with an active retrofit hold, whereas `taskqueues` projects `nomination_records` follow-up items only when a nomination record is persisted. Raising `HazardRouted` inside `_operation` rolls back before persistence and creates zero nomination queue items or audit entries.
* `C11` (`src/core/pyproject.toml:34-67`): `mypy` runs with `strict = true` over `files = ["src", "tests"]` (`resident_decisions` has a legacy override, while `nomination_route.py` and `test_nomination_route.py` are strictly checked); `ruff` enforces `line-length = 100` and `select = ["E", "F", "I", "B", "UP"]`.
* `C12` (`src/core/tests/test_nomination_route.py:1-74`): Running bare `python3 -m unittest discover -s tests -p 'test_*nomination*.py' -v` from `src/core` fails with `ImportError` because shared user-site `zava-forward-core` resolves `zava_forward.core` to `/home/azureuser/source/ama/src/core/src`. Additionally, `test_nomination_route.py` is the only file matched by `'test_*nomination*.py'` and currently tests only four synthetic dictionary calls rather than `Store` and `SqlStore` workflows.

### External Evidence

* None required; all specifications, regulatory snapshots, and code contracts reside inside the repository.

### Contradictions / Conflicts

* `nomination_route.hazard_routing(None)` (`C4`) treats `None` (unknown hazard status) as requiring immediate `#85` hazard routing, whereas `_refuse_hazard` in `resident_decisions.py:252-255` ignored explicit `hazard_concern=None` on `nomination_correct` and `challenge_open`. Resolved in favor of fail-closed `#85` routing whenever `"hazard_concern"` is supplied and is not `False`.

## Findings Mapped to Questions and Evidence

* Q1 (`C1`, `C2`, `C3`): Harden `nomination_route.missing_before_review` to reject blank/whitespace strings and bare role-label owners, reuse it inside `nomination_follow_up`, enforce known named-owner identity in `_res_nomination_review`, and add `nomination_acknowledge` so an unready/legacy referral can be assigned a named owner, staff-recorded acknowledgement, and staffed non-digital route before review.
* Q2 (`C6`, `C7`, `C8`): Fix `_raiser` to strip `representative_ref` and check confirmed in-date `Communicate` authority across the representative's recorded case-measure authorities; support optional `raised_by` and `representative_ref` in `_res_challenge_open` as well as `_res_nomination_correct`; enrich `nomination_route.challenge_trail` (retaining `representative_ref`, `channel`, `challenged_review`, `evidence_ref`, `rationale`, `reviewer`, `outcome`, and `stale_from_version`) and surface it via `followup_view`.
* Q3 (`C8`, `C9`): Bound `dependent_review_versions` to reviews up to the corrected version, support optional `dependencies` in `_res_nomination_correct` backed by `nomination_route.re_review_set` (preserving exact existing `re_review` keys when `dependencies` is omitted per `C9`, and recording transitive `dependents` while preserving prior versions and unrelated decisions when supplied), and verify `priority_challenge_state` + `nomination_correct` leave priority, consent, unrelated proposals/decisions, and prior versions intact with `automatic_acceptance=False` and `automatic_sanction=False`.
* Q4 (`C4`, `C5`, `C10`): Consolidate `HazardRouted` and `HAZARD_ROUTING_MESSAGE` in `nomination_route.py` (re-exported by `resident_decisions.py`), route any supplied `hazard_concern is not False` (including explicit `None`) across `nomination_record`, `nomination_acknowledge`, `nomination_review`, `nomination_correct`, and `challenge_open` immediately to `#85` (`raise_hazard`) with zero queue items or state mutations.
* Q5 (`C11`, `C12`): Prepend worktree `src/core/src`, `src/core/tests`, and `src/agents/src` to `sys.path` and clear cached `zava_forward*` modules at top of `tests/test_nomination_route.py` (with `# noqa: E402` for `ruff` and static imports for `mypy --strict`), assert worktree module origin, and test both pure `nomination_route` helpers and full `Store` + `SqlStore` end-to-end flows under `'test_*nomination*.py'`.

## Key Discoveries

* `D1`: Bare `unittest discover` loads `/home/azureuser/source/ama/src/core/src` from shared `.local` site-packages unless `tests/test_nomination_route.py` bootstraps this worktree's `src` onto `sys.path` and evicts preloaded `zava_forward` namespace entries (`C12`).
* `D2`: Explicit `hazard_concern=None` in `nomination_correct` and `challenge_open` bypassed `_refuse_hazard` (`C4`), and `nomination_review` lacked `hazard_concern` routing altogether (`C5`).
* `D3`: `_res_challenge_open` rejected `raised_by` and `representative_ref` (`C7`), and `_raiser` failed to strip `representative_ref` before lookup (`C6`).
* `D4`: Whitespace-only strings satisfied `missing_before_review` (`C1`), and unacknowledged legacy referrals had no `nomination_acknowledge` action to become review-ready (`C3`).
* `D5`: `_res_nomination_correct` has strict regression invariants on case keys and default `re_review` dict shape (`C9`) that must be preserved when integrating `nomination_route.re_review_set`.

## Alternatives and Decision State

### Selected Recommendation

* Refine `src/core/src/zava_forward/core/nomination_route.py` as the single typed domain rule module (owning `HazardRouted`, `HAZARD_ROUTING_MESSAGE`, `missing_before_review`, `require_ready_for_review`, `hazard_routing`, `challenge_trail`, and `re_review_set`), wire `resident_decisions.py` to delegate to it across `nomination_record`, `nomination_acknowledge`, `nomination_review`, `nomination_correct`, `challenge_open`, and `followup_view`, and expand `tests/test_nomination_route.py` + `tests/test_resident_decisions.py` to verify both pure rules and JSON/SQLite store persistence under bare `unittest discover`.

### Alternative: Editable `pip install -e .` in user site-packages

* Rejected: Mutating shared `/home/azureuser/.local/lib/python3.12/site-packages` in a multi-worktree environment would break sibling worktrees and make test isolation depend on ambient global state.

### Alternative: Add SQL columns or tables for nomination dependency edges

* Rejected: `Store` and `SqlStore` already persist `nomination_records` and `affected_challenges` transactionally inside `cases.body` with optimistic `rowversion` concurrency; altering SQL DDL would widen scope to live SQL Server infrastructure gates without adding domain safety.

## Open Questions, Risks, and Residual Uncertainty

* Governance decisions `OD-41` and `OD-42` and UI authoring workflows remain open outside `src/core`; commits must reference `Refs #130` and never claim whole-issue closure.

## Current Decisions

* Keep SQL schema unchanged; deliver all four criteria cleanly in `nomination_route.py` and `resident_decisions.py` with full `Store` and `SqlStore` test parity.
* Bootstrap worktree paths inside `tests/test_nomination_route.py` without touching shared site-packages.

## Unresolved Decisions

* `OD-41` and `OD-42` remain human governance decisions outside this `src/core` slice.

## Potential Next Research

* Follow-on UI authoring forms in `src/api` for `nomination_record`, `nomination_acknowledge`, `nomination_correct`, and `nomination_review` once `src/core` controls land.

## Planning Readiness

* Planning Readiness: `Ready`
* Research disposition: `executed`

## Closeout Record

* Research completed in read-only mode with zero source edits during Research; all four acceptance criteria and the bare verification harness are mapped to `C1`..`C12`.

## Advisory Next Step

* Advance automatically to `rpi-plan` using `.copilot-tracking/research/2026-11-14/nomination-challenge-130-2142-research.md`.

## Sources

* `docs/case_study_48_original.md`
* `docs/case_study_48_addendum.md`
* `docs/brd/business-requirements.md` (`FR-037`, `AC-065`, `RULE-005`, `OD-41`, `OD-42`)
* `docs/prd/product-requirements.md` (`FR-037`, `FR-043`, `FR-052`, `AC-071`)
* `docs/journeys/customer-journey-atlas.md` (`O01`, `O02`)
* `src/core/src/zava_forward/core/nomination_route.py`
* `src/core/src/zava_forward/core/resident_decisions.py`
* `src/core/src/zava_forward/core/challenges.py`
* `src/core/tests/test_nomination_route.py`
* `src/core/tests/test_resident_decisions.py`

## Artifact Self-Check

* Complete 3-wave cycle (`Wider`, `Deeper`, `Contrarian`) recorded: Yes.
* Stable `C#` codebase evidence IDs with `path:line`: Yes (`C1`..`C12`).
* No source files edited during Research: Yes.
* Planning Readiness and Research disposition recorded: Yes (`Ready`, `executed`).
