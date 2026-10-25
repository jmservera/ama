---
title: PR 448 Code Comment Research Lane
description: Focused read-only evidence for unresolved code-related PR feedback
ms.date: 2026-10-25
---

## Delegated Research Contract

* Cycle / wave: proportional Wider -> Deeper -> Contrarian.
* Lane: hybrid, focused code evidence research for PR 448.
* Purpose: distinguish surviving defects, comments on deleted or moved paths, and risks transferred to the private study kit. This is not a formal security assessment or full independent review.
* Questions:
  * Does `anc/check_paper.py` still require an unreachable historical baseline before structural checks?
  * Which unresolved protocol-check comments remain applicable to the retained harness?
  * Does the retained experiment-design example have concurrent log or rollback hazards?
  * Were comments on the removed `anc/consolidation-mve-kit/` transferred elsewhere, rather than resolved by removal?
* Scope: only named feedback surfaces and their directly owning code at PR head `a2b80b184ae3eec059aa4b83eb49c28d3bf61432`, base `df3e9643c1cf20b2fe143ad73819b3b8b393b003`, and available local snapshot evidence. No source, manuscript, README, protocol, experiment-kit, parent report, Git, GitHub, or review-thread changes.
* Non-goals: implementation, approval decisions, full private-kit review, security assessment, experiment execution, and DLP or live-result inspection.
* Evidence criteria: every material claim records snapshot, source location, check and observed result, confidence, and uncertainty. Prefer exact Git objects; if unavailable without fetch, record the gap.
* Limits: focused analysis only; no destructive rollback execution, no dependencies or fixtures outside this evidence root, and no writes outside this file.
* Initial status: investigating.

## Initial Preflight

The approved lane path is under `docs/capstone/thought-leadership/everything-but-the-software/anc/`, and is distinct from the read-only parent record `docs/capstone/thought-leadership/everything-but-the-software/anc/revision-report.md`. The requested lane file did not exist before this creation. The local committed HEAD supplied by the caller is `7e49697ab64d1e1a921805a7aa0520d4a2865bcc`; actual HEAD remains to be recorded only if available through a permitted read-only evidence operation.

## Investigation Log

| Wave | Action | Result | Next condition |
| --- | --- | --- | --- |
| Wider | Created bounded evidence record and opened supplied review-comment snapshot. | The lane file was absent; the parent record is distinct. | Extract unresolved threads 5-20 and 22-24, then locate named surfaces. |
| Wider | Read supplied comment JSON and enumerated the local ancillary tree. | Unresolved indices 5-20 and 22-24 comprise one retained checker, one retained historical checker, one retained shell example, a README completeness claim, and comments on absent `anc/consolidation-mve-kit/` paths. | Inspect the three retained code surfaces and their direct references. |
| Deeper | Read `check_paper.py`, `protocol_checks.py`, the retained harness documents, README, and saved check output. | The baseline subprocess is mandatory and precedes all structural checks; the protocol directory now exists, but its check accepts absent context/vetting notes and is explicitly labelled historical; the TCR example has both a fixed shared log and commit-failure rollback bypass. | Seek counter-evidence for later correction or transferred private-kit fixes within the permitted evidence. |
| Contrarian | Searched the retained proposal for unique-log cleanup and rollback patterns, checked checker exception handling, and compared README scope wording. | No `mktemp`, exit trap, baseline exception handling, or retained old-kit path exists. README narrows the ancillary proposal to historical material and redirects execution to the private tagged kit. | Lane criteria met; private-kit disposition remains outside available evidence. |

## Findings

### F1: Historical baseline blocks all structural validation

* Comment applicability: index 5 remains live in the locally inspected ancillary source. `BASELINE = "0d5dcb02"` is fixed at `anc/check_paper.py:17`. `main()` invokes `git show <baseline>:<main.tex>` with `check=True` at `anc/check_paper.py:69-74`, before the count, citation, label, environment, brace, abstract, result-switch and optional LaTeX checks at `anc/check_paper.py:75-146`.
* Concrete reproduction by control-flow inspection: when the object is absent, `subprocess.run(..., check=True)` raises `CalledProcessError`; no `try` block exists, so the following structural checks cannot run. This is deterministic from the inspected source; no Git command was run under the lane restriction.
* Supporting context: the saved output reports a prior successful structural run, including `PASS structural checks`, at `anc/revision-checks.out.txt:1-31`. It does not demonstrate availability in a source archive, shallow clone or post-squash clone.
* Confidence: High for the local source behaviour; Medium for applicability to PR head because exact-object inspection is unavailable in this lane.
* Uncertainty: the permitted read-only tools do not expose local Git object lookup or the PR head file; no fetch or GitHub read operation was performed.

