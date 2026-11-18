<!-- markdownlint-disable-file -->

# Task Research: issue-117-doc-scan-fix-rebase-0358b9ad5

| Field              | Value                                                                                                 |
|--------------------|-------------------------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                                            |
| Researcher / agent | rpi-research (under RPI Agent)                                                                        |
| Status             | Complete                                                                                              |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-research.md             |

## Research Brief

* What to research: Root cause and surgical fix options for `test_resident_acceptance_never_clears_technical_or_hazard_gates` (`JsonResidentDecisions` and `SqlResidentDecisions`) in `src/core/tests/test_resident_decisions.py:2526` relative to `is_available_case_document` (`src/core/src/zava_forward/core/doc_controls.py`) and `#117`'s fail-closed malware scan quarantine contracts (`test_technical_evidence_usability.py`, `test_document_rescan.py`, `test_resident_documents.py`, `src/api/tests/test_document_controls.py`), plus the rebase overlap from `fa6f8d1dd` (`5c5370a4a`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`).
* Why it matters: `PR #1781` (`5c5370a4a`) passed 9/10 CI checks and failed only `src-core` on those two test cases while the stacked parent branch advanced to `0358b9ad5`. Fixing the failure without weakening `#117` fail-closed quarantine on missing/malformed scan metadata ensures 10/10 CI alignment on the rebased branch.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` on branch `feat/demo-117-doc-scan`.
* Scope: `src/core/src/zava_forward/core/doc_controls.py`, `src/core/src/zava_forward/core/store.py`, `src/core/tests/test_resident_decisions.py`, `src/core/tests/test_technical_evidence_usability.py`, `src/core/tests/test_document_rescan.py`, `src/core/tests/test_resident_documents.py`, `src/api/tests/test_document_controls.py`, other test files constructing synthetic `documents` entries, git range `fa6f8d1dd..0358b9ad5`, and `.github/workflows/src-ci.yml`.
* Non-goals: Pushing to remote, opening/updating PRs, running `tools/rpi-checks.py`, adding HTTP routes, or mutating shared `~/.local` site-packages.
* Criteria: Every claim backed by `path:line` and read-only git inspection; fail-closed `#117` missing-scan invariants preserved unconditionally.
* Requested outputs: Converged fix + rebase recommendation and exact validation matrix.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                     |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Why did `test_resident_decisions.py:2526` fail, do any other tests construct raw synthetic `documents` stubs, what does `#117` require for missing scan fields, and what changed in `fa6f8d1dd..0358b9ad5`? |
| Codebase scope                       | `src/core/`, `src/api/tests/test_document_controls.py`, `.github/workflows/src-ci.yml`, `.copilot-tracking/`              |
| External scope                       | none                                                                                                                      |
| Initial internal candidate areas     | `src/core/src/zava_forward/core/doc_controls.py`, `src/core/tests/test_resident_decisions.py`, `src/core/tests/test_technical_evidence_usability.py`, `src/api/tests/test_document_controls.py` |
| Initial external candidate areas     | none                                                                                                                      |
| Research posture                     | focused                                                                                                                   |
| Posture provenance                   | default (bounded CI failure + stacked branch rebase with named files and commands)                                        |
| Explicit limits / deadline           | Do not push; leave clean committed worktree; match `src-ci.yml` focused validation.                                       |
| Posture-specific completion basis    | focused scope and materiality                                                                                             |
| Edits allowed during research?       | no, research-only                                                                                                         |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                      |
| Known constraints / excluded sources | Shared host `~/.local` editable installs; isolate via `PYTHONPATH`.                                                       |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                    | Match and provenance                                 | Scoped authority or output contract                                  | Selected / skipped reason                                                     |
|---------------------|----------------------------------------------|------------------------------------------------------|----------------------------------------------------------------------|-------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA repo) | `applyTo: "**"` matches workspace and tracking paths | Enforces KB reading, Focused tier, noreply git config, no-push       | Selected: mandatory repository governance                                     |
| Skill               | `git-merge` / `web-design-guidelines`        | Installed plugin/project skills                      | Git merge helper / Web UI guidelines                                 | Skipped: pure Python backend rebase and unit-test fixture fix (`0` web edits) |
| Research specialist | `hve-core-all:rpi-researcher`                | General research lane subagent                       | Bounded subagent lane artifact                                       | Skipped (inline preferred): bounded 4-file inspection completed in <6 calls   |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered  | Resulting decision or selected further research                                 |
|------------------|-------------------------------------------------------------------------------------------------------|-----------------------|---------------------------------------------------------------------------------|
| Intake           | Explicit non-interactive caller brief specifies exact CI failure, rebase ref, validation, and no-push | N/A (non-interactive) | Execute focused 3-wave cycle inline.                                            |
| Direction change | None.                                                                                                 | N/A                   | Keep surgical fixture fix + rebase onto `0358b9ad5` + focused CI validation.    |
| Convergence      | Failure reproduced and contrasted against `#117` missing-scan quarantine contract and `merge-tree`.   | Converged             | Proceed to `rpi-plan` with `Planning Readiness: Ready`.                         |

