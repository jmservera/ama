<!-- markdownlint-disable-file -->

# Task Research: fictional-form-review-97-b6-rubric

| Field | Value |
| --- | --- |
| Date | 2026-10-23 |
| Researcher | rpi-research skill, session 8fe80adc-6a17-41ed-8337-e921375d1cc6, additional owner-authorized cycle 1 of at most 4 (stop early on PASS; ask before a fifth) |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-23/fictional-form-review-97-b6-rubric-research.md |
| Parent | 97 history preserved: recovery Review (Residual work), FIN-001 correction and Review (Conformant), gates for b22d8639 and c8266cb8 and a74652aa (all historical) |

## Brief

* Finding B6 (independent reviewer 8c4ae0f9, Medium, high confidence): .github/rubric/scores/latest.json B6 rationale describes the new core README section (src/core/README.md 928-943) but its evidence cites docs/capstone/pitch/tokenomics-pitch-brief.md:1-137 and src/api/README.md:2555-2561. Total 55 unchanged.
* Scope: engineering proposal correction only. Posture: focused. Non-goals: no manual edit of the generated score, no spoofed evidence or approval, no runtime validation weakening, no gate, push, PR update or merge, no Azure or paid scoring.
* Admission: HEAD and PR424 head a74652aa, clean tracked/untracked/ignored; fresh origin/main f1e2d830f17558efd868919de1973ea7244a8841; no unique remote commits beyond HEAD; PR 424 open draft, mergeable. PR 442 (resident proposal, separate session) not read or touched.

## Evidence

| ID | Finding | Location |
| --- | --- | --- |
| C1 | Current B6 evidence is the pitch brief and src/api/README.md:2555-2561, while the rationale cites src/core/README.md:928-943. The defect is confirmed in the committed bytes. | .github/rubric/scores/latest.json (B6 block) |
| C2 | The previous bot commit b22d8639 had B6 evidence core README 928-937 and the focused test; the later bot commit a74652aa replaced it with the pitch-brief and API citations while changing the rationale to the core README wording. The mismatch was introduced by the second automatic rescore, not by issue edits. | git show a74652aa -- .github/rubric/scores/latest.json |
| C3 | latest.json is written only by the rubric-score workflow: a Copilot-engine agent (claude-sonnet-5, max 300 AI credits) proposes scores, gate.py filters them, and a record step commits as github-actions[bot] and pushes to the PR branch. It runs on pull_request synchronize and is not run locally. | .github/workflows/rubric-score.md |
| C4 | gate.py keeps the previous criterion if a score change cites no changed file; for unchanged scores it accepts the model's proposed evidence without checking it against the rationale. No deterministic check relates rationale text to evidence. | .github/rubric/scripts/gate.py:180-196 |
| C5 | No script, schema or documented procedure supports hand-correcting a score. A manual edit would counterfeit generated bot output. | repository search, C3 |
| C6 | Rebase onto f1e2d830 is conflict free: main added only max_file_bytes to .github/rubric/artifacts.json and did not change latest.json since 140d8f49. The rebased branch keeps both bot commits and all issue commits; the log diff against main is one ms.date line and appended entries. | git diff origin/main, rebase result c158ab1e |
| C7 | Local rubric script tests under .github/rubric/scripts (pytest) show 21 failed, 324 passed and 7 skipped on this branch (command: python3 -m pytest -p no:cacheprovider .github/rubric/scripts -q, re-run after critique; an earlier narrower run of test_gate.py and test_prepare.py gave 9 failed, 81 passed). The scripts have no diff from main, so the failures are not caused by issue edits; cause not investigated (out of scope). tools/rpi-checks.py contains no reference to rubric, so the complete gate is not known to run these tests; this was checked by text search only. | pytest run 2026-10-23 |

## Waves (one complete cycle, inline)

* Wider: repository search for the generation, gating and recording path and for any manual-correction route.
* Deeper: read the workflow record step, gate.py evidence handling and both bot diffs.
* Contrarian: alternatives (a) hand edit B6 evidence: rejected, forges generated output (C5); (b) drop the two bot commits so main's canonical score is restored and let the workflow regenerate: possible but rewrites published history and needs a coordinator-approved force-with-lease, so only offered; (c) add or alter issue text to coax a better score: speculative, non-deterministic, risks the unapproved-proposal boundary; rejected; (d) leave as is and rescore on the next push: supported path.

## Synthesis

* Recommendation: no deterministic repository fix exists. Rebase only. The supported correction is a fresh automatic rubric rescore on the next published head, which regenerates latest.json; this needs the paid workflow and a push, both outside this run. Record B6 as an unresolved generated-output blocker routed to the coordinator, with option (b) as a coordinator decision.
* Research disposition: executed. Planning Readiness: Ready (to a no-hand-edit, rebase-and-record plan).
* Unresolved human items: Finance FD-01..FD-14, template authority, binding, OQ-015 (criterion 1 unmet; criterion 2 delivered by PR 377).
