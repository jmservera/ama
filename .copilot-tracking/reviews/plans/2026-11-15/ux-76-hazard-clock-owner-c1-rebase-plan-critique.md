<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #76 C1 Rebase Continuation onto `#1641` (`08c36e4dc`)

## Metadata

* Task ID: issue-76-c1-rebase
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Rebase `feat/ux-76-hazard-clock-owner` (`8bd8a4f4d` and `c98e58bf4`, currently based on `0c1fa1da4`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`, incorporating PR `#1770` / Issue `#133` and PR `#1771` / Issue `#108`): (1) record compact RPI artifacts under `.copilot-tracking/*/` (`ux-76-hazard-clock-owner-c1-rebase-*`); (2) run `git fetch origin feat/demo-164-chat-grounding-provenance-0900` and `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`; (3) resolve the append-only conflicts in `src/api/README.md` and `src/core/README.md` preserving both sides' dated sections in README chronological order; (4) run the three caller-specified focused validation commands (`unittest` across the three `#76` core/api test files, `ruff check` + `ruff format --check` + `mypy` in `src/core`, and `ruff check` + `ruff format --check` in `src/api`); (5) commit tracking artifacts locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leave `git status --short` empty, and do not push.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-research.md, .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-plan.md, .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-phase-details.md, .copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan-critique.md, .copilot-tracking/rpi-sessions/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-state.json, src/api/README.md, src/core/README.md, read-only Git commit/diff inspection of `0c1fa1da4..08c36e4dc` (`d8cb35d25`, `08c36e4dc`) against `8bd8a4f4d` and `c98e58bf4` (including `heldout_eval.py`, `pyproject.toml`, and `ranking.py`), and read-only dry execution of the Python 3.12 `unittest` file-path CLI selector.
* Decisions, dependencies, and acceptance criteria considered: `FR-1`, `FR-2`, `NFR-1`, `NFR-2`, `AC-1` through `AC-4`, research citations `C1` through `C6`, and repository branch/commit and focused-tier validation rules in .github/copilot-instructions.md.
* Assessment boundary: Evaluates completeness, commit-by-commit rebase conflict replay mechanics, README section ordering, upstream semantic/typing/freeze compatibility (`#133` and `#108`), Python 3.12 `unittest` CLI invocation behavior, and post-review commit closeout sequencing from read-only repository evidence without modifying tracked files or running mutating Git commands.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1, AC-1 / C1, C2, C5 | Covered | Read-only inspection of `0c1fa1da4..08c36e4dc` vs `0c1fa1da4..c98e58bf4` confirms `src/api/README.md` and `src/core/README.md` are the only overlapping paths across both commits (`8bd8a4f4d` and `c98e58bf4`), and untracked `ux-76-hazard-clock-owner-c1-rebase-*` files are disjoint from all tracked paths in `0c1fa1da4..08c36e4dc`. `P01-T01` also verifies `git rev-parse --short origin/feat/demo-164-chat-grounding-provenance-0900` immediately after `git fetch` before rebasing. |
| FR-2, AC-1 / C1-C4 | Covered | Both `src/api/README.md` and `src/core/README.md` maintain newest-first (reverse-chronological) feature sections directly below YAML frontmatter (`2026-11-15` -> `2026-11-11` -> `2026-10-31`). Placing `#76` (`2026-11-15, Refs #76`) immediately after frontmatter followed by `#108` (`2026-11-15, Refs #108`) preserves both sections in full, keeps Commit 1 (`8bd8a4f4d` `MEMBERSHIP_REVISION = 4`) aligned at lines 8-22 so Commit 2 (`c98e58bf4` `MEMBERSHIP_REVISION = 5` + staff-order-invariant lookup) replays cleanly without a second conflict, and retains `#133`'s auto-merged `aftercare` update near line 5108 of `src/core/README.md`. |
| NFR-1, AC-2, AC-3 / C5, C6 | Covered | Read-only dry run with `PYTHONDONTWRITEBYTECODE=1` confirms Python 3.12 `python3 -m unittest src/core/tests/test_hazard_safeguarding_clock_owner.py src/core/tests/test_hazard_safeguarding_clock_owner_76.py src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py -q` accepts workspace-relative `.py` paths and runs 9/9 tests (`OK`). Upstream `#108` `pyproject.toml` overrides are scoped solely to `heldout_eval` and `tokenomics_comparison`, and `ranking.policy_hash(ranking.POLICY_V1)` remains `b66fdaccdcbd46a0eb257572a2b8f0fb98e7eafd53b468b67084d9a19761be2c`, introducing zero `capability_version_drift` in `#108`'s frozen held-out manifest. |
| NFR-2, AC-4 | Covered | `P02-T02` verifies diff boundaries, ensures repository-local `user.email` uses `{id}+{login}@users.noreply.github.com` from `gh api user`, reconciles `changes.md` and checklist markers before `rpi-review`, and stages/commits all seven `ux-76-hazard-clock-owner-c1-rebase-*` tracking artifacts locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` after `rpi-review` writes `review.md` and `state.json`, leaving `git status --short` empty with no `git push`. |
| P01 / P01-T01 | Covered | Covers fetch, SHA check, two-commit rebase onto `08c36e4dc`, lossless reverse-chronological resolution of `src/api/README.md` and `src/core/README.md`, clean Commit 2 (`c98e58bf4`) continuation, ancestry check, and zero conflict markers. |
| P02 / P02-T01 | Covered | Executes all three caller-specified focused validation commands verbatim across `src/core` and `src/api` with locked zero-delta test budget (`0` removals, `0` new test files). |
| P02 / P02-T02 | Covered | Sequences `Implement` reconciliation, `rpi-review` log/state completion, and the single local tracking commit cleanly without pushing. |

## Verdict

* Verdict: Pass
* Rationale: All functional requirements (`FR-1`, `FR-2`), non-functional requirements (`NFR-1`, `NFR-2`), acceptance criteria (`AC-1` through `AC-4`), and tasks (`P01-T01`, `P02-T01`, `P02-T02`) are complete, internally consistent, and verified against read-only Git object diffs and runtime checks. Commit-by-commit replay mechanics across `8bd8a4f4d` and `c98e58bf4` onto `08c36e4dc`, README reverse-chronological ordering, Python 3.12 `unittest` file-path invocation, and `#133`/`#108` semantic isolation are all confirmed with zero actionable gaps.

## Findings

* No actionable findings (`0` Critical, `0` High, `0` Medium, `0` Low).

## Strengths and Residual Risk

* Two-commit README replay mechanics verified without traps: During Commit 1 (`8bd8a4f4d`) conflict resolution on `src/core/README.md`, keeping Commit 1's `#76` block (`MEMBERSHIP_REVISION = 4`) immediately below frontmatter `---` and above `#108`'s block (`08c36e4dc`) preserves Commit 1 accuracy and matches `c98e58bf4`'s exact hunk context (`lines 8-22`), so `GIT_EDITOR=true git rebase --continue` replays Commit 2 cleanly to advance `src/core/README.md` to `MEMBERSHIP_REVISION = 5` with staff-order-invariant wording.
* Zero semantic or freeze-digest interaction with `#133` and `#108`: Neither `d8cb35d25` (`#1770`) nor `08c36e4dc` (`#1771`) touches any `#76` module (`taskqueues.py`, `store.py`, `sqlstore.py`, `workflows.py`, `projection.py`, `insights.py`, `ranking.py`, `web/app.js`), and `#76`'s `ranking._hazard` update leaves `ranking.policy_hash(ranking.CURRENT)` unchanged (`b66fdaccdcbd46a0eb257572a2b8f0fb98e7eafd53b468b67084d9a19761be2c`), preserving `heldout_eval._capability_version_snapshot()` invariants.
* Python 3.12 `unittest` file-path CLI verified directly: Read-only invocation of the exact `AC-2` command executes all 9 tests across `src/core/tests/test_hazard_safeguarding_clock_owner.py`, `src/core/tests/test_hazard_safeguarding_clock_owner_76.py`, and `src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py` and exits `0`.
* Accepted residual risk: Live SQL Server container execution (`MssqlParity` under `ZF_TEST_MSSQL=1`) runs in hosted GitHub Actions CI once the rebased branch is pushed under owner/coordinator authorization, as recorded in the plan's Follow-Up Items.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique executed strictly read-only against repository commits (`0c1fa1da4`, `d8cb35d25`, `08c36e4dc`, `8bd8a4f4d`, `c98e58bf4`), tracking artifacts, and bytecode-suppressed (`-B`) `unittest` CLI verification prior to running `git fetch` or `git rebase`.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: planning_parent
* Smallest next action: Finalize planning status on .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-plan.md and advance directly to `rpi-implement` (`P01-T01`).
* User response required: No
