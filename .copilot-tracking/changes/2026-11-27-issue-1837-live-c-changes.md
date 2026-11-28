# Issue 1837 changes (run c), 2026-11-27

Refs #1837. Base `337d3999d5`. Synthetic demo, desktop only. Tier: FULL classification (src change in `src/api/checks/`); the coordinator owns the gate, `rpi-checks.py --all` not run. Impact basis: browser-check harness only; no handler, permission, secret, dependency or deployment change.

## Change

* `src/api/checks/nomination_browser_check.py`: the page route handler aborts `/api/assistants*` requests. The registry GET holds a `BEGIN IMMEDIATE` write lock beyond the 5 s busy timeout under load, which made the harness's out-of-band write fail with `database is locked`.

## Divergence

* A first repair (network idle wait) failed three runs and was reverted before commit.
* The `implement-start` witness recorded the source as already dirty: the first edit was issued in the same tool batch as the witness call (the changes record was persisted first).
* Failing-first evidence is a captured lock-holder stack and repeated failures ([record](../../docs/reference/research/issue-1837-live-2026-11-27-c/lock-diagnosis-before.txt)), not a deterministic test; the failure depends on host load.

## Validation

See the [research note](../../docs/reference/research/issue-1837-live-demo-evidence-2026-11-27-c.md): fixed check passed 3 of 3 runs; 68 unit tests OK, zero skips; standalone-form and challenge axe passed; mypy and ruff clean.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Failing-first coverage, three browser submissions, valid challenge target | Proven (earlier record) | [failing run at 9da3fcd](../../docs/reference/research/issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt); route-forms check passes here |
| Valid submissions retain records; JSON callers compatible | Proven locally; live write unproven | route-forms axe run, unit tests; live writes withheld (irreversible shared-demo records) |
| Negative tests: authorization, isolation, malformed, same-origin/CSRF | Proven locally | `tests.test_nomination_api_routes`; [2026-11-20 live no-write probe](../../docs/reference/research/issue-1837-live-2026-11-20/live-negative-probe.json) |
| Browser journeys with axe, zero unexpected skips | Proven locally for forms, challenge and nomination view | this run's axe JSON files; the nomination view check now passes 3 of 3 |
| Dated RPI evidence; independent exact-head review; hosted CI | Partly proven; owner-gated | dated artifacts here; review and CI need publication, not permitted |
| Full tier receipt | Unproven | src change under `src/api/checks/`; verified external receipt is coordinator-owned and not run here |
