---
title: Capacity booking checkpoint correction 1 research (Refs #440 #82 #81)
description: Research for one evidence-wording correction to the eleventh checkpoint classification row
ms.date: 2026-11-06
ms.topic: reference
---

Research disposition: executed (focused, inline; no delegation). Planning Readiness: Ready.

## Brief

* Correction 1 of the new capacity checkpoint. Frozen head `147fec2196f52b4b2e76cf6caae4c3db239765f9`, tree `f0b31989a095193dd0924272b5692f72e7f0fc24`, ignored-clean at entry. Pins unchanged by supplied direction: governance `a97bea15`, lifecycle `af891a5cc`, main `bb3a3b03`.
* Trigger: root assessment finding R-C1. Documentation only; no test rerun, no source, SQL, browser or gate.

## Findings

* C1: docs/architecture/cutover-evidence-pack.md, eleventh classification table, row "193 core tests pass on the export of `af891a5cc`" overstates execution. Raw log `/tmp/l440af891/out/run.log` (sha256 `3fd61476e1c5ceb642590380499abe252872fe825855adce3734bb568edab9e6`, verified at entry) line 93 `Ran 193 tests in 65.877s` and line 95 `OK (skipped=1)`: 193 total, 192 executed, 1 declared skip, suite exit 0.
* C2: the command-details paragraph of the pack already states 193 tests, 1 skip and names the single `skipTest` "JSON-only separate-file audit ordering". It is correct and stays unchanged. Index and log say "193 tests" without claiming 193 executed.
* C3: the raw log does not itself name the skipped test (line 95 gives the count only); the name is source-attributed to the `skipTest` in the exported source, as the pack paragraph states.
* C4 (historical wording qualification, originals unchanged): the original critique Strengths line "No source, API or store schema changed in #1229" is imprecise. Source did change (appointments, gates, procurement); no new API or store schema changed. The original research heading "Source read (git diff of #1229, 23 files, +519/-16 ...)" mislabels the 23-file scope as #1229 alone; it is #1228 plus #1229 over `cd271cfa5`. The original critique and final pack distinguish them correctly.
* C5: the first author Review did not catch R-C1 and is not claimed to have. Its outcome is preserved.

## Alternatives

* Edit index and log too: rejected, they do not overstate.
* Rerun tests: rejected, observation unchanged and out of scope.

## Decision

Change only the one classification row. Record C4 qualifications in this research and the new Review, not in historical files.
