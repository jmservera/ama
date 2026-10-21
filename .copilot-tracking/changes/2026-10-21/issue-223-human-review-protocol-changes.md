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

## Corrective change C01 (after failed complete gate; does not alter original evidence)

* Trigger: gate failure 2026-10-21T04:08:41Z at head 78bdb8ac9e30f8ec09e13bd6b38e5c63c32f64dd, sole finding CRITICAL GHSA-6q48-6c7w-9gw2 certifi 2026.7.22 (fixed 2026.10.19). Receipt /tmp/ama-review-protocol-followon-0210-223/receipt.json and adverse logs preserved untouched.
* Change: four requirements.txt files taken verbatim from a3257c71f4963d98a88c501d040b3d07eada4392 (12 lines changed: certifi pin and its two hashes each). Provisional shared reuse.
* Focused checks (no gate, no builds): per-file diff versus a3257c71 empty; only certifi/hash lines differ from prior head; all four show certifi==2026.10.19 with 2 hashes and no 2026.7.22; the two hashes verified by `pip download --no-deps --require-hashes` of certifi 2026.10.19 into a temporary directory (removed). 
* Not done: complete gate, independent assessment, push, PR. No second original Review; protocol text unchanged; all #223 criteria unmet; #108, OQ-017, consent/privacy/accessibility remain dependencies.
