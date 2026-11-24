# Changes: issue 2320 briefing without write lock on repeat reads (2026-11-24)

Status: in progress. Disclosure: the source edits and the test were prototyped before the plan was persisted; the plan, critique and this record were written afterwards from that work, and the witness `implement-start` follows them.

## Files

* `src/core/src/zava_forward/core/store.py`: `release_denial`, `_briefing_denial_unchanged`, cache hit rule.
* `src/core/src/zava_forward/core/sqlstore.py`: read-only `release_denial`; `release_block` audits through it.
* `src/api/tests/test_assistant_release.py`: repeat held briefing takes no write lock and appends no audit.
* `docs/reference/research/issue-2320-live-2026-11-24.md` (+ probe folder), `docs/reference/README.md`, `docs/reference/log.md`.

Status: complete. Tier FULL (src changed); the coordinator runs the gate. Validation: 682 tests OK (172 skipped), ruff check clean, mypy 3 pre-existing errors unchanged. Test fails on the base, passes with the fix.

## Per-criterion table

| Criterion | Result |
| --- | --- |
| Profile where briefing spends time and why a GET waits for the write lock | Proven (code and live log); no SQL timing profile |
| Answers within 5 s or named state, never 503 on a quiet system | Unproven: not deployed; live baseline 11 to 14 s under shared load |
| Test proves the read path does not take the write lock | Proven for a repeat GET under a held denial; first GET after a data change must still record |
| Live re-check after deployment | Unproven: deployment reserved to the owner; pre-fix baseline recorded |
