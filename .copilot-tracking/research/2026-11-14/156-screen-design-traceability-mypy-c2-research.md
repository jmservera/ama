---
title: "Task Research: 156-screen-design-traceability-mypy-c2"
description: "Cycle-2 CI failure investigation for PR #1727 (Issue #156) strict mypy union-attr errors in test_screen_design_traceability.py"
ms.date: 2026-11-14
ms.topic: reference
---
<!-- markdownlint-disable-file -->

| Field              | Value                                                                                          |
|--------------------|------------------------------------------------------------------------------------------------|
| Date               | 2026-11-14                                                                                     |
| Researcher / agent | rpi-research (coordinated by RPI Agent)                                                        |
| Status             | Complete                                                                                       |
| Artifact path      | .copilot-tracking/research/2026-11-14/156-screen-design-traceability-mypy-c2-research.md       |

## Research Brief

* What to research: Root cause, scope, and idiomatic strict-mypy remediation for the two `[union-attr]` failures reported by `src-ci.yml` (`src-api` job) on `src/api/tests/test_screen_design_traceability.py` in PR #1727 (Issue #156).
* Why it matters: Hosted CI run `43644223724` (job `132598509967`) failed `mypy` at commit `deadb7144`, blocking PR #1727 despite passing unit tests and doc traceability checks.
* Audience or intended use: Downstream `rpi-plan`, `rpi-implement`, and `rpi-review` phases in this automatic Cycle-2 RPI loop.
* Scope: `src/api/tests/test_screen_design_traceability.py`, `src/api/tests/test_ux_design_traceability.py`, `src/api/pyproject.toml`, `.github/workflows/src-ci.yml`, and existing `.copilot-tracking/` artifacts for Issue #156 on PR #1727.
* Non-goals: Changing `docs/reference/research/ux/screen-design-traceability.md`, claiming human design/WCAG acceptance for Issue #156, modifying `pyproject.toml` mypy exemptions, or pushing to `origin`.
* Criteria: Fix must eliminate all `mypy` errors across `src/api` (`0 errors`), pass `ruff check .` and `ruff format --check .`, pass `unittest` execution of `tests/test_screen_design_traceability.py`, and preserve all existing `.copilot-tracking/` files.
* Requested outputs: Dated Cycle-2 research artifact with a selected convergence recommendation ready for planning.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                               |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | Why does `mypy` fail on lines 40 and 74 of `src/api/tests/test_screen_design_traceability.py`, what is the exact PR #1727 worktree/branch state, and which narrowing pattern satisfies `mypy`, `ruff`, and `python -O`? |
| Codebase scope                   | `/home/azureuser/source/ama-demo-wt/feat-156-design-traceability-1840` (`src/api/tests/`, `src/api/pyproject.toml`, `.github/workflows/src-ci.yml`, `.copilot-tracking/`) |
| External scope                   | none                                                                                                                                |
| Initial internal candidate areas | `src/api/tests/test_screen_design_traceability.py`, `src/api/tests/test_ux_design_traceability.py`, `src/api/pyproject.toml`        |
| Initial external candidate areas | none                                                                                                                                |
| Research posture                 | focused                                                                                                                             |
| Posture provenance               | default (bounded internal CI fix with named source targets and exact failure log)                                                   |
| Explicit limits / deadline       | Preserve all existing `.copilot-tracking/` artifacts; commit locally and do not push                                                |
| Posture-specific completion basis| focused scope and materiality                                                                                                       |
| Edits allowed during research?   | no, research-only                                                                                                                   |
| Resolved evidence root           | `.copilot-tracking/` inside `/home/azureuser/source/ama-demo-wt/feat-156-design-traceability-1840`                                  |
| Known constraints / excluded sources | Do not claim human acceptance or tick Issue #156 acceptance criteria; do not weaken strict `mypy` configuration                 |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                      | Scoped authority or output contract                            | Selected / skipped reason                                                       |
|---------------------|---------------------------------------|-----------------------------------------------------------|----------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` across repository                         | Validation tiers, branch reuse, noreply git config, Markdown style | Selected: governs PR #1727 branch reuse, focused validation tier, and commit authorship |
| Skill               | `python-foundational`                 | Python typing and test quality topic match                | Python typing idioms                                           | Skipped: sibling `test_ux_design_traceability.py` already defines the exact repo convention |
| Research specialist | `hve-core-all:rpi-researcher`         | General RPI research subagent registered in host          | Independent delegated research lanes                           | Skipped (inline): single tightly coupled 87-line test file and 2 compiler errors |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered | Resulting decision or selected further research                                 |
|------------------|-------------------------------------------------------------------------------------------------------|----------------------|---------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit caller scope, target file, exact mypy errors, and test commands | Unanswered (non-interactive) | Proceed directly in resolved PR #1727 worktree `/home/azureuser/source/ama-demo-wt/feat-156-design-traceability-1840` |
| Direction change | None; caller scope remained stable throughout Cycle 1                                                 | Not applicable       | Keep focused posture on `src/api/tests/test_screen_design_traceability.py`      |
| Convergence      | All questions answered with direct compiler, linter, and sibling-test evidence                        | Not applicable       | Converge on pairing `self.assertIsNotNone(...)` with `assert match is not None` and `assert target_cls is not None` |

## Scope and Success Criteria

* Scope: Resolve PR #1727 worktree/branch mapping, verify the exact `src-api` `mypy` failure, inspect repo lint/type rules and sibling traceability tests, and select the cleanest fix without touching production code or existing tracking artifacts.
* Assumptions: Confirmed via `git worktree list`, `git branch -vv`, and `gh pr view 1727` that PR #1727 (`headRefName: feat/ux-156-design-traceability-1840`, `baseRefName: feat/demo-233-same-home-tensions-0825`, `headRefOid: deadb7144`) resides in `/home/azureuser/source/ama-demo-wt/feat-156-design-traceability-1840`, where local branch `docs/ux-156-design-traceability-1840` is currently checked out at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840` and no local `feat/ux-156-design-traceability-1840` ref exists yet.
* Success criteria:
  * Every research question is answered with grounded `path:line` evidence.
  * Findings, decisions, and readiness claims cite Evidence Log IDs (`C1`–`C8`).
  * Alternatives are compared with trade-offs and rejection rationale.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Run the full RPI loop in order for PR #1727 Cycle-2 CI `mypy` `union-attr` fix on `src/api/tests/test_screen_design_traceability.py` (lines 40 and 74), preserving existing `.copilot-tracking/` files, recording dated `2026-11-14` artifacts, verifying `mypy`, `ruff`, and `unittest`, and committing locally without pushing.
