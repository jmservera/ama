<!-- markdownlint-disable-file -->

# Task Research: issue-117-doc-scan-rebase-fa6f8d1dd

| Field              | Value                                                                                           |
|--------------------|-------------------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                                      |
| Researcher / agent | rpi-research (under RPI Agent)                                                                  |
| Status             | Complete                                                                                        |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-research.md           |

## Research Brief

* What to research: Exact commit ancestry, file overlap, three-way merge conflict boundary, semantic interactions across overlapping `src/core` modules, Python environment isolation, and focused validation commands required to rebase `feat/demo-117-doc-scan` (`4d91dae33`, anchored on `243764945`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`, incorporating PR #1773 `36aeddae3`, PR #1768 `f71331d42`, and PR #1774 `fa6f8d1dd`).
* Why it matters: Guarantees a clean, zero-regression rebase that preserves both `#76`'s statutory/operational safety clock and named-owner projection in `Store.focus` and `#117`'s fail-closed `is_available_case_document(d)` quarantine gate across all download and derivative consumers, while validating against the local worktree code and leaving `git status --short` empty without pushing.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` on branch `feat/demo-117-doc-scan`.
* Scope: Git commits `243764945..fa6f8d1dd` and `243764945..4d91dae33`, overlapping files (`store.py`, `taskqueues.py`, `projection.py`, `chat_case_answers.py`), `.copilot-tracking/` `#117` tracking records, and focused validation runners (`ruff`, `mypy`, `unittest` in `src/core` and `src/api`).
* Non-goals: Pushing to remote, opening or editing GitHub PRs, running `tools/rpi-checks.py`, adding HTTP routes in `server.py`, or mutating shared user-site `pip` installs used by other worktrees.
* Criteria: Every claim grounded in workspace `path:line` and read-only git inspection (`git merge-tree`); conflict hunks, auto-merged modules, and worktree-isolated `PYTHONPATH`/`MYPYPATH` validation commands verified cleanly.
* Requested outputs: Converged conflict-resolution, validation, and post-rebase tracking commit plan input.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                                              |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Which files overlap between `fa6f8d1dd` and `4d91dae33`, what exact merge conflict occurs, are auto-merges semantically safe, and how must validation isolate cwd? |
| Codebase scope                       | `src/core/src/zava_forward/core/{store,taskqueues,projection,chat_case_answers,doc_controls}.py`, `src/{core,api}/pyproject.toml`, `src/{core,api}/tests/`, `.copilot-tracking/` |
| External scope                       | none                                                                                                                                                               |
| Initial internal candidate areas     | `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/taskqueues.py`, `src/core/src/zava_forward/core/projection.py`, `src/core/src/zava_forward/core/chat_case_answers.py` |
| Initial external candidate areas     | none                                                                                                                                                               |
| Research posture                     | focused                                                                                                                                                            |
| Posture provenance                   | default (bounded internal rebase continuation with named source commit `4d91dae33`, target commit `fa6f8d1dd`, and single 2-line conflict hunk)                    |
| Explicit limits / deadline           | Do not push; leave `git status --short` empty; focused validation tier (`ruff check .`, `ruff format --check .`, `mypy`, and `#117` tests in `src/core` & `src/api`). |
| Posture-specific completion basis    | focused scope and materiality                                                                                                                                      |
| Edits allowed during research?       | no, research-only                                                                                                                                                  |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                                               |
| Known constraints / excluded sources | Shared non-sandboxed host environment where `~/.local` editable installs point to another worktree; must isolate via worktree-local `PYTHONPATH`/`MYPYPATH`.       |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                    | Match and provenance                                 | Scoped authority or output contract                                    | Selected / skipped reason                                                       |
|---------------------|----------------------------------------------|------------------------------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA repo) | `applyTo: "**"` matches workspace and tracking paths | Enforces KB reading, Focused tier, noreply git config, no-push         | Selected: mandatory repository governance                                       |
| Skill               | `git-merge` / `web-design-guidelines`        | Installed plugin/project skills                      | Git merge helper / Web UI guidelines                                   | Skipped: pure Python backend rebase (`0` web files modified in `4d91dae33`)     |
| Research specialist | `hve-core-all:rpi-researcher`                | General research lane subagent                       | Bounded subagent lane artifact                                         | Skipped (inline preferred): 4 overlapping files verified directly in <5 calls   |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered  | Resulting decision or selected further research                                 |
|------------------|-------------------------------------------------------------------------------------------------------|-----------------------|---------------------------------------------------------------------------------|
| Intake           | Explicit non-interactive caller brief specifies exact commits, target ref, validation, and no-push.   | N/A (non-interactive) | Execute focused 3-wave cycle inline.                                            |
| Direction change | None.                                                                                                 | N/A                   | Keep strict rebase + conflict-resolution + focused validation + tracking scope. |
| Convergence      | `git merge-tree --write-tree --messages fa6f8d1dd 4d91dae33` proves exact single-hunk conflict.       | Converged             | Proceed to `rpi-plan` with `Planning Readiness: Ready`.                         |

