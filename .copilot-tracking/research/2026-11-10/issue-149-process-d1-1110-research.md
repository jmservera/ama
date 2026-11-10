---
title: Issue 149 process D1 research (2026-11-10)
ms.date: 2026-11-10
---

Refs #149 #440. Research for one metadata and provenance process D1. It is not a source correction, a legacy budget reset or an automatic D2 or D3. Local only.

## Disposition

Research executed (primary agent, read-only). Planning Readiness: Ready.

## Evidence

* Baseline head `26a40c7dfc40c947888fd3d9004c0fdea4e9c3f6`, tree `8bfe74286f0246790d1bf842e1a6e2fe90a3f423`, clean, branch `feat/demo-ux-coverage-parent-149-1110`. `origin/main` re-fetched: `d52f20a5198de7269f39daf794911545aee01ced`, unchanged.
* Old integration witness log `phase149-coverage-integration-evidence-1110/issue-149/events.jsonl`, sha256 `14de2fc4610d07d8fa07f84a5ee9aa3db857026e1e8d6d2d7951e4621ff0efde`, 7 records. Actual Root verification exit 1: QUALIFIED at seq 4 `implement-start` (source changed in committed history before that boundary), plus notes that state, plan and changes artifacts changed after observation (seq 2 to 6).
* Cause (sequence): seq 1 launch observed clean local `736561ba0` at 09:13:51Z. The authorized normal fast-forward to the already reviewed remote input `ae4b20007` came after launch. Seq 2 to 4 then observed `ae4b20007` (tree `c3e755d07`), so the helper sees the inherited child commits (#1363, #1365, #1366, #1367, #1372) as source changed before this task's implementation boundary. Those commits were reviewed in their own tasks, not authored by the integration task. The own work is the normal merge `0e5758da2531564dbcceef889f1ee479c3c220f2` (tree `a9b51381c57e`, 09:21:05Z, after implement-start 09:21:00Z) and the two docs/tracking commits `92da89667`, `69f965d46` and the state commit `26a40c7df`.
* Instrument limitation: the helper compares the launch boundary with the later events and cannot tell an adopted reviewed input from own work. Local writable record, not tamperproof.
* Source identity: `git rev-parse 0e5758da:src` equals `HEAD:src` (`6502cdfe1d181e159a642ea45af9607cf1b294f5`); the 26a40 head differs from the merge only in docs and `.copilot-tracking` (9 files, additions and the corrected read window in the pack).
* Old artifact byte hashes and every tracked file under `.copilot-tracking`, `docs` and `src` are snapshotted outside the repository (`phase149-process-d1-evidence-1110/baseline-sha256.txt`, sha256 `8ef65f47d115...`) for an equality proof.

## Constraints read

The brief allows only new D1 RPI files and one separate additive provenance qualification. No source, existing docs, index, log, old tracking or checker, design or authentication repair. Original local checks carry forward only by source identity to the merge, with dates, pins and exits, and are not new runtime evidence for the metadata head, hosted CI, independent review or acceptance.
