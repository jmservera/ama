# Research: validation-only capture for #136 (2026-11-09)

Refs #136, Refs #1258. Slug `ranking-blob-bicep-136-validation-capture`. Research disposition: executed; Planning Readiness: Ready.

## Frozen subject

* Branch `feat/ranking-blob-bicep-136-1109`, HEAD `3de2c2f4c8ad64cf22c579dce05eeec6f4f5245f`, tree `da8ef003240f070587bb4c5f2881455674210483`, clean worktree at start.
* Reviewed source head `95fcaf561a9f046671d2cdf1bac8a6619f703610` (tree `364431a5a1afe063fa4cfb17f7e4e01f8deae8e9`). `3de2c2f4c` adds only `.copilot-tracking` records on top of it.
* Declared parent `52f9b61bb22c5ceaaed0f9bf6a55dab7a7a59cb8` (topic `fix/ranking-archive-ancestor-durability`, #1258), NOT main. No main, #1292 or sibling content is imported by this task.

## Why this task exists

The integration handoff states that its raw temporary logs were removed, including the output of an invalid first API wiring run that imported the primary checkout's distributions (exit 1, 11 failures, 13 errors, wrong distribution). Only concise outcomes survive in `.copilot-tracking/changes/2026-11-09-ranking-blob-bicep-136-c5-integration-changes.md` and the review. Those raw outputs are LOST and are not reconstructed here. The coordinator needs fresh producer evidence (command, identity, stdout/stderr, exit) retained outside the repository.

## Evidence sources read

* Coordinator brief and `demo-rpi-common.md` (demo-targeted tier, no blanket gate, no push, owner-selected scratch rules).
* Integration handoff, state, review and changes records; `.github/workflows/src-ci.yml` (infra job runs `az bicep build` and `lint`, `unittest discover -s infra/tests`, then pinned `ruff==0.17.1` `--isolated` check and format on the changed infra test file).
* Tool identities at start: `ruff 0.17.3` ambient (CI pins 0.17.1; difference is disclosed), azure-cli 2.91.0, Python 3.12.3.

## Constraints and risks

* Ambient editable installs point at the primary checkout `/home/azureuser/source/ama/src/*`, which lacks `ranking_archive_blob`; they are invalid for this evidence. Use an owned venv with editable installs of THIS worktree only after an ambient-independent check fails for a missing dependency, and print the imported Core and API file paths before any unit run.
* Plain repo-config `ruff check` flags RUF100 on the untouched `# noqa: S307` line. It is a pre-existing baseline outside the CI command; it is run and recorded, not suppressed or fixed.
* Productive review-correction count for this child stays 1 of 5. A failing selected check stops publication; no source correction without explicit scoped instruction.

## Not in scope

Full matrix, `rpi-checks`, SQL, browser, scanners, deployment, real Azure, role grants, what-if, push, PR, board.