## Scope and Success Criteria

* Scope: Rebase `4d91dae33` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`), resolve `src/core/src/zava_forward/core/store.py`, run focused validation across `src/core` and `src/api`, and record/commit tracking updates cleanly.
* Assumptions:
  * Auto-merged hunks in `chat_case_answers.py`, `projection.py`, and `taskqueues.py` remain semantically orthogonal.
  * Prepending this worktree's `src/` and `tests/` paths in `PYTHONPATH` and `MYPYPATH` prevents cross-worktree editable-install leakage without disturbing shared `~/.local` packages.
* Success criteria:
  * Every research question is answered with `path:line` evidence.
  * Findings, decisions, and readiness claims cite Evidence Log IDs (`C1`–`C8`).
  * Alternatives are compared and one convergence recommendation is selected.

## Task Research Requests

* Explicit requests:
  1. Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`) and rebase `feat/demo-117-doc-scan` onto `origin/feat/demo-164-chat-grounding-provenance-0900`.
  2. Run focused validation (`ruff check .`, `ruff format --check .`, `mypy`, and the `#117` document malware scan quarantine tests in `src/core` and `src/api`) on the rebased HEAD, and leave `git status --short` empty. Do not push.
* Inferred research questions:
  * Which exact commits and files overlap between `243764945..fa6f8d1dd` and `4d91dae33`?
  * Why does `store.py` conflict and how do `#76` safety items and `#117` clean-document filtering compose?
  * How do we ensure `unittest` and `mypy` evaluate `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan` rather than another worktree's `~/.local` editable install?
  * How must `.copilot-tracking/` state/artifacts be persisted and committed so `git status --short` is empty on exit without amending commits unnecessarily?
* Caller constraints and non-goals: Do not push; leave `git status --short` empty; non-interactive autonomous execution.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                                  | Source / checkpoint | Effect on active brief, evidence, or revalidation                 |
|----------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|---------------------|-------------------------------------------------------------------|
| narrow                                                   | Focused validation tier: `ruff check .`, `ruff format --check .`, `mypy`, and `#117` unit tests in `src/core`/`src/api` | Caller intake       | Targets exact static and behavioral checks on rebased HEAD.       |
| exclude                                                  | Do not push to remote; do not modify shared environment outside this worktree.                                         | Caller / host rules | Local git operations and worktree-scoped `PYTHONPATH`/`MYPYPATH`. |

## Research Questions

