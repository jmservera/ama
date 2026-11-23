# Research: issue 2313 round 2 (Refs #2313)

Research disposition: executed (builds on merged work in 2c06796f5f). Planning Readiness: Ready.

Finding: the what-if workflow (`infra-plan.yml`) and `infra-image-build.yml` are on main. All four criteria remain unticked on GitHub. The one code-satisfiable gap recorded in the prior note is that `tools/rpi-checks.py` does not hash or classify `infra-image-build.yml`, so workflow drift goes unnoticed by the gate. Tests `test_matrix_drift_*` iterate `WORKFLOWS`, so adding the file is covered by existing drift tests; coverage classification for job `build` must be added.
Owner-only: `INFRA_PLAN_ENABLED`, OIDC, environments (#138). Live Azure not required.
