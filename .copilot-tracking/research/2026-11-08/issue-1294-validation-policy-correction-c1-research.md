<!-- markdownlint-disable-file -->

# Task Research: issue-1294-validation-policy correction C1

| Field | Value |
|---|---|
| Date | 2026-11-08 |
| Researcher | rpi-research (host skill invoked), run inline by the parent |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c1-research.md |

## Research Brief

* Topic: independent review of candidate 397ce435 (/home/azureuser/.copilot/session-state/f751a4dc-045d-479c-8035-8588858e3b08/files/review-1294-397ce-independent.md) found four revise items. Research the cited runner, workflow and harness code and decide the corrections.
* Scope: tools/rpi-checks.py, src/api/checks/employee_chat_browser_check.py, .github/workflows/src-ci.yml, and the four guide passages from commit 8a5cab9. Non-goals: workflow, tool, source, branch-protection changes; no browser, Docker, SQL or network use.
* Output mode: convergence. Posture: focused (named defects, named code), provenance: caller brief.
* Limits: this worktree only; read-only; the first-attempt, retry and review artifacts are preserved.

## Opening State (honest record)

The independent review and the cited runner lines were read before this artifact was written, in the same turn as the skill invocation; no other search preceded it. No extension subagent was dispatched; the three waves ran inline.

## Cycle 1

### Wider wave

* Runner direct-check contract: `EMPLOYEE_CHAT_PASS = "PASS employee chat: "` and `EMPLOYEE_CHAT_STATES` (actual-model-unavailable, synthetic-cited-answer, demo-disclaimer-model-answer) at tools/rpi-checks.py:134-139 (C1). `check_employee_chat_log` requires the marker in the command output and rejects any "skipped" (case-insensitive) at tools/rpi-checks.py:1555-1557 (C2). `check_employee_chat_results` requires a JSON list whose states equal the tuple in order, `violations == []`, `passes` a non-bool integer > 0, and no "skipped" in the JSON at tools/rpi-checks.py:1560-1574 (C3).
* Pinned axe: `AXE_SHA256` at tools/rpi-checks.py:82 (C4); runner downloads axe 4.10.3 and compares the digest before the harness at tools/rpi-checks.py:2345-2352 (C5); the harness itself raises unless the SHA-256 of `--axe` equals its pin at src/api/checks/employee_chat_browser_check.py:402-404 (C6). The harness prints `PASS employee chat: ...` only after its scans and writes `axe-results.json` to `--out` at src/api/checks/employee_chat_browser_check.py:381-393 (C7).
* Chat-panel selector: `CHAT_PANEL_BROWSER_SELECTOR` at tools/rpi-checks.py:123 (C8); `check_skips` with `expected_test` requires exactly "Ran 1 test", no skips, a bare `OK` line and the named test reported passing at tools/rpi-checks.py:1577-1624 (C9). The runner invokes it with `ZF_BROWSER_TESTS=1` at tools/rpi-checks.py:2336-2342 (C10).
* Runner counterparts of the guide's "Hosted-only" items: Bicep build and lint tools/rpi-checks.py:1103-1106 and 2228-2234 (C11); migration group at 1118 and 2247 (C12); tracked working-data guard "Tracked sandbox/working data guard failed" at 2175 (C13); Trivy and SPDX image steps at 1277-1320 and the SPDX verification at 1476-1481 (C14); workflow-to-local mapping `("src-ci.yml","no-working-data"): "static"` and namespace mapping at 2270-2271 (C15).
* Hosted counterparts: Trivy scan and upload-artifact at .github/workflows/src-ci.yml:152-200 (C16); Bicep build/lint at 230-233 (C17); branding migration at 268 (C18); `no-working-data` is its own job `src-no-working-data` at 281-282 (C19).
* Full-tier wording introduced by 8a5cab9: .github/copilot-instructions.md "and for any workflow, gate-tool, dependency-manifest or Dockerfile change" (C20); src/README.md:66-68 (C21); coordinator agent file Local validation tiers paragraph at ~470 (C22); policy example row "Gate tool or workflow ... Full" in src/README.md (C23).

