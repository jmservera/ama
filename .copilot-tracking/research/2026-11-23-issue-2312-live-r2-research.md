---
title: Issue 2312 live r2 research (2026-11-23)
ms.date: 2026-11-23
---

## Research disposition

Executed. Planning Readiness: Ready. Parent task `issue-2312-live` (research, changes and review read first) delivered all four criteria; this pass looks for gaps in that delivered code.

## Evidence (probes run on the base with the synthetic manifest and predictions)

* A prediction whose `critical_errors` is a string instead of a list is iterated per character: 13 bogus "undeclared critical error" messages (`a`, `c`, `d`, ...), and the declared error observed count stays 0.
* A held-out case with no prediction entry raises no input error: it is silently scored wrong, so an incomplete prediction file is indistinguishable from a wrong model.
* A duplicated critical error in one case counts twice against `max_critical_misses` (observed 2), inflating the count relative to cases.
* No command-line entry point exists, so "a runner that reports results" can only be used from Python. `heldout_freeze.py` has no CLI either.

## Per-criterion status of the issue (live probe, no Azure involved)

All four criteria are offline code criteria; the first three are already proven by tests in the parent commit. Criterion 4 (approvals under #108) is owner-gated and is not asserted. No Azure resource is needed or created; the demo estate is untouched.

## Design decision

Add strict prediction-shape validation (each held-out case must have an object with a string `answer` and a list of strings `critical_errors`; shape faults become sorted `input_errors`), count each critical error name once per case, and add a `python -m zava_forward.agents.eval_harness` CLI (manifest path, predictions path, optional recorded result path to verify) with exit codes 0 pass, 1 fail/invalidated, 2 unusable input.
