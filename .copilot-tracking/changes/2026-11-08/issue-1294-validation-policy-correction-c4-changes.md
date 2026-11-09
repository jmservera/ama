<!-- markdownlint-disable-file -->
# Changes: issue-1294-validation-policy-correction-c4

Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c4-plan.md. Details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c4-phase-details.md. Research: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c4-research.md. Critique: .copilot-tracking/plans/critiques/2026-11-08/issue-1294-validation-policy-correction-c4-plan-critique.md.
Status: complete. Base HEAD 2f1aa2e4d42b79364b95622d6198975203c1417e (tree 97b940c4824d22ddb7bd9a6d54fc926beb960f77); origin/main fa7ae0c9770e890f82482456bfcb8e97f1e05429.

## P01 Guide and log corrections

* src/README.md (F2): project steps run only for selected projects after `image-paths`; markdown directly in `src/` or under a project directory selects nothing; widening from non-`src/` paths other than the namespace-only tools, unknown `src/` directories and dependency manifests; `src-no-working-data` runs whenever Source CI starts; hosted results labelled inferred; the examples row for `src/README.md` states the data guard and widening; the legacy CI paragraph no longer says checks run for every project; path-filter wording says "listed tools" (static review L1) and names the namespace-only tools (static review M1).
* src/README.md (F3): receipt paragraph says a changed base needs a new run for full and `--exact-base` receipts, while a partial receipt may stay valid only with `BASE RELAXED`.
* src/README.md (F5): SQL example uses `src/core/src/zava_forward/core/mssqlstore.py`; hosted column states a core change selects every project, namespace and mssql; chat rows note namespace and mssql are also selected.
* src/README.md (F6): focused block fetches `origin/main` and sets `BASE_SHA`; resume is a separate failed-receipt-only command using `$FAILED_RECEIPT_BASE_SHA` (the failed receipt's recorded base, per PC-003).
* docs/reference/log.md (append-only): a provenance correction entry (F4, F7, F8) and a C4 update entry; removed lines 0.
* F4: strict probe (fails on `loader.errors`, exact three flattened IDs): exit 0 with the runner PYTHONPATH, exit 1 with it unset (three `_FailedTest`); command and environment in sandbox 5 checks/loader-probe-command.txt; proves import and name resolution only, not a browser run.

## Finding dispositions

All eight confirmed, none inapplicable: F1 independent static assessment obtained (below); F2, F3, F5, F6 corrected; F4 strict probe recorded; F7, F8 provenance corrections below and in the log.

## Provenance corrections (F7, F8; retained evidence not rewritten)

* F7: the C3 changes record described the sandbox 4 pre-run status as clean. The raw sandbox 4 pre-run-status.txt actually lists modified `docs/reference/log.md` and `src/README.md`, the untracked C3 research, plan, details, critique and sandbox, and ignored `tools/__pycache__/`.
* F8: report 4 tested HEAD bd63b22 plus the uncommitted C3 patch (target-diff-vs-bd63b22.patch; README diff sha256 6f33a32a5968d3c807833611a8f899799ef72189a9700f409861913a16f59333, log diff sha256 0874887823ad3e8c2e6a95a971eb65724c59fd9d9f6b54067ab17c9bdcbf8763). The C3 outcome log entry and the C3 tracking records were added after grading and were not simulated; "no edit after grading" holds only for guide wording, and "the last two log entries" understates the later entry. Report 4 and the C3 record are unchanged.
* This run (report 5): the C4 tracking records and report 5 are created after grading and were not simulated; the C4 log entries were present when tested.

## P02 Static assessment (F1)

* Independent fresh-context general-purpose subagent, label "proxy independent static assessment, not canonical host-bound HVE stage" (model not observable), rubric: hve-builder requirements-catalog and review-rubric. Log: .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-static-review-c4-log.md. First pass verdict Pass with M1 (Medium) and L1 confirmed and fixed; targeted closure (same log, appended) Pass, M1 and L1 Closed, no new finding. The earlier lead self-assessment in report 1 stays historical. Static scope: the four targets; instruction files unchanged by C4.
* Blob identities at behavior freeze (equal after grading and expected equal at commit): src/README.md b6f456731b56fe11fa58c291b62eed2a105e6662; .github/copilot-instructions.md dd8c0b20f44b1c98db9aad327302f64da008c5e8; coordinator agent 3a46e98a42e477ce2d9928dd495f53a4e1cde570; docs/reference/log.md c930d1bdf725dd75ff0e81924cb8ec7eef67ca6b. The closure was run after the M1/L1 edit, before these were captured; sha256 values in sandbox 5 source-identities-pre-dispatch.txt.

## P03 Behavior (proxy, simulation)

* One attempt: report .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-5.md, sandbox .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-5 (retained). Full run, 16 scenarios, independent grader Pass, zero confirmed defects, three Low nonblocking observations, no edit afterwards. Proxy: no intended-profile or native claim. Human box unchecked.

## P04 Validation, tier basis

* Focused checks (output .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-5/checks/focused-checks.txt): source `git diff --check` exit 0; log removed lines 0; added ASCII violations 0; stale-phrase grep finds only the legitimate "Hosted-only: upload-artifact" label; README link scan clean; selector probes in selector-probe.txt including the actual candidate file list (24 files: all five projects, namespace, mssql if Source CI starts; inference, unobserved); loader probes exit 0 and 1.
* Raw whitespace, recorded separately: `git diff --check base..HEAD` reports findings only in retained raw sandbox files (sandbox 3 selection.txt, two sandbox 3 patches, sandbox 4 patch); not rewritten. Source documents pass.
* Tier: focused. Basis: guide and instruction wording only; no workflow, tool, dependency, Dockerfile, SQL, security-control or deployment change; the README edit does match the Source CI path filter. Ran locally: the checks above and HVE static and behavior stages. Not run: any hosted CI, a full gate, a browser run. Hosted Source CI is unobserved; with the real candidate paths it is expected to run all selected projects once published.

## Remaining

* Human acceptance of proxy static and behavior evidence; independent exact-head assessment; hosted CI observation after publication.
