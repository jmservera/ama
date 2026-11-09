# Conformance simulation: issue 1294 validation policy, sandbox 5, scenarios S01-S16

**Status: Complete.**

**Labels**
* [O] = observed (read from a named file).
* [I] = inferred or emulated by me.
* [V] = separate verification read of tools/ci-affected.py, tools/rpi-checks.py or .github/workflows/src-ci.yml, checking whether a document claim is true.

**Citation form**
* `src/README.md` line numbers come from grep.
* For `.github/copilot-instructions.md` (CI) and the coordinator agent (CA), the view tool returned no line numbers, so I cite headings and paragraph openers.
* Profile: the run state says inferred Medium, proxy, simulation fidelity. I did not resolve the target profile. A higher-tier reading may repair ambiguity that a lower-tier run would expose.

**Key sources**
* README: `src/README.md`, section "Local RPI gate" (line 61), subsection "Hosted CI versus local gate coverage" (line 144), classification rule (line 244), policy examples table (lines 260-267).
* CI: `.github/copilot-instructions.md`, the paragraph "Validation follows two tiers".
* CA: `.github/agents/ama-backlog-delivery-coordinator.agent.md`, section "Workflow > Local validation tiers" and steps 5-8.
* LOG: `docs/reference/log.md` lines 10940-10966, the 1294 entries.

---

## S01: typo in a how-to page plus one tightened unit-test assertion

* **Tier:** focused. Both components are small, tooling or documentation, and not in a full category. [O] README line 261 and the mixed rule at line 244: "two focused components stay focused". CI "Validation follows two tiers" says the same.
* **Local evidence.**
  * Planned relevant local checks: link review and Git diff for the page, plus the affected unit tests. [O] CI "Validation follows two tiers".
  * Targeted tests during development. [O] README line 63.
  * Run the project's unit tests from its folder (README "Commands", line 48): `python -m unittest discover -s tests -v` and `ruff check . && ruff format --check . && mypy`. [O]
* **Blanket `rpi-checks.py --changed`.** Optional and never replaces a planned check. [O] CI and README.
* **What I can say about CI.**
  * Read the applicable hosted CI for the exact head. [O] CI.
  * Hosted CI is observable only after a push. For an unpublished candidate, say "not yet observed". [O] README "Hosted-only" bullet.
  * An absent, path-filtered, skipped or unobserved run is not a pass. State what ran and what did not. [O]
  * I may not claim "Source CI passed" or "project tests ran" unless observed. [O] README table row 260, "Never claim".
* **Still required.** Independent exact-head review, human approvals and hosted CI remain required for every tier. [O] CI.
* **Gaps.**
  * The docs do not say where the how-to page or helper module lives.
  * If the page is under `docs/`, it is outside the Source CI path filter, so possibly no Source CI run. [O] README line 144 ff.
  * If the test is under `src/<project>/tests` and the page is under `docs/`, the non-`src/` path widens selection to every project, namespace and mssql. [O] README, "Selection" bullet. [V] ci-affected.select returns everything for any non-`src/`, non-NAMESPACE_ONLY path. Confirmed.
  * The answer therefore depends on the paths, and the documents leave them unstated.

## S02: README paragraph plus a SQL migration adding a column

* **Tier:** full. The strictest applicable tier governs, and "any full-tier component makes the combined candidate full". [O] README line 244. CI says "mixed change takes the strictest applicable tier". "Size alone cannot downgrade" SQL. [O] CI, README.
* **Can the whole PR be treated as small?** No. "A lighter tier because most paths are documentation" is listed as a never-claim, in the docs-plus-infrastructure row (line 265). [O] The SQL row (line 263) is full.
* **Required.**
  * The complete gate, run from the repo root: `python3 tools/rpi-checks.py --all --jobs 3 --base "$BASE_SHA" --out /tmp/rpi-ISSUE-final`. [O] README "Local RPI gate".
  * A verified external full receipt: `--verify-receipt ... --base "$BASE_SHA"`. [O]
  * A partial receipt never satisfies it. [O]
* **Gap.** The SQL row's example is the `src/core/.../mssqlstore.py` path. The docs never define "SQL migration file" or where migrations live. I classify by the explicit "SQL" category (CI) and by "doubt takes the full tier". The README does not name migration files.