## Scope and Success Criteria

* Scope: Rebase `feat/demo-117-doc-scan` (`5c5370a4a`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`), update the synthetic uploaded-evidence stub in `src/core/tests/test_resident_decisions.py:2522-2524` so it carries explicit clean synthetic scan metadata without weakening `is_available_case_document`, run focused `src-ci.yml` validation across `src/core` and `src/api`, and commit updated `.copilot-tracking/` artifacts cleanly without pushing.
* Assumptions:
  * Auto-merged hunks in `assistants.py` (`#146` monitoring declarations) and `doc_controls.py` (`#109` sensor non-authority refusal) remain orthogonal to `#117`'s malware scan quarantine checks.
* Success criteria:
  * Every research question is answered with workspace `path:line` evidence.
  * Findings, alternatives, and readiness cite stable `C1`–`C8` evidence IDs.
  * `#117` fail-closed quarantine on missing `scan` / `scan_status` remains intact.

## Task Research Requests

* Explicit requests:
  1. Rebase `feat/demo-117-doc-scan` onto the latest parent branch `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`).
  2. Fix `test_resident_acceptance_never_clears_technical_or_hazard_gates` (`JsonResidentDecisions` and `SqlResidentDecisions`) while keeping all `#117` tests (`test_technical_evidence_usability.py`, `test_document_rescan.py`, `test_resident_documents.py`, `src/api/tests/test_document_controls.py`) passing.
  3. Run focused validation matching `src-ci.yml` across `src/core` and `src/api`.
  4. Update `.copilot-tracking/` RPI artifacts for `#117` and commit cleanly with the `Co-authored-by` trailer without pushing.
* Inferred research questions:
  * Why does `test_resident_decisions.py:2526` fail while `dataset.py`'s `supplied_resident_fixture` and all 9 other CI jobs pass?
  * Would relaxing `is_available_case_document` for `generated=False` without `scan` violate `#117` and break `test_technical_evidence_usability.py`?
  * Do any commits in `fa6f8d1dd..0358b9ad5` conflict with `5c5370a4a` or introduce additional raw `generated=False` document stubs?
  * What `ruff` / `mypy` constraints apply to `src/core/tests/test_resident_decisions.py` and auto-merged `doc_controls.py` / `assistants.py`?
* Caller constraints and non-goals: Do not push; leave clean worktree; non-interactive autonomous execution.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                 |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|-------------------------------------------------------------------|
| narrow                                                   | Focused validation matching `src-ci.yml` (`unittest`, `ruff check`, `ruff format --check`, `mypy`)      | Caller intake       | Targets exact static and behavioral checks in `src/core` & `api`. |
| exclude                                                  | Do not push to remote; do not weaken `#117` fail-closed missing-scan quarantine.                        | Caller / security   | Local git commits and worktree-scoped `PYTHONPATH`.               |

