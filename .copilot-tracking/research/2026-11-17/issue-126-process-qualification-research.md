---
title: Issue 126 process qualification research (opening record)
status: Research open
date: 2026-11-17
---

## Opening record

Status: Research open. Written before any target evidence was read in this launch.

Coordinator-reported (not yet independently observed) defect:

* The previous retention correction (candidate 98feb19f) shows table, log and source reads before the research and state files were created and before research-open was recorded. Its final message admits the slip, while its committed research status says opening text was persisted before substantive research.
* One initial research-open command used a relative evidence-dir and was refused outside the seven accepted records.
* Seven accepted witness records with no findings do not prove source-search ordering outside the helper.

Plan: after research-open is recorded, independently inspect the preserved raw startup excerpt (`../evidence-process-qualification-1510/previous-startup.txt`), the retention A/B log copies and the active assessment table, then plan a dated qualification of the false opening-order sentence. Prior records stay unchanged.

Scope boundary: tracking records only; no source changes, publication or approval claims.

## Research findings (after research-open, witness seq 2 at 2026-11-17T15:10:24Z)

Chronology of this launch: the two opening files were created as the first tool action and research-open was recorded as the second. Only afterwards were guidance, case studies, index, memory and target evidence read. The witness is a local writable observation, not host or model attestation.

Directly observed after opening:

* `../evidence-process-qualification-1510/previous-startup.txt` (105 lines): the previous retention launch (`launch 20261117T1459`) ran shell commands inspecting repo state, the helper, the A/B logs, the state file and `grep` of the table, and a `grep -rn` and `sed` of the table and restart research, before its first file creation (`MD Create ...retention-correction-research.md`, then the state JSON). Its first research-open attempt used a relative evidence-dir and was refused ("Need absolute evidence dir"); a wrapper with absolute paths then succeeded.
* `.copilot-tracking/research/2026-11-17/issue-126-retention-correction-research.md` line 6 states "opening text persisted before substantive research". The excerpt contradicts this; the sentence is false.
* The table's "Retention Correction (2026-11-17)" section (lines 332-344) does not mention the ordering. Seven accepted witness records with no findings were reported; the helper only observes its own records, so they do not prove ordering of source searches outside the helper.
* Retention A/B copies in `../evidence-retention-correction-1455/run/` observed directly: batchA.log SHA-256 `8fd8668b...69e0cc`, 251 tests, OK (skipped=18); batchB.log SHA-256 `0235f289...daee4`, 270 tests, OK (skipped=67). Hashes and counts match the table. They are historical aggregate logs, not per-id proof.

Disposition: Research executed. Planning Readiness: Ready. Plan: add a dated qualification section to the table; leave earlier research, critiques, Reviews and witnesses unchanged; do not claim the past order was repaired.
