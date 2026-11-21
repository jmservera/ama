# Details: issue 2205 (2026-11-21)

* Phase 2: in `src/core/src/zava_forward/core/assistants.py` add `quality_scope(self)` near `quality_scope_denial`; keys `mode` (`demo-homes`, `invalid-refused`, `unrestricted`), `homes` (list), `trigger` (`operator-requested-only` or `any`), `background_scan` (`skips-quality` or `includes-quality`), `per_reading_calls` (always `none`), `model_call_authority_present` (bool).
* Phase 3: tests assert each mode and that no provider call occurred.
* Phase 4: `docs/capstone/demo/runbook.md` preflight line; `src/api/README.md` sentence; `docs/reference/research/issue-2205-live-2026-11-21.md`; `docs/reference/log.md`; index entry.
