---
title: Details - process D3
description: Phase details
ms.date: 2026-11-10
---

## Phase 1

The provenance qualification states the exact discrepancy: D2 plan 911 bytes, sha256 `60cb4035...ad32` at the D2 plan-done observation; 0 bytes (`e3b0c442...b855`) at implement-done, review-done and in the committed tree. It states the inferred truncation cause, that the old path and chain are preserved unrepaired, that D2 is not full unqualified evidence, and restates the D1 qualifications (refused commit-complete, stub changes record, stale review, invalid first red, import fault). It records source identity unchanged at `46dfa754` and the targeted checks carried by identity only.

## Phase 2

The disposition record lists reviewer id, supplied head and tree, base, verdict approve with no findings, both original Medium resolved, the 19-file delta and raw-log coverage, file hashes, and limitations: static only, no tests or Git executed by the reviewer, Ruff and default-byte equality are producer claims, `--record` still an operational risk. It is not a future independent pass.

## Phase 3

Before `commit-complete`, check every new file has size above zero and the plan hash equals the hash observed at `plan-done`; then commit and supply `--claim-commit` from `git rev-parse HEAD`.