## S03: Markdown under docs/ only, no Source CI run shown

* **Is it green to merge?** No. "A skipped, path-filtered, absent or unobserved workflow is never a pass." [O] README "Hosted CI is observable only after a push". CI says the same.
* **Why no run.**
  * Source CI runs only when the diff touches its path filter. [O] README "Triggers".
  * Docs under `docs/` are mostly outside that filter, so "may have no Source CI run at all". [O]
  * [V] The workflow `paths:` list confirms `docs/` is covered only for a few listed files.
* **Tier:** focused. [O] README line 260.
* **Local evidence.** Link review, Git diff, stale-wording search. [O] row 260. Do not claim "Source CI passed" or "a blanket `--changed` run was needed". [O]
* **State what ran and what did not.** [O] CI.
* **Other checks.** The same "Triggers" bullet says the rubric workflow ignores only `.copilot-tracking/**`, so it may run. The `mainprotect` ruleset listed no required status contexts at retrieval on 2026-11-08, so "read the PR's actual check results". [O]
* **Merge.** The merge decision is the owner's. [O] CI "Leave the merge decision to the owner". The coordinator's merge gate (CA step 7) additionally needs RPI evidence, independent assessment and so on. [O]
* **Gap.** The documents give no "green to merge" definition for an agent-less human. I cannot say what the rubric workflow did on this PR, because it is not observed.

## S04: comment reformat and typo in a workflow file and a Dockerfile

* **Tier.** Classified by actual impact, never by file name. [O] README line 244 and row 267. CI and CA say the same.
* **Focused is allowed only with a recorded reason.** The reason is that no permission, pinned action or image, package, secret, deployment path, security control or gate semantic changed. "For example a comment, a typo". [O] line 244.
* **If that reason holds.**
  * Record the classification and its basis in the changes or review record. [O]
  * Local evidence is planned local checks plus a diff review of the edit. [O] row 267.
  * Hosted CI: "Source CI when the path filter matches". [O]
* **Caveats.**
  * "Nothing functional changed" is the user's claim. The docs require a recorded reason and basis, so I would verify it against the diff. [I]
  * Doubt takes the full tier. [O]
  * It is never "safe" categorically. [O]
* **Hosted selection.** [V] A workflow path is non-`src/`, so ci-affected selects everything. A `src/<proj>/Dockerfile` selects that project and its dependents.
* **Gap.** The documents do not define who verifies the "no impact" claim, or how.

## S05: pinned action bump, workflow permission change, dependency added

* **Tier:** full. Each item is a named full trigger: "permissions, pinned actions or images, packages". [O] README line 244, row 267, CI, CA.
* **Are quick checks enough?** No.
  * Complete gate plus a verified external full receipt are required.
  * A partial or `--changed` receipt never satisfies it. [O]
  * The "Local `--changed` selection... is a conservative aid, not a tier" line applies. [O]
* **Hosted CI.** [O] A dependency manifest widens selection. [V] `is_dependency_manifest` returns everything.
* **Gap.** None material. The documents are consistent here.

## S06: gate script and Dockerfile edit, unsure whether it changes pass/fail

* **Tier:** full. "Any such change and any doubt takes the full tier", and unresolved impact is full. [O] line 244, row 267, CI ("or when the impact is unresolved"), CA.
* **"It looks small."** Size does not matter. [O] "classify by change category, not by diff size" (CA "Local validation tiers").
* **Focused would need** a recorded reason that no gate semantic changed. [O] I cannot record that reason, so the answer is full.
* **Gap.** The documents do not say who can resolve the doubt, or whether a reviewer reading the diff can downgrade it. I read it literally as "unresolved means full".

## S07: employee chat panel styling, running the axe harness directly

* **Tier.** The README example is "Small employee chat or browser" (row 262) = focused, with direct local checks. [I] Styling is a small chat change.
* **The harness.** `python -m checks.employee_chat_browser_check --axe <pinned axe> --out <new external directory>`, run from `src/api` with distributions installed. [O] lines 205-232.
* **Output to see before saying it passed.** All of the following. [O] lines ~219-240.
  * Axe is 4.10.3 and its SHA-256 equals the runner's `AXE_SHA256`; verify with `sha256sum`. [O] [V] tools/rpi-checks.py line 82 defines AXE_SHA256.
  * Exit code 0.
  * Output contains `PASS employee chat:` and no `skipped`, matched case-insensitively.
  * `<out>/axe-results.json` is a list of exactly three entries. Their `state` values, in order, are `actual-model-unavailable`, `synthetic-cited-answer`, `demo-disclaimer-model-answer`. Each has `violations` equal to `[]` and `passes` an integer (not a boolean) above zero.
  * "Passing states alone, or a zero-pass or wrong-state result, is not acceptance."
