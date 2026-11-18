<!-- markdownlint-disable-file -->

# Task Research: ux-76-hazard-clock-owner-c1-rebase

| Field              | Value                                                                                 |
|--------------------|---------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                            |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                               |
| Status             | Complete                                                                              |
| Artifact path      | .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-research.md  |
| Planning Readiness | Ready                                                                                 |
| Disposition        | executed                                                                              |

## Research Brief

* What to research: Verify commit ancestry, 3-way merge conflicts across both branch commits (`8bd8a4f4d` and `c98e58bf4`), and any runtime, schema, or `MEMBERSHIP_REVISION` interactions when rebasing `feat/ux-76-hazard-clock-owner` from `0c1fa1da4` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`, after `#1770` / Issue #133 and `#1771` / Issue #108 merged).
* Why it matters: `c98e58bf4` completed and verified Issue #76 C1 (`MssqlParity` staff-order invariance), while target base `origin/feat/demo-164-chat-grounding-provenance-0900` advanced by two commits (`d8cb35d25` and `08c36e4dc`). Cleanly rebasing now leaves `feat/ux-76-hazard-clock-owner` fast-forward-based on `08c36e4dc` and passing focused validation without regressing `#133`, `#108`, `#83`, or `#76`.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` for `ux-76-hazard-clock-owner-c1-rebase`.
* Scope: `0c1fa1da4..08c36e4dc`, `0c1fa1da4..c98e58bf4`, `src/api/README.md`, `src/core/README.md`, `src/core/src/zava_forward/core/taskqueues.py`, and focused test/lint/typecheck runners in `src/core` and `src/api`.
* Non-goals: Pushing to `origin`, running `tools/rpi-checks.py`, or modifying application source/test logic unless rebase interaction requires it.
* Criteria: Exact conflict sites and commit-by-commit replay behavior proven; zero semantic conflicts confirmed; README section ordering verified; focused validation commands confirmed.
* Requested outputs: Compact 3-wave synthesis (`C1`–`C6`), convergence recommendation, and planning readiness record.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                          |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Which commits conflict during `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, how should `src/api/README.md` and `src/core/README.md` order both sides' entries, and do `#1770`/`#1771` introduce any code/typing/queue-revision overlap with `#76`? |
| Codebase scope                       | `src/core/`, `src/api/`, `.copilot-tracking/*/2026-11-15/ux-76-hazard-clock-owner*`                            |
| External scope                       | none                                                                                                           |
| Research posture                     | focused                                                                                                        |
| Posture provenance                   | default (bounded rebase continuation with exact base/head SHAs and caller validation specification)            |
| Explicit limits / deadline           | Focused validation tier; commit tracking artifacts locally with `Refs #76` and Copilot trailer; do NOT push    |
| Edits allowed during research?       | no, research-only                                                                                              |
| Resolved evidence root               | `.copilot-tracking/` default                                                                                   |
| Known constraints / excluded sources | Preserve prior `ux-76-hazard-clock-owner-*` and `ux-76-hazard-clock-owner-c1-*` artifacts untouched            |

## Extension Registry and Provenance

| Kind        | Candidate                         | Match and provenance                        | Scoped authority or output contract                   | Selected / skipped reason                                              |
|-------------|-----------------------------------|---------------------------------------------|-------------------------------------------------------|------------------------------------------------------------------------|
| Instruction | `.github/copilot-instructions.md` | `applyTo: "**"`                             | Focused validation tier, noreply author, RPI tracking | Selected automatically                                                 |
| Skill       | `web-design-guidelines`           | Web UI changes only                         | Pre-edit and review checklist for web files           | Skipped: rebase continuation resolves two Markdown README files only   |
| Specialist  | `hve-core-all:rpi-researcher`     | Registered general RPI research lane worker | Independent subagent lane artifact                    | Skipped: bounded 2-file rebase inspection fits inline read-only checks |

## User Participation and Research Decisions

