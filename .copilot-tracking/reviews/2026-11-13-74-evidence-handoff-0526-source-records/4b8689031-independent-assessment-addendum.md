---
title: Evidence addendum, independent exact-head assessment, #74 home building applicability display
ms.date: 2026-11-13
---

Addendum to `2026-11-13-74-home-building-applicability-display-independent-assessment.md` (commit `c3aecd946`, preserved unchanged). Candidate unchanged: `f50c5c7fdd179e4d3c187130afbdf1e369983992`, tree `65e39a2821c95f13a9a5375ab5bea633688273ef`, base `15bfee2d7f6ae9b73d24c51d3dbbea7c7b78f626`. Reviewer ran nothing; Refs #74 only.

## What the transcript was read for

Read `rpi-74-initial-applicability-0458.log` (545 lines, author's native session transcript, local synthetic UI/unit only). Not read: `rpi-149-final-ai-0104.log`, `.env`, private data, raw SQL. No other result paths are named in it.

## What it actually supports

The transcript retains the commands, the order and the tool-call headings with line-count and duration stubs (for example "28 lines… 9s"). It does NOT retain the command outputs. A search for node-ok, `Ran N tests`, exit codes, `passed` and `COMPLETE:` found no output text. Supported as commands run (not results):

* Red-first: a browser-check edit adding the three scope rows and assertions was run before any `app.js` edit (transcript: "Red before the change"), with the first assertion text "does not establish".
* Node `--check`, Ruff check/format, mypy and `tests.test_home_case_api -q` were invoked in one batch with the default `PYTHONPATH=../core/tests:../agents/tests` (editable install). A following command printed the `zava_forward.api` `__path__` and grepped the unittest `FAIL:` block: this is the adverse wrong-source observation (the editable install resolves to another checkout). The author's later claim of one unrelated 404 is consistent with that step but its output is not retained.
* A rerun used `PYTHONPATH=$W/api/src:$W/core/src:$W/agents/src:$W/core/tests:$W/agents/tests` with `W=$(git rev-parse --show-toplevel)/src`, and printed `zava_forward.api.server.__file__` first. That is the command that would establish worktree provenance; the printed path is not retained.
* Two debug runs printed the rendered text to find a mismatch, then `sed` changed the asserted text to "do not establish" (matching the final source). So an earlier red/failure was caused by the check's own wording, which is the invalid red the author describes, and the first "red before the change" cannot be treated as a valid base-red.
* A later run stashed `app.js` and ran the browser check, then popped. A final run reverted `app.js` with `git checkout`, ran the check (`tail -2`), re-applied the saved patch, and counted `PASS` lines. This is the pair that would constitute valid base-red and candidate-green. Its outputs (failing check name, PASS count) are not retained.
* The Ruff format, Ruff check and mypy after the final type-fix edit ran only in the batch before `git checkout`; no outputs retained. The final edited check file is the committed one only by the author's later commit, not by output.
* `flock -n /tmp/ama-rpi-heavy.lock` is on every browser command (nonqueued). Retained: the command form. Not retained: whether the lock was acquired (a failed `flock -n` would have produced no run and a non-green result).

## Corrected scope of the prior Pass

* The prior Pass stands for the static diff, source contract and design review. Its evidence section already said test results were author-reported; this addendum narrows it further: the transcript does not independently corroborate any numeric or pass/fail result. Node, Ruff/format/mypy, six API tests (source provenance via worktree `PYTHONPATH`), valid base-red, candidate-green, no-JS-error and no-write claims all remain AUTHOR-REPORTED, with commands but no retained outputs or exit codes.
* The wrong-source 404 and invalid red remain adverse observations that happened and are not baseline failure; they are not erased by "discarded". They also show the first red was caused by assertion wording, not the base code.
* The plan's ticked API-regression checkbox is a disclosed attribution limitation. No unit test was added; none is claimed.

## Gaps

* Exact gap: no retained output, exit code or `__file__` provenance line for any of the checks, and no retained red failure text. The red-on-base and green-on-candidate claims rest on the author's summary.
* Not retained: axe (skipped by design, `ZF_AXE_JS` unset).

## Fresh no-execution verdict

* Static/design verdict: Pass, unchanged.
* Executed-behaviour verdict: Not independently evidenced. The claim of a valid red/green is plausible from the command sequence and from the assertion logic, but unproven by retained results.
* Publication blocker for the FOCUSED tier: none from source defects. A precise evidence gap remains. Before publication, either obtain exact-head hosted CI (the browser check is local-only, so CI may not cover it) or a retained reviewer-run, or have the PR text state browser red/green as author-reported without retained output. Do not cite it as verified.
* Unchanged limits: no source approval, no human/AT/WCAG acceptance, axe skipped, no AC tick or closure, G5 optional and owner-unconfirmed, prior non-blocking label/`translate`/README observations stand.