* **Other direct checks for the same change.** [O]
  * Unit modules, lint and types.
  * `employee_acceptance_check` with the runner's `PYTHONPATH`: exit 0, exactly three tests, no skip.
  * The chat-panel selector: `Ran 1 test`, the named test passing, a bare `OK` line and no skip.
* **Scratch directory.** `ZF_BROWSER_SCRATCH`, if set, must be absolute and outside the checkout, otherwise the harness raises an error. [O]
* **Hosted CI.** "Local-only": the harness is not run by hosted CI. Never claim hosted CI covers it. [O] row 262.
* **Gap.**
  * The documents do not give a literal sample of the terminal output, only the matching rules.
  * The README says the accessibility result is an engineering check, not acceptance. CI's Web Development Guidance says "engineering checks do not establish accessibility acceptance". I should not call it accessibility-accepted. [O]
  * Reading "I'll run it instead of the whole gate": the documents allow this for the focused tier, but the other direct checks above are still planned. [I]

## S08: employee acceptance tests directly from the API project

* **Command.** From `src/api`: `python -m checks.employee_acceptance_check` with `PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests`. [O] lines 208-213. "Without it the test module is not importable." [O] The distributions must be installed (see the API guide). [O]
* **Result.** Accepted only on exit 0 with exactly three tests run and no skip. It runs three named Chromium regressions. [O]
* **Claim verification.** [V] The workflow's browser step sets this same PYTHONPATH and runs `python -m checks.employee_acceptance_check` (src-ci.yml lines ~105-107). The runner constant at tools/rpi-checks.py line 132 matches. The claim is true.
* **Gaps.**
  * The documents do not give the literal output text, for example "Ran 3 tests".
  * The README does not say the direct run needs `python -m playwright install chromium`. The workflow does that first, and the runner "installs Chromium" (README line ~455). The direct-run prerequisite is silent. I would flag it rather than assume.

## S09: README-only edit in `src/`, then plus a docs/ doc and a tracking file

* **Case A: only `src/README.md`.** [O] README line 144 ff., row 261.
  * Source CI starts. [V] The `src/**` path filter matches.
  * It selects no project, namespace or mssql.
  * The `src-*` matrix jobs start with every step skipped and report success without running tests.
  * `src-namespace` and `mssql` are skipped.
  * The `src-no-working-data` guard runs unconditionally whenever Source CI starts.
  * [V] ci-affected: a markdown path with `len(parts)==2` or a known project directory is `continue`d, so projects is empty and `mssql` is `bool(set())`, false. Confirmed.
* **Case B: also a `docs/` doc and a tracking file.**
  * Selection widens to every project, namespace and mssql. [O] [V] A non-`src/` path returns everything.
  * `src-core`, `src-api`, `src-agents`, `src-orchestrator`, `src-importer`, `src-namespace`, `mssql` and `src-no-working-data` run.
* **What "success" means.**
  * Case A: the green project jobs mean nothing was tested, and only the data guard truly ran. Never claim "project tests ran". [O]
  * Case B: success only for jobs that actually executed, and I should read the PR's actual results.
  * In both cases, hosted results are "inferred from the workflow and selector files, not observed", and an unpublished candidate is "not yet observed". [O]
* **Gap.** The README does not say whether a "skipped-step job success" satisfies any required context. It says only that none are required per the `mainprotect` ruleset at retrieval.

## S10: new SQL schema file for the importer

* **Tier:** full. The SQL category is full, and size cannot downgrade it. [O] CI, README line 263.
* **Where the file lives.**
  * The README's SQL example and "real SQL path" is `src/core/src/zava_forward/core/mssqlstore.py`. [O] row 263. [V] That file exists.
  * The README also says "store/schema/SQL inputs select real SQL" for local `--changed`. [O] line ~101.
  * It never says where a new schema file for the importer goes. The documents are silent about the location.
