---
title: One-command Entra setup changes
description: Implementation evidence and acceptance boundary for issue 351
ms.date: 2026-10-16
---

## Scope and State

Current continuation: owner selected implementation of all routed findings
and ready delivery on existing PR #356. Main merged as d007c69, preserving
both append-only log sides. Full infra reproduction in a fresh pip venv with
editable core/agents/api ran 169 tests: one failure in secret lifecycle's
hardcoded URI assertion after secret-name parameterization. Source boundary
is infra plus requested docs/RPI artifacts; no live tenant or private data.
RV safeguards and regression coverage are implemented and validated locally.
Source commit 90da083 is pushed, all eight hosted checks pass, PR body is
updated and `gh pr ready 356` succeeded. Original Review below remains
historical, not rerun. This final evidence-only closeout does not alter source.

## Initial Delivery (Historical)

Full plan P01/P02 authorized by expanded owner request. Implementation delivered
for review; the one independent Review is Complete / Not accepted. Three
Medium findings block ready delivery. Publication will be draft, not accepted.
Plan/details/critique use the stable one-command-entra-setup-351 slug.
No Azure mutation or private roster read is authorized for this development run.

## P01 Implementation

Implemented the standard-library setup CLI, its isolated safe Azure runner,
typed private user/group roster, tag/name and origin-linked discovery,
additive application/SP/role/callback convergence, bounded human consent
polling, optional app/Key Vault credential handoff and auth/runtime wiring.
The old CLI routes to the new flow while the old imported Python API remains.
API/edge tags are additive; no networking or policy changes.

## P02 Validation and Delivery

101 targeted tests passed, combining:

`PYTHONPATH=/home/azureuser/source/ama-wt/issue-351/src/core/tests:/home/azureuser/source/ama-wt/issue-351/src/agents/tests <session-venv>/bin/python -m unittest infra.tests.test_setup_entra infra.tests.test_initialize_api_auth infra.tests.test_edge_module infra.tests.test_identity_rbac infra.tests.test_bicep_policy -q`

The new setup suite has 39 tests. Initial combined run found source packages
missing; installed core/agents/api editable with pip --no-deps in the isolated
session venv, then reran successfully. Initial ruff was unavailable; installed
ruff/mypy with pip in the same session venv after that observed failure.
New-code ruff (--target-version py310) and mypy passed. Both CLI --help local
launches passed; git diff --check passed. Bicep tests compile locally, not
Azure deployment. No application serving code changed; full API server/SQL/AI
launch is not applicable to this standard-library infrastructure CLI slice.

Updated infra guide, manifest metadata, knowledge index and append-only log.
No private roster, dataset, live identity, secret or environment file was read.
Final preservation-patch validation passed: all 39 new setup tests, ruff,
mypy and git diff --check. Review executed independently once and reproduced
two gaps with memory-only fake data; see its canonical record.
Published draft PR #356: https://github.com/jmservera/ama/pull/356.
Implementation commit: 719016f, pushed without history rewrite.
Main advanced by one commit during the task; no silent rebase/merge was made.
The issue body is unchanged. Ready delivery remains blocked, not accepted.

## Acceptance Audit

| Criterion | Evidence/status |
| --- | --- |
| Single command, no required arguments, legacy CLI | Implemented; local CLI launch and full fake-az no-argument runs |
| API tag discovery, fallback names, ambiguity and overrides | Offline proven, including wrong-app candidate guidance |
| API/edge discovery across main and pending 344 | Offline proven for linked origin/routes/default/custom domains; local branch/pending diff read only; live topology not exercised |
| App registration, SP, roles, callbacks and safe reruns | Offline proven, including non-UUID sentinel, preservation, unknown-create outcome and no duplicate writes |
| Optional secret handling | Offline proven for app and Key Vault, no secret in output/argv, private-file cleanup and interrupted handoff blocker; live vault identity/secret validity unproven |
| Auth and runtime wiring | Offline proven, including null/disabled auth, HTTPS/proxy, exclusions/token-store preservation and failed rollout verification |
| Private fictional roster, user/group app roles | Partial: generated synthetic identifiers only; actual private file not read; RV-001 shows a fresh planned conflict is rejected only after registration/SP writes; zero-write invalid-role rejection UNMET |
| Consent and human instructions/polling | Offline proven matching Graph User.Read grant and timeout; actual human consent not performed; no automatic broad management grant |
| Isolated device login/profile and SP authority guidance | Offline proven for prompts, missing login, tenant binding, 0700 profile and Option A/B; actual interactive sign-in not performed |
| Python/az/extension/network/Graph preflight and friendly failures | Partial: mocked tools/ARM/Graph checks pass, but RV-002 selected-vault endpoint probe before credential creation is UNMET; actual network/tenant authority unexecuted |
| Check/dry-run and final summaries | Partial: no remote mutation/login/profile creation and drift/pending summaries proven; RV-003 a converged config with an already-Failed rollout can pass check, so failed-no-op detection is UNMET |
| Tests under infra/tests, stdlib implementation | Implemented; 101 combined targeted tests pass |
| SQL staff binding/restart and human browser acceptance | UNMET / not executed; explicit separate private-network/human gates, not claimed by configuration setup |
| Legal/consent/safety boundaries and private data | Preserved; no operational approval or source-currentness claim |
| Push/PR/checks/owner merge | Branch pushed, draft PR #356 opened; ready merge blocked by RV-001 through RV-003; issue body checkboxes intentionally untouched; no merge performed |

