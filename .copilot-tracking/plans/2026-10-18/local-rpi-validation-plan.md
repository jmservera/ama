# RPI Plan: Local-first validation and Actions budget

## Task Metadata

* Task ID: actions-budget-local-rpi
* Task slug: local-rpi-validation
* Planning status: Accepted plan reconciled; P01-P03 executed, original Review Not accepted (RV-001)
* Plan date: 2026-10-18
* Base: 612cbed78a35a4ab426571aa7d2aeb0ae6d691dd
* Phase details: .copilot-tracking/details/2026-10-18/local-rpi-validation-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-18/local-rpi-validation-plan-critique.md

## Executive Summary

Implement one fail-closed local RPI gate, then retire duplicate hosted
validation only after its unique checks have a retained home. The recommended
steady state is complete local pre-push validation plus one consolidated
Source projects CI run per eligible PR update, with no routine main-push
repeat. Retaining the current pull_request trigger does not mean one run total
per PR: every matching push or rebase can trigger it. No workflow or repository
setting was changed during planning. The owner has now approved implementation
and will disable the two MVP workflows. Other issue pushes and merges remain
paused until equivalent local coverage is actually restored.

### What You May Not Know

The API unit suite runs in three workflows; all three also run after merging
to main. MVP CI additionally owns the SQL Server suite and SPDX generation,
which Source projects CI does not replace. MVP validation uniquely runs the
branding migration regressions and compileall. The main protection and ruleset
APIs returned HTTP 403, so required-check configuration is unverified. Local
evidence is less independent than a hosted check and cannot establish GitHub
approval enforcement, OIDC, Azure what-if, deployment or live acceptance.

For PR #412's final revision the 12 job timestamps total 35 minutes 33 seconds
of execution: MVP CI 11:04, MVP validation 5:46 and Source projects CI 18:43.
These are observed job durations, not a billing statement or a forecast.
The two MVP workflows account for 16:50 of that sample, but part of their
coverage must move into the retained workflow. Main-push runs repeat the
three workflows after merge. An additional what-if path-detection job took
nine seconds despite no infra change; the actual Azure what-if was skipped.
Actual account remaining minutes, charged totals and storage use were not read.

### Approved Implementation and Remaining Boundaries

Recommend consolidating to one hosted validator per eligible PR update, not
disabling everything or promising one run total per PR. The owner approved
implementation on 2026-10-18 and stated that they will disable MVP validation
and MVP CI immediately. Implement local coverage and consolidation first;
do not rely on either disabled workflow for the transition PR.
Emergency local-only mode is a separate owner-approved, temporary policy that
suspends automated merges until the coordinator gate is deliberately updated;
it must not pretend missing hosted contexts are green. Changing protection,
switching to local-only acceptance remain unapproved. The owner, not the
implementation loop, manages the immediate workflow disable actions.

## User Decisions and Requirements

* The owner is running out of GitHub Actions budget.
* Identify workflows that can safely be disabled.
* Run all checks inside each RPI loop locally before pushing the PR.
* On 2026-10-18 the owner directed: "Go ahead and implement this first, I will
  disable MVP validation and CI right away."
* Prioritize this work before resuming other backlog pushes; preserve the
  paused #137 worktree and original execution evidence.
* Do not change branch protection, deploy, disable other workflows or claim
  unavailable required checks passed.

## Goals

* Reduce hosted execution without silently removing unique coverage.
* Make local validation a fail-closed, source-bound prerequisite for pushing.

## Scope and Non-Goals

* In scope: local runner, focused runner tests, coordinator/repository guidance,
  preserved unique checks in consolidated source CI, legacy dispatch-only
  transition, approved main-push duplication removal, and current RPI evidence.
* Out of scope: remote workflow settings, protection, application-domain code,
  subscriptions, deployments, managed-agent settings or artifact deletion.

## Functional Requirements

* Preserve every unique automated check in the current validation workflows.
* Include real local SQL Server, browser checks and image scans, not mocks in
  place of these integration gates.
* Separate locally reproducible checks from authenticated GitHub/Azure controls.
* Bind receipts to the exact source, base, tool versions and image digests.

