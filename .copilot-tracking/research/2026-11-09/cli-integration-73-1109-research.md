# Research: parent73 CLI component integration with current main (2026-11-09)

Task: `issue-73-cli-integration-1109`. Mode `convergence`, posture `focused` (bounded internal task, named sources). Skill `rpi-research` activated 2026-11-09. Research is read-only; no source edited in this phase.

## Brief

* Scope: component-only integration of the already reviewed child #135 CLI (PR #1334, merged into parent branch `feat/demo-exception-workflows-73-1109`, not main) with current main. Parent #73 and whole #135 stay open and unmet.
* Pins: parent `a4317567f806d9585db716d6ae5ad4af6bed5366`; main `3bc20719803a77490c704f985559720e23aa169d`; merge base `a04668ae9...` (`git merge-base HEAD origin/main`).
* Budget: parent #73 current integration cycle 0/5 (this is cycle 1 of 5). Child #135 C2 of 5 stays separate, historical, spent; not reset.
* Non-goals: no Core/API/shared hook/register/navigation/roles change, no new feature or refactor, no budget/role/identity/schema change, no served queue, no whole-#135/#73 acceptance, no issue/board/PR/push writes.
* Active owner controls: #132 C5 owns staff_intake/server/app/roles/store/sqlstore/procurement; #1238 resident_decisions; #891 core AI/chat; #153 time capture. None are touched.

## Extensions

| Item | Disposition | Provenance |
| --- | --- | --- |
| AMA repository instructions | selected | custom instructions (branch, identity, validation tiers) |
| Web guidance | skipped | backend/importer-only work, exempt |
| `rpi-plan`, `rpi-implement`, `rpi-review`, `rpi-plan-critique` skills | later phases | RPI agent contract |
| Specialist subagents | skipped | tightly coupled, small delta; inline waves |

## Evidence

Source read in full: coordinator report `demo-next-ready-96-122-report.md` (static, not merge approval); live GitHub bodies of #73 and #135 (`gh issue view`, 2026-11-09). Repository Original/Addendum/reference index/memory are inherited from the child research; no knowledge-base file is changed here.

| ID | Evidence |
| --- | --- |
| C1 | Parent-only side of the delta (`git diff a04668ae9..a4317567f --stat`): 19 files = importer `README.md`, `__main__.py` (+109), `exceptions.py` (+345), `mapping.py` (+15/-6), `tests/test_import_exceptions.py` (+472) and 14 `.copilot-tracking` child RPI artifacts. No Core, API, hook, workflow, dependency manifest or infra file. |
| C2 | Main-side delta (`git diff a04668ae9..origin/main`): 5 commits (#1331, #1332, #1336 and two rubric score commits). Touches 39 non-tracking files (21 api, 13 core, 2 docs/reference, 1 docs/architecture, 1 agents, 1 `.github/rubric/scores`) plus main's own `.copilot-tracking` files; **nothing under `src/importer`**. Core changes are `ai*.py`, `assistants.py`, `assistant_release.py`, `resident_decisions.py`, `sensor_*.py`, `simulation_lane.py` and one mypy-override line in `src/core/pyproject.toml`. |
| C3 | Core contracts the CLI uses are unchanged on main: `exception_feeds.py` (`feed_failed_imports`, line 121), `exception_queue.py`, `exception_register.py`, `quarantine`: empty diff since the merge base. `exception_register.py:24` still defines `NOT_CONNECTED`. |
| C4 | `exceptions.py:21-22` imports only `feed_failed_imports` and `ExceptionQueue/Record` from Core. `grep importer src/api/pyproject.toml src/api/src` is empty: no API to importer edge. |
| C5 | Importer `pyproject.toml` depends on `zava-forward-core[blob]>=0.1.0,<0.2`; mypy project config `files = ["src","tests"]`, Core excluded via `follow_imports = skip`. |
| C6 | Trial merge (`git merge-tree --write-tree HEAD origin/main`) produced tree `97ce8c10653e51413c58a35843c5aed10b6edb7f` with no conflict output. The two sides touch disjoint paths (only potentially shared: tracking dirs, which are distinct files). |
| C7 | Environment: installed `zava-forward-*` dists resolve to the primary checkout (`/home/azureuser/source/ama/src/...`), not this worktree. Verification therefore needs a fresh virtual environment with this worktree's Core and Importer installed. Local ruff 0.17.3/mypy 2.4.1 differ from project pins (0.17.1/2.4.0). |
| C8 | Local git author email already equals the resolved noreply address `8036360+jmservera@users.noreply.github.com`. |

## Dependency interpretation (not a waiver)

* #80, #84, #122 remain literal whole-issue dependencies of #135 and are unmet/retained. The CLI does not call stock conflict resolution (#84), #80 transition thresholds, continuity restart or old-image admission (#122) (C3, C4 and the report). Component delivery into main does not require those unimplemented runtime journeys.
* The actual parent diff shows no technical dependency and no unrelated parent work (C1), so the STOP condition in the brief is not triggered.
* Whole-#135 criteria stay unmet: conflict both-values display, failed model calls and stranded tasks in an owned queue, controlled audited recovery, scoped operator access and outage honesty are absent. Served queue/refusal transport/recovery stay absent and `NOT_CONNECTED` remains.

## Contrarian wave

* Could main's Core AI/sensor changes break the importer? Importer imports only exception feed/queue (C3, C4); those are byte-identical. Residual risk is low; verified by running the importer suite against combined source.
* Could a merge silently alter the importer? Disjoint paths (C2, C6) make that unlikely; confirm by post-merge `git diff` of `src/importer` equal to the parent's.
* Does the report overstate readiness? It states static evidence only; this phase supplies the exact-delta evidence it lacked. Execution evidence is deferred to Implement.

## Parent synthesis

* Decision: proceed with ordinary merge of current main into this owned parent branch after Plan, critique and Implement activation; no rebase, force, reset or amend.
* Alternatives rejected: rebase (forbidden); cherry-picking the importer commit to a main branch (outside brief and loses the parent lineage); editing Core to wire the register (owned by #132).
* Open limits: no actual SQL Server, browser, model or network; hosted CI and independent exact-head review remain required before publication.

Research disposition: `executed`. Planning Readiness: `Ready`.

## Planning follow-ups

1. Verify with a fresh venv (Core+Importer from this worktree), 71 importer tests, exact importer-project mypy, Ruff, separate-process CLI scenarios.
2. Confirm combined tree keeps register `NOT_CONNECTED` and no API to importer edge.

## Next Steps

Active-parent action: persist state, then activate `rpi-plan` (Plan phase).
