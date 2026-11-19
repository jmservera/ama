# Issue 114 live research, 2026-11-19

Refs #114. Synthetic desktop demo, resource group `ama`. Base `309635e29`.

## Unticked criteria

Only one: "Per-year audit and ledger digest verification proven by test before reliance". The other two are ticked in the issue.

## Findings

* `Store.verify_ledger_before_reliance` in `src/core/src/zava_forward/core/store.py` seals intact past years, verifies per-year chains, anchors and heads, and blocks reliance on any problem.
* Existing tests cover it: `test_recovery`, `test_sqlstore`, `test_ledger_digest_blob`. Re-run today from `src/core`: `PYTHONPATH=src:tests python3 -m unittest test_recovery test_sqlstore test_ledger_digest_blob -q` gave 62 tests, OK, 42.9 s.
* Prior live notes (2026-11-18) record per-year tamper detection on live-shaped data and that the deployed image lacked the method.
* Read-only Azure check today: `ca-cutover-test-demo-api` runs image `zava-forward-api@sha256:5368f4e4...`, revision `--0000033`, Running. Same digest as the 2026-11-18 note, so the image gap is unchanged. Rolling it is a deployment change, outside the owner decisions.

## Disposition

The criterion wording is "proven by test", and the tests prove it. No missing code or test was found, so no source change. Deployed-image proof stays unproven for the demo (needs an image roll and a multi-year database). Research disposition: executed. Planning readiness: Ready (documentation-only).
