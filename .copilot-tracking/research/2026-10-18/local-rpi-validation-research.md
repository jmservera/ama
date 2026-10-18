<!-- markdownlint-disable-file -->
# Research: Local-first validation

## Research Brief and Parameters

* Task: actions-budget-local-rpi; slug: local-rpi-validation; date: 2026-10-18.
* Purpose: verify current implementation inputs for issue #413, not replan.
* Audience: qualified implementation session and independent coordinator.
* Posture: focused, explicitly requested by the caller. Output mode: audit,
  preparing reconciliation of the already accepted plan.
* Scope: native validation workflows, their source contracts, local tool
  readiness, accepted plan/details and original critique dispositions.
* Exclusions: private data, other worktrees, remote writes, cloud execution,
  new critique, application-domain changes and container-helper changes.
* Questions: Q1 unique coverage; Q2 destructive SQL ownership; Q3 exact-source
  receipts; Q4 hosted transition and unavailable controls.

## Extension Registry and Participation

Repository instructions and RPI research/implementation protocols apply.
The caller supplies phase direction and accepted decisions; no interactive
intake is necessary. Research was performed inline in this qualified CLI
session. No worker or new critique was dispatched. Web design skills are not
applicable to workflow/tooling edits. Research does not authorize publication.

## Cycle 1

### Wider

Read the complete accepted plan/details/critique/changes, all three validation
workflows, repository instructions, source README and coordinator guidance.
Read live issue #413 and list workflow state. Both legacy workflows are
already disabled_manually; Source projects CI remains active.

Reflection: the retained workflow must independently contain SQL and unique
legacy coverage; dispatch-only files cannot supply required PR coverage.

### Deeper

Read the existing container helper, SQL fixtures/connection builder, API/core
dependency manifests, strict browser harness and workflow contract tests.
Observed Python 3.12.3, Docker 29.9.0, 15,933 MiB RAM, 10,885 MiB available,
206 GiB disk available. Actual trivy/actionlint invocations failed as missing.

Reflection: SQL fixtures accept only loopback server names and support
ZF_SQL_PORT separately. Use 127.0.0.1 plus Docker-assigned loopback port,
not a comma-appended server string. Fixtures create two additional named
databases; isolation must cover the entire owned server, not only one DB.

### Contrarian

Checked the assumption that clean HEAD alone is enough: editable setuptools
installs can create ignored egg-info, tests can write caches, and user HOME
can supply credentials. A detached checkout alone is insufficient without
pre/post candidate and snapshot checks, external caches and scrubbed HOME.
General discovery deliberately skips opt-in SQL/browser suites; zero skips
is appropriate for the explicit legacy SQL gate, not general discovery.
Protection and ruleset reads actually returned 403 again. Main still resolves
to the supplied initial base. No remote setting or workflow was changed.

Reflection: retain original adverse critique, record dispositions separately,
and never treat local evidence as proof of hosted protection or approvals.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| C1 | .github/workflows/src-ci.yml:1 | Five project environments, namespace, Bicep/infra, strict harness lint, four images and fixable/full Trivy policy. |
| C2 | .github/workflows/mvp-ci.yml:116 | Exact seven SQL selectors; legacy image uniquely stresses logo mode and emits SPDX. |
| C3 | .github/workflows/mvp-validation.yml:32 | Compileall, migration requirements/regression, JS and tracked-data guard union. |
| C4 | src/check-container.py:44 | Existing helper owns dynamic ports/cleanup and positive/negative hardening plus PNG/plain startup; preserve unchanged. |
| C5 | src/api/tests/test_assistants.py:1142 | Destructive SQL fixtures require local host and create assistant/ledger databases. |
| C6 | src/core/src/zava_forward/core/mssqlstore.py:78 | Separate ZF_SQL_PORT and password auth support random owned endpoint. |
| C7 | infra/tests/test_pipeline.py:103 | Existing tests assert pinned infra dependencies precede discovery in retained and rollback workflows. |
| C8 | src/api/checks/regulatory_ux_check.py:21 | Pinned axe 4.10.3 SHA256 already exists; no silent skip in local runner. |
| C9 | .github/workflows/infra-plan.yml:6 | Source projects CI workflow_run is the privileged boundary; leave it intact. |
| C10 | .github/agents/ama-backlog-delivery-coordinator.agent.md:206 | Obsolete mandatory mvp test path and cloud fallback need replacement by local receipt gate. |
| W1 | https://github.com/jmservera/ama/issues/413 | Read 2026-10-18: implementation acceptance, independent assessment/hosted checks remain separate gates. |

## Synthesis, Decisions and Readiness

Q1-Q4 are answered by C1-C10 and observed read-only CLI results recorded in
`/tmp/rpi-413-local-validation.log`. Reuse accepted design: one Python runner
matrix and one focused test file, no framework. PC-001/PC-002 were already
resolved by the parent; the original Revise verdict is not rewritten.
No new critique or planning loop is warranted.

Research disposition: executed. Planning Readiness: Ready for reconciliation
of the existing accepted plan, not new plan creation. Runtime readiness is
not yet established: missing tools, dependency restores, actual SQL/browser/
images/scans and final exact-HEAD receipt remain implementation work.
Hosted checks, protection mapping, independent exact-head review and merge
remain coordinator/owner gates. No claim of earlier execution is made.

## Self-check and Re-entry

All three waves executed inline in order; primary inputs inspected directly.
No application source changed during research. No private dataset or credential
file was read. Re-enter only for a material in-scope evidence conflict, not
to repeat the accepted critique. Parent next action: reconcile then implement
P01-T01 through P03 in order; one original Review after implementation.