## Research Questions

|  # | Sub-question                                                                                                                                      | Type (depth / breadth / straightforward) | Priority | Status   |
|---:|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|----------|
| Q1 | Why did `test_resident_acceptance_never_clears_technical_or_hazard_gates` fail at `test_resident_decisions.py:2526`?                              | depth                                    | H        | answered |
| Q2 | Should the fix update `test_resident_decisions.py` or `is_available_case_document`, and how does that interact with `#117` usability invariants?  | depth                                    | H        | answered |
| Q3 | What commits landed in `fa6f8d1dd..0358b9ad5`, do any files conflict during rebase, and did any new tests add raw `documents` stubs?              | breadth                                  | H        | answered |
| Q4 | Which formatting, lint, and strict-typing gates apply to `test_resident_decisions.py` and the rebased `src/core` / `src/api` suites?              | straightforward                          | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-15/issue-117-doc-scan-research.md`, `.copilot-tracking/research/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-research.md`, `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-state.json`, and `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-state.json`.
* Reused (verified) findings:
  * `e9c31f7fa` (`feat(core): quarantine uploads until malware scan is clean`) enforces fail-closed `is_available_case_document` across `Store.focus`, `Store.checklist`, `signoffs.missing_items`, and all derivative consumers, with zero `server.py` route changes.
* Superseded / stale:
  * Parent branch `origin/feat/demo-164-chat-grounding-provenance-0900` advanced 6 commits from `fa6f8d1dd` to `0358b9ad5` (`704c6b07a` #1775, `6bdcf7f90` #1777, `e282dc327` #1778, `2c5402f9a` #1779, `3aacab3a6` #1780, `0358b9ad5` #1782).
  * `src-core` full `unittest discover` exposed `test_resident_decisions.py:2522-2526`, which was not included in the prior rebase's subset test command.

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow (focused `src-ci.yml` validation), exclude (no push, preserve `#117` fail-closed missing-scan quarantine).
* Active research posture and completion basis: `focused`; focused scope and materiality.
* Explicit limits or deadline effect: none.

#### Wave 1: Wider

* Plan and independent lanes: Inline breadth inspection of `git ls-remote`, `git log fa6f8d1dd..0358b9ad5`, `git merge-tree --write-tree --messages 0358b9ad5 5c5370a4a`, repository-wide `grep` for `["documents"] =`, and `.github/workflows/src-ci.yml`.
* Worker evidence relationships or inline fallback: Inline:
  * Q3 -> `origin/feat/demo-164-chat-grounding-provenance-0900` is at `0358b9ad51435387057d08293a8a42846abd2cef` (6 commits ahead of `fa6f8d1dd`) (`C1`). Read-only `git merge-tree --write-tree --messages 0358b9ad5 5c5370a4a` exits `0` with zero conflicts, cleanly auto-merging `assistants.py` and `doc_controls.py` (`C2`).
  * Q1 -> Running `PYTHONPATH=src:tests python3 -m unittest test_resident_decisions -q` reproduces the exact 2 failures (`JsonResidentDecisions` and `SqlResidentDecisions` in `test_resident_acceptance_never_clears_technical_or_hazard_gates`) out of 434 tests (`C3`).
