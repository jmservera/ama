# Research r4: issue 189 live-state verifier (2026-11-18)

Refs #189. Disposition: executed; prior passes (research, r3) were docs-only and reused as evidence. Planning Readiness: Ready.

Open criterion: "Run has an owner, a time limit and a budget alert", verified live.

Gap: `verify_bicep_run_controls` checks static Bicep only. Nothing in code checks the DEPLOYED hub owner tag and budget notifications, and prior passes found recipients on noreply/invalid domains without any machine check. Owner decision 2026-11-18 requires code and tests, not docs-only evidence.

Plan scope: new module `src/core/src/zava_forward/core/synthetic/run_live_check.py` (pure verifier over `az` JSON plus CLI), tests in `src/core/tests/`, README line, then read-only live run against resource group `ama`.
