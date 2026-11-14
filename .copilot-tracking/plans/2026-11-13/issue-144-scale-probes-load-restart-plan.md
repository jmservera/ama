# Plan: Issue #144 scale, probes, load and restart (local slices)

* Task: `issue-144-scale-probes-load-2315`; research: [research](../../research/2026-11-13/issue-144-scale-probes-load-restart-research.md); details: [details](../../details/2026-11-13/issue-144-scale-probes-load-restart-details.md).
* Validation tier: focused (owner decision D4, issue #1294). Basis: new tests, a benchmark record and documentation only; no workflow, Dockerfile, dependency, permission, secret, deployment or Bicep change. Doubt does not apply.
* Critique: one final-candidate critique, recorded in the review artifact.

## Phases

* [x] Phase 1: infra source-contract test `infra/tests/test_container_hosting_completeness.py` (limits, bounded scale, probes, single revision, rollback prose, fixture declaration).
* [x] Phase 2: separate-process load and SIGKILL restart test and benchmark `src/api/tests/test_scale_fixture_load_and_restart.py`.
* [x] Phase 3: run the benchmark at 60,000 homes and record `docs/architecture/scale-restart-2026-11-13.json`.
* [x] Phase 4: update `infra/README.md` hosting table and `src/api/README.md`; append `docs/reference/log.md` entry.
* [x] Phase 5: focused validation and review.

## Non-goals

No edit to the four frozen Bicep files. No criterion ticked. No hosted, Azure, autoscaling or production-scale claim.