### Deeper wave

* Finding 1 (confirmed): the README direct-check text ("three states report no violations and no skip") omits ordered state names, positive integer `passes`, and the `PASS employee chat:` marker, which C2-C3 require. Because the harness writes `axe-results.json` and prints the marker (C7), a direct reviewer can check all of them from the command's stdout and `<out>/axe-results.json`; no wrapper is needed. The runner copies that JSON to `employee-chat-results.json` before checking it (tools/rpi-checks.py:2403-2406); direct use reads the original file. The runner also runs the selector's `Ran 1 test` check on the verbose unittest output, so a direct run needs `-v` to see the named test line (C9, C10).
* Finding 2 (confirmed): the "Hosted-only" bullet is false. Trivy, SPDX, Bicep, migration and the working-data guard all have local counterparts (C11-C15), and `no-working-data` is a separate hosted job, not a namespace step (C19). The genuinely hosted-only behavior is `actions/upload-artifact` retention of Trivy and SPDX outputs (C16) and hosted runner/matrix/path-filter execution. The previous wording also credited the "migration checks" to namespace; C18 shows it as a step.
* Finding 3 (confirmed): the unconditional full tier for four file classes (C20-C23) is an expansion of the owner's category list (big features, releases, infrastructure, deployment, SQL, security-sensitive). The pre-existing paragraph (base fa7ae0c) already had "Small issues, tooling and documentation-only candidates" in the focused tier; local `--changed` selects the full matrix for workflow paths, which is a conservative selection aid, not a tier policy. Workflow, dependency and Dockerfile edits can be security, infrastructure or deployment impact (for example permissions, pinned actions, base images, package versions), so they must be classified by impact, with unresolved risk taking the full tier.
* Finding 4 (confirmed by artifacts): the committed behavior report records lead-authored scenarios, a proxy profile and a grader that did not read the examples table; the sandbox was removed after the run, contrary to the no-cleanup boundary. The report and log stay verbatim; the correction repeats the behavior test with retained evidence.

### Contrarian wave

* Alternative A: keep unconditional full tier for workflow/gate-tool/dependency/Dockerfile edits as conservative. Rejected: contradicts the owner's request that a small, demonstrably non-security tooling edit not pay the full gate; conservatism is retained through the "unresolved risk takes the full tier" rule.
* Alternative B: drop any mention of these file classes. Rejected: the guide would lose the real risk signal; keep them as explicit impact triggers to classify, not as categorical tiers and not as categorically safe.
* Alternative C: add a wrapper or CI step for the direct harness check. Rejected: needs workflow/source change that is not authorized; list as follow-up (already recorded).
* Alternative D: keep "Hosted-only" but rename. Rejected: the correct structure is Shared (executed both places), Local-only, Hosted-only (artifact upload, hosted runners, path filter, matrix), because C11-C15 show local counterparts.
* Counter-evidence check: the harness `--out` default creates the output directory only after scans (C7), so the direct command should name a new external directory; unchanged from the prior text.

## Parent Synthesis

* Accepted: all four findings. Decisions: (1) README direct-check text restates the full acceptance contract with how each element is checked directly; (2) README coverage bullets become Shared / Local-only / Hosted-only with named execution boundaries; (3) remove categorical full-tier wording in instructions, README lead, coordinator and the table row, replace with impact-based classification and an explicit "not categorically safe" statement; (4) repeat the behavior test with independently designed scenarios, resolved profile, retained sandbox, independent grading.
* Unresolved: host model restrictions may prevent resolving the High/Medium profile; record as proxy or Deferred honestly.
* Planning Readiness: Ready. Research disposition: executed.

## Evidence Notes

* Codebase evidence IDs C1-C23 above cite `path:line` as read in this worktree at HEAD 397ce435ae4dddfcf9279179656049b8b670b720. No external (W#) evidence was used.
