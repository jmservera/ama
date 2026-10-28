---
title: Design-system browser check changes
ms.date: 2026-10-28
---

## Scope and status

Task: design-system-browser-check. P01 and P02 completed: implementation,
independent Review and requested publication. Plan and phase details use the same
dated task slug. One critique completed Pass without findings.

## P01-T01: Harness correction

Implemented heading-scoped visible current-copy locator and its disappearance
assertion. All three success fixtures now carry scope/count fields from one
shared mapping. One focused assertion checks exact assigned scope and two-case
rendering. Held-request counts, stale-response rejection, cache and retry remain.
No app/store/dependency/workflow changes. No tests removed.

## P01-T02: Validation

Baseline exact entry point failed at workbench_browser_check.py:271 after
30000ms, matching both PR #517 attempts. Blocked-outbound diagnostic confirmed
one held request and current loading copy. Corrected results are recorded below.
External venv: /tmp/ama-browser-check-fix-venv, pip dev extras plus Chromium.
No .env read, private dataset, heavy lock, Docker build or cloud/model call.

The corrected exact entry point passed four times, including two after final
callback binding, with Chromium 156.0.8078.4 / Playwright 1.64.0.
Logs: /tmp/ama-browser-check-fix-browser-{1,2,3,4}.log.
All held-request, cancellation, recovered scope/count, stale-response rejection,
cache and workflow retry assertions pass.
API Ruff/format/mypy passed (90 typed files), core Ruff/format/mypy passed
(153 typed files). API full discovery passed: 1148 tests, 314 existing skips,
536.019s. Core discovery ran 1437 tests, 186 skips, 404.642s, with two errors
because the public scenario manifest pins the changed harness source hash.
Original logs: /tmp/ama-browser-check-fix-{api,core}-tests.log.

An additional isolated strict lint diagnostic exposed existing I001 import
ordering and B023 queue-callback findings, both reproduced in the unmodified
HEAD harness. A new fixture-callback B023 was corrected by explicit binding;
only the identical two baseline diagnostics remain. Existing configured lint
passes; no exemptions were changed.

## Amendments and divergences

No material divergence. Focused small-issue validation tier and explicit
no-Docker scope preserved. Callback binding is ordinary local implementation
judgment; baseline strict-lint cleanup is outside this regression.

Immediately relevant amendment: refresh the scenario manifest's existing recipe
SHA-256 plus required knowledge-base index/log after the core suite exposed that
dependency. No weakening/removal of its integrity test, fixture change, version
bump, new scenario iteration or approval claim. Plan/details reconciled before
Review; failed original core run retained. The 19 targeted manifest/inventory
tests pass; final full core discovery passes, 1437 tests / 186 existing skips
in 297.792s (/tmp/ama-browser-check-fix-core-final.log).

## Validation boundary and review readiness

P01 complete. API/core discovery used the existing general-discovery contract:
314/186 skips remain, including opt-in SQL Server, live Azure and browser-only
integration paths. No required coverage is newly skipped and no skip conditions
changed. Real Chromium synthetic coverage ran separately; no full Docker/SQL/
scanner receipt or live/human acceptance is claimed.
All four public source bindings match and `git diff --check` passes.
Review-ready implementation includes only the harness, API README, dependent
recipe SHA-256 and required knowledge-base index/log maintenance.
Additional focused API checks (`test_workbench test_ui_support`) pass, 13 tests.
Original independent Review: Complete / Conformant, no RV findings, at
.copilot-tracking/reviews/logs/2026-10-28/design-system-browser-check-review.md.
The Review records all five changed non-RPI source hashes for exact-head
comparison; runtime evidence is attributed to the parent rather than claimed as
independently rerun. No second Review is planned.

## Follow-up-only work

Optional later harness lint cleanup: pre-existing I001/B023 diagnostics under
isolated strict lint. No correctness failure demonstrated for the queue callback
(its expectation is consumed synchronously); do not broaden this fix.

## P02: Publication

Implementation plus original dated evidence committed as
fbbbb88828650e7defe1f2849e97499641300fae, with the requested Copilot trailer
and GitHub-derived local noreply identity for author/committer.
Committed-candidate gate passed: browser entry point, 13 API workspace/UI tests,
19 core manifest/inventory tests, both packages' configured Ruff/format/mypy.
Evidence: /tmp/ama-browser-check-fix-committed-fbbbb888.log and
/tmp/ama-browser-check-fix-focused-fbbbb888.json.
Fresh origin/main remained 197e5e3c6d4f7cfb135c9a985af3f13e0f688ac4;
clean head and all five reviewed source hashes verified. The independent
reviewer separately attested the exact committed boundary and original Review
preservation without a second Review.

Pushed fix/design-system-browser-check without force and opened
https://github.com/jmservera/ama/pull/519 targeting main with Refs #517, #516,
#514 only. This closeout changes RPI evidence only; its final committed head
must receive fresh external focused checks/source-boundary verification before
the update push. Final evidence destination:
/tmp/ama-browser-check-fix-publication-final.json (not a full-matrix receipt).

## Remaining boundary

No implementation or requested first-publication task remains. Hosted checks,
human approval and merge remain separate; no merge was performed. The automatic
session waits in Follow-up without starting the optional baseline lint cleanup.
