---
title: "RPI Plan Critique: PR #1792 c2 Ruff Format Remediation (Issue #100)"
description: "Single-pass credibility critique of the Issue #100 PR #1792 c2 Ruff line-length=100 formatting plan and phase details"
ms.date: 2026-11-15
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: issue-100-mgmt-tokenomics-c2-lint
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Remediate the sole hosted CI failure on PR #1792 (`feat/insight-100-mgmt-tokenomics` at `d3a2c5405`, targeting `feat/demo-164-chat-grounding-provenance-0900` / PR #1641), where `8/10` CI jobs passed and `src-core` (`132805147399`) and `src-api` (`132805147369`) failed only Step 6 (`Lint`: `ruff check . && ruff format --check .`) because `tokenomics.py` and `progress.py` were formatted at repo-root default `line-length = 88` instead of package-configured `line-length = 100`. Deliver all seven dated `c2` `.copilot-tracking/` artifacts, reformat the two files inside `src/core` and `src/api`, validate under the Focused tier (`ruff check .`, `ruff format --check .`, `mypy`, and Focused `unittest` suites), and create one local commit on `feat/insight-100-mgmt-tokenomics` with `Refs #100` and the Copilot `Co-authored-by` trailer without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-research.md (`C1` through `C8`), .copilot-tracking/plans/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-plan.md, .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-phase-details.md, .github/workflows/src-ci.yml, src/core/pyproject.toml, src/api/pyproject.toml.
* Decisions, dependencies, and acceptance criteria considered: Package-scoped `ruff format` at `line-length = 100` on `src/core/src/zava_forward/core/tokenomics.py` and `src/api/src/zava_forward/api/progress.py`; AST parse-equivalence (`ast.dump(..., include_attributes=False)`) against `d3a2c5405`; Focused validation tier under owner decision D4 and Issue #1294; augmented `-p "test_*tokenomics*.py"` test discovery alongside caller commands; repository-local privacy-safe `{id}+{login}@users.noreply.github.com` author and committer identity; post-Review single local commit with `Refs #100` and no remote push; pinned dev toolchain (`ruff==0.17.1`, `mypy==2.4.0`).
* Assessment boundary: Evaluates completeness, internal consistency, CI parity, AST-invariance verification, test-selector coverage, validation-tier classification, and git closeout sequencing from the supplied artifacts and configuration files without mutating source files or executing live formatting or test runs.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 / FR-2 (`c2` RPI tracking trail) | Covered | All seven dated `2026-11-15` `c2` artifact paths (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews/logs`, `rpi-sessions`) are enumerated consistently across the research file tree, FR-2, Acceptance Criteria, and P02-T01. |
| Caller Req 2 / FR-1 (`ruff format` + `ruff check`) | Covered | P01-T01 and P01-T02 invoke `python3 -m ruff format` and `python3 -m ruff check . && python3 -m ruff format --check .` from within `src/core` (`302` formatted files, `C3`, `C5`) and `src/api` (`214` formatted files, `C4`, `C6`), matching .github/workflows/src-ci.yml (`working-directory: src/${{ matrix.project }}`, `C1`). |
| NFR-1 (AST and behavioral invariance) | Covered | P01-T01 and P01-T02 verify `ast.dump(ast.parse(...), include_attributes=False)` equality against `d3a2c5405` for both `tokenomics.py` (5 line-wrap hunks, `C5`) and `progress.py` (1 call-wrap hunk, `C6`). |
| Caller Req 3 / NFR-2 (Focused `mypy` and `unittest`) | Covered | P02 and P02-T01 run both bare and `PYTHONPATH`-explicit `mypy` in `src/core` and `src/api` plus both caller-specified `unittest` globs and `-p "test_*tokenomics*.py"` (with `tests` on `src/api` `PYTHONPATH` and `-W error::ResourceWarning`), preventing the silent zero-test miss on `test_management_tokenomics_api_100.py` and omission of `test_management_tokenomics_invariant_100.py` identified in `C7`. |
| Caller Req 4 / FR-2 (Local commit, `Refs #100`, no push) | Covered | P02 and P02-T01 verify `{id}+{login}@users.noreply.github.com` via `gh api user` and sequence a single post-`rpi-review` local commit on `feat/insight-100-mgmt-tokenomics` containing the 2 Python files and 7 `c2` tracking artifacts with `Refs #100` and the `Co-authored-by` trailer, leaving `origin/feat/insight-100-mgmt-tokenomics` untouched at `d3a2c5405`. |
| Research `C1`-`C8` and D4/#1294 tier classification | Covered | Focused tier is justified (`C8`): pure AST-identical formatting in 2 Python modules touches no SQL, Bicep, Dockerfiles, dependency manifests, CI workflows, `src/api/checks/` browser scripts, or `src/api/src/zava_forward/api/web/` UI files. |
| P01 (`P01-T01`, `P01-T02`) and P02 (`P02-T01`) | Covered | Task boundaries, target files, exact commands, expected file counts, and completion evidence are concrete, non-overlapping, and directly executable. |

## Verdict

* Verdict: Pass
* Rationale: The plan and phase details are complete, internally consistent, and grounded in verified primary evidence (`C1`-`C8`), .github/workflows/src-ci.yml, src/core/pyproject.toml, and src/api/pyproject.toml. Every caller requirement, CI parity command, test-discovery edge case (`C7`), AST-invariance check, privacy-safe git identity safeguard, and post-Review single-commit boundary (without remote push) is explicitly addressed with zero substantive gaps.

## Findings

No actionable `PC-xxx` defects or revision items identified (`0` Critical, `0` High, `0` Medium, `0` Low).

## Strengths and Residual Risk

* Contrarian test-selector safeguard (`C7`): Adding `-p "test_*tokenomics*.py"` (and `tests` on `src/api` `PYTHONPATH`) alongside the caller-listed commands prevents `unittest discover` from silently skipping `src/core/tests/test_management_tokenomics_invariant_100.py` (`6` tests) and matching `0` files against `src/api/tests/test_management_tokenomics_api_100.py` (`2` multi-endpoint HTTP tests).
* Exact CI and AST parity (`C1`, `C3`-`C6`): Package-directory Ruff invocations match `.github/workflows/src-ci.yml` (`working-directory: src/${{ matrix.project }}`), confirm `[tool.ruff.format] exclude` leaves `src/api/src/zava_forward/api/server.py` untouched, and prove semantic invariance via `ast.dump` comparison against `d3a2c5405`.
* Clean post-Review commit sequencing: Preparing local `{id}+{login}@users.noreply.github.com` git identity during P02-T01 and executing the single atomic commit after `rpi-review` writes `review.md` and final `state.json` avoids dirty post-commit tracking files or prohibited commit amendments (`--amend`).
* Accepted residual risk (unpushed local HEAD): Because the caller explicitly forbids pushing (`Do NOT push`), hosted CI on PR #1792 remains red at remote `d3a2c5405` until the coordinator pushes the new local commit and observes fresh hosted `src-core` and `src-api` runs.
* Accepted scope boundary (`c1` follow-ups): Prior `c1` follow-up items (`RV-001`, `RV-002`, and `OD-51` commercial governance sign-off) remain explicitly tracked under Follow-Up Items outside this surgical `c2` formatting fix, and `Refs #100` preserves non-closing issue linkage.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Read-only critique boundary: This assessment inspected the supplied research, plan, phase details, workflow, and `pyproject.toml` configurations statically without executing mutating `ruff format` commands, test suites, or git configuration changes.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: planning_parent
* Smallest next action: Finalize the plan (`Planning status: Ready`, record `Pass` disposition in Critique Disposition and Implementation Context Record) and proceed directly to `rpi-implement` (`P01-T01`, `P01-T02`, `P02-T01`).
* User response required: no