|  # | Sub-question                                                                                                                                             | Type (depth / breadth / straightforward) | Priority | Status   |
|---:|----------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|----------|
| Q1 | What commits landed between `243764945` and `fa6f8d1dd`, and which files intersect with `4d91dae33`?                                                     | straightforward                          | H        | answered |
| Q2 | What exact lines conflict in `src/core/src/zava_forward/core/store.py`, and how do both sides' changes compose?                                          | depth                                    | H        | answered |
| Q3 | Are the 3 auto-merged files (`chat_case_answers.py`, `projection.py`, `taskqueues.py`) and `pyproject.toml` free of semantic, lint, or `mypy` collisions? | depth                                    | H        | answered |
| Q4 | How must Python test/type runners and `.copilot-tracking/` commits be sequenced so validation tests this worktree and `git status --short` ends empty?   | depth                                    | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-15/issue-117-doc-scan-research.md`, `.copilot-tracking/plans/2026-11-15/issue-117-doc-scan-plan.md`, `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md`, `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-state.json`, and sibling rebase artifacts `issue-154-rep-expiry-views-rebase-0c1fa1da4-*` / `issue-116-entra-output-0052-c1-rebase-*`.
* Reused (verified) findings:
  * `4d91dae33` touches 19 source/test files across `src/core` and `src/api/tests/test_document_controls.py` plus 7 `.copilot-tracking/` files, with zero edits to `src/api/src/zava_forward/api/server.py`.
* Superseded / stale:
  * Parent tip `origin/feat/demo-164-chat-grounding-provenance-0900` advanced from `243764945` to `fa6f8d1dd` via 3 squash-merged PRs: `36aeddae3` (#1773, Refs #215), `f71331d42` (#1768, Refs #76), and `fa6f8d1dd` (#1774, Refs #216).

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow (focused validation tier), exclude (no push, preserve shared host environment).
* Active research posture and completion basis: `focused`; focused scope and materiality.
* Explicit limits or deadline effect: none.

#### Wave 1: Wider

* Plan and independent lanes: Inline breadth inspection of `git fetch`, commit range `243764945..fa6f8d1dd`, `comm -12` file intersection with `4d91dae33`, and `git merge-tree --write-tree --messages origin/feat/demo-164-chat-grounding-provenance-0900 4d91dae33`.
* Worker evidence relationships or inline fallback: Inline:
  * Q1 -> Remote branch `origin/feat/demo-164-chat-grounding-provenance-0900` resolves to `fa6f8d1dd0493342718a70c134dd9fcb3305cd6c` (`36aeddae3`, `f71331d42`, `fa6f8d1dd` above `243764945`) (`C1`). Only 4 files overlap between `4d91dae33` and `243764945..fa6f8d1dd`: `chat_case_answers.py`, `projection.py`, `store.py`, and `taskqueues.py` (`C2`). `git merge-tree` proves 3 of the 4 auto-merge cleanly and `src/core/src/zava_forward/core/store.py` has the sole conflict (`C2`).
* Reflection: Conflict surface is a single file (`store.py`). Proceed to Wave 2 to inspect exact hunks across all 4 overlapping files and `pyproject.toml`.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Line-by-line inspection of `store.py`, `chat_case_answers.py`, `projection.py`, `taskqueues.py`, and `src/{core,api}/pyproject.toml`.
* Plan and independent lanes: Inline diff and file-range inspection.
* Worker evidence relationships or inline fallback: Inline:
  * Q2 -> In `src/core/src/zava_forward/core/store.py`:
    * Imports (`store.py:51,57`): `4d91dae33` updates line 51 (`from .doc_controls import DocControlsMixin, is_available_case_document, open_scanner`) while `f71331d42` updates line 57 (`safeguarding_view`); 6 lines apart, auto-merges cleanly (`C3`).
    * `Store.focus` (`store.py:630-631` in `4d91dae33` vs `store.py:660-662` in `fa6f8d1dd`): `f71331d42` replaces `open_h = [h for h in c["hazards"] if not h["released"]]` with `staff_list = self.data.get("staff") or list(self.staff.values())` and `open_h = self._open_safety_items(c, staff=staff_list)`, immediately above `ev = {d["kind"] for d in c["documents"]}`, which `4d91dae33` changed to `ev = {d["kind"] for d in c["documents"] if is_available_case_document(d)}` (`C3`). Keeping both (`staff_list` + `_open_safety_items` for `open_h`, and `is_available_case_document(d)` for `ev`) preserves both `#76` safety owner projection and `#117` document quarantine with zero semantic interference.
    * `Store.checklist`, `rescan_document`, and `document_bytes` (`store.py:1133-1135,1266,1330` in `4d91dae33`) are 200+ lines below `f71331d42`'s last hunk (`require_safety_clear` at line 940) and auto-merge cleanly (`C3`).
  * Q3 -> In the 3 auto-merged files:
    * `chat_case_answers.py`: upstream `36aeddae3` only updates `RULES[VISIT_CONSENT]` (`lines 43-47`), whereas `4d91dae33` imports `is_available_case_document` (`line 12`) and filters `case_facts` documents (`line 195`) (`C4`).
    * `projection.py`: upstream `f71331d42` adds `raw_safeguarding_items` import (`line 35`), `hold_notes` safeguarding redaction (`lines 252-262`), and `_is_high_sensitivity_path` safeguarding summary check (`lines 408-411`), whereas `4d91dae33` imports `is_available_case_document` (`line 26`) and gates `redact_staff_detail` document summaries (`line 635`) (`C5`).
    * `taskqueues.py`: upstream `f71331d42` bumps `MEMBERSHIP_REVISION = 5` and adds safeguarding helpers/clocks (`lines 3-45, 146-520, 645, 687-743, 892-893`), whereas `4d91dae33` imports `is_available_case_document` (`line 6`) and gates `evidence_freshness` document scanning (`line 338` pre-rebase / `~797` post-rebase) (`C6`). Note: import sorting in `taskqueues.py` (`I001` in `ruff check .`, since `taskqueues.py` is NOT in `per-file-ignores`) must keep `from .doc_controls import is_available_case_document` sorted cleanly after stdlib `from typing import Any`! Let's verify `ruff check .` and `ruff format --check .` on `taskqueues.py` post-rebase (`C6`, `C7`).
    * Neither `src/core/pyproject.toml` nor `src/api/pyproject.toml` changed in `243764945..fa6f8d1dd`, and `store.py` remains in `ruff.format.exclude` and `mypy.overrides` (`ignore_errors = true`) (`C7`).
