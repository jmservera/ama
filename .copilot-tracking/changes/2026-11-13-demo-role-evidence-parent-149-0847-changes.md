---
title: Role-screen evidence parent integration changes
description: Changes and verification for the main-based integration parent
ms.date: 2026-11-13
---

## Changes

* Merged `32fd2163547589b50f1e4e4bea4407321b82ab71` (#231 review) and `eeb8ec157905265355f94177f9280863ba92486e` (#232 original `fbd12ac9` plus recovery) with `--no-ff` merge commits after the prospective critique commit `d9b33e7cb`. No cherry-pick, no rewrite.
* Appended one section to `docs/architecture/cutover-evidence-pack.md`, one index row to `docs/reference/README.md`, one entry to `docs/reference/log.md`.
* Base `347962dace94171724cc8db4044c8d783335fecf` (fetched, unmoved).

## Verification (local, docs-only tier)

* Blob equality: 6 of 6 #231 paths, 35 of 35 #232 paths (including the 16 original-commit paths) equal their child blobs in the parent; 0 mismatches. Child path sets do not overlap.
* `src`, `infra`, `tools` and `.github` have no diff against the base; the only non-`.copilot-tracking` changes are the three docs files.
* The evidence pack and log keep their prior content as a byte prefix. `git diff --check` passes, no non-ASCII in added lines, secret scan shows only a benign guideline phrase.
* No executable test, full gate, browser, SQL, install or network write was run. Hosted CI and human approvals are not claimed.

## Outstanding

Independent Review of the frozen candidate; root assessment before publication; one eventual main PR with Refs only (#149, #231, #232, #151, #440), no closing keywords. No push, PR, issue, board or AC write.