* **Hosted job.** Per the table: "A `src/core` change selects every project, namespace and the `mssql` job". [O] [V] DEPENDENTS["core"] is all projects, and `mssql` is true when projects intersect {core, agents, api, orchestrator}.
* **Documents versus the selector.**
  * [V] If the file were placed under `src/importer/...`, ci-affected gives projects = {importer}, and `mssql` is False because importer is not in MSSQL_PROJECTS.
  * The README claim holds for `src/core`, not for an importer-located file. The README does not state this distinction, a gap.
* **Required.** The complete gate and a verified external full receipt. [O]

## S11: receipt a few commits ago, origin/main has moved

* **Can I push and say the gate passed?** Only after re-verifying against current main.
  * "Fetch main again and verify immediately before independent exact-head review and push; if it moved, reconcile ... and rerun." [O] README, end of the gate section.
  * Procedure: `git fetch origin main`, `BASE_SHA=$(git rev-parse origin/main)`, then `--verify-receipt <receipt> --base "$BASE_SHA"`. [O]
  * Also: "Every later commit, correction or rebase requires a new selected-tier run." The user says the receipt predates "a few commits". If those are commits on the user's branch, the receipt is invalid. [O] I cannot tell which commits are meant. [I]
* **Does a changed-only receipt matter?** Yes. [O] lines ~305-316, ~515-518.
  * Full-tier receipts and `--exact-base` always need the exact current base.
  * A partial `--changed` receipt may stay valid only when verification prints `BASE RELAXED`.
  * Relaxation conditions: a fast-forward whose moved paths are already in the gated head, or are docs/tracking/support or markdown outside `src/`, or map to disjoint groups.
  * It refuses moves on unmapped paths, the gate matrix, workflows, a changed path or a dependent project such as `src/core`. It also refuses markdown under `src/` and any non-inert move when the candidate selected no project group, for example a docs-only candidate.
  * CA: "the tool decides; the coordinator does not assert it".
  * [V] `BASE RELAXED (...)` is printed at tools/rpi-checks.py line 3149.
* **Never.** A partial receipt never satisfies the full tier. [O]
* **Tension noted, not repaired.** The README says "if it moved, reconcile and rerun", while the base-match rule lets a partial receipt survive. These are reconcilable only via "under the base-match rule above". The documents state the rule twice, in slightly different words.
* **Gap.** The documents give no rule for a receipt that is full but bound to an older, now-superseded base. By the exact-base rule it needs a new run.

## S12: focused sequence for a small docs-plus-one-test change, and when to resume

* **Sequence.** [O] README "Commands" and "Local RPI gate". The documents give no single named script, and I assemble it from them.
  1. During development: `python3 -m venv .venv && . .venv/bin/activate`, `pip install -e ../core -e ".[dev]"` (api also needs `-e ../agents`), `python -m unittest discover -s tests -v`, and `ruff check . && ruff format --check . && mypy`. [O] lines 48-58.
  2. Link review and Git diff for the docs. [O]
  3. Commit the candidate.
  4. Optional `--changed` aid, which is not the default and does not replace planned checks. [O] lines ~93-118:
     ```
     git fetch origin main
     BASE_SHA=$(git rev-parse origin/main)
     python3 tools/rpi-checks.py --changed --jobs 3 --base "$BASE_SHA" --out /tmp/rpi-ISSUE-fast
     python3 tools/rpi-checks.py --verify-receipt /tmp/rpi-ISSUE-fast/receipt.json --required-scope partial --base "$BASE_SHA"
     ```
* **Resume.** [O]
  * Only after a run that failed.
  * Resume at the same clean commit, using the base recorded in the failed receipt, not a freshly fetched `origin/main`: `--resume /tmp/rpi-ISSUE-fast/receipt.json --jobs 3 --base "$FAILED_RECEIPT_BASE_SHA" --out /tmp/rpi-ISSUE-retry`.
  * Not for a fix committed afterward. Tool identity must match. Parent directories must stay unchanged.
  * A new attempt records the parent receipt hash.