* Reflection: `taskqueues.py` auto-merge near top-of-file imports (`from collections.abc import Mapping, Sequence` added at line 3 right above `from .doc_controls import is_available_case_document`) is a great catch to verify with `ruff check .` and `ruff format --check .` immediately after rebase! Proceed to Wave 3 Contrarian checks.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries:
  1. Cross-worktree Python package contamination: `python3 -m pip list` shows `zava-forward-{core,agents,api}` editable installs in `~/.local` pointing to `/home/azureuser/source/ama-demo-wt/feat-164-chat-revocation-0042/...` (`C8`). If we run `pip install -e` globally, we would clobber a concurrent user/worktree's environment; if we run `unittest` or `mypy` without `PYTHONPATH`/`MYPYPATH`, Python would import `feat-164-chat-revocation-0042` instead of our rebased `feat-117-doc-scan` worktree!
  2. Dirty tracked tree during `git rebase` and final `git status --short` empty requirement: Tracked parent `#117` files (`issue-117-doc-scan-*`) are inside `4d91dae33`. Modifying them before `git rebase` would block `git rebase`, and leaving child RPI state/review files uncommitted at exit would leave untracked files in `git status --short`.
  3. Cross-feature interaction between `#76` (`Store.focus`, `taskqueues.context`) and `#117` (`test_technical_evidence_usability.py`, `test_document_controls.py`, `test_hazard_safeguarding_clock_owner*.py`).
