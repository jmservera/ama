---
title: Issue 149 integration provenance qualification (2026-11-10)
ms.date: 2026-11-10
---

Refs #149 #440. Additive provenance qualification written by the coordinator for one metadata process D1. It is not an independent assessment, an approval, a waiver, a source correction, a cure of the old witness chain or a new runtime test. One D1 debit; no D2 or D3 is started and no legacy budget is reset. Local only.

## Original witness chain (preserved, unedited)

* Log `phase149-coverage-integration-evidence-1110/issue-149/events.jsonl` (session ROOT), 7 records, sha256 `14de2fc4610d07d8fa07f84a5ee9aa3db857026e1e8d6d2d7951e4621ff0efde`, final head `26a40c7dfc40c947888fd3d9004c0fdea4e9c3f6`, tree `8bfe74286f0246790d1bf842e1a6e2fe90a3f423`.
* Actual verification: exit 1, not a pass. Literal qualification at seq 4 `implement-start`: "source changed in committed history before implement-start" for 12 paths (`app.js`, atlas and paging and role-screens checkers, their tests, #156 design notes, `src/api/README.md`, index and log). Notes only: state, plan and changes artifacts changed after observation (seq 2 to 6).
* The original handoff `handoff-149-coverage-integration-1110.md` reported this exit 1 and QUALIFIED reason correctly and is not corrected.

## Exact sequence

| Step | Time (UTC, 2026-11-10) | Identity | Authorship and status |
| --- | --- | --- | --- |
| Seq 1 launch, recorded by Root | 09:13:51 | clean local `736561ba0cccb9beb69eea3ae0d3a997bd0dd9bd`, tree `5ad73beb3` | Observed before the input adoption |
| Authorized normal fast-forward to the reviewed remote input | about 09:13 to 09:19 | `ae4b20007ec9bc1d4bd5dd3eef91445f29f5e50f`, tree `c3e755d07edf` | Already reviewed input adoption. The child commits #1363 (#233), #1365 (#231), #1366 (#230), #1367 (#153) and #1372 (#156) were reviewed in their own tasks. This task did not author them and the record does not claim it did |
| Seq 2 research-open, 3 plan-done, 4 implement-start | 09:19:57, 09:20:51, 09:21:00 | head `ae4b20007` | Own actual events; the helper compares them with seq 1 and so sees the inherited commits as source changed before this implementation boundary |
| Own prospective main integration | 09:21:05 | normal merge `0e5758da2531564dbcceef889f1ee479c3c220f2` of `d52f20a5198de7269f39daf794911545aee01ced` (tree `a817c8480a08`), tree `a9b51381c57eb233e8aae2371a3b8456e23147ab`, no conflict | Own work, after implement-start |
| Own docs and tracking commits | 09:25:59 to 09:26:33 | `92da89667`, `69f965d46`, `26a40c7df` | Own work; seq 5 implement-done, 6 review-done, 7 commit-complete |

Instrument limitation: the helper cannot distinguish an adopted reviewed input from own source work when the adoption follows launch. The record is local and writable, not tamperproof and not host or model attestation. The original integration review and critique are the task's own self-checks, not independent assessment.

## Source identity and carried-forward local checks

* `HEAD:src` is `6502cdfe1d181e159a642ea45af9607cf1b294f5`, equal to `0e5758da:src`. The final head differs from the merge only in docs and `.copilot-tracking` (9 files). This metadata candidate adds only new files under `.copilot-tracking`.
* The original local checks were run on 2026-11-10 at about 09:15 to 09:25Z against the merge source, with Python 3.12.3, ruff 0.17.1, mypy 2.4.0, Playwright 1.64.0, Chromium 156.0.8078.4 and an owned virtual environment. They carry forward by that source identity only, as recorded in the cutover pack section "Parent 149 coverage integration checkpoint (2026-11-10, Refs #149 #440 #153 #156 #230 #231 #233 #96)": API unit 194 run, 4 opt-in skips, exit 0; handoff browser 9 OK, exit 0; Core `test_import_refusals test_atlas_screen_trace` 38 run, 7 opt-in SQL skips, exit 0; importer 79 OK, exit 0; ruff, format and file-less mypy clean for API, Core and importer, exit 0; role-screens (47, 70, 36, 36, 47, 46), atlas 362, paging 89 and Held download 31 PASS under one nonqueued `flock -n /tmp/ama-rpi-heavy.lock` admission, exit 0; axe only in the role-screens stories.
* The M4a Core command fault (exit 1, missing `PYTHONPATH=tests`) and the later M4a2 pass (exit 0) both stay preserved in the raw logs (`phase149-coverage-integration-evidence-1110/checks/`, manifest `SHA256SUMS`).
* These are not a new runtime test against this metadata head, not hosted CI and not independent review.

## Limits

* No independent exact-head assessment of the integrated final parent has happened; Root must review the complete current-main-relative source and metadata and the raw integration evidence before publication.
* No whole #149 or #440, UX, WCAG, assistive-technology, human, content, design, SQL Server, model, cost or approval claim. #1362 (checker false positive, correction balance UNKNOWN), #156 M1 and PR 1371 and #1373 repairs are untouched and unresolved here. No source, existing docs, index, log or old tracking file changed.