## Amendments and Divergences

Critique corrections are incorporated in the final plan. No new user decision.
The old callback-only Python API remains available for existing importers/tests;
the CLI will route to the supported setup flow.
Current-state amendment: add `entraClientSecretName` with the unchanged
historical default and pass it through Bicep. A setup-generated app-bound vault
secret otherwise would be overwritten by the fixed historical reference on a
later declarative deployment. Compiled regression covers forwarding and use.
This is narrowly coupled deployment persistence, not a new feature direction.
Explicit --bearer-only gates intentional service-mode selection; no-argument
runs preserve the existing action and report browser acceptance incomplete.
No automatic-session mode or child task was started.

## Independent Review and Routing

Review: .copilot-tracking/reviews/logs/2026-10-16/one-command-entra-setup-351-review.md.
Execution Complete, outcome Not accepted; three Medium findings, no Critical
or High finding. No second critique/Review or source correction was performed
after this task's one Review. Findings route to later rpi-implement:

* RV-001: preflight fresh planned effective roster conflicts before directory writes.
* RV-002: probe the selected vault endpoint before addPassword, without secret reads.
* RV-003: reject failed/in-progress provisioning even when runtime settings match.

This explicit draft boundary follows the accepted PC-008 delivery gate.
No claim that the script fully satisfies all expanded acceptance criteria.

## Remaining Human Gates

Live tenant execution, admin consent, private SQL bindings/restart and browser
sign-in are unexecuted. Juan Manuel Servera remains the exercise Legal,
Compliance and DPO owner; setup does not activate legal rules or grant approval.

## Owner-Selected Later Implementation: P01-T01 / P02-T01 / P02-T04

The owner explicitly requested continuation of PR #356 after Review, on the
same branch, including main merge and ready publication. This is implementation
of routed findings, not a second critique or post-implementation Review.

* RV-001: moved role-key/membership conflict detection into roster resolution,
  before registration discovery or any directory writes. Fresh state tests
  cover both roster orders and ordinary/check/dry-run execution, asserting
  zero writes and no registration/SP creation. Matching user/group roles
  remain accepted and reruns idempotent.
* RV-002: selected-vault metadata listing precedes addPassword. Denial and
  timeout produce no credential; no secret values are fetched by the probe.
  Successful ordering, recovery on subsequent rerun and no repeated probe on
  existing credential reuse are covered. Read-only runs never probe. Metadata
  visibility is not evidence of future write authority/network availability;
  existing post-creation failure recovery is retained.
* RV-003: a final fresh app read requires Succeeded provisioning independently
  of runtime patch necessity. Failed, Updating, InProgress, Canceled and absent
  state yield incomplete exit 2 on otherwise-converged ordinary/check/dry-run
  runs, without writes. A subsequent Succeeded state returns clean again.
* Compatibility: preserved the published PR #352 Custom host/proto header
  configuration and linked callback, including public-url check/rerun.
  Existing callback-only imported API is unchanged; legacy CLI delegates all
  setup options. The sentinel's existing-registration lookup and UUID rewiring
  now has an explicit regression in addition to fresh creation.
* CI: repaired inventory expectations for the secret-name parameter/default
  and interpolated URI. Existing compiled controls still check forwarding and
  use. Formatted the three new policy assertions that violated workflow lint;
  added explicit exception chaining for the setup login-boundary diagnostic.

### Validation and Mutation Evidence

