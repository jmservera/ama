<!-- markdownlint-disable-file -->

# Review: climate-paired-alt-source-178

| Field | Value |
|---|---|
| Date | 2026-10-22 |
| Review execution | Complete (single pass, read-only apart from this record) |
| Outcome | Residual work |
| Assessed boundary | Plan P01 and P02 plus critique dispositions, research W1-W7, changes record, committed tools, fixtures, report and docs. P03 (gate, push) is outside this boundary and reported separately |
| Plan | .copilot-tracking/plans/2026-10-22/climate-paired-alt-source-178-plan.md |
| Research | .copilot-tracking/research/2026-10-22/climate-paired-alt-source-178-research.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-22/climate-paired-alt-source-178-plan-critique.md |
| Changes | .copilot-tracking/changes/2026-10-22/climate-paired-alt-source-178-changes.md |

## Reconciliation

* Plan markers: P01 and P02 checked with evidence, P03 open and named as outstanding in the changes record. Handoff prose, follow-ups and validation state agree.
* Critique PC-001..PC-005 each map to code or tests: UTC-keyed comparison and shifted-source test (PC-001); 1.0 tolerance with boundary tests (PC-002); licence wording split and `underlying_c3s_reuse_verified: false` (PC-003); percentile rule in the report and hand-computed tests (PC-004); per-series rejection matrix (PC-005).
* Requirements: FR1-FR5 and AC1-AC3 satisfied by direct inspection. AC4 depends on P03.

## Validation

* python3 -m unittest discover -s tools -p 'test_climate_*.py': 33 tests OK (22 new).
* Mutation checks: loosening the RH tolerance, removing the dew-point, hour-step, cross-source and fill-value guards each fail the suite. The adapter file was restored and the suite re-run green.
* Documented reproduction command output is byte-identical to docs/reference/research/climate-paired-bounds-178.json.
* The blocker artifact and Durham report are unchanged by this task (diff empty against the branch state before the task).
* Full gate, receipt and verifier: unavailable at review time, run in P03.

## Findings

| ID | Severity | Finding | Destination |
|---|---|---|---|
| RV-001 | Medium | Licence for the demo is a reading of published terms. Open-Meteo's free tier is non-commercial; whether the demonstrator qualifies, the underlying C3S terms and the NASA POWER licence text are unverified. Documented as pending, correctly not approved | Residual work: owner and legal confirmation |
| RV-002 | Medium | Accuracy is demonstrator level. ERA5 and POWER disagree by about 1.2 degC and 8.3 RH points mean absolute; there is no station comparison; one grid cell and one year | Residual work: authorised MIDAS or other station source, multi-year window |
| RV-003 | Low | Humidity consistency is only checked for Open-Meteo (it supplies dew point). POWER humidity is range- and alignment-checked only | Residual work, acceptable for a cross-check source |
| RV-004 | Low | Retrieval is not performed by the adapter; the committed raw fixtures plus hash are the only provenance. Response headers were not retained | Residual work, accepted for a fixed demonstrator sample |
| RV-005 | Low | Meteostat was not examined, so the comparison is not exhaustive | Residual work, recorded as "not examined" |

No defects and no decision gaps. No finding conflicts with a confirmed owner decision. Issue #178 criteria remain unticked; the licence criterion is explicitly unmet.

## Routing

* RV-001..RV-005: distinct follow-up items for later user-selected work. No return to Implement or a second Review in this task.
