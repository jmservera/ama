---
title: Resident browser check 571 phase details
description: Bounded correction, test ownership and evidence requirements
ms.date: 2026-10-30
---

Task 571 / resident-browser-check-571. P01 and P02-T01 complete; local commit
pending; no correction blockers.

<!-- rpi:phase id=P01 -->
## P01: Correct and protect the resident check

<!-- rpi:task id=P01-T01 -->
### P01-T01: Supported prompts and fresh replies

Use `Which documents are missing from my case?`, `How do I fill in my form?`
and `What is wrong with my document warning or error?` (research C3/C4).
Keep explicit safety/consent/regulations questions and their expectations.
Typed helper may wait for actual assistant HTTP response and a new assistant
article count, then return that article. Do not select `.last` before waiting
for a new message or let old response text satisfy assertions. Keep `Survey:
Missing` and all existing document assertions. Scope subsequent document-source
geometry and other-resident missing-document assertions to their own replies.
Do not refactor unrelated delay/session/callback tests.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Semantic and rejected-input coverage

Extend current real HTTP document test with exact accepted check inputs and
rules/advisory/source assertions. Add one refused-input test for the three
stale prompts using existing `assert_host_routes`, proving no advisor,
credentials, reservation or provider use. Keep existing mixed-request negative
grammar tests. Add no redundant new framework or shared prompt registry.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Validation and documentation

Use installed local distributions in task-owned `/tmp/ama-571-venv`.
Commands from `src/api`, with
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests`:

```bash
python -m checks.resident_assistant_browser_check --axe /tmp/ama-520-axe-4.10.3.min.js --out /tmp/ama-571-resident-green
python -m unittest discover -s tests -p 'test_resident*.py' -q
ruff check . && ruff format --check . && mypy
flock -w 600 /tmp/ama-rpi-heavy.lock python -m unittest discover -s tests -q
```

Do not install or activate cloud credentials. Negative probe runs actual
Chromium/fixture app with temporary in-memory patch, no source modification.
Record exact invocation, result and expected failing assertion. Re-run positive
check if implementation changes; preserve original adverse output. API guide
explains complete supported questions, bounded unknown refusals and latest-reply
acceptance. No knowledge-base file materially changes, so no index/log churn.

Completion evidence: positive Chromium/axe check passed all 32 scan states;
negative probe failed exactly on the second document reply while earlier
document facts remained in chat. Focused chat units 27/27; resident discovery
154 run/7 opt-in skips; full API discovery 1363 run/318 skips under required
flock; Ruff check/format and mypy passed. Compact output and provenance are in
the dated changes evidence JSON. Original external outputs retained.

<!-- rpi:phase id=P02 -->
## P02: Independent review and local delivery

<!-- rpi:task id=P02-T01 -->
### P02-T01: Review

After implementation reconciliation, fresh reviewer activates `rpi-review`
once, with read access to candidate/evidence and write access only to the
designated Review artifact. Review covers acceptance meaning, source boundary,
regression sensitivity, commands, results and explicit skipped limits.
No re-review loop. New findings route to follow-up rather than silently fixing.

Executed once. Original Review outcome: Conformant within scoped correction,
no implementation defects. Frozen three-file diff SHA-256:
`bb7572a0272c3f41db1fef08ec6bdf558363f6ab1a8ffa81c3d9bccb15e6f30a`.
Original critique Revise retained; PC-001 disposition accepted by reviewer.
Low residual RV-001 human/live acceptance and RV-002 publication gates routed
to existing/future owners, not active implementation. No second Review.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Local commit

Resolve account through `gh api user` (public ID/login only), configure local
privacy-safe email, use same author/committer identity and required Copilot
trailer. Commit message uses `Refs #571`, never closing syntax. No push,
PR creation, Azure or deployment. Local gate/publication evidence not claimed.
Preserve all original RPI evidence. Final state distinguishes completed task
from session lifecycle and records outstanding gates.
