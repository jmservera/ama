---
title: Issue 350 feedback correction4 phase details
description: Implementation and validation details with exact evidence limits
ms.date: 2026-10-22
---

Task ID: issue-350-demo-feedback-correction4.
Plan: .copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-correction4-plan.md.

## P01-T01: Localized strict types

Research C1-C3/C5: `server.py` passes account provider fields and map values
directly. In `check_me`, after existing account-key/provider guard, reject any
name/email not str. Existing provider guard already rejects all non-string
types; retain it unchanged. After map-key guard, reject tiles unless None or
str, and attribution unless str. Field-specific failure reasons required.
No `nonempty_str` on name/email/tiles/attribution; no URL/email parsing.

## P01-T02: Focused regressions

Mutate one field at a time in both real-builder staff/contractor fixtures.
Serialize through `report_for` to establish real JSON behavior. Include null,
list, dict, bool, int, float for account name/email/provider and attribution;
tiles excludes null from invalid values. Include empty and populated lists/
objects and both booleans to avoid truthiness-based false positives.
Positive cases: null tiles plus empty attribution for each role, explicit empty
contractor email, empty account name/email and arbitrary strings, preserving
provider nonempty. Confirm valid boundary still has overall blocked,
acceptance not-accepted, and case_write_reload blocked.
PC-002 applied: explicitly test empty/nonempty arbitrary strings for each of
name/email/tiles/attribution for both roles and require `me_contract` PASS on
every positive mutation. Negative mutations require FAIL and the relevant
account/map contract diagnostic (existing provider diagnostic retained).

## P02-T01: Cache-free focused validation

Use already installed `/tmp/fh350-venv` packages, not PYTHONPATH workarounds.
Use `PYTHONDONTWRITEBYTECODE=1`, Python `-B` and Ruff `--no-cache`.
Test failures caused by new assertions can be captured before implementation to
prove regressions. Record final count/results independently of prior 58 tests.
Keep logs external. Confirm no ignored inputs regenerated.
PC-001 rejected: worker-local scratch restrictions conflict with the owner's
explicit `/tmp` output instruction and do not govern this primary execution.

## P02-T02: Initial gate attempt

Research C4: gate rejects dirty/untracked inputs before checks and before output
directory creation; later commits invalidate any receipt. The owner's explicit
commit-only-after-pass instruction prohibits preparing a committed candidate.
Do not stage/hide/exclude inputs, modify the gate, use an alternate index or
run against old HEAD. Attempt the requested exact-base command once with unique
external output and external console capture; record expected preflight refusal
honestly. A receipt absent after refusal cannot be verified; do not substitute a
historical receipt. No commit, identity lookup, push or PR update on failure.
If a lock is reached, wait with long timeout and do not interrupt its owner.

Actual execution: waited using exclusive flock without interrupting any holder,
then invoked exactly one gate with the required base and
`--out /tmp/ama-350-correction4-20261022-Qdq0J7/full-gate --lock-timeout 86400`.
Exit 1: `BLOCKED: Candidate has tracked modifications or untracked inputs`.
Preflight stopped before checks/output creation. No receipt exists; exact-new-
HEAD/base verification is unavailable because no new HEAD was authorized.
HEAD remains 05b5b7d2b754ae0e7134df8db1a867861726a821.
No ignored inputs were regenerated.

## P02-T03: Owner-authorized committed-candidate gate

On 2026-10-23, the owner selected `authorize_local_commit_then_gate`. This
supersedes the earlier commit-after-receipt sequence for this bounded
correction. Commit the exact corrected candidate locally, with no push, then
run exactly one fresh full gate against
`b4d467cad84535ed106cffa1ae9aa303db7bfed2` using a unique external output.
Verify any emitted receipt against the exact commit and base. If the gate or
receipt verification fails, stop without a further attempt. If both pass,
obtain an independent coordinator assessment before any push or PR update.

The required `get_changed_files` tool is unavailable. On 2026-10-23, the owner
authorized one `git diff --cached` fallback to inspect the staged content for
this isolated commit. Use that fallback once, then commit locally without
push. Do not use additional diff commands. The single fresh gate remains
pending after commit.

## P03-T01: One Review

Review corrected diff, actual test/lint output and gate result against FR1-FR4,
explicit write scope and acceptance limitations. Record one outcome and route
residual work for coordinator/owner; no repeat Review, source correction loop
or acceptance claims. Keep previous RPI evidence untouched.