* Reflection: Rebase onto `0358b9ad5` is conflict-free, and the CI failure reproduces deterministically. Proceed to Wave 2 to inspect `is_available_case_document`, `dataset.py`, `test_technical_evidence_usability.py`, and the 2 auto-merged files.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Exact contract of `is_available_case_document` (`doc_controls.py`), synthetic fixture conventions (`dataset.py`), `#117` missing-scan assertions (`test_technical_evidence_usability.py`), and upstream hunks in `doc_controls.py` and `assistants.py`.
* Plan and independent lanes: Inline file-range and git-diff inspection.
* Worker evidence relationships or inline fallback: Inline:
  * Q1, Q2 -> In `doc_controls.py:183-190`, `is_available_case_document(doc)` returns `True` when `doc.get("generated") is True`, checks `scan_status(doc) == "clean"` whenever `doc.get("generated") is False or "scan" in doc or "scan_status" in doc`, and returns `True` only for legacy/synthetic dicts that omit all three keys (`C4`). In `test_resident_decisions.py:2522-2524`, the test constructs `dict(id=f"SYN-{kind}", kind=kind, generated=False)` with `generated=False` and no `scan` dict solely as a pre-state setup to verify `self.store.detail("ZF-1")["gate"] == []` before returning the `coordination` sign-off and proving that resident acceptance never clears technical or hazard gates (`C3`).
  * Q2 -> By contrast, `dataset.py:113-115` (`supplied_resident_fixture`) already constructs valid synthetic uploaded evidence with `scan=dict(status="clean", scanner="Synthetic metadata fixture")` (`C5`), while `test_technical_evidence_usability.py:16-17,29-31,39-67` explicitly asserts that `dict(kind=k, generated=False)` with missing `scan` MUST fail closed (`is_available_case_document(item)` is `False`, `Store.checklist` marks `present=False`, and `missing_items` reports `Evidence: <kind>`) (`C6`).
  * Q3 -> In `fa6f8d1dd..0358b9ad5`, `doc_controls.py` adds `#109` sensor non-authority refusal checks in `_manager`, `place_legal_hold`, and `release_legal_hold` plus `from . import controls` (`C7`), and `assistants.py` adds `#146` `monitoring_status` declarations around lines 1582-1619 (`C7`); both are completely disjoint from `#117`'s `scan_status` / `is_available_case_document` / `assistants` document-context hunks.
* Reflection: Updating `test_resident_decisions.py:2522-2524` to include `scan=dict(status="clean", scanner="Synthetic metadata fixture")` matches `dataset.py:113-115` and preserves 100% of `#117`'s fail-closed security contract. Proceed to Wave 3 Contrarian checks.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries:
  1. What if we instead changed `is_available_case_document` to allow `generated=False` when `"id"` starts with `"SYN-"` or when `"scan"` is absent?
  2. Did any other test in `src/core/tests/` (including the 6 new commits in `fa6f8d1dd..0358b9ad5`) construct `generated=False` documents without `scan`, or could full `src/core` test discovery uncover any other failure?
  3. Is `test_resident_decisions.py` subject to strict `ruff format --check` and `mypy --strict` (unlike the legacy-exempt files in `pyproject.toml`)?
* Plan and independent lanes: Inline audit of `pyproject.toml`, `grep` across `src/**/tests/**` in `fa6f8d1dd..0358b9ad5`, and `doc_controls.py` security invariants.
* Worker evidence relationships or inline fallback: Inline:
  * Relaxing `is_available_case_document` for missing `scan` would directly break `TechnicalEvidenceUsability.test_missing_scan_does_not_satisfy_evidence` and `test_failed_infected_malformed_and_conflicting_statuses_fail_closed` (`test_technical_evidence_usability.py:29-67`) AND create a production quarantine bypass if any unmigrated upload record lacked `"scan"`, or an unacceptable `"SYN-"` ID backdoor in production security logic (`C4`, `C6`).
  * Searching `src/core/tests/test_resident_decisions.py` and the entire `fa6f8d1dd..0358b9ad5` test diff for `documents` / `generated` confirms `test_resident_decisions.py:2522-2524` is the sole `generated=False` un-scanned fixture expecting clean evidence availability (`C3`, `C7`). Running full `unittest discover -s tests -q` in `src/core` after rebase in `rpi-implement` will additionally prove 100% parity with `src-ci.yml` (`C8`).
  * `src/core/pyproject.toml:42-70` does NOT exempt `tests/test_resident_decisions.py` from `ruff format`, `ruff check`, or `mypy --strict`, so the multi-line list comprehension in `test_resident_decisions.py` must adhere strictly to `ruff format` (100-char line length) and strict typing (`C8`). Auto-merged imports in `doc_controls.py` (`from . import controls` above `from .documents import ...`) are already alphabetically sorted (`C7`, `C8`).
