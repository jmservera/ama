<!-- markdownlint-disable-file -->

# Task Research: fin-99-investment-envelope-2142

| Field              | Value                                                                                 |
|--------------------|---------------------------------------------------------------------------------------|
| Date               | 2026-11-14                                                                            |
| Researcher / agent | rpi-research (via RPI Agent)                                                          |
| Status             | Complete                                                                              |
| Artifact path      | .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-research.md     |

## Research Brief

* What to research: Current `src/core` implementation of Issue #99 (Investment envelope, liquidity and downside tolerance controls), BRD requirements (`RULE-011`, `RULE-012`, `BG-008`, `OD-12`, `OD-15`), remaining functional/safety gaps, and worktree-isolated test verification under bare `mypy` and `unittest discover -s tests -p 'test_*99*.py' -v`.
* Why it matters: Issue #99 requires proving in `src/core` that investment envelope, liquidity/covenant headroom, and downside tolerances are recorded strictly as human-approved inputs (never invented) and that any breach emits a deterministic pause signal for a named human decision without automatically cutting or restarting live activity.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` within the confirmed automatic RPI loop.
* Scope: `src/core/src/zava_forward/core/exposure_limits.py`, `src/core/src/zava_forward/core/finance.py`, `src/core/tests/test_issue_99_acceptance.py`, `src/core/tests/test_exposure_limits.py`, `src/core/README.md`, and upstream BRD/case-study context.
* Non-goals: Inventing Zava North Homes company figures or Board approvals (`OD-12`, `OD-15`), modifying `src/api` or web UI, pushing to remote, or closing Issue #99 before real human/Board inputs exist.
* Criteria: Both locally verifiable acceptance criteria must be proven in `src/core` with strict `mypy`, `ruff check`, `ruff format --check`, and `unittest discover -s tests -p 'test_*99*.py' -v` resolving against this worktree's `src/core/src`.
* Requested outputs: Converged recommendation for `src/core` refinements and acceptance test suite.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                        |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | How does `src/core` record human-approved envelope, liquidity/covenant, and downside limits and emit breach pause signals, and what gaps remain? |
| Codebase scope                   | `docs/`, `src/core/`, `src/api/tests/test_finance_exposure_api.py`, `.copilot-tracking/`                                     |
| External scope                   | none                                                                                                                         |
| Initial internal candidate areas | `docs/brds/agentic-retrofit-programme-brd.md`, `src/core/src/zava_forward/core/exposure_limits.py`, `src/core/src/zava_forward/core/finance.py`, `src/core/tests/` |
| Initial external candidate areas | none                                                                                                                         |
| Research posture                 | focused                                                                                                                      |
| Posture provenance               | default (bounded internal `src/core` task with named files, explicit verification command, and supplied acceptance criteria) |
| Explicit limits / deadline       | Changes scoped to `src/core` and `.copilot-tracking/`; do not push; leave clean working tree                                 |
| Posture-specific completion basis| focused scope and materiality                                                                                                |
| Edits allowed during research?   | no, research-only                                                                                                            |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                         |
| Known constraints / excluded sources | Shared multi-worktree Python environment: never mutate global `~/.local` editable installs; never invent company numbers |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | AMA Repository Instructions      | `applyTo: "**"` matches docs, `src/core`, tracking | Requires case-study/KB checks, no invented company facts, `Refs #99` boundary, focused validation | Selected: governs evidence and safety boundaries |
| Skill               | `python-foundational`            | Python 3.12 typing/testing domain match           | Optional Python guidance                     | Skipped: `src/core/pyproject.toml` already defines strict `mypy` and `ruff` rules |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered general research worker           | Bounded delegated lane artifact              | Skipped (inline): tightly coupled single-module `src/core` inspection completed in <=5 direct reads |
| Research specialist | `Housing Finance and Grants Lead`| Role agent for Zava North Homes finance context   | Sector-informed hypothesis framing           | Skipped: BRD `RULE-011`, `RULE-012`, `BG-008`, `OD-12`, `OD-15` already capture exact requirements |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive automatic RPI session with explicit target, scope, acceptance criteria, and verification command | No interaction available | Proceed in focused convergence mode scoped to `src/core` |
| Direction change | Untracked `src/core/tests/test_issue_99_acceptance.py` discovered in worktree alongside shared-env editable install path pointing to `/home/azureuser/source/ama` | No interaction needed | Preserve and extend `test_issue_99_acceptance.py`; prepend worktree `src/` path locally in the test file rather than altering shared site-packages |
| Convergence      | Cycle 1 answered all questions across Wider, Deeper, and Contrarian waves | No interaction needed | Stop research after Cycle 1 with Planning Readiness `Ready` |

