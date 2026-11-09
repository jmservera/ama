---
title: R10 queue dispatch design checkpoint 440 plan critique
description: Independent read-only critique of the plan, details and research for the seventeenth documentation-only checkpoint
ms.date: 2026-11-06
---

## Scope and execution

* Execution status: Complete.
* Inputs: plan, details and research for task `440-r10-design-checkpoint` (paths under `.copilot-tracking/`), the caller constraints, and four read-only checks at HEAD `c582e44b199a` (pack headings, README anchors, 136 ref, design blob).
* Not performed: any research beyond the supplied inputs, any test, SQL, browser or container run, and any re-read of the R10 design body.

## Verdict

Verdict: Revise. The plan is credible and safely scoped, but five planner-owned corrections are needed so acceptance criteria are verifiable and the text cannot overclaim.

## Verified facts

* Last `##` heading in the pack is Sixteenth (line 4666), with `###` Provenance qualifications as the final subsection; no Seventeenth heading exists. FR-1 allocation holds.
* Local ref `feat/infra-hosting-integration-136` resolves to `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`.
* Design blob at `1e19209985d9` re-resolves to `de776799aafc925c372c6c1c85e0c72ecc75b389`.
* README line 452 already ends the fourteenth-to-sixteenth paragraph with the sixteenth anchor, so P2-T1 has a valid insertion point.

## Findings

### PC-001 Medium: append-only claim is unverifiable as written (AC-1, P3-T1)

* Related: AC-1, FR-2, P3-T1.
* Issue: the pack ends with a Sixteenth `###` subsection, and README sentence insertion is "at the end of the existing index paragraph". A mid-paragraph edit shows as one changed line (a deletion plus an addition) in `git diff`, contradicting "only additions".
* Action owner: planner.
* Resolving evidence: AC-1 wording changed to "`git diff --numstat` shows zero deletions for the pack and log; the README shows one modified line whose old text is a strict prefix of the new text", or the sentence is added as a new paragraph so zero deletions hold everywhere. Check `git diff --numstat` per file.
* Direct apply: yes.

### PC-002 Medium: "31 earlier RPI records" count is unsupported (AC-1, Executive summary)

* Related: AC-1, P3-T1.
* Issue: no input enumerates 31 records. `.copilot-tracking` holds many more files for task 440 (about 61 date-and-440 matches in the working tree), and the research does not list them.
* Action owner: planner.
* Resolving evidence: P3-T1 defines the set by command (for example `git diff --name-status c582e44b199a -- .copilot-tracking` shows only `A` rows for new 440-r10 files, and none of M, D or R), and drops the fixed number or states how it was derived.
* Direct apply: yes.

### PC-003 Medium: timing and observation claims risk repeating the corrected labels (Research, P3-T2)

* Related: research "about 14:05Z", P3-T2, Prospective ordering.
* Issue: the prior checkpoint needed a correction for unobserved time labels. The research quotes "2026-11-06 about 14:05Z" and the root critique times "13:50:29 to 13:51:53" as facts. The checkpoint should not copy either as its own observation.
* Action owner: planner.
* Resolving evidence: an explicit rule in P1-T2 that the pack section carries no clock time except one taken from actual command or tool-boundary output captured in the Changes record, and that root-supplied times are labelled "per root assessment, not independently observed".
* Direct apply: yes.

### PC-004 Medium: approval-overclaim controls rely on a self-check (AC-4, P1 Done-when)

* Related: AC-4, FR-1, "Done when the section contains no sentence implying approval".
* Issue: this is a judgement, not a check. Words such as "accepted", "closed", "resolved", "Pass" and "approved" occur legitimately (owner CODE decisions resolved, ADR 0003 accepted, critique "closed" coverage) and can be misread as design approval.
* Action owner: planner.
* Resolving evidence: add a scripted grep of the appended text for `approv|accept|closed|resolved|Pass|ratif` and require each hit to be in the same sentence as one of: Proposed, DRAFT, unapproved, code-role authority only, historical, or a quoted prior status. Also require a literal sentence that the draft design, this checkpoint and its recommendation are not approved by any owner, role or ADR.
* Direct apply: yes.

