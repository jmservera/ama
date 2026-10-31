<!-- markdownlint-disable-file -->
---
title: PR 558 unresolved threads phase details
ms.date: 2026-10-31
---

## Metadata

Task ID: pr-558-unresolved-threads-2026-10-31.
Task slug: pr-558-unresolved-threads.
Plan: .copilot-tracking/plans/2026-10-31/pr-558-unresolved-threads-plan.md.
Research: .copilot-tracking/research/2026-10-31/pr-558-unresolved-threads-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete; actual verification and regressions passed | P01-T01, P01-T02 |
| P02 | Depends on P01 | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Source and compatibility

<!-- rpi:task id=P01-T01 -->
### P01-T01: Canonical hashing

C3: four raw Get-FileHash calls follow actual Test-DeckCandidate execution.
Replace only these with shared canonical-text hashing using bytes decoded
without dropping BOM and re-encoded after CRLF/lone-CR normalization. Prefer
byte-preserving newline replacement so unrelated whitespace cannot disappear.
Keep binary/template/media helpers unchanged. Add one dot-source test script
that uses temporary external UTF-8 fixtures and cleans only those owned files.
Cases: LF, CRLF, lone CR, significant whitespace, empty input and BOM retention;
compare actual four inputs with regenerated receipt only after Verify and
refresh; semantic-only mode runs before refresh. Avoid introducing Pester.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Verification and receipt

Copy only checked-in delivery into a new external output folder and run current
`-Action Verify`, not Build or native Render. All package guards must pass before
transferring generated report fields into receipt. Record report SHA-256 and
canonical convention. Run existing Test-NativeShapes.ps1 (32 assertions),
new source-hash regression and owner's requested runner tests. Update source
guide and index/log only for durable canonical-hash findings.
PowerShell container must have no network at execution, run as current UID/GID,
mount repository read-only and only the owned output path read-write.
Resolve `mcr.microsoft.com/powershell:7.4-ubuntu-22.04` to an immutable digest,
record acquisition and actual runtime version, then execute with `--pull=never`.
All runtime scratch/HOME/cache paths are inside the owned writable mount.
PC-001 is a worker-specific constraint not applicable to parent execution;
retain original critique, unchanged runner lock and actual gate requirement.

<!-- rpi:phase id=P02 -->
## P02: Publication

Current implementation/validation evidence:
.copilot-tracking/changes/2026-10-31/pr-558-unresolved-threads-changes.md.
Original Review, commit and complete external gate remain pending.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Disclosure and Review

Describe February 1 exclusive ceiling as through January 2027, preserving
activation, expiry and consent gates. Describe SQL CHECK replacement and
idempotency, employee/resident assistant routing and UI, and added actual browser
execution in hosted src-ci. Current main includes some runtime changes; describe
as included history, not new authorizations issued by this correction.
Review compares canonical inputs, generated report, receipt, docs, tests and
external body. Required independent Review occurs once.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Exact-head gate and remote thread operations

Use authenticated account id/login for repository-local noreply email.
Commit original evidence before complete external gate. Command:
`python3 tools/rpi-checks.py --all --lock-timeout 0 --base <origin-main-sha> --out <new-external-directory>`.
Preserve every failure. Fetch main again, verify current receipt and get
independent exact-head assessment; no post-gate source/evidence commit.
Normal push `git push origin HEAD:jmservera/fabric-research`, then body edit and
GraphQL replies/resolutions. Re-read thread state to confirm all three resolved.
Never resolve a thread with unverified claimed fixes or bypass publication gate.
