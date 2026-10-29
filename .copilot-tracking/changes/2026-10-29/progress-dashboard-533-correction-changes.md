---
title: Progress dashboard correction changes
ms.date: 2026-10-29
---

Task 533-correction-2026-10-29, Refs #533, PR #540. Declared scope:
full approved correction plan. Critique executed once Complete / Pass.

## P01: Backend and regressions

P01-T01 complete. Added explicit history list guard and dedicated DateRangeError
with scoped endpoint reasons.fields metadata. Two added inherited unit methods
cover non-list histories and exact inclusive range semantics; HTTP assertions
cover typed range metadata versus unrelated 400s. No tests/assertions removed.
Initial direct probe reproduced null-history TypeError using current source.
New tests before production edits failed (2 tests, 7 subtest errors, including
null/int/bool TypeError and not-yet-implemented exception). After fix, all 25
progress tests pass in 4.237s, JSON/SQLite and real HTTP boundaries included.

## P02: Inline field errors

P02-T01 complete. Shared load uses structured range fields/status, links adjacent
field-error paragraphs through aria-describedby and aria-invalid, and focuses
start after show(). Read failures keep alert/retry and main focus. Existing
app.js and CSS are unchanged. Extended browser check covers four invalid range
scenarios with linked text/focus/values, correction and axe on error/recovered
states, two valid boundary scenarios, 503 and unrelated 400. README documents
both fixes. Targeted real browser execution passed.

## P03: Validation and review

P03-T01 complete. Targeted Ruff passed; first formatter check identified one
wrapping-only change, applied through Ruff; subsequent lint passed. Strict mypy
passed all 102 configured files. node --check and git diff --check passed.
All four scenario-manifest source pins match; no pinned files edited.
Requested journey venv absent; existing /tmp/ama-533-venv is available
with dependencies. Current worktree src is required on PYTHONPATH. No installation,
cloud or full publication gate authorized. Heavy admission uses flock -n.

Nonblocking full-suite admission was busy. No full discovery or full browser
suite ran; no waiting/retry or heavy lock bypass. The conditional harness
recorded that its combined full run did not execute. Then ran only the targeted
progress browser/check, consistent with the caller's targeted-only fallback.
No full API-suite pass is claimed.

External evidence root: /tmp/ama-533-correction-20261029-r1.
lock-busy.log records denied admission. targeted.log: 35 tests pass in 5.589s
(progress, workbench, role screens and workspace scripts).
browser-targeted.log and browser-targeted/: progress browser passed on Chromium
156.0.8078.4 with pinned axe 4.10.3 SHA-256
880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb.
Eleven scanned states have zero violations: dashboard/archive, four range-error
states, four corrected states, and a 503 read failure. All four actual invalid
states have no incomplete rules. Existing dashboard/recovered-dashboard
color-contrast incomplete rules (14 or 23 offscreen/clipped nodes) remain for
human assessment, not an automated conformance claim. Browser also passes
all existing chart/API/table, URL/history, pagination, keyboard, reflow,
failure retry and late-response checks with no uncaught JavaScript errors.

Frozen source diff (git diff -- src/api) SHA-256:
e653d3975581e09f493db8d4f49fd4c54246db15a9cda921588e4a7d44d33077.
All six source/doc edits remain within approved scope.

## Amendments and Divergences

Environment-only deviation documented above and in research. No scope change.

## Remaining Work and Handoff

P01/P02 and P03-T01 complete. Only P03-T02 independent Review and local commit
handoff remain. Original parent outcomes remain historical.
No push, az or force-push; local commits only.

## Follow-Up Items

Owner/coordinator: full API discovery once heavy lock is free (not a failed
test or reason to skip required publication gates).
Owner/accessibility participants: existing screen-reader/usability and
dashboard color-contrast incomplete assessment. No acceptance inferred from axe.
Coordinator: any later publication still requires its applicable exact-head
gates and approvals; no publication is requested here.
