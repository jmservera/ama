<!-- markdownlint-disable-file -->
# RPI Phase Details: rebuild-148

## Metadata

Task ID 148; slug rebuild-148; date 2026-10-27.
Plan: .copilot-tracking/plans/2026-10-27/rebuild-148-plan.md.
Evidence: .copilot-tracking/research/2026-10-27/rebuild-148-research.md C1-C7.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Author and validate bounded automation | complete, source-only | P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: Author and validate bounded automation

Context: historical manual runbook has service-specific deletion dependencies
and separate budget inventory. New code belongs in installed src packages.
Intent: executable local authoring proof without cloud authority.
Boundary: never use a real profile, secret, private dataset, resource or model.
Validation: typed sequencing, negative fixtures, persistent SQLite rehearsal.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement checked sequencing and local rehearsal

Implement an immutable resource record, known-type ordering, exact scope
validation, a backend Protocol and engine. Backend inventories are separate
for generic resources and budgets; validate the full inventory before writes.
Re-read before each deletion and refuse newly introduced resources; permit
owned child disappearance after parent deletes only where the engine's exact
remaining inventory accounts for it. Use individual child-first operations;
no implicit descendant disappearance is allowed in this adapter. Before and after
every deletion compare both inventories to exact expected immutable records,
including kind, scope, lock and retention evidence. Missing safety evidence,
same-ID changes, added budgets/resources or unexplained removals fail before
the next deletion. This does not eliminate a future cloud race.

Implement a fixed mandatory stage tuple. Every perform is followed by verify;
failures stop later stages and preserve partial state, no automatic cleanup
masking failures. Bootstrap cannot expose apps; apps follow seed/credential.
The dry-run exposes stage/integration/check contracts and no operational success.

Fixed stage IDs in order: parameters, dependencies, discover, images, credential,
sql-users, seed, applications, authentication, staff, health, api-denial,
browser-redirect, workload-sql, model-standard, model-capable, restart.
Runbook step 1 maps to parameters; 2 to dependencies/discover; 3 to images/
credential; 4 to sql-users/seed; 5 to applications; 6 to authentication/staff;
7 to all remaining checks. Images means applicable API/agents/orchestrator/importer
immutable release images, not historical single-image assumptions. Discovery
means deployment outputs, not guessed hashed names. Both enabled models and
workload-identity SQL proof are distinct obligations. Every check returns a
local-simulation classification or real local SQL evidence, never live proof.
Use exact-trace and failed-verification subtests within the 30-test limit.

Use an owned SQLite local backend with fixed invented example.test staff/cases,
separate resource/budget tables and persisted stage witnesses. Seed/staff and
restart verification query persisted rows via new connections, not an in-memory
success flag. Local image/auth/health stages are explicitly simulations, never
calls to the existing Azure helpers. Do not copy secret or tenant provisioning.
CLI uses only a newly created TemporaryDirectory for rehearsal, never arbitrary
cleanup paths or inherited ZF_DATA. The engine is reusable; no cloud backend
or apply option is exposed. Maximum 30 tests in one external test module.

Completion evidence: full local roundtrip, repeated fresh runs, every dependency
ordering, injected stage/check/delete failure, foreign/unknown/locked resource,
new inventory, separate budget and malformed-input tests.

Actual evidence: rebuild.py and 22 tests in test_rebuild.py; full orchestrator
68-test suite, zero skips, passes. Installed CLI dry-run and synthetic-local
roundtrip pass. Synthetic SQL is deliberately a control-plane fixture schema,
not the production core SQL store: this prevents simulation from being mistaken
for application-store integration. All image/HTTP/auth/model stages remain
simulated-not-live.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Document limits and run local validation

Depends on P01-T01. Add component/runbook links and reproducible installed-module
commands; no tracking links in production documentation. Explain zero-I/O dry-run,
synthetic-only disposable rehearsal, no Azure adapter, no preservation/tenant/
retention approval and no issue checkbox completion. Do not rewrite historical
2026-10-12 results. No knowledge-base file change needed: infra/component guides
are canonical for this tool, with existing index routing.

Run orchestrator existing unittest discovery with core test support, Ruff
check/format and mypy. Initial missing import justifies pip installation into
an external venv. Keep outputs outside git; summarize exact commands/results
in changes evidence. No full/heavy gate. One independent post-implementation
Review assesses source/local boundary and criteria without claiming cloud proof.

Completed: both runbook updates, full orchestrator suite, Ruff check/format,
strict mypy, git diff whitespace and installed CLI modes. mssql-python 1.15.0
was restored after actual missing-library mypy errors; original failed attempt
is retained in changes evidence. No dependency manifest changed.