## Non-Functional Requirements

* Python 3.12 and pip only; no private data or inherited real AI credentials.
* Isolate resources per worktree and bound VM memory use.
* No skipped or missing applicable gate is reported as passed.

## Acceptance Criteria

* A single local command executes all five isolated Python suites/static
  checks, namespace/data/JS/infra/migration/browser gates, real owned SQL,
  four image contracts, separate logo stress, Trivy and SPDX.
* Exact-commit clean-checkout receipts reject failures, missing checks,
  contamination, tampering and changed source/base/tool/image inputs.
* Heavy work is globally serialized with bounded owned resources, scrubbed
  environments and no configured private datasets.
* Coordinator and repository guidance require verification before every push,
  including corrections/rebases, preserving full RPI and independent review.
* Source CI preserves unique legacy coverage and eligible PR cadence, removes
  duplicate main-push triggers, and retains dispatch-only rollback without
  protection/deployment changes. Unknown remote controls remain a merge gate.
* The original critique and parent PC-001/PC-002 dispositions are preserved.
* The implemented runner's focused tests and actual full local matrix pass on
  a clean candidate, and its exact-head receipt verifies before any push.
* Independent review and the retained hosted checks pass before merge.

## Workflow Disposition

| Workflow | Recommendation | Condition and consequence |
| --- | --- | --- |
| Proper Warm PoC validation | Disable obsolete entry | The workflow file is absent from current main; last listed runs are 2026-10-07. No current src coverage depends on that retired PoC. Verify it is not an owner-retained historical dispatch before changing state. Little current-run saving. |
| Capstone Rubric Scorer | Leave disabled | Already disabled_manually. Preserve rubric source/lock and deterministic tests; final portfolio assessment remains a distinct obligation, not a synthetic local success. |
| MVP validation | Retire after migration | Mostly duplicates Source projects CI. Move compileall and branding migration regressions plus its tracked-data guard union into the retained validator first. Keep its file available as dispatch-only during rollback. |
| MVP CI | Retire after migration | Move exact real SQL Server selectors, SPDX generation and unreadable-logo build scenario first. Do not lose the SQL gate or SBOM to save minutes. |
| Source projects CI | Keep as consolidated validator | Full local matrix before push; retain pull_request events, one consolidated run per eligible update, not per PR lifetime. Remove ordinary main-push repetition only with approved gate change and preserve manual dispatch. |
| Infrastructure PR what-if | Keep privileged boundary, reduce dispatches | Source CI workflow_run linkage is intentional. Filter the existing changes job to relevant successful same-repository PRs; local validation cannot prove authenticated what-if. Existing what-if jobs already use private self-hosted runners. |
| Source image release and deployment | Keep manual | Already workflow_dispatch-only; no ordinary PR-trigger cost. Its four build jobs use hosted runners, later jobs use private self-hosted runners. Do not dispatch during development or move its approvals onto the VM. |
| Copilot code review | Optional turn off auto-review | Can use the existing independent CLI reviewer instead, if owner accepts removal of hosted review. Official docs say private-repository Copilot code review also consumes Actions minutes plus AI credits. Do not turn off independently of review-policy approval. |
| Claude and Copilot cloud agent | Leave unused/manual, inspect before disabling | Managed dynamic workflows, not tracked YAML. Local CLI sessions do not require cloud assignment. Their exact triggers, usage and billing were not inspected; no claim of automatic savings. |
| Dependabot Updates and Dependency Graph | Keep | Preserve dependency maintenance. Managed workflows are not duplicate src test suites; billing contribution not measured. |

## Local Coverage Contract

The default pre-push mode is `all`, even for documentation-only PRs, to match
the owner's request. Targeted tests during implementation remain useful but
never replace this final gate. Optimized scope selection is a follow-up, not
permission to omit checks now.