* Reflection: Contrarian checks confirm both why `doc_controls.py` must NOT be weakened and that `test_resident_decisions.py` must pass strict `ruff format` and `mypy`.

#### Parent Synthesis and Disposition

| Material / claim                                                                                                                               | Evidence IDs | Parent disposition | Evidence-based rationale                                                                                              | Primary-artifact treatment |
|------------------------------------------------------------------------------------------------------------------------------------------------|--------------|--------------------|-----------------------------------------------------------------------------------------------------------------------|----------------------------|
| Add `scan=dict(status="clean", scanner="Synthetic metadata fixture")` to the synthetic setup stub at `test_resident_decisions.py:2522-2524`    | C3, C5, C6   | accepted           | Matches `dataset.py:113-115` (`supplied_resident_fixture`), fixes both JSON and SQL tests, and keeps `#117` intact.   | Selected recommendation    |
| Rebase `feat/demo-117-doc-scan` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`) cleanly                               | C1, C2, C7   | accepted           | `git merge-tree` exits `0` with clean, orthogonal auto-merges in `doc_controls.py` (`#109`) and `assistants.py` (`#146`). | Selected recommendation    |
| Run both the targeted `src-ci.yml` commands and full `src/core` `unittest discover` with worktree-local `PYTHONPATH`                           | C8           | accepted           | Proves exact `src-core` CI job parity alongside `#117` core and API suites without mutating `~/.local`.               | Selected recommendation    |
| Relax `is_available_case_document` for `generated=False` documents missing `scan` or matching `"SYN-*"` IDs                                    | C4, C6       | rejected           | Violates `#117` fail-closed quarantine invariant and breaks `test_technical_evidence_usability.py:29-67`.             | Rejected alternative       |

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Exact root cause, canonical fixture convention, conflict-free merge-tree simulation onto `0358b9ad5`, and strict lint/format/type constraints are 100% verified.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded CI failure and 2-file auto-merge verified directly via read-only git, grep, view, and unittest reproduction.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | `origin/feat/demo-164-chat-grounding-provenance-0900` is at `0358b9ad51435387057d08293a8a42846abd2cef`, 6 commits ahead of `fa6f8d1dd` (`#1775`, `#1777`, `#1778`, `#1779`, `#1780`, `#1782`). | `src/core/README.md:1` | bash (`git ls-remote`, `git log`) | high | Latest stacked parent tip |
| C2 | `git merge-tree --write-tree --messages 0358b9ad5 5c5370a4a` exits `0` with zero conflicts, auto-merging `assistants.py` and `doc_controls.py`. | `src/core/src/zava_forward/core/doc_controls.py:29` | bash (`git merge-tree`) | high | Conflict-free rebase |
| C3 | `test_resident_acceptance_never_clears_technical_or_hazard_gates` sets `dict(id=f"SYN-{kind}", kind=kind, generated=False)` as pre-state setup before asserting `gate == []` at line 2526, causing the sole 2 failures out of 434 tests in `test_resident_decisions.py`. | `src/core/tests/test_resident_decisions.py:2522` | view / bash (`unittest`) | high | Exact reproduction of `PR #1781` `src-core` failure |
| C4 | `is_available_case_document` enforces `scan_status(doc) == "clean"` whenever `doc.get("generated") is False or "scan" in doc or "scan_status" in doc`. | `src/core/src/zava_forward/core/doc_controls.py:183` | view | high | Core `#117` fail-closed gate |
| C5 | Canonical synthetic fixture helper `supplied_resident_fixture` constructs uploaded evidence stubs with `scan=dict(status="clean", scanner="Synthetic metadata fixture")`. | `src/core/tests/dataset.py:113` | view | high | Established repository test convention |
| C6 | `TechnicalEvidenceUsability` explicitly asserts that `dict(kind=k, generated=False)` with no `scan` fails closed (`is_available_case_document` is `False` and `Evidence: <kind>` remains missing). | `src/core/tests/test_technical_evidence_usability.py:29` | view | high | Prohibits weakening `is_available_case_document` |
| C7 | Upstream `fa6f8d1dd..0358b9ad5` changes in `doc_controls.py` (`#109` sensor refusal) and `assistants.py` (`#146` monitoring status) are disjoint from `#117` hunks, and no new tests add un-scanned `generated=False` document fixtures. | `src/core/src/zava_forward/core/doc_controls.py:141` | bash (`git diff`, `git show`) | high | Auto-merge is semantically clean |
| C8 | `tests/test_resident_decisions.py` is NOT in `src/core/pyproject.toml` format/lint/mypy exclusions and must pass `ruff check`, `ruff format --check` (line-length 100), and `mypy --strict` alongside `src-ci.yml` unit suites. | `src/core/pyproject.toml:34` | view | high | Strict style and typing required |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* `none`

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `test_resident_decisions.py:2522-2524` constructs `generated=False` upload stubs without `scan` metadata when setting up a clean pre-gate state, so `#117`'s `is_available_case_document` rightly quarantines all 4 `EVIDENCE` items and leaves `gate` non-empty at line 2526. | C3, C4 | high | Pinpoints exact 3-line setup defect in `test_resident_decisions.py`. |
| Q2 | Adding `scan=dict(status="clean", scanner="Synthetic metadata fixture")` in `test_resident_decisions.py:2522-2524` aligns with `dataset.py:113-115` while preserving `#117` fail-closed missing-scan quarantine tested in `test_technical_evidence_usability.py`. | C4, C5, C6 | high | Unambiguous surgical test-fixture fix; zero production weakening. |
| Q3 | Rebasing `5c5370a4a` onto `0358b9ad5` has zero merge conflicts; auto-merges in `doc_controls.py` and `assistants.py` are orthogonal (`#109` sensor refusal and `#146` monitoring status), and no upstream tests introduce raw `generated=False` stubs. | C1, C2, C7 | high | Clean `git rebase` onto `0358b9ad5`. |
| Q4 | `test_resident_decisions.py` is strictly linted, formatted (`ruff format`), and type-checked (`mypy --strict`); worktree-local `PYTHONPATH` matches `src-ci.yml` validation across `src/core` and `src/api`. | C8 | high | Ready for `rpi-plan` -> `rpi-implement` -> `rpi-review`. |