Fresh private session venv: `pip install -e src/core -e src/agents -e src/api`.
Initial full infra reproduction failed 1/169 tests at the inventory assertion.
Ruff/mypy were initially absent; restored with pip after those failures.
Namespace validation exposed missing orchestrator/importer distributions;
installed those editable with pip, then all five namespace imports passed.

Final local results:

| Evidence | Result |
| --- | --- |
| `REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q`, installed distributions and absolute source test PYTHONPATH | 177 passed, no skips |
| `python -m unittest infra.tests.test_setup_entra -q` | 47 passed |
| Every `infra/*.bicep` and `infra/modules/*.bicep` build and lint | Passed offline |
| Exact src-namespace workflow ruff/format selections, including container tooling | Passed |
| Setup ruff (Python 3.10 target), mypy; container tooling strict mypy | Passed |
| Both CLI `--help` local launches; diff whitespace | Passed |
| Five-distribution namespace CLI/import/no-init checks | Passed |
| API suite from src/api with absolute core/agents test PYTHONPATH | 557 passed, 110 opt-in skips |
| Source compileall and browser JavaScript syntax | Passed |
| Hosted validate run 38944911484 and source run 38944911514 at 90da083 | All eight checks passed, including both previously failing jobs |
| RV-001 in-memory removal of resolve_roster planned-conflict guard | KILLED by fresh zero-write regression, assertion failure |
| RV-002 in-memory removal of selected-vault metadata try/probe | KILLED by unreachable-vault zero-credential regression, assertion failure |
| RV-003 in-memory removal of final provisioning guard | KILLED by converged-runtime all-mode regression, assertion failure |

Mutation execution used an isolated session script: replace only the named
guard's AST source span with `pass`, execute the modified module in memory,
patch the test module's SETUP reference and run the named behavioral unittest.
Each variant failed assertions, not import/runner errors. Source files remained
unchanged during mutation checks. No new mutation framework/dependency.

Validation-command correction: an extra API run from repository root failed
five module imports because its tests expect the project directory as cwd.
Reran from `src/api`, exactly the workflow directory, with absolute test paths;
557 tests passed (110 opt-in skips). No source workaround or test bypass.

### Current Acceptance Audit

| Criterion | Current evidence/status |
| --- | --- |
| No-argument stdlib setup; legacy CLI and tool guidance | Proven locally with mocked end-to-end runs and both CLI launches |
| API discovery, candidates/overrides and linked edge callbacks | Proven offline; current published edge Custom headers retained, no branch edits |
| Literal managed-identity sentinel creates/finds real registration and wires UUID client | Proven offline for both fresh and existing registration, idempotent reruns |
| Additive registration/SP/roles/settings and preservation | Proven offline; no live mutation claim |
| Private typed user/group roles and fresh conflict before writes | Proven offline, including mutation-killed fresh zero-write regression; actual private roster not read |
| Optional secret creation and selected-vault endpoint preflight | Proven offline, mutation-killed zero-credential regression; actual endpoint/write authority/secret validity UNMET |
| Failed/non-ready no-op provisioning, check/dry-run | Proven offline in all three modes, mutation-killed; no remote writes/login in read-only mode |
| Isolated login, Graph authority, consent instructions/polling | Proven with mocks; actual interactive login/authority/human consent UNMET |
| Infra workflow validation | 177 tests, offline Bicep and exact infra/container static checks passed; all eight hosted checks passed at source commit 90da083 |
| Authorized browser sign-in, private SQL staff binding/restart | UNMET / not run; separate human/private-network operator gates |
| Privacy, legal and safety/financial authority | No private data/roster/Azure mutation; no rule activation or invented approval |
| Publication | Main merge d007c69; source/evidence 90da083 pushed without force; existing PR #356 body updated and marked ready after all eight hosted checks passed |

Historical independent Review outcome remains Not accepted for its original
assessed source. These later implementation dispositions do not relabel it
conformant or imply new independent review. No issue-body criteria ticked.

### Delivery Result

Full plan P01/P02 implementation is Complete; no active implementation markers
remain. Manual mode, Implement phase, session stopped; no automatic follow-up
session or repeated Review. Source-readiness blockers are empty. Original
Review is Complete / Not accepted for its assessed snapshot, with subsequent
owner-selected implementation and mutation evidence recorded separately.

Existing PR #356 is open and ready, not merged. The body removes the old draft
blockers, uses Refs #351 only, and distinguishes local mock proof from every
unmet live gate. Final closeout changes only RPI artifacts; application, infra,
tests and workflow source are identical to the green source candidate.
