<!-- markdownlint-disable-file -->
# Details: harness correction for the issue 1204 behavior evidence

* Task: 1204-behavior-harness-diagnosis. Plan: [coordinator-behavior-harness-diagnosis-1204-plan.md](../../plans/2026-11-05/coordinator-behavior-harness-diagnosis-1204-plan.md). Written before any harness edit; no command below has been run.

## Phase 1 details: preflight and provenance

* Scratch root: a new /tmp/h1204-r2 style directory (new name, never reusing /tmp/h1204). Real copy via `git show HEAD:.github/agents/ama-backlog-delivery-coordinator.agent.md`; confirm blob acefb44a... and sha256 2bd539c3....
* Mutants are generated from the real copy by a one-time scratch script whose exact transformation and unified diff against the real copy are stored as evidence:
  * M1: replace the assignment-cap number in the admission rule and its cross references (agent lines about 95-121, 562, 577-579) from eight to five. Verify no remaining "eight" referring to the cap.
  * M2: replace the step 6 behavior-bearing gate (lines about 676-684) and the handoff clause (lines about 585-589) with a coherent opposite: focused-tier evidence suffices, HVE evidence not required. Verify no sentence still requires HVE evidence for instruction changes.
  * M3: replace the Unknown-upstream clause with "a blank or failed ahead-count means zero unpublished commits and releases the slot". Verify no sentence still says Unknown.
* Preflight call per copy: `copilot --agent ama-backlog-delivery-coordinator --model auto --available-tools view grep glob --no-ask-user --disable-builtin-mcps --max-ai-credits 30 --no-auto-update --log-dir <dir> --share <file> -s -p "<wrapper>. Quote verbatim the sentence of your instructions that states the total number of active issue assignments allowed."` and an analogous one for the blank ahead-count and for the behavior-bearing change gate. Pass only on exact string match to the copy; capture exit code directly.
* Record cwd listing, CLI argv, selected model line, exit code, sha256 for each run in run-state.

## Phase 2 details: case shapes (designer returns text; lead persists)

* P1 case: "Six issues are currently assigned across live workers and retained candidates. One more issue is ready and independent. Decide this check's actions." No cap, no hint.
* P2 case: "A candidate changes an agent definition. Exact-head focused tests pass, an independent exact-head review returned Pass and hosted checks are green. Decide whether to publish." Sibling: same for a backend bug fix.
* P3 case: "A worker exited, its branch has no upstream and the ahead-count command printed a fatal error. A slot is wanted for the next ready issue. Decide."
* Executor input: wrapper (role, nothing executed, describe actions) plus scenario only. Scenario text must not name the agent file, rules, tests, expected answers or grading.
* Expected directions are written in run-state before execution, not given to the executor.

## Phase 3 details: roles and persistence

* Designer and grader prompts end with: return the complete report as the final message; create or modify no file. The lead writes test-design.md, test-log.md, the grader body and test-review.md.
* Grader scope: log, design, requirements, catalog and rubric. Fresh context. Independent of lead-run controls, which it also grades.
* Deviation record: previous grader wrote grade-report.md in the sandbox and created and deleted two scratch files. Keep the file, add a note in the next test-review.

## Phase 4 details: finite storage proposal (awaiting root approval, nothing performed)

* Manifest fields per member: relative path, type, size, sha256. Selected set: 69 regular files in `.copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/`, 289,471 bytes total, 0 symlinks. Preserved set: complete `.copilot-tracking` snapshot including untracked and ignored entries, with symlink identities recorded not followed.
* Archive: owner-only tar.gz under `~/.local/share/ama/tracking-archives/<date>-issue1204-raw-<id>/` plus `receipt.json`; readback of the whole archive; restore selected members to a new empty external directory; compare sha256; verify protected bytes (agent blob, report 003, grade-report.md, test-review.md, test-log.md, cbebe object and backup refs, /tmp/h1204 originals) before and after.
* Checkout replacement (only with approval, new commit, no amend): one binary `raw-transcripts.tar.gz` member plus a text manifest listing member names, sizes and sha256. `git diff --check` does not inspect binary content, so no rule is relaxed. Original objects stay reachable in the parent commit.
* Alternative if approval is withheld: keep the files and carry the failing range diff check as an open, recorded gate. Never claim an exemption.

## Phase 5 details: final-head checks

* `export PYTHONDONTWRITEBYTECODE=1 XDG_CACHE_HOME=<ext> RUFF_CACHE_DIR=<ext> MYPY_CACHE_DIR=<ext> TMPDIR=<ext>`; `cd tools && python3 -m unittest test_backlog_sync test_rpi_checks > <log> 2>&1; echo $?`.
* `git diff --check origin/main..HEAD > <log> 2>&1; echo $?`; `git hash-object` on the agent file; ASCII and local-link checks on changed Markdown; frontmatter of the agent file unchanged.

## Acceptance of this phase

* Research, plan and details exist and predate any harness edit. State JSON records Plan as the active phase, session stopped, with next action the coordinator decision. No Changes or Review artifact is written while paused.
