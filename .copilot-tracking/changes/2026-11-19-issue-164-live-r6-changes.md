# Changes, issue 164 live r6, 2026-11-19
Refs #164. Files: docs/reference/research/issue-164-live-20261119T134556Z-2026-11-19.md, docs/reference/README.md, docs/reference/log.md, tracking artifacts. No source change; tier FOCUSED.

| Criterion | Proven or unproven |
| --- | --- |
| Thresholds approved; task registered with reviewer and enable state | Partly proven (registered, disabled, function named); threshold approval and named individual unproven, person decision |
| Results bound to serving model and approved thresholds | Unproven, no actual-model result |
| Competent human exercises | Unproven, needs people |
| Actual-call authority and payload approval | Unproven, no finite authority recorded |

Validation: src/agents test_chat_eval and test_chat_heldout 76 OK; registry read offline; read-only az containerapp show; git diff review. mypy and ruff not applicable (no Python change). Not run: rpi-checks.py --all, browser re-probe.
