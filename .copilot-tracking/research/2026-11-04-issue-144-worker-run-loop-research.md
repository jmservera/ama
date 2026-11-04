# Research: issue 144 worker run loop slice (2026-11-04)

Prior delivery: #682 (load harness, restart audit test, hosting contract tests, status table in infra/README.md). Earlier RPI evidence: 2026-11-01 issue-144-container-hosting research, plan, changes and review.

Acceptance status before this slice:

* Criterion 1 (real worker images through the pipeline): unmet. `dispatch.py` defines ports; the entrypoint only printed a version.
* Criterion 2: defined and compile-tested; no live rollout. Criterion 3: platform-blocked (no Container Apps schema support). Criterion 4: local run only, not declared scale; needs a hosted run. Criterion 5: verified on the SQL store; no Azure restore proof. Tokenomics criterion: met by #682.

Smallest locally testable slice: a cooperative run loop and fail-closed `serve` command for the agents worker. The queue adapter (new Azure dependency, image pin change) and API post-back (fence checks, security-sensitive) are later stacked slices that need the complete gate.

Planning Readiness: Ready. Research disposition: executed.