* Plan and independent lanes: Inline verification of `PYTHONPATH`/`MYPYPATH` precedence, sibling rebase commit conventions (`243764945`, `71f5c9f9b`), and cross-feature test suites.
* Worker evidence relationships or inline fallback: Inline:
  * Prepending `PYTHONPATH=src:tests` in `src/core` and `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests` (plus `MYPYPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests`) in `src/api` puts our worktree's source directories ahead of `~/.local` site-packages without mutating the shared host environment (`C8`). We can assert `zava_forward.core.__file__` resolves inside `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/` as an explicit sanity check!
  * Keeping tracked files unmodified until `git rebase --continue` succeeds, then running validation, completing `rpi-review`, persisting final `Follow-up` state in `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-state.json` (and updating parent `issue-117-doc-scan-*` records), and committing all `.copilot-tracking/` additions/updates in one clean tracking commit (matching merged PRs #1766 `243764945` and #1772 `71f5c9f9b`) satisfies non-amend governance AND leaves `git status --short` completely empty (`C7`, `C8`).
  * Running `#76`'s `test_hazard_safeguarding_clock_owner.py` alongside `#117`'s quarantine suites and `test_role_endpoint_inventory.py` directly verifies that our `Store.focus` conflict resolution and `taskqueues.py` auto-merge preserve `#76` as well as `#117`.
* Reflection: Contrarian wave caught the cross-worktree editable-install trap (`C8`) before running a single test!

#### Parent Synthesis and Disposition

| Material / claim                                                                                                               | Evidence IDs | Parent disposition | Evidence-based rationale                                                                              | Primary-artifact treatment |
|--------------------------------------------------------------------------------------------------------------------------------|--------------|--------------------|-------------------------------------------------------------------------------------------------------|----------------------------|
| Only `src/core/src/zava_forward/core/store.py` conflicts when rebasing `4d91dae33` onto `fa6f8d1dd`                            | C1, C2, C3   | accepted           | Proven by read-only `git merge-tree --write-tree --messages fa6f8d1dd 4d91dae33`.                     | Selected recommendation    |
| Resolve `Store.focus` by combining `#76`'s `staff_list` + `self._open_safety_items` with `#117`'s `is_available_case_document` | C3           | accepted           | Orthogonal lines (`open_h` vs `ev`); preserves both safety owner projection and document quarantine.  | Selected recommendation    |
| Prepend worktree-local `PYTHONPATH` and `MYPYPATH` instead of running global `pip install -e`                                  | C8           | accepted           | Protects shared host worktrees while guaranteeing imports resolve to `feat-117-doc-scan`.             | Selected recommendation    |
| Commit finalized `.copilot-tracking/` artifacts after `rpi-review` and final state transition so `git status --short` is empty | C7, C8       | accepted           | Matches merged sibling PRs (`#1766`, `#1772`), avoids amending without permission, leaves tree clean. | Selected recommendation    |
| Run `pip install -e` into shared `~/.local` site-packages                                                                      | C8           | rejected           | Would overwrite editable links currently pointing to `feat-164-chat-revocation-0042` on shared host.  | Rejected alternative       |

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Exact merge-tree simulation, hunk analysis, environment isolation, and commit/clean-tree sequencing are 100% verified from primary evidence.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded 4-file overlap verified directly via read-only git and file views.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | `origin/feat/demo-164-chat-grounding-provenance-0900` fetched at `fa6f8d1dd0493342718a70c134dd9fcb3305cd6c`, 3 commits ahead of `4d91dae33`'s base `243764945` (`36aeddae3` #1773, `f71331d42` #1768, `fa6f8d1dd` #1774). | `src/core/src/zava_forward/core/store.py:1` | bash (`git fetch` / `git log`) | high | Exact target SHA matches caller prompt |
| C2 | `comm -12` and `git merge-tree --write-tree --messages fa6f8d1dd 4d91dae33` show 4 overlapping files (`chat_case_answers.py`, `projection.py`, `store.py`, `taskqueues.py`), with `store.py` as the sole content conflict. | `src/core/src/zava_forward/core/store.py:630` | bash (`comm`, `git merge-tree`) | high | 3 files auto-merge cleanly |
| C3 | In `Store.focus`, `f71331d42` replaces `open_h` (`store.py:630`) with `staff_list` + `self._open_safety_items(c, staff=staff_list)`, adjacent to `4d91dae33`'s `ev = {d["kind"] for d in c["documents"] if is_available_case_document(d)}` (`store.py:631`); imports (`51` vs `57`) and lower document methods (`1133`, `1266`, `1330`) are disjoint. | `src/core/src/zava_forward/core/store.py:631` | view / bash (`git diff`) | high | Deterministic 3-line union |
| C4 | `chat_case_answers.py` upstream diff only touches `RULES[VISIT_CONSENT]` (`lines 43-47`), disjoint from `4d91dae33`'s `is_available_case_document` filter (`lines 12, 195`). | `src/core/src/zava_forward/core/chat_case_answers.py:195` | grep / bash (`git diff`) | high | Clean auto-merge |
| C5 | `projection.py` upstream diff touches safeguarding note/path helpers (`lines 35, 252-262, 408-411`), disjoint from `4d91dae33`'s `redact_staff_detail` document summary hold (`lines 26, 635`). | `src/core/src/zava_forward/core/projection.py:635` | grep / bash (`git diff`) | high | Clean auto-merge |
| C6 | `taskqueues.py` upstream diff bumps `MEMBERSHIP_REVISION = 5` and adds safeguarding clock/owner projection (`lines 3-45, 146-520, 645, 687-743, 892-893`), disjoint from `4d91dae33`'s `is_available_case_document` import (`line 6`) and `evidence_freshness` check (`line 338`). | `src/core/src/zava_forward/core/taskqueues.py:338` | grep / bash (`git diff`) | high | Verify `ruff` import order after auto-merge |
| C7 | `src/core/pyproject.toml` and `src/api/pyproject.toml` have zero diffs in `243764945..fa6f8d1dd`; `.copilot-tracking/` artifacts are git-tracked (as in `4d91dae33`, `243764945`, `71f5c9f9b`). | `src/core/pyproject.toml:34` | view / bash (`git show`) | high | Tracked artifacts require final clean commit |
| C8 | Shared host `~/.local` pip editable installs point to sibling worktree `feat-164-chat-revocation-0042`; worktree-local `PYTHONPATH` and `MYPYPATH` isolate execution safely without mutating shared packages. | `src/api/pyproject.toml:55` | bash (`pip list`) / view | high | Prevents cross-worktree test/type leakage |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* `none`

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `fa6f8d1dd` adds 3 commits (`#1773`, `#1768`, `#1774`) above `243764945`; 4 files overlap with `4d91dae33` and only `store.py` conflicts. | C1, C2 | high | Confirms exact rebase target and single-file conflict scope. |
| Q2 | `Store.focus` conflicts only on adjacent `open_h` (`#76`) and `ev` (`#117`) lines; keeping both preserves both features cleanly. | C3 | high | Exact conflict resolution ready for `rpi-implement`. |
| Q3 | `chat_case_answers.py`, `projection.py`, and `taskqueues.py` auto-merge cleanly with zero `pyproject.toml` changes; `ruff` import order in `taskqueues.py` will be verified post-rebase. | C4, C5, C6, C7 | high | No semantic collisions across auto-merged modules. |
| Q4 | Worktree-prepended `PYTHONPATH`/`MYPYPATH` isolates tests and `mypy` to this worktree; committing finalized `.copilot-tracking/` records post-Review leaves `git status --short` empty without pushing. | C7, C8 | high | Ready for `rpi-plan` -> `rpi-implement` -> `rpi-review`. |

## Key Discoveries

* `git merge-tree` proved read-only that `src/core/src/zava_forward/core/store.py` (`Store.focus`) is the sole conflict when rebasing `4d91dae33` onto `fa6f8d1dd` (`C2`, `C3`).
* Shared `~/.local` editable installs point to another worktree (`feat-164-chat-revocation-0042`); explicit worktree-local `PYTHONPATH` and `MYPYPATH` (verified via `zava_forward.core.__file__`) ensure all validation runs against the rebased `feat-117-doc-scan` HEAD without disturbing concurrent users (`C8`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Keep tracked files clean while running `git rebase origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`) in `rpi-implement`; resolve the single `Store.focus` hunk in `src/core/src/zava_forward/core/store.py` by retaining `staff_list` + `self._open_safety_items(c, staff=staff_list)` alongside `ev = {d["kind"] for d in c["documents"] if is_available_case_document(d)}` and complete `git rebase --continue`; run focused validation (`ruff check .`, `ruff format --check .`, `mypy`, and `#117` + `#76` + endpoint-inventory unit tests in `src/core` and `src/api` with worktree-local `PYTHONPATH`/`MYPYPATH`); update `#117` tracking artifacts and child rebase RPI artifacts; and create one clean local tracking commit after `rpi-review` and final state transition so `git status --short` is empty without pushing.
* Rationale: Preserves exact rebased feature commit provenance, avoids unrequested `git commit --amend` on already-reviewed feature changes, isolates shared-host Python imports, and satisfies `git status --short` empty at exit.
* Evidence refs: C1, C2, C3, C4, C5, C6, C7, C8
* Implementation impact: Rebase `4d91dae33` onto `fa6f8d1dd` resolving `store.py`, validate `src/core` and `src/api`, update parent/child `.copilot-tracking/` artifacts, and commit tracking records locally.
* Confidence: high: conflict boundary and environment isolation verified directly.

### Alternative: Overwrite Shared Editable Installs via `pip install -e` and Amend Feature Commit

* Approach: Run `pip install -e src/core -e src/agents -e src/api` in the shared user environment and fold child RPI artifacts into `4d91dae33` via `git commit --amend`.
* Trade-offs: Saves setting `PYTHONPATH`/`MYPYPATH` and keeps a single commit, but mutates shared `~/.local` `.pth` links used by sibling worktrees on this non-sandboxed host and amends the feature commit unnecessarily after rebase.
* Evidence refs: C7, C8
* Rejection rationale: Violates shared-environment safety and sibling rebase conventions (`#1766`, `#1772`).

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Verify `zava_forward.core.__file__` and `zava_forward.api.__file__` point to `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan` during validation, and commit the finalized `Follow-up` state JSON as the final step so `git status --short` is empty.
* Follow-up: Parent `#117` follow-ups (`RV-001` direct `SqlStore.rescan_pending` test, Azure Storage Defender Bicep tags, and DPO/Legal retention schedule governance) remain tracked in `prioritized_follow_ups`.
* Residual uncertainty: none

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Rebase `4d91dae33` onto `fa6f8d1dd` resolving `Store.focus` with both `_open_safety_items` and `is_available_case_document` | confirmed | user / evidence | Exact union of orthogonal `#76` and `#117` lines | C1, C2, C3 | Preserves both features cleanly |
| Isolate focused validation with worktree-local `PYTHONPATH`/`MYPYPATH` and leave `git status --short` empty via clean post-Review tracking commit without pushing | confirmed | user / constraint / evidence | Protects shared host environment and satisfies clean-tree + no-push requirements | C7, C8 | Reproducible local validation and clean git status |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| none | none | none | none | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | none | Rebase boundary and validation isolation are fully determined | Only if target ref moves again | no | Q1–Q4; C1–C8 |

## Planning Readiness

* Status: Ready
* Decision state: Converged on `Store.focus` union conflict resolution atop `fa6f8d1dd`, worktree-isolated focused validation across `src/core` and `src/api`, and clean post-Review tracking commit leaving `git status --short` empty.
* Evidence basis: C1, C2, C3, C4, C5, C6, C7, C8
* Preconditions met: `origin/feat/demo-164-chat-grounding-provenance-0900` fetched at `fa6f8d1dd`; `git merge-tree` conflict boundary verified read-only.
* Blockers: none
* Smallest action to change readiness: none

## Closeout Record

| Field                            | Record                                                                                     |
|----------------------------------|--------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                   |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian                                                     |
| Lane evidence or inline fallback | inline: 4-file rebase overlap and host Python environment inspected directly               |
| Research disposition             | executed                                                                                   |
| Planning Readiness               | Ready (C1–C8)                                                                              |
| Blockers                         | none                                                                                       |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic continuation to `rpi-plan`                        |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (C1–C8)                                                                                                |
| Output mode and planning support | convergence; yes — unambiguous single-hunk conflict resolution and isolated validation commands               |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | Research disposition recorded (passed); Planning Readiness Ready (passed); pre-transition state write (next) |
| Continuation result              | automatic continuation to `rpi-plan`                                                                         |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-research.md                         |
| Notes for planning or re-entry   | Keep tracked `#117` files unmodified until `git rebase --continue` completes in `rpi-implement`.             |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All rebase overlap, conflict hunks, auto-merge safety, shared-host isolation, and clean-tree tracking commit rules are verified from workspace evidence (`C1`–`C8`).

## Sources

No external sources used.