| Local group | Required coverage | Existing owner |
| --- | --- | --- |
| Packages | Five isolated development environments; all five unittest suites, dependency rules, Ruff lint/format and mypy | src-ci.yml project matrix and each pyproject.toml |
| Namespace/data | Five side-by-side editable installs, PEP 420 import paths and four module versions plus API version; all tracked-data and test-sandbox guards | src-ci namespace/no-working-data, mvp-ci test and mvp-validation |
| Compile/JS | compileall for four existing source trees; app.js and assistants.js Node syntax | MVP workflows |
| Infrastructure | All Bicep build/lint, REQUIRE_AZ_BICEP=1 full infra suite, exact isolated Ruff and mypy groups, actionlint for active tracked native workflows | src-ci namespace, infra README |
| Browser | Strict standalone harness lint/format, Chromium design-system and regulatory UX checks, pinned verified axe 4.10.3 | src-ci api, stronger no-silent-axe-gap pre-push rule |
| Database | Real disposable local SQL Server 2022 with the exact complete selector list and no missing required SQL test | mvp-ci mssql |
| Containers | All four images, src build context, UID/GID/data/namespace checks, positive and negative hardened/plain startup contracts, separate unreadable-logo API build scenario | src-ci image, src/check-container.py, mvp-ci image |
| Supply chain | Trivy v0.76.0 fixable HIGH/CRITICAL gate, unfixed-inclusive report and SPDX; no ignore file or baseline | src-ci/mvp-ci image, src/trivy.yaml |
| Migration | Existing branding migration suite and pinned authoring dependencies | mvp-validation |
| Issue behavior | Additional explicitly planned runtime/browser/SQL/AI-fixture commands from the issue's RPI plan, with separate result entries | Per-issue plan and changes record |

## Receipt and Push Contract

1. Complete implementation and original RPI Review, reconcile artifacts and
   commit the candidate locally. Uncommitted work is never pushed.
2. Reject tracked modifications and untracked candidate inputs, then run
   `python3 tools/rpi-checks.py --all --base <reviewed-main-sha>
   --out <private-session-directory>` from a fresh runner-owned detached
   worktree of that exact HEAD. Install editable distributions from that clean
   snapshot, not from the original issue directory. Never copy untracked or
   ignored inputs from the original checkout. This is a proposed interface,
   not an existing command.
3. Emit an atomic result manifest only after recording every gate. Include
   HEAD, full tracked-tree SHA, base/merge-base, matrix/helper hashes, command
   argv/cwd, tool versions, times, exit codes, test/skip counts and reasons,
   Docker digests, vulnerability database freshness and receipt/log hashes.
   Sanitize secrets; do not hash or include private datasets.
4. Keep the final receipt outside the checkout to avoid self-referential
   evidence commits. Any committed copy is historical evidence, not the final
   exact-head receipt. If an artifact is committed after checking, rerun the
   gate for the new HEAD. Log-only output outside the repository changes no
   candidate content.
5. A proposed `--verify-receipt` operation rejects tracked modifications and
   untracked source/test/configuration inputs in both the candidate and
   validation worktrees, and rechecks exact HEAD/tree/base and matrix version
   just before push. No candidate input is excluded merely because ignored.
   Outputs, environments and caches stay outside both worktrees; no preexisting
   ignored candidate input is admitted to the clean validation snapshot.
   Coordinator push
   orchestration is authoritative; an opt-in local pre-push hook may call it,
   but hooks are bypassable and not an independent security boundary.
6. A failure, timeout, missing prerequisite, unexpected skip, receipt mismatch,
   base movement or unavailable required gate blocks push. Current existing
   expected opt-in skips during general discovery are enumerated, not treated
   as proof of their integration gate; the explicit SQL group must execute
   the required SQL tests. Axe unavailability blocks a complete browser claim.
7. Corrections, commits, rebases and changes to relevant tool/DB/image identity
   invalidate receipts. Fetch main immediately before push and review. If main
   moved, reconcile it in the issue's authorized RPI loop, then rerun. Never
   silently rewrite a branch or waive a gate.
8. Independent review assesses the final head and actual complete execution
   evidence. Push once when both evidence and review permit it, then open/update
   the PR. Do not fabricate commit statuses, add skip-ci trailers or mark
   missing contexts successful. The final GitHub merge gate remains separate.