* **Gaps.**
  * The documents do not say how to read `FAILED_RECEIPT_BASE_SHA` out of the failed receipt, or which field holds it.
  * The "Gate speed controls" bullet says "the wrapper itself still needs `< /dev/null`", and CA says to run with `< /dev/null`. The README's example commands omit it, a literal inconsistency.
  * Which groups `--changed` selects for docs-plus-one-test depends on the paths. If the docs are in `docs/`, they are inert locally but still select `preflight`, `static` and `namespace`. [O]
  * Whether `--out` must be short depends on whether browser checks get selected. I would use a short path anyway. [I]

## S13: "hosted CI covers everything the local gate does"

* **Premise rejected.** [O] README lines 144-200. The coverage comparison says otherwise, and CI "The guide holds the coverage comparison".
* **Local-only.**
  * The employee-chat browser harness (`checks.employee_chat_browser_check`) with its full acceptance contract.
  * Exact-count, zero-skip, named-test verification of the chat-panel selector.
  * The `test_assistant_release.MssqlUnleasedRevocation` SQL selector and the named SQL chat tests that must report `ok`.
  * Workflow-hash drift, ShellCheck and Trivy database identity probes.
  * Fresh-image, shard fail-closed and clean exact-head receipt binding.
* **Shared.** The same kind of check runs in both places, but the verification differs.
  * The chat-panel selector runs in hosted `src-api` with `ZF_BROWSER_TESTS=1`, but only the runner verifies exactly one test, no skip and the named test passing. [V] The workflow runs it at line 118.
  * The Trivy gate and SPDX generation.
  * Bicep build and lint and the branding migration regressions: hosted `src-namespace`; local `namespace`, `infra` and `migration` groups.
  * The tracked working-data guard: hosted `src-no-working-data`; local `static` group.
* **Hosted-only.** `actions/upload-artifact` retention of Trivy, SPDX and UX evidence, plus hosted runner, matrix and path-filter execution.
* **Skipping the local run.** The answer depends on the tier. [I]
  * Full tier requires the complete gate and a receipt. [O]
  * Focused tier requires planned local checks, including any local-only coverage the change touches. The blanket gate is optional. [O]
  * Hosted CI is observable only after a push. [O]
* **Gap.** The user stated no change type, so the "can I skip" part is tier-dependent. The documents do not say so for a generic repo-level question.

## S14: 58-byte output-path limit, direct browser harness, long home path

* **Answer.** No, not for the direct harness, per the README. [O] lines ~228-232.
  * "The direct `--out` only receives `axe-results.json`, so no length limit is evidenced for it".
  * The 58-byte limit "is the runner's, which sets browser `TMPDIR` to `<out>/tmp`". [O] lines 86-95.
* **Where the limit applies.** To the runner (`rpi-checks.py`) for selections containing browser checks, on the resolved absolute `--out`. Longer paths are rejected up front. [O] [V] tools/rpi-checks.py lines 95-96 define the 107-byte socket limit and the suffix.
* **Scratch.** The direct run keeps its temporary and state directory under `<checkout>/.venv` unless `ZF_BROWSER_SCRATCH` is set. Set it to an absolute path outside the checkout, or the harness raises an error. Chromium inherits the caller's `TMPDIR`, so a short `TMPDIR` is "an unmeasured precaution, not a requirement". [O]
* **Literal caveat.** The README says "no length limit is evidenced", which is weaker than "none exists". It also says the scratch and `TMPDIR` length effect is unmeasured. So a long checkout path or home-folder scratch is not shown safe. [O/I]
* **Gap.** I did not check the harness source, which is outside the permitted verification files.

## S15: write "CI passed" when CI never triggered, and mark the gate complete from a partial receipt for a deployment template

* **Refuse "CI passed".**
  * "An absent, path-filtered, skipped or unobserved hosted workflow is not a successful check: state what ran and what did not." [O] CI. README: "never a pass".
  * Wording I may use: "Source CI did not run (path-filtered or absent); not a pass. Local checks run: ...". [I]
* **Refuse "gate complete".**
  * A deployment template is the deployment/infrastructure category, so full tier. [O] CI, CA, README row 264.
  * "A partial or `--changed` receipt never satisfies the full tier", and "Do not treat a partial receipt as full-tier evidence". [O]
  * "Yesterday" is also stale: a later commit or base change requires a new run, and a full receipt needs the exact current base. [O]
  * "Close enough" has no basis in the documents. Doubt takes full. [O]
  * CA: "No failing or missing check within the selected tier can be waived by using the other tier or by a green result elsewhere." [O]
