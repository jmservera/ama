<!-- markdownlint-disable-file -->

# Task Research: immutable-blob-ledger-digests-115-rebase

| Field              | Value                                                                                          |
|--------------------|------------------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                                     |
| Researcher / agent | rpi-research (RPI Agent automatic child session)                                               |
| Status             | Complete                                                                                       |
| Artifact path      | .copilot-tracking/research/2026-11-15/immutable-blob-ledger-digests-115-rebase-research.md     |

## Research Brief

* What to research: Exact commit ancestry, conflict surface, cross-feature semantic interactions, and isolated focused validation requirements for rebasing `feat/demo-115-blob-ledger` (`681903493`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`) for Issue #115 without pushing.
* Why it matters: `origin/feat/demo-164-chat-grounding-provenance-0900` advanced three commits (`36aeddae3` `#215`, `f71331d42` `#76`, `fa6f8d1dd` `#216`) past `681903493`'s parent (`243764945`). Furthermore, this environment shares global Python user site-packages with sibling worktrees, so validation must isolate `zava_forward` editable packages and leave `git status --short` completely empty on the final rebased `HEAD`.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` in this automatic RPI child loop.
* Scope: Git commit range `243764945..fa6f8d1dd` vs `243764945..681903493`, `src/core/README.md` conflict resolution, `src/core` + `src/orchestrator` + `infra/tests` focused validation (`ruff check .`, `ruff format --check .`, `mypy`, `#115` blob ledger tests, `test_bicep_policy.py`), and clean-worktree RPI artifact commit conventions.
* Non-goals: Pushing to `origin`, running `tools/rpi-checks.py`, altering unrelated `#76`/`#215`/`#216` code, or mutating shared global Python user site-packages.
* Criteria: Every question answered with exact `path:line` codebase evidence (`C1`–`C8`), three complete research waves (`Wider`, `Deeper`, `Contrarian`), convergence recommendation selected, and `Planning Readiness: Ready`.
* Requested outputs: Primary research artifact in convergence mode.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                        |
|--------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1: Which files overlap between `681903493` and `243764945..fa6f8d1dd`? Q2: Do `#76`, `#215`, or `#216` affect `ledger_digest_blob`, `src/core/pyproject.toml`, or `infra/`? Q3: How must focused validation run without mutating shared worktree Python environments while leaving `git status --short` empty? |
| Codebase scope                       | `src/core/`, `src/orchestrator/`, `infra/`, `tools/rpi-checks.py`, `.copilot-tracking/`                                      |
| External scope                       | none                                                                                                                         |
| Research posture                     | focused                                                                                                                      |
| Posture provenance                   | default (bounded internal rebase and validation task with exact commit SHAs and named test/lint commands)                    |
| Explicit limits / deadline           | Single automatic RPI child run; focused validation tier; leave `git status --short` empty; do not push                       |
| Posture-specific completion basis    | focused scope coverage with complete `Wider`, `Deeper`, and `Contrarian` verification across git diffs and local toolchains  |
| Edits allowed during research?       | no, research-only                                                                                                            |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                         |
| Known constraints / excluded sources | Shared non-sandboxed host environment; preserve `Refs #115` and privacy-safe `user.email`                                    |

## Extension Registry and Provenance

| Kind                | Candidate                                  | Match and provenance                        | Scoped authority or output contract                            | Selected / skipped reason                                                       |
|---------------------|--------------------------------------------|---------------------------------------------|----------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`          | `applyTo: "**"`                             | AMA branch, email privacy, focused validation, `Refs #115`     | Selected: mandatory repository rules                                            |
| Skill               | `rpi-research`                             | Active Research phase skill                 | Three-wave research artifact and `Planning Readiness` contract | Selected: active phase skill                                                    |
| Research specialist | `hve-core-all:rpi-researcher`              | Registered lane worker                      | Independent subagent research lane                             | Skipped (inline fallback): single tightly coupled git-rebase boundary (<5 probes)|

## User Participation and Research Decisions

| Checkpoint  | Questions or no-interaction rationale                                                        | Answers / unanswered | Resulting decision                                                                                 |
|-------------|----------------------------------------------------------------------------------------------|----------------------|----------------------------------------------------------------------------------------------------|
| Intake      | Caller supplied exact target ref `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`), candidate commit `681903493`, validation list, clean-status invariant, and no-push rule | N/A | Execute focused inline three-wave research                                                         |
| Convergence | Only `src/core/README.md` overlaps; isolated `/tmp` venv avoids mutating shared site-packages; tracking commit keeps `git status --short` empty | N/A | Select Option A (rebase `681903493` onto `fa6f8d1dd` + isolated `/tmp` venv validation + `docs(rpi)` tracking commit) |

