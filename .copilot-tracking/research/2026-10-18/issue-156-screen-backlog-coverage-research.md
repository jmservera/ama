---
title: Issue 156 screen backlog coverage research
description: New bounded issue-universe research, distinct from the merged fifteen-row slice
ms.date: 2026-10-18
---

## Research brief

Status: Complete. Research disposition: executed. Output mode: audit. Task identity:
`issue-156-screen-backlog-coverage`. Focused audit for the coordinator and
design owners; automatic ordered RPI explicitly requested on 2026-10-18.
Research root: `.copilot-tracking/research/2026-10-18/`.

Determine a defensible complete time-bounded public issue universe, classify
screen scope from issue bodies and current pinned repository evidence, and
identify exact journey/task-flow/design traces or explicit missing evidence.
Do not create UI, claim human acceptance, alter issue checkboxes or replace
the merged #400 phase records. Missing designs are not a blocker to enumerating
coverage. No private support/data, live platform operations or spend.

## Extensions and participation

Repository instructions selected for public documentation, required context,
KB indexing/logging, privacy-safe commit and topic PR. RPI research selected;
documentation authoring/validation applies in implementation. UI implementation,
browser, Azure, SQL and accessibility conformance execution skipped: no runtime
or UI change or acceptance audit. Research is inline because this is one
continuous inventory trace; independent critique and original Review will be
separate bounded agents in their proper phases. No intake question necessary:
caller supplied scope, base, phase order and evidence constraints.

## Questions and prior-knowledge gate

* Q1: Does the supplied export cover the live repository issue universe?
* Q2: Which issues include a screen, exclude screens, aggregate children or
  remain ambiguous after full-body review?
* Q3: What exact existing journey/task-flow/design evidence supports each
  screen issue, and which remaining gaps need an owner or actual artifact?

Prior #400 is source evidence only, not reused phases. Initial live #156 body
and owner comment confirm AC1 unticked, AC2-4 checked, overall gate Blocked.
The clean branch starts at caller base
`2ca6d1c48bb95b65e6c349fe508e99c00a74efbe`.

## Cycle 1

### Wider

Paginated REST issues with `state=all&per_page=100`, excluding pull requests,
returned 184 unique issues (139 open, 45 closed). Supplied coordinator export
also has 184; issue-number sets agree. The 500 export limit was not reached.
Issue numbers are sparse, 6 to 360; highest repository PR is not an issue count.
Reflection: all-state classification is tractable, and prevents delivered screen
features or non-obvious governance surfaces being silently excluded.

### Deeper

Read all issue scope/acceptance blocks, with delivery blocks for ambiguous
operator, registry, document and regulatory surfaces, not just title keywords.
Source READMEs sometimes contradict stale live delivery text: the current
`src/api/README.md:1849-1871` panel section describes merged #160-163 storage,
while #162's live delivery text still says endpoints do not exist; #211 has API controls
but explicitly no rule-card UI. Current pinned source wins for existence, not
acceptance. Existing profile rows T01-T11 and C01-C04 supply partial historical
traces, not all 74 known screen-bearing issues. Eight ambiguities need explicit
owner delivery-surface decisions, not further unbounded inventory searching.

Reflection: include cross-cutting changes to visible denials, export controls,
privacy text, sign-in and external operator dashboards as screen scope. Do not
turn service/API diagrams or code into reviewable design artifacts.

### Contrarian

Tested three counterexamples to keyword-only selection: #160 is storage-named
but prescribes user thread actions; #110 is ingestion-named but requires visible
exceptions; #327 is performance-only but changes queue/CSV behavior. They remain
screen-bearing. #156 defines a documentation gate rather than a new screen.
#233 is not an epic: it requires a cross-role screen-design pass, so receives a
trace row rather than disappearing into #225-232. Closed #77/#87/#88/#91/#101
retain screen scope without inferring current design acceptance. #150 CLOSED
does not cure the design-system source's stale "stays open" sentence.

