---
title: Provenance - numeric D1 witness qualifications (Refs #216, #208)
description: Actual cause and narrow scope of the refused commit-complete and related qualifications of the numeric D1 chain
ms.date: 2026-11-10
---

## Scope

Metadata only. It records facts about the numeric D1 candidate `4e61626b7765b77bef630165d4725e06c8febe1c` (tree `acac6ccf974d15740c0908930458daf5585b7dc3`, parent `ab365e53d024e269c9ad4f0b0e33a8361a43e30b`). It does not cure the old RPI chain, does not witness the older source reasoning, and adds no runtime evidence. Process D2 is a finite debit after the spent source D1; the historical issue balance is UNKNOWN; no reset, no automatic D3 and no source grant.

## Preserved old chain (unchanged)

* Witness `phase216-numeric-d1-evidence-1110`: 7 records, log sha256 `85c40318dd82f9f6c95e935c783774be1633e6a50deafe947e3b0a1593645c83` (re-hashed during this process, equal). Events 1 to 6 ok; seq 7 `commit-complete` REFUSED.
* Actual verify exit 1, output kept at `verify-216-numeric-d1-1110.txt` in the session files.
* No retry, edit or resurrection of that chain.

## Actual cause and narrow qualification

* Refused commit-complete: the D1 `record commit-complete` call omitted `--claim-commit`. The launch record asserts `commit_claim` null, so the helper compared a null claim to the real HEAD and refused ("commit claim does not match the actual HEAD"). The commit itself exists, clean, with the required trailer. The refusal is a process omission, not a source defect.
* Stale review: `review-done` observed the uncommitted delta; the commit came after it, so verify reports the review source as stale against the committed tree. That is the review-then-commit order, not a changed reviewed source (the commit contains only the reviewed delta plus tracking evidence).
* Implement-done stub: the first attempt to write the full changes record failed because the file already existed, so `implement-done` observed the stub. The record was completed afterwards and discloses this in its own text.
* Retained D1 adverse attempts: first derived-ratio red used unpaired participants and failed for the wrong reason; a combined unittest invocation failed on import path set-up; the first command-tests run failed on the same unpaired test. Outputs are in the D1 evidence directory `commands/`.

## Source identity (observed read-only in this process)

* HEAD, tree and parent as above; status clean at start.
* `git diff --name-only ab365e53 4e61626b -- src` lists exactly `src/agents/README.md`, `src/agents/evals/run_regulatory_gates.py` and `src/agents/tests/test_paired_report_command.py` (+67/-14). The scorer `paired_trial.py` sha256 `85450ae64373dcfb60fb1cdca22ab9e7083d1b72daaa140758687c2e9ddd7736` is unchanged.
* D1 test and lint results are carried by this exact source identity only; no test was rerun here.

## Not claimed

The numeric D1 delta has not been independently resolved. The same reviewer will inspect the actual numeric source delta and evidence after this frozen candidate. Whole issues #216 and #208 stay open.
