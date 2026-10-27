---
title: PR 429 main refresh research
description: Focused evidence for an isolated documentation-only rebase
ms.date: 2026-10-27
---

## Research Brief

Task identity: pr-429-main-refresh-2026-10-27; slug: pr-429-main-refresh.
Researcher: RPI parent. Output mode: convergence. Posture: focused (bounded
caller request). Audience: PR owner and independent reviewers.
Evidence root: .copilot-tracking/. Status: Complete.

Research how to replay PR #429 onto current main without losing either side,
reusing its documentation checks and preserving original adverse Review
outcomes. Source edits, Azure, uv, secrets, issue closure and merge are excluded.
The caller explicitly requests all four RPI phases, an isolated worktree,
branch-only force-with-lease publication and exact-head mergeability reporting.
No automatic-mode switch is needed: all four manual phase advances are explicit.

## Research Parameters and Direction Controls

* Internal candidates: topic commits, reference log/index, cut-over evidence,
  previous dated RPI records, current validation tool and repository guidance.
* External candidates: authenticated GitHub PR metadata for #429 and #439 only.
* Questions: authoritative remote head/base; overlap and preservation; exact
  prior checks; publication gates and safe remote update.
* Edits during research: evidence and workflow state only.
* Main checkout has unrelated untracked files. They will remain untouched.
  The caller-selected new worktree isolates this task.
* The named topic is checked out elsewhere with an older local head. Use a
  fresh local carrier branch tracking the authoritative remote; push explicitly
  to the named remote topic, never move the other checkout's branch.

## Extension Registry and Participation

Repository instructions apply to all task files. RPI research and documentation
skills selected for evidence and local-safe validation. Git rebase expertise is
used directly; no research worker is justified for this tightly coupled trace.
Independent plan critique and final Review are required later. Web, regulatory
research and company-role agents are irrelevant. Interaction is unavailable and
the caller's scope and exceptional-action permission are explicit.

## Prior Knowledge Gate

Read original case study, addendum, reference index and owner memory. No customer,
regulatory or operational acceptance claims need updating. Previous research is
context, not current validation. Cross-session query for the preceding seven
days found no #429/#439 session summaries.

## Research Cycle Log

### Cycle 1: Wider

Inspected local status/worktrees and live PR metadata, fetched origin, and
listed topic-only commits and changed paths. #439 merged at current main.
Reflection: the requested topic already contains original RPI evidence and a
prior rebase record; preserve these rather than relabel them.

### Cycle 1: Deeper

Inspected the historical changes report, topic-only commits and current main's
gate interface. The old topic has no topic-only merge commits. The reference
log ends differently on each side: main's #126 cost entry versus topic's #201
soak entry. Both must survive with the whole main log a byte-exact prefix.
The README modifies different task rows, so preserve both. Reflection: do not
choose an entire side of either document.

### Cycle 1: Contrarian

Checked merge inventory and rubric-only diff. There are no merge-only changes
in the current topic range; its prior integration evidence is already committed.
The final old rubric commit is solely a stale score snapshot tied to the old
head. Preserve its original Git object but omit that commit during replay;
retain current main's score and let hosted scoring reassess publication.
Historical ten broken links are not new regressions and must not motivate
rewriting append-only history. The full gate invokes Azure CLI offline Bicep;
the caller forbids Azure use. Inspect the changed-path selection after replay
and run only a non-Azure documentation tier if available; otherwise report that
gate blocked rather than run Azure or manufacture a full receipt.

### Parent Synthesis and Re-entry

C1-C3 and W1-W2 answer the bounded questions. Accept isolated rebase, exact
log preservation and explicit remote lease. Reject merge, generic force,
historical score carry-forward and rewriting old defects. No further cycle
is warranted: remaining unknowns are implementation/check outcomes, not research.

## Evidence Log

| ID | Finding | Source | Confidence |
| --- | --- | --- | --- |
| C1 | Prior preparation checked local links and heading anchors, exact main-log prefix, original topic entries and git diff whitespace; ten unchanged link defects remained on #429 | .copilot-tracking/changes/2026-10-27/docs-prs-rebase-changes.md:36 | High |
| C2 | Current main documents a new changed-path gate tier, with full gate retained separately | src/README.md:48 at 49c942b3 | High |
| C3 | Topic adds one acceptance-preparation index row and one historical log entry | docs/reference/README.md:312 and docs/reference/log.md:7399 in remote topic diff | High |
| W1 | PR #429 is open, target main, remote head ad79455a3ec2c47d935fbc3cd055555ff188bc35 and mergeability CONFLICTING | https://github.com/jmservera/ama/pull/429 retrieved 2026-10-27 | High |
| W2 | #439 merged as 49c942b33b89100c084d48a91215989e22de5887 on 2026-10-27 | https://github.com/jmservera/ama/pull/439 retrieved 2026-10-27 | High |

## Alternatives and Decision State

Rebase is caller-selected. Merge is excluded. Reusing an occupied local topic
would disturb another checkout; a fresh carrier in the requested worktree is
selected. A generic force push is excluded; lease must bind W1's original SHA.

## Risks and Readiness

Conflict resolution, remote movement, immutable log history and stale receipt
claims require exact checks. Planning Readiness: Ready. Research disposition: executed.
Current decisions: retain original RPI evidence and both task additions; use
49c942b33b89100c084d48a91215989e22de5887 as reviewed base, rechecking origin/main
before publication. Required complete-gate execution may be blocked by the
no-Azure boundary; no full-gate success is claimed. Self-check: questions,
provenance, all three waves, alternatives, constraints and handoff are recorded.

## Planning Qualification (2026-10-27)

PC-001 correctly distinguishes offline local Bicep commands from Azure service
operations. The original contrary inference above is preserved as superseded,
not a genuine gate blocker. Enforce the stricter supplied --all requirement;
no cloud operations or fallback are authorized. PC-002's claimed prohibition on
/tmp file operations is absent from the active parent instructions and rejected.
Both original critique findings and this separate disposition remain available.
