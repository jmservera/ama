---
title: Issue 1845 withdrawn-sensor canary plan critique
description: Single original critique of the canary repair plan, with verbatim reviewer findings and dispositions
ms.date: 2026-11-17
ms.topic: reference
---

## Execution

* Critique executed once, by an independent read-only `rubber-duck` subagent,
  on the first draft of the plan and details (regex matcher over serialized
  JSON). Not repeated for this task.
* Verdict: Revise.

## Reviewer findings (verbatim)

1. **Blocking: matcher weakens privacy coverage.** The regex in the details file
   (phase 1 helper) misses `23.70` and a canary preceded by an escaped Unicode
   digit; the current substring check catches both. It does catch `x23.7`.
   Fix: retain substring checks for JSON strings and keys; handle numeric
   values separately, including equivalent numeric readings.
2. **Significant: clean metadata can still collide.** The matcher flags
   `"sensor-v23.7"` and numeric metadata equal to `23.7`. The latter is
   indistinguishable by value alone from a leaked numeric reading. Fix:
   specify and test how metadata is distinguished without blanket stripping;
   if identical values lack enough context, resolve that ambiguity before
   claiming universal clean-metadata acceptance.
3. **Significant: failing-before evidence is incomplete.** The details test
   the clean collision at helper level, not through the integration
   assertion; simultaneous leak mutations can fail on the first projection
   and mask the rest. Fix: inject clean collisions into the actual
   integration path, then independently inject each canary into each
   projection and verify the named assertion fails.

## Dispositions

| Finding | Disposition | Applied change |
| --- | --- | --- |
| 1 | Accepted | Matcher now walks the parsed projection: string values and keys keep the original substring check; numeric leaves are compared by numeric value (so `23.7` and `23.70` match, `1794924123.7340033` does not). The regex is dropped. |
| 2 | Accepted in part | No stripping. A numeric leaf exactly equal to the canary is still treated as exposure (conservative); the plan states this limit instead of claiming universal acceptance. A string such as `sensor-v23.7` keeps the original substring behaviour, so there is no new false negative. |
| 3 | Accepted | Failing-before now injects clean colliding timestamps into the real integration path, and injects each of the original and edited canaries into each of the four projections one at a time, expecting the named projection assertion to fail. |

No finding conflicts with a confirmed decision. No second critique is run.
