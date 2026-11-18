---
title: Issue 221 restart authority and suspension drill evidence (demo)
description: Repository-check evidence on 2026-11-18 for the two open criteria of #221, with the live Azure boundary stated
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 221
  - RULE-024
  - NFR-014
estimated_reading_time: 3
---

Refs #221. Scope is the synthetic desktop demo. The owner authorised live Azure on 2026-11-18 but excluded drills, so the drill was run as a repository test, not against the demo apps.

## Method

From `src/core` in the worktree: `PYTHONPATH=src:tests python3 -m unittest tests.test_operator_suspension_drill tests.test_restart_gate_sql_fences tests.test_governance -q` gave `Ran 101 tests ... OK (skipped=18)`. The two drill modules ran verbosely with all 15 tests `ok`. Live read: `ca-cutover-test-demo-api` revision `--0000031` is Running on image digest `sha256:5368f4e4...c5fb`. No source changed.

## Per-criterion result

| Criterion | Result | Evidence |
| --- | --- | --- |
| Guardrail breach record names restart authority per RULE-024 | Proven in repository tests | `restart_authority.py` validates the authority (rejects blank, placeholder, memory and AI authorities, and automatic restart); `governance.py` refuses a restart when the breach record lacks a valid authority or the restart cites another one. Tests `test_rule_024_rejects_invalid_authority_and_enforces_multi_actor_separation`, `test_validate_restart_authority_rejects_blank_placeholder_memory_and_ai`, `test_self_designation_distinct_actor_and_privacy_non_echo` pass. |
| Suspension and manual fallback drill is tested (NFR-014) | Proven in repository tests | `test_nfr_014_end_to_end_suspension_manual_fallback_hazard_and_restart_drill` passes: suspension, manual and hazard routes, then a gated restart. The SQL fence tests (`test_restart_gate_sql_fences`) also pass. |

## What this does not prove

* The checks ran on the worktree code, not the deployed image; the image digest was not mapped to a commit, so the live app is not shown to contain this code.
* No breach, suspension or restart was exercised on live Azure (drills excluded by the owner), and the SQL tests that need a server were among the 18 skipped.
* A real drill by named operators is production work (#1905-#1908).
