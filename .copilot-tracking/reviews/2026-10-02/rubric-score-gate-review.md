<!-- markdownlint-disable-file -->

# Review: rubric-score-gate

* Task ID: 2026-10-02-rubric-score-gate
* Plan: .copilot-tracking/plans/2026-10-02/rubric-score-gate-plan.md
* Changes: .copilot-tracking/changes/2026-10-02/rubric-score-gate-changes.md
* Review type: one-pass, read-only acceptance review (no re-review in this task)
* Reviewed: `.github/workflows/rubric-score.md`, `.github/workflows/rubric-score.lock.yml` (jobs `rubric_prepare`, `agent`, `record_rubric_score`, `conclusion`, activation checkout), `.github/rubric/{rubric.json,artifacts.json,scores/latest.json,README.md}`, `.github/rubric/scripts/{prepare.py,gate.py,test_gate.py}`, rubric guide and seed source
* gh-aw runtime behaviour checked against `github/gh-aw` sources (`restore_base_github_folders.sh`, `save_base_github_folders.sh`)

## Outcome

**Non-conformant.** One High finding (RV-001) defeats G2 and FR-8: a pull request that deletes, moves out of the glob, or oversizes a scored artifact file cannot lower the score, so it passes and is approved. Fix RV-001 before relying on the gate. Medium findings RV-002 to RV-004 should be fixed or verified in the first live run. The rest are follow-ups.

## Verified as correct

* Seed baseline equals the manual review per criterion: A 4,5,4,1,2,3,2 = 21; B 4,3,1,2,1,4,4 = 19; C 5,2,5 = 12; D 4,4,1 = 9; total 61, floors not met (AC-2).
* Floors (60% per section, no criterion at 1) and bands (66, 78, 90) match `ama-capstone-assessment-guide.md` L114-L136; floor check precedes band.
* `evaluate()` fails closed on agent failure, detection failure, zero or multiple tool calls, invalid JSON, missing or unknown criteria and out-of-range or boolean scores (NFR-5). Carry-forward of closed criteria and the changed-file evidence rule work as specified for edited files.
* Baseline, rubric and registry are read from `origin/main` via `git show`; `manual-seed` bootstrap is honoured only from the base ref (NFR-2, PC-002).
* No `${{ }}` expression is interpolated inside a `run:` script or `github-script` body in the source or the compiled lock file. `github.head_ref` reaches shell only through `env: HEAD_REF` and is quoted; in `checkout.with.ref` it is not shell-evaluated.
* Gate job checks `needs.detection.result` itself, so a failed detection cannot produce a pass even though the compiled `if:` does not require detection success.
* `python3 /tmp/rubric-tools/gate.py` puts `/tmp/rubric-tools` on `sys.path[0]`, so PR files cannot shadow stdlib modules.
* All jobs that run three-dot diffs use `fetch-depth: 0` and fetch `main`; `Path.glob` patterns in `artifacts.json` (`docs/brds/**/*.md`, `src/**/*`) behave as intended; `fnmatch` excludes match across `/` as intended.
* AC-1, AC-3, AC-4, AC-5 and AC-6 are met (AC-6 with the caveat in RV-011).

## Findings

### RV-001 High: Removing or hiding an artifact file cannot lower the score

* Files: `.github/rubric/scripts/prepare.py` L64-L80, L159-L165; `.github/rubric/scripts/gate.py` L135-L137
* Evidence: `changed_files` is built from files that currently match the include globs (`match_files` on the head tree) intersected with the branch diff. A deleted file, a file moved outside `docs/brds/**`, or a file grown beyond `max_file_bytes` is absent from `artifacts[...]["files"]`, so it never enters `changed_files`. The artifact fingerprint still changes, so the agent runs, but any lowered score must cite a file in `changed_files`; citing the deleted file fails `evidence_path(ref) in changed`, and the gate reverts to the baseline. Example: a PR deleting `docs/brds/agentic-retrofit-programme-brd.md` leaves `changed_files` empty (the other BRD file is unchanged), every drop is reverted, total stays 61, `rubric/score` is success, the bot APPROVEs and records the old scores in `latest.json`. The agent context also omits the deletion (`changes.diff` is filtered to `changed_files`).
* Fix: on pull requests, take `git diff --name-status {base}...HEAD` and add every path (including `D` and the old side of `R`) that matches an artifact's include globs (via `fnmatch`, not `glob`) to that artifact's changed set, plus paths skipped for size. Include those paths in `changes.diff` and in context as `removed_files`. Accept a lowered score that cites a removed path. Add a gate test for deletion and a prepare test for the changed-set computation.
* Routing: fix now (Implement).

### RV-002 Medium: Agent context is built on a different tree than the gate state