## Cycle 1 Waves

### Wave 1: Wider (Commit Lineage and File-Overlap Breadth)

* Verified `feat/demo-115-blob-ledger` sits at `681903493` directly atop `243764945`, while fetched `origin/feat/demo-164-chat-grounding-provenance-0900` resolves to `fa6f8d1dd0493342718a70c134dd9fcb3305cd6c` with three commits since `243764945`: `36aeddae3` (`#215`), `f71331d42` (`#76`), and `fa6f8d1dd` (`#216`).
* Compared `git diff --name-only 243764945..681903493` (17 files) against `git diff --name-only 243764945..fa6f8d1dd` (300 files): exactly **one** file overlaps (`src/core/README.md`), with zero overlap in `src/core/pyproject.toml`, `infra/`, `src/orchestrator/`, or `.copilot-tracking/` (`C1`, `C2`, `C3`).

### Wave 2: Deeper (README Conflict Seam, Typing Coupling, and Validation Isolation)

* In `src/core/README.md`, `681903493` inserts `## Immutable Blob ledger digests and scheduled verification (2026-11-15, Refs #115)` at line 9 immediately above `## Offline RAI held-out evaluation and tokenomics candidate comparison (2026-11-15, Refs #108)` (`C1`), while `f71331d42` inserts `## Hazard and safeguarding clock and named owner projection (2026-11-15, Refs #76)` at the same line 9 (`C2`), and `fa6f8d1dd` inserts `### Owned citation/refusal evaluation gates and rule-card ship comparator (#216)` far lower around line 4913 (`C2`). Placing the `#115` H2 section immediately above the `#76` H2 section preserves newest-first reverse-chronological order and all `#115`, `#76`, `#108`, and `#216` documentation intact.
* `fa6f8d1dd` adds strictly typed `src/core/src/zava_forward/core/regulatory_eval_gates.py` and `src/core/tests/test_regulatory_eval_gates_216.py` without modifying `src/core/pyproject.toml` (`C3`), so `681903493`'s `disallow_untyped_calls = false` override for `zava_forward.core.ledger_digest_blob` and `test_ledger_digest_blob` (`C4`) replays cleanly and `mypy` in `src/core` checks the combined 346+ source/test files under `strict = true`.
* `infra/tests/test_bicep_policy.py` imports both `zava_forward.core.ledger_digest_blob` and `zava_forward.orchestrator.digest_blob` (`C5`) and runs under `REQUIRE_AZ_BICEP=1` (`C6`). Because global `/usr/bin/python3` currently resolves editable `zava-forward-core` to sibling worktree `/home/azureuser/source/ama-demo-wt/feat-164-chat-revocation-0042/src/core`, running validation inside a temporary isolated venv (`/tmp/zf-115-rebase-venv` with `--system-site-packages` and `--no-deps --no-build-isolation -e src/core -e src/orchestrator`) tests the exact rebased worktree code without mutating shared global site-packages, and removing `/tmp/zf-115-rebase-venv` afterward leaves zero host side effects.

### Wave 3: Contrarian (Untracked Rebase Collisions and Clean-Worktree Invariant)

* Challenge 1: Could untracked `.copilot-tracking/.../immutable-blob-ledger-digests-115-rebase-*` files block `git rebase` or violate `leave git status --short empty`?
  * Counter-evidence and mitigation: None of the `immutable-blob-ledger-digests-115-rebase-*` paths exist in `243764945..fa6f8d1dd`, and parent state `immutable-blob-ledger-digests-115-state.json` is kept untouched so `git status --short` has zero modified tracked files when `git rebase` starts (stashing or moving untracked tracking files to `/tmp` across `git rebase` if needed). After `rpi-review` and final `Follow-up` state persistence, committing the 7 `immutable-blob-ledger-digests-115-rebase-*` tracking files in `docs(rpi): record #115 rebase onto #164 RPI artifacts` (`Refs #115`, matching sibling rebase commits `36aeddae3` and `f71331d42`, `C7`) and re-running focused validation on the final `HEAD` guarantees `git status --short` is empty while preserving durable RPI evidence.
* Challenge 2: Could `src/core/README.md` merge resolution break relative Markdown links checked by `src/core/tests/test_live_doc_links.py`?
  * Counter-evidence and mitigation: Include `test_live_doc_links.py` and `test_dependency_rule.py` alongside `test_ledger_digest_blob.py`, `src/orchestrator/tests/test_digest_blob.py`, `infra/tests/test_bicep_policy.py`, and `infra/tests/test_monitoring_alerts.py` in focused validation (`C8`).

## Evidence Log

