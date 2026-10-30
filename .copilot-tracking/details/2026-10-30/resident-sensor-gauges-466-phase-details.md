---
title: Resident issue 466 phase details
description: Bounded implementation and validation expectations
ms.date: 2026-10-30
---

Task: 466 / resident-sensor-gauges-466.

<!-- P01 -->
## P01: Reconcile evidence

<!-- P01-T01 -->
### P01-T01: Update the existing API guide

Use research C1-C7/W1-W2. Add six-criterion matrix adjacent to existing resident
assistant documentation, with current recorded decision rather than choosing
a new model/cap. State that current issue checkbox for AC6 remains unticked and
owner/coordinator reconciliation is required. Correct unconditional
unknown-documents wording to distinguish available facts from unknowns.
No runtime or web assets change. Completion is an accurate narrow diff.

<!-- P02 -->
## P02: Validate and preserve outcomes

<!-- P02-T01 -->
### P02-T01: Local engineering evidence

Use session-owned pip venv after missing imports/tools were observed.
From src/api run exactly the requested PYTHONPATH discovery, Ruff check,
Ruff format --check and mypy, with heavy work serialized by flock.
Run focused core resident tests and existing sensor/assistant browser harnesses.
Use pinned axe 4.10.3 for chat and own-home sensor text/table states.
Fixtures start an actual loopback HTTP app; verify responsive health check.
No SQL-configured/live entry point or credential file is read.
Store outputs externally; failed checks remain explicit evidence.

<!-- P02-T02 -->
### P02-T02: Independent Review and final gate

Activate rpi-review once and use a fresh bounded independent reviewer.
Record findings without a same-task correction/Review loop. Keep required
human acceptance open. Commit implementation plus original RPI evidence using
authenticated privacy-safe author/committer identity and required trailer.
Fetch main, do not rebase or change the supplied base autonomously.
Run complete local gate on the committed candidate with external output;
the runner itself acquires the heavy lock. Preserve receipt outside git,
not by a later evidence commit that would invalidate it. No push or PR.

## Current handoff

P01-T01 and P02-T01 are complete. Changes record retains commands, counts,
external log hashes and browser/axe incompletes. No runtime or web assets
changed. P02-T02 deliberately remains pending at Review intake because the
original Review and committed-candidate full gate are its remaining lifecycle
operations; this is not an unimplemented product requirement.
