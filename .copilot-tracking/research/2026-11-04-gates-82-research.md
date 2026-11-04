---
title: Issue 82 deterministic gates research
date: 2026-11-04
---

## Delivered already

* PR #898: GateResult (pass, fail, unknown with reason, owner, correction), rule record (source, effective date, version, reviewer), accountable-role safety release by a different person.
* PR #1035: funding, safety and resident gates fail closed on 'Ready to book' (`gates.booking_gates`, `Store.require_booking_gates`).

## Unmet

* Evidence gate was a free-text check outside the structured result. Eligibility, authority, capacity, quality and finance gates do not return structured results.
* Rule records are unreviewed exercise fixtures; reviewer naming needs a human.

## Slice 1 (this PR)

Evidence gate as a structured, rule-tied result wired into the booking path. Planning readiness: Ready.