## Key Discoveries

* `test_resident_decisions.py:2522-2524` used `dict(id=f"SYN-{kind}", kind=kind, generated=False)` without `scan` metadata solely to clear the technical gate in pre-state setup, whereas `dataset.py:113-115` (`supplied_resident_fixture`) uses `scan=dict(status="clean", scanner="Synthetic metadata fixture")` and `test_technical_evidence_usability.py:29-67` mandates that `generated=False` without `scan` fail closed (`C3`, `C4`, `C5`, `C6`).
* Read-only `git merge-tree` proves rebasing `5c5370a4a` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`) succeeds with zero conflicts (`C1`, `C2`, `C7`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Keep tracked files clean while rebasing `feat/demo-117-doc-scan` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`); update `src/core/tests/test_resident_decisions.py:2522-2524` to include `scan=dict(status="clean", scanner="Synthetic metadata fixture")` formatted cleanly for `ruff format` and `mypy --strict` while keeping `is_available_case_document` unchanged; run all requested focused `src-ci.yml` validation commands plus full `src/core` unit discovery; and commit the code fix and finalized `.copilot-tracking/` RPI artifacts cleanly with the `Co-authored-by` trailer without pushing.
* Rationale: Fixes both `JsonResidentDecisions` and `SqlResidentDecisions` failures at their exact synthetic fixture source, matches `dataset.py:113-115`, preserves 100% of `#117` fail-closed malware scan quarantine invariants, and rebases cleanly onto `0358b9ad5`.
* Evidence refs: C1, C2, C3, C4, C5, C6, C7, C8
* Implementation impact: Conflict-free rebase onto `0358b9ad5`, 1-comprehension fixture update in `src/core/tests/test_resident_decisions.py`, focused validation in `src/core` and `src/api`, and clean local commits.
* Confidence: high: reproduced failure and verified merge-tree and `#117` invariants directly.