## Implementation Ownership and Test Budget

* Canonical implementation: tools/rpi-checks.py; its command matrix is in that
  file, not a new parallel configuration service.
* New orchestration tests: tools/test_rpi_checks.py, at most 12 test methods.
* Existing infra workflow tests may be updated in at most two existing files
  to preserve their behavioral coverage when commands move.
* Existing domain, SQL, browser, container and migration tests stay in place.
  Exact test removals: none.
* Generated targets: private manifest/log/scan/SPDX output only; do not edit
  rubric-score.lock.yml or generate a new workflow framework.
* Test cases own orchestration: nonzero failure; missing binary/dependency;
  timeout; unexpected skip; receipt identity change; base movement; dirty
  tracked tree or untracked source/test/config input; unique resources/SQL
  endpoint ownership; interruption cleanup;
  tampered receipt; matrix coverage drift; axe/scan database unavailable.
  Parameterize these where useful without adding duplicate domain tests.
* Fake-process unit tests cannot prove command parity. Run one complete actual
  matrix on the VM, then run the final updated source again after any
  executable change that invalidates its receipt.
* Planning ran no suites. Implementation now requires the actual matrix;
  historical planning rationale is retained in the original critique and
  changes record, not treated as execution evidence.

## Sources

* .github/workflows/src-ci.yml
* .github/workflows/mvp-ci.yml
* .github/workflows/mvp-validation.yml
* .github/workflows/infra-plan.yml
* .github/workflows/src-deploy.yml
* .github/workflows/rubric-score.md
* .github/agents/ama-backlog-delivery-coordinator.agent.md
* .github/copilot-instructions.md and src/README.md
* src/check-container.py and src/trivy.yaml
* Live workflow inventory and PR #412 job timestamps, read 2026-10-18
* GitHub Actions billing documentation, retrieved 2026-10-18:
  https://docs.github.com/en/billing/concepts/product-billing/github-actions
* GitHub skip semantics, retrieved 2026-10-18:
  https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement a complete local validation gate

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Establish exact workflow-to-local coverage

* Reuse the inventory above; compare every workflow step with the local matrix
  and make any intentional runtime-only omission explicit.
* Freeze versions and existing allowlists, not new dependency policy.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Implement the runner and focused failure tests

* Execute every group in the phase details with structured logs, explicit
  skip classification and signal-safe owned-resource cleanup.
* Preflight tools; install pinned missing dependencies only after a real
  missing-tool/package result. Use pip, never uv.
* Execute heavy groups serially under a host-wide resource lock; do not run
  three full SQL/image/browser gates concurrently on the 16 GB VM.

<!-- rpi:phase id=P02 -->
### [x] P02: Integrate local evidence into RPI delivery

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Make pushing conditional on exact-source local receipts

* Amend the coordinator's outdated mvp unit-suite instruction to the canonical
  five src projects and add verify-before-push, corrections and rebase rules.
* Keep RPI research/plan/critique/implementation/original Review and independent
  assessment. Do not use local validation to bypass human blockers.
* Update existing src/README.md and relevant repository guidance to one runner
  invocation. KB index/log updates are required only if a KB file changes.

<!-- rpi:phase id=P03 -->
### [x] P03: Consolidate hosted validation without coverage loss

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Verify protection and move unique hosted checks

* Record unavailable required-context configuration without blocking independent
  local implementation. The coordinator/owner verifies mapping before merge;
  never change protection or fabricate missing contexts through this plan.
* Add SQL, SPDX/logo, compileall and migration checks to Source projects CI,
  retaining current check names until an explicit approved context transition.
* Update existing workflow contract tests to assert coverage survives relocation.
* Validate the consolidation locally before its first single hosted run.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Apply owner-approved trigger and disable changes

* Proposed normal policy: retain pull_request event behavior, one consolidated
  workflow run per eligible PR update; workflow_dispatch for recovery, no
  push-to-main repeat. Prefer one complete final push, but any subsequent
  matching correction/rebase also starts a new run. Do not add a draft-only condition that itself starts
  many runners or a skip token that leaves required contexts pending.
