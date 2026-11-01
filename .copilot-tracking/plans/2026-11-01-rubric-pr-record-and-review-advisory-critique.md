---
title: Rubric PR recording and Copilot review advisory plan critique
description: One final-candidate critique of the D1 and D2 plan with dispositions
ms.date: 2026-11-01
ms.topic: reference
---

## Critique execution

* Executed once, by an independent rubber-duck review of the plan, details and research. Verdict: revise required (2 blocking, 1 non-blocking). No repeat critique for this task.
* No finding conflicts with a confirmed owner decision, so all were applied directly.

## Dispositions

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Push events run with `BASE_REF=HEAD`, so `differs_from_base` never detects a changed rubric, registry, workflow or trusted script on `main`; a merged instrument-only change would skip scoring and the refresh | Accepted. For non-PR events derive `instrument_changed` from the same diff range as `diff_args` (`baseline.commit..HEAD` or fallback). Tests cover each instrument path with no artifact change |
| 2 | Single force-pushed `rubric/baseline-refresh` branch: a stale or restarted run could edit or merge a PR whose head another run replaced | Accepted. Record the pushed SHA, verify the open PR head equals it before edit and merge, merge with `--match-head-commit`, and abort with a notice on mismatch. Run concurrency already cancels older push runs per ref. Test an interleaved head change |
| 3 | Freshness `known` undefined for a missing or non-ancestor baseline commit | Accepted. `known=false`, `pending=null`, visible "freshness unavailable" line; tests for missing and non-ancestor commits |
