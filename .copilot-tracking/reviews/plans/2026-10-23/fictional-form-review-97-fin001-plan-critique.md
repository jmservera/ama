<!-- markdownlint-disable-file -->
# RPI Plan Critique: fictional-form-review-97-fin001

## Metadata

* Task ID: 97-fin001 (parent 97-recovery)
* Critique date: 2026-10-23
* Plan: .copilot-tracking/plans/2026-10-23/fictional-form-review-97-fin001-plan.md
* Phase details: .copilot-tracking/details/2026-10-23/fictional-form-review-97-fin001-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: documentation-only correction of the false "registers unchanged" claims at docs/reference/research/retrofit-synthetic-data/form-review-pack-97.md:28-29 and src/core/README.md:935-936, plus any directly coupled same false claim; no validation weakening, fixture authority change, invented approval, runtime or test change, full gate or unrelated fix; append-only KB log entry.
* Research and evidence considered: .copilot-tracking/research/2026-10-23/fictional-form-review-97-fin001-research.md (C1-C8) re-checked against src/core/src/zava_forward/core/forms.py:126-133, src/core/tests/test_form_review_pack.py:41-50, src/core/evals/fictional_form_review_pack.json (lines 13, 38, 358), the guide, src/core/README.md, docs/reference/research/retrofit-synthetic-data/data-dictionary.md:328-333, docs/reference/README.md:283, provenance-register.json, src/agents/evals/registry.json and docs/reference/log.md.
* Decisions, dependencies, and acceptance criteria considered: plan FR-1..FR-3, AC-1..AC-3, P01-T01..T03, P02-T01..T02.
* Assessment boundary: the supplied files only. No test was run and no draft wording exists yet, so the critique cannot confirm the final prose.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| C1-C8 evidence | Covered | All line references and quotes match the files (forms.py:131-133 refusal, test:41-50, fixture:38, 358, 13). |
| FR-1 / P01-T01 | Partial | Right target; replacement wording is left as sketch (PC-002). |
| FR-2 / P01-T02 | Partial | Right target; the same sentence also carries the "registered `DS-...`" provenance usage (PC-002). |
| FR-3 / P02-T01 | Partial | The log type, ms.date and required fields are unspecified (PC-001). |
| Coupled-claim search | Covered | Fixture line 13 is conditional and true. Index row 283, data dictionary line 328 and the 2026-10-20 log entry use "registered" for the provenance register. No other false claim found (PC-004). |
| AC-1..AC-3 | Partial | AC-1 grep is too narrow and AC-2 names no command (PC-003). |
| Commit and gate requirements | Missing | No commit task, identity step or gate statement (PC-005). |

## Verdict

* Verdict: Revise
* Rationale: scope and evidence are sound and no coupled false claim was missed. The plan lacks executable detail that the caller's requirements and the repository conventions make mandatory: the log entry type, date and contents, a sufficient verification command, the commit and identity step, and the unrun-gate statement. All are direct planner corrections.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: P02-T01 log entry is underspecified and could violate the log conventions

