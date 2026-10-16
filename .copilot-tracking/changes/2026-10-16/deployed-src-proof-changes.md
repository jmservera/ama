---
title: Deployed src proof changes
ms.date: 2026-10-16
---

Task: issues-200-201-deployed-src-proof. Scope: full approved plan.
Implementation complete; review-ready handoff. Publication follows Review.

## P01: Implementation Direction

Honor explicit false networking, stage environment without workloads, add opt-in
secretless bearer ingress and bounded in-VNet initialization/smoke tooling.
All six critique findings are incorporated in plan/details.
At the initial P01 checkpoint, P01-T01 through P01-T03 were complete: explicit private network control,
environment-only staging, opt-in bearer mode and proof image/runner with eight
offline tests. Full infra discovery passes 114 tests; every Bicep build/lint
passes; scoped Ruff check and format pass.

## P02: Azure Execution

ACR run dba built all four source images and passed existing image contracts.
Run dbb built the proof image from the API digest. All images captured before
registry isolation. Dedicated `id-cutover-test-init` created within ama, with
registry-scoped AcrPull. No subscription role assignments or tenant writes.
Private bootstrap what-if: 9 Create, 43 Modify, 47 NoChange, 18 Unsupported,
11 Ignore, zero Delete. Only cutover resources modified, pre-existing forward
budget preserved. At that checkpoint apply was active; SQL administrator was
initializer, SQL and ACR public access Disabled, internal environment provisioning. Raw logs remain in
session storage. No data-plane call has run from the VM.

Bootstrap completed Succeeded at 14:03:51 UTC. Initializer execution
`job-cutover-test-init-siaykij` succeeded: SQL resolves to 10.40.4.25, empty
database preflight passed, two contained users granted, one fictional case and
zero staff initialized. Separate API-MI execution
`job-cutover-test-verify-oerk856` succeeded without a seed file, matching marker.
Application rollout what-if has 10 Create, 47 Modify, 52 NoChange, 18 Unsupported,
16 Ignore and zero Delete. First rollout uncovered an immediately relevant
existing alert-schema mismatch: queries referenced legacy _CL logs while
management-plane table metadata reports ContainerAppConsoleLogs with JobName/Log.
Corrected both queries and added a compiled regression; no validation bypass.
The retained runner source also ensures an owned partially initialized proof
can retry with its synthetic seed; Store still skips reseeding populated cases.
This correction is offline-tested only. Deployed runner dbb predates it;
clean initialization and seedless verification behavior are unchanged.

Corrected complete rollout Succeeded at 14:17:06 UTC. Private ingress smoke
passed health 200, anonymous 401, malformed bearer 401 and forged principal
401. Managed-identity HTTP token acquisition returned 400; authorized HTTP and
human staff remain Blocked. No tenant role or invented human binding added.
API revision `ca-cutover-test-api--bl42b7u` was Healthy/Running with two replicas.
Explicit restart replaced both replicas; post-restart HTTP smoke passed.

First post-restart SQL verification failed closed in the instrument: API startup
had legitimately added five assistant tables absent from the runner allowlist.
An API-MI metadata-only job confirmed exact names, without case/staff reads.
The allowlist now derives those names from the installed assistant MSSQL DDL,
while still rejecting unknown tables; offline regression added.
Since ACR is private, no repair image build or network reopening was attempted.
Instead, the tracked runner source was deployed explicitly as the verify job's
Python command through an ARM job specification, using the same immutable proof
image/packages and API MI. Source hash and rerun are captured in final evidence.
No SQL initialization or reseeding occurred after restart.

## P03: Delivery

Final pack/JSON/index/log and infra guide updated. Azure inventory: 87 generic
resources, all three budgets retained, zero deletions. Aggregate smoke is
Partially passed; bounded private infrastructure Passed, tenant staff and
authorized HTTP Blocked. Owner checklist stays unchecked.
Corrected post-restart execution `job-cutover-test-verify-8ycguks` Succeeded at
14:22:48 UTC without a seed. Its explicit source-command SHA-256 is
0560f367cf36fa7dd0e850040c55463b712b781a465d1ebd5f4e8de6406cd7e4.
Final validation: 117 infra tests including ten runner tests; all Bicep
build/lint and scoped Ruff check/format passed. Source workload packages were
unchanged; no claim of new full-project suites or measured coverage.
Staged identifier/token scan, Markdown links (workspace-relative RPI convention),
unchecked owner gates and protected-path assertions passed. Reference audit:
130 parity rows, 1464 reference locations, no missing destinations; generated
inventory refreshed. All implementation markers reconciled.
The single Review is Complete with outcome Residual work; bounded private
infrastructure is supported, RV-001 through RV-003 route tenant/staff and
functional/owner acceptance to distinct follow-ups. Review reran 117 infra
tests successfully.

Publication: commit 36dde3b pushed to the existing topic branch; PR #342 opened
against main with Refs #200 and Refs #201 only. Checks have started; no merge
performed. Nine generated-audit tests also passed before publication.
Requested delivery is complete with tenant/staff/owner limits still explicit.
