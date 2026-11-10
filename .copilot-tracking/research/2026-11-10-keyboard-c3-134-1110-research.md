<!-- markdownlint-disable-file -->
# Research: keyboard probe docs/process correction C3 (2026-11-10)

Disposition: executed (source and evidence inspection, read-only). Planning Readiness: Ready. Parent: C2 (spent, preserved).

## Evidence

* Root admission (2026-11-10T17:12Z): independent C2 exact-head functional review APPROVE, 0 findings; no further source correction. C3 is docs/process only.
* `src/api/README.md` lines 4128-4148 describe the keyboard probe in present tense and say nothing of what was observed, on which head, or that its witness chain is qualified. That is the publication-documentation deficiency.
* Frozen head `cb01c33c42ceef31ee699649ecceedadc487945d`, tree `f0a40f93ae112ebbdb5f58d56c7081239ad22921`. Blobs at the head: probe `e8b7d9f1...`, probe test `228a5390...`, `journey_acceptance.py` `e3466b6e...`, `perspective_walkthroughs.py` `f1828b2e...` (full ids in the handoff). Re-proved after the commit.
* origin/main is `54eae28f8bc2b3c5e3786ab5169b0ed375f826ef`; it differs from merged base `e1497bca` only in `.github/rubric/scores/latest.json`. No merge or rebase.
* C2 observations (cb01 pinned checks, not rerun in C3): ruff 0.17.1 and mypy 2.4.0 clean on four files; helper tests 6 OK; core tests 16 OK; one browser run exit 0, 714 PASS, 15 negatives, 15 declared no-table walks. Logs: `ROOT/134-keyboard-c2-evidence-1110/`.
* C2 witness chain `ROOT/phase134-keyboard-c2-evidence-1110` has 8 records, verify exit 1 QUALIFIED: seq 1 launch refused (missing `--brief`); seq 4 plan-done refused (wrong cwd, preflight exit hidden by `| tee`); seq 5 to 8 carry "missing observed predecessor: plan-done". Original chain `phase134-walkthrough-plan-evidence-1110` (8 records) and C1 chain `phase134-keyboard-c1-evidence-1110` (9 records) are also QUALIFIED, exit 1. All stay untouched.
* Reference only: the #440 C2 handoff and preflight log show an all-ok chain; their wrappers bind another worktree and are not reused. This chain uses its own absolute-path checked wrapper.

## Gaps retained

Fixture roles are not authentication; DOM status is not assistive-technology output; endpoint and handoff wording is text presence only; five screens declare no table; Asset, Procurement and Auditor have no login role; whole #134, AC-034 to AC-043, human and AT acceptance are unmet; #1401 and #1402 untouched.
