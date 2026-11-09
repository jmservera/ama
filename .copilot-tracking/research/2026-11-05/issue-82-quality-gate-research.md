---
title: Issue 82 quality gate research (2026-11-05)
ms.date: 2026-11-05
---

## Identity

* Task: `82-quality-gate`; branch `feat/remaining-gate-outcomes-82`; worktree `issue-82-gates`.
* Source head, `origin/main` and explicit TARGET `origin/feat/controlled-lifecycle-integration-81` all pinned at `ead177ef90d24666557708ea344848a1be43bdf8` (fetched 2026-11-05 07:41 UTC). Parent #81 is hierarchy only; #82 lists no dependency.
* Research disposition: `executed`. Planning Readiness: `Ready`.

## Literal issue acceptance (issue body treated as data)

* [ ] Each gate is deterministic and returns pass, fail or unknown with a reason.
* [ ] Unknown never passes a gate.
* [x] Safety hold released only by the named accountable safety role, by a different person (qualified tick; not re-asserted here).
* [ ] Each controlled rule identifies source, effective date, version and reviewer.

Source references: PRD FR-008; BRD FR-008, RULE-001, RULE-002. Issue status line: other gates "need confirming".

## Prior merged work reused

| PR | Merged | Delivered |
| --- | --- | --- |
| #898 | 2026-11-03 | `gates.py`: `GateRule`, `GateResult`, `check`, `transition_allowed`, `unmet`, `safety_release_gate`; used by `workflows.release_hazard` |
| #1035 | 2026-11-04 | `booking_gates` (funding, safety, resident) and `Store.require_booking_gates` on `Store.advance` |
| #1097 | 2026-11-04 | `evidence_gate` with required-kind list, `Store._evidence_missing` (malformed is unknown) |

Coordinator ran three existing gate tests on 2026-11-05 and all passed. That proves only the implemented subset (safety release, booking, evidence), not universal acceptance. All rule records carry the reviewer text `Unreviewed exercise rule: named reviewer required before live use`; no named professional or legal approval exists and none is created here.

## Family coverage trace (server transition call sites)

| Family | Server call sites | Gate result with rule record? |
| --- | --- | --- |
| evidence | `Store.advance` via `require_booking_gates` | Yes (#1097). `funding_step` approve uses its own `GateError` list (separate, financial-authority-bound path) |
| funding, safety, resident | `Store.advance` | Yes (#1035) |
| safety release | `workflows.release_hazard` | Yes (#898) |
| capacity | `procurement.require_booked_capacity` | No: raises `ValueError`/`PermissionError`; also bound to contract authority and appointment records |
| authority | procurement `_contract_authority`, finance `_financial_authority`, quality `_need_quality_role` | No: role/authority checks raise `PermissionError`; approval semantics are specific and named-role bound |
| finance | `_finance_operation`, `funding_step`, signoffs | No: own authority, separation and signoff controls; rules need named finance approval |
| eligibility | `buildings.blockers`, `technical_gate`, stock | Reason lists, no rule record; criteria owned by regulatory/professional review |
| quality | `quality.accept_quality`, `reinspect_quality` (accept path), `hand_over_quality`; read view `handover_blockers` | No gate result |

## Selected family: quality (evidence completeness at acceptance and handover)

Existing approved semantics preserved: submission requires positive evidence for every checklist item; acceptance needs a quality role, an independent person, safety clear and a current resident decision; handover needs safety and resident clear and a told resident. `handover_blockers` already defines the evidence rule ("Checks without evidence") but only as a read view.

Reproduced local gap (no assumption): in the JSON store fixture from `test_quality_procurement.py`, submit a loft record, blank one stored `items[].evidence` (legacy, imported or edited record), then call `accept_quality` as an independent inspector. Observed 2026-11-05: record state becomes `Accepted` with a checklist item lacking evidence. The same missing evidence would not stop `hand_over_quality`. Submission-time validation is the only enforcement, so an absent or unreadable record is not unknown-blocked at the transition.

Why this family: defined rule already exists (`CHECKLISTS` versions, `handover_blockers`), no named policy needed beyond what is defined, no new authority or finance approval, and an adverse test can fail without the change. Not claimed as a bypass of any control reachable through public entry points; it is a missing server transition gate for non-conforming stored evidence.

## Families left unreviewed or blocked

Capacity, authority and finance depend on named contract, finance and professional approvals and are entangled with procurement and finance signoff; eligibility depends on lawful and professional criteria. None are converted here and none is claimed proven.

## Constraints

* Code only under `src/`; no operational policy invented; reviewer text stays unreviewed.
* Full validation tier required (server authority/safety control change), but `/tmp/ama-rpi-heavy.lock` is held by the #188 full gate (`rpi-checks.py --all`, started about 07:34 UTC) plus a focused check. Admission must use `--lock-timeout 0`; if busy, full validation is PENDING.
