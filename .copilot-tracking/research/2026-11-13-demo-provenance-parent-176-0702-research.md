---
title: "#176 provenance publication parent packaging research"
date: 2026-11-13
---

## Scope

Package the frozen LOCAL child `25a7135b1b6046b960e5993e7f7333bfb7055347` (branch `fix/demo-document-provenance-176-0649`, based on main `33c261a639b768e06bbd7fe0bd8840d71e3f05bd`, built on source diagnostics `472b3261a`) into a compact publication parent on `fix/demo-provenance-parent-176-0702` (base `5661ef2123f9e9b62a567bcd6fb537bf67b8c2d0`). Packaging only: no source, schema, behavior or provenance-claim change; whole #176 stays open. Disposition: executed (new investigation of the diff, blobs and policy).

## Evidence

* Base `5661ef212` is a descendant of main33 and differs from it only in `.github/rubric/scores/latest.json`; none of the child's changed paths are touched by base.
* `git diff --name-status 33c261a63 25a7135b1` lists 36 added or modified paths: three source/test files, `docs/reference/log.md` (one appended entry), and RPI/evidence records for the 0638 diagnostics and the C2 provenance loop.
* Two child files, `before-document_form_fixtures.json` (17,887 lines, 484,017 bytes) and `before-document_control_fixtures.json` (3,130 lines, 72,189 bytes), are raw pre-change snapshots. Their Git blobs equal the main33 and base blobs of `src/importer/evals/document_form_fixtures.json` (`e39d618e788d...`) and `src/core/evals/document_control_fixtures.json` (`360dc62a2dad...`); SHA-256 of both pairs also matches the child's `before-sha256.txt`. They are therefore not unique and carry no evidence absent from public main.
* The child's untracked `.venv-176c2` is not in the commit and is not published.
* The [tracking retention policy](../../docs/reference/method/tracking-retention-policy.md) says heavy generated outputs belong outside the checkout, keep dated records of commands and inputs, and give no deletion authority. This packaging deletes nothing.
* `docs/reference/log.md` is also appended by published docs checkpoint PR1506, which merged after this base. A textual conflict is possible at the file end; both entries must be kept when explicitly reconciled.

## Planning Readiness

Ready.
