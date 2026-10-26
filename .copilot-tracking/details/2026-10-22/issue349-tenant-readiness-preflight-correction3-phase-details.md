---
title: Issue 349 correction3 phase details
description: Bounded implementation and gate task details
ms.date: 2026-10-22
---

## Metadata

Task ID: 349-correction3. Slug: issue349-tenant-readiness-preflight-correction3.
Plan: .copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan.md.
Research: .copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-correction3-research.md.
Current state: P01 and P02-T01 complete. One critique and one Review executed;
original Revise critique retained and disposed, Review Complete/Conformant
for bounded pre-commit correction. P02-T02 pending at committed evidence snapshot.

<!-- rpi:phase id=P01 -->
## P01: Implement and validate

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add regressions and strict provider requirement

C1-C4/W1-W2 prove property-level projection and strict bool semantics.
Add `providerEnabled` to Fake's valid auth response. At most three new test
methods; no deletions or generated targets. Cover each flag absent and False,
None, strings, integers including 1, float, dictionaries and arrays, with other
flag true; both true positive; both false negative. Test query path independently.
At CLI layer verify both formats, sanitized payloads, exit/overall,
readOnly=true and acceptanceEstablished=false. Run red first, then update only
AUTH_QUERY and the existing `enabled` conjunction. No new status/reason.
Completion: focused green tests and unchanged unrelated checks/call templates.
Actual: exactly three methods added and Fake positive flag; two source lines
changed. Red-first 35 tests with 30 failures, then green 35/35.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Run targeted validation

Depends on P01-T01. Run exact plan unittest, isolated no-cache Ruff lint and
format on the two targets, plus whitespace diff check. Preserve concise
results in changes artifact; no bytecode or cache files in repository.
Actual: bytecode-disabled suite passes; pinned Ruff 0.17.1 isolated no-cache
lint passes, format reports two files already formatted; diff check passes.

<!-- rpi:phase id=P02 -->
## P02: Review and local candidate gate

<!-- rpi:task id=P02-T01 -->
### P02-T01: Execute one independent Review

Depends on P01-T02. Fresh independent worker; write only this correction's
Review artifact at .copilot-tracking/reviews/logs/2026-10-22/issue349-tenant-readiness-preflight-correction3-review.md.
No source edits, live calls, gate, commit or remote mutation by reviewer.
Review execution and outcome recorded separately. Route findings without
repeating Review or overwriting historical outcomes.
Actual: Complete / Conformant, zero technical defects; reviewer passed 34
synthetic tests, honestly excluding one existing fixture for worker-local
restrictions. Parent passed full 35. RV-001 routes remaining commit/gate;
RV-002 and RV-003 preserve coordinator and hosted/human follow-ups.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Commit once and run one full gate

Depends on P02-T01. Resolve gh api user id/login, configure local noreply
email, explicitly use for author/committer. One Conventional Commit with
Copilot trailer. Fetch main and keep owner-specified base; if base differs,
record blocker rather than silently changing it. Use mktemp for unique /tmp
output path, exactly one --all invocation, no lock manipulation.
Verify exact-head receipt without replaying its commands. Preserve failed
outputs and stop without retry/push. Gate evidence remains external because
committing it would invalidate the receipt. PR stays draft; independent
coordinator assessment and human/hosted acceptance remain outside this loop.
