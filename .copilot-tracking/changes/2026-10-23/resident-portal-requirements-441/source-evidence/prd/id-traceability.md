---
title: Resident PRD amendment — stable allocation and upstream trace
date: 2026-10-23
status: draft
---

## Registry authority and allocation

The complete PRD text at `140d8f494482c78e84d15f3d46b9223d3c487af0`
was scanned before allocation, including staff-chat tables and BRD-referenced
IDs outside the central tables. This is PRD-local allocation, not reuse of
upstream BRD numbers. PRD FR-061 is Tokenomics; BRD FR-061 is the new routine
dispatch policy. PRD FR-051 is RAI release; BRD FR-051 is the regulatory
assistant. PRD FR-060 is the regulatory assistant and retains no-send.

| Family | Base definitions | Highest mention at base | Added | Candidate definitions |
| --- | --- | --- | --- | --- |
| FR | 61 | FR-061 | FR-062 to FR-071 | 71 |
| AC | 93 | AC-110 | AC-111 to AC-140 | 123 |
| NFR | 17 | NFR-017 | NFR-018 to NFR-021 | 21 |
| GOAL | 4 | GOAL-004 | GOAL-005 | 5 |
| CON | 9 | CON-009 | None | 9 |
| DD | 8 | DD-008 | DD-009 | 9 |
| OQ | 27 | OQ-027 | OQ-028 to OQ-031 | 31 |

PRD AC-001 to AC-073 and AC-091 to AC-110 are 93 actual definitions.
Mentions of AC-086 to AC-090 in upstream BRD references do not allocate
new PRD definitions; existing gaps are not filled. No old IDs are renumbered.
All original FR/AC/NFR/GOAL/CON/DD definition rows remain byte-preserved;
only OQ-023's definition is prospectively clarified.

## Author-maintained requirement trace

The normative author table is inserted in the PRD's `Resident upstream trace`
section. This companion adds acceptance intent and ownership context. All
BRD references are to the **unsigned candidate v0.20.0**, never an approved
baseline. Every new FR links to GOAL-005. Additional GOAL-002 links cover
case/control integrity; GOAL-004 links cover agent/value evaluation.

| PRD requirement | PRD AC | Additional goal | Upstream BRD FR / AC | Acceptance intent |
| --- | --- | --- | --- | --- |
| FR-062 | AC-111 to AC-113 | GOAL-002 | FR-053 / AC-104/105 | Own current projection/approved version only; adversarial reads denied |
| FR-063 | AC-114/115 | GOAL-002 | FR-054 / AC-106/107 | Durable safe receipt, quarantine, review not acceptance, negative retry |
| FR-064 | AC-116/117 | GOAL-002 | FR-055 / AC-108/109 | Scoped response, human/capacity confirmation, postponement without sanction |
| FR-065 | AC-118/119 | GOAL-002 | FR-056 / AC-110/111 | Omnichannel provenance, manual connector gaps, replay/ambiguous-match queue |
| FR-066 | AC-120 | GOAL-002 | FR-057 / AC-112 | Owned exceptions and accepted receiver distinct from delivery |
| FR-067 | AC-121 to AC-123 | GOAL-004 | FR-058 / AC-113/114 | Cited current answers, disclosure, unknown/model failure, controlled/hazard handoff |
| FR-068 | AC-124/125 | GOAL-002 | FR-059 / AC-115; RULE-027 / AC-125 | Verified safe preferences/help; optional service with non-digital parity |
| FR-069 | AC-126 to AC-128 | GOAL-002 | FR-060 / AC-116/117 | Separate login/entitlement/recovery/representative scope and immediate-next-request revocation |
| FR-070 | AC-129 to AC-131 | GOAL-004 | FR-061 / AC-118/119; RULE-028 / AC-126 | Complete policy OFF by default, controlled negatives, audit/disable without invented reviewer |
| FR-071 | AC-132/133 | GOAL-004 | FR-062 / AC-123/124 | Frozen contact/case/task/cohort protocol and honest paired outcome/effort reporting |
| NFR-018 | AC-134 | GOAL-005 | NFR-013 / AC-120 | Six essential mobile/keyboard/screen-reader task checks, no conformance assertion |
| NFR-019 | AC-135/136 | GOAL-005 | NFR-014 / AC-121/122 | Isolation/files/injection, diagnostic minimisation, separate retention/rights classes |
| NFR-020 | AC-137/138 | GOAL-005 | NFR-014; FR-056/057/061 / AC-111/112/119/122 | Accurate fail-closed state, replay/recovery and owned accepted handoff |
| NFR-021 | AC-139 | GOAL-005 | OD-55, not an approved numerical requirement | Author-proposed five-session bounded response measurement |
| GOAL-005 | AC-140 | None | FR-053 to FR-062; RULE-027/028 | Six-script manifest, no hidden essential privacy/accessibility deferral |

The BRD goal links for FR-053 to FR-062 and NFR-013/014 are preserved in
the inserted PRD upstream table. Its 23 added criteria AC-104 to AC-126 all
have an explicit mapping above; the 30 PRD criteria elaborate, not renumber,
that upstream contract. BRD AC-120 to AC-122 are quality criteria, and
AC-125/126 rule criteria, not unmapped FR acceptance gaps.

## Coverage and status

* New FR-to-AC: 10/10 = 100%; new FR-to-GOAL: 10/10 = 100%.
* Whole candidate FR-to-AC: 71/71 = 100%, threshold 80%.
* Whole candidate FR-to-GOAL: 71/71 = 100%, target 100%.
* An inherited FR-059 matrix range additionally links GOAL-002 whereas its
  definition links GOAL-004 only. Preserved and exposed, not silently repaired;
  new FR-to-goal rows match exactly. Coverage does not prove reciprocal fidelity.
* All 30 added criteria are **Not run**. No linked criterion is an executed
  acceptance, achieved business goal, authority waiver or owner signature.
* Six GOAL-005 scripts supplement rather than change the eleven staff-profile
  and nine workflow denominators. AC-140 is a goal-level manifest check, not
  a silently allocated eleventh FR.
* No tracker planning/upload is requested. Any later backlog must refine
  capability-sized requirements into scoped delivery/validation work, not
  treat structural coverage as completed stories.
