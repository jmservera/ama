# Research: quality sensor risk explanation (Refs #111)

* Issue #111: derive reproducible versioned signals; missing or stale data is INSUFFICIENT and never lowers priority (FR-050, AC-067, AC-068). Thresholds are exercise values; R1 to R3 not complete.
* Code search of `src/agents/src/zava_forward/agents/` found no existing Quality damp/mould inspection prioritization; `alert_triage.py` is the closest style precedent (pure, dict-in, no invented evidence).
* Disposition: executed. Planning Readiness: Ready.
* Constraint: avoid `chat_eval.py` (PR #1643). Parent `f907cd2c7` (PR #1641).
* Environment note: the editable install resolves to another checkout, so the worktree needs `PYTHONPATH=src` for validation.
