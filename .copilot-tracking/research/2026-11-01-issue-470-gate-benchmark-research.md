# Issue 470 remaining criteria research (2026-11-01)

* Task slug: issue-470-gate-benchmark; research disposition: executed; Planning Readiness: Ready.
* Sources: issue 470 body and comments; merged PRs 475, 584, 669, 613.

## Findings

* Criteria 1, 2, 3 and 5 are ticked and delivered by merged PR 475 (`tools/rpi-checks.py` has `--changed`, `--jobs`, `--resume`, receipt `scope` and `--required-scope`; tests exist).
* Criterion 4 (measured full-run time before and after, recorded in a PR) is unmet. PR 475 measured only the changed tier (60.9 s) against the historical 23 to 26 minute serial full run. The parallel full gate was never measured. The owner comment says the owner decides whether to authorise the benchmark run. The closure audit of 2026-10-31 confirms a partial-tier time cannot satisfy it.
* The benchmark needs two comparable full gate runs (serial `--jobs 1` and parallel `--jobs N`) with Docker, SQL and Trivy prerequisites, about 25 to 50 minutes of command time on 4 vCPU. The task brief excludes the heavy local gate.

## Conclusion

No acceptance criterion is deliverable without the owner-authorised benchmark. No source change is justified. Inventing or estimating timings would violate the evidence rules.
