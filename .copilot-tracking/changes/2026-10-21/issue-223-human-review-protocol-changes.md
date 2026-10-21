<!-- markdownlint-disable-file -->

# Changes: issue-223-human-review-protocol

Plan: .copilot-tracking/plans/2026-10-21/issue-223-human-review-protocol-plan.md | Date: 2026-10-21 | Base: 993a7b88c03f5240f1e7a4c7c7afa7c064281622 (origin/main verified fresh before commit)

## P01 Protocol section

* Added H3 "Meaningful human-review protocol (#223; proposed, Not run)" to src/agents/README.md under the AI evaluation harness: dependency block (#108 open, #222 unapproved manifest, OQ-017), criterion map (all unmet), E1-E6 plus C0 case classes, decision rules, baseline arms, automation-bias design, retention fields (existing versus gaps; identity retention UNFILLED), OQ-017 evidence, denominators, effort and comparators, outcomes.
* All PC-001 to PC-009 critique findings applied (see plan Critique Disposition).

## P02 Index and log

* docs/reference/README.md: one Inspect row. docs/reference/log.md: one appended query entry; earlier entries untouched.

## P03 Validation

* Added-line non-ASCII scan: none. Anchor exists. Git diff reviewed: 3 files, additions only.
* Focused: `cd src/agents && PYTHONPATH=src:../core/src:../core/tests:tests python3 -m unittest discover -s tests -p test_ai_eval.py` passed 13 tests. (First attempt without source paths failed with ModuleNotFoundError because distributions are not pip installed; no install needed.)
* Complete local gate (tools/rpi-checks.py --all), push, PR NOT performed by this task (coordinator owns); no gate receipt exists.

## Remaining and follow-ups

All #223 criteria unmet and untouched. Open: thresholds/samples/panel approvals, OQ-017 holders, #108, #222 manifest, consent/privacy, costed plan, Finance, identity retention decision.
