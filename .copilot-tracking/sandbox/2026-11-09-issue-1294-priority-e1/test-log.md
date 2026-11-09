# Behavior test log: issue 1294 E1 (PROXY SIMULATION)

* Executor: one fresh-context general-purpose subagent, read-only, given only the policy files named in the prompt; answered 13 sub-scenarios (S1-S12, S9a/S9b) from the documents. Policy answers only; nothing was executed, no model binding or hosted CI was observed.
* Grader: the lead, against the oracle in test-design.md written before dispatch. Not independent of the implementer; independence rests on the executor context and the later coordinator exact-head review.
* Source identities graded: the working-tree hashes in test-design.md (the same bytes that were then committed; a later edit would invalidate this run).

## Grading

| Scenario | Result |
| --- | --- |
| S1 docs-only | Match (Focused, link and diff review, hosted possibly none, no blanket --changed) |
| S2 src/README.md only | Match (Source CI starts, no project selected, data guard runs) |
| S3 small employee chat | Match (harness, acceptance 3 tests, chat-panel selector; hosted does not run harness) |
| S4 SQL store | Match (Full, verified external full receipt) |
| S5 sensor_analysis | Match (Full; sensor suite local-only; hosted mssql does not run it) |
| S6 Bicep | Match (Full; --changed partial) |
| S7 docs plus infra | Match (Full) |
| S8 docs plus chat | Match (Focused, union including harness) |
| S9a/S9b workflow | Match (permission: Full; typo: Focused with recorded reason; doubt Full) |
| S10 focused no receipt, base moved | Match (targeted checks, no mandatory --changed; partial receipt only if produced and BASE RELAXED) |
| S11 absent/skipped hosted CI | Match (never a pass; local-only checks kept) |
| S12 proxy and approvals | Partial: approvals and green-CI limits matched; the documents do not mention proxy evidence labels, which live in the RPI evidence, so "not decided" is the correct reading, not a defect |

Result: Pass with the stated proxy limits (12 of 12 sub-areas, one partial by design).

## Ambiguities reported and dispositions

* Hosted results are inferred, table states them as expectations: already labelled "inferred, not observed" in the guide; no edit.
* S10 spans the README receipt paragraph ("new selected-tier run") and the coordinator focused rule: reads consistently; no edit.
* Rubric README branch-specific `gh workflow run` example and `/tmp` example paths: pre-existing, outside #1294; recorded, not edited.

## Limitations

Proxy simulation. The host cannot bind the intended target models or observe a canonical host-bound run. Not native, not intended-profile, not qualified-human proof. No test, gate, browser or hosted workflow was executed by this run.
