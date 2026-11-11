---
title: Handoff waiting screen feature-wave checkpoint plan critique (Refs #440 #83)
description: One independent critique pass over the research, plan and details before Root admission
ms.date: 2026-11-11
---

## Execution

One read-only `rubber-duck` subagent pass (model `claude-sonnet-5.5`, sync) over the research, plan and details, compared with the previous checkpoint artifacts and the last pack section. It ran no test, installed nothing and edited nothing. Verdict: conformant after fixes (no blocking finding). No critique is repeated for this task.

## Findings and dispositions

| Id | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| WC-01 | medium | The plan assumed every browser class takes the heavy lock. In the candidate only W1 (`WaitingViewBrowser`) and W3 (`UnacceptedDownloadBrowser`, via `heavy_lock_or_none`) do; the W2 browser class (`HandoffReadGuidanceBrowser`) launches Chromium with no lock, so a busy lock would not skip it | Applied and re-read by the author (`setUpClass` at the candidate has no lock): research, plan and details now say W1 and W3 take the lock non-blocking and skip when busy, W2 takes none, the preflight lock-free and memory check protects W2, and W2 never runs concurrently with W1 or W3 |
| WC-02 | low | The venv install line departs from the component README (`--no-deps`, orchestrator) without saying so, and the package index contact and the `playwright==1.64.0` pin were not stated | Applied: the pin from the `dev` extra is stated, the deviation and the unverified need for importer helpers are recorded, the index contact is recorded |
| WC-03 | low | The pack contract did not carry the previous section's opening disclaimer in an adapted form | Applied: an adapted opening statement is required (draft, not approved, local observed on synthetic fixtures, no acceptance) |
| WC-04 | low | The five brief-mandated headings were not tied to the `###` structure of the earlier sections | Applied: used as `###` subsections, template tables fold into them |
| WC-05 | low | The inherited 10 cases of W6 come from `Matrix` in `tests/test_role_matrix.py`, not named | Applied: pointer added; the count is re-derived at the admitted main |

Checked and found correct by the critique: base and candidate identities and tree ids; ancestry of `b7d66e42`; blobs and statuses of BRD, PRD and ADR documents; per-class static counts and the 45, 69 and 81 reconciliation; `ZF_BROWSER_TESTS` gating; the `PYTHONPATH` shape; requirement rows and the #83 BRD source-reference drift; screen behaviour claims (unscoped GET, null `approved_limit_hours`, abort and 401, 403, malformed, valid empty, recheck, no automatic escalation); owner-brief boundaries; Markdown style; stop rules and admission gate.

## Limitations

The critic is the same model family as the author. It read artifacts and source, not a hosted or runtime result, and ran no selector, so selector resolution and counts are static reads. The author re-read the one medium finding in the candidate source before applying it. The critique does not review PR 1444's merge, which has not happened.
