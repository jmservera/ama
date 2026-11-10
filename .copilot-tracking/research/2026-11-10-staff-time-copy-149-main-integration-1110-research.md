---
title: Parent 149 component-only main integration research (staff-time plain-language disclosure)
ms.date: 2026-11-10
task_id: 149-copy-main-integration-1110
---

## Disposition and scope

Research executed 2026-11-10T00:38Z to 00:39Z, before any merge. Planning Readiness: Ready.

Scope is only the existing reviewed staff-time plain-language disclosure component (child 153, merged into the owned parent by PR 1335) plus necessary own tracking. This is a component-only integration of pinned current main into the owned parent. It does not claim the whole UX epic 149 or the whole of 153. No new feature, copy or redesign, and no Core, API server, app, roles, store, procurement or SQL-store hook, schema, security, cost or live-authority change. Issue 132 keeps its shared hooks. Existing consent, human, manual and accessibility limits stay. Production and assistive-technology acceptance is not established.

## Identities (verified, not assumed)

| Item | Value |
| --- | --- |
| Branch | `feat/demo-content-workflows-149-1109` (existing, owned) |
| Local head at start | `a04668ae94b5c2f38e6c55ed789db245e8c71d16`, clean (`git status --short` empty) |
| Owned parent origin head | `befe28e48bb5d916dfda000321a0d31059e92989`, tree `a05c35128390805b18a88e4791229b11ef1b2456` (child PR 1335 merge) |
| Local start is ancestor of owned parent | yes; fast-forwarded only, no reset |
| Pinned current main | `ddeebd01694ddb46b456451d9ac6390347e51aaa`, tree `b917297ef34bc3e7e7948f9e46ffe6b7e66e6c88`, ancestor of origin main |
| Origin main at fetch | `3b8d3209893e49b240ec3484b5f1067ec6ec5a61` (newer than the pin; deliberately not used) |
| Merge base (parent and pin) | `a04668ae94b5c2f38e6c55ed789db245e8c71d16` |
| Product blobs on parent | `timecapture.js` `14e0b5adbd9f183986b01bbe095b7189c10059f1`; `test_timecapture_copy.py` `f7cac3acd97407bed67d8a08e9263171c67b1f2f` |
| Dry-run merge tree (`git merge-tree --write-tree`) | `88ef4643dd6805e6cdcacdb014c0b64b58dc5954`, exit 0, no conflict |

## Actual full parent to main delta

* Parent side, merge base to `befe28e48`: 16 paths. Product source: only `src/api/src/zava_forward/api/web/timecapture.js` (modified) and `src/api/tests/test_timecapture_copy.py` (added). The other 14 are original dated child 153 and C1 records under `.copilot-tracking/` (research, plans, critiques, details, changes, reviews, two state files). No unexpected unrelated parent source.
* Main side, merge base to pin: 207 paths (6 commits: 1b7a1719b quality sensors, a8593a7a8 and e1c630fd2 rubric, b613276e9 resident retry, 3bc207198 docs checkpoint, ddeebd016 AI transport attempts). It touches Core, Agents, API server, app.js, assistants.js, ops.js, case-workspace.js, pyproject files, tests and knowledge base, none of which the parent edits.
* File overlap between the two sides: none (`comm` of changed paths is empty).
* The main delta mentions `timecapture` only in an unchanged-semantics mypy override list in `src/api/pyproject.toml` (existing entries, plus new entries for unrelated quality-sensor modules) and in main-side tracking text that cites the 153 test as a lock holder. `test_content_standard.py` on main adds one allowed identifier (`v.provenance`) and `AUDITED_FILES` already lists `timecapture.js`, so the audited copy rule applies unchanged.

## Findings that constrain the plan

* No meaningful product conflict and no reserved shared-hook overlap exist in the changed-path sets, so the merge is an ordinary merge of the pinned commit. STOP conditions are not met; they remain armed for the merge itself.
* The previously installed `zava-forward-*` editable distributions point at the primary checkout `/home/azureuser/source/ama`, not this worktree, and the global tools are Ruff 0.17.3, mypy 2.4.1, Playwright 1.64.1. The declared dev extras pin Ruff 0.17.1, mypy 2.4.0, Playwright 1.64.0. Validation therefore uses a new venv outside the checkout, `/tmp/zf-149-1110/venv`, with `pip install -e src/core -e src/agents -e "src/api[dev]"` from this worktree (done 00:38Z to 00:39Z, versions verified, Chromium 1248 present in the Playwright cache).
* Heavy lock `/tmp/ama-rpi-heavy.lock` was free at 00:38Z by a non-blocking probe. Browser admission is one `flock -n`, never queued or killed.
* Child 153 evidence is frozen and is not re-litigated: frozen at `eea9` (C1) as reported by the owner brief, independent assessment `4c52` approve with 0 findings, exact API project 204 passed, 12 actual tests including 5 browser with 0 skips, all published-head CI passed. Core CI's single 6141 ms outlier had the same Core tree `66fdcd8` as a prior green run, one controlled local repro passed (max 196.9 ms), and one failed-job rerun passed. The original failure is preserved. C1 budget: four of five remaining; this task consumes none.

## Unknowns (not resolved here)

* Whether the merged tree passes after main's `src/api` Python and JS changes. Resolved only by the focused checks in the plan.
* Hosted CI for the merged head does not exist yet and is not claimed.