* Related IDs: FR-3, P02-T01
* Evidence: docs/reference/log.md:8-22 (types limited to `ingest`, `query`, `restructure`, `memory`, `lint`; entries must list files touched and any contradiction raised; frontmatter ms.date is 2026-10-22). The last entry is the 2026-10-20 one, so "append at the end" is correct although it is not the latest date. Plan P02-T01 gives no type, title or contents, and says to update ms.date only "if required".
* Concern: an implementer may invent a nonconforming type (recent entries use `update`, which the conventions do not list), omit the files touched or the contradiction, or leave ms.date stale.
* Impact: non-searchable or non-conforming log, and an ambiguous frontmatter date.
* Smallest useful change: specify heading `## [2026-10-23] lint | Corrected form review pack registration claims (#97)`. Name the files touched (the guide, src/core/README.md, the log). State the contradiction: the guide and the core README said the public schema registers unchanged, while `register_schema` refuses the placeholder reviewer. Say that only a derived copy with a registered reviewer registers, and stays Unapproved. State that no runtime, test, fixture, index or dictionary change was made, that the "registered" provenance wording was checked and is accurate, and that criterion 1 stays unmet and nothing is approved. Set ms.date to 2026-10-23, since the file changes materially, and do not edit earlier entries (the 2026-10-20 entry's "registered ... pack" is the accurate provenance meaning).
* Action owner: planning parent
* Exact resolving evidence: P02-T01 in the phase details states the type, title, file list, contradiction and ms.date decision. After implementation, `git diff docs/reference/log.md` shows only the appended block and the ms.date line.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: P01 wording is a sketch and risks a new inaccurate or overreaching claim

* Related IDs: FR-1, FR-2, P01-T01, P01-T02, C3-C5
* Evidence: guide lines 28-29 (the bullet continues "with sixteen fields ..."); src/core/README.md:932-936, which also contains "(registered `DS-FICT-FORM-REVIEW-PACK`...)" in the same paragraph; forms.py:131-133; test:41-50.
* Concern: T01 says the block is "the proposed definition for the existing path", which leaves unstated that the public file is refused as published. T01 also never says that the derived copy differs only in `reviewer`, that the substituted reviewer must be an existing registered person, and that registration records no approval. T02 does not address the same-paragraph "registered `DS-...`" wording, so a reader can still confuse provenance registration with schema registration.
* Impact: a half-correct fix would leave the ambiguity, or overclaim that the test or a reviewer can approve.
* Smallest useful change: add the required content to both tasks: (a) the public file is refused by `register_schema` because the placeholder reviewer is not a registered person; (b) a copy that differs only in `reviewer`, set to an existing registered person, registers; (c) it stays Unapproved with null approval evidence and no approval is implied; (d) the sixteen-field text is preserved. In README, keep "registered `DS-FICT-FORM-REVIEW-PACK`" but make the schema sentence explicitly say it is the provenance register ID, or change it to "listed in the provenance register" (this is the same paragraph and not an unrelated fix). Keep the guide's lines 63-67 consistent and untouched. Use plain ASCII with no em dashes.
* Action owner: planning parent
* Exact resolving evidence: P01-T01 and T02 list (a)-(d); post-edit diff of the two files shows only those paragraphs.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Verification commands are not exact and AC-1 can miss variants

* Related IDs: AC-1, AC-2, P02-T02
* Evidence: plan AC-1 searches only "registers unchanged" and "registers through this path"; phase details say "focused tests" without a command. Test location: src/core/tests/test_form_review_pack.py. The repository instructions pair tests with component guides.
* Concern: the AC-1 grep would not catch paraphrases such as "registers as Unapproved" without a reviewer qualifier. No runnable command is specified, and the research does not record which Python environment or PYTHONPATH the core tests need.
* Impact: false claims could survive, and AC-2 could be reported as passed without evidence.
* Smallest useful change: replace AC-1 with a case-insensitive search of the two files for `unchanged`, `registers through`, `registers as` and `regist` in the pack sections, reviewed by hand. State that no remaining sentence says the public file registers unmodified. Record the exact test command from the src/core guide (for example from src/core, `python3 -m unittest tests.test_form_review_pack -q`, plus provenance or registry tests if the command exists) and the observed result in the changes file. Add `git diff --name-only` equal to the guide, README, log and tracking files only, and the ASCII and no-em-dash check on the diff.
* Action owner: planning parent (command confirmation by the implementer)
* Exact resolving evidence: the changes file records the command, exit status and diff name list.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: Record the coupled-claim search result and the fixture line 13 residual in the plan

* Related IDs: C6, C8, Scope
* Evidence: fixture line 13 "Registering its schema records Unapproved status" is true, but it reads as if the public schema registers; fixture authority must not change. docs/reference/README.md:283, data-dictionary.md:328 and provenance-register.json use "registered" as the provenance meaning and are accurate. src/agents/evals/registry.json and .github/rubric/scores/latest.json only reference the test and the pack.
* Concern: the plan lists non-goals but not the examined residuals, so the implementer or a later reviewer may reopen them or silently edit the fixture.
* Impact: scope creep, or a fixture authority change.
* Smallest useful change: add one line in the plan Scope section, "Examined and left unchanged: fixture statement line 13 (conditional, true; fixture unchanged), index row 283, dictionary 328-333, provenance register and the 2026-10-20 log entry", with the reason. The guide correction should make clear that the fixture statement refers to a derived copy.
* Action owner: planning parent
* Exact resolving evidence: plan Scope contains the residual list; `git diff` shows no change to the fixture, index, dictionary, registry or provenance register.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: No commit, identity or unrun-gate step although the caller and repository require them

* Related IDs: User Decisions and Requirements, P02, Executive Summary readiness
* Evidence: plan requirements state "Commit scoped correction and tracking with a Conventional Commit and the Copilot trailer" and "no full gate", but neither phase has a task for the commit. The repository instructions require repository-local `git config --local user.email` set to the `{id}+{login}@users.noreply.github.com` address resolved via `gh api user`, and the plan is silent on the branch check. The instructions also say a final RPI candidate needs the local gate before publication, and the caller excludes it. Untracked tracking directories exist (git status).
* Concern: the commit is requested but unplanned, with no identity step, subject or file list. The plan does not say that the gate is intentionally not run, so "Ready" could be read as gate-ready.
* Impact: wrong author email, an omitted trailer, unscoped files (for example a stray receipt) or a false implication of publication readiness.
* Smallest useful change: add P02-T03: check `git status --short` and the branch; configure the local noreply email via `gh api user`; stage only the guide, README, log and this task's tracking files (plan, details, research, critique, changes); commit `docs(core): correct form review pack registration claims (refs #97)` with the Co-authored-by trailer; no push. Add to the plan an explicit statement that the complete local gate is not run under the owner's direction, is not claimed, and is required before any publication; the earlier b22d8639 gate is historical.
* Action owner: planning parent
* Exact resolving evidence: P02-T03 exists; after implementation `git log -1 --format=%ae%n%B` shows the noreply address and the trailer, and `git show --stat` lists only the intended files.
* Decision route: direct planner correction (the owner brief already authorizes the commit and no gate)

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: Critique disposition and changes-file ownership should be closed before readiness

* Related IDs: Critique Disposition, Executive Summary, Phase Checklist
* Evidence: the plan says "Readiness: Ready after the single critique disposition", and Critique Disposition reads "Pending".
* Concern: the plan does not record how each PC finding is dispositioned, nor that no second critique is run.
* Impact: ambiguity about whether implementation can start.
* Smallest useful change: after applying PC-001..PC-005, record a disposition of each as Accepted with the plan section changed, state that no further critique is planned, and update Readiness. Do not edit this critique.
* Action owner: planning parent
* Exact resolving evidence: the plan Critique Disposition table lists PC-001..PC-006 with outcomes.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Scope is tight and evidence-backed: the two false claims are the only ones sharing the defect, and every cited line was verified.
* Validation, fixture authority, runtime and tests are protected, and unresolved Finance decisions and criterion 1 are kept unmet.
* Residual risk: README's "registered" provenance wording and fixture line 13 stay ambiguous to some readers by design, because the fixture cannot change.

## Questions or Blocking Evidence Gaps

* None. No user decision is required.

## Limitations

* No tests or greps were run. This critique read the files and did not validate wording that has not been written.

## Recommended Next Action

* Highest-impact finding: PC-005
* Action owner: planning parent
* Smallest next action: apply PC-001..PC-006 directly to the plan and phase details, then finalize without another critique
* User response required: no

| Artifact | Description |
|---|---|
| [.copilot-tracking/plans/2026-10-23/fictional-form-review-97-fin001-plan.md](.copilot-tracking/plans/2026-10-23/fictional-form-review-97-fin001-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-10-23/fictional-form-review-97-fin001-phase-details.md](.copilot-tracking/details/2026-10-23/fictional-form-review-97-fin001-phase-details.md) | Phase details under critique |
| [.copilot-tracking/research/2026-10-23/fictional-form-review-97-fin001-research.md](.copilot-tracking/research/2026-10-23/fictional-form-review-97-fin001-research.md) | Research evidence C1-C8 |

## Next Steps

No user action is required. The planning parent applies PC-001 to PC-006 directly and finalizes without another critique. `/rpi-plan` is needed only if this is a standalone run.
