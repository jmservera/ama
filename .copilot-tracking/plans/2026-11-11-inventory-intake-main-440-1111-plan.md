---
title: Inventory and staff intake current-main checkpoint plan (Refs 440, 131, 132, 1362)
ms.date: 2026-11-11
task_id: 440-inventory-intake-main-1111
---

## Objective and boundaries

Append one dated documentary record to the existing cutover evidence pack, plus an append-only knowledge base log entry and an index pointer if the pack's existing index sentence needs it, after targeted local observations on pinned main `0509ddcef14d9c2046791b283fad65229f536202`. No source change, no new test, no new issue, no push, PR or GitHub write, no full gate, SQL Server, Docker, live, Azure, model or private-data run. Research: [research](../research/2026-11-11-inventory-intake-main-440-1111-research.md). Details: [details](../details/2026-11-11-inventory-intake-main-440-1111-details.md).

## Phases

* [ ] P1 Environment: fresh private venv `/tmp/ama-440-inventory-venv-1111`, editable installs of this worktree's `src/core`, `src/agents`, `src/api` (no dev extra at first; Playwright 1.64.0 restored only after an actual import failure); prove every `zava_forward.*` module resolves inside this worktree; no `ZF_DATA`, `.env`, credential or provider variable.
* [ ] P2 Observations (existing tests only, raw output and exit code per command under ROOT `inventory-intake-main-440-observation-1111/`): O1 Core inventory selector; O2 Core QA gate selectors; O3 API resident inventory; O4 staff intake API; O5 role endpoint inventory and content standard; O6 Atlas checker helper without browser, then with browser only if the shared lock is free by one non-blocking `flock -n`; O7 staff intake browser recorded blocked (pinned axe prerequisite absent; not installed).
* [ ] P3 Static trace and gap classification: document-qualified requirement to decision to code to test to observation to remaining owner; the combined journey (inventory-managed case, staff capture, independent QA) is stated as untested by any existing selector.
* [ ] P4 Documentary checkpoint: append the dated section to `docs/architecture/cutover-evidence-pack.md`; append a log entry to `docs/reference/log.md`; index touch only if needed.
* [ ] P5 Review once (author-executed), record outcome, then commit own documentary checkpoint and dated RPI with the repo-local noreply identity and Copilot trailer; write the Root handoff.

## Gates and stop conditions

* Strict state parse, `load_artifacts` and a successful preflight run before every witness marker; a failed preflight blocks the marker.
* Missing dependency: restore only declared own packages after an actual failure, never global or shared.
* Busy shared lock or missing prerequisite: record the affected check as blocked and continue independent analysis; no queueing, no kill, no skip token, no waiver.
* A failing observation is preserved raw and reported as adverse; it is compared with owners 131, 132 and 440 before any claim, and no source fix or ticket follows from it.
* If origin main moves, record both identities and do not merge or rebase merely to refresh.
* Never tick an issue criterion, close an epic, declare roster, identity, legal, QA or resident approval, or start the 1420 expansion.

## Tier classification

Focused tier (documentation plus targeted existing tests). Basis: documentation-only change with targeted local observation of three merged increments; it touches no workflow, gate tool, dependency manifest, Dockerfile, infrastructure, deployment, SQL schema or security control. No full local gate or receipt is required or claimed; independent exact-head review and hosted CI remain required before publication.
