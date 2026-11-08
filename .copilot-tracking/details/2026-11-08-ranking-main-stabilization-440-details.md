---
title: Ranking current-main stabilization checkpoint 440 details
description: Phase details for the scoped issue 440 current-main stabilization checkpoint after the ranking publication integration merged to main
ms.date: 2026-11-08
---

## Phase 1 details: installed-package focused observations

Scratch root `S=/mnt/ama-gates/ranking-main-440-1108`. Preconditions in one command: lock holder via `fuser /tmp/ama-rpi-heavy.lock`, competing `rpi-checks`, `docker build` and test processes via `pgrep`, `df -h /mnt`, and `test ! -e "$S"`. Stop and report if any fails.

Commands, each run from `/home/azureuser/source/ama-wt/checkpoint-ranking-main-440` with `PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S/tmp PIP_CACHE_DIR=$S/pip PIP_DISABLE_PIP_VERSION_CHECK=1`:

* `python3 -m venv $S/venv`
* `mkdir -p $S/export $S/data $S/home $S/tmp && git archive HEAD src | tar -x -C $S/export`, then `$S/venv/bin/python -m pip install $S/export/src/core $S/export/src/agents $S/export/src/api` (non-editable and out of tree, so the installed distribution is what the tests import and the checkout gets no `build/` or `*.egg-info`); then `pip check` and `pip list` saved to the scratch directory, and `git status --short --ignored` must be 0 lines.
* Identity probe: `$S/venv/bin/python -c "import zava_forward.core as c, zava_forward.core.ranking_publication as p, zava_forward.core.ranking_publication_runner as r; print(c.__file__, p.__file__, r.__file__)"` run from a directory outside the worktree (`$S`) so a source path cannot shadow the install. The api module is imported the same way.
* Core: `cd src/core && PYTHONPATH=tests $S/venv/bin/python -m unittest discover -s tests -p "test_ranking_publication*.py" -q`.
* API: `cd src/api && PYTHONPATH=../core/tests:../agents/tests $S/venv/bin/python -m unittest discover -s tests -p "test_ranking_*.py" -q`.
* Agents: `cd src/agents && PYTHONPATH=../core/tests $S/venv/bin/python -m unittest discover -s tests -p "test_cohort_ranking_eval.py" -q`.

Every selector also sets `ZF_DATA=$S/data/zavaforward.json` and `HOME=$S/home`; no private dataset is read. `df -h /mnt` is recorded before the install, after it and before the API run; stop below 2 GB. Each log goes to `$S/<name>.log` with the exit code; skips are counted from the unittest summary. An import failure or wrong selector is preserved and rerun once in corrected form (both kept). The test-helper path is a path to helper modules only; the package under test must resolve to site-packages in the identity probe.

Classification of results: passing selectors are local observed installed-package evidence at `a80acada` for those test files only. They are not a full gate, not real SQL, not browser, and not live model evidence.

## Phase 2 details: traceability table rows

| Requirement or decision (document, version, blob) | Source and test targets | Class |
| --- | --- | --- |
| PRD PR-006 (0.21.0 in-review) | `ranking.py`, `ranking_publication.py`, `ranking_publication_runner.py`; core publication and runner tests | local observed (this session) plus historical receipt |
| PRD PR-007 and PR-008 | `cohort_ranking_eval.py` docstring and test; ranking function has no AI input | local observed (agents selector); live model unknown |
| PRD FR-012 with AC-015, AC-040 | runner refusal codes, sign-off problems, `ranking.reasons`; API scale tests | local observed for deterministic behaviour; AC-015 and AC-040 acceptance not claimed |
| PRD FR-054 with AC-073 | cohort evaluation, blocked on unapproved thresholds (OQ-018) | implemented unverified for approval; blocked |
| ADR 0002 decision 4 (Proposed, blob `cbe21530`) | policy file, registry, snapshot, publication runner; the implementation-status row is a dated 2026-10-08 snapshot | dated history; current contract in `src/core/README.md` |
| ADR 0003 and ADR 0006 | local-first and layout boundaries only | no change |
| BRD 0.21.0 draft | general ranking and fair-prioritisation statements only | draft, not approval |

HTTP and auth boundary rows are filled from the API wiring and policy selector output: manager-only snapshot, status and publish; non-manager 403; 409 `committed_unconfirmed`; archive storage error shape; audit actions. Record exactly which assertions the selectors made, not the source alone.

## Phase 3 details: canonical records

Pack section heading: `## Ranking publication current-main stabilization checkpoint (2026-11-08, Refs #440 #79 #1231)`, appended after the last existing section (the 2026-11-07 parent 73 checkpoint), with subsections for source and document identities, evidence observed, actual commands and outcomes, traceability, boundary findings, existing owners and comparison, not run and open gates, classification, recommendation and limitations. Use only `Refs`.

Recommendation wording must be derived from the observations: continue when the selectors pass and no new defect appears; fix only if a check fails and it is traced; propose pivot only with evidence. It must name the gates it does not satisfy: independent exact-head review, hosted CI, human and policy-owner approvals, whole 79, 1231 and 440 closure, 81, 86 and 107 expansion approvals, deployed scheduling, Legal and DPO retention, supported filesystem and crash behaviour, live model and Azure acceptance.

Retained history to cite by path in the section: the original socket-path preflight refusal and R35 and adverse records for the ranking publication (read this session: `.copilot-tracking/reviews/2026-11-08/issue-79-r33-parent-dd92-review.md` RV-001 and RV-002 name the R35 and R31 and 7990 adverse history; no tracked file in this checkout holds the original socket-path preflight refusal log, so the record states that the refusal is retained by the coordinator and its log is not read here, with no invented path) and the failed serialized `gh pr diff` as a coordinator-reported failure. Index paragraph: one paragraph in `docs/reference/README.md` after the closest existing cutover-pack paragraph naming the new section and its anchor. Log entry: appended at the end of `docs/reference/log.md` using the file's heading style `## [2026-11-08] update | ...`.

## Phase 4 details: validation commands

* `git diff --check` and `git diff --numstat origin/main...HEAD` (zero removed lines for the pack, README and log).
* ASCII check of added lines with a Python one-liner that reads `git diff -U0` output and flags bytes above 127.
* Anchor and relative-link resolution for the added pack and README text; the new heading is unique by count.
* New records: frontmatter present, no H1, JSON state parses, no Markdown link syntax in tracking records.
* `git status --short --ignored` equals zero lines.
* The focused gate and its partial receipt verification run last at the final head, with the exact base equal to `origin/main` at that moment; the result is kept in the external handoff, not embedded in tracked records.
* A grep of added lines and commit messages for closing keywords and approval wording about 79, 1231 and 440.

## Stop conditions

Identity drift (HEAD, branch, main), lock held, disk below 2 GB, a selector that needs SQL, browser or a model call, selection that expands beyond preflight, namespace and static, or a confirmed defect: stop that step, record the blocker and return through the coordinator. A blocked result is never reported as a pass.
