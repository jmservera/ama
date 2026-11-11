---
title: Keyboard probe compatibility integrated-main checkpoint research (Refs #440 #132)
description: Read-only evidence for one documentary checkpoint after merged PR 1438
ms.date: 2026-11-11
---

Task `keyboard-checkpoint-440-1111`. Research disposition: `executed` (read-only Git, `gh` and Root evidence files; no runtime). Planning Readiness: `Ready`.

## Identities (read 2026-11-11 04:48 to 04:52 UTC)

* Worktree branch `docs/demo-keyboard-checkpoint-440-1111`, clean. `git fetch origin main` then `origin/main` is `74e63363bdcb6f9d420ff9c71b8332a9baf0044b`, tree `e89381c5fa93d093ca8ab90f95812a023c1d3e7a`; both equal the pin and local HEAD. No relevant input changed, so no stop condition arose.
* PR 1438 (`gh pr view`): MERGED 2026-11-11T04:43:41Z, merge commit `74e63363`, zero closing references. Assessed head `f62d4b66ed96d54ace8b42343c30cdea2140a614`; Root recorded mergeable, 19 of 19 hosted checks SUCCESS (the Root list `1438-final-checks-1111.json` was read) and tree `e89381c5` equal to the merged tree.
* Hosted Source projects CI run 42958485921 (`gh api`): completed success on head `f62d4b66`, event pull_request. Jobs read: src-no-working-data, src-changes, mssql, image-paths, src-namespace, src-api, src-core, src-importer, src-orchestrator, src-agents, all success. Step-level skipped counts: 12 each for src-core, src-importer, src-orchestrator and src-agents (causes not examined), 0 elsewhere. Test-level skips are not known.
* Independent published review `3e182ded-9135-47cc-a341-58186013ee67`: verdict approve, zero findings (Root `independent-132-keyboard-e4-published-1111/functional-findings.json`). Durable comment 6786933451 on PR 1438 exists (created 2026-11-11T04:21:51Z). Existing #134 blocker comment 6786645682 exists (created 2026-11-11T04:03:12Z).

## Product delta (read from merged tree tracking and Root path list)

* 24 paths in the PR (Root `1438-final-paths-1111.txt`): the probe, its test, the README line, and `.copilot-tracking` RPI evidence. The reviewer read the supplied 946-line reference diff.
* Product delta is zero in behaviour: one `NO_REGION_GAPS` entry for `staff-job-pack-intake` in `src/api/checks/specialist_keyboard_browser_check.py`, a seventh unit test, README "five" to "six". The unknown-screen and unexpected-table fail-closed predicate is unchanged.

## Retained browser observation

* `/tmp/zf132-e4/browser.log` (863 lines, local, not committed) from source candidate `f8939a5a438b3fac62c548d2a42c50f36f8a2778`: 805 printed assertions, 15 negatives, 46 OBS lines, 22 declared gap walks, seven staff-intake roles. `git diff f8939a5a 74e63363 -- src` is empty (verified), so the source is equivalent to current main. This is a dated local observed output on a source-equivalent head, not a fresh main run. Axe not run; the HTTP status and empty-order cause are unobserved.

## Requirement and ADR documents (blobs at the pin, read 2026-11-11)

* BRD `docs/brds/agentic-retrofit-programme-brd.md` 0.21.0 `draft` `34d88395de861e9799eb9e24121a21c92c7a5adc`.
* PRD `docs/prds/zava-forward-retrofit-programme-demonstrator.md` 0.21.0 `in-review`, author-complete-unsigned-pending-review-and-owner-acceptance, `c788b917bafaede215f326f0efc71e071a687f1c`. Rows read: AC-034, AC-039, AC-042, AC-043 and FR-016/FR-017.
* ADR 0003 Accepted with amendment 2026-10-15 `d60645397b20fb70ac3d1dc47c7a6c8671201306`; ADR 0006 Accepted 2026-10-15 `956da1a3b804c803041fe2e8a312bd9f400273ae`; ADR 0007 Proposed 2026-11-04, not accepted `abb21088a9bb9771234a305b8052c3bcdd181b33`.

## Gaps and exclusions

* Unpublished #134 connected candidate `468bdd3` has a High checker false pass and zero correction authority; excluded and not claimed on main.
* Whole #132 remains 4 checked and 2 unmet (variation named owner; delivery channel and identity decision). #134 all-perspective, AT and whole-journey criteria are untouched. #149, #233, #80, #73 and #440 stay open.
