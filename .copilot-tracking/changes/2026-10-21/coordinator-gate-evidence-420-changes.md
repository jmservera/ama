<!-- markdownlint-disable-file -->
# Changes: PR420 gate-evidence correction

| Field | Value |
|-------|-------|
| Task slug | coordinator-gate-evidence-420 |
| Date | 2026-10-21 |
| Plan | .copilot-tracking/plans/2026-10-21/coordinator-gate-evidence-420-plan.md |
| Base | f3e8a8f1fc1018e338eb8efb7e4b6e8c123d0762 (PR420 head); origin/main 993a7b88c03f5240f1e7a4c7c7afa7c064281622 |

## P01-T01 validation-01 correction

* Modified `.copilot-tracking/hve-builder/2026-10-20/coordinator-sonnet-55-validation-01.md`: replaced the row "Repo-wide doc lint/build, application gates, network/CI/model calls | n/a | Not run (none exist or required)" with a doc lint/build row and a separate complete-local-gate row stating it was not run in this stage and remains separately mandatory; scoped the Pass verdict to mechanical validation; added a dated correction note quoting the original wording.
* No claim that the gate ran earlier.

## P01-T02 correction record

* Created `.copilot-tracking/hve-builder/2026-10-21/coordinator-sonnet-55-validation-02.md` (draft first, check results appended after P02-T01 ran them).

## P02-T01 validation

* `git diff --check` rc 0; non-tracking diff versus f3e8a8f1 empty; grep confirms the phrase only appears as quoted original; origin/main unchanged at 993a7b88.
* Complete local RPI gate not run; coordinator-owned (launch clarification). No push, PR, cloud or paid call.

## Amendments, divergences, follow-ups

* Critique PC-001 to PC-003 applied directly (see plan Critique Disposition). No divergence. Follow-ups: none.

## Remaining work

* Coordinator: full gate on the frozen head, receipt verification, independent exact-head assessment, publication.

## Amendment: hve-builder activation (after f79be1d4)

* hve-builder was activated in `validate` mode. A Low-profile validation subagent (claude-haiku-4.5, per the Low profile list) ran local nonmutating checks and wrote `.copilot-tracking/hve-builder/2026-10-21/coordinator-sonnet-55-validation-03.md`: mechanical Pass only, all listed checks Passed.
* Appended an HVE lifecycle disclosure to validation-02. No source, plan, critique or original Review artifact changed; no second Review reconstructed.
* Not run: complete local RPI gate (coordinator-owned), HVE behavior execution (Medium skip unchanged), CI lanes, authoritative CLI README fetch.

## P03-T01 gate-failure dependency correction (after 474454d1)

* Complete exact-head gate failed 2026-10-21T03:12:14Z; the failed receipt and logs at /tmp/ama-coordinator-followon-0105-420 are preserved and not edited. api, importer and orchestrator image gates each show only CRITICAL GHSA-6q48-6c7w-9gw2, certifi 2026.7.22, fixed 2026.10.19. Container controls and negative probes passed. Not publication approval.
* Reused only src/core, src/api, src/importer and src/orchestrator requirements.txt from native issue119 commit a3257c71f4963d98a88c501d040b3d07eada4392 (certifi 2026.7.22 to 2026.10.19, two new hashes each). No tracking/map edits cherry-picked; no other worktree touched.
* Focused checks: all four files identical to a3257c71 (git diff --quiet); each lists certifi==2026.10.19 with two sha256 hashes; zero remaining certifi==2026.7.22 under src; pip download --no-deps --require-hashes of the pinned wheel succeeded (index hash match); git diff --check rc 0.
* Not run: full gate, image builds, scanners, tests; Review not repeated, no second original Review. hve-builder was activated only after the original correction (see the earlier amendment); this change adds no HVE behavior claim and the HVE Pass remains mechanical only.
* Residual: reuse is provisional; own complete exact-head gate and independent assessment are still required.
