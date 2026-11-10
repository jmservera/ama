---
title: Details - process D4
description: Phase details
ms.date: 2026-11-10
---

## Phase 1

The provenance record states the D2 plan discrepancy (911 bytes, sha256 `60cb4035...ad32` observed at D2 `plan-done`; zero bytes later and in the committed tree), the D3 refusal (duplicate `changes` key, second null; D3 reached only research-open and plan-done, then a refused implement-start; never implement, review or commit-complete), the six preserved D3 sha256 values from the Root snapshot, the D1 qualifications (refused commit-complete, stub changes record, stale review, invalid first red, import fault) and source identity unchanged at `46dfa754`. Prior numeric checks are carried by identity only.

## Phase 2

The disposition record gives reviewer id, supplied head and tree, verdict approve with no findings, both original Medium resolved, file hashes and limits: static only, no tests or Git by the reviewer, `--record` remains an operational risk, not a D4 approval.

## Phase 3

Before `commit-complete`: assert every new phase artifact size is above zero, the plan sha256 equals the `plan-done` observation, the six D3 files still match their snapshot, and no tracked file changed; then commit and supply `--claim-commit` from `git rev-parse HEAD`.
