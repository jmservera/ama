<!-- markdownlint-disable-file -->
# Research: issue-1294 validation policy, correction C2

## Research Brief (opening state, persisted before substantive search)

* Task: bounded correction C2 for issue #1294 after the independent review of 7260826 (verdict revise).
* Purpose: confirm and plan three findings: (F1 High) fresh full behavior cycle on final source; (F2 Medium) README says every mixed change is full; (F3 Low) the runner 58-byte `--out` limit is attributed to the direct employee-chat harness.
* Scope: src/README.md, .github/copilot-instructions.md, coordinator agent file for wording consistency; read-only inspection of tools/rpi-checks.py and src/api/checks/*. Non-goals: workflow, tool, source edits; hosted CI; deleting evidence.
* Posture: focused (bounded internal task with named targets and supplied failure evidence); provenance: caller brief. Output mode: convergence. Interaction: none available (non-interactive); no questions needed.
* Extensions: instruction `.github/copilot-instructions.md` (selected, Markdown and knowledge-base conventions); skills hve-builder-tester (selected for F1 in implementation); specialists: none dispatched, waves run inline.
* Prior art read before this artifact: the independent review file and the C1 research (already in this session); disclosed.
* Questions: Q1 where does the 58-byte limit apply and what does the direct harness do with `--out` and TMPDIR? Q2 what do the three files say about mixed changes? Q3 what must a fresh behavior cycle cover?

## Evidence

### Wider wave

* C1 src/README.md:68 lead says "mixed changes take the strictest tier" (correct).
* C2 src/README.md:219 says "Any such change, any doubt and any mixed change takes the full tier" (defect: F2). The Mixed example row (src/README.md:234) shows documentation plus infra/main.bicep, strictest (full), which is correct but has no focused-plus-focused case.
* C3 .github/copilot-instructions.md:88 says "A mixed change takes the strictest applicable tier" (correct).
* C4 .github/agents/ama-backlog-delivery-coordinator.agent.md:478 says "mixed work takes the full tier if any part requires it" (correct, consistent with strictest applicable).
* C5 tools/rpi-checks.py:239-253 `admit_browser_output` applies the 58-byte limit to the runner's `--out` only because the runner sets TMPDIR to `<out>/tmp` (line 1717; comment line 94: Chromium adds a 45-byte suffix to TMPDIR within the 107-byte socket path).

### Deeper wave

* C6 src/api/checks/employee_chat_browser_check.py:399-413: direct `--out` is used only at the end to write `axe-results.json` (`output.mkdir`, `write_text`); it is not a browser temp root. The harness then calls `design_system_browser_check.main`.
* C7 src/api/checks/design_system_browser_check.py:227-238 and 257: scratch is `tempfile.TemporaryDirectory(prefix="zf-browser-", dir=scratch_parent())` where `scratch_parent` is `ZF_BROWSER_SCRATCH` (absolute, outside the checkout) or, when unset, `<checkout>/.venv` (created if missing, an untracked or ignored write into the worktree).
* C8 src/api/checks/design_system_browser_check.py:241-247: the server child env passes only PATH, HOME, LANG and bytecode variables, so TMPDIR is not passed to the app server. Neither harness file sets TMPDIR for Chromium; the browser inherits the caller's TMPDIR.
* C9 Conclusion for F3: the 58-byte limit is runner-specific. For a direct run the evidence supports no `--out` length limit. Chromium's own singleton socket path depends on the caller's TMPDIR; the runner's derivation (C5) implies a TMPDIR of at most 62 bytes, but that was not exercised directly, so the guide may advise a short TMPDIR as an unmeasured precaution only. The unlisted side effect (C7) is worth stating: set `ZF_BROWSER_SCRATCH` to an absolute path outside the checkout to avoid creating `.venv` in the worktree.

### Contrarian wave

* Counter-hypothesis: a direct `--out` could still matter. Refuted by C6: it is only the results directory.
* Counter-hypothesis: keep the 58-byte statement as a harmless safe default. Rejected: it states an unsupported requirement for a direct run and confuses the runner contract; a precaution must be labelled as such.
* Counter-hypothesis: the mixed rule is right because the repository policy says doubt takes full tier. Rejected: C3 and the owner brief say strictest applicable; two focused components stay focused unless a real risk makes them doubtful.
* F1: HVE tester correction reuse requires prior Complete and Pass with no open finding. Report 2 is Revise with an after-grade edit, so reuse is ineligible. A fresh full run (new design, execution, grading, new sandbox 2026-11-08-issue-1294-policy-3) is required. The host forbids a model override on the task tool, so the profile stays unresolved and the run a proxy; no intended-profile or native claim.

## Synthesis

* Accepted: fix src/README.md:219 to strictest applicable with focused-plus-focused staying focused and any full-tier component making the candidate full; add a focused-plus-focused example row; align the table's Mixed row label; replace the 58-byte direct-check sentence with the evidence-supported statement (C6-C9) and keep the runner-only 58-byte section intact; optionally align the coordinator wording (already consistent, no change).
* Rejected: edits to workflows or tools; reusing report 2 grades.
* Deferred: intended-profile run (host constraint); measuring Chromium socket behavior directly (no browser run authorized for wording).
* Risks: a new behavior run may find further wording defects; apply them in one batch and, because no reuse is possible, a further run would be needed; record any remaining Revise honestly instead of looping.

## Research disposition and readiness

* Research disposition: executed (inline waves; no worker dispatched).
* Planning Readiness: Ready.
