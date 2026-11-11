---
title: Closure-wave checkpoint prospective admission amendment (Refs #440)
description: Additive record of Root's admission decisions before any observation; the original plan and critique are unchanged
ms.date: 2026-11-11
---

## Status

Additive amendment recorded before any observation. Original plan (`aa6f34fe`), details and critique stay as written. This is Root's prospective admission, not an observed result.

## Root decisions

1. Main advanced from `8aedb56b5909903abd6c6f84777b49f237c1cbb0` to `e0dec207dab2cce2e2bf9d0084e1cdea9d10ec1d` (tree `4fcaac76dca4c6dd5cb252fe676a0dad20d2d7d4`). Verified by fetch: `git diff --name-status` shows only `M .github/rubric/scores/latest.json`; one commit (`chore(rubric): record score 78/100`); the old pin is an ancestor. An ordinary committed no-ff merge of that main into this topic precedes any test. No rebase, amend, reset or source conflict resolution; unexpected source or document movement or any conflict stops for Root. All claimed runtime source must equal that main.
2. Admitted once each, existing selectors with nonzero exact counts: N1, N2, N3, N5, N6, N7, N8, N9, N10. N4 (whole importer, 82) is omitted by Root: `TransferFailureTests` (8) covers the modified importer error-contract surface. This is a recorded scope omission, not a skipped or passed full suite. N8 expects 24.
3. B2, then B1, then B3, sequentially, once each, lock acquired once per harness. B1 and B3 self-lock and are never outer-flocked; B2 alone uses `flock -n -E 99`. Busy, missing or skipped is blocked, not success. First failures preserved. No SQL Server, Docker, full suite or Core 3057.
4. Private venv `/tmp/ama-440-closure-venv-1111` allowed. The chosen dependency and import preflight runs first and is captured; local `src` distributions and `playwright==1.64.0` install only after an actual missing-dependency failure. No global or shared install, no manifest change. Existing Chromium, node and axe must pre-exist and are not installed. All module and helper origins must lie under this exact worktree; stale editable paths fail.
5. Validation child commands use a newly owned private HOME, never the real HOME or `~/.zava-forward`; no `.env` or private dataset read. The Capacity harness clears most environment, so `PLAYWRIGHT_BROWSERS_PATH` is not assumed to survive; if needed a new symlink inside the private `HOME/.cache` to the pre-existing Chromium cache is allowed after read-only verification of target identity, never altering the shared cache. HOME is never exported over the Copilot CLI or auth process. `ZF_DATA` unset; private-home default-data state recorded before and after.

## Unchanged limits

* No new correction budget and no implied C6 for #80; #1360 and #144 E1 and E2 stay spent with three left each. Failures map to #80, #1419, #1360, #144 or #440; no source fix, new test or new issue.
* The #132 candidate `fdf0d3beb` stays unpublished with independent exact-final review underway separately; its tests are excluded from this checkpoint's main claims and nothing is duplicated. Resume condition: Root's #132 disposition, then a main refresh.
* After the admitted runs: ONE dated section in `docs/architecture/cutover-evidence-pack.md` and ONE append-only `docs/reference/log.md` entry, with the document-qualified trace, actual commands, exits, counts and skips, identities, a bounded continue or fix recommendation and the #1420 disposition. Whole #80, #73, #144, #131, #132 and #440 stay open. No human, QA, resident, Legal, production or accessibility acceptance; no fresh web-guidelines review and no WCAG conformance from axe. Original adverse and process records stay.
* No publication; Root assesses the exact final head first.
