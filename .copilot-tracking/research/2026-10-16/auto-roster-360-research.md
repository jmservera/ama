<!-- markdownlint-disable-file -->
# Demo automatic staff roster research

## Research Brief

Owner-directed implementation follow-up, Refs #360. Focused internal convergence
research for the setup operator. Generate a private seeded demo roster from SQL
codes and enabled Graph members, preserve existing safeguards and continue the
existing Entra/SQL flow. No live setup, Azure writes, private datasets or secrets.
Evidence root: `.copilot-tracking/research/2026-10-16/`.

## Research Parameters and Direction Controls

The owner explicitly requests Research, Plan, Implement and Review artifacts,
implementation, offline verification and a pushed PR. This is an end-to-end
delivery request, not a request to enter a continuing automatic session.
Repository instructions, ADR 0006 and the supplied privacy/scope rules apply.
Research is inline because the SQL/Graph/setup trace is tightly coupled.
Domain skills: RPI phase skills selected; security-review and UI skills skipped
because neither a vulnerability audit nor a web change is requested.

## Questions and Candidate Areas

1. Which SQL candidate/Graph contracts can be reused?
2. Where must demo-profile, write/confirmation and privacy guards run?
3. Can generated assignments satisfy the SQL distinct-person and supplier rules?

Initial areas: `infra/scripts/setup-entra.py`,
`infra/scripts/initialize-workbench-staff.py`, their offline tests and runbook.

## Research Cycle Log

Cycle 1, Wider: baseline has a private-template stop and an existing SQL helper.
Deeper: traced candidate subprocess, Graph collection/paging, role manifest,
SQL distinct identity/immutable binding and advisory-lock ordering.
Contrarian: direct ingress does not prove a development profile; production
uses test environment names too. A positive environment tag alone is therefore
insufficient when a deployment explicitly reports production. Graph has no
universal human-person flag, so use the documented mailbox/resource naming
contract conservatively and fail on malformed directory data.

Reflection: preserve existing populated rosters and exact template recognition,
never replace partially completed invalid input. Candidate lookup must precede
remote mutation. The existing VNet job has no approved Graph/profile transport;
print a single exact setup command for a private-connected authorized host.

## Evidence Log

* C1: `infra/scripts/setup-entra.py:523`: existing missing-roster template writer.
* C2: `infra/README.md:1439`: SQL binding and restart are separate from app roles;
  distinct members and supplier-scoped Contractor are mandatory.
* C3: `docs/adrs/0006-src-layout-and-cutover.md:46`: source layout owner decision.
* C4: `infra/scripts/initialize-workbench-staff.py:154`: complete coverage,
  immutable bindings and existing supplier scope.
* C5: `infra/scripts/initialize-workbench-staff.py:318`: candidate listing currently
  omits Contractor scope; extend that same read-only contract, not a new SQL path.
* C6: `infra/scripts/setup-entra.py:576`: advisory lock rejects concurrent changes.
* C7: `infra/entra/app-registration.json:20`: ProgrammeManager is the available
  administrative workbench role; no blanket administrator role exists.
* C8: `infra/main.bicep:84`: production is the default deployment profile.
* W1: https://learn.microsoft.com/en-us/graph/api/user-get-mailboxsettings?view=graph-rest-1.0
  retrieved 2026-10-16: `/users/{id}/mailboxSettings/userPurpose` GET,
  MailboxSettings.Read prerequisite. Scoped API contract lookup after critique
  identified a material positive-eligibility gap, not permission to grant access.
* W2: https://learn.microsoft.com/en-us/graph/api/resources/mailboxsettings?view=graph-rest-1.0
  retrieved 2026-10-16: purpose distinguishes individual user from shared/room/
  equipment mailboxes; unknown purpose cannot establish eligibility.

## Findings and Alternatives

Q1 answered by C2/C4/C5: reuse SQL helper, retaining supplier for existing
Contractor rows. Do not invent an extra Contractor code.
Q2 answered by C6/C8: gate generation before directory enumeration, SQL discovery,
private roster writes or remote auth mutation. Read deployment parameters when
tags do not explicitly carry the profile; refuse unknown or production contexts.
Q3 answered by C4/C7: reserve the first stable ProgrammeManager code for admin,
shuffle remaining sorted people with a printed seed. Choose the allowed stop
alternative on shortage, not user reuse (the initializer forbids duplicate IDs).
Persist the seed atomically with the roster in a versioned private envelope,
while retaining legacy array readers. Existing incomplete template is replaced
only after one confirmation; read-only modes preview without writes.

## Risks and Residual Uncertainty

Graph resource/shared-mailbox naming is not independent Exchange recipient-type
attestation. The critique-driven implementation therefore requires positive
individual-user mailbox purpose (W1/W2); missing read authority fails closed.
The wider/deeper/contrarian reflection was extended for this material gap:
verified the API, inspected purpose values and rejected naming-only eligibility.
This is directory/Exchange classification evidence, not independent human identity
or competence attestation. Existing bound SQL prevents regeneration.
Live SQL, actual tenant person eligibility, sign-in and restart remain Not run.
Production-profile refusal must override demo/test tags and direct ingress.

## Current Decisions

Reuse the active clean topic branch `feat/auto-roster-360`, based on the merged
setup continuation. Preserve no-live-write boundary. Never fabricate SQL codes.

## Planning Readiness

Ready. Research disposition: executed, complete. One focused cycle covers the
named trace; no external discovery or independent research lane is necessary.
Selected approach: guarded generator integrated before auth mutation, persisted
seed and roster, unchanged complete-coverage/distinct-user SQL validation.
