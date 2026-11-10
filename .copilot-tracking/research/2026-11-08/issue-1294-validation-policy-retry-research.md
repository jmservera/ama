<!-- markdownlint-disable-file -->

# Task Research: issue-1294-validation-policy-retry

| Field              | Value                                                                           |
|--------------------|---------------------------------------------------------------------------------|
| Date               | 2026-11-08                                                                      |
| Researcher / agent | rpi-research (host skill invoked via hve-builder bridge), parent-run inline     |
| Status             | Complete                                                                        |
| Artifact path      | .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-retry-research.md |

## Research Brief

* What to research: actual hosted Source CI triggers, affected-project selection and executed checks compared with local `tools/rpi-checks.py --all` and `--changed`; local-only guarantees; current wording in the instruction, guide and coordinator files that must change.
* Why it matters: issue #1294 (owner highest priority) needs a lighter local-validation policy for small and documentation-only candidates that keeps relevant coverage and the higher-risk safeguards.
* Audience or intended use: the rpi-plan and rpi-implement phases of this issue, and the hve-builder Major improve lifecycle.
* Scope: `.github/workflows/`, `tools/rpi-checks.py` and its tests, `src/README.md`, `.github/copilot-instructions.md`, `.github/agents/ama-backlog-delivery-coordinator.agent.md`, other files that restate the gate policy.
* Non-goals: workflow, application, branch-protection and security-control changes; the #470 full-gate timing measurement.
* Criteria: every claim cites `path:line`; absent, path-filtered or skipped CI is never a pass.
* Requested outputs: findings, per-file change list, tier classification, planning readiness.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                  |
|----------------------------------|------------------------------------------------------------------------|
| Research question(s)             | See Research Questions                                                 |
| Codebase scope                   | this worktree only                                                     |
| External scope                   | none                                                                   |
| Initial internal candidate areas | files listed in Scope                                                  |
| Research posture                 | balanced                                                               |
| Posture provenance               | default (bounded internal task with named targets)                     |
| Explicit limits / deadline       | worktree only; no `find /`, no other worktrees, no private data        |
| Edits allowed during research?   | no, research-only (this artifact only)                                 |
| Resolved evidence root           | .copilot-tracking/                                                     |

## Extension Registry and Provenance

| Kind        | Candidate                                   | Match and provenance                     | Selected / skipped reason |
|-------------|---------------------------------------------|------------------------------------------|---------------------------|
| Instruction | .github/copilot-instructions.md             | applyTo `**`                             | selected                  |
| Skill       | hve-builder, hve-builder-tester             | caller brief names them                  | selected for later stages |
| Skill       | web-design-guidelines and design skills     | no web files in scope                    | skipped                   |
| Specialist  | RPI Researcher                              | lanes are tightly coupled, low volume    | skipped; inline fallback  |

## User Participation and Research Decisions

| Checkpoint | Rationale                                       | Answers | Decision                  |
|------------|-------------------------------------------------|---------|---------------------------|
| Intake     | Non-interactive run; issue and brief are clear  | n/a     | proceed with balanced     |

## Prior Knowledge Gate

* First attempt (nonconforming): run-owned research file `.copilot-tracking/research/2026-11-08/issue-1294-validation-policy-research.md` (SHA-256 `7305e775...bf12d`) and log `/tmp/rpi-1294-validation-policy-1108.log`. It was produced without invoking the rpi-research bridge or persisting opening state first, and ran an unnecessary `find /`. It is preserved untouched, untracked, as adverse evidence. Its claims are starting points only; every finding below is re-verified here.
* Attempt-created ignored `tools/__pycache__/` preserved, not used as evidence.

## Direction Controls

| Control type | Direction                                              | Source        | Effect                       |
|--------------|--------------------------------------------------------|---------------|------------------------------|
| narrow       | no workflow/app/security/branch-protection changes     | caller brief  | reassess tier if research proves one necessary |
| exclude      | other worktrees, shared dirs, private data, heavy gate | caller brief  | none                         |

## Research Questions

