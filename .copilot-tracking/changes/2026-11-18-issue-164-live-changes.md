---
title: Issue 164 live changes
description: Changes and per-criterion proven/unproven table for issue 164 live evidence
ms.date: 2026-11-18
---

Docs and evidence only; no `src/` or `infra/` change. Tier FOCUSED. Basis: no source, SQL, security-control, infrastructure or deployment change; Azure access was read-only and one synthetic chat thread was created and deleted.

## Files

* Added `docs/reference/research/issue-164-live-chat-grounding-evidence-2026-11-18.md`.
* Updated `docs/reference/README.md` (index row) and `docs/reference/log.md` (appended entry).
* Added evidence under `.copilot-tracking/evidence/2026-11-18/issue-164-live/` (probe script, JSON, Azure settings, screenshot).
* RPI artifacts: research, challenges, plans, details, this file, review, state.

## Per-criterion table (issue 164 unticked criteria)

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Thresholds approved; chat task registered with accountable reviewer and enable/disable state | Partly proven | Registered, `enabled` false, demo switch owner `jmservera`; thresholds `proposed`, no approver, accountable individual unknown |
| 2 | Results bound to serving model and control versions with approved thresholds, reviewers, outcomes | Partly proven | Versions recorded; no actual-model chat result (0 dispatches); thresholds unapproved; no reviewer |
| 3 | Competent human exercises on seeded critical suggestions | Unproven (needs people) | Not obtainable for the demo; offline panel evidence only |
| 4 | Actual calls need approved payload handling and finite authorisation; human consent/accessibility/privacy approval | Partly proven | No model call occurred (held unknown liability); caps are engineering limits; payload/provider approval and consent absent |
| 5 | Criteria do not authorise implementation, memory, calls, deployment or live use | Consistent; nothing to prove | Task stays unapproved, demo-only, memory off for user |

No criterion is newly tickable.

## Validation

* Offline: `tests.test_chat_heldout tests.test_chat_eval_revocation_effort tests.test_epic104_bounded_ai_invariants` from `src/agents`: 54 tests, OK.
* Live probe: all calls HTTP 200 after the disclosed first failed thread attempt; credential literal scan clean.
* mypy and ruff: not applicable, no Python source or infra file changed.
* Hosted CI: not observed; no push or PR by instruction. `rpi-checks.py --all` not run, by instruction.
