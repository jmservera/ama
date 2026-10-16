# Demo direct ingress changes

## P05 owner-directed continuation intake

Read the existing plan/changes first and reused their evidence, not rerun
research or critique. Clean feat/demo-direct-ingress matches open PR 362.
New requirements replace manual missing-secret/roster/SQL handoffs with a
default resumable orchestration and an honest private-network blocker.
Implementation active; offline validation pending. No Azure changes authorized.

## P05 implementation and validation

P05-T01 is implemented. Default direct setup creates/reuses credentials,
discovers the Bicep-created vault/attached identity, announces demo-only
private-vault fallback, records store/name tags, creates only a private
missing-roster template before any cloud calls, validates private input,
offers candidate/UPN helpers, verifies Entra after reconciliation and
orchestrates SQL check/one confirmation/apply/verified restart.
SQL helper preserves approved roles, bridges manifest keys/full labels,
discovers/validates Disabled public SQL and pins the selected API/subscription.
No approved personal-roster transport exists for the proof job, so the exact
authorized-host command is the implemented remote-connectivity alternative.

Coordination detects app/environment/revision/group-deployment activity and
uses local exclusion plus an owned advisory app tag, conditional when an ETag
is supplied. Strong cross-host simultaneous-start exclusion is not proved;
the supported wrappers cooperate, but raw portal activity remains outside it.
This limitation is explicit, not counted as strict distributed-lock acceptance.

P05-T02 store protection is implemented: default Key Vault parameter plus
Bicep guards, deployment CLI and CI refuse app-local full application
deployment. Dependency-only update is explicit. An initial implementation
using ARM listSecrets was rejected by the existing no-secret-list Bicep policy;
replaced with fail-closed deployment protection, preserving that policy.

Offline infrastructure suite: 257 passed without skips including local Bicep
compilation (initial failing mocks and the new store guard were corrected).
Scoped four-script mypy passed with installed-distribution import-untyped
diagnostics disabled; no production type error remains. Ruff baseline
comparison across all nine changed Python files found zero introduced
diagnostics; existing baseline warnings are retained. API auth suite starts
responsive ephemeral loopback servers with generated fixtures: 32 passed
using absolute project-test PYTHONPATH. Expected law-store-unavailable
diagnostics remained explicit; no deployed service/private dataset was used.
Final documentation/diff audit and delivery remain pending.

### P05 final candidate receipt

Final infra discovery passed 260 tests without skips in 61.735 seconds,
including compiled Bicep policy/credential-store guards. Four production
scripts passed scoped mypy (import-untyped disabled for installed source
distributions); focused Ruff passed. Baseline comparison of all nine changed
Python files had zero introduced findings. Existing broad lint/style warnings
are not represented as fixed. API loopback auth passed 32 tests with absolute
project-test PYTHONPATH. CLI help, Markdown local link targets (zero missing),
and git diff --check passed.

No full post-implementation Review was repeated. The original review record
now contains the requested bounded P05 acceptance audit with the candidate
evidence and explicit coordination/raw-deployment/live gaps. No second critique,
tenant authority, human approval, migration, Azure write, private-data read,
resource retirement or issue checkbox update was performed.

Task ID: issue-360. Slug: demo-direct-ingress. Full plan implementation.

## Execution

Implementation completed. P01 infrastructure and P02 auth/probes are independent,
write-disjoint phases. Parent owns P03 documentation and P04 validation/delivery.
Phase partition refined for safe delegation without scope change; no further
critique. All PC findings are incorporated in the current phase details.

## Boundaries

No Azure operations, identity provisioning, private data access or deployment.
Only local Bicep compilation may invoke az. Issue checkboxes remain untouched.
Default profile and edge behavior must remain compatible.

## Validation

