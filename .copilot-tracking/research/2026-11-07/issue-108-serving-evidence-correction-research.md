---
title: Issue 108 corrective research (execution-order and serving-evidence overclaim)
description: Corrective RPI iteration 2 research for issue 108, written before any document revision
ms.date: 2026-11-07
---

## Disposition

Research executed for a corrective iteration. Planning Readiness: Ready. Written before any source or document revision in this iteration; the plan, details and critique are written after it and confirmed present before implementation.

## Acknowledged original order violation

The original iteration (commits `d777f7e2f`, `84ae95d83`) edited the synthesis (log `/tmp/rpi-108-demo-metadata-1107.log` line 116) before the first plan creation (line 150) and research creation (line 153). Its research, plan, critique and Review files were therefore retrospective in order and are adverse historical evidence of process, not proof of a prospective research, plan, implement, Review loop. They are preserved unchanged. Content facts and the passing partial receipt for `84ae95d8` stay historical.

## Evidence on the draft

* `docs/reference/resources/ai-tokenomics.md` lines 294-307 say the provider response `model` plus "retained serving attestation" can support the serving version, and line 351-353 name "serving attestation" for a call. Neither separates version confirmation from physical processing region.
* The original state follow-up rank 2 says a finite real call "Closes the serving region/version gap". That overclaims: a response `model` identifier can inform version confirmation, but it does not attest the physical processing region or data residency.
* Official source already cited (Foundry deployment types, retrieved 2026-11-07): Global types may process in any Azure region. No source in this iteration shows a response field that reveals the processing region; none is invented.
* Issue #108 criteria unchanged and unticked; this iteration reads no Azure resource, makes no call and infers nothing about the serving region.

## Decisions

* Clarify only the prose in the existing section; keep every figure, unknown, budget and gate.
* State that region or data-residency evidence needs source-qualified provider or operational attestation plus the relevant named approvals.
* Correct the follow-up overclaim in the new state record, not in the original state file.
