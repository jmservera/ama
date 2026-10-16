# Demo automatic roster changes

Task auto-roster-360, Refs #360. Full-plan offline delivery complete.

## P01: Implementation

P01 complete. Research and single critique complete. Critique corrections preserve owner intent:
positive mailbox-purpose evidence, resource-bound profile gate, shared envelope,
bound-SQL regeneration refusal and private fallback command. No live Azure work.
The shared infra module keeps legacy-array and generated-envelope readers
consistent. The new Bicep profile tag is authoritative over user-supplied tags.
Nested resource-bound deployment tag parameters are supported, avoiding a false
production default for newly tagged module deployments.

Ordinary implementation judgment: choose the owner's allowed stop alternative
for insufficient people, no --allow-reuse path because SQL must remain distinct.
Persisted generated identities recheck mailbox purpose before lock/auth mutation;
changed input and existing bound SQL rows are never silently overwritten.

## P02: Validation and Delivery

Full infra suite: 282 tests passed without skips, compiled Bicep included.
SQL initializer: 15 focused tests passed. Script mypy passed with
`--follow-imports skip --disable-error-code import-untyped`; shared module also
passes strict mypy. Existing script lint baseline excludes E501/E402/I001/B007/
UP017; all new lines separately checked, shared module and Bicep policy tests
receive full E/F/I/B/UP checks. 32 local loopback authentication tests passed;
they start responsive synthetic apps and exercise health/role boundaries.
Initial full-suite failures were missing PyYAML and expected new profile tag;
restored missing dependencies via pip in a session-only venv and updated the
coupled tag assertion. No system Python override or private data used.
Runbook, manifest guidance, evidence pack, index and append-only log updated.
One post-implementation Review executed: Complete, outcome Residual work for
separate authorized live acceptance (RV-001); no material source defect found.
Review: `.copilot-tracking/reviews/logs/2026-10-16/auto-roster-360-review.md`.
Implementation commit `37dd1ec` pushed to `feat/auto-roster-360`; PR #363 opened
against main: https://github.com/jmservera/ama/pull/363.
Delivery-state receipt is a documentation-only follow-up commit, not a source
change or another Review. All active plan tasks complete; no merge requested.
No issue checkboxes changed. Live sign-in/SQL/restart remain Not run.
