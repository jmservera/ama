---
title: Issue 73 live changes (2026-11-24)
ms.date: 2026-11-24
---

Status: complete. Documentation only, no `src/` change, so the focused tier applies; `rpi-checks.py` was not run. No Azure resource was created or changed, no write call made, nothing ticked or closed.

## Files

* Modified `docs/architecture/cutover-evidence-pack.md`: extra commands table, "Not run" line and rows for #73, #149 and #157 in the per-epic closure readiness table.
* Modified `docs/reference/README.md` and `docs/reference/log.md`: index row and log entry.
* Added `docs/reference/research/issue-73-149-157-closure-checkpoint-live-2026-11-24.md`.
* Added evidence under `.copilot-tracking/evidence/2026-11-24/issue-73-live/` (test logs, probe script, redacted probe output, screenshot).

## Validation

Tools 16 tests OK; `src/core` 270 OK (7 skipped); `src/api` 288 OK (1 skipped), run sequentially; signed-in GET probe returned 200 on all 12 routes read; relative links checked. Hosted CI not observed (no push).

## Per-criterion proven or unproven

| Epic | Criterion | Proven or unproven | Reason |
| --- | --- | --- | --- |
| #73 | #440 checkpoint | Evidence proven for demo; box left to owner | #440 is open and ticking is an owner action |
| #73 | Children closed or deferred (ticked) | Proven | 6 of 6 closed |
| #73 | Requirements trace to check or deferral | Proven except BG-011 | BG-011 is a pilot outcome measure; the owner must accept it as the recorded deferral |
| #149 | #440 checkpoint | Evidence proven for demo; box left to owner | As above |
| #149 | Child features accepted | Unproven | #152, #155 and #156 acceptance needs person-run usability and assistive-technology evidence, excluded for the demo |
| #149 | Evidence recorded; artefacts traceable (ticked) | Proven locally | UX evidence and traceability suites pass |
| #157 | #440 checkpoint | Evidence proven for demo; box left to owner | As above |
| #157 | Child features accepted | Unproven as a whole | Screen-reader testing, DPO and Legal approval and real-model operation are outside the demo; retention sweep not proven on the live revision |
| #157 | Decision accepted; no memory as evidence; consumption bounded (ticked) | Proven locally | Chat memory, privacy and routing suites pass |