| #  | Sub-question                                                                             | Type     | Priority | Status |
|---:|------------------------------------------------------------------------------------------|----------|----------|--------|
| Q1 | What do the hosted workflows trigger on, select and execute, including path filters?     | breadth  | H        | open   |
| Q2 | What do local `--all` and `--changed` run, skip, verify and receipt?                     | depth    | H        | open   |
| Q3 | Which guarantees are local-only; is the employee-chat browser selector and skip check in CI? | depth | H        | open   |
| Q4 | Which instruction/guide/agent text states or contradicts the gate policy?                | breadth  | H        | open   |
| Q5 | Contrarian: can CI replace local checks; what breaks if documentation-only skips the gate? | depth  | M        | open   |

## Research Cycle Log

### Cycle 1

* Active direction controls: no workflow/app/security/branch-protection change; worktree-only search.
* Posture: balanced; completion basis is scope coverage and adequate evidence for the named files.
* Explicit limits: none beyond the controls. Delegation: skipped; the lanes are tightly coupled and low volume, so all waves ran inline (fallback recorded, no worker ran).

#### Wave 1: Wider

* Surveyed the five workflows, `tools/ci-affected.py`, `tools/rpi-checks.py`, and every file that restates the gate policy (grep for `rpi-checks`, `local-rpi-gate`, `focused tier`).
* Hosted facts: Source projects CI (`src-ci.yml`) is the only PR-triggered source workflow and is path-filtered (C1). `mvp-ci.yml` (named "Source CI") and `mvp-validation.yml` are `workflow_dispatch` only (C2). `infra-plan.yml` runs after "Source projects CI" completes and only when `infra/` changed and a repository variable enables it (C3). The rubric workflow ignores only `.copilot-tracking/**` (C4). `ci-affected.py` selects projects, namespace and mssql from the diff and selects everything on any doubt (C5).
* Local facts: `--all` runs every group; `--changed` selects by path and treats `*.md` and `docs/`, `.copilot-tracking/`, `support/` as inert, always adding `preflight` and `static` and, through dependencies, `namespace` (C6, C7). `preflight` probes docker, az bicep, actionlint, shellcheck and Trivy, so a documentation-only `--changed` run still needs the heavy toolchain (C8).
* Policy statements: instructions say every candidate needs a local gate and the focused tier "(`--changed`) is the default" (C9). The guide and coordinator already say focused work needs relevant unit and focused tests only (C10, C11).
* Reflection: the contradiction is real but narrower than the issue suggests; the guide and coordinator mostly agree. The load-bearing question is which local-only guarantees disappear if `--changed` is dropped.

#### Wave 2: Deeper

* Employee-chat browser harness: local `browser` group runs `employee_acceptance_check`, the chat-panel selector with `ZF_BROWSER_TESTS=1` and zero-skip exact-test verification, the pinned axe download with SHA-256 check, `design_system`, `case_journey`, `employee_chat_browser_check` and a results validator that rejects any skip or missing state (C12, C13, C14). Hosted `src-api` runs `employee_acceptance_check`, `design_system`, `regulatory_ux`, `case_journey` and the same chat-panel selector with `ZF_BROWSER_TESTS=1`, but no workflow references `employee_chat_browser_check` and axe is not integrity-checked (C15, C16). So the selector name is shared, and CI does execute that test (the env var defeats `skipUnless`, a missing Playwright errors rather than skips: C17), but CI has no exact-count/zero-skip verification, and the employee-chat axe harness is local-only.
* SQL: local `SQL_SELECTORS` include `test_assistant_release.MssqlUnleasedRevocation` that the hosted `mssql` job omits, and the local gate requires named chat tests to report `ok`, not only skip-free (C18, C19). Hosted `mssql` runs only when `ci-affected.py` flags it.
* Other local-only guarantees: workflow hash drift in preflight, ShellCheck, exact Trivy DB identity, fresh-image rule for full receipts, shard fail-closed discovery, clean-snapshot and exact-head receipt binding, resume chain (C8, C20). Hosted-only: Trivy gate and SPDX SBOM upload, logo build, `no-working-data`, namespace/infra/Bicep jobs on selected diffs (C1).
* Truthfulness trap: a `src/**/*.md`-only change triggers Source CI, but `ci-affected.py` selects no project, so every `src-*` matrix job starts with `run: false` and reports success while skipping all steps; namespace and mssql are skipped (C21). A docs-only PR touching none of the path filter has no Source CI run at all. Neither is evidence that tests ran.
* Required checks: the active ruleset `mainprotect` lists `required_status_checks` with an empty list at retrieval (W1). So "applicable required hosted CI" means hosted checks that apply and actually executed for the head, as read from the PR, not a configured required context. This must not be changed here.
* Reflection: dropping `--changed` for small changes is safe only if relevant local-only guarantees are named and run directly. The employee-chat axe harness and exact skip verification are the concrete ones.

