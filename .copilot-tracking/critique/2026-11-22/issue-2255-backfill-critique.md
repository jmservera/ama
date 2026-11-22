---
title: Issue 2255 critique
date: 2026-11-22
---

# Critique (one pass, final candidate)

Verdict: proceed with changes applied directly.

* Overwriting an existing `aware_at` would corrupt a real record: the tool skips any hazard that has one (applied).
* Inventing `response_due_at` would impersonate the hazard service: not written; the reference clock derives the target (applied).
* Safeguarding items must not be re-dated for a demo: skipped (applied).
* Re-dating needs to stay visible and reversible: `demo_clock_seed` marker keeps the original `noticed`, plus one audit entry with counts (applied). A revert mode is not built; the marker and audit entry identify every change if the owner wants one.
* Writing outside the store would skip queue flags and the audit chain: the tool uses `store._case`, `store.audit` and `store.save` only (applied).
* A one-shot run is not idempotent by design: a second run finds nothing to write because `aware_at` is now set.
* The tool lives in `infra/scripts`, not `src`, so it is not shipped in the image; it is staged through exec. The live SQL write still takes the full tier (not published, no rpi-checks --all run here).
