<!-- markdownlint-disable-file -->
# Changes: discovery parent refresh onto current main, 2026-11-08

Plan: [plan](../../plans/2026-11-08/parent-refresh-123-plan.md). Research: [research](../../research/2026-11-08/parent-refresh-123-research.md). Critique: [critique](../../plans/2026-11-08/parent-refresh-123-critique.md). Refs #123, #440, #128.

## Commits (all local, none pushed)

* `47c6c991fdcb7a93df5036c345187c4b140867e8`: prospective Research, Plan, details, critique and state, committed before any merge.
* `91b77b2c16cb72ec32cfb2602f8462f9a5c7e1ed` (tree `799e60044b26ca62595708ccadefbad1667c689e`): ordinary merge of `origin/main` `f548b65f4aa31eb92a2cc9cb801130e422daed7f` into the topic. Clean, no conflicts, no resolution edits. The pre-planning forecast tree `8493726d` differs only because the planning commit followed it.
* This Changes record, the author Review and the final state are committed after the merge. Their own commit identity is reported in the handoff, not here.

## Observed after the merge

* `5beb7ba7` and `f548b65f` are both ancestors of HEAD. No reset, rebase, amend or force.
* `.github/rubric/scores/latest.json` equals main: blob `6741ddd61aba2ff80cd8b7cb2f59e63cb1af7db3`, mode 100644, parses as JSON.
* Evidence pack, log and README: each pre-merge topic tip and each main tip is an ordered, multiplicity-preserving line subsequence of the merged file. No checkpoint was dropped.
* `paired_equity.py` and `test_paired_equity.py` are byte-identical to the pre-merge topic. No source, threshold, approval or requirement edit; `fairness_evidence=False` and `activation_allowed=False` unchanged.
* Main-relative scope after the merge, before these records: 175 files, +8619/-2. Non-tracking paths: evidence pack, `docs/reference/README.md`, `docs/reference/log.md`, `src/core/README.md`, `paired_equity.py`, `test_paired_equity.py`. The 2 deletions are the inherited one-line replacements. The rest are dated `.copilot-tracking` records. Tier stays FOCUSED; no SQL, security, auth, policy, infrastructure or deployment path is changed by this topic.

## Light checks (local, current source, not the selected-tier gate)

* Environment: `PYTHONDONTWRITEBYTECODE=1`, external caches under `/tmp/c0811`, `/tmp/ci764b-venv` with Ruff 0.17.1 and mypy 2.4.0, `PYTHONPATH` to this worktree; import asserted to `src/core/src`.
* 171 tests ran, OK, no skips: paired equity, journey (acceptance, building, register, store, trace, resident design), cohort evaluation, RAI release and invalidation, ranking publication and its runner. Exit 0.
* Core Ruff check passed; format check 215 files; mypy 268 source files; all exit 0.
* 27 changed JSON files parsed. `git diff --check origin/main...HEAD` exit 0.
* 90 added relative links checked in changed Markdown: 83 resolve. 7 do not, all in two inherited original child records (`2026-11-06-r10-index-pin-correction1-440-critique.md`, `2026-11-06-sensor-retained-evidence-checkpoint-440-critique.md`), which link sibling plan, details and research files without their directory prefix. Both files are byte-identical to parent `5beb7ba7` (added by parent commit `9bacb87dc`). They are preserved as original records and not edited. This is an inherited historical link defect in tracking records, not introduced here and not a functional defect.

## Not run (separate or pending)

* The selected-tier `--changed` gate, partial-receipt verification, independent exact-head review, hosted checks, offline design and requirement traces are pending at commit time; their results are emitted externally after freeze.
* API-side tests and image groups run only via the gate. No SQL Server, browser, model or cloud work.