#### Wave 3: Contrarian

* Counter 1, keep `--changed` default: it gives one verified receipt and identical checks for every candidate. Rebuttal: for documentation-only candidates it needs docker, az, trivy, actionlint and shellcheck, takes the shared heavy-lock path and its inputs invalidate on any later commit, while the diff contains no executable input (C6, C8). The owner's D4 and the issue direct a lighter tier.
* Counter 2, rely on CI for small employee-chat changes: refuted by C15 and C16: the axe harness is not hosted. The brief requires direct local checks or moving it to CI; moving it is a workflow change the research does not justify.
* Counter 3, add a CI pass for docs: a documentation-only PR may legitimately have no Source CI; adding a workflow changes required hosted checks and is excluded.
* Counter 4, the rubric README step 3 and retention policy say "complete local gate": checked; step 3 is a specific rubric-score lifecycle for a source branch (C22) and the retention policy sentence is generic and would read as universal (C23). Only the generic sentence needs rewording; rubric README step 3 is scoped and left unchanged.
* Counter 5, mixed scope: `changed_groups` already returns the full matrix on any unmapped path, so a mixed diff cannot silently take a lighter local tier by selection, but the instruction-level tier is a human/coordinator decision, so the text must state strictest-wins explicitly (C7, C11).
* Reflection: no counter-evidence overturns the direction; it adds the requirements that the policy names local-only checks and the CI absent/skipped rule.

### Parent Synthesis (Cycle 1)

* Accepted: replace the blanket `--changed` default in `.github/copilot-instructions.md` with a tier table (targeted/focused, full) and the CI-truthfulness rule; mirror the same in `src/README.md` Local RPI gate (add a hosted-versus-local coverage table, local-only list and policy examples) and the coordinator's Local validation tiers (strictest wins, `--changed` optional, absent CI not a pass, local-only checks direct); reword `tracking-retention-policy.md` generic "complete local publication gate" to "selected-tier local publication gate".
* Rejected: changing `tools/rpi-checks.py`, workflows, `ci-affected.py`, branch protection or rubric README step 3 (scoped, not contradictory); moving `employee_chat_browser_check` into CI (workflow change, not proven necessary because direct local check is available).
* Deferred: the #470 timing measurement; a possible later issue to host the employee-chat axe harness in CI and to add zero-skip verification of the hosted chat-panel step.
* Alternatives: A) wording-only reconciliation (selected); B) wording plus new CI step (rejected, scope/tier escalation, needs owner approval); C) wording plus a tool flag for docs-only receipts (rejected, no receipt needed for the focused tier; tool change risks receipt verification).
* Tier: focused for the local gate (documentation/instruction only, no SQL, infra, deployed runtime or security control). HVE classification: Major (behavior-bearing instruction mutation), a separate axis.
* Re-entry decision: no further cycle needed; no substantial new finding in Wave 3 and sources are redundant.

## Policy examples to record and test (from the evidence)

| Case                                       | Expected local checks                                                                                                           | Hosted CI expectation (not a pass until observed)                                              | Never                                              |
|--------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|----------------------------------------------------|
| Documentation or instruction only          | Markdown/link review, Git diff, repository-wide scan for stale wording; HVE gates for behavior-bearing instruction artifacts    | Possibly no Source CI (path filter); `src/**/*.md` runs Source CI with no project selected      | blanket `--changed`; calling absent CI a pass      |
| Small employee chat/browser change         | Targeted unit tests, lint/types, `employee_acceptance_check`, chat-panel selector exactly one test zero skips, `employee_chat_browser_check` with the pinned axe | `src-api` runs the selector and four other checks; it does not run the employee-chat axe harness | treating hosted `src-api` as covering the harness |
| SQL                                        | Full tier                                                                                                                       | `mssql` job when selected                                                                      | partial receipt                                    |
| Bicep or security                          | Full tier                                                                                                                       | `src-namespace`, infra what-if if enabled                                                      | partial receipt, weakened control                  |
| Mixed (docs plus SQL/Bicep/security)       | Strictest tier                                                                                                                  | union                                                                                          | lighter tier by size                               |

## Evidence Log

