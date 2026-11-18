---
title: Issue 164 live audit r3 changes
ms.date: 2026-11-18
---

Refs #164. Demo only, desktop. Tier FOCUSED: documentation and evidence only, no src change; `rpi-checks.py --all` not run. Disclosure: the research note, index and log were written before the `implement-start` witness call (documentation-only task); the witness is observational.

## Files

* Added docs/reference/research/issue-164-live-chat-grounding-evidence-r3-2026-11-18.md
* Edited docs/reference/README.md (index row) and docs/reference/log.md (appended entry)
* Added .copilot-tracking/evidence/2026-11-18/issue-164-live-r3/ (probes, raw JSON, screenshots, az output, offline test output)
* Added a new state file issue-164-live-r3-state.json; the earlier issue-164-live-state.json is unchanged

## Validation

* Offline: from src/agents, `PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest tests.test_chat_heldout tests.test_chat_eval_revocation_effort tests.test_epic104_bounded_ai_invariants -v`: 54 tests, OK.
* Live: widget probe (7 asks, HTTP 200, 0 model calls), registry read, read-only az show; secret scan of JSON found no `@`.
* mypy, ruff and web checks not applicable (no src or web change).

## Per-criterion proven/unproven

| Criterion | Status |
| --- | --- |
| Thresholds approved; chat task registered with accountable reviewer and enable state | Partly proven: registered and disabled, proven; thresholds `proposed` and accountable individual `unknown`, unproven |
| Results bound to actual serving-model and control versions, approved thresholds, reviewers | Unproven: no actual-model result, no approval |
| Competent human exercises block seeded critical suggestions | Unproven: needs competent people |
| Actual-call authority, payload/provider handling, human-exercise approvals | Partly proven: no call or spend; approvals and finite chat-call authority absent |

Production-only (not claimed): real held-out data, production memory, production enablement, named accountable individuals. No criterion newly tickable. Adverse: the "text the resident" ask falls back without a refusal route.
