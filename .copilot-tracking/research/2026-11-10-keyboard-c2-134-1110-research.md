<!-- markdownlint-disable-file -->
# Research: keyboard probe correction C2 (2026-11-10)

Disposition: executed (source inspection). Planning Readiness: Ready. Parent: C1 (spent, preserved).

## Evidence

* Independent report `independent-134-keyboard-c1-2036/functional/functional-findings.json`: approve_with_comments, 2 Medium false greens.
* Finding 1: `focus_failures` (probe lines 122-125) accepts any `boxShadow` other than none or transparent black. `rgba(0, 90, 158, 0) 0px 0px 0px 2px` (non-black, alpha 0) and `rgb(0, 90, 158) 0px 0px 0px 0px` (zero extent) pass. All five existing focus negatives force box-shadow none, so the branch is untested.
* Product ring (read-only, `style.css` line 48): `outline: 3px solid ink; box-shadow: 0 0 0 2px #f2a900`, computed as `rgb(242, 169, 0) 0px 0px 0px 2px`.
* Finding 2: after the reset `wait_status` (probe line 302) there is no `assert_status`, so reset-state semantics are unchecked.
* Origin/main moved only to `54eae28f` (rubric `latest.json`); no change to the probe, tests, web files, core register files or README since the merged base `e1497bca`. No merge needed.
* Pins: ruff 0.17.1 and mypy 2.4.0 in own venv `/tmp/z134c1`.
* Witness lesson: C2 `launch` seq 1 was refused (needs `--brief`; my preflight did not model it); retained, seq 2 accepted.

## Decisions

* Constrain the shadow oracle to the known supported computed shape (one comma-free, non-inset `rgb()` or `rgba()` shadow with alpha above 0 and spread of at least 2px); anything else fails. No CSS parser abstraction.
* Add reset-status assertion and negatives. No product, oracle, register, enum or acceptance change; DOM, fixture, proxy, no-table and assistive-technology limits stay explicit.