* Files: `.github/workflows/rubric-score.lock.yml` L236-L251 (activation sparse checkout without `ref`, saved as the "base" snapshot) and L566-L570 (restore replaces `.github/` after PR checkout); `.github/workflows/rubric-score.md` L101-L114
* Evidence: gh-aw `restore_base_github_folders.sh` deletes and replaces the whole `.github` folder with the activation snapshot before `pre-agent-steps`. `prepare.py context` therefore computes `instrument_changed`, `scores_file_changed` and `open_criteria` against a `.github/` tree that differs from the PR head used by `rubric_prepare` and the gate. If the snapshot is base-branch content, the setup PR has no `.github/rubric/` in the agent workspace, `cp .github/rubric/scripts/prepare.py` (L110) fails, the agent job fails and `rubric/score` stays pending, contrary to README step 4. If the snapshot is the merge ref, the "trusted" restore is a no-op. The activation checkout sets no `ref`, so which case applies needs live confirmation.
* Fix: compute the context once in `rubric_prepare` on `head.sha`, upload `/tmp/gh-aw/agent/rubric` as an artifact and download it in `pre-agent-steps` (removes the duplicate script load), or run `prepare.py context` with `--root` pointing at a `git worktree` of `head.sha`. State in the README what the setup PR run does.
* Routing: fix now, or verify on the first live PR and fix if the setup PR stays pending.

### RV-003 Medium: Instrument changes cannot move scores, contrary to README

* Files: `.github/rubric/scripts/prepare.py` L35, L152, L159-L172; `.github/rubric/scripts/gate.py` L135-L137; `.github/rubric/README.md` Limits and Risks; `.github/workflows/rubric-score.md` L287, L290
* Evidence: (a) rubric and registry are read from `main`, so a PR's instrument change does not apply in that PR; (b) `instrument_changed` opens all criteria, but the changed-file evidence rule reverts every change unless an artifact file also changed, so a rubric, prompt or model change alone never moves scores; (c) after merge, the push run compares `HEAD` with itself, so it never sees an instrument change; (d) `INSTRUMENT_PATHS` lists `rubric-score.md` but not `rubric-score.lock.yml`, which is what runs; (e) when instruments change alongside an artifact, live criteria B1-B5 and C2 become open and can move by citing the BRD, contradicting README "stay at their baseline until a capstone deck or pitch artifact provides evidence"; bootstrap also tells the agent to rescore them "from scratch" while L287 says keep the baseline without evidence.
* Fix: store an instrument fingerprint in `latest.json` and compare it with `main`'s instrument fingerprint; when they differ, open all criteria and waive the changed-file rule for that run. Add the lock file to `INSTRUMENT_PATHS`. Keep live criteria closed unless a deck or pitch artifact is in `changed_artifacts`, including bootstrap. Otherwise correct the README to say instrument changes take effect only with the next artifact change.
* Routing: follow-up (Plan), README correction can be fixed now.

### RV-004 Medium: Manual dispatch cannot force a rescore

* Files: `.github/workflows/rubric-score.md` L10, L57-L60; `.github/rubric/scripts/prepare.py` L174; plan Follow-Up Items
* Evidence: `should_score` is false on unchanged `main` because fingerprints match and `differs_from_base(HEAD)` is always false, so the planned variance calibration ("dispatch two or three times on unchanged main") skips the agent every time. A dispatch on a non-`main` branch compares the branch with itself and, on failure, opens an issue titled "regressed on main".
* Fix: add a `workflow_dispatch` boolean input `force` passed to `prepare.py decide --force` (forces `should_score` and opens all criteria without evidence waiver), and restrict issue creation to `refs/heads/main`.
* Routing: fix now (small, unblocks the calibration follow-up).

### RV-005 Low: Agent text sanitisation is partial and rationale persists unsanitised

* Files: `.github/rubric/scripts/gate.py` L35-L39, L84-L85, L206-L209; `.github/workflows/rubric-score.md` L227-L236
* Evidence: `sanitize()` escapes `<`, `>`, `|` and `@` but leaves Markdown links and images (`[text](url)`, `![](url)`), bare URLs and `#123` references, which render in the sticky comment and in issues opened on `main`. Raw rationale (up to 1000 chars) is committed to `latest.json`, merged to `main` and returned to the next agent as trusted baseline context, so injected text can persist across runs.
* Fix: neutralise `](`, `![` and `http(s)://` (or render rationale inside escaped code spans), strip control characters, store the sanitised and truncated rationale in `latest.json`, and label baseline rationale as untrusted data in the prompt.
* Routing: follow-up.

### RV-006 Low: Evidence path normalisation discards legitimate changes

* Files: `.github/rubric/scripts/gate.py` L42-L44
* Evidence: only `./` and `:N` or `:N-M` suffixes are stripped. `docs\brds\x.md`, `/home/runner/work/ama/ama/docs/brds/x.md`, `/docs/brds/x.md`, `x.md#L10` and `x.md:L10` do not match `changed_files`, so the change is silently reverted (fail-safe but noisy).
* Fix: replace `\` with `/`, strip a `GITHUB_WORKSPACE` prefix and a leading `/`, strip `#L\d+(-L\d+)?` and `:L?\d+(-L?\d+)?`, apply `posixpath.normpath`; add parametrised tests.
* Routing: follow-up.

