---
title: Issue 149 axe statement D2 research (2026-11-10)
ms.date: 2026-11-10
---

Refs #149 #440. Research for one bounded process D2 (D1 spent; no D3, no source correction, no budget reset). Local only.

## Disposition

Research executed (read-only). Planning Readiness: Ready.

## Evidence

* Baseline head `be5a3b5daa877f47451350b5117ea758cef7355a`, tree `6bd78a025b19a5b032adb8fe19255b94ff93a3c2`, clean; `HEAD:src` `6502cdfe1d181e159a642ea45af9607cf1b294f5`; `origin/main` `d52f20a5198de7269f39daf794911545aee01ced` unchanged.
* Statement at `docs/architecture/cutover-evidence-pack.md:6341`: "Axe: ran in the six role-screen stories (the programme stories at 1280 px on `main` only, ...)". Raw logs `phase149-coverage-integration-evidence-1110/checks/M1-roles-*.log` and `B4-roles-*.log` contain axe lines only for selectors 230 (5), 231, 231q, 231p, 231qp (3 each); `M1-roles-default.log` has none. Atlas, paging and Held logs state that axe did not run. So the "six" overstates: five selectors ran axe, default did not.
* Independent reviewer `fa061121-54f6-4539-9300-392d0d7f2ed5` (original assessment under `independent-149-integrated-parent-1110/`): head `be5a3b5da`, 128 files, 5420 lines read in full, verdict approve_with_comments, 2 Medium (existing #1362 checker false positive; existing #156 M1 empty-page vs empty-set), 0 Critical/High/Low. Reviewer limits: no fresh guideline retrieval, no independent git or hash execution, no tests, baseline logs not exhaustively read.
* Follow-up `fresh-guidelines-baseline/`: additive, same head; Root retrieved the guidelines at 09:38:16Z (sha256 `d246b026f4f29b5823a9cc857f9edf3d2507002e055e32040cadeaf3b38e0234`, hash supplied by Root, not recomputed by the reviewer); all B1-B5 logs read; `app.js` hunks pass the fetched guidelines; one NEW Medium documentation-contract overstatement (the axe statement); cumulative 3 Medium, 0 Critical/High/Low.
* Artifact sha256: original findings `f17b788f98905c59...`, original ledger `074aa619e9707bc0...`, follow-up findings `bcdfcf91b15c27f8...`, follow-up ledger `6b3bf87ca10b1bb...`, guidelines text `c99f5a07dae3b1a9...` (full values in the qualification).

## Constraint

Only mutable existing path: the new 149 checkpoint axe line. Everything else, including the index and log, stays unchanged; the old literal statement is preserved in D2 records, not erased.
