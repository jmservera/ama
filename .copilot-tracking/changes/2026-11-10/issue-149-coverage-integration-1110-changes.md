---
title: Issue 149 coverage parent integration changes
description: Changes and execution record for the main merge and focused qualification of parent 149
ms.date: 2026-11-10
---

## Status

Implementation complete (P1 to P4). Single Review pending; it owns the final boundary.

## Log

* Input state: branch `feat/demo-ux-coverage-parent-149-1110` at `ae4b20007ec9bc1d4bd5dd3eef91445f29f5e50f` (fast-forwarded from `736561ba0` at 09:13Z), main `d52f20a5198de7269f39daf794911545aee01ced`.
* Merge: `git merge --no-ff origin/main` produced `0e5758da2531564dbcceef889f1ee479c3c220f2`, tree `a9b51381c57eb233e8aae2371a3b8456e23147ab` (equals the prospective tree), parents `ae4b20007` and `d52f20a51`. No conflict, no hand resolution. Main delta 24 and parent delta 12 non-tracking paths verified; overlap only `docs/reference/README.md`, `docs/reference/log.md` and `src/api/README.md`.
* Qualification: baseline B1 to B5 on the unmerged input and combined M1 to M5 all exit 0 except M4a, my own command fault (missing `PYTHONPATH=tests`), kept as original and rerun as M4a2 (exit 0). Raw logs are in the Root evidence directory `checks/` with `SHA256SUMS`.
* Documents changed: `docs/architecture/cutover-evidence-pack.md` (new dated section at the end), `docs/reference/README.md` (one paragraph), `docs/reference/log.md` (one appended entry). No source, test, workflow or manifest file edited.
* Web read: Web Interface Guidelines fetched in full; the changed `app.js` and `role-screens.js` hunks were read only and no web file was edited.
* Deviations: none from the plan. Residuals: #1362, PR 1371 test, #156 M1, hosted CI and independent assessment remain open for other owners.