| ID  | Evidence                                                                                              | Location                                                                    |
|-----|-------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| C1  | Source projects CI PR path filter, jobs and conditional jobs                                          | .github/workflows/src-ci.yml:3-6, 56-60, 203-206, 281-296                    |
| C2  | Legacy "Source CI" and validation are dispatch-only                                                   | .github/workflows/mvp-ci.yml:3-4; .github/workflows/mvp-validation.yml:3-4   |
| C3  | what-if follows Source projects CI, only when infra changed and variable enabled                      | .github/workflows/infra-plan.yml:5-8, 18-29, 35-46                           |
| C4  | rubric workflow ignores only tracking paths                                                           | .github/workflows/rubric-score.lock.yml:59-75                                |
| C5  | ci-affected selection and select-all-on-doubt                                                         | tools/ci-affected.py:1-9, 69-100                                             |
| C6  | `inert_path`, `changed_groups`, `required_groups`                                                      | tools/rpi-checks.py:554-571, 691-736                                         |
| C7  | unmapped path falls back to full matrix                                                               | tools/rpi-checks.py:731-732                                                  |
| C8  | preflight probes toolchain, workflow hash drift                                                        | tools/rpi-checks.py:2006-2026                                                |
| C9  | blanket-gate and `--changed` default wording                                                           | .github/copilot-instructions.md:72-75                                        |
| C10 | guide policy: focused uses unit and focused tests                                                      | src/README.md:61-66, 428-434                                                 |
| C11 | coordinator tiers, mixed takes full                                                                    | .github/agents/ama-backlog-delivery-coordinator.agent.md:449-471, 608-621, 676-684 |
| C12 | local browser group                                                                                    | tools/rpi-checks.py:2320-2433                                                |
| C13 | exact-test and skip verification                                                                       | tools/rpi-checks.py:1577-1630, 124-131                                       |
| C14 | employee chat results validator and axe hash                                                           | tools/rpi-checks.py:1555-1575, 82                                            |
| C15 | hosted browser step list                                                                               | .github/workflows/src-ci.yml:96-118                                          |
| C16 | no workflow references the employee chat harness                                                       | grep of `.github/workflows` and `tools` (matches only rpi-checks, its tests, docs, api README:775) |
| C17 | selector is `skipUnless` env var only; no `skipTest`                                                   | src/api/tests/test_chat_panel.py:837                                         |
| C18 | local SQL selectors                                                                                    | tools/rpi-checks.py:39-49                                                    |
| C19 | hosted mssql selectors lack MssqlUnleasedRevocation; required ok chat tests are local                   | .github/workflows/src-ci.yml:325-329; tools/rpi-checks.py:147-175            |
| C20 | receipt scope, resume, full-scope fresh-image rule                                                     | tools/rpi-checks.py:2957-3150; src/README.md:128-207                         |
| C21 | docs-only src md selects no project; matrix `run: false` still starts jobs                             | tools/ci-affected.py:80-100; .github/workflows/src-ci.yml:56-74              |
| C22 | rubric README step 3 scoped lifecycle                                                                  | .github/rubric/README.md:345-358                                             |
| C23 | retention policy generic wording                                                                       | docs/reference/method/tracking-retention-policy.md:13-15                     |
| W1  | active ruleset `mainprotect` has empty required_status_checks; branch protection 404 (retrieved 2026-11-08 via `gh api repos/jmservera/ama/rulesets/24504150`) | GitHub API, 2026-11-08 |

## Planning Readiness

* Research disposition: executed (one complete cycle; wider, deeper, contrarian; parent synthesis).
* Planning Readiness: Ready.
* Output mode convergence: selected alternative A, wording-only reconciliation of C9, C10, C11, C23 with the example table above. Out of scope for this change: C1 to C8, C12 to C19 (describe, do not alter).
* Nonconforming first attempt recorded; its artifact and log are preserved unmodified and not relied upon.
* Open items: whether to file follow-ups for hosting the employee-chat harness in CI and zero-skip verification of the hosted selector; the #470 timing remains unmeasured.

## Self-check

* Opening state persisted before the first substantive search: yes for this artifact; the preceding `rpi-checks.py` and workflow reads occurred after creation. Earlier `git status`, issue fetch and template reads were intake only.
* Read-only: yes; only this research file written. Findings cite `path:line`; the one external fact is a point-in-time API read (W1), to be rechecked before publication.