| Checkpoint  | Questions or no-interaction rationale                                                   | Answers / unanswered | Resulting decision or selected further research       |
|-------------|-----------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------|
| Intake      | Non-interactive session with complete target SHA (`08c36e4dc`), steps, and checks       | N/A                  | Proceed with `focused` posture and `convergence` mode |
| Convergence | All questions answered with read-only Git merge-tree and `path:line` codebase evidence | N/A                  | Converge on Option A and advance to `rpi-plan`        |

## Research Questions

|  # | Sub-question                                                                                                    | Type     | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------------|----------|----------|----------|
| Q1 | What changed upstream in `0c1fa1da4..08c36e4dc` and locally in `0c1fa1da4..c98e58bf4`?                          | internal | High     | Answered |
| Q2 | How do both commits (`8bd8a4f4d` and `c98e58bf4`) behave when replayed onto `08c36e4dc`, and how are READMEs ordered? | internal | High     | Answered |
| Q3 | Could `#1770` (`#133`) or `#1771` (`#108`) break `#76` queue revisions, `mypy`, `ruff`, or tests after rebase?  | internal | High     | Answered |

## Cycle 1 Execution (Wider -> Deeper -> Contrarian)

### Wider Wave

* Inspected `0c1fa1da4..08c36e4dc` (`d8cb35d25` PR `#1770` for `#133` aftercare neutral-text guards; `08c36e4dc` PR `#1771` for `#108` offline RAI held-out evaluation and tokenomics comparison) against local `0c1fa1da4..c98e58bf4` (`8bd8a4f4d` Cycle 0 and `c98e58bf4` Cycle 1).
* Verified `git merge-tree --write-tree 08c36e4dc c98e58bf4` and `git merge-tree --write-tree 08c36e4dc 8bd8a4f4d` both report conflicts solely in `src/api/README.md` and `src/core/README.md`, with zero code or test file conflicts (`C1`, `C2`).

### Deeper Wave

* Examined `src/api/README.md` (`lines 1-55`) and `src/core/README.md` (`lines 1-70` and `lines 5069-5120`) on `08c36e4dc`, `8bd8a4f4d`, and `c98e58bf4` (`C3`, `C4`):
  * Both READMEs maintain reverse-chronological feature sections immediately below YAML frontmatter (`ms.date: 2026-11-15`), e.g. `2026-11-15 (Refs #108)` -> `2026-11-11 (Refs #83)` -> `2026-10-31 (Refs #572)`.
  * `d8cb35d25` (`#133`) edited `src/core/README.md` at `lines 5069-5118` (`aftercare` section), which auto-merges cleanly without conflict.
  * `08c36e4dc` (`#108`) prepended `## Offline RAI held-out evaluation... (2026-11-15, Refs #108)` at `line 9` of both `src/api/README.md` and `src/core/README.md`, colliding with `8bd8a4f4d` (`#76`), which also prepended `## Hazard and safeguarding clock and named owner... (2026-11-15, Refs #76)` at `line 9`.
  * Commit 2 (`c98e58bf4`) updates `src/core/README.md` `lines 8-22` (`MEMBERSHIP_REVISION = 4` -> `MEMBERSHIP_REVISION = 5` and the staff-order-invariant note) with `ms.topic: reference` / `---` in its leading context (`C4`). Placing `#76` right below frontmatter followed immediately by `#108` (`#76` newest rebased topic above `#108` merged on `08c36e4dc`, above `2026-11-11 #83`) preserves the READMEs' reverse-chronological newest-first structure AND lets `c98e58bf4` replay onto `8bd8a4f4d` cleanly with zero second-commit conflict.

### Contrarian Wave