* Inferred research questions: Verify actual git worktree and branch backing PR #1727; confirm no other files in `src/api` fail strict `mypy`; verify `ruff` lint rule compatibility with `assert ... is not None`.
* Caller constraints and non-goals: Convergence mode; no push; preserve existing `.copilot-tracking/` files.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                          | Source / checkpoint | Effect on active brief, evidence, or revalidation                               |
|----------------------------------------------------------|--------------------------------------------------------------------------------|---------------------|---------------------------------------------------------------------------------|
| narrow                                                   | Restrict code edits to `src/api/tests/test_screen_design_traceability.py`      | Caller brief        | Excludes `pyproject.toml` overrides and documentation edits                     |
| exclude                                                  | Preserve all existing `.copilot-tracking/` files and do not push to remote     | Caller brief        | Add net-new `156-screen-design-traceability-mypy-c2-*` artifacts alongside prior files |

## Research Questions

|  # | Sub-question                                                                                              | Type            | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | Which worktree, local branch, and upstream PR head correspond to PR #1727 (Issue #156)?                   | straightforward | H        | answered |
| Q2 | Why does `mypy` emit `[union-attr]` at lines 40 and 74 of `src/api/tests/test_screen_design_traceability.py`, and are there any other `mypy` errors in `src/api`? | straightforward | H | answered |
| Q3 | Which narrowing construct satisfies strict `mypy`, `ruff` (`E,F,I,B,UP`), `python -O`, and existing repository test conventions? | depth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-14-design-traceability-156-research.md`, `.copilot-tracking/research/2026-11-14/156-design-trace-c2-2140-research.md`, `.copilot-tracking/changes/2026-11-14/156-design-trace-c2-2140-changes.md`, `.copilot-tracking/reviews/2026-11-14/156-design-trace-c2-2140-review.md`.
* Reused (verified) findings: Commit `124aca48e` introduced `src/api/tests/test_screen_design_traceability.py`, commit `a5e1c9964` refined its counts/links, and commit `deadb7144` added requirement IDs to `docs/reference/research/ux/screen-design-traceability.md`.
* Superseded / stale: Earlier Cycle-2 (`2140`) addressed only the markdown requirement-ID check and did not re-run `src/api` `mypy`, leaving the two `[union-attr]` errors in `test_screen_design_traceability.py` unresolved in CI run `43644223724`.

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow to `test_screen_design_traceability.py`; preserve prior `.copilot-tracking/` artifacts; no push.
* Active research posture and completion basis: focused; focused scope and materiality.
* Explicit limits or deadline effect: none blocking; all local tools (`mypy`, `ruff`, `unittest`, `gh`) available.

#### Wave 1: Wider

* Plan and independent lanes: Verify repository worktrees, PR #1727 metadata, failed CI run `43644223724` logs, `.github/workflows/src-ci.yml` `src-api` pipeline steps, `src/api/pyproject.toml` tool settings, and sibling traceability tests.
* Worker evidence relationships or inline fallback: Inline investigation (`C1`, `C2`, `C5`, `C6`, `C7`, `C8`) — single worktree and single failing test module make subagent fan-out unnecessary overhead.
* Reflection: Confirmed PR #1727 maps to `/home/azureuser/source/ama-demo-wt/feat-156-design-traceability-1840` where local `docs/ux-156-design-traceability-1840` sits at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840` (base `feat/demo-233-same-home-tensions-0825`), so creating/switching local branch `feat/ux-156-design-traceability-1840` at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840` honors caller Step 4 and PR #1727's `headRefName` without deleting `docs/ux-156-design-traceability-1840` (`C8`). Full `mypy` across 280 files in `src/api` confirmed only the 2 errors in `test_screen_design_traceability.py` exist (`C1`, `C2`).

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Exact AST and regex call sites in `src/api/tests/test_screen_design_traceability.py` (`C3`, `C4`) and sibling convention in `src/api/tests/test_ux_design_traceability.py` (`C7`).
* Plan and independent lanes: Inspect typeshed behavior for `re.search` and `unittest.TestCase.assertIsNotNone`, check Ruff lint rules (`select = ["E", "F", "I", "B", "UP"]`, `line-length = 100`) in `src/api/pyproject.toml` (`C5`), and compare `test_ux_design_traceability.py:78-84` (`C7`).
* Worker evidence relationships or inline fallback: Inline (`C3`, `C4`, `C5`, `C7`).
* Reflection: On line 40 (`C3`), `re.search(r"#(\d+)\]", row[0])` returns `Match[str] | None` and `.group(1)` is chained directly without checking `None`. On lines 69–74 (`C4`), `node = next(..., None)` has type `ast.ClassDef | None`; `self.assertIsNotNone(node, ...)` on line 73 performs the runtime assertion with a helpful message, but `unittest.TestCase.assertIsNotNone` cannot narrow types in `mypy`. Sibling `test_ux_design_traceability.py:81-82` (`C7`) solves this exact issue by keeping `self.assertIsNotNone(...)` and immediately adding `assert ... is not None`, which is fully allowed under Ruff (`S101` is not enabled in `C5`).

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether `assert match is not None` / `assert target_cls is not None` has drawbacks under `python -O`, Ruff formatting, or strict `mypy`, and evaluate `pyproject.toml` mypy overrides or `if ... is None: self.fail(...)` instead.
* Plan and independent lanes: Compare three approaches: (A) `self.assertIsNotNone(...)` followed by `assert match is not None` / `assert target_cls is not None`; (B) `if x is None: self.fail(...)` without `assert`; (C) `[[tool.mypy.overrides]]` exemption in `src/api/pyproject.toml`.
* Worker evidence relationships or inline fallback: Inline (`C3`, `C4`, `C5`, `C6`, `C7`).
* Reflection: Approach C (`pyproject.toml` exemption) violates repository intent that exemptions apply only to legacy `mvp/` migrated tests (`C5`, `C6`). Pure `assert x is not None` alone would be stripped under `python -O`, whereas pairing `self.assertIsNotNone(match, row[0])` + `assert match is not None` and `self.assertIsNotNone(target_cls, f"{klass} not found in {path}")` + `assert target_cls is not None` preserves descriptive `unittest` failures even under `-O`, narrows types cleanly in `mypy`, matches `test_ux_design_traceability.py:81-82` (`C7`), and directly implements the caller-specified `assert match is not None` / `assert target_cls is not None` guards.

#### Parent Synthesis and Disposition

| Material / claim                                                                                   | Evidence IDs | Parent disposition | Evidence-based rationale                                                                 | Primary-artifact treatment |
|----------------------------------------------------------------------------------------------------|--------------|--------------------|------------------------------------------------------------------------------------------|----------------------------|
| Align worktree branch to local `feat/ux-156-design-traceability-1840` at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840` | C1, C8 | accepted | `gh pr view 1727` shows `headRefName: feat/ux-156-design-traceability-1840` (`deadb7144`), while local checkout is `docs/ux-156-design-traceability-1840`; creating local `feat/ux-156-design-traceability-1840` satisfies caller Step 4 and `push.default = simple` without deleting `docs/ux-156-design-traceability-1840` | Finding Q1 & Current Decisions |
| Pair `self.assertIsNotNone(...)` with `assert match is not None` and `assert target_cls is not None` | C3, C4, C5, C7 | accepted | Eliminates both `[union-attr]` errors, keeps runtime assertion under `-O`, passes Ruff, and matches `test_ux_design_traceability.py` | Selected Recommendation |
| Exempt `test_screen_design_traceability` in `src/api/pyproject.toml`                               | C5, C6       | rejected           | Weakens strict typing on a new test file and touches shared project config unnecessarily | Rejected Alternative 1     |
| Replace `assert` with `if ... is None: self.fail(...)` only                                        | C4, C7       | rejected           | Diverges from sibling `test_ux_design_traceability.py` idiom and caller's explicit `assert ... is not None` specification | Rejected Alternative 2 |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Focused scope saturated; all 3 research questions answered with direct compiler and codebase evidence and zero contradictions.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: single 87-line test file with two deterministic `mypy` `[union-attr]` errors reproduced locally in <2s.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | Hosted CI job `src-api` (`src-ci.yml`) runs `unittest discover -s tests -v`, `ruff check . && ruff format --check .`, and `mypy` from `src/api` | `.github/workflows/src-ci.yml:93` | view / gh | high | CI run `43644223724` job `132598509967` failed solely in `Type check` (`mypy`) |
| C2 | `src/api` enforces `strict = true` across `files = ["src", "tests", "checks"]`, checking `tests/test_screen_design_traceability.py` without overrides | `src/api/pyproject.toml:55` | view / bash | high | Local `python3 -m mypy` reproduced exact 2 errors across 280 checked files |
| C3 | `re.search(r"#(\d+)\]", row[0]).group(1)` chains `.group(1)` directly on `Match[str] | None`, triggering `mypy` `[union-attr]` | `src/api/tests/test_screen_design_traceability.py:40` | view / mypy | high | Needs `match = re.search(...)`, `self.assertIsNotNone(match, row[0])`, `assert match is not None` |
| C4 | `node = next(..., None)` has type `ast.ClassDef | None`; `self.assertIsNotNone(node, ...)` does not narrow `node` before `node.body`, triggering `[union-attr]` | `src/api/tests/test_screen_design_traceability.py:69` | view / mypy | high | Renaming `node` to `target_cls` and adding `assert target_cls is not None` after `self.assertIsNotNone` resolves line 74 |
| C5 | Ruff config in `src/api/pyproject.toml` sets `line-length = 100`, `target-version = "py312"`, and `select = ["E", "F", "I", "B", "UP"]` (no `S101` ban on `assert`) | `src/api/pyproject.toml:30` | view | high | `assert ... is not None` is clean under both `ruff check .` and `ruff format --check .` |
| C6 | Per-file Ruff/mypy exemptions in `src/api/pyproject.toml` are explicitly restricted to legacy files migrated unchanged from `mvp/` (`archive v0.21.0`) | `src/api/pyproject.toml:37` | view | high | New test files must satisfy strict `mypy` and `ruff` directly |
| C7 | Sibling `test_ux_design_traceability.py` narrows optional `ast.ClassDef | None` by pairing `self.assertIsNotNone(node, token)` with `assert node is not None` | `src/api/tests/test_ux_design_traceability.py:78` | view | high | Canonical repository idiom for strict `mypy` narrowing in `unittest.TestCase` |
| C8 | Repository branch workflow instructs reusing the active branch/worktree backing an open PR (`docs/ux-156-design-traceability-1840` -> `origin/feat/ux-156-design-traceability-1840` for PR #1727) | `.github/copilot-instructions.md:148` | view / git | high | Confirmed via `gh pr view 1727` (`headRefOid: deadb7144`) and `git worktree list` |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* Local branch name vs remote PR #1727 `headRefName`: Worktree `/home/azureuser/source/ama-demo-wt/feat-156-design-traceability-1840` currently has local branch `docs/ux-156-design-traceability-1840` checked out at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840`, with no local `feat/ux-156-design-traceability-1840` ref yet (`C8`). Creating and switching to local `feat/ux-156-design-traceability-1840` at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840` during implementation aligns the local branch with caller Step 4 and PR #1727's `headRefName` while keeping `docs/ux-156-design-traceability-1840` intact.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | PR #1727 (`deadb7144`, `headRefName: feat/ux-156-design-traceability-1840`, `baseRefName: feat/demo-233-same-home-tensions-0825`) resides in `/home/azureuser/source/ama-demo-wt/feat-156-design-traceability-1840` (`docs/ux-156-design-traceability-1840` at `deadb7144`); create/switch local `feat/ux-156-design-traceability-1840` tracking `origin/feat/ux-156-design-traceability-1840` | C1, C8 | high | Reuse active worktree, align local branch name to `feat/ux-156-design-traceability-1840`, and preserve all existing `.copilot-tracking/` artifacts |
| Q2 | Strict `mypy` fails only at `test_screen_design_traceability.py:40` (`re.search(...)` returning `Match[str] \| None`) and `:74` (`next(..., None)` returning `ClassDef \| None`, not narrowed by `self.assertIsNotNone`); all other 279 files in `src/api` pass | C1, C2, C3, C4 | high | Surgical 2-site fix in `src/api/tests/test_screen_design_traceability.py` is sufficient |
| Q3 | Pairing `self.assertIsNotNone(...)` with `assert match is not None` and `assert target_cls is not None` narrows both optionals for `mypy`, preserves descriptive unittest failures under `-O`, passes Ruff, and matches `test_ux_design_traceability.py` | C3, C4, C5, C7 | high | Ready for `rpi-plan` and `rpi-implement` |

## Key Discoveries

* `python3 -m mypy` in `src/api` checks 280 source files under `strict = true` and reports zero errors outside `src/api/tests/test_screen_design_traceability.py` (`C2`, `C3`, `C4`).
* `src/api/tests/test_ux_design_traceability.py:81-82` (`C7`) already establishes the exact repository pattern: `self.assertIsNotNone(...)` followed immediately by `assert ... is not None`.
* Under `.github/copilot-instructions.md` (`C8`), this test-only strict-typing fix is a focused-tier change: targeted `mypy`, `ruff check .`, `ruff format --check .`, and `unittest` checks apply locally without altering gate tools, Dockerfiles, workflows, or security controls.

### Complete Examples

```python
match = re.search(r"#(\d+)\]", row[0])
self.assertIsNotNone(match, row[0])
assert match is not None
seen.add(int(match.group(1)))
```

```python
target_cls = next(
    (n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == klass),
    None,
)
self.assertIsNotNone(target_cls, f"{klass} not found in {path}")
assert target_cls is not None
self.assertIn(
    method, {n.name for n in target_cls.body if isinstance(n, ast.FunctionDef)}
)
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: In `src/api/tests/test_screen_design_traceability.py`, bind `match = re.search(r"#(\d+)\]", row[0])`, assert `self.assertIsNotNone(match, row[0])` and `assert match is not None` before `match.group(1)`; rename `node` to `target_cls`, assert `self.assertIsNotNone(target_cls, f"{klass} not found in {path}")` and `assert target_cls is not None` before accessing `target_cls.body`.
* Rationale: Directly eliminates both `[union-attr]` errors under `mypy --strict`, retains clear `unittest` failure diagnostics even if assertions are stripped, conforms to Ruff (`line-length = 100`, `E,F,I,B,UP`), matches sibling `test_ux_design_traceability.py`, and honors the caller's exact `assert match is not None` / `assert target_cls is not None` contract.
* Evidence refs: C2, C3, C4, C5, C7
* Implementation impact: Single source file `src/api/tests/test_screen_design_traceability.py` plus dated Cycle-2 `.copilot-tracking/` artifacts.
* Confidence: high: reproduced exact CI failure locally and confirmed repo conventions.

File tree:

```text
src/api/tests/test_screen_design_traceability.py (modified)
.copilot-tracking/rpi-sessions/2026-11-14/156-screen-design-traceability-mypy-c2-state.json (added)
.copilot-tracking/research/2026-11-14/156-screen-design-traceability-mypy-c2-research.md (added)
.copilot-tracking/plans/2026-11-14/156-screen-design-traceability-mypy-c2-plan.md (planned)
.copilot-tracking/details/2026-11-14/156-screen-design-traceability-mypy-c2-details.md (planned)
.copilot-tracking/changes/2026-11-14/156-screen-design-traceability-mypy-c2-changes.md (planned)
.copilot-tracking/reviews/2026-11-14/156-screen-design-traceability-mypy-c2-review.md (planned)
```

### Alternative: Add module override in `src/api/pyproject.toml`

* Approach: Add `"test_screen_design_traceability"` and `"tests.test_screen_design_traceability"` to `[[tool.mypy.overrides]]` with `ignore_errors = true`.
* Trade-offs: Zero changes to the test file, but disables all type checking for the module and modifies shared project configuration.
* Evidence refs: C5, C6
* Rejection rationale: `src/api/pyproject.toml:37` reserves exemptions for legacy `mvp/` migrated modules; newly added tests must pass strict `mypy`.

### Alternative: Narrow exclusively with `if ... is None: self.fail(...)`

* Approach: Replace `self.assertIsNotNone` / `assert ... is not None` with `if match is None: self.fail(row[0])` and `if target_cls is None: self.fail(...)`.
* Trade-offs: Narrows types via `NoReturn` without `assert`, but adds extra branches and diverges from sibling `test_ux_design_traceability.py` and the caller's explicit `assert match is not None` / `assert target_cls is not None` specification.
* Evidence refs: C4, C7
* Rejection rationale: Pairing `self.assertIsNotNone(...)` with `assert ... is not None` achieves the same `-O` safety while staying 100% consistent with `test_ux_design_traceability.py:81-82` and the caller's brief.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Worktree `/home/azureuser/source/ama-demo-wt/feat-156-design-traceability-1840` had local branch `docs/ux-156-design-traceability-1840` checked out tracking `origin/feat/ux-156-design-traceability-1840` at `deadb7144`; creating and switching to local branch `feat/ux-156-design-traceability-1840` tracking `origin/feat/ux-156-design-traceability-1840` ensures the commit lands directly on `feat/ux-156-design-traceability-1840` without deleting `docs/ux-156-design-traceability-1840`.
* Follow-up: Human design, content, and accessibility reviews for Issue #156 remain open outside this CI typing fix (`screen-design-traceability.md` leaves Issue #156 criterion 1 unticked).
* Residual uncertainty: none for the `mypy` fix.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
|----------|--------|----------------|-----------|--------------|--------------|
| Work in `/home/azureuser/source/ama-demo-wt/feat-156-design-traceability-1840` and commit on local branch `feat/ux-156-design-traceability-1840` tracking `origin/feat/ux-156-design-traceability-1840` | confirmed | caller / repo branch rules | Matches open PR #1727 (`headRefName: feat/ux-156-design-traceability-1840`, `deadb7144`), honors caller Step 4, and preserves existing `.copilot-tracking/` history | C1, C8 | Commit stays local on `feat/ux-156-design-traceability-1840` ready for owner/orchestrator push |
| Narrow `match` and `target_cls` using `self.assertIsNotNone(...)` + `assert ... is not None` | confirmed | caller / codebase convention | Satisfies strict `mypy`, `ruff`, `-O` safety, and `test_ux_design_traceability.py` | C3, C4, C5, C7 | Minimal surgical change in `src/api/tests/test_screen_design_traceability.py` |
| Classify validation as focused tier | confirmed | `.github/copilot-instructions.md` | Test-only typing guard edit with zero security, infra, workflow, SQL, or gate-semantics impact | C1, C8 | Run `mypy`, `ruff check`, `ruff format --check`, and targeted `unittest` |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| None for Cycle-2 CI typing fix | Not applicable | none | none | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Role-owner wireframes and human design acceptance for Issue #156 | Closes remaining unticked Issue #156 criteria | Separate human UX review workstream (#155 / #156) | deferred | C8 |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation selected (`self.assertIsNotNone` + `assert match is not None` / `assert target_cls is not None` in `src/api/tests/test_screen_design_traceability.py`).
* Evidence basis: C1, C2, C3, C4, C5, C6, C7, C8
* Preconditions met: Exact CI failure reproduced locally; sibling pattern verified; Ruff and mypy configurations inspected; PR #1727 branch/worktree verified clean.
* Blockers: none
* Smallest action to change readiness: none (already Ready)

## Closeout Record

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                     |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian completed in order                                                    |
| Lane evidence or inline fallback | Inline investigation (`C1`–`C8`); single 87-line test file did not warrant subagent dispatch                 |
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`–`C8`)                                                                                            |
| Blockers                         | none                                                                                                         |
| Continuation owner and state     | Confirmed automatic RPI Agent; automatic transition to `Plan`                                                |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`–`C8`)                                                                                            |
| Output mode and planning support | convergence; yes, single concrete implementation approach selected                                           |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | All Research gates passed; pre-transition state write to `Plan` required before activating `rpi-plan`        |
| Continuation result              | automatic continuation to `rpi-plan`                                                                         |
| Primary evidence file            | .copilot-tracking/research/2026-11-14/156-screen-design-traceability-mypy-c2-research.md                     |
| Notes for planning or re-entry   | Preserve all existing `.copilot-tracking/` files; run `mypy`, `ruff`, and `unittest` from `src/api`; do not push |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All questions answered with direct local reproduction and zero remaining uncertainty within focused scope.

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
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings Mapped to Questions, Key Discoveries, Alternatives and Decision State, Open Questions, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
* Missing or limited sections: none
