---
title: Issue 2312 live research (2026-11-23)
ms.date: 2026-11-23
---

## Research disposition

Executed. Planning Readiness: Ready.

## Evidence

* `src/agents/src/zava_forward/agents/heldout_freeze.py` already checks a freeze manifest (versions, held-out split, expected outcomes, critical errors, cohorts, thresholds, digest-bound approval) and returns `frozen` or `insufficient`. It does not run an evaluation.
* `src/agents/tests/heldout_freeze_fixture.py` holds a synthetic manifest; no JSON schema or checked-in example file exists.
* `jsonschema` 4.10.3 is installed; `zava_forward.core.rai_release.digest` is the canonical SHA-256 helper.
* No existing runner scores predictions against a frozen manifest or binds a result to the frozen versions.

## Design decision

Add `eval_harness.py` beside the freeze check. Reuse `check_freeze` as the gate. Add a JSON schema and a synthetic manifest plus synthetic predictions under `src/agents/evals/`. The runner is offline and takes predictions as data (no model call). The recorded result stores the manifest digest and the five versions; `verify_recorded` invalidates it when any differs.

## Acceptance criteria

Each criterion is code-provable offline; no live Azure resource is needed and none is created.
