---
title: "Task Research: resident-integration-462"
description: "Continuation research for Issue #462: non-rewriting integration of current main into the retained resident showcase candidate and local release-readiness"
ms.date: 2026-11-17
---

| Field         | Value                                                                                  |
|---------------|----------------------------------------------------------------------------------------|
| Date          | 2026-11-17                                                                             |
| Researcher    | rpi-agent (automatic mode, session rpi-462-integration)                                |
| Status        | Complete (opening section written before the research-open boundary; findings appended after it) |
| Retained head | 926b20a8856622515c60948bf9ed890b241fc1fc                                               |
| Pinned main   | 1c9ac230be1dad9a4ecc21975f9ffe0845309fc4                                               |
| Merge base    | 5e0c7f74432ffce73cfeaa672e4e40a605ca6274                                               |
| Branch        | feat/resident-demo-rpi-gate-462 (declared target main, no upstream, no PR)             |
| Artifact path | .copilot-tracking/research/2026-11-17/resident-integration-462-research.md             |

## Research Brief

* What: determine how to bring the retained #462 candidate (`926b20a8`) onto pinned current main (`1c9ac230`) without rewriting history, and what local engineering and release-readiness evidence the isolated synthetic resident showcase can honestly show from this confined worker.
* Why: the coordinator's first canonical FULL run at unchanged `926b20a8` against actual main refused with "Candidate does not descend from the reviewed main base" (see `unchanged-head-refresh.log` in the external evidence directory). Main now also holds the reviewed #1297 gate repair, so the original blocker B1 (runner skip allowlist) is expected to be resolved on main, not by this branch.
* Non-goals: rebuilding the already merged resident login, projection or UI; fabricating prospective evidence for earlier work; any deployment, Azure access, secret read, model call, push, PR or merge; any change to gate semantics, pins, permissions, infrastructure or application policy.

## Research Disposition

Disposition: executed (continuation). Planning Readiness: Ready (assessed after the findings below).

## Opening facts (observed before source comparison)

* Original session `rpi-462-resident-demo` launched 2026-11-16T08:29:52Z on this logical branch; its state is `.copilot-tracking/rpi-sessions/2026-11-16/issue-462-state.json` and is preserved unchanged. This continuation has its own state file and its own worktree witness; the new witness cannot retrospectively attest the original run.
* Original blocker B1 (full gate on base `5e0c7f74`, project-api unexpected required skip) and rank 1 follow-up (main runner fix) are recorded in the original state.
* Refusal evidence: `Candidate does not descend from the reviewed main base`, run at unchanged head against the actual main.
* The owner grant (2026-11-16) for an isolated resident synthetic deployment applies only after FULL gates; this worker may not deploy or spend.
* The FULL tier stays selected. This confinement has no Docker socket and no SQL Server, so SQL parity, image and heavy browser checks are named continuations unless the heavy lock is free.

## Planned research questions

1. What conflicts, if any, does a no-commit merge of the pinned main produce against the two candidate commits (docs, threat model, README links, knowledge-base index and log, tracking artifacts)?
2. What changed on main in the resident, auth, case, projection and runner areas since the merge base that affects the threat model or its claims (dependency, validation and provenance statements)?
3. Is the #444/#455 dependency, prior scoring and review evidence still as recorded, without manual grading or unchanged-rerun fishing?
4. Which light local checks apply and what do they prove and not prove?

## Findings

Appended after the `research-open` witness boundary (seq 2). All findings are read-only observations of the worktree and of commit `1c9ac230`.

### F1 Merge feasibility

* `git merge-base 926b20a8 1c9ac230` is `5e0c7f74`. Main moved 25 commits and 175 files.
* A read-only `git merge-tree --write-tree --name-only 926b20a8 1c9ac230` reports a clean merge (result tree `16faf2ec`) with no conflicted paths. The candidate commits touch only documentation and tracking files (threat model, `src/api/README.md`, `docs/reference/README.md` and `log.md`, `.copilot-tracking/`), none of which main changed in a coupled way. A merge conflict at implement time is therefore not expected; if one appears it is recorded as an exact blocker.
* The refusal in the unchanged-head refresh log (`Candidate does not descend from the reviewed main base`) is explained: the candidate descended from `5e0c7f74`, not from `1c9ac230`. Only a merge that makes `1c9ac230` an ancestor changes that.

