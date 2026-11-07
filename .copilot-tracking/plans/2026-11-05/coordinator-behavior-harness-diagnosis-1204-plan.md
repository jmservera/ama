<!-- markdownlint-disable-file -->
# Plan: harness correction for the issue 1204 behavior evidence

* Task: 1204-behavior-harness-diagnosis. Written 2026-11-05 after the research record and before any harness edit. Research: [coordinator-behavior-harness-diagnosis-1204-research.md](../../research/2026-11-05/coordinator-behavior-harness-diagnosis-1204-research.md). Details: [coordinator-behavior-harness-diagnosis-1204-details.md](../../details/2026-11-05/coordinator-behavior-harness-diagnosis-1204-details.md).
* Status: plan only. Paused for the coordinator; no model call, archive, move or prune has run. Unpublished candidate retains the eighth assignment.

## Scope and exclusions

* Harness and evidence only. The target agent file (blob acefb44a4d254ede6d86413343127b763dec42cb), its frontmatter and the tools configuration stay unchanged and opaque. No source edit, no new automation, no tools edit.
* Preserve unchanged: original Revise report 003, the independent grade, all raw outputs, test log and test review, pass 5 normalized transcripts, cbebe objects and backup refs, /tmp/h1204.
* Heavy lane belongs to runner 2306020 for #185: no rpi-checks, lock, SQL, browser, scanner, image or cloud work.

## Decisions

| ID | Decision |
| --- | --- |
| D1 | Reuse eligibility: report 003 is Revise, so it is not eligible for correction-run reuse. Prior grades are historical observations only. |
| D2 | Rerun scope: a full run per canonical Flow step 3 for any run that claims Pass (fresh design with new stable IDs, full execution, fresh independent grading). A reduced discriminating-only run is labelled Partial and cannot support Pass. Root chooses; recommended order is Phase A (Partial, narrow) then Phase B (full) only if A shows discrimination. |
| D3 | No behavior-source change. If a rerun shows the real source failing a pair, that is a later, separately authorized correction, not part of this plan. |
| D4 | Intended Automatic profile is already approved: request `--model auto`, record the actual auto-selected model per run, autoTier unknown. No re-ask, no new model setting, no stronger claim. |
| D5 | SC-14: record the overstatement qualification (Low); do not regrade and do not require ceremonial gate restatement. |

## Phases

### Phase 1: provenance and activation proof (harness)

* Each executed copy gets a preflight before its scenarios: one read-only call asking the agent to quote verbatim, from its own instructions, the sentence that defines the total session limit and the sentence on blank ahead-count. The lead compares the quote to the copy with an exact string match. A mismatch stops that lane (Deferred or Not available), not a silent pass.
* Record per copy: sha256, git blob, cwd, CLI request, selected model line, exit code. Keep the cwd a minimal fixture containing only the one agent file.
* Controls are coherent contradictory mutations built in /tmp scratch copies only (design in details, P1 to P3), each with its exact diff recorded and the mutant's remaining text checked for internal consistency before use.

### Phase 2: leak-free, source-dependent cases

* Design by a fresh generic designer (harness default model) that returns content only. Cases omit the figure or fact the source must supply (P1 no cap stated; P2 no statement about behavior evidence; P3 only the blank output). A sibling non-agent case must behave the same under real and mutant.
* Directional expectations (real versus mutant) are recorded by the lead in run-state before execution, outside the executor input. The executor sees only the wrapper and scenario text.

### Phase 3: independent grading and persistence

* Designer and grader return the complete content as the final message and create or modify no file. The lead writes sandbox files, including the grade body verbatim and then the review. The earlier grade-report.md written by the grader stays, with a deviation record.
* Each control run is graded independently, including any control the lead ran. A grader sees logs, design, requirements and rubric only.

### Phase 4: evidence storage without waiver

* Do not edit raw bytes, normalize, add gitattributes exemptions or suppress the check. Do not move or remove anything in this plan.
* Proposal for root approval (finite, per-run): archive exactly the 69 committed files under `raw/` (path, type regular, size, sha256, 289,471 bytes total) plus the full `.copilot-tracking` snapshot (tracked, untracked and ignored; symlinks recorded as identities, never followed) into an owner-only tar.gz outside the checkout under `~/.local/share/ama/tracking-archives/<date>-issue1204-raw-<id>/`, with `receipt.json`. Verify full readback, restore the selected members into a new empty external directory, compare hashes, and re-check protected bytes (source blob, report 003, grade, review, cbebe and /tmp/h1204 originals).
* Only after root approval and a passing restore proof, a NEW commit (never an amend) may replace the 68 plain-text transcript files in the checkout with one binary archive member plus a text manifest, which is lossless and does not relax `git diff --check`. The original commit stays reachable. If root declines the replacement, the range `git diff --check` keeps failing and the candidate cannot meet that focused check; this is recorded as an open gate, not waived.
* New runs write raw transcripts to external scratch and commit only a manifest (path, size, sha256) plus compact extracts, per the policy default.

### Phase 5: focused checks and handoff

* After any future tracked change: direct-exit `python3 -m unittest test_backlog_sync test_rpi_checks` from tools (97 expected) with external caches and no bytecode; `git diff --check origin/main..HEAD` (range form) with actual exit; source blob equality; frontmatter, ASCII and local-link checks. No rpi-checks.
* The earlier 97-test run predates the last commit; it is not exact-head proof and must be rerun at the final head.

## Expected discrimination

* P1: real admits, mutant refuses. P2: real holds the agent change, mutant publishes; backend sibling publishes in both. P3: real treats blank as Unknown and keeps the slot, mutant releases and admits. Any pair where real and mutant do not differ in the expected direction is recorded as no discrimination, not tuned after the fact; goalposts are not moved and the old Revise is not regraded.

## Self-critique (single pass, not independent)

* Risk: a model's general knowledge may still follow the real rule under a mutant. Mitigation: P1 depends on a number only the source holds; P2 and P3 invert the rule coherently and are checked for contradictions left behind.
* Risk: Auto may route different models per run. Recorded per run; no pinning.
* Risk: preflight quoting could prime the agent. Mitigation: the preflight runs as a separate call, not in the scenario session.
* No conflict with a confirmed owner decision found; no finding rejected.

## Resume point

Phase 1 requires root consumption of this diagnosis, then a root decision on D2 (Phase A Partial first, or direct full run) and on Phase 4 approval. Until then no paid CLI call and no storage change.
