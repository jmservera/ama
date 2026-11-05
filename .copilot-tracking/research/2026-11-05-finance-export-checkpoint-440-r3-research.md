---
title: Finance export checkpoint r3 research (Refs #440 #96)
description: Prospective audit of one evidence statement about the failed initial archive-root attempt
ms.date: 2026-11-05
ms.topic: reference
---

Research disposition: executed inline (focused, audit mode). Planning Readiness: Ready.

## Scope

Audit only the pack sentence in the ninth finance checkpoint saying the initial failed archive-root attempt's output "was not preserved, so only the repaired exit 0 is evidenced". Head `8e750e420e7f426fb1bdb8feff585fc5b4b95a72`, tree `57e9c209c9f8938d693c5ea42d55f83346a55a91`; target, finance source and main unchanged (verified). Original and r2 records stay as historical snapshots.

## Findings

* C1 The retained native log `/tmp/rpi-440-finance-export-checkpoint-20261105.log` (sha256 `2478faf4600cdb22390c14dbc3bde2a85d60f04021722f29273015b05ea90c70`, lines 54-61) shows step "Run light form tests on pinned source" failing before step "Diagnose archive layout". Exact retained snippet:

```text
/bin/bash: line 1: cd: /tmp/f440fin/src/core: No such file or directory
Failed with exit code 1
```

* C2 The failure was on the shell `cd`, before any Python import or test command, so no test execution occurred in that attempt. No dedicated per-test output file was created for it; `/tmp/f440fin/run.log` belongs to the repaired run (40 tests OK, 21.384s).
* C3 The r2 statement is therefore wrong: wrapper error and exit 1 are preserved, only a dedicated test output is absent.
* C4 The snippet holds no secrets; unrelated log content must not be copied.

## Decision

Correct the live sentence, persist the snippet in r3 records, append one log correction, keep the repaired exit 0 historical and not rerun. Contrarian check: rewriting r2 or prior log lines is rejected (append-only, historical snapshots).
