<!-- markdownlint-disable-file -->
# RPI Plan Critique: post-153 integration checkpoint for #440

## Metadata

* Task ID: post153-integration-440-1112
* Critique date: 2026-11-12
* Plan: .copilot-tracking/plans/2026-11-12/post153-integration-440-1112-plan.md
* Phase details: .copilot-tracking/details/2026-11-12/post153-integration-440-1112-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: one bounded documentation and evidence checkpoint for existing issue #440 covering merged PRs #1470 and #1475; documentation plus focused observations only; no new issues, fixes, closing keyword or tick; no full gate, Docker, SQL, browser, Azure or model; origin proof by installed `__file__` with hash equal to git blob; four evidence classes; requirement-qualified traceability; dedup against existing owners; five synthetic ids and route syntax checked against public source only; local commit with privacy-safe identity and trailer, no push.
* Research and evidence considered: .copilot-tracking/research/2026-11-12/post153-integration-440-1112-research.md; the raw directory /home/azureuser/.copilot/session-state/d351ddc0-f4e6-4e5f-ae56-db0937d3ad2b/files/checkpoint-440-post153-1112/ (all .out, .err, .exit, .py, .txt files); repository sources at HEAD 4074b44f3 (git objects, assistants.js, app.js, runbook.md, tests, design-system.md, WCAG baseline, README, log, pack headings).
* Decisions, dependencies and acceptance criteria considered: plan FR-1..5, NFR-1..3, AC-1..5, P01..P03, FU-1..4, test ownership lock.
* Assessment boundary: read-only; no tests rerun, no network (live issue and PR states in the research could not be re-read and are taken as recorded). Conclusions cover plan credibility, not the future section text.

### Fact checks against the repository and raw outputs

| Claim | Result |
| --- | --- |
| HEAD, root/src/docs/infra/tools trees | Verified (`git rev-parse`) |
| #1470 merge `088e8c3c0` tree `68f0db87`; #1475 merge `38d3ed187` tree `cc219a7f` | Verified |
| 4 files, 554 insertions, 179 deletions since `bbb1d20cc`; pin `src` tree `60d84101` | Verified (`git diff --stat bbb1d20cc HEAD -- src`) |
| Six non-evidence paths of #1470 (incl. `log.md`, `content-standard.md`) and 16 tracking files | Verified (stat lists 19 tracking files in 4 task sets; count of 16 not reproduced, see PC-007) |
| #1475 paths: `runbook.md`, README, `log.md` plus 7 tracking files | Verified |
| Blob prefixes for the seven documents | Verified |
| `assistants.js:130-135` single `details`; `:103,133` role-less `pre` with `tabindex` and `aria-label`; `:45,115-116` edit label; `test_case_journey.py:1299` label assert | Verified |
| 10 `role: "region"` occurrences; `app.js:853` example | Verified |
| `app.js:382-387` route/tab read, `:1146` quality tab; `chat_case_answers.py:16` `ZF-\d+` | Verified |
| Runbook five-home section `runbook.md:48-119`; five rows; one origin; pack mentions origin once | Verified (heading line 48, next section line 120) |
| Origin proof for four modules (path inside worktree, hash equal to blob) | Verified in `preflight.out`; fifth module `zava_forward.core.sensors` errors with "No module named" |
| 19, 31 and 187 tests, exits 0; `skipped=92` | Verified in `.err` files; `.out` files are empty |
| First `test_case_journey` attempt: 31 tests, 35 errors, `node` not found | Verified in `test_case_journey-attempt1-nonode.err` |
| "No existing test covers the five-home section" | Largely verified: `git grep` finds no test or tool referencing the section; only `.github/rubric/scores/latest.json` and `src/core/README.md` mention it. No generic link checker covers it |
| "WCAG baseline and design-system contain no rule text for scrollable regions" | Not accurate, see PC-003 |
| `node --check` observed | No raw output in the directory, see PC-001 |
| All 92 skips are SQL | Plausible from source (`MSSQL` gate at `test_quality_sensors.py:1802` on `MssqlReadModel` and `MssqlHttp`) but reasons were not captured, see PC-002 |

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller: documentation plus focused observations only; no scope expansion | Covered | Plan scope, non-goals and test lock |
| Caller: origin proof by `__file__` and hash | Partial | Four modules proven; test modules, fixtures and the sensors ERR are not addressed (PC-005) |
| Caller: separate four evidence classes | Partial | FR-3 names them; no class assignment per boundary is drafted (PC-008) |
| Caller: requirement-qualified traceability | Missing | No BRD/PRD requirement IDs named anywhere (PC-008) |
| Caller: do not equate historical with current | Partial | 281-test campaign excluded, but not stated as historical or which suites that campaign covered that were not rerun (PC-007) |
| Caller: dedup against existing owners | Missing | No search record for F1 to F3 (PC-004) |
| Caller: five ids and route syntax against public source only | Covered with a self-referential id regex (PC-006) |
| FR-2 commands, exit statuses, counts, raw paths | Partial | No command log retained; `node --check` has no raw output (PC-001) |
| G1/FR-1 identities | Covered | All verified |
| P02 index and log | Covered | README line 212 already links the runbook anchor; ms.date already 2026-11-12; log tail format matches |
| P03 validation and commit | Partial | No step for tracking-file inclusion decision or review/changes records (PC-009) |
| AC-1..AC-4 | Covered | Testable by diff |

