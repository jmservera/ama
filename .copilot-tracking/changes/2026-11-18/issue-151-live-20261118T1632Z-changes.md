# Changes: issue 151 live closure (2026-11-18)

Tier FOCUSED, docs and evidence only; no `src` change; `rpi-checks.py --all` not run. Honest note: the research note, index and log edits were drafted before this file existed, so `implement-start` was recorded after them; no source was edited.

## Files

* `docs/reference/research/issue-151-live-r4-role-routes-evidence-2026-11-18.md` (new)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (appended entry)
* `.copilot-tracking/evidence/2026-11-18/issue-151-live-r4/` (scan script, results JSON, redacted raw axe)
* `.copilot-tracking/{research,plans,details,critiques,changes,reviews}/2026-11-18/issue-151-live-20261118T1632Z-*` and state file

## Per-criterion table

| # | Criterion | Result for the demo |
| --- | --- | --- |
| 1 | Target level and scope recorded | proven earlier (ticked); not re-tested |
| 2 | Audit coverage | proven earlier (ticked); rounds 1 to 4 add live evidence |
| 3 | Automated checks in CI | proven earlier (ticked); baseline test 18 OK locally |
| 4 | Manual screen-reader and keyboard checks per role workflow | PARTLY PROVEN: scripted keyboard and axe on Programme Manager (13 screens), seven role screens and resident app; UNPROVEN: screen reader (excluded for demo), repairs and contractor workflows (no accounts; denial screens only), manual rather than scripted keyboard |
| 5 | Accessible equivalents (#119) | proven earlier (ticked); not re-tested |
| 6 | Accessibility statement draft | proven earlier (ticked); not re-tested |

## Validation

* Live Playwright scan, nine routes: 0 axe violations, 0 incomplete, no trap.
* `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests.test_accessibility_baseline -q` in `src/api`: 18 OK.
* Credential literal scan of the evidence folder: no match. No Azure resource created or changed.
* mypy, ruff and src-ci tiers not applicable: no Python source or web file changed.
