# Changes: issue 157 live loop (2026-11-19)

Tier: FOCUSED (index row text only; no src, SQL, infrastructure or deployment change; no rpi-checks --all).

Baseline (before edit): `python3 -m unittest tools.test_check_legacy_references` FAILED 1 of 8 (`test_repository_has_no_violations`: `docs/reference/README.md:1355: retired path without archive tag v0.21.0`).

## Files

* docs/reference/README.md (row 1355 names archive tag `v0.21.0`; new index row for the research note)
* docs/reference/log.md (entry)
* docs/reference/research/issue-157-live-criteria-2026-11-19.md (new)
* .copilot-tracking/ artifacts

## Per-criterion table

| Criterion | Proven or unproven | Reason |
| --- | --- | --- |
| Complete the #440 stabilization checkpoint | Unproven | #440 still has two unticked criteria (file triage drafts with owner approval; PR with independent review). Delivered here: the one remaining cut-over gate violation (D2 residual) is fixed. D1, D3, D4 remain open drafts |
| Child features accepted | Unproven | #162 (granted break-glass needs a deployed setting change), #164 (thresholds and task registration need owner approval) open; #159 screen-reader testing waived for the demo, not evidenced |
| Decision accepted (ticked) | Not re-opened | ADR 0004, 2026-10-15 |
| No memory as controlled-decision evidence (ticked) | Not re-opened | PR #1552 |
| Chat consumption bounded (ticked) | Not re-opened | PRs #1547, #1558 |

## Validation

* After the edit: `python3 -m unittest tools.test_check_legacy_references` OK (8 tests); `python3 tools/check-legacy-references.py` 0 violations, 0 link violations.
* mypy, ruff and src tests: not applicable (no Python or src file changed). No rpi-checks --all.
* Order note: an initial README edit preceded the changes file and was reverted with `git checkout`, then reapplied after `implement-start`. The first two `plan-done` calls were refused because the critique file and state artifact paths were not yet recorded; the third succeeded.
