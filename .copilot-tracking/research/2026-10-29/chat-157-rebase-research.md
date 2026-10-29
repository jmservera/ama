<!-- markdownlint-disable-file -->

# Task Research: chat-157-rebase

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/chat-157-rebase-research.md |

## Research Brief

Bring PR #503, Refs #157, onto origin/main without losing branch chat
accounting or main's #506 bounded audit snapshot. Audience: coordinator and
independent reviewer. Output mode: convergence, preparing implementation.
Scope: rebase conflicts, source/test compatibility, scenario pins and local CI
selectors. Non-goals: new features, Azure operations, push, issue closure,
rewriting historical adverse RPI outcomes or asserting hosted acceptance.

## Research Parameters

Focused posture, selected by the bounded caller brief. Internal candidates:
core chat/accounting, regulatory chat, package tests, CI and scenario manifest.
External scope: GitHub PR metadata only. Evidence root: .copilot-tracking/.
Research edits are evidence only. Full API discovery requires shared-lock
admission; use /tmp/mv and installed src distributions. No private datasets.

## Extension Registry and Provenance

Repository instructions and RPI phase skills selected for layout, preservation,
validation and dated evidence. Web skills skipped: no UI change is proposed.
Research specialist skipped: the shared conflict is one continuous trace,
best investigated inline. Independent critique and final review remain required.

## User Participation and Research Decisions

The user explicitly requests all four phases and authorizes rebase and local
commit. No routine phase prompt is needed in this non-interactive execution.
PR metadata says OPEN and isDraft=false, despite the request's draft label;
do not change its state. Existing checks passed only on the old branch head.

## Scope and Success Criteria

Preserve both feature intents, both append-only/index contributions and main's
rubric/scenario copies. All source stays in src, tests outside packages.
Run focused chat/regulatory tests, package Ruff and applicable mypy. Record
all command results and residual hosted/human/publication gates honestly.

## Task Research Requests and Direction Controls

User-authorized rebase of the existing branch, not a new workstream.
No push, no Azure resource changes, no issue-closing keywords.
Original dated evidence must remain intact.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | How do main's audit snapshot and branch accounting compose? | depth | Answered |
| Q2 | Which pinned sources and test selectors need revalidation? | straightforward | Answered |
| Q3 | What local/hosted evidence can this no-push task establish? | straightforward | Answered |

## Prior Knowledge Gate

Read original/addendum, reference index and owner memory. Inspected existing
chat-review-fixes changes and git divergence. Prior checks are historical,
not fresh candidate evidence. No matching session-store result was found.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Clean branch feat/agent-chat-157, matching open PR #503. Eleven branch commits
include isolated chat, accounting/provenance and redacted-length corrections.
Main ends at 3e742ef1 (#506). Existing hosted contexts passed for old HEAD.
Reflection: prioritize regulatory_chat integration and current CI contracts.

#### Wave 2: Deeper

Main's usage_status captures the maximum SQL audit sequence and bounds both
ends of the query. JSON captures file size, reads only the captured tail,
then caps positions. Main also extracts _refer and adds automatic conflict
routing/offline usage receipts. Branch adds actor_role to all three direct
message writers, including copied historical messages. Preserve these in
main's refactored writers, not the obsolete doubt implementation.
Reflection: the actual conflict extends beyond a single audit line.

#### Wave 3: Contrarian

Whole-file main selection loses actor_role and breaks SQL insertion; whole-file
branch selection loses bounded snapshots and conflict referral. Prior CI cannot
prove the composed result. Existing scenario tests validate exact SHA bindings
to four public sources; retain main manifest and rerun rather than blindly
changing hashes. /tmp/mv lacks installed namespace distributions (observed
ModuleNotFoundError), so restore existing editable dependencies before tests.
Reflection: focused regression coverage, not conflict-marker absence, decides
compatibility. No further cycle is needed for this bounded integration.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| C1 | src/README.md:69 | Local gate scope, isolated SQL and lock requirements distinguish focused checks from publication. |
| C2 | .copilot-tracking/changes/2026-10-29/chat-review-fixes-157-changes.md:57 | Historical regulatory direct-writer actor_role regression requires preserved accounting coverage. |
| C3 | src/core/src/zava_forward/core/regulatory_chat.py:326 | Branch records actor_role in direct repository writes. |
| C4 | src/core/tests/test_scenario_manifest.py:21 | Manifest validation verifies current public fixture bindings. |
| C5 | .github/workflows/src-ci.yml:75 | CI runs package tests, Ruff/check-format and mypy; API has isolated browser harness lint. |

Main-version evidence: regulatory_chat.py at origin/main 3e742ef1, lines
144-186 (bounded audit read), 382-398 (paired writer), 467-528 (referral).

## Findings, Alternatives and Decision State

Accept surgical composition of main audit/referral with branch actor roles.
Reject whole-file choice for regulatory_chat for the concrete losses above.
Accept main rubric/scenario copies per explicit caller direction. Preserve
both log/index contributions; no approval or historical result is rewritten.

## Open Questions, Risks and Further Research

Hosted CI on the rebased head cannot run without coordinator publication.
Required independent/human and complete publication gates remain distinct.

## Planning Readiness

Ready. Research disposition: executed. Q1-Q3 answered at this scope. Hosted
acceptance remains unavailable until coordinator push; this is not a local
implementation blocker. Self-check: three ordered inline waves, evidence,
alternatives and constraints recorded, no source changes during Research.
