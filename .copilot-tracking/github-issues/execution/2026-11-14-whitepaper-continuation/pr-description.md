<!-- markdownlint-disable-file -->
# docs(whitepaper): integrate S1 study results, falsifiable predictions, and v19 supplement

Integrate the completed 315-trajectory five-arm S1 empirical study, workflow replay, blinded `gpt-6-luna` Assessment v3 judging, human calibration spot-check, original-source verification, and hypothesis-falsifiability critique into the unified 66-page whitepaper and additive Supplement (`docs/capstone/thought-leadership/everything-but-the-software/main.pdf`, draft v19).

## Changes

* **Empirical results and companion uncertainty (v15–v17)**: Integrated the 313/315 completed trajectories (5,341 measured steps across 5,357 attempts and 14 source commits), 630-endpoint workflow replay, 1,252-call blinded `gpt-6-luna` Assessment v3 ratings, 90-row human calibration spot-check, owner-attested intervention coverage (`intervention-coverage/v1`), and companion complete-pair bootstrap intervals (`B-D` $+1.19$ pp, 95% CI $[+0.10, +2.22]$; `B-A` $+1.41$ pp, $[+0.33, +2.45]$) while preserving `primary_estimates_available = false` for the two transport-quarantined C/E trajectories and 54 incomplete-billing holds.
* **Source verification and provenance finalization (v18)**: Recorded original-source checks and access boundaries (including Laban v1's 39% vs 35% figure-caption difference and institutional-abstract support for Besker), active participant-anonymity review, retained VM timing and version metadata bindings across all 5,357 attempts, owner-reported manager approval and 27 October 2026 CELA submission status, and selection of `jmservera/ama-thought-mve` as the study deposit.
* **Falsifiable predictions and longer-horizon follow-up design (v19)**: Replaced the elastic conjecture phrasing with three explicit testable predictions and a structural manipulation check (`tab:predictionverdicts`: P1 short-horizon decay not supported; P2 primary coverage gain below the $\Delta_* = 10$ pp threshold; P3 CR1 adaptability and short-horizon credit payback not supported; structural treatment fidelity supported), surfaced the per-model coverage split in the Abstract, Section 7.9, and Conclusion (GPT 6.1 Sol $+3.15$ pp $[0.00, +6.30]$ from F9 ranking acquisition vs Sonnet $+0.26$ pp and Gemini $+0.15$ pp intervals spanning zero), and added Section 8.5 (`sec:futureexperiment`) specifying a 30-to-40-cycle brownfield factorial follow-up experiment.
* **Authoring suite and delivery bindings**: Extended `anc/test_measurement_provenance.py` to 67 tests, preserved all 1,378 prior table fields, and bound the 66-page Tectonic PDF (`6b00bc227ccd56b89c352d1cea57871a85fd55aa6bf000eb75385b0a64a45977`, Supplement starting on page 47) under `falsifiability_revision` in `anc/supplement-integration.json`.

## Validation

* `git diff --check`: Passed (zero whitespace or conflict issues).
* `.venv/bin/python -B docs/capstone/thought-leadership/everything-but-the-software/anc/check_paper.py`: Passed (`ABSTRACT_SOURCE_CHARACTERS 1811 < 1920`, 94 cited/embedded bibliography entries, 105 reusable BibTeX entries, zero unresolved labels or environments).
* `.venv/bin/python -B -m unittest discover -s docs/capstone/thought-leadership/everything-but-the-software/anc -p 'test_*.py' -q`: Passed (67 tests in 17.5s).
* `tectonic -X compile docs/capstone/thought-leadership/everything-but-the-software/main.tex --untrusted`: Passed (66 pages, Supplement page 47, zero errors, zero overfull boxes, all pages nonblank and visually inspected; inherited `inputenc` warning disclosed).
* Hosted CI and independent exact-head review: Pending after pull request creation.

## Follow-up

* Two transport-quarantined trajectories (`pilot-estimation-gemini-4-argon-E-15` at 10/21 steps and `pilot-estimation-gpt-6.1-sol-C-20` at 18/21 steps) remain partial in `jmservera/ama-thought-mve`; the non-destructive 14-step recovery and 8-call judging procedure plus the remaining 11 `TODO(author)` closures are documented in `docs/capstone/thought-leadership/everything-but-the-software/anc/revision-report.md`.