## Verdict

* Verdict: Revise
* Rationale: The plan is scoped correctly and most facts verify, but one claimed observation (`node --check`) has no retained output, one research claim is false (no repository rule on scroll regions), skip attribution and several caller requirements (requirement IDs, dedup evidence, historical separation) are not yet planned. All are direct planner corrections; none needs a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `node --check` and command provenance have no retained raw evidence

* Related IDs: FR-2, AC-2, G2, plan Executive summary, P01-T01
* Evidence: raw directory listing: no node-check file; only `node-path.txt` (a PATH directory). The raw directory has `.exit` and `.err` files but no file recording the exact commands, working directory, `env -i` variables or `PYTHONPATH`. The research states the environment only as a plan ("Evidence plan fixed by research").
* Concern: The plan cites a passing `node --check` as "already taken" and requires "actual commands" in the section, but neither the result nor the commands can be reproduced from the raw files. AC-2 ("every number traceable to raw outputs") cannot be satisfied for these items. Hosted workflows already run `node --check` on `assistants.js` (`.github/workflows/mvp-ci.yml:36`), which must not be borrowed as current local evidence.
* Impact: An unsupported "observed" claim in an evidence pack breaks the local observed class.
* Smallest useful change: Either rerun `node --check` on `assistants.js` and `app.js` locally with node on PATH and keep `.out`, `.err` and `.exit` files; or drop it from the plan as not observed. Add a retained command manifest (commands, cwd, env, node version, venv interpreter) and list the raw files with sha256 so a reader can detect later change.
* Action owner: planning parent
* Exact resolving evidence: raw directory contains the node-check exit file (or the plan no longer cites it), a command manifest, and a sha256 list; the pack section's command table cites only those files.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: "187 tests with 92 SQL skips" is ambiguous and the skip reason is not captured

* Related IDs: FR-2, FR-3, research Wave 3, Questions table
* Evidence: `test_quality_sensors.err`: "Ran 187 tests ... OK (skipped=92)"; no `-v` output; source gate `test_quality_sensors.py:1802-1817`.
* Concern: The research says "187 run, 92 skipped", which suggests 187 executed. unittest counts skipped tests inside "Ran 187", so 95 executed and 92 skipped. Attribution of all 92 to SQL is an inference from source, not an observed skip reason. The stderr also contains `GET /api/assistants/proposals status=503` and "Sensor consent index could not be reconciled" lines whose expected-or-not status is unexplained.
* Impact: A miscounted or over-attributed result misstates what ran, and these tests (which read `assistants.js` only as text) are weak evidence for #1470.
* Smallest useful change: Write "187 collected, 95 executed, 92 skipped; skip reason read from the `MSSQL` gate in source, not captured at run time", or rerun with `-v` and keep skip reasons. Name the 503 and consent log lines as unexplained stderr, not as results.
* Action owner: planning parent
* Exact resolving evidence: plan and section state 95 executed and 92 skipped with the reason source; log noise recorded as observed stderr.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: F1 rests on a false statement about repository accessibility rules

* Related IDs: F1, FU-1, research Wave 3, FR-4
* Evidence: research line 59 says the design-system and WCAG baseline "contain no rule text for scrollable regions". `docs/reference/research/ux/design-system.md:94-95` and `:109` define a named, focusable `role=region` for overview table scroll areas; `docs/reference/research/ux/wcag-conformance-baseline.md:54-55` records named focusable `table-scroll` regions and `ops.js` `aria-label` handling.
* Concern: The rule exists for table scroll regions, but none addresses technical `pre` blocks. The sentence as written is wrong, and it makes "no repository rule is breached" look broader than the evidence.
* Impact: The finding could be misrouted or read as an unfounded accessibility claim.
* Smallest useful change: Reword F1: the repository documents named `role=region` only for table scroll areas; no repository rule covers scrollable `pre` blocks; ARIA prohibits naming a generic element (cite the standard as external, unverified here, not fetched this pass); the pattern differs from `app.js:853`. Keep it static, unverified, no conformance claim.
* Action owner: planning parent
* Exact resolving evidence: F1 text cites `design-system.md:94-95,109` and states the gap precisely; research line 59 not repeated in the pack.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Deduplication against existing owners is asserted, not evidenced