### F2: Protocol-check path comment is obsolete, but the retained checker has bounded false-negative and false-positive risks

* Comment applicability: index 14's stated missing-directory failure is contradicted by the retained local layout. `PROTOCOL` targets `anc/mve-feature-consolidation-harness` at `anc/protocol_checks.py:10`; that directory and `experiment-design.md`, `hypotheses.md`, and `mve-plan.md` are present in the inspected tree. The saved output records `PASS protocol consistency checks` at `anc/revision-checks.out.txt:20-31`.
* Current false-negative: under `--check-documents`, `context.md` and `vetting.md` are optional: absent files only print `UNAVAILABLE` at `anc/protocol_checks.py:40-45`; the required-fragment loop skips each absent source at `anc/protocol_checks.py:53-58`. Yet the plan says details live in those files at `anc/mve-feature-consolidation-harness/mve-plan.md:4`, and the design names `vetting.md` as mitigation material at `anc/mve-feature-consolidation-harness/experiment-design.md:216`. Thus a PASS cannot establish the advertised package is complete.
* Current false-positive/staleness risk: the checker hard-codes the historical four-run/eight-feature A/B assumptions at `anc/protocol_checks.py:19-28` and asserts first-pass fragments at `anc/protocol_checks.py:47-55`. The README now explicitly classifies it as historical and says it does not check the current ten-feature A/B/C design at `README.md:27` and `README.md:154-157`. A current-design document could therefore fail this legacy agreement check without indicating a current-design defect.
* Confidence: High for current local checker semantics; Medium for PR-head identity.
* Uncertainty: no current private study-kit checker was inspected.

### F3: Retained TCR example still corrupts concurrent diagnostics and does not meet its stated commit-or-revert invariant

* Comment applicability: index 23 remains live. The plan permits four parallel sessions at `anc/mve-feature-consolidation-harness/experiment-design.md:188`, while every invocation redirects `make test` to `/tmp/tcr.log` at line 141 and reads it after failure at line 144. Shell redirection truncates this fixed path before each `make test`, so concurrent invocations can overwrite another invocation's diagnostic file. This conclusion follows from the literal shell control flow; no concurrent process was launched.
* Transferred/retained rollback issue: index 6 was attached to the removed kit, but the same pattern survives in the retained example. The `if` condition contains only `make test` at line 141; `git add -A && git commit ...` is in the success body at line 142. Failure of either Git command bypasses the `else` at lines 143-144, leaving the worktree unchanged from the attempted refactor and contradicting line 129's promise to commit or revert. No destructive rollback wrapper was run.
* Confidence: High for both shell control-flow conclusions; Medium for PR-head identity.
* Uncertainty: this is an earlier proposal, not the authoritative private study kit, as the README states at `README.md:24-27` and `README.md:170-176`.

### F4: Removed-kit findings were not resolved by deletion in this repository

* Comment applicability: indices 6-13 and 15-20 target `anc/consolidation-mve-kit/` files. The focused ancillary file enumeration returned no such path; the only retained harness files are the four proposal documents under `anc/mve-feature-consolidation-harness/`. The supplied PR comment JSON is the provenance for the original paths and issue descriptions.
* Result: removal means the old code is not locally executable or reviewable as part of this package. It does not, by itself, provide counter-evidence that the analyzer interval, host-import, pytest collection, empty-suite, consent, egress, generated-report, or stale-protocol concerns were fixed in the private study kit.
* Scope boundary: `README.md:170-176` directs execution to a separate tagged private kit and states the local MVE copies are earlier proposals. The authorized private snapshot `0a4f6e1294282dca9b86a735417b10937a373b45` was not accessible through the permitted read-only tools in this lane; it was not reaudited.
* Confidence: High that the named old paths are absent from the inspected local ancillary tree; Unavailable on their private-kit disposition.

### F5: Package-completeness comment remains materially supported for the historical proposal only

* Comment applicability: index 22 is supported for the retained historical proposal. The procedure references three `harness/*.prompt.md` files at `anc/mve-feature-consolidation-harness/experiment-design.md:81-83`; the plan refers to `context.md` and `vetting.md` at `anc/mve-feature-consolidation-harness/mve-plan.md:4`; focused search found references but no corresponding files in the ancillary tree.
* Limitation: README.md:170-176 correctly redirects execution to the separate tagged private kit and identifies these as earlier proposals. Therefore this is a documentation/package-completeness defect for the historical ancillary materials, not evidence that the private kit itself is incomplete.
* Confidence: High for the local package; Unavailable for the private kit.

## Evidence Relationships