* Commit RPI changes/artifacts together and avoid an immediate second
  artifact-only push: PR filters use the cumulative diff and can rerun all jobs.
* Keep legacy workflow files dispatch-only for one transition PR. The owner
  already disabled both on 2026-10-18; perform no remote workflow-state change.
  Preserve exact rollback instructions and require coordinator confirmation
  before publication/merge.
* Privileged infra-plan still consumes successful Source CI workflow_run;
  do not disconnect it accidentally. No local OIDC/approval fabrication.
* Record exact prior trigger/settings state for rollback. Re-enable workflows
  and restore triggers if parity or enforcement regresses, without modifying
  existing protection or rewriting history.
* Model cost as U times the consolidated per-update matrix, where U is eligible
  PR updates. Current cost is U times all three matrices plus their main-push
  repeats after merge. The new consolidated run gains the migrated unique
  checks, so the observed 16:50 legacy duration is not a guaranteed saving.
  A true final-only/manual trigger is an unapproved alternative requiring
  owner selection and explicit required-context/infra-plan implications.

## Dependencies

* The owner approves the hosted-policy transition and verifies any required
  contexts that cannot be inspected with current API access.
* Python 3.12.3, Node 24.21.0, Docker 29.9.0 and Bicep 0.48.1 are present on the
  VM. Trivy and actionlint were not found on PATH. Planning installs nothing.
* Chromium, axe and Python package readiness will be checked by implementation,
  not assumed from unrelated prior runs.
* GitHub billing documentation says self-hosted compute is not charged Actions
  hosted minutes; self-hosting still costs VM capacity and artifact storage can
  accrue. Registration of a persistent runner is not part of this proposal.
* Do not execute untrusted PR code with the VM's inherited az/gh credentials.
  Local gates run owner-reviewed topic code with constructed fixtures in
  scrubbed environments; foreign/untrusted PRs need separate isolated runners.
* Local emulators cannot prove authenticated Azure/OIDC and environment
  controls. Record those as separate unmet release gates, not local failures
  disguised as successes.

## Critique Disposition

One critique completed with Revise, one High and one Medium finding. Both
planner-owned corrections are now applied; the original critique is preserved
and no second critique is requested.

| Finding | Owner and disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 High, untracked candidate inputs | Planner, resolved | Receipt contract now validates a fresh detached exact-HEAD snapshot, installs only snapshot sources, rejects original/validation untracked inputs and tracked modifications, keeps all caches/output external, and tests source/test/config contamination during creation and verification within the fixed test budget. |
| PC-002 Medium, inaccurate hosted cadence | Planner, resolved | Executive summary, workflow table, P03-T02 and phase details explicitly retain one consolidated workflow per eligible PR update, U-based cost comparison, and separate unapproved final-only alternative. |

## Follow-Up Items

* Cache/pin optimization and changed-scope fast mode are follow-up work, not
  substitutes for complete initial local coverage.
* Artifact retention cleanup requires a separate evidence-preservation review;
  no historical logs, SBOMs or release evidence are deleted here.
* Managed agent workflow usage/billing audit is separate; do not guess from
  their presence in the workflow inventory.

## Handoff

* Full P01-P03 implementation steps were executed and the consolidated matrix
  verified at 2c98c0e3fac0657bb67f093ac8f4561685c8c8d3. The one original Review
  is Complete, outcome Not accepted: RV-001 reproduces execution of an
  unvalidated receipt-adjacent environment binary during verification.
  Implementation markers preserve performed work, not acceptance of that
  defect. Route correction to a separately authorized Implement follow-up.
* Final artifact commit requires a fresh complete external receipt. It cannot
  close RV-001 or override the original Review. No publication is authorized.
* Changes and validation evidence:
  .copilot-tracking/changes/2026-10-18/local-rpi-validation-changes.md
* Other autonomous delivery remains paused until the actual gate is available.
* Independent exact-head assessment, protection/context mapping and retained
  hosted confirmation remain coordinator/owner gates, not locally proven.