* Related IDs: FR-4, FU-1..FU-4, caller dedup requirement
* Evidence: plan and research name owners (#153, #132, #134) but record no search of open issues, review artifacts or the pack for an existing record of the `pre` accessible-name question, the unrun browser check, the missing runbook test or the live preflight. FU-4 and the runbook's own preflight list already own the live check.
* Concern: Without a recorded search, F1 to F3 may duplicate existing items, and nothing says whether owners were told (no comment can be posted under the no-network rule).
* Impact: Duplicate findings and false routing violate the caller's dedup rule.
* Smallest useful change: Run and record a local search (`git grep` over `docs`, `src/*/README.md`, `.copilot-tracking` for "aria-label", "technical record", "assistants_browser_check", "runbook" test coverage) with terms and results; where a live issue read is not available, label dedup "local sources only; live issue search not performed". Fold FU-4 into the runbook's existing preflight and call F3 a coverage observation, not a new item. State that no owner was notified.
* Action owner: planning parent
* Exact resolving evidence: the section lists search terms, hits per finding and the unverified-live-search limit; no finding is stated as "new" without that record.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Origin proof is incomplete for the test code and the sensors module result is unexplained

* Related IDs: caller origin-proof requirement, FR-2, AC-2
* Evidence: `preflight.out` proves four package modules (paths under the worktree, hashes equal to blobs). The fifth, `zava_forward.core.sensors`, prints "No module named", which the plan does not mention. The tests run from `PYTHONPATH` directories (`src/core/tests`, `src/agents/tests`, `src/api`); their files and imported fixtures (`release_support`, `dataset`, `sensor_consumer_fixture`, `test_assistants`) are not hashed. `pip-install.out` shows pre-existing user-site installs of the same distributions that pip could not uninstall.
* Concern: The `ERR` line could be read as a failed check or silently dropped; test-file origin is unproven; the pre-existing user-site installs are not discussed.
* Impact: The origin claim covers only part of what ran.
* Smallest useful change: Record that `zava_forward.core.sensors` is not a module in this tree (verify `git ls-tree`), so it is a bad probe, not an origin failure. Add a hash proof (`__file__` vs `git rev-parse HEAD:path`) for the three test modules run and for `assistants.js`/`app.js`; or state they are proven only by cwd and path. Note the user-site installs and that the loaded paths were nevertheless under the worktree. Record ignored `egg-info` state before and after (`ignored-before.txt` does not say whether pip ran first).
* Action owner: planning parent (one small additional local observation)
* Exact resolving evidence: a raw preflight file listing each loaded test module path and hash equal to blob, plus the explained sensors line and egg-info state.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: Five-home static check is syntactic and its id regex is self-referential

* Related IDs: C5, C6, F3, FR-3
* Evidence: `five-home-static-check.py` uses `ZF-\d{4}-\d{4}` and substring tests (`'get("tab")'`, a template-literal string). Other public sources use the same shape (`src/api/checks/employee_workspace_browser_check.py:18`, `src/api/README.md:4824`, `ZF-2026-0597`) but define no id rule; `chat_case_answers.py:16` accepts `ZF-\d+`. "Other public mentions: []" excludes the runbook and `.copilot-tracking`, and the `.out` shows `True` for the readme anchor and links.
* Concern: Passing proves internal consistency and route syntax, not id existence or a contract; the plan already says this, but not the existence of other public example ids of the same shape.
* Impact: Minor overstatement risk.
* Smallest useful change: State "shape matches other public example ids (cite two); no public source defines the shape or contains these five ids", and describe the check as string-level. Keep the script outside the repo with its sha256 in the manifest.
* Action owner: planning parent
* Exact resolving evidence: section wording as above; script hash in the raw manifest.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Historical versus current results and the affected-set rationale are not drawn explicitly

* Related IDs: G1, G2, FR-1, research Wave 1 (d), Exclusions
* Evidence: the previous section (`cutover-evidence-pack.md:7387`+) records the 281-test campaign at `bbb1d20cc` and excluded unmerged #1470, #1475 and local commit `6819456`. `git grep` shows `test_workspace_scripts.py` and `loading_briefing_browser_check.py` also reference `assistants.js`; research dismisses the first as an allowlist and does not mention the second. The research lists 16 tracking files for #1470 but the stat shows 19 across four task sets.
* Concern: The plan never states that the previous campaign remains a historical result at a different pin, that the three suites rerun here are a new, smaller observation, or whether `6819456` is still unmerged (the source delta suggests so, but this is not stated). Omitted `assistants.js` references have no recorded rationale.
* Impact: Readers could infer 281-test continuity or full #1470 coverage.
* Smallest useful change: Add to P01-T01 an exclusions table: previous 281 tests (historical, pin `bbb1d20cc`, not rerun), `6819456` status, `test_workspace_scripts.py` and `loading_briefing_browser_check.py` (referenced, not run, with the reason), and correct the tracking-file count or drop it.
* Action owner: planning parent
* Exact resolving evidence: the section's exclusions table cites each path and reason; count matches `git show --stat`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: Requirement-qualified traceability and evidence-class assignment are not planned

* Related IDs: FR-3, P01-T01, caller traceability requirement
* Evidence: details P01-T01 says "requirement trace (BRD/PRD qualified; evidence classes)" but names no requirement IDs; research states the addendum and original case study were not read, and no BRD or PRD requirement was read for this task (only blob and status).
* Concern: "Qualified" cannot be satisfied without naming the requirements and the evidence class each boundary supports.
* Impact: The trace would be generic or fabricated at implement time.
* Smallest useful change: Pick the specific BRD/PRD requirement IDs (and the content-standard rule IDs for #1470) from the existing documents before implementation, or state "no requirement IDs verified; trace unqualified" for any row. Draft the class table: node fixtures and static tests as local observed (regression only); browser keyboard behaviour as implemented-unverified; live origin, id existence and endpoint as blocked; resident-facing acceptance and sensor availability as unknown.
* Action owner: planning parent
* Exact resolving evidence: details file lists requirement IDs with file:line citations and a four-class table row for each boundary.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-009 -->
### PC-009 [Low]: Phase list omits the review and changes records and the tracking-file commit boundary

* Related IDs: AC-4, AC-5, P03-T01, P03-T02
* Evidence: the plan names a changes record and a review artifact, and AC-4 allows "new tracking files", but no task creates or checks them; the commit scope for `.copilot-tracking/` files (plan, details, research, critique, changes, review, plus raw evidence outside the repo) is not defined. NFR-2 bars `.copilot-tracking/` references in the commit message while the pack section will cite an external absolute path.
* Concern: Ambiguity about what the commit contains and whether the pack cites non-committed external paths a reader cannot open.
* Impact: Diff-boundary check (AC-4) could pass or fail inconsistently.
* Smallest useful change: Add P03 tasks for the changes record and review artifact; list the exact files to stage; state in the section that raw files are external and not committed, with the hash list from PC-001.
* Action owner: planning parent
* Exact resolving evidence: P03 lists each staged path; `git show --stat` of the commit matches it.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Scope discipline, adverse-attempt retention (the no-node run), the contrarian note on the unverified browser behaviour and the explicit non-claim on id existence are credible.
* Identities, trees, blobs, code line references and the five-home contract checks verify against the repository.
* Residual risk accepted by design: no browser, live, SQL or assistive-technology evidence; F1 stays static and unverified.

## Questions or Blocking Evidence Gaps

* None that need a user decision. The one missing local observation is the `node --check` result (PC-001), which the planner may rerun locally or remove.

## Limitations

* No network; live issue and PR states in research are not re-verified. ARIA 1.2 naming rules were not fetched.
* Tests were not rerun; results rely on the retained `.err`/`.exit` files.
* The BRD, PRD, addendum and original case study were not read in this critique.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: rerun or drop `node --check` and add the command manifest with sha256 list, then apply PC-002 to PC-009 directly and finalize without another critique.
* User response required: no

## Artifacts

| Path | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-11-12/post153-integration-440-1112-plan.md](post153-integration-440-1112-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-11-12/post153-integration-440-1112-phase-details.md](../../details/2026-11-12/post153-integration-440-1112-phase-details.md) | Phase details under critique |
| [.copilot-tracking/research/2026-11-12/post153-integration-440-1112-research.md](../../research/2026-11-12/post153-integration-440-1112-research.md) | Research evidence |

## Next Steps

Return to the planning parent: apply PC-001 to PC-009 as direct corrections, then finalize. No user action is required.
