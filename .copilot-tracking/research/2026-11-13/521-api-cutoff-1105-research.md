# Research: #521 API cutoff test proof (2026-11-13)

Task: `521-api-cutoff-1105`. Base `3b05143179f83235c5b4e80e70aad99bdc44d83f`. Disposition: executed (bounded, tracking-only).
Read first: case study original/addendum, `docs/reference/README.md`, `memory.md` (context only).

## Findings

* `src/core/.../resident_showcase.py:42` defines `AUTHORITY_END` (target `2028-01-01T00:00:00Z`, exclusive).
* `test_resident_demo_check.py:83-107`: fixture SQL window end `== datetime(2028,1,1)`, `!= 2027-02-01`, `!= 2026-11-01`, start `< ` end, end equals `rs.AUTHORITY_END`.
* `test_resident_demo_api.py:414-436`: identity valid_to=AUTHORITY_END; 2027-01-31T23:59:59Z still allowed; at `AUTHORITY_END.timestamp()` token verify is None and view/login return 503. Test name still says "february boundary" (stale name, no edit in scope).
* `test_resident_demo_api.py:827`: refusal test uses `2026-11-01` as an expired/mixed-settings value.
* Gap: no explicit +1s/+1ms assertions in these two files; the exact-boundary check plus 2027-01-31 allowed cover old-cutoff-no-longer-applies / new-cutoff-applies. Reported as observation, not fixed (no src/tests edits permitted).

## Planning Readiness

Ready. Only remaining work: run the two modules in a `--system-site-packages` venv with in-worktree editable installs.
