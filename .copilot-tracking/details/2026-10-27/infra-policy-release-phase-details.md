<!-- markdownlint-disable-file -->
# RPI Phase Details: infra-policy-release

## Metadata

Task ID: 147-138. Slug: infra-policy-release. Date: 2026-10-27.
Plan: .copilot-tracking/plans/2026-10-27/infra-policy-release-plan.md
Evidence: .copilot-tracking/research/2026-10-27/infra-policy-release-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Governance and release authoring | Complete | P01-T01, P01-T02 |
| P02 | Validate and reconcile evidence | Complete | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Governance and release authoring

Context: merged definitions exist; research C6-C9 establishes independent gaps.
Boundaries: templates/workflows/docs/tests only; no live writes or runtime code.
Completion: named guard, exact-SHA CI prerequisite, four release SBOM artifacts.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Require pilot locks and clarify historical exception

Add pilotRequiresLocks to the main parameter-guard arguments and guard parameter/
checked output using existing minLength(1) pattern. Keep enableLocks default
false for dev/test. Extend the existing matrix with locked/unlocked pilot cases
and dev/test compatibility; preserve named guard expectations.
EX-001 remains an owner-controlled historical record with existing dates;
reason/status clarify current SQL always private, no authorized bypass/renewal.
No pricing, scope or assignment-name change.
PC-002: extend assert_parameter_controls across dev/test/pilot and both lock
states, union pilotRequiresLocks into the existing expected failures only for
unlocked pilot. Add pilotRequiresLocks to forced-ok guard mutations. Preserve
committed pilot example's existing region/quota/location placeholder failures.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Gate release on exact source CI and retain release SBOMs

Add main-only read-only prerequisite before build. Query the existing
src-ci.yml workflow runs using GitHub API filters head_sha, branch=main,
event=workflow_dispatch, status=success; compare returned head SHA with
RELEASE_SHA. API failure/missing/wrong evidence must exit nonzero. Use
GH_TOKEN only, never OIDC here; environment fields passed through env.
Source CI is deliberately not auto-dispatched or renamed.
PC-001: use explicit --method GET on
repos/{repository}/actions/workflows/src-ci.yml/runs with head_sha, branch=main,
event=workflow_dispatch, status=success, per_page=1. Use jq with --arg sha to
require an object with a nonempty workflow_runs array containing a record with
head_sha equal to RELEASE_SHA, head_branch=main, event=workflow_dispatch,
status=completed, conclusion=success. Bash -e -o pipefail propagates gh/jq errors.
Fake gh checks exact endpoint/method/filters; test success, empty/null/malformed,
wrong SHA/event/branch, same-SHA failed/incomplete, API errors even with plausible
success output. No trusting only query filters or echoing response.
Add SPDX generation/upload to each existing four-project build matrix,
same zava-forward image scanned/exported. Reuse pinned Trivy/upload actions.
Bound existing tests: assert dependency chain, permissions/query filters,
exact image SBOM path and execute extracted Bash under fake gh for success,
missing/wrong SHA and API failure.
PC-003: in test_release_is_main_only_serialized_and_gates_exact_image,
identify vulnerability scan steps separately from format=spdx-json; retain both
original scan assertions and verify one SPDX invocation and unique artifact
per matrix project, matching image, error on missing file, generation/upload
before docker save and no failure-tolerant condition bypassing export.

<!-- rpi:phase id=P02 -->
## P02: Validate and reconcile evidence

Dependencies: P01. No scoped heavy gate warranted; no full gate authorized.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run targeted/full infra tests, compiler and actionlint

Run existing targeted compiled-policy/governance/pipeline tests first; all
infra tests with REQUIRE_AZ_BICEP=1 afterward. Build every top-level and module
Bicep to stdout discarded, never generated source-tree JSON.
Use actionlint with infra/tests/actionlint.yaml for existing workflow names.
Record exact results; missing dependencies are blockers until resolved with pip.
No cloud login/what-if/deploy and no workflow dispatch.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Update runbook and criterion-level evidence

Document source-CI main manual prerequisite and per-release SBOMs, pilot lock
guard and historical exception. In changes and PR map #147's four criteria
and #138's six criteria to existing/new authoring and outstanding live proof.
No unchecked owner decision becomes accepted. Review once independently with
exact source diff and local evidence; preserve findings and route later work.
Commit artifacts with required coauthor, private-safe local GitHub email,
push current branch without force and create one PR to main.

## Completion Evidence

P01-T01: pilotRequiresLocks exists in main/guard; compiled matrix covers all
three environments and both lock states plus forced-ok mutation. EX-001 retains
owner/expiry and denies current public-SQL authority.
P01-T02: read-only source-ci gates build; actual Bash fake-gh cases validate
method/filter/response failures; four-project release matrix emits exact-image
SPDX before export with hard missing-file errors.
P02-T01: 452 existing infra tests passed, zero skips; all 25 Bicep files built/
linted, all five relevant workflow files passed actionlint; modified tests
passed pinned Ruff lint/format. Initial host run failed installed-API smoke
because distributions were absent; restored using pip in isolated session venv
and full suite passed. No heavy gate or Azure operations.
P02-T02: runbook records prerequisite/SBOM/locks/owner gaps; changes record maps
all issue criteria. Original critique preserved; independent Review next.