### F2 Main changes that touch resident claims

* `fa8329d5` (#1826) adds sensor freshness and provenance to the resident view: `sensor_freshness()`, `SENSOR_PROVENANCE`, `RECENT_SECONDS = 900` and the derived keys `freshness`, `source` and `calibrated` inside the existing `sensors` object of `showcase_view`, plus a status group in `demo.js`. These keys are derived server-side from stored readings, add no new database column and carry no staff or canary field. The threat model rows T7 (database fields) and T10 and the "17 named columns" statement therefore need a dated update, not a rewrite: the column allowlist is unchanged, the output allowlist gains three derived keys. The stored text states the readings are synthetic, not calibrated and not live.
* `14296ce8` (#1831) enforces a retained sensor SQL gate and a 320px journey limit in the runner and browser checks; `resident_sensors_browser_check.py` and `case_journey_browser_check.py` changed. Their execution needs the heavy lock, Chromium and SQL, so it is a named continuation here.
* `tools/rpi-checks.py` gained required opt-in SQL and browser groups and an exact `(class, reason)` skip allowlist (`DISCOVERY_SKIPS`), each bound to a zero-skip execution group. This is the reviewed #1297-lineage repair that the original blocker B1 asked for. This task does not touch the runner and does not rely on it to pass.
* The rest of main (papers, whitepaper prose, map tile and count tests, employee workbench chat keyboard) does not touch the resident login, session, projection or SQL boundary.

### F3 Dependency and scoring evidence

* #444 is closed and PR #455 is merged (original research F1, 2026-11-16; no contrary evidence has been seen since). Main tip `1c9ac230` is the bot commit `chore(rubric): record score 79/100` scoring `d98725d8`. This continuation does not edit a score, rerun an unchanged scorer or assume a newer score repairs an older source. Whether the historical failed rubric counts as resolved remains a coordinator and owner judgement; issue criterion 2 stays unchecked.

### F4 Issue state (from the supplied `issue-source.json`)

* Checked: criteria 3, 4 and 8 (login mapping and denials; secret documentation and HTTPS session controls; deployed record).
* Unchecked: criterion 1 (genuine prospective RPI order, threat model and independent review), 2 (dependency), 5 (SQL parity, Docker, browser, lint/type/unit and a current-main exact-head gate verified by receipt, hosted checks and coordinator assessment), 6 (pre-spend record) and 7 (gated deployment with live HTTPS acceptance).
* Issue comments (2026-11-04 to 2026-11-10) record the interim ungated deployment and state that retrospective process criteria cannot be established by a working login. Nothing in this continuation changes that.

### F5 Honest provenance of evidence

* Historical implementation (login, projection, UI, domain tests) is on main and was not witnessed by this continuation.
* Original 2026-11-16 research, plan, critique, changes and review are preserved unchanged. Their local SQL parity, Docker non-root and browser results were recorded by that original run on a different host; this worktree witness cannot attest them and this task does not re-claim them.
* New in this continuation and newly witnessed: the non-rewriting integration, dated updates to the threat model and index, light local regressions run from this worktree, and the retained list of checks not runnable in confinement.

### F6 Capability and lock state in confinement

* No Docker socket and no SQL Server. `/tmp/ama-rpi-heavy.lock` exists; whether the coordinator's #1837 FULL run holds it is decided by a non-blocking attempt at check time, never by waiting.
* Python 3.12.15 is available; light tests need an external venv with the `src/core`, `src/agents` and `src/api` distributions installed from this worktree.

## Planning Readiness

Ready. Scope for the plan: (1) merge pinned main with `--no-commit --no-ff` after `implement-start`; (2) a dated threat-model update and knowledge-base log entry for the derived sensor keys, the new base and the validation provenance, with no claim beyond evidence; (3) light targeted resident/auth/case/projection/domain tests and Ruff/format/mypy from an external venv; (4) a non-blocking attempt at the heavy lock for browser checks, with pending checks retained if busy; (5) web-design-guidelines review of the merged `demo.js` change; (6) one critique, one review, one final merge commit.

## Follow-ups (provisional)

* Coordinator: current-base complete gate, external receipt verification, independent exact-head assessment, hosted CI, pre-spend admission and gated deployment criteria 6 and 7.
* Make the login limiter atomic and send `Retry-After` on 429 (original review R-003).
* Operator verification of the live SQL view and principal grants.