Reflection: API-only rule-card approval (#211) still has a planned human
review surface; mark its task flow/design missing where not supplied, rather
than excluding it. Keep #121/#125/#126/#127/#187/#189/#213/#222 as unknown
after inspecting their actual criteria: records, controls and review outputs
do not specify an application screen versus CLI/report/manual route.

### Parent synthesis and cycle re-entry

Accepted Q1: complete all-state issue-number set, 184 unique IDs, matches export.
Accepted Q2: 74 includes-screen (57 open/17 closed), 86 no-screen (59 open/27
closed), 16 epic-covered (all open), eight unknown (seven open/one closed).
Accepted Q3: exact existing partial traces can be linked; current feature-specific
design evidence remains NOT SUPPLIED. Do not claim literal AC1 satisfied.
Rejected alternative: fifteen profiles as proxy for backlog completeness.
Rejected alternative: exclude all closed issues or all API-named stories.
Deferred only real artifacts, task-flow gaps and explicit owner scope decisions.
No next research cycle: bounded universe reviewed and all material ambiguities
enumerated. Additional inventory searching would not supply missing owner intent
or designs. New issues/edited scope require a new dated delta, not retroactive
changes to this source snapshot or #400's frozen records.

## Evidence log

| ID | Claim | Provenance | Retrieved |
| --- | --- | --- | --- |
| W1 | #156 is open partial, #400 merged and AC1 incomplete | https://github.com/jmservera/ama/issues/156 and https://github.com/jmservera/ama/issues/156#issuecomment-6245518420 | 2026-10-18 |
| W2 | All-state issue universe is 184; export ID sets match REST | https://api.github.com/repos/jmservera/ama/issues?state=all&per_page=100 with `gh api --paginate`, pull requests excluded | 2026-10-18 |
| C1 | Fifteen existing trace rows, source pins, decision register and Blocked gate | `docs/reference/research/ux/zava-forward-prototype-profile-review.md:8-171`, read at base | 2026-10-18 |
| C2 | Nine workflow screen families and exact profile-flow contract; PRD v0.17.0 is a candidate | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:482-525`, `:727-798` and profile contract | 2026-10-18 |
| C3 | Current partial runtime evidence distinct from design acceptance | `src/api/README.md:841-965`, `:1269-1308`, `:1645-1871` | 2026-10-18 |
| C4 | Stage-based role journeys, nomination and source-change flows | `docs/reference/research/ux/customer-journeys/customer-journey-atlas.md:101-168` and linked role sections | 2026-10-18 |
| C5 | Required memory, original, addendum, index and customer primer reviewed; no specification change needed | `docs/reference/README.md:1-80`, `docs/reference/memory.md:1-54`, `docs/case_study_48_original.md:1-59`, `docs/case_study_48_addendum.md:8-178`, `docs/reference/research/sector/housing-association-primer.md:8-88` | 2026-10-18 |

REST retrieval completed before 2026-10-18T04:13:45Z; raw JSONL SHA-256:
`c3364f3da214433d9773e1b02cfbc3a0efc432f062ba5c942408c6e7bc341016`.
Coordinator export SHA-256:
`e3774b99ab045926f971b47b321847d35fef59c5368ecf1b3bedba7f28291117`.
Raw temporary files are not committed; durable issue IDs, state and concise
acceptance-basis evidence belong in the existing synthesis.

## Frozen classification membership and critique resolution

This membership, not totals alone, is the expected semantic input to validation.
Critique reconstruction had count-preserving swaps: it included #105/#162 but
excluded #117/#210. The adopted evidence distinction is explicit: #105 is registry
schema/envelope (visible release denial belongs to #219), #162 server isolation
with no additional prescribed UI; #117 affects visible upload availability and
retention controls in current source, #210 explicitly requires a non-AI provision
viewer. These are source-based parent dispositions, not a second critique.

* includes-screen: 74, 75, 76, 77, 78, 79, 80, 82, 83, 84, 85, 86, 87, 88,
  90, 91, 92, 94, 95, 96, 97, 98, 99, 101, 102, 106, 107, 110, 111, 112,
  116, 117, 119, 120, 122, 130, 131, 132, 133, 134, 135, 146, 150, 151,
  152, 153, 154, 159, 160, 161, 163, 210, 211, 212, 214, 215, 217, 219,
  220, 221, 225, 226, 227, 228, 229, 230, 231, 232, 233, 327, 344, 349,
  350, 360.
* no-screen: 6, 10, 23, 33, 38, 46, 47, 48, 49, 51, 52, 53, 64, 103,
  105, 108, 114, 115, 118, 124, 128, 129, 137, 138, 139, 140, 141, 142,
  143, 144, 145, 147, 148, 155, 156, 158, 162, 164, 166, 167, 168, 169,
  170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183,
  184, 185, 186, 188, 190, 191, 192, 193, 194, 196, 197, 198, 199, 200,
  201, 202, 203, 206, 209, 216, 223, 224, 290, 322, 323, 329, 332, 339,
  351, 358.
* epic-covered: 73, 81, 89, 93, 100, 104, 109, 113, 123, 136, 149, 157,
  165, 195, 208, 218.
* unknown: 121, 125, 126, 127, 187, 189, 213, 222.

PC-001 resolved by caller-authorized parent export access and temporary
workspace-relative source projection at
`.copilot-tracking/research/2026-10-18/issue-156-screen-backlog-coverage-source-evidence.json`.
Original export SHA above recomputed; comparison: 184 unique each, export-only
0, REST-only 0, per-ID state mismatches 0, 139 open/45 closed.
Projection contains original ID/state membership, provenance and captured REST
bodies for independent Review; remove after Review, never commit raw data.
PC-002 resolved by frozen membership and exact class/trace-set checks in details.
PC-003 resolved by precise panel README versus stale #162 issue attribution.

## Decisions, risks and readiness

All 184 issues will receive a durable public classification, compactly grouped
where no-screen evidence is shared. Screen issues require individual trace rows.
No metadata closure or issue state will be treated as design approval.
Planning Readiness: Ready. Source inventory work is eligible and not human-blocked.
Human/design/accessibility/content acceptance remains Blocked separately.
Self-check: three waves executed in order; sources and contradictions recorded;
all questions answered or precisely bounded; no source edits in Research.