* Checked whether `#1770` or `#1771` modified `taskqueues.py`, `store.py`, `sqlstore.py`, `mssqlstore.py`, `workflows.py`, `web/app.js`, or `MEMBERSHIP_REVISION`: neither PR touched any `#76` module (`C5`). `taskqueues.MEMBERSHIP_REVISION` on `08c36e4dc` remains `4` (from `#1769`), so `c98e58bf4`'s `MEMBERSHIP_REVISION = 5` remains unique and accurate.
* Checked `src/core/pyproject.toml` and `src/api/pyproject.toml` diffs in `08c36e4dc` (`C6`) and grepped `src/core/tests` and `src/api/tests` for `README.md` assertions: `#1771` only appended scoped `[[tool.mypy.overrides]]` entries for `heldout_eval` / `tokenomics_comparison` modules, and no test asserts README section line numbers.
* Checked untracked files before rebasing: `.copilot-tracking/` files for `ux-76-hazard-clock-owner-c1-rebase-*` have unique filenames disjoint from `0c1fa1da4..08c36e4dc`, so `git rebase` will not clobber or block on untracked session files.

## Evidence Register

* `C1`: `src/api/README.md:1-28` (`08c36e4dc` vs `8bd8a4f4d`) — Both `08c36e4dc` (`#108`) and `8bd8a4f4d` (`#76`) update `ms.date: 2026-11-15` and insert a dated `2026-11-15` `##` section immediately above `## Handoff waiting times screen (2026-11-11, Refs #83)`.
* `C2`: `src/core/README.md:1-50` (`08c36e4dc` vs `8bd8a4f4d`) — Both `08c36e4dc` (`#108`) and `8bd8a4f4d` (`#76`) update `ms.date: 2026-11-15` and insert a dated `2026-11-15` `##` section immediately above `## Retained sensor readings for employees and Quality evidence (Refs #1288, #107)`.
* `C3`: `src/core/README.md:5069-5118` (`d8cb35d25` / `08c36e4dc`) — `#133` updates `neutral_text` documentation near EOF, auto-merging cleanly during 3-way merge.
* `C4`: `src/core/README.md:8-22` (`c98e58bf4`) — Commit 2 updates `MEMBERSHIP_REVISION = 4` to `MEMBERSHIP_REVISION = 5` and documents `code` -> `email` -> `name` lookup under `## Hazard and safeguarding clock and named owner projection (2026-11-15, Refs #76)` immediately after the frontmatter `---`.
* `C5`: `src/core/src/zava_forward/core/taskqueues.py:30-35` — `MEMBERSHIP_REVISION = 5` on `c98e58bf4` has zero overlap with `#1770` (`aftercare.py`, `aftercare_intake.py`, `quality.py`) or `#1771` (`heldout_eval.py`, `tokenomics_comparison.py`, `server.py`).
* `C6`: `src/core/pyproject.toml:150-159` and `src/api/pyproject.toml:109-115` (`08c36e4dc`) — Upstream `mypy` overrides are scoped exclusively to `heldout_eval` and `tokenomics_comparison`, preserving strict typing on `#76` modules and tests.

## Alternatives and Convergence Recommendation

* **Option A (Selected):** Fetch `origin feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`), run `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, resolve the Commit 1 (`8bd8a4f4d`) append-only top-of-file section conflicts in `src/api/README.md` and `src/core/README.md` in reverse-chronological order (`#76` `2026-11-15` rebased head section followed by `#108` `2026-11-15` merged section, above `2026-11-11 #83` / `#1288, #107`) so Commit 2 (`c98e58bf4`) also replays cleanly, run the three caller-specified focused validation commands across `src/core` and `src/api`, and commit the `ux-76-hazard-clock-owner-c1-rebase-*` tracking artifacts with `Refs #76` and the Copilot trailer without pushing.
* **Option B (Rejected — Squash `8bd8a4f4d` and `c98e58bf4` during rebase):** Unnecessarily rewrites verified commit boundaries when standard non-interactive rebase preserves both clean commits (`feat(queues)` + `fix(queues)`).

## Readiness and Self-Check

* Research execution status: Complete (1 full Wider -> Deeper -> Contrarian cycle).
* Research disposition: `executed`
* Planning Readiness: `Ready`
* Self-check:
  * All questions `Q1`–`Q3` answered with `C1`–`C6` `path:line` evidence: pass.
  * Research-only constraint honored (zero tracked files modified during Research): pass.
  * Ready for parent RPI Agent automatic transition to `rpi-plan`.
