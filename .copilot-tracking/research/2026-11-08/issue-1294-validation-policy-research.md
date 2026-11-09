<!-- markdownlint-disable-file -->

# Task Research: issue-1294-validation-policy

| Field              | Value                                                                           |
|--------------------|---------------------------------------------------------------------------------|
| Date               | 2026-11-08                                                                      |
| Researcher / agent | rpi-research (native RPI session; also the hve-builder `rpi-research` bridge)   |
| Status             | Complete                                                                        |
| Artifact path      | .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-research.md |

## Research Brief

* What to research: how hosted Source CI (`.github/workflows/src-ci.yml`) and the local gate (`tools/rpi-checks.py` `--all` and `--changed`) actually select and execute checks, which guarantees are local-only, and which current instruction or guide text contradicts the owner's lighter-validation direction (issue #1294).
* Why it matters: decides what the policy may relax (blanket `--changed` for small and documentation-only candidates) without losing coverage, and which text must change.
* Audience: the plan, the hve-builder (improve, Major) lifecycle, the independent reviewer and the coordinator.
* Scope: `.github/copilot-instructions.md`, `src/README.md#local-rpi-gate`, `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `.github/workflows/*.yml`, `tools/ci-affected.py`, `tools/rpi-checks.py`, GitHub rulesets (read-only API).
* Non-goals: any workflow, runner, application, security-control or branch-protection change; measuring the #470 full-gate timing (separate, unmeasured, not closed here); running a full gate, Docker or any heavy gate (the approved cleanup owns `/tmp/ama-rpi-heavy.lock`).
* Criteria: every claim cites a file and line or a read-only command output retrieved 2026-11-08; absent, path-filtered or skipped CI is never recorded as a pass.
* Output mode: convergence (recommend a bounded documentation-only policy change).

## Research Parameters

| Field | Value |
|---|---|
| Research posture | balanced (bounded internal task, named sources, but a policy decision with safety consequences) |
| Posture provenance | default |
| Explicit limits | no heavy gate, no install, no private data, no other worktree |
| Evidence root | `.copilot-tracking/` default |
| Source identity | HEAD and `origin/main` both `fa7ae0c9770e890f82482456bfcb8e97f1e05429`; branch `docs/validation-policy-1294`; worktree clean at start |

## Extension Registry and Provenance

| Kind | Candidate | Match | Decision |
|---|---|---|---|
| Instruction | `.github/copilot-instructions.md` | `applyTo: **` | selected: documentation, branch, knowledge-base and regulatory conventions (this task changes the instruction itself) |
| Skill | `hve-builder`, `hve-builder-tester` | behavior-bearing instruction change, owner-required | selected: improve mode, Major |
| Skill | `rpi-research`, `rpi-plan`, `rpi-implement`, `rpi-review` | owner-required loop | selected |
| Skill | web guidelines, design-taste | no web file changes | skipped: backend/doc only |
| Specialist | `RPI Researcher` lanes | investigation is one tightly coupled trace across about six files | skipped, inline (delegation would add latency without isolation benefit) |

## Evidence

IDs are stable for the plan. Wave tags: W1 wider, W2 deeper, W3 contrarian.

### C1 Hosted Source CI trigger and selection (W1, W2)

* `src-ci.yml` runs on `pull_request` only for the path filter on its line 4: `src/**`, `infra/**`, `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, `tools/ci-affected.py`, `tools/test_ci_affected.py`, `tools/install-actionlint.py`, `tools/test_install_actionlint.py`, `tools/backlog-sync.py`, `tools/test_backlog_sync.py`, `tools/rename-zava*`, three named synthetic-data/DPIA/journey documents, `support/synthetic-data/**`, and five workflow files. A PR that changes only other documentation (`docs/**`, `.github/*.md`, `.github/agents/**`, `.copilot-tracking/**`) starts no Source CI run. Absence is not a successful check.
* `mvp-ci.yml`, `mvp-validation.yml` and `src-deploy.yml` have `workflow_dispatch` only (never run on a PR). `infra-plan.yml` is a `workflow_run` consumer of a successful Source CI pull request run, so it also does not run when Source CI is absent. `rubric-score.md` runs on PRs to `main` with `paths-ignore: .copilot-tracking/**`; it is a rubric score, not a code check.
* `tools/ci-affected.py` (`select`) is fail-open. Within `src/`, a Markdown file directly in `src/` or in a project root selects no project and no namespace job. Any path outside `src/` that is not one of the namespace-only tool paths returns "everything" (all five projects, namespace and mssql). Therefore once any one filtered path triggers Source CI, an accompanying `docs/`, `.github/` or `.copilot-tracking/` path widens the hosted run to the full project matrix. Retrieved by calling `select()` on sample paths (read-only, 2026-11-08): `src/README.md` with `.github/agents/*.md` selected all five projects, namespace and mssql. A `src/README.md`-only PR would select none, so every `src-<project>` job would report success with every step skipped (`matrix.run` false). That is a skipped job, not an executed check.
* `project` matrix steps are individually guarded by `matrix.run`. The five-step browser sequence (employee acceptance, design-system, regulatory axe, case-journey, and the chat-panel selector) runs for the `api` project whenever `api` is selected, including for a `core` change. Image build, container contract, Trivy and SPDX run only when `infra/scripts/pipeline.py changed-images` lists the project. The `namespace` job runs install-all-five, compile, `node --check`, Bicep build and lint, infra tests, tooling contracts, branding regression and actionlint. `mssql` runs the real SQL Server contracts only when selected.
* GitHub enforcement (read-only `gh api`, 2026-11-08): classic branch protection returns 404 (not protected). Ruleset `mainprotect` (active) has `deletion`, `non_fast_forward`, `pull_request` (0 required approvals) and `required_status_checks` with an empty list. Ruleset `main` is `disabled`. So no named hosted check is currently enforced by GitHub; "required hosted CI" is owner policy that a human or the coordinator must verify from the actual run list. Recent docs-only PRs (for example #1290, #1285, #1272, #1269) show an empty check list, and #1286 (which touched a named path) shows the full `src-*` set, which matches the filter analysis. Branch protection and rulesets are not to be changed here.

### C2 Local gate coverage and local-only guarantees (W1, W2)

* `required_groups` (`tools/rpi-checks.py` line 554): `preflight`, `project-*`, `namespace`, `static`, `infra`, `migration`, `browser`, `mssql`, `image-*`, `logo-0600`. `--all` runs them all. `--changed` (`changed_groups`, line 691) always selects `preflight` and `static` (transitively `namespace`) and then per path: inert paths (`.md` anywhere, `docs/`, `.copilot-tracking/`, `support/`) add nothing; `tools/rpi-checks.py` and its test add `tooling`; `infra/` adds `infra`; `src/<project>/` adds dependent projects, images for runtime/build inputs, `browser` for `src/api` web or checks, `mssql` for store, schema, SQL, assistants or requirements inputs. Any other path (for example a workflow or other tool) falls back to the full list.
* Retrieved selections, 2026-11-08, from calling `changed_groups` (read-only): documentation-only, `.github/agents` and `src/README.md` selected `preflight, namespace, static`; `src/api/.../web/app.js` plus a chat test selected `project-api, browser, image-api, logo-0600` plus the universal groups; a `src/core` store file selected every project, every image, `mssql`; `infra/main.bicep` selected `infra`; a workflow file selected the full list. Mixed `docs` plus Bicep selected `infra` (inert paths never lower a selection).
* The runner embeds a hosted-to-local coverage map (`coverage_rows`, line 2268): `project` maps to `project-*; browser; image-*; logo-0600`, `namespace` to `namespace; static; infra; migration`, `no-working-data` to `static`, `mssql` to `mssql`; `src-deploy`, `infra-plan`, path context, artifact upload are recorded as hosted-only.
* Local-only execution and verification guarantees (not present in hosted CI): receipt binding of HEAD, tree, base and tool identity and `--verify-receipt`; clean, untracked and ignored-input refusal; heavy-lock admission and cgroup-capacity workers; ShellCheck as a required preflight dependency; pinned axe SHA-256 identity; exact check counts (employee acceptance `expected_count=3`, line 1408 and 1876); fresh image build for full scope; Trivy database metadata binding; fail-closed unknown-skip parsing.
* Chat-panel browser selector: `src/api/tests/test_chat_panel.py` line 837 `@unittest.skipUnless(os.environ.get("ZF_BROWSER_TESTS") == "1", "opt-in local Chromium")` for `PanelTests.test_browser_warning_failure_keyboard_refusal_and_live_log`. Hosted CI runs exactly `ZF_BROWSER_TESTS=1 python -m unittest -v test_chat_panel.PanelTests.test_browser_warning_failure_keyboard_refusal_and_live_log` (src-ci line about 100, `api` and `matrix.run` only), so with the variable set it executes and a failure fails the step. The hosted step does not verify "exactly one result, one test, zero skips" and would pass vacuously if the variable or selector were later removed from the command. The local runner records the verbose log, requires one verbose successful result for that ID, one reported test and zero skips (`src/README.md` lines about 325-340). The hosted ordinary `unittest discover` run leaves the test skipped by design. So the selector is covered hosted when the api project runs, and the stricter skip verification is local-only. This corrects the premise "CI does not name it": it does name it.

### C3 Current wording and contradictions (W2)

* `.github/copilot-instructions.md` lines 72-75: "Every final RPI candidate, including documentation-only work, requires a local gate ... The focused tier (`python3 tools/rpi-checks.py --changed`) is the default." This makes `--changed` a blanket requirement and conflicts with the owner direction and with the two downstream texts below. It also states the complete gate is required "only" for the listed categories, then immediately requires full-gate steps without tier gating in the same paragraph.
* `src/README.md` "Local RPI gate" (lines about 66-76): "small issues, tooling and documentation use planned unit and focused tests, with hosted CI still required" (consistent with the owner direction), but its next paragraphs present `--changed` as the small-issue command with no statement that it is optional, no CI path-filter reconciliation and no tier examples. The gate-speed section says timings are "not yet recorded" (#470, unchanged).
* `.github/agents/ama-backlog-delivery-coordinator.agent.md` "Local validation tiers" (lines about 449-460) already says focused work requires "relevant unit and focused tests only"; "Focused runs may use `--changed`" (optional wording). Lines about 744-757 (receipt refresh) only concern a partial receipt when one exists. Remaining gap: no statement of path-filtered or skipped CI, no local-only preservation rule, no example table.
* `docs/reference/research/delivery-bottleneck-analysis-2026-10-31.md` D4 is dated history (approved 2026-11-01, "the focused tier is the default local gate"). It is historical evidence, not a current instruction; do not edit it. The D4 text also appears to say the focused tier means `--changed`; the owner's 2026-11-08 direction (issue #1294) refines it. Record this as a refinement in the knowledge-base log, not by rewriting history.

### C4 Local-only coverage to preserve with direct checks (W2, W3)

| Local-only behavior | Applies when | Direct local check without a blanket `--changed` | Hosted substitute |
|---|---|---|---|
| Exact chat-panel browser selector with skip verification | a change to `src/api` web, `chat_panel`, assistants UI or `checks/` | run the selector with `ZF_BROWSER_TESTS=1 -v`; require `Ran 1 test`, `OK`, no `skipped` | hosted executes the selector when `api` runs, without the skip assertion |
| Employee acceptance and axe browser checks | same | the `checks.employee_acceptance_check` command and the axe checks | hosted browser step for `api` |
| Real SQL contracts | store, schema, SQL, requirements | full tier (SQL) | hosted `mssql` when selected |
| Receipt, clean-tree, ignored-input refusal | full tier | `--all`, external receipt, `--verify-receipt` | none (local-only) |
| ShellCheck and actionlint parity | workflow or shell changes | out of focused scope (workflow change) or `--changed` selection | hosted namespace job |
| Doc-only link and diff review | any docs | Markdown link check and `git diff --check` | none (no Source CI for pure docs) |

### C5 Contrarian findings (W3)

* Risk: calling a docs-only change "covered by hosted CI" is false because the path filter starts no Source CI. Mitigation: policy text says a docs-only candidate's evidence is its planned local checks plus whatever hosted runs actually exist; absent CI is `not triggered`, never `passed`.
* Risk: a PR that changes `src/README.md` and also any non-src path widens hosted CI to the full matrix (fail-open), and a PR with only `src/README.md` yields skipped (not executed) project jobs. Mitigation: policy requires the handoff to list per-job outcomes, distinguishing `success`, `skipped` and `not triggered`. This candidate itself changes `src/README.md` and tracking paths, so expect the full hosted matrix; the local focused tier does not predict hosted results.
* Risk: relaxing the blanket `--changed` could drop the browser skip verification. Mitigation: that guarantee is retained as a direct targeted check and remains in `--all`/`--changed` for browser selections; nothing in the runner changes.
* Risk: "small" is subjective. Mitigation: tier by category (not size). Anything touching SQL, infrastructure/Bicep, deployment, security controls, releases or a major feature takes the full tier; mixed takes the strictest; unmapped paths that `--changed` expands to the full list are reported, and the full tier applies only when a full category applies.
* Counter-evidence against moving checks into CI instead: path-filtered docs workflows, zero enforced required checks and cloud cost make hosted CI unsuitable as the sole control for docs; changing workflows is out of scope.
* Alternative rejected: add a docs job to Source CI (workflow change, shared-state risk, out of scope). Alternative rejected: tests in `tools/` that pin the policy examples (extends the tooling/Source CI surface; behavior is verified instead through the hve-builder simulation and the retrieved selection evidence).

## Recommendation (convergence)

Documentation-only change to three current files, focused tier:

* `.github/copilot-instructions.md`: replace the blanket paragraph with a tier-based policy (focused default for small, tooling and documentation; full for the listed categories; mixed strictest); keep full-tier steps, external receipt, review, human and shared-resource rules; add the CI truthfulness rule.
* `src/README.md`: in the Local RPI gate section, state the tier policy and add the CI-versus-local reconciliation, the local-only inventory and the testable example table; keep the `--changed` mechanics, labelled optional.
* `.github/agents/ama-backlog-delivery-coordinator.agent.md`: align the focused bullet, add the CI-truthfulness handoff rule and example pointer, without changing the full tier or receipt rules.
* Knowledge base: append a `docs/reference/log.md` entry; no index change (no new knowledge-base file) unless the index lists the instruction text. Do not edit the dated D4 history.
* Add `.copilot-tracking/github-issues/issue-1294.md`.

Tier: focused (instruction and guide only; no SQL, infrastructure, deployment, security control or major feature). HVE classification of the instruction mutation: Major (decision rules and stage gates change). These two classifications are independent.

## Planning Readiness

Ready. Research disposition: executed. Open items for the plan: exact wording; hve-builder baseline, static review, Major behavior simulation (contained, no native destructive execution) and host validation; per-job hosted-outcome wording; #470 timing stays unmeasured and open.

## Not run and limitations

* No full gate, Docker, Chromium, SQL, Azure or provider call was run or is claimed; hosted CI has not run for this candidate.
* The sample selections were computed by importing the two selector modules read-only; they describe selection logic, not CI results.
