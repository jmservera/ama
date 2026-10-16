---
title: Issue 212 phase details
description: Implementation boundaries and validation evidence ownership
ms.date: 2026-10-16
---

## P01

### P01-T01

Create an append-only rule_card_check table in the existing card transaction.
Only new draft proposals can bind a validated executable contract; include it
in history so owner approval covers its exact immutable contents. No binding
means unknown, even for an activated legacy prose card. Seed drafts unchanged.

### P01-T02

Read persisted SQL cases under the existing store lock. Persist checks, alert
publication decisions and checkpoints atomically in the law adapter. Hash
card/source state, case rowversion and trigger; only schedule adds UTC minute.
Persist evaluation time with the checkpoint. Exact
replay returns the prior check. Alerts never change a hazard hold or send.
Explicitly approved hours are bounded integers, not parsed from legal prose.
Missing, future, invalid or ambiguous evidence returns unknown. Source lookup
uses exact provision identifiers, current versions and status/completeness.
Only an alert's named owner may acknowledge or give an outcome. Reporting a
false positive records history; it cannot suppress checks or resolve a risk.

Hazard predicate: absent/non-list hazards or missing/invalid awareness,
release evidence, source or urgency is unknown. An explicit empty list is
not applicable. For each evidenced open hazard compute due = awareness plus
the owner-approved elapsed hours; now >= due is breach risk, now >= due minus
attention hours is attention, otherwise clear. A clear is only this bounded
check, not legal compliance or hold release. No default statutory period.
The no-clock variant is unknown for open hazards. Released hazards need the
existing independent release decision evidence to count as clear.
Automated-decision predicate: absent evidence is unknown; explicit empty
automated_decisions is not applicable; significant true needs a named human
decision owner, decision time and evidence, else attention/unknown as appropriate.
No arbitrary fact paths, scripts, inferred applicability or model outputs.

### P01-T03

Expose /api/law/alerts scoped by role and case; actions derive actor/date
server-side and reject authority fields. Reuse existing trusted owner
capabilities for dispositions. Check after committed case mutations; failures
are logged and shown as unknown without undoing independent safety work.
Provide a bounded schedule entry point, no installed scheduler/deployment claim.

## P02

### P02-T01

Add test_rule_engine.py to core and API tests. Use constructed SQL facts and
explicit simulated approvals only inside test setup. Update the existing
inventory rather than adding a second route registry. Document contracts,
trigger recipe, safe manual path and unmet acceptance. Append log only.

### P02-T02

Absolute project paths for PYTHONPATH. Tools from /tmp/zf164. Run core/API
unittest, ruff and mypy; no uv, private dataset or cloud calls. Record measured
results and one final review artifact with an honest nine-row AC audit.

### P02-T03

Resolve gh api user, verify the supplied noreply email, configure local git
author/committer, commit with Copilot trailer, normal push, open PR using Refs
#212, and leave merge/issue checkboxes to the owner.
