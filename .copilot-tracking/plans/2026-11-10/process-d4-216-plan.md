---
title: Plan - process D4 recovery records (Refs #216, #208)
description: Metadata-only records preserving the refused D3 partial attempt and the final independent numeric disposition
ms.date: 2026-11-10
---

## Phases

* Phase 1: write a provenance qualification under `.copilot-tracking/changes/2026-11-10/` covering the D2 zero-byte plan, the D3 duplicate-key refusal, the preserved six D3 hashes, the D1 qualifications and the unchanged source identity.
* Phase 2: write an independent source disposition under `.copilot-tracking/reviews/2026-11-10/` from the `numeric-d1-final` reviewer files, with head, coverage and limitations.
* Phase 3: write the full changes record, run one self-review after `implement-done`, check every new phase artifact is non-empty and the plan hash is unchanged, then commit with the actual `--claim-commit`.

Details: `.copilot-tracking/details/2026-11-10/process-d4-216-details.md`. Critique: `.copilot-tracking/reviews/plans/2026-11-10/process-d4-216-plan-critique.md`.

## Boundaries

* Only new `.copilot-tracking` files plus the six pre-existing untracked D3 files, kept byte-identical. No source, README, scorer, report or tracked-file edit; the empty D2 plan and the malformed D3 state are not repaired.
* No runtime, gate, install, model, cloud or private data. This plan file is never edited after `plan-done`; progress lives in the state and changes files.
* The D4 state is written only with `json.dump` from a dictionary and validated for duplicate keys at every depth before each event.