## Scope and Success Criteria

* Scope: Pure-core approval-gated investment envelope, liquidity/covenant headroom floor, and downside tolerance controls in `src/core/src/zava_forward/core/exposure_limits.py`, core documentation in `src/core/README.md`, and unit/acceptance tests in `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py`.
* Assumptions: Existing 3-argument callers of `record_limits(approval, envelope, tolerances)` in `src/core` and `src/api` must remain backward-compatible without signature breakage.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Deliver locally verifiable Issue #99 acceptance criteria in `src/core` ("Envelope and tolerances are recorded as human-approved inputs, not invented" and "A breach produces a pause signal for a human decision"), write all 4 `.copilot-tracking/` artifacts, verify with bare `mypy`, `ruff`, and `unittest discover -s tests -p 'test_*99*.py' -v`, and commit cleanly without pushing.
* Inferred research questions: Whether `exposure_limits.py` covers liquidity/covenant minimum headroom controls (`BG-008`, `RULE-011`, `OD-12`), whether approval/observation validation has bypass edge cases, and whether `unittest discover` resolves this worktree's `src/core/src`.
* Caller constraints and non-goals: Do not invent company figures; do not push; keep `git status --short` empty at completion.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Deliver locally verifiable criteria in `src/core` and verify with bare `mypy`, `ruff`, and `test_*99*.py` | User prompt (Intake) | Scopes implementation to `src/core` while preserving `src/api` caller compatibility |
| exclude                                                  | Do not invent Board/Finance figures (`OD-12`, `OD-15`) and do not push to remote | User prompt & repo instructions | Prohibits numeric defaults and remote writes |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status                    |
|---:|------------------|------------------------------------------|-----------|---------------------------|
| Q1 | What exact controls do BRD `RULE-011`, `RULE-012`, `BG-008`, `OD-12`, and `OD-15` require for Issue #99? | straightforward | H | answered |
| Q2 | What does `src/core` (`exposure_limits.py`, `finance.py`, `form_review.py`) already implement, and what gaps remain? | depth | H | answered |
| Q3 | Can unapproved, malformed, negative, or unvalidated inputs bypass `record_limits` or `assess`? | depth | H | answered |
| Q4 | Does bare `python3 -m unittest discover -s tests -p 'test_*99*.py' -v` test this worktree's `src/core/src` without polluting shared site-packages? | straightforward | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-03/issue-99-exposure-limits-research.md`, `.copilot-tracking/research/2026-11-12/finite-exposure-99-1112-research.md`, `.copilot-tracking/research/2026-11-14-issue-99-envelope-controls-research.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/reference/research/sector/housing-association-primer.md`, `docs/reference/research/company/company-profile-research.md`.
* Reused (verified) findings: `exposure_limits.py` already handles `approved_by`/`approved_at` (with `approver`/`approved_on` aliases), 6 `RULE-012` downside ceiling dimensions, `pause_signal` with `automatic_cut=False`, and non-finite (`inf`/`nan`) exposure observations (`C4`, `C5`, `C6`).
* Superseded / stale: Earlier artifacts left three material gaps open: (1) liquidity and covenant minimum headroom floor controls (`BG-008`, `RULE-011`, `OD-12`, and Issue #99's title) were absent; (2) negative finite observations (`committed = -5`) were noted as a follow-up in `finite-exposure-99-1112-research.md` and still evaluate as `"Within"`; and (3) bare `unittest discover` loads `/home/azureuser/source/ama/src/core/src` rather than this worktree (`C5`, `C8`).

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow to `src/core`; exclude invented figures and remote push
* Active research posture and completion basis: focused; focused scope and materiality
* Explicit limits or deadline effect: Scoped strictly to `src/core` and `.copilot-tracking/`

#### Wave 1: Wider

* Plan and independent lanes: Inline survey of Issue #99 metadata, Case Study 48 original/addendum, KB index, BRD (`BG-008`, `RULE-011`, `RULE-012`, `OD-12`, `OD-15`), PRD references, and all `exposure_limits` callers across `src/core` and `src/api`.
* Worker evidence relationships or inline fallback: Inline (`Q1 -> C1, C2, C3`; `Q2 -> C4, C5, C6, C7`).
* Reflection: `exposure_limits` is only called by `FinanceMixin.exposure_signal` (`src/core`), `test_exposure_limits.py`, `test_issue_99_acceptance.py`, and `test_finance_exposure_api.py` (`src/api`). While envelope ceiling and 6 `RULE-012` maximum tolerances exist, liquidity and covenant minimum headroom controls (`BG-008`, `RULE-011`, `OD-12`) are missing, and `src/core/README.md` does not yet document `exposure_limits`.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Inspect `exposure_limits.py` validation/assessment contracts line-by-line, `FinanceMixin.exposure_signal` file loading, `pyproject.toml` strict `mypy`/`ruff` configuration, and `sys.path` import behavior in `src/core`.
* Plan and independent lanes: Inline deep inspection of `exposure_limits.py`, `finance.py`, `test_exposure_limits.py`, `test_issue_99_acceptance.py`, `pyproject.toml`, and runtime `sys.path`.
* Worker evidence relationships or inline fallback: Inline (`Q2, Q3 -> C4, C5, C6`; `Q4 -> C8`).
* Reflection: Runtime probe confirmed `import zava_forward.core.exposure_limits` resolves to `/home/azureuser/source/ama/src/core/src/zava_forward/core/exposure_limits.py` when invoked via bare `python3 -m unittest discover` in this worktree (`C8`). Prepending `Path(__file__).resolve().parents[1] / "src"` in `test_issue_99_acceptance.py` isolates this worktree cleanly without mutating shared `~/.local` site-packages.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge the assumption that existing `exposure_limits.py` already satisfies all edge cases of "human-approved inputs, not invented" and "breach produces a pause signal".
* Plan and independent lanes: Inline adversarial trace of `_approval`, `record_limits`, `load_limits`, and `assess` against forged dicts, conflicting attribution fields, malformed ISO timestamps, negative finite observations, annual-plan caps, and liquidity/covenant floors.
* Worker evidence relationships or inline fallback: Inline (`Q3 -> C4, C5`):
  1. Passing an unvalidated dict directly to `assess(raw_dict, exposure)` bypasses `record_limits` and only runs `stale_reason` (`C5`), allowing missing `approver`/`restart_owner`, empty tolerances, or `amount=inf` to return `"Within limits"`.
  2. `_approval` regex `r"\d{4}-\d{2}-\d{2}(T[0-9:.+\-Z]+)?"` accepts invalid ISO timestamps such as `"2026-01-01T99:99:99"` or `"2026-01-01T---"` and silently ignores conflicting `approved_by` vs `approver` or `approved_at` vs `approved_on` values (`C4`).
  3. Negative finite observations (`committed = -5`, `tolerances={"capital": -10}`) pass `_finite_observation` and report `"Within"` rather than `"Unknown"` (`C5`).
  4. Liquidity minimum floor and covenant headroom minimum floor (`observed < minimum`) are completely unrepresented (`C1`, `C2`, `C4`).
* Reflection: All four contrarian findings are genuine, high-confidence correctness gaps in `exposure_limits.py` that can be fixed cleanly and backward-compatibly in `src/core`.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment  |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|-----------------------------|
| Add optional human-approved `liquidity` (minimum floor + currency, optional `covenant_minimum` + `covenant_unit`) and optional `annual_plan` envelope cap to `record_limits`, `load_limits`, and `assess` | C1, C2, C3, C4, C5, C6 | accepted | Directly delivers Issue #99 liquidity/headroom and `RULE-011` annual-plan controls without inventing defaults or breaking 3-arg callers | Selected recommendation |
| Re-validate `limits` structure inside `assess`, reject negative finite exposure observations as `Unknown`, validate full ISO timestamps, and reject conflicting attribution aliases | C4, C5 | accepted | Eliminates false `"Within limits"` bypasses and guarantees unattributed/forged/negative inputs never suppress pause signals | Selected recommendation |
| Ensure `test_issue_99_acceptance.py` prepends worktree `src/` to `sys.path` and asserts loaded module path | C8 | accepted | Ensures bare `unittest discover -s tests -p 'test_*99*.py' -v` tests this worktree without mutating shared global site-packages | Selected recommendation |
| Surface `liquidity` and `pause_signal.decision_owner` in web UI | C6 | deferred | Outside `src/core` caller scope for this task | Follow-up item |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Focused scope saturated; every research question has direct codebase line evidence and runtime verification.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded single-package `src/core` scope completed directly in <=5 targeted searches/reads without subagent latency.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`)           | Tool                                | Confidence       | Notes       |
|----|-----------------|----------------------------------|-------------------------------------|------------------|-------------|
| C1 | `BG-008` requires maintaining affordability via minimum liquidity and covenant headroom within board-approved tolerances, noting company data is required | `docs/brds/agentic-retrofit-programme-brd.md:641` | grep | high | Establishes minimum-floor semantics for liquidity/covenant controls |
| C2 | `RULE-011` (`AC-037`) requires a board-approved investment envelope integrated with asset plan, liquidity forecast, and covenant model before exceeding annual plan; `RULE-012` (`AC-038`) defines 6 downside tolerance dimensions (`safety`, `resident`, `quality`, `capital`, `grant`, `capacity`) | `docs/brds/agentic-retrofit-programme-brd.md:1573` | grep | high | Lines 1573-1574 define both envelope/liquidity/annual-plan and 6 downside dimensions |
| C3 | `OD-12` and `OD-15` record that Zava North Homes' actual capital envelope, liquidity, covenants, and Board downside tolerances are missing company evidence | `docs/brds/agentic-retrofit-programme-brd.md:2130` | grep | high | Lines 2130-2133 and 2289-2292 forbid inventing company numbers |
| C4 | `exposure_limits._approval` and `record_limits` require human attribution and finite non-negative envelope/tolerances with zero defaults, but lack optional liquidity/covenant minimum-floor support, accept invalid ISO timestamp suffixes, and ignore conflicting `approved_by`/`approver` or `approved_at`/`approved_on` pairs | `src/core/src/zava_forward/core/exposure_limits.py:51` | view | high | Lines 51-101 inspected |
| C5 | `exposure_limits.assess` emits `pause_signal` (`automatic_cut=False`), `Held`, `Unknown`, `Breach`, and `Within limits`, but does not re-validate raw `limits` dicts beyond `stale_reason`, treats negative finite observations as `"Within"`, and lacks minimum-floor breach checks for liquidity/covenants | `src/core/src/zava_forward/core/exposure_limits.py:143` | view | high | Lines 47-49 and 143-214 inspected |
| C6 | `FinanceMixin.exposure_signal` and `/api/finance/exposure` consume `load_limits`, `committed_exposure`, `assess`, and `held`; existing tests call `record_limits(approval, envelope, tolerances)` with 3 positional arguments | `src/core/src/zava_forward/core/finance.py:351` | grep / view | high | Also verified in `src/api/tests/test_finance_exposure_api.py:82-145` |
| C7 | `form_review.py` holds diagnostic `OD-12` and `OD-15` ledger entries with `approved_envelope=None` and `approved_tolerances=None` | `src/core/src/zava_forward/core/form_review.py:29` | grep | high | Confirms `exposure_limits.py` owns executable limit recording and breach assessment |
| C8 | Untracked `src/core/tests/test_issue_99_acceptance.py` exists in worktree, and bare `python3` resolves `zava_forward.core.exposure_limits` to `/home/azureuser/source/ama/src/core/src/...` via shared `~/.local` editable install | `src/core/tests/test_issue_99_acceptance.py:1` | view / bash | high | Also checked `src/core/pyproject.toml:30-42` (`mypy` strict + `ruff` config) |

### External Evidence

| ID | Claim / finding | Source (title) | URL     | Retrieved      | Version/date | Confidence       |
|----|-----------------|----------------|---------|----------------|--------------|------------------|

### Contradictions / Conflicts

* `none`

## Findings Mapped to Questions and Evidence

| Question | Finding             | Evidence IDs | Confidence          | Decision or readiness implication    |
|----------|---------------------|--------------|---------------------|--------------------------------------|
| Q1       | Issue #99 traces to `BG-008`, `RULE-011`, `RULE-012`, `OD-12`, and `OD-15`: human-approved investment envelope (with optional annual-plan baseline), minimum liquidity/covenant headroom floors, and 6 downside maximum tolerances, producing a human-decision pause signal on breach without inventing company figures | C1, C2, C3 | high | Requires supporting both upper-ceiling limits and optional minimum-floor liquidity/covenant controls |
| Q2       | `exposure_limits.py` implements envelope + 6 downside maximums + `pause_signal`, and `finance.py` exposes `exposure_signal`, but liquidity/covenant floors, `annual_plan` cap checks, and `src/core/README.md` documentation for `exposure_limits` are missing | C4, C5, C6, C7 | high | Add additive optional `liquidity` / `covenant` floor and `annual_plan` controls plus README docs |
| Q3       | Contrarian trace found 3 validation gaps: raw `limits` dicts passed directly to `assess()` bypass `record_limits()`, negative finite observations (`< 0`) evaluate as `"Within"`, and `_approval()` accepts malformed timestamp suffixes or conflicting attribution aliases | C4, C5 | high | Harden `_approval()`, `_non_negative_finite_observation()`, and `assess()` validation |
| Q4       | Shared `~/.local` site-packages points at `/home/azureuser/source/ama/src/core/src`; prepending worktree `src/` in `test_issue_99_acceptance.py` ensures bare `unittest discover` tests this worktree safely | C8 | high | Include worktree `src/` path guard and module-origin assertion in `test_issue_99_acceptance.py` |

## Key Discoveries

* Liquidity and covenant headroom (`BG-008`, `RULE-011`, `OD-12`) are **minimum floor** controls (`observed < minimum` triggers `Breach`), unlike envelope and the six `RULE-012` downside dimensions which are **maximum ceiling** controls (`observed > maximum` triggers `Breach`) (`C1`, `C2`, `C4`).
* Making `liquidity` (and optional `covenant` minimum floor or `envelope.annual_plan`) keyword-optional in `record_limits` and JSON-optional in `load_limits` preserves 100% compatibility with all existing 3-argument callers while rejecting unapproved/malformed liquidity inputs when supplied (`C4`, `C6`).
* Re-validating `limits` via `record_limits` inside `assess` and rejecting negative finite observations (`< 0`) as `Unknown` closes silent `"Within limits"` bypass paths (`C5`).
* In this shared multi-worktree host, modifying `~/.local` via `pip install -e .` would disrupt sibling worktrees; prepending `Path(__file__).resolve().parents[1] / "src"` in `test_issue_99_acceptance.py` isolates test imports to this worktree under the exact user-specified bare verification command (`C8`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Extend `zava_forward.core.exposure_limits` additively with optional human-approved `liquidity` (minimum liquidity floor + currency, and optional covenant headroom minimum + unit) and optional `envelope["annual_plan"]` cap (`RULE-011` `AC-037`), harden `_approval` (strict ISO `date`/`datetime` parsing and alias consistency) and `assess` (canonical `limits` validation + non-negative finite observation guard), preserve and expand `src/core/tests/test_issue_99_acceptance.py` (with worktree `src/` path isolation) and `src/core/tests/test_exposure_limits.py`, and document the module boundary in `src/core/README.md`.
* Rationale: Satisfies Issue #99's title, BRD rules (`BG-008`, `RULE-011`, `RULE-012`, `OD-12`, `OD-15`), and both locally verifiable acceptance criteria, fixes all contrarian bypass vectors, keeps 100% backward compatibility with `finance.py` and `src/api`, and passes bare `mypy`, `ruff`, and `unittest discover` safely in a shared environment.
* Evidence refs: C1, C2, C3, C4, C5, C6, C8
* Implementation impact: `src/core/src/zava_forward/core/exposure_limits.py`, `src/core/tests/test_issue_99_acceptance.py`, `src/core/tests/test_exposure_limits.py`, `src/core/README.md`
* Confidence: high: all code paths and verification commands are local and deterministic.

File tree:

```text
src/core/
  README.md                                      (updated)
  src/zava_forward/core/
    exposure_limits.py                           (updated)
  tests/
    test_exposure_limits.py                      (updated)
    test_issue_99_acceptance.py                  (created/committed)
```

### Alternative: Require `liquidity` as a mandatory 4th positional argument in `record_limits`

* Approach: Change `record_limits(approval, envelope, liquidity, tolerances)` to require liquidity on every call.
* Trade-offs: Enforces liquidity presence everywhere, but breaks existing `test_exposure_limits.py`, `test_issue_99_acceptance.py`, and `src/api/tests/test_finance_exposure_api.py` fixtures (`approved-limits.json` files without a `liquidity` key).
* Evidence refs: C6, C8
* Rejection rationale: Rejected because `src/api` is out of edit scope and backward-compatible keyword/JSON-optional `liquidity` preserves existing callers while still strictly validating and evaluating liquidity/covenant floors whenever recorded.

### Alternative: Run `pip install -e src/core` in the shared user environment

* Approach: Overwrite `~/.local/lib/python3.12/site-packages` editable `.pth` to point to this worktree so bare `unittest discover` finds this worktree.
* Trade-offs: Avoids `sys.path` setup in tests, but mutates shared host state across dozens of active git worktrees.
* Evidence refs: C8
* Rejection rationale: Rejected under shared-environment safety rules; test-local `sys.path` prepending isolates this worktree with zero side effects on other worktrees.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Real Zava North Homes Board-approved investment envelope, liquidity/covenant thresholds, and downside tolerances (`OD-12`, `OD-15`) remain external human/Board governance inputs; commits/PRs must use `Refs #99` rather than closing Issue #99 (`C3`, `C7`).
* Follow-up: Surface `liquidity` floor findings and `pause_signal.decision_owner` explicitly in the web Finance workbench (`C6`).
* Residual uncertainty: none for local `src/core` engineering criteria.

## Current Decisions

| Decision     | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale     | Evidence IDs | Implications                       |
|--------------|-------------------------------------------------------|-----------------------------------------------|---------------|--------------|------------------------------------|
| Keep zero company defaults; record envelope, optional annual plan, optional liquidity/covenant minimum floors, and downside tolerances strictly from attributed human-approved inputs | confirmed | user / evidence (`RULE-011`, `RULE-012`, `BG-008`, `OD-12`, `OD-15`) | Prevents invented thresholds while covering full Issue #99 domain | C1, C2, C3, C4 | Additive optional `liquidity` parameter and strict validation in `exposure_limits.py` |
| Harden `assess` and `_approval` against forged dicts, negative observations, invalid ISO timestamps, and conflicting attribution aliases | confirmed | evidence (Contrarian wave) | Ensures unapproved or incomparable inputs always return `Held` or `Unknown` with `pause_signal.paused=True` | C4, C5 | Eliminates false `"Within limits"` results |
| Isolate worktree import in `test_issue_99_acceptance.py` without mutating shared site-packages | confirmed | constraint (shared environment + bare verification command) | Ensures `unittest discover -s tests -p 'test_*99*.py' -v` tests this worktree's `exposure_limits.py` | C8 | Safe, deterministic verification |

## Unresolved Decisions

| Decision     | Smallest evidence or answer needed     | Owner                                  | Impact     | Blocker status                       |
|--------------|----------------------------------------|----------------------------------------|------------|--------------------------------------|
| Board ratification of Zava North Homes actual capital envelope, liquidity/covenant floors, and downside tolerances (`OD-12`, `OD-15`) | Signed Board minute and Finance forecast model | Finance and Board (external human governance) | Required before Issue #99 can be closed in production governance; does not block local `src/core` delivery | important |

## Potential Next Research

| Priority  | Research item                  | Expected value     | Trigger                            | Selected?               | Related questions / evidence |
|-----------|--------------------------------|--------------------|------------------------------------|-------------------------|------------------------------|
| L         | Inspect Finance workbench UI rendering of `pause_signal` and `liquidity` findings | Aligns staff UI presentation with `exposure_limits` detail fields | Follow-up UI task outside `src/core` | deferred | Q2; C6 |

## Planning Readiness

* Status: Ready
* Decision state: Converged on additive `exposure_limits.py` controls + validation hardening + worktree-isolated acceptance tests in `src/core`.
* Evidence basis: C1, C2, C3, C4, C5, C6, C7, C8
* Preconditions met: Scope, target files, backward-compatibility contracts, strict typing/lint configuration, and verification command confirmed.
* Blockers: none
* Smallest action to change readiness: none (already `Ready`)

## Closeout Record

| Field                            | Record                                                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                                       |
| Completed waves                  | Wider, Deeper, and Contrarian completed in order in Cycle 1                                                                    |
| Lane evidence or inline fallback | Inline fallback: bounded 4-file `src/core` scope inspected directly without subagent overhead                                  |
| Research disposition             | executed                                                                                                                       |
| Planning Readiness               | Ready (C1, C2, C3, C4, C5, C6, C7, C8)                                                                                         |
| Blockers                         | none                                                                                                                           |
| Continuation owner and state     | Confirmed automatic RPI Agent; automatic continuation to Plan                                                                  |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (C1-C8)                                                                                                |
| Output mode and planning support | convergence; yes, Planning Readiness is `Ready`                                                              |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | Prior-knowledge gate passed; 3-wave cycle passed; self-check passed; pre-transition state persisted          |
| Continuation result              | automatic continuation to `rpi-plan`                                                                         |
| Primary evidence file            | .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-research.md                            |
| Notes for planning or re-entry   | Preserve 3-arg `record_limits` signature compatibility for `src/api`; do not touch shared `~/.local` installs |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All in-scope `src/core` modules, callers, BRD rules, and test-runner constraints are verified with high-confidence codebase evidence; further research would be redundant.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings Mapped to Questions, Key Discoveries, Alternatives and Decision State, Open Questions, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check
* Missing or limited sections: none
