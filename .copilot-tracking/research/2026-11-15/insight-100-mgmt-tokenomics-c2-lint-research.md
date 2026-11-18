---
description: "Primary evidence artifact for Issue #100 PR #1792 c2 Ruff format remediation"
---
<!-- markdownlint-disable-file -->

# Task Research: insight-100-mgmt-tokenomics-c2-lint

| Field              | Value                                                                               |
|--------------------|-------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                          |
| Researcher / agent | rpi-research (RPI Agent automatic child session)                                    |
| Status             | Complete                                                                            |
| Artifact path      | .copilot-tracking/research/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-research.md |

## Research Brief

* What to research: Verify the exact hosted CI failure on PR #1792 (`d3a2c5405`), confirm `.github/workflows/src-ci.yml` lint invocations and `pyproject.toml` Ruff configurations across `src/core`, `src/api`, and root, verify `ruff format --check --diff` across every package touched by `d3a2c5405`, and confirm Focused-tier validation boundaries.
* Why it matters: Commit `d3a2c5405` passed `8/10` CI jobs on PR #1792 (`feat/insight-100-mgmt-tokenomics` -> `feat/demo-164-chat-grounding-provenance-0900`) and failed only `src-core` and `src-api` `Lint` due to `line-length = 100` vs repo-root `88` formatting. Accurate verification ensures zero unintended semantic diffs or missed files.
* Audience or intended use: `rpi-plan`, `rpi-implement`, `rpi-review`, and Backlog Delivery Coordinator exact-head verification.
* Scope: `.github/workflows/src-ci.yml`, `pyproject.toml` (if any), `src/core/pyproject.toml`, `src/api/pyproject.toml`, `src/core/src/zava_forward/core/tokenomics.py`, `src/api/src/zava_forward/api/progress.py`, and all other files changed in `d3a2c5405`.
* Non-goals: Behavioural changes to tokenomics logic, rebasing or pushing to remote, modifying `pyproject.toml` or CI workflows, or changing `src/api/src/zava_forward/api/web/`.
* Criteria: Every modified package in `d3a2c5405` checked against `src-ci.yml` commands; exact line diffs identified with `path:line` evidence; validation tier classified per owner decision D4 and Issue #1294.
* Requested outputs: Primary research artifact with `C#` evidence log, synthesis, convergence recommendation, and Planning Readiness.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                              |
|----------------------------------|----------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1-Q4 covering CI failure scope, Ruff configuration mismatch, affected lines, and validation tier  |
| Codebase scope                   | `.github/workflows/src-ci.yml`, `src/core/`, `src/api/`, `.copilot-tracking/*100*`                 |
| External scope                   | none (internal repository and PR #1792 CI check run metadata)                                      |
| Initial internal candidate areas | `.github/workflows/src-ci.yml`, `src/core/pyproject.toml`, `src/api/pyproject.toml`, `tokenomics.py`, `progress.py` |
| Initial external candidate areas | none                                                                                               |
| Research posture                 | focused                                                                                            |
| Posture provenance               | caller-specified (bounded internal `c2` lint/format fix with supplied CI failure context)          |
| Explicit limits / deadline       | Focused validation tier; commit locally on `feat/insight-100-mgmt-tokenomics`; do not push         |
| Posture-specific completion basis| focused scope and materiality                                                                      |
| Edits allowed during research?   | no, research-only                                                                                  |
| Resolved evidence root           | `.copilot-tracking/`                                                                               |
| Known constraints / excluded sources | Non-interactive session; preserve `d3a2c5405` runtime semantics; no push to origin             |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md`| `applyTo: "**"` matches repository and evidence   | Enforces D4/#1294 validation tiers, local mypy/ruff parity with `src-ci.yml`, and git commit rules | Selected: binding repo instruction |
| Skill               | `python-foundational`            | Semantic match to Python formatting/testing       | General Python tooling guidance              | Skipped: exact Ruff and unittest commands are governed by `src-ci.yml` and caller instructions |
| Skill               | `web-design-guidelines`          | Web UI changes under `src/api/.../web/`           | Web UI accessibility/design rules            | Skipped: no web UI files are in scope for `c2` |
| Research specialist | `hve-core-all:rpi-researcher`    | General delegated lane worker                     | Compact lane artifact under `subagents/`     | Skipped (inline): tightly coupled 2-file lint inspection completes faster and cleaner inline |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive execution with complete caller scope, exact target files, validation commands, and do-not-push rule | Not applicable (non-interactive) | Proceed directly in `focused` posture on `feat/insight-100-mgmt-tokenomics` |
| Direction change | No direction changes arose; Contrarian wave found test-glob selector nuance (`test_management_tokenomics_invariant_100.py` and `test_management_tokenomics_api_100.py`) solvable within Focused tier | Not applicable | Include both caller globs and exact `*tokenomics*` test modules during validation |
| Convergence      | Single Cycle 1 resolved all Q1-Q4 with high-confidence codebase and CI job evidence | Not applicable | Converge on package-scoped `ruff format` for the 2 files and advance to `Plan` |

## Scope and Success Criteria

* Scope: Inspect `d3a2c5405` diff, PR #1792 check-run results, `.github/workflows/src-ci.yml`, `src/core` and `src/api` `pyproject.toml`, and read-only `ruff check` / `ruff format --check --diff` outputs.
* Assumptions: Only `src/core/src/zava_forward/core/tokenomics.py` and `src/api/src/zava_forward/api/progress.py` fail `ruff format --check .` in their package directories, and no `ruff check .` diagnostics or web UI files are affected. (To verify in Cycle 1.)
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Verify and fix the `c2` Ruff `line-length = 100` formatting mismatch in `src/core/src/zava_forward/core/tokenomics.py` and `src/api/src/zava_forward/api/progress.py` via a complete dated `c2` RPI loop under Focused validation, committing locally with `Refs #100` and Co-authored-by trailer without pushing.
* Inferred research questions: Confirm whether any test files or other packages touched by `d3a2c5405` also fail package-scoped `ruff check .` or `ruff format --check .`, whether formatting triggers any new `ruff check` rules (such as import sorting or line-length), and why Focused tier applies under D4/#1294.
* Caller constraints and non-goals: Research phase is strictly read-only (`--check --diff` only); do not push to remote; preserve `d3a2c5405` functional behavior.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Restrict `c2` scope to `src-ci.yml` lint/format parity for PR #1792 (`d3a2c5405`) under Focused validation tier | User intake          | Focuses Cycle 1 on `src-ci.yml`, `pyproject.toml`, and package-scoped Ruff/mypy/test checks |
| exclude                                                  | Do not push commits to remote; leave clean frozen HEAD for coordinator review | User intake          | Constrains Plan/Implement git closeout to local commit only |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status   |
|---:|------------------|------------------------------------------|-----------|----------|
| Q1 | Which files were changed in `d3a2c5405` and which jobs passed/failed in PR #1792 hosted CI? | straightforward | H | answered |
| Q2 | How do `.github/workflows/src-ci.yml` and package `pyproject.toml` files configure `ruff check` and `ruff format`, and why did repo-root Ruff diverge? | straightforward | H | answered |
| Q3 | What exact lines in `src/core` and `src/api` (including tests) fail `ruff format --check --diff` or `ruff check .`, and could formatting alter runtime semantics or trigger lint/type issues? | depth | H | answered |
| Q4 | Does Focused validation tier apply under owner decision D4 / Issue #1294, and are any scenario-manifest hashes or web UI checks implicated? | straightforward | M | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/rpi-sessions/2026-11-15/insight-100-mgmt-tokenomics-state.json`, `.copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-changes.md`
* Reused (verified) findings: `c1` completed task `issue-100-mgmt-tokenomics` (`insight-100-mgmt-tokenomics`) on `feat/insight-100-mgmt-tokenomics` (`d3a2c5405`) targeting `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) with follow-ups RV-001, RV-002, and OD-51 recorded.
* Superseded / stale: `c1` validation ran `ruff check` without package-scoped `ruff format --check .` inside `src/core` and `src/api` (`line-length = 100`), leaving 2 files formatted at repo-root default `line-length = 88` and causing PR #1792 CI `src-core` and `src-api` Step 6 (`Lint`) failures.

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow (`c2` `src-ci.yml` lint/format parity under Focused tier); exclude (no push to remote)
* Active research posture and completion basis: focused; focused scope and materiality
* Explicit limits or deadline effect: Read-only checks only during Research; Focused validation tier and local-only commit constraint bound downstream phases

#### Wave 1: Wider

* Plan and independent lanes: Inline survey of `git show --stat d3a2c5405`, `gh pr view 1792`, `gh pr checks 1792`, `.github/workflows/src-ci.yml`, and `pyproject.toml` files across the repository.
* Worker evidence relationships or inline fallback: Inline execution mapped Q1 -> `d3a2c5405` (19 files changed across `.copilot-tracking/`, `src/core`, and `src/api`) and PR #1792 (`8/10` jobs passed; `src-core` and `src-api` failed) (`C1`, `C2`), and Q2 -> absence of a repo-root `pyproject.toml` vs `line-length = 100` in `src/core/pyproject.toml` and `src/api/pyproject.toml` (`C3`, `C4`).
* Reflection: Confirmed the branch (`feat/insight-100-mgmt-tokenomics`) and CI matrix configuration; prioritized exact step-failure verification and read-only `ruff format --check --diff .` inspection across all 302 `src/core` and 214 `src/api` formatted files in Wave 2.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Exact GitHub Actions failing step in jobs `132805147399` (`src-core`) and `132805147369` (`src-api`), and line-level formatting diffs in `src/core` and `src/api`.
* Plan and independent lanes: Inline inspection of `gh api repos/jmservera/ama/actions/jobs/{132805147399,132805147369}`, `(cd src/core && python3 -m ruff check . && python3 -m ruff format --check --diff .)`, `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check --diff .)`, and surrounding source lines in `tokenomics.py` and `progress.py`.
* Worker evidence relationships or inline fallback: Inline execution mapped Q1/Q2 -> Step 6 (`Lint`) as the sole failing step in both `src-core` and `src-api` after Step 5 (`Unit tests and dependency-rule test`) passed (`C2`); mapped Q3 -> 5 pure whitespace/line-wrap hunks in `src/core/src/zava_forward/core/tokenomics.py` (`514-516`, `708-710`, `722-724`, `810-812`, `866-868`) and 1 pure call-wrap hunk in `src/api/src/zava_forward/api/progress.py` (`239-245`), with `All checks passed!` from `ruff check .` in both packages (`C5`, `C6`).
* Reflection: Formatting changes are AST-identical whitespace adjustments; Wave 3 needs to challenge whether any other changed files were hidden by `[tool.ruff.format] exclude`, whether formatting could violate `ruff check` (`E501`/`I001`), and whether the caller's `unittest discover -p` globs actually select the `c1` Issue #100 test files.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge (1) whether `server.py` or test files in `d3a2c5405` hide latent lint/format mismatches, (2) whether caller-supplied `unittest -p` globs execute the Issue #100 invariant and API tests, and (3) whether D4/#1294 requires the full external RPI gate instead of Focused tier.
* Plan and independent lanes: Inline audit of `[tool.ruff.format] exclude` lists (`src/core/pyproject.toml:42-46`, `src/api/pyproject.toml:54-59`), `glob` over `src/core/tests/*tokenomics*` and `src/api/tests/*tokenomics*`, and D4/#1294 tier rules in `.github/copilot-instructions.md`.
* Worker evidence relationships or inline fallback:
  * Supports 2-file format target: `src/api/src/zava_forward/api/server.py` is intentionally listed in `[tool.ruff.format] exclude` (`C4`), while `test_management_tokenomics_invariant_100.py` and `test_management_tokenomics_api_100.py` already pass `ruff format --check .` at `line-length = 100` (`C5`, `C6`).
  * Challenges test-selector globs (`C7`): In `src/core/tests/`, `-p "test_tokenomics*.py"` matches `test_tokenomics_comparison.py` but omits `test_management_tokenomics_invariant_100.py`; in `src/api/tests/`, `-p "test_management_tokenomics_100.py"` matches `0` files because the actual file created in `d3a2c5405` is `test_management_tokenomics_api_100.py` (and `src/api` discovery benefits from `tests` in `PYTHONPATH`).
  * Supports Focused validation tier (`C8`): Whitespace-only formatting in 2 Python modules touches no SQL, Bicep/infra, Dockerfiles, dependency manifests, CI workflows, `src/api/checks/` recipes, or `src/api/src/zava_forward/api/web/` UI assets.
* Reflection: Contrarian check prevented a silent zero-test pitfall on `src/api` and missing `test_management_tokenomics_invariant_100.py` on `src/core`. Running both the caller's exact commands and `-p "test_*tokenomics*.py"` (with `tests` included in `src/api` `PYTHONPATH`) guarantees real test execution.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|----------------------------|
| Package-scoped `ruff format` on `tokenomics.py` and `progress.py` resolves all PR #1792 CI failures | `C1`, `C2`, `C3`, `C4`, `C5`, `C6` | accepted | Both `src-core` and `src-api` failed solely at Step 6 (`Lint`), and `ruff format --check --diff .` identifies only those 2 files across 516 checked files | Selected convergence recommendation |
| Augment validation test globs to include `-p "test_*tokenomics*.py"` alongside caller commands | `C7` | accepted | Prevents silent `Ran 0 tests` for `test_management_tokenomics_100.py` vs actual `test_management_tokenomics_api_100.py` and ensures `test_management_tokenomics_invariant_100.py` executes | Carried into Plan validation requirements |
| Classify `c2` as Focused tier under owner decision D4 / Issue #1294 | `C8` | accepted | Pure formatting change in 2 Python modules alters no AST, runtime logic, SQL, security boundary, `checks/` script, or `web/` asset | Recorded in Current Decisions and Planning Readiness |
| Modify root `pyproject.toml` to align repo-root Ruff with `line-length = 100` | `C3` | rejected | Out of scope for Issue #100 `c2` and would widen blast radius across `tools/`, `infra/`, and repository root | Recorded as rejected alternative |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: All four research questions (`Q1`-`Q4`) are answered with high-confidence primary codebase and CI job evidence; zero unresolved hypotheses remain.
* Revised brief or revalidation required: none
* Readiness effect: Ready (`C1`-`C8`)

## Evidence Log

* Delegation: inline: bounded 2-file `c2` formatting investigation where all evidence comes from direct local Ruff/git diffs and PR #1792 check-run metadata in fewer than 8 calls.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | `Source projects CI` runs matrix jobs with `working-directory: src/${{ matrix.project }}` and Step `Lint` running `ruff check . && ruff format --check .` | `.github/workflows/src-ci.yml:68-96` | view | high | Explains why package-local `pyproject.toml` governs CI formatting |
| C2 | Commit `d3a2c5405` on `feat/insight-100-mgmt-tokenomics` (`PR #1792` -> `feat/demo-164-chat-grounding-provenance-0900`) passed `8/10` CI jobs and failed `src-core` (`132805147399`) and `src-api` (`132805147369`) solely at Step 6 (`Lint`) after Step 5 (`Unit tests`) passed | `.copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-changes.md:1-15` | bash (`git show`, `gh pr checks`, `gh api`) | high | Verified exact head `d3a2c5405c22e9db2428a2839de69265938346a4` |
| C3 | `src/core/pyproject.toml` sets `[tool.ruff] line-length = 100` and does not exclude `tokenomics.py` in `[tool.ruff.format] exclude`; no root `pyproject.toml` exists in the repository | `src/core/pyproject.toml:26-46` | view / glob | high | Repo-root `ruff format` defaults to `line-length = 88` |
| C4 | `src/api/pyproject.toml` sets `[tool.ruff] line-length = 100`, excludes `server.py` under `[tool.ruff.format] exclude`, and formats `src/zava_forward/api/progress.py` at `line-length = 100` | `src/api/pyproject.toml:33-59` | view | high | Confirms why `progress.py` is checked and `server.py` was unaffected |
| C5 | Running `ruff check .` and `ruff format --check --diff .` in `src/core` passes lint (`All checks passed!`) and flags only `src/zava_forward/core/tokenomics.py` (`1 file would be reformatted, 301 files already formatted`) at 5 pure line-wrap hunks | `src/core/src/zava_forward/core/tokenomics.py:514-868` | bash / view | high | Hunks at lines `514-516`, `708-710`, `722-724`, `810-812`, `866-868` |
| C6 | Running `ruff check .` and `ruff format --check --diff .` in `src/api` passes lint (`All checks passed!`) and flags only `src/zava_forward/api/progress.py` (`1 file would be reformatted, 213 files already formatted`) at 1 pure call-wrap hunk | `src/api/src/zava_forward/api/progress.py:239-245` | bash / view | high | Re-indents `dict(tokenomics.store_ai_consumption_economics(...))` |
| C7 | Actual Issue #100 test modules created in `d3a2c5405` are `src/core/tests/test_management_tokenomics_invariant_100.py` (alongside `test_tokenomics_comparison.py`) and `src/api/tests/test_management_tokenomics_api_100.py` | `src/core/tests/test_management_tokenomics_invariant_100.py:1` | glob / view | high | `-p "test_*tokenomics*.py"` covers all tokenomics tests in both packages |
| C8 | Focused validation tier applies to bounded non-gate Python formatting fixes that do not alter SQL, deployment, Dockerfiles, workflows, `src/api/checks/`, or `src/api/src/zava_forward/api/web/` | `docs/case_study_48_addendum.md:1` | view | high | Per repository instructions (`owner decision D4, 2026-11-01, refined by issue #1294`) |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

No external sources used.

### Contradictions / Conflicts

* Caller prompt shorthand vs workspace filenames: Prompt prose refers to branch `feat/ai-100-mgmt-tokenomics` and test pattern `test_management_tokenomics_100.py`, whereas checked-out `PR #1792` (`d3a2c5405`) is branch `feat/insight-100-mgmt-tokenomics` (`C2`) and the `src/api` test module is `test_management_tokenomics_api_100.py` (`C7`); resolved by primary repository/PR state -> commit on the active checked-out branch `feat/insight-100-mgmt-tokenomics` and run both the caller-specified commands and `-p "test_*tokenomics*.py"` so every Issue #100 test suite executes.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `d3a2c5405` changed 19 files; PR #1792 passed `8/10` CI jobs and failed `src-core` and `src-api` solely in Step 6 (`Lint`). | `C1`, `C2` | high | Confirms zero functional, SQL, namespace, or container regressions in `d3a2c5405`. |
| Q2 | `src/core/pyproject.toml` and `src/api/pyproject.toml` set `line-length = 100`; absence of a root `pyproject.toml` caused root-invoked Ruff in `c1` to wrap at `88` columns. | `C1`, `C3`, `C4` | high | Formatting must be run inside `src/core` and `src/api`. |
| Q3 | Only `src/core/src/zava_forward/core/tokenomics.py` (5 hunks) and `src/api/src/zava_forward/api/progress.py` (1 hunk) require reformatting; all hunks are AST-neutral whitespace/parenthesis wraps. | `C5`, `C6` | high | Safe surgical 2-file formatting fix with zero behavioural impact. |
| Q4 | Focused tier applies under D4/#1294; no `checks/` manifest SHA-256 or `web/` UI checks apply, and running `-p "test_*tokenomics*.py"` alongside caller test commands guarantees full Issue #100 test execution. | `C7`, `C8` | high | Planning Readiness is `Ready`. |

## Key Discoveries

* `src/core/src/zava_forward/core/tokenomics.py` has 5 single-line collapse/wrap adjustments under `line-length = 100` (`514-516`, `708-710`, `722-724`, `810-812`, `866-868`) and `0` `ruff check` lint issues (`C5`).
* `src/api/src/zava_forward/api/progress.py` has 1 multiline call-indentation adjustment at lines `239-245` (`dict(tokenomics.store_ai_consumption_economics(...))`) and `0` `ruff check` lint issues (`C6`).
* Including `-p "test_*tokenomics*.py"` (and `tests` in `src/api` `PYTHONPATH`) ensures `test_management_tokenomics_invariant_100.py` (6 tests) and `test_management_tokenomics_api_100.py` (2 multi-endpoint HTTP tests) actually execute alongside `test_tokenomics_comparison.py` (`C7`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Run `python3 -m ruff format` from within `src/core` on `src/zava_forward/core/tokenomics.py` and from within `src/api` on `src/zava_forward/api/progress.py`, verify full package `ruff check .`, `ruff format --check .`, bare `mypy`, and Focused unit tests (both exact caller commands and `-p "test_*tokenomics*.py"`), and commit the 2 formatted files together with the complete dated `c2` `.copilot-tracking/` artifact set on `feat/insight-100-mgmt-tokenomics` without pushing.
* Rationale: Directly matches `.github/workflows/src-ci.yml` working-directory execution (`C1`), touches only the 2 failing files (`C5`, `C6`), preserves exact AST/runtime semantics, and keeps the diff minimal for coordinator review.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`
* Implementation impact: 2 Python source files reformatted + 7 new dated `c2` `.copilot-tracking/` artifacts committed locally on `feat/insight-100-mgmt-tokenomics`.
* Confidence: high: all CI failure logs and package-local Ruff diffs were directly reproduced.

File tree:

```text
src/
  core/src/zava_forward/core/tokenomics.py          (reformat to line-length=100)
  api/src/zava_forward/api/progress.py              (reformat to line-length=100)
.copilot-tracking/
  research/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-research.md
  plans/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-plan.md
  details/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-phase-details.md
  reviews/plans/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-plan-critique.md
  changes/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-changes.md
  reviews/logs/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-review.md
  rpi-sessions/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-state.json
```

### Alternative: Add a repository-root `pyproject.toml` setting `line-length = 100`

* Approach: Create a root `pyproject.toml` to prevent future root-level Ruff invocations from defaulting to `line-length = 88`.
* Trade-offs: Would avoid root-level CLI surprises, but alters repository-wide tool discovery across `tools/`, `infra/`, and root scripts outside Issue #100 scope.
* Evidence refs: `C1`, `C3`
* Rejection rationale: Out of scope for a surgical `c2` PR lint fix and violates minimal blast-radius discipline.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Ensure git author/committer local configuration uses privacy-safe `{id}+{login}@users.noreply.github.com` from `gh api user` before committing, and do not push to remote (`exclude` control).
* Follow-up: Prior `c1` follow-ups (`RV-002`, `RV-001`, and `OD-51` governance closure) remain tracked as post-Review follow-ups outside this `c2` formatting fix.
* Residual uncertainty: Hosted CI on PR #1792 (`src-core` and `src-api`) will remain red on remote until the coordinator pushes the new local commit.

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|------------|--------------|--------------|
| Reformat `tokenomics.py` and `progress.py` using package-local `ruff format` (`line-length = 100`) | confirmed | user / evidence | Sole failure in PR #1792 CI (`src-core`, `src-api` Step 6 `Lint`) | `C1`-`C6` | Zero semantic/AST change; restores 10/10 CI parity |
| Apply Focused validation tier and run both caller test commands and `-p "test_*tokenomics*.py"` | confirmed | constraint / evidence | D4/#1294 Focused tier applies; augmented glob ensures `test_management_tokenomics_invariant_100.py` and `test_management_tokenomics_api_100.py` execute | `C7`, `C8` | Full local verification of Ruff, mypy, and Issue #100 unit/HTTP suites |
| Commit locally on `feat/insight-100-mgmt-tokenomics` with `Refs #100` and Co-authored-by trailer; do not push | confirmed | user | Explicit caller boundary leaving frozen HEAD for coordinator review | `C2` | Remote PR #1792 push stays coordinator-owned |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| `OD-51` commercial tariff and spend-ceiling governance sign-off | Executive commercial sign-off and live Azure billing export reconciliation | Project owner | Required before closing Issue #100 as live reconciled economics (already handled via `"Unknown"` fail-closed invariant) | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Evaluate root Ruff workspace configuration across `tools/` and `infra/` | Prevents accidental `line-length = 88` formatting from repo root | Separate developer-tooling issue if requested by owner | deferred | Q2; `C3` |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation confirmed for package-scoped `ruff format` on `src/core/src/zava_forward/core/tokenomics.py` and `src/api/src/zava_forward/api/progress.py` under Focused validation tier.
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`
* Preconditions met: Exact CI failure step verified, read-only package-local Ruff diffs captured, zero semantic changes confirmed, validation selectors verified.
* Blockers: none
* Smallest action to change readiness: none (already `Ready`)

## Closeout Record

| Field | Record |
|-------|--------|
| Research execution status | Complete |
| Completed waves | Wider, Deeper, and Contrarian for Cycle 1 |
| Lane evidence or inline fallback | inline: bounded 2-file `c2` lint/format inspection completed directly against local Ruff/git and PR #1792 check-run metadata |
| Research disposition | executed |
| Planning Readiness | Ready (`C1`-`C8`) |
| Blockers | none |

* Missing or limited sections: External Evidence intentionally empty (internal codebase and CI metadata task).
