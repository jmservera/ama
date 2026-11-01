# Review: issue 228 supplier, contractor and procurement screens (2026-11-01)

Execution: executed once, self-review of the diff against acceptance criteria. Outcome: conformant for the read-only slice; four criteria only partly proven, routed to follow-up.

| Criterion | Finding |
| --- | --- |
| Package queue: period, scope and version, offered versus committed, call-off reference | Met (table, tested). Work-order reference shown for the selected home; the queue sits behind the shared home chooser from #152. Met with that limit. |
| Draft readiness only, unmet prerequisites, next reviewer | Met for the five prerequisites; reviewer shown by role, named person "Unassigned" because no reviewer data exists. |
| Submission and acknowledgement separate from independent review and acceptance | Shown as separate states, all not recorded. No submit, correction or acknowledgement function exists (PRD defers it, OD-47), so the flow is not delivered. Partial. |
| No portal, identity claim, booking, self-approval; no vulnerability reason | Met; tests assert no controls and no reason text. |
| WCAG 2.2, keyboard, textual state | Existing table-scroll region, captions, textual states. No browser or axe run locally. Unproven. |
| Design system components, no role simulator | Reuses host card, dl and table classes. Met. |

Verdict on closing: submission, correction and checklist capture are not built and accessibility is unproven, so the PR uses Refs.
Routed follow-ups: supplier-scoped job pack submit and correct endpoints (needs OD-47), reviewer assignment data, browser and axe check, validation in #155.

Post-review corrections (PR #655 Copilot threads, 2026-11-01): the three valid findings (prerequisite validity for withdrawn or rescoped orders, capacity evidence status beside recorded counts, fixed "Not supplied" and "Not started" states) were fixed with regression tests. Original outcome is unchanged and no second Review was run.