Source packages were initially missing. Created a pip-only isolated session
venv and installed all five src distributions plus API dev extras/PyYAML.
Absolute PYTHONPATH API authentication loopback suite passed: 32 tests, 11.05s.
It starts responsive local HTTP servers on ephemeral ports using temporary
synthetic fixture state, exercising health, welcome, auth and role denials.
Expected explicit law-store-unavailable diagnostics are not a suite failure.
No deployed service, private dataset or billable model call was used.
Changed documentation local link targets and git diff --check passed.
Infrastructure/auth/probe focused results remain pending lane completion.

Full API discovery initially ran from repository root and reported six import
errors for project-relative tests/checks. Corrected to documented src/api cwd
with absolute project test PYTHONPATH: 563 tests, 110 opt-in skips, passed in
178.15s. No runtime source change was needed; the first invocation was wrong.

## P02 auth/probes

Lane completed with 72 focused tests passing. Direct flag/tag selection,
external-app validation, strict FQDN callbacks, NoProxy and explicit browser
conversion use shared provisioning/roster/enforcement logic. Edge discovery
and cdn checks are absent from direct mode, retained for edge mode.
Public smoke uses strict status and redirect-host checks, opt-in bounded local
auth hops and owner-owned private role-session files. Omitted role session
is Not run. No credential or redirect query is logged.
Both CLI help launches passed locally. device_login remains untouched so this
task does not duplicate PR 359.

## P01 infrastructure

Explicit switch and guards, fixed demo workload suffix, dedicated delegated
subnet/NSG, NoProxy/external environment DNS mode, tag and API-only staging
implemented. Existing dependency prefixes and identity references unchanged.
Background false omits agents and all four jobs; tests assert their conditions,
external/internal names, roles/guard combinations and backing private controls.
Lane targeted suite: 82 tests passed. CI-aligned Ruff/format/scoped mypy passed.

## Integrated validation

REQUIRE_AZ_BICEP=1 infra discovery: 234 tests passed in 59.094s, no skips.
All infra/*.bicep and infra/modules/*.bicep built and linted locally with az;
no deploy, what-if or other Azure operation invoked.
CI-aligned Ruff and format on test_bicep_policy.py passed; setup production
mypy --check-untyped-defs passed. Probe script/tests Ruff passed.
Setup script/test strict all-rule Ruff retains 159 baseline diagnostics
(119 E501 + 2 UP017 script; 38 E501 tests), with zero introduced diagnostics.
Probe mypy retains three baseline diagnostics (two untyped installed imports
and private_dns return inference); no newly introduced type errors.
No unrelated formatting/type cleanup was performed.
Setup/probe focused tests: 54 and 18 passed. CLI help and documentation link
targets/new anchors, git diff --check passed. API suite: 563 tests with 110
explicit conditional skips; no live SQL/browser/AI acceptance inferred.

## P03 documentation

Migration proposal added to infra/README.md: distinct names/subnet/environment,
private DNS and identity checks, image/config parity, environment/API-only staging,
queue/scheduled/import drain and reverse rollback, exact human/live gates,
selective retirement without deleting ama, pricing assumptions and cost overlap.
Updated ADR 0001 and architecture notes only for demo-edge applicability,
retaining historical evidence. Evidence pack audits all a-f, with c/d/e unmet.
KB index updated and append-only log added; owner memory untouched.
History-only 15e8158 confirms old broad public exposure, browser EasyAuth and
FQDN callback prior art, not copied obsolete configuration.
Official Container Apps billing/pricing pages retrieved 2026-10-16; numeric
regional rates unavailable, so documented rates are explicitly illustrative.

## Remaining Work

P01-P04 complete. One Review execution Complete, outcome Not accepted for its
assessed candidate; RV-001/RV-002 routed and implemented in the distinct
demo-direct-ingress-review-corrections record. No second Review or conformant
verdict is claimed. PR https://github.com/jmservera/ama/pull/362 opened on
feat/demo-direct-ingress; source and all required artifacts committed/pushed.
Current main's device-code and missing-tool fixes merged non-destructively.
Final integrated infra suite: 238 tests passed; setup production mypy passed.
Live c/d/e remain later owner/coordinator work. Required human PR/cost/migration
review and live proof are not completed approval.
