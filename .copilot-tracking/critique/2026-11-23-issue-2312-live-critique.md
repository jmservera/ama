---
title: Issue 2312 live critique (2026-11-23)
ms.date: 2026-11-23
---

## Execution and verdict

Executed once on the final candidate plan. Verdict: proceed with amendments applied directly.

## Findings and dispositions

* The synthetic manifest carries a threshold approval so `check_freeze` returns `frozen`. Disposition: name the approver as a synthetic fixture and have every result carry the freeze note, so no approved threshold is claimed (criterion 4).
* A result could be replayed after a version change. Disposition: the recorded result stores the manifest digest and all five versions; `verify_recorded` compares both and names the changed version.
* A runner that scores an unfrozen manifest would hide gaps. Disposition: refuse with outcome `not_frozen` and list the gaps.
* Predictions reporting an undeclared critical error would pass silently. Disposition: count it as an input error that fails the run.
* Determinism: sort all outputs, no clock or randomness in the result.
