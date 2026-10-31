---
title: Employee briefing validation capacity correction changes
description: Fresh validation and current-main publication evidence for issue 531
ms.date: 2026-10-31
---

## Metadata and Execution Status

Task 531 / employee-briefing-loading-531-capacity-correction; automatic child of
employee-briefing-loading-531. Declared scope P01 assurance, then parent-owned
P02 publication. Status In progress. P01-T01 complete; P01-T02 active.
Plan/details/research/critique share this slug dated 2026-10-31.
Original parent changes, Review and critique remain unchanged.

## Completed Work

P01-T01: clean original topic, no existing PR; fetched and merged main
1330869ea675ff019958846330108b4f45e163ce as 18c1531f without conflict or rewrite.
Rubric, src-ci and tools/rpi-checks.py match main. Both log histories retained.
No independent workflow/hash or infrastructure change.

## Implementation-Time Plan and Detail Updates

One original critique Complete / Revise, PC-001 Medium applied directly.
Mandatory external wrapper patches the existing explicit scratch dir and adds
-B only to the owned loopback server. No source helper, new scenario, removed
scenario or runtime UI edit. Parent external artifact root:
/home/azureuser/.copilot/session-state/150adff8-0bdd-4492-abae-8a03af70abcf/files/.
Imported existing pip venv successfully; Python 3.12.3, no install needed.
No new significant/divergent decision.

## Validation Record

API and pinned-axe browser execution are running. Ruff check . passed;
configured ruff format --check . passed (65 files formatted). Explicit runner
lint passed. Focused mypy passed (1 source file).
An extra file-only format diagnostic bypasses the inherited checks/*.py
exemption and reports the existing runner would be reformatted. The same
explicit stdin formatter on origin/main exits 1. No unrelated whole-file
reformat is made; this diagnostic is not the configured project gate.
This local judgment preserves the existing format exemptions rather than
introducing a framework/style migration.

Current lock holder
observed PID 2813851; not stopped or modified. Standalone browser will wait
1800 seconds, retry once only if flock returns dedicated acquisition code 75.
Full gate owns the same lock internally and will use --lock-timeout 1800.
No historical pass is substituted.

## Blockers and Remaining Work

No active implementation blocker. Publication needs correction Review, evidence
commit, full gate, current-base receipt verification and exact-head assessment.
Live AC7 and missing specialist note remain explicitly unmet follow-ups; Refs #531.

## Follow-Up Items

* Prior RV-002: discovery-backed UX specialist design note.
* Prior RV-003: separately authorized live employee verification.
* Staff, screen-reader/voice-control and full Fluent acceptance remain separate.
