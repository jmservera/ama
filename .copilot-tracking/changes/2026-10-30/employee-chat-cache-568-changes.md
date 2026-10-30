---
title: Employee chat and release cache implementation evidence
ms.date: 2026-10-30
---

## Scope and Status

Task 568, employee-chat-cache-568; full plan P01-T01 through P01-T03.
Implementation complete. Plan/details and one original critique are dated
2026-10-30 with the same slug. PC-001 rejected with parent-host evidence;
PC-002/003 applied before source edits. No source or tests removed.

## P01-T01: Shared Static Delivery

Implemented typed packaged snapshots in `static_assets.py`, wired into the
employee, resident showcase and preview handlers. HTML asset attributes carry
content-derived release versions; non-HTML assets revalidate with byte ETags.
Auth/host/allowlist checks precede conditional handling. HEAD/304 have no body;
304 omits Content-Length rather than describing an empty representation.
P01-T01 complete: focused real-socket tests passed within 78 tests, 20.026s.

## P01-T02: Recovery and Chat

Recovery now resolves original versioned script src; bounded retry tests cover
shared chat, adapter, async helper and Leaflet. Added ordinary employee real-endpoint
Enter/Send browser checks; preserved controlled race matrix. P01-T02 complete:
the admitted chat-submit browser run passed with Chromium and actual local APIs;
existing shared focus implementation is unchanged. Version-retaining loader
regressions also passed in the full discovery run; only unrelated old static
expectations within that run failed.

## P01-T03: Validation

System Python probe lacked aiohttp. Existing `/tmp/mv` has Playwright; use its
pip-installed environment through PATH for requested python3 commands.
Heavy commands require the caller's `/tmp/ama-rpi-heavy.lock`.
Focused command: `python3 -m unittest test_static_assets test_workspace_scripts
test_chat_widget_focus test_ui_support test_auth test_resident_preview_api -q`
with requested source/test PYTHONPATH and `/tmp/mv/bin` on PATH, under flock:
78 tests OK. Fixture-only rule-store unavailable logs are expected explicit
diagnostics, not failures. Initial Ruff reported import ordering/line length;
used repository formatter/import fixes before rerunning.
Ruff check and format then passed. Mypy exposed seven fixture/factory boundary
typing errors; corrected with precise existing factory return/argument types and
fixture attributes/method annotations, without broad casts or ignore overrides.
The first queued full-API/browser command exhausted its 600-second lock wait
without admission (exit 1, no test execution). Retrying under the same required
shared lock; no unprotected validation or alternate lock is used.
The admitted run passed Ruff/format/mypy (120 files) and the complete chat
browser check, including real employee replies, all 12 race combinations,
intentional dismissal, session changes and real resident rules replies.
API discovery ran 1,384 tests in 483.452s: two failures, 320 skips. Both failures
were old static expectations (bare logo src and resident asset no-store), now
updated to assert the intended version URL/revalidation policy without weakening
API/error headers. Cache browser failed because its string polling expression
used eval under the application's CSP; changed polling to function predicates,
not the CSP. Original failed run/output remains preserved.
The next focused/cache request also timed out before lock admission. A subsequent
admitted run passed all 10 focused checks in 3.544s, then both cache browsers:
same-origin/context legacy-cache reuse, executed release B, applied CSS B,
shared widget B, employee Leaflet B, exact versioned first-failure/recovery URL
(two requests), and actual ETag/304 revalidation. Browser Chromium 156.0.8078.4.
Ruff check/format and mypy (120 source files) passed again. Final full discovery
is running under the same admitted lock.

External evidence root:
`/home/azureuser/.copilot/session-state/50f32963-b5c2-4665-b044-30dc1dde1c9c/files/employee-chat-cache-568/`.
`chat-submit/results.json`, `chat-submit/employee-real-replies.json`,
`chat-submit/employee-matrix.json` and `asset-cache-v2/results.json` hold actual
browser outcomes; screenshots were inspected. `api-tests.log` preserves the
original two-failure full run; `api-tests-final.log` is the new run.

## Amendments and Divergences

None. Historical live employee behavior is not established by source evidence.

## Remaining Work and Review Readiness

P01 and all three tasks complete; no remaining implementation tasks or product
blockers. Final full API discovery passed: 1,384 tests in 487.490s, OK with 320
skips. Ruff check, format (63 files) and mypy (120 source files) passed, as did
both actual local browser harnesses. The original failed run is not overwritten.
Plan checklist, details, changes evidence and handoff are reconciled.
Ready for one independent Review. No push authorized. These checks do not
constitute full publication gate, human accessibility or deployed acceptance.

## Criteria Proven Before Review

| Criterion | Evidence |
| --- | --- |
| AC1 shared chat and Enter/Send visibility/focus | Shared-byte socket assertions; real employee/resident endpoints; 12 controlled employee case/refresh combinations; dismissal/session matrix |
| AC2 release URLs and packaged dependency identity | Deterministic snapshot tests and both same-origin warm-cache release B browsers, including employee Leaflet |
| AC3 conditional/cache/no-store separation | Real HTTP tests for all entry aliases, ETag/body, weak/list/star conditions, HEAD, old/bare URLs, API/host denial |
| AC4 versioned bounded recovery | Node executes actual loader for four dependencies; browser observes same initial/recovery versioned widget URL |
| AC5 requested local checks | Final full discovery, Ruff/format/mypy and Chromium results above; 320 skips not treated as executions |

Unproven: historical deployed employee bytes, live sign-in/model, multi-browser
and human assistive-technology acceptance, hosted approval and full publication
receipt. Existing pages are not hot-reloaded; freshness applies to normal new
page loads after a process release.
