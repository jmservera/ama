# Changes 2026-11-24: issue 157 live recheck

Status: implemented and reviewed locally. Tier: full (src change); the coordinator runs the gate and external receipt. No push, no PR.

## Source changes
* `src/core/src/zava_forward/core/chat_privacy.py`: `ChatPrivacy.sweep_retention` (hourly throttle, failure logged, never blocks chat); `add_memory` counts live items only.
* `src/core/src/zava_forward/core/chat_isolation.py`: `current_user` calls the sweep.
* Tests: `src/core/tests/test_chat_privacy.py` (three tests, both stores), `src/core/tests/test_chat_memory.py` (one test). All failed first (6 errors), now pass.
* Docs: `docs/reference/research/issue-157-retention-enforcement-live-2026-11-24.md`, storage approval note, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation
* core: 98 tests OK (privacy, memory, threads, single-route); api `test_*chat*.py`: 550 OK, 1 skipped; ruff clean; mypy only the 3 pre-existing errors.
* Live: signed-in Playwright probe, evidence under `.copilot-tracking/evidence/2026-11-24/issue-157-live-20261124T035902Z/`. No Azure change.
* Not run: `rpi-checks.py --all` (coordinator), hosted CI, deployment of the fix.

## Amendments and divergences
None from the plan or critique.

## Per-criterion table
| Criterion | Verdict | Why |
| --- | --- | --- |
| Complete the #440 stabilization checkpoint | Unproven | #440 criteria 7 and 8 need owner approval, a PR and a non-worker reviewer; a bug was fixed locally toward it |
| If accepted, child features are accepted | Unproven as a whole | children closed; remainders need excluded screen-reader, DPO/Legal and real-model work |
| Decision accepted or epic closed (ticked) | Not reopened | ADR 0004 |
| No memory used as evidence (ticked) | Not reopened | #1552; live memory list empty |
| Chat consumption bounded and reported (ticked) | Not reopened | #1547, #1558 |
| Retention enforced for the stated period (sub-evidence for child acceptance) | Proven locally, unproven live | new tests; needs deployment |
