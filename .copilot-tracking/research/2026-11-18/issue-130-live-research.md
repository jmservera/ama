---
title: Issue 130 live demo research (opening)
ms.date: 2026-11-18
---

Task: issue-130-live. Refs #130. Research disposition: executed (live demo probes).

## Scope

* Issue #130 has one unticked criterion: "Representative participation and comprehension require authorized human evidence; constructed UI checks alone cannot pass that gate."
* Owner decisions 2026-11-18: synthetic desktop demo; live Azure authorised (rg ama, cap USD 700); person-run assistive-technology, DPO and Legal approval are not needed for the demo; production-only items stay deferred to #1905 to #1908.
* Known prior finding (#220 note): live staff writes from an Entra principal are refused (403) by `resident_decisions._operation`. Needs re-verification for the nomination route here; no src change allowed.

## Planned probes

* Live read of the nomination route and permissions; live write attempts (record, acknowledge, correct, review); representative authority and wrong-identity refusals; manual route; hazard route; unknown-not-none; the demo's representative-participation gate statement.
* Evidence dir: `.copilot-tracking/evidence/2026-11-18/issue-130-live/`.

## Planning readiness

Ready (opening). Findings are appended below after probing.

## Findings (executed)

* Only one criterion is unticked (representative participation and comprehension need authorized human evidence). It cannot be proven for the demo: data are synthetic, `representative_authorities` is empty, and person-run testing is excluded by the owner decisions.
* Live reads work (permissions, route HTML fragment, Resident tab panels). Live writes (record, owner variants, null hazard concern) all return 403 "Reload your current staff identity..." from the known Entra principal vs roster comparison in `resident_decisions._operation` (see issue 220 note). Representative fields on a new referral return 400.
* Offline suites pass: core 19 tests, api 9 tests.
* Evidence: `.copilot-tracking/evidence/2026-11-18/issue-130-live/`; note `docs/reference/research/issue-130-live-nomination-route-evidence-2026-11-18.md`.

Planning Readiness: Ready.
