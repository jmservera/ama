---
title: Issue 146 critique, live2 (single pass)
---

Verdict: proceed. Findings applied directly.

* Keep the change in `infra/scripts` and `infra/tests`; do not touch `src/` (focused tier) and do not edit Bicep.
* Job names must not be parsed out of rule names; take them from an explicit `--jobs` list so absence is detectable. Rule name for job J is `alert-J-failed`.
* Without `--jobs` behaviour must stay unchanged (existing tests).
* A partial result must not read as enabled; `all_classes_enabled` must be false.
* Output carries names and booleans only.