### Alternative: Relax `is_available_case_document` When `"scan"` Is Absent on `generated=False` Stubs

* Approach: Treat `generated=False` documents without `"scan"` or `"scan_status"` (or with `"SYN-"` IDs) as available in `src/core/src/zava_forward/core/doc_controls.py`.
* Trade-offs: Avoids touching `test_resident_decisions.py`, but breaks `test_technical_evidence_usability.py:29-67` and introduces a fail-open quarantine hole or synthetic-ID backdoor in production security logic.
* Evidence refs: C4, C6
* Rejection rationale: Directly violates Issue `#117` fail-closed quarantine requirements.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Format the updated comprehension in `src/core/tests/test_resident_decisions.py` cleanly for `ruff format --check` and run full `src/core` unit discovery in addition to the targeted `#117` test modules so no other `src-core` regression can hide.
* Follow-up: Parent `#117` follow-ups (`RV-001` direct `SqlStore.rescan_pending` test, Azure Storage Defender Bicep tags, and DPO/Legal retention schedule governance) remain tracked in `prioritized_follow_ups`.
* Residual uncertainty: none

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Rebase `feat/demo-117-doc-scan` onto `0358b9ad5` and add `scan=dict(status="clean", scanner="Synthetic metadata fixture")` in `test_resident_decisions.py:2522-2524` without weakening `is_available_case_document` | confirmed | user / evidence | Matches `dataset.py:113-115` and preserves `#117` fail-closed missing-scan quarantine | C1, C2, C3, C4, C5, C6 | Clears `src-core` CI failure with zero security regression |
| Run focused `src-ci.yml` validation across `src/core` and `src/api` plus full `src/core` `unittest discover`, commit cleanly with `Co-authored-by` trailer, and do not push | confirmed | user / constraint / evidence | Guarantees `src-core` and `src-api` CI parity and clean worktree for coordinator | C7, C8 | Ready for coordinator review and push |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| none | none | none | none | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | none | Root cause, rebase boundary, and validation matrix are 100% determined | Only if parent branch advances again | no | Q1–Q4; C1–C8 |

## Planning Readiness

* Status: Ready
* Decision state: Converged on conflict-free rebase onto `0358b9ad5`, adding clean synthetic scan metadata to `test_resident_decisions.py:2522-2524` while keeping `is_available_case_document` fail-closed, running `src-ci.yml` validation across `src/core` and `src/api`, and committing code + `.copilot-tracking/` artifacts cleanly without pushing.
* Evidence basis: C1, C2, C3, C4, C5, C6, C7, C8
* Preconditions met: `origin/feat/demo-164-chat-grounding-provenance-0900` verified at `0358b9ad5`; `git merge-tree` exit `0` verified; failure reproduced read-only.
* Blockers: none
* Smallest action to change readiness: none

## Closeout Record

| Field                            | Record                                                                                     |
|----------------------------------|--------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                   |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian                                                     |
| Lane evidence or inline fallback | inline: CI failure reproduction, `#117` invariants, and `0358b9ad5` merge-tree verified    |
| Research disposition             | executed                                                                                   |
| Planning Readiness               | Ready (C1–C8)                                                                              |
| Blockers                         | none                                                                                       |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic continuation to `rpi-plan`                        |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (C1–C8)                                                                                                |
| Output mode and planning support | convergence; yes — surgical fixture correction, conflict-free rebase, and `src-ci.yml` validation commands   |

