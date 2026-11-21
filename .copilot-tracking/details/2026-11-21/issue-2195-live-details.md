# Issue 2195 phase details

Date: 2026-11-21.

## Phase 1: router

Keywords per agent (lowercase word match, plural-tolerant by stem prefixes):

* stock-prioritisation: stock, epc, ranking, prioritise, prioritisation, archetype
* assessment-preparation: assessment, survey, design, technical, pas
* funding-evidence: funding, grant, grants, claim, invoice, budget, milestone
* works-resident-coordination: appointment, handoff, capacity, schedule, access, resident update
* quality-evidence: quality, inspection, defect, acceptance, sensor, reading, discrepancy

Highest unique score wins; a tie or zero keeps the general agent.

## Phase 2: panel

Compute routing before `skill_sources`; set effective skill to the routed agent; add `routing` in `finish()`
and in `ask_unstored`'s return.

## Phase 3: UI

`chat-widget.js` `message()` gains `routing`; `chat.js` and resident `assistant.js` pass it.
`resident_demo/chat.py` gains `routing(topic, question)`; `app.py` returns it.

## Phase 4: validation

Targeted unittest, `test_accessibility_baseline.py`, `test_content_standard.py`, mypy and ruff per modified project.