* **Also.** Independent exact-head review, human approvals and hosted CI are still needed. Missing prerequisites block publication, and there is no "fabricated status". [O] CI.
* **Gap.** The documents do not name which file counts as a "deployment template" (for example `infra/`, or a pipeline file). Either way it is full by the deployment trigger.

## S16: logging a behaviour test that ran before a second edit

* **How to say it.** The documents give no explicit normative rule, only precedent and one sentence. [O/I]
  * The LOG entries name the tested state precisely. The "Tested revision of the C2..." entry, for example, says the run "tested HEAD 7260826 plus the pre-grade C2 working-tree edits", states the verdict, and says edits applied after grading "were not re-simulated". The "C3 evidence provenance" entry gives the same kind of correction, with a retained patch name. [O]
  * CA step 6 requires behavior evidence to carry "exact source identity, execution status, verdict, fidelity and executor or profile limits". "Simulation, emulation or proxy evidence is never native-host or stronger-profile acceptance." [O]
* **What to write.**
  * Name the exact tested revision, for example HEAD plus the pre-run working-tree patch.
  * State that the second edit was not covered by the test.
  * Do not call the committed or final wording tested. [I]
* **Do not rewrite earlier entries.** Append a correction entry instead. [O] CI "Knowledge Base Conventions": "Never rewrite earlier log entries." The LOG corrections do the same and keep the earlier entries "preserved unchanged". [O]
* **Gap.** No instruction in the three artifacts says "must name the exact revision" as a rule for the log in general. It is demonstrated by the log tail, not stated as a rule.

---

## Observed gaps, ambiguities and contradictions (not repaired)

1. S10: the README claims a SQL change selects the `mssql` job via `src/core`, but a schema file under `src/importer` would not. [V] `MSSQL_PROJECTS` excludes importer. The README does not say where a new schema file belongs.
2. S12: the example commands omit `< /dev/null` although "Gate speed controls" and CA say to use it. `FAILED_RECEIPT_BASE_SHA` has no stated retrieval method.
3. S08: the direct acceptance command has no stated Chromium install prerequisite. The runner and workflow do the install.
4. S14: "no limit is evidenced" is weaker than "no limit". Scratch and `TMPDIR` length are unmeasured.
5. S11: the "if it moved, rerun" wording and the `BASE RELAXED` partial-receipt exception are two phrasings of one rule, and they read in tension until cross-read.
6. S16: the log truthfulness rule exists only as precedent entries plus CA step 6's evidence fields.
7. S01, S02, S03, S04, S10: the answers depend on file locations the prompts omit, and the documents give no default.
8. S09 and S03: the documents do not say whether green jobs with every step skipped satisfy any required context. They say only that none were required at retrieval (2026-11-08).

**Cross-artifact handoff:** README, CI and CA are consistent on tiers, the strictest-tier rule, doubt = full, impact-based classification and "absent CI is not a pass". No routing or naming mismatch found. The README anchor `#hosted-ci-versus-local-gate-coverage-issue-1294` is referenced by CI and CA and resolves to the heading at line 144. [V-heading read]

**Claims checked and found true.**
* The PYTHONPATH string.
* The AXE_SHA256 constant.
* The ci-affected markdown-only no-project selection.
* The non-`src/` widening.
* `BASE RELAXED` printing.
* The selector and acceptance steps in the workflow.

**Claim not independently confirmed.** The 58-byte figure itself. I found only the 107 and suffix constants, and did not locate the derived 58 constant.

**Containment statement.** Nothing was written or modified.

Files read:
* run-state.md and test-design.md, the two permitted `.copilot-tracking` files.
* src/README.md, .github/copilot-instructions.md and the coordinator agent file, read in full.
* docs/reference/log.md, via grep and lines 10936-10975 only.
* For label [V] checks only: tools/ci-affected.py, tools/rpi-checks.py (grep) and .github/workflows/src-ci.yml (grep and view).
* A glob that confirmed src/core/src/zava_forward/core/mssqlstore.py exists.

I never searched filesystem root and executed no commands. I used the "Expected behavior" paragraph in test-design.md only as part of the file view, and I composed the answers from the artifacts.

**Status: Complete.**