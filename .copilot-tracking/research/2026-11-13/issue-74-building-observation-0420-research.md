<!-- markdownlint-disable-file -->
# Research: #74 buildingView operational observation (issue-74-building-observation-0420)

Date 2026-11-13. Worktree issue-74-browser-0410, branch test/demo-home-browser-74-0410, head e8dec941d567653c02163f551874ca26f2b527fa (product source equal to origin/main 6f2918011). Disposition: reused plus bounded source read. Prospective: nothing below has been observed yet.

## Reuse

* Planning task 5676f9025 (research, plan, details, one critique): `buildingView` is source-inspected, unobserved (CR-003); critique not repeated for that task.
* V2 mapping 232e09aa5: marks building-screen rendering Rendered-unobserved and proposes editing the maintained check. Root does not admit that edit. This task is the narrower alternative: one read-only operational observation with owned scratch instrumentation, no maintained assertion, check, product, test or config change, and no added source budget or history.
* Home browser run (e8dec941d changes): 24 PASS, not repeated here.

## Requirement text read

PRD `docs/prds/proper-warm-retrofit-programme-demonstrator.md` line 610 FR-001 (one home case linked to its building) and 611 FR-002 (show building-level shared systems, dependencies, holds, works and costs separately from each home's evidence, decision, cost allocation and outcome; a shared building ID alone does not establish package applicability). The BRD FR-001/FR-002 and NFR-002 were not read (NFR-002 is performance, not relevant to this observation). No outcome definition is invented; "outcome" stays undefined.

## Source facts

* `homeCaseView` (`app.js` about 1325-1365) renders a link `Open full building context` to `#/building/<id>` inside the h2 section "Shared at building level, not this home's evidence".
* `buildingView` (about 1370-1411) fetches `/api/buildings/<id>` and renders h1 `<name> (<id>)`, h2 sections Shared systems, Dependencies, Work stopped pending review, Shared works, Shared building costs, Linked home cases; it shows `Affected homes`/`Packages` per item when the field is present.
* Fixture `home_case_data()` (home_case_browser_check.py) gives building SYN-B1 "Fictional exercise block" with SYS-1, DEP-1 (case ZF-2), HOLD-1, WORK-1 (ZF-2), COST-1 GBP 12000.00, homes ZF-2 and ZF-3 each with a GBP 6000.00 allocation; login `pam@example.test` (Retrofit Programme Manager) with the synthetic password.
* `design_system_browser_check.main(browser_check, data_factory)` writes the fixture to a temp directory under `ZF_BROWSER_SCRATCH`, binds an ephemeral 127.0.0.1 port, starts the server child with ZF_DATA/ZF_STATE in that directory, passes only PATH/HOME/LANG/bytecode vars, and terminates and waits the server in `finally`. It is reusable unchanged by passing a different browser callable.

## Reuse feasibility

Fixture and harness are reusable without product or check edits. Playwright, Chromium cache and pinned axe from the frozen b0e evidence directory exist; axe is not needed here and is not used.

## Limits

The observation is not assistive-technology or WCAG evidence, not criterion 2 acceptance, not outcome acceptance, not permanent regression coverage. G5 applicability (home panel), unknown-funding rendering (CR-002) and author chronology limits are unchanged. Scratch path note: the brief names an absolute output directory under session 38e61c82 while the native context is b0e0aec9; the named directory is used for outputs only, as instructed, and was newly created; its other contents were not read.
