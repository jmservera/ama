---
title: Issue 149 parent main ecb2 integration changes
ms.date: 2026-11-08
---

## Changes

Merge commit f642777d (parents fd48abc9 and ecb28815). No conflict, no source edit by this continuation.

## Source-preservation proof

* `src/api`, `src/core`, `tools`, `infra` and `.github/workflows`: raw diff from fd48abc9 is empty (bytes and modes).
* Only `src/agents` (README, `chat_eval.py`, its test) differs from fd48abc9; it equals main, arrived through earlier main PR 1284, and nothing under `src/api` or `src/core` imports `chat_eval`. It is outside the 149 selected paths.
* Rubric score JSON parses. Main-relative delta is the parent's 14 non-tracking paths plus tracking records; the log and index show 0 removed lines against main, and the parent's earlier log entries are present.

## Validation

Docs-only integration tier: structural JSON parse, diff and byte-identity proof only. Unit, browser and axe checks were not rerun because no relevant input changed. The original fd48abc9 evidence (76 API, 19 Core, atlas 194, data operator 100 with two axe scans, 212 installed files) stays original evidence for that head, with its harness, archive and date-path qualifications. No whole-issue, AT, model or human acceptance. Refs #149 and #229 only.
