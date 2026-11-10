---
title: Research - process D2 provenance for the numeric D1 candidate (Refs #216, #208)
description: Metadata-only research of the refused commit-complete and related D1 process qualifications
ms.date: 2026-11-10
---

## Execution

* Research disposition: executed (read-only inspection of git, the D1 witness log, verify output and tracking records). No source edit, no nested agent, no runtime rerun.
* Start identity (observed): HEAD `4e61626b7765b77bef630165d4725e06c8febe1c`, tree `acac6ccf974d15740c0908930458daf5585b7dc3`, parent `ab365e53d024e269c9ad4f0b0e33a8361a43e30b`, status clean.
* Debits: source D1 spent; this process D2 is another finite debit. Historical balance UNKNOWN; no reset, no automatic D3, no source grant.

## Observations

* D1 witness log (`phase216-numeric-d1-evidence-1110`): 7 records, sha256 `85c40318dd82f9f6c95e935c783774be1633e6a50deafe947e3b0a1593645c83` (re-hashed now, equal). Seq 7 `commit-complete` outcome refused: "commit claim does not match the actual HEAD". Actual verify exit 1.
* Cause: the D1 `record commit-complete` call omitted `--claim-commit`, so the commit claim recorded at launch (null) was compared with the real HEAD. The commit itself exists and is clean.
* Stale review: `review-done` observed the uncommitted delta; the commit followed, so verify reports "review source is stale". Narrow and expected for review-then-commit order.
* The `implement-done` witness observed a stub changes record because the first full-record write failed (file existed); the record was completed afterwards and discloses it.
* Source delta from `ab365e53` to HEAD is exactly three files: `run_regulatory_gates.py`, `test_paired_report_command.py`, `src/agents/README.md` (+67/-14). `paired_trial.py` sha256 `85450ae64373dcfb60fb1cdca22ab9e7083d1b72daaa140758687c2e9ddd7736` unchanged.
* Original independent assessment: reviewer `6339ad63-3729-49ea-924b-b9293482c70d`, findings sha256 `20cc5257ea2f29fbb335d97ccf607c2cbde7947cdf8f4e758d016593c798f7cb`, read-ledger sha256 `4be9a340390a63255250bec1b145e78f307674dbd69a519f643224bc6984fc97`.

## Planning Readiness

Ready: write NEW provenance and independent-record artifacts only.