| Question | Relationship | Provenance |
| --- | --- | --- |
| Baseline reachability | Supports index 5: unavailable baseline aborts all subsequent structural checks. | `anc/check_paper.py:17,69-146`; `anc/revision-checks.out.txt:1-31` |
| Protocol path | Weakens index 14's original missing-directory statement, but supports a newer bounded completeness/staleness concern. | `anc/protocol_checks.py:10,40-58`; `README.md:27,154-157`; retained harness files |
| Parallel TCR diagnostics | Supports index 23: a single `/tmp/tcr.log` is shared by planned parallel sessions. | `anc/mve-feature-consolidation-harness/experiment-design.md:141-144,188` |
| Commit rollback | Supports transferred index 6 concern in the retained TCR example. | `anc/mve-feature-consolidation-harness/experiment-design.md:129,141-144` |
| Removed-kit code concerns | Leaves unresolved in the private kit; deletion locally is not a fix verification. | supplied PR comment JSON; local ancillary enumeration; `README.md:170-176` |

## Per-Comment Applicability

| Unresolved index | Comment surface | Applicability in inspected package | Evidence disposition |
| --- | --- | --- | --- |
| 5 | `anc/check_paper.py` baseline | Live. | Supported by F1. |
| 6 | Removed-kit TCR rollback | Old path absent; equivalent rollback shape survives in historical proposal. | Supported for retained example; private-kit transfer unverified. |
| 7 | Removed-kit shared TCR log | Old path absent; equivalent fixed log survives in historical proposal. | Supported for retained example; private-kit transfer unverified. |
| 8 | Removed-kit interval verdicts | Old path absent. | Unresolved in private kit; not reaudited. |
| 9 | Removed-kit host import boundary | Old path absent. | Unresolved in private kit; not reaudited. |
| 10 | Removed-kit pytest collection errors | Old path absent. | Unresolved in private kit; not reaudited. |
| 11 | Removed-kit empty-suite acceptance | Old path absent. | Unresolved in private kit; not reaudited. |
| 12 | Removed-kit interval analyzer | Old path absent. | Unresolved in private kit; not reaudited. |
| 13 | Removed-kit consent contradiction test | Old path absent. | Unresolved in private kit; not reaudited. |
| 14 | `anc/protocol_checks.py` missing directory | Not live as stated. | Weakened by F2; current historical-check limitations remain. |
| 15 | README continuation path | Not an executable-code finding. | README now directs execution to private tagged kit; no source edit assessed. |
| 16 | Removed-kit duplicate stale protocol | Old path absent. | Unresolved in private kit; not reaudited. |
| 17 | Removed-kit agent egress | Old path absent. | Unresolved in private kit; not reaudited. |
| 18 | Removed-kit consent suite setup | Old path absent. | Unresolved in private kit; not reaudited. |
| 19 | Removed-kit Ruff failure handling | Old path absent. | Unresolved in private kit; not reaudited. |
| 20 | Removed-kit generated-report metric | Old path absent. | Unresolved in private kit; not reaudited. |
| 22 | Historical proposal assets absent | Live only as historical-package completeness. | Supported by F5; README limits its operational claim. |
| 23 | Historical proposal shared TCR log | Live. | Supported by F3. |
| 24 | Parent revision-report count | Outside delegated code lane and read-only parent record. | Not assessed. |

## Checks Run and Limits

* Ran read-only source and structured-text inspections only. The saved historical output at `anc/revision-checks.out.txt:1-31` was read; no checker, experiment, rollback wrapper, Git command, network operation, dependency installation, fixture creation, or private-kit inspection was run.
* The supplied comment JSON was read at `/home/jmservera/.vscode-server/data/User/workspaceStorage/b4147410cf313d23a2875c7fbc83acc3/GitHub.copilot-chat/chat-session-resources/d8cad357-804b-4303-af3e-1acddb098dfe/call_8vrodnuwhdnPQVqgnohe0num__vscode-1792862512847/content.json` on 2026-10-25.
* Exact PR base/head object reads and actual local HEAD verification are unavailable through this lane's permitted read-only tool set. Therefore the results are anchored to the supplied PR-comment snapshot and the current local ancillary files, not asserted as an exact checkout of `df3e9643c1cf20b2fe143ad73819b3b8b393b003`, `a2b80b184ae3eec059aa4b83eb49c28d3bf61432`, or local `7e49697ab64d1e1a921805a7aa0520d4a2865bcc`.

## Stop Decision

Status: complete within the focused lane. Wider identified surviving versus absent surfaces; deeper inspected each locally surviving code path and direct documentation contract; contrarian checks found no local counter-fix and established the README's private-kit boundary. Further investigation would require the exact PR Git objects or authorized private-kit snapshot, which are outside the available evidence path and would widen this lane.