### RV-007 Low: Branch diff failure fails open

* Files: `.github/rubric/scripts/prepare.py` L101-L106, L163-L164, write_context diff
* Evidence: when `git diff {base}...HEAD` fails (no merge base, missing ref), `pr_changed_files` returns `None` and every file of a changed artifact counts as changed, weakening the evidence rule; `changes.diff` is silently empty.
* Fix: on `pull_request`, raise and let `main()` return `EXIT_ERROR` (fail closed); log the git stderr.
* Routing: follow-up.

### RV-008 Low: Symlinked directories and PPTX size are not bounded

* Files: `.github/rubric/scripts/prepare.py` L68-L70, L206
* Evidence: on Python 3.12 (ubuntu-latest), `Path.glob("**")` follows directory symlinks; only the leaf is checked with `is_symlink()`, so a symlinked directory under `docs/brds/` can pull files from outside the workspace into fingerprints and agent-visible paths. `max_file_bytes` limits compressed PPTX size only; `archive.read` decompresses without a bound.
* Fix: skip candidates whose `resolve()` is not under `root.resolve()`; check `ZipInfo.file_size` against a limit before reading slides.
* Routing: follow-up (deck extractor is `planned`).

### RV-009 Low: Bootstrap fallback executes PR-head scripts with a write token

* Files: `.github/workflows/rubric-score.md` L127-L131, L144-L151
* Evidence: the gate job checks out with default `persist-credentials: true` and, when `main` lacks the scripts, copies and runs the PR's `gate.py`/`prepare.py` with `contents`, `pull-requests`, `statuses` and `issues` write. This applies to the setup PR and to any later state where the scripts are removed from `main`.
* Fix: set `persist-credentials: false` and pass the token only to the push command; in `pull_request` runs, fail closed when the scripts are missing on `main` except for an explicit, documented setup case.
* Routing: follow-up.

### RV-010 Low: Status and comment lifecycle gaps

* Files: `.github/workflows/rubric-score.md` L89-L99, L216-L219, L253; lock L1231
* Evidence: (a) the conclusion pre-step also fires when the gate job ran but failed after setting `failure`, posting a misleading "stays pending" comment; (b) a skip by the daily AI credit guard, or a `prepare.py decide` error, leaves `rubric/score` pending or absent with no explanation; (c) a push rejected for permissions is reported as "Branch moved during scoring"; (d) the sticky lookup matches any author's comment starting with the marker, so `updateComment` can 403 and abort before the review is posted; (e) a stale bot REQUEST_CHANGES review remains when a later run takes the skip path.
* Fix: condition the pre-step on `needs.record_rubric_score.result == 'skipped'`; set an explicit failure status when `decide` fails; use a distinct description for push failure; filter the sticky comment by `c.user.login === 'github-actions[bot]'`; dismiss or supersede the prior bot review on the skip path.
* Routing: follow-up.

### RV-011 Low: Test framework diverges from plan and prepare.py is untested

* Files: `.github/rubric/scripts/test_gate.py` L9; plan P02-T03 and PC-015
* Evidence: the plan specifies stdlib `unittest`; the tests import `pytest`, and the changes record does not list this as a divergence. No tests cover `prepare.compute_state`, glob matching, deletion handling or evidence normalisation.
* Fix: record the divergence (or convert), and add `test_prepare.py` using a temporary git repository.
* Routing: follow-up.

### RV-012 Low: README and configuration drift

* Files: `.github/rubric/README.md` Owner Setup step 4, Limits; `.github/workflows/rubric-score.md` L20, L178; lock L1635
* Evidence: README says AI credits are "capped at 300 per run", but the detection job has its own default cap of 400. README says the first run happens after merging the setup PR, but the setup PR itself triggers a run (see RV-002). The model is pinned in two places (`engine.model` and `--model`), so they can drift.
* Fix: correct the README; pass the model from `needs.agent.outputs.model` (or one env value) to the gate.
* Routing: fix now (documentation), model plumbing as follow-up.

## Pending live validation

* Safe-output item schema: the gate expects items with `type == "record_rubric_score"` and a top-level `scorecard` field in `agent_output.json`; confirm on the first live run.
* RV-002 setup-PR behaviour and which snapshot the restore step uses.

## Routing summary

| Finding | Severity | Routing |
|---------|----------|---------|
| RV-001 | High | Fix now |
| RV-002 | Medium | Fix now or verify on first live run |
| RV-003 | Medium | Follow-up (README part fix now) |
| RV-004 | Medium | Fix now |
| RV-005 | Low | Follow-up |
| RV-006 | Low | Follow-up |
| RV-007 | Low | Follow-up |
| RV-008 | Low | Follow-up |
| RV-009 | Low | Follow-up |
| RV-010 | Low | Follow-up |
| RV-011 | Low | Follow-up |
| RV-012 | Low | Fix now (docs), follow-up (model) |