* `C1`: `src/core/README.md:9-35` — `681903493` inserts `## Immutable Blob ledger digests and scheduled verification (2026-11-15, Refs #115)` directly above the `#108` H2 section.
* `C2`: `origin/feat/demo-164-chat-grounding-provenance-0900:src/core/README.md:9-32,4913-5016` — `f71331d42` inserts the `#76` H2 section at line 9 and `fa6f8d1dd` inserts the `#216` H3 section at line 4913; `src/core/README.md` is the sole overlapping path between `681903493` and `243764945..fa6f8d1dd`.
* `C3`: `src/core/pyproject.toml:23-39` — Configures `ruff` (`line-length = 100`, `py312`, `E,F,I,B,UP`) and `mypy` (`strict = true`, `files = ["src", "tests"]`), untouched in `243764945..fa6f8d1dd`.
* `C4`: `src/core/pyproject.toml:73-77` — `681903493` adds `zava_forward.core.ledger_digest_blob`, `test_ledger_digest_blob`, and `tests.test_ledger_digest_blob` to `disallow_untyped_calls = false`.
* `C5`: `infra/tests/test_bicep_policy.py:1196-1238,2126` — Imports `zava_forward.core.ledger_digest_blob` and `zava_forward.orchestrator.digest_blob` to validate compiled ARM `digestRetention` immutability policies, container wiring, and scheduled alert mutations.
* `C6`: `tools/rpi-checks.py:50-55,988-1020,1144-1152` — Defines `REQUIRE_AZ_BICEP=1` for `infra/tests` discovery and `--isolated --select E,F,I,B,UP --target-version py312 --line-length 100` `ruff` flags for `infra/tests/test_bicep_policy.py`.
* `C7`: `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-changes.md:1-60` (on `fa6f8d1dd`) — Establishes repository convention for newest-first `src/core/README.md` rebase resolution and clean post-Review local `Refs #N` tracking commits when `Do not push` is active.
* `C8`: `src/core/tests/test_ledger_digest_blob.py:1-50` and `src/orchestrator/tests/test_digest_blob.py:1-50` — Define the `#115` Blob ledger unit test suites across `src/core` and `src/orchestrator`.

## Alternatives and Convergence Selection

* **Option A (Selected)**: Rebase `681903493` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`), resolve `src/core/README.md` keeping `#115` H2 immediately above `#76` H2, validate inside an isolated `/tmp/zf-115-rebase-venv` (running `ruff check .`, `ruff format --check .`, `mypy`, `#115` blob ledger tests in `src/core` and `src/orchestrator`, `az bicep build`/`lint`, and `REQUIRE_AZ_BICEP=1` `test_bicep_policy.py` + `test_monitoring_alerts.py`), commit the child RPI tracking set as `docs(rpi): record #115 rebase onto #164 RPI artifacts` (`Refs #115`), re-verify focused checks and `git status --short == ""` on final `HEAD`, and remove `/tmp/zf-115-rebase-venv`.
* **Option B (Rejected — Amend `681903493` with rebase tracking artifacts)**: Mixes child rebase RPI artifacts into the parent implementation commit and complicates commit-boundary inspection compared with a clean tracking commit on top of the rebased code commit.
* **Option C (Rejected — Mutate global `pip install -e` in `/home/azureuser/.local`)**: Risks breaking concurrent sessions in sibling worktree `feat-164-chat-revocation-0042` on this shared non-sandboxed host.

## Current Decisions, Risks, and Readiness

* Current decisions:
  * D1: Preserve `immutable-blob-ledger-digests-115-state.json` unmodified and track this continuation in `immutable-blob-ledger-digests-115-rebase-state.json` (`parent_task = issue-115-immutable-blob-ledger-digests`).
  * D2: Resolve `src/core/README.md` with `#115` immediately above `#76` (`C1`, `C2`, `C7`).
  * D3: Run all Python lint, format, `mypy`, and `#115` / `infra` tests in `/tmp/zf-115-rebase-venv` (`--system-site-packages`, editable `src/core` and `src/orchestrator` installed `--no-deps --no-build-isolation`) and delete `/tmp/zf-115-rebase-venv` before finishing (`C5`, `C6`, `C8`).
  * D4: Commit child RPI artifacts locally (`Refs #115`, no push) after Review/Follow-up transition and re-verify focused checks + empty `git status --short` on `HEAD`.
* Unresolved decisions or risks: None blocking planning or execution; hosted CI and live Azure WORM lock/Monitor proof remain deferred (`Do not push`, `Refs #115`).
* Research disposition: `executed`
* Planning Readiness: `Ready`
* Self-check: Passed (`Wider` -> `Deeper` -> `Contrarian` completed; all claims backed by `C1`–`C8`; zero source edits during Research).