### PC-005 Low: anchor collision and slug risk (AC-2, P2)

* Related: AC-2, P2-T1, P2-T2, FR-4.
* Issue: GitHub slugs for headings carrying `(date, Refs #440 #144 ...)` drop punctuation, as the existing anchors show. A heading that repeats text with a subsection title (for example another `### Trace`, `### Findings`) creates duplicates: the Sixteenth section already has `### Trace` and `### Gaps, owners, recommendation`, so a new `### Trace` yields a `-1` suffix slug. The plan lists subsections but not their names.
* Action owner: planner.
* Resolving evidence: P1-T2 names the new subsections with a distinguishing prefix or suffix and fixes the section heading text before writing; P3-T1 computes the slug with the existing anchors as the pattern and greps for a unique heading count; links in README and log use that slug.
* Direct apply: yes.

### PC-006 Low: topology statement could overclaim or be stale (Research Finding 3, caller constraint)

* Related: P1-T2 Pins table, FR-3.
* Issue: the local-ref observation is a point-in-time fact in a shared repository where the ref could move or be deleted. The reflog message "Created from origin/main" is the evidence for "created from main"; the plan does not say to record the exact commands and results in the Changes record, nor to say "as observed at the time of the check, not a guarantee".
* Action owner: planner.
* Resolving evidence: P3-T1 re-runs `git rev-parse`, `git reflog show` on the ref, `git ls-remote --heads origin` and `gh pr list --state all --head`, and the text says "observed, not authorization, ancestry or approval".
* Direct apply: yes.

### PC-007 Low: AC-3 and fetch scope (AC-3, P3-T1)

* Related: AC-3, P3-T1.
* Issue: AC-3 requires "fresh" confirmation of main and governance pins but main may advance during the turn. The plan has no rule for a pin mismatch (the checkpoint must then record the new value and not silently keep the old one) and no statement that fetch updates only remote-tracking refs (no branch creation or publication).
* Action owner: planner.
* Resolving evidence: add "if a pin differs, record both and re-verify blob identities" to P3-T1.
* Direct apply: yes.

### PC-008 Low: critique disposition and process ordering (Critique Disposition, P4)

* Related: Critique Disposition, P4-T2.
* Issue: the plan says the planning commit precedes canonical edits, but the caller constraint forbids publication. P4-T2 commits locally; a statement is needed that the commit is local only, with no push, PR or board write. AC-5 also needs the `git status --short --ignored` result to be quoted, not only asserted.
* Action owner: planner.
* Resolving evidence: P4-T2 says "local commit only; no push" and the Changes record quotes the final status output.
* Direct apply: yes.

## Missed items

* Design provenance: the design file's own status (DRAFT, unapproved, unconsumed) and its 15360-byte size should be re-resolved with `git cat-file -s` alongside the blob (PC-005 evidence pattern), since the size is only supplied.
* Evidence-label legend: the pack section should define Proposed, Approved (code-role only), Observed, Implemented-unverified, Unobserved, Deferred in one place so later readers cannot read "Approved" as design approval. This is covered by PC-004 and is a planner correction.

## Acceptance coverage

* AC-1: revise per PC-001 and PC-002.
* AC-2: verifiable once PC-005 is applied.
* AC-3: verifiable with PC-007.
* AC-4: verifiable with PC-004.
* AC-5: verifiable with PC-008.

## Highest-impact finding

PC-004 (approval-overclaim control is a judgement, not a check). Owner: planner. Smallest action: add the scripted hit-by-hit grep and the literal not-approved sentence. User response required: no.

## Next Steps

No user action is required. The planning parent applies PC-001 to PC-008 directly, records dispositions in the plan, and proceeds without another critique.
