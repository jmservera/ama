---
title: Resident demo authority extension research
description: Focused source-only research for issue 521
ms.date: 2026-10-28
---

## Research Brief

Extend the resident demo authority through 2027-01-31 UTC for issue #521.
Audience: implementation and independent reviewers. Output mode: convergence.
Posture: focused, selected from the named code/SQL/helper targets.
Resolved evidence root: `.copilot-tracking/research/2026-10-28/`.

## Direction Controls and Extensions

User explicitly requests the full ordered RPI loop and publication on
`chore/resident-authority-extension-521`. No Azure access, `az`, secrets,
`.env`, resource changes, paid actions, uv, force-push or main push.
Keep synthetic resident-only scope, min replicas zero and all approval guards.
Live apply remains pending separate owner confirmation.
Repository instructions and RPI phase skills apply; UI skills are inapplicable.
Research is inline because the bounded authority trace is tightly coupled.
Independent final-candidate critique and Review will be delegated.

## Questions and Candidate Areas

1. Where are active authority boundaries and executable copies?
2. How can Python share one authority without weakening SQL's independent guard?
3. What rotation, cost and publication prerequisites must remain pending?

Start with `src/core`, `src/api`, `infra/sql`, `infra/scripts`, component
READMEs and relevant tools tests. Existing historical evidence is not current
authority. No external/cloud discovery is needed to change this local constant.

## Research Cycle Log

### Cycle 1 Wider

C1: `src/core/src/zava_forward/core/resident_showcase.py:34` already loads
the packaged JSON policy. `resident-demo.json:2` currently caps it at
2026-12-31T23:59:59Z; the issue's November Python baseline is stale.
Reflection: reuse the existing source of truth, rather than add another.

### Cycle 1 Deeper

C2: `infra/resident-demo.bicep:29` loads that same JSON;
`infra/scripts/resident_demo_secrets.py:49` aliases AUTHORITY_END.
C3: `infra/sql/resident-showcase.sql:22` still embeds November 1 and
only creates the constraint on a new table. Merely changing the literal will
not migrate an existing database. `infra/scripts/resident_showcase_sql.py:30`
already renders principal placeholders, providing a natural policy substitution.
C4: `src/core/tests/test_resident_showcase_sql.py:353` tests the old SQL limit;
core config and infra helper/deploy tests encode the December cap.
Reflection: SQL needs a checked, transactional replacement on rerun, not row
renewal. Add renderer and real-loopback-SQL migration regression coverage.

### Cycle 1 Contrarian

C5: `infra/README.md:3442` documents prior December renewal but explicitly
retains old SQL rows and vault expiries. Extending source cannot renew those.
C6: `src/api/README.md:77` and `infra/sql/resident-assistant.sql` retain a
separate inference tariff/admission expiry. Do not extend model spending.
C7: `src/README.md:72` requires the full committed exact-head publication gate
for SQL changes. `tools/rpi-checks.py:1322` preflight runs Azure CLI for offline
Bicep; the caller explicitly forbids running `az`. Publication is blocked
unless a valid allowed complete gate can be obtained, not waived or faked.
Reflection: preserve the old inference guard and live-expiry independence.
No Azure discovery is permitted, so actual accrued spend/headroom is Unknown.

## Alternatives and Decision State

Select 2027-02-01T00:00:00Z in the existing packaged JSON and render SQL from
AUTHORITY_END. Reject end-of-day fractional instants and duplicated constants.
Reject table-only creation changes because deployed constraints would remain
stale. Preserve all rows and require separate named renewal approval.
Retain all prior guards and exact-resource what-if restrictions.

## Cost and Rotation Evidence

C8: `infra/README.md:3360` restricts the helper to two *new* secrets; it rejects
Modify. Do not relax it to rotate existing secrets. Rotation of existing versions
needs a separately reviewed exact-operation plan. USD30 resident allowance is
within USD700, not new headroom. New source-only resources and current paid
actions: zero. Bound any later operation with a fresh all-in headroom check.

## Synthesis and Readiness

All three questions are covered by C1-C8. Accepted: shared cap, checked SQL
migration, independent live gates. Deferred: actual headroom, credential/SQL
renewal and live verification. Research disposition: executed.
Planning Readiness: Ready for source-only work; Azure apply and publication
remain separately gated. No additional research cycle is justified: remaining
unknowns require expressly prohibited live access, not more local searching.
No subagent or external source was used; tightly coupled trace handled inline.
