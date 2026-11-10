# Issue 74 qualified audit supplement: correction and outcome mapping

Date: 2026-11-10. Supplements [the original matrix](2026-11-10-issue-74-main-acceptance-matrix.md) (commit `f6621435387f0d2e6cf5eef2946e7117a17617cf`), which is preserved unchanged apart from one appended pointer line. Plan: [plan](../plans/2026-11-10-issue-74-qualified-audit-plan.md).

Evidence class: documentation qualification only. No new browser, API or core run was made and this is not a fresh current-main audit. All observations remain attributed to base `c66370042eb08f07839d054433f4483078703cf2` and the original source-qualified constructed synthetic fixture, even if main has advanced. Nothing here is real customer, human, assistive-technology, hosted-CI or live acceptance. #74 and #73 remain open; criterion 2 is not ticked, narrowed or closed.

## Correction of the browser count (2026-11-10)

Source: independent reviewer `16d01594-c6d6-4270-846d-52f621953fe8`, Low finding; confirmed by direct count of the original raw log.

| Item | Original statement | Corrected from the raw log |
| --- | --- | --- |
| Browser `home_case_browser_check` output | "17 PASS lines" (original matrix line 18, original state decision, original external handoff) | 16 lines begin `PASS` (log lines 1-14, 16, 17); line 15 is `COMPLETE: all checks ran, including axe 4.10.3`; line 18 is `exit=0`; 18 lines in total |
| Exit, skips, axe, writes, JavaScript errors | exit 0, no skips, axe 4.10.3 zero violations, no non-read requests, no JS errors | Unchanged; each has its own PASS line in the log |
| Core and API | 7 ok, 3 ok | Confirmed in the raw logs (`Ran 7 tests ... OK`, `Ran 3 tests ... OK`) |

Raw log `03-core-home-case.log`, `04-api-home-case.log` and `05-browser-check.log` (sha256 `6dfcd77b9d9b4b2b8d614f844e57220ed6f64da9e1f9d512ed39fb49ca79f273`) are in the Root evidence folder `phase74-main-acceptance-audit-evidence-1110` and were not edited. Wherever the original artifacts say 17, read 16 PASS plus one COMPLETE line. This correction does not change any status, gap or recommendation.

## Planning-only outcome interpretation (synthetic demo)

Root adopted, for planning only, the Housing Data and Performance Lead's provisional synthetic-demo interpretation (`domain-demo-acceptance-1932.txt`, section 1). A home outcome is a tuple, not one success badge. It is not a customer baseline, an approved requirement, observed positive acceptance, resident consent or a new UI implementation. PRD v0.21.0 is `in-review`; BRD v0.21.0 is `draft`.

| Outcome component | Already observed (finance role, constructed fixture, base c663) | Unknown or unobserved | Original gap | Smallest future proof slice (not started) |
| --- | --- | --- | --- | --- |
| Current stage with as-of, source, version, holds, reopening | `Stage:` token in the home region for ZF-2; version status and no-transfer notice shown; building holds in the building region only | Stage value, as-of and source not asserted; reopening not asserted | G6 (and G5 for scope) | Assert stage value and version text in the home region for two homes |
| Per-measure disposition with evidence and version, or Unknown | Core shows sibling document and quality absent from ZF-2 links | Own-home documents and quality disposition never positively asserted; ZF-3 never opened in the browser; Unknown rendering not asserted | G2 | Two-home assertion that each home region shows only its own documents and quality state, including an explicit Unknown |
| Resident handover evidence or Unknown | Nothing observed | Whether the screen renders handover evidence or Unknown at all | None (new, falls under owner definition of outcome) | Owner confirms the field; then one assertion of handover or Unknown per home |
| Intended versus measured performance, or Not measured | Nothing observed | Whether the screen renders performance or Not measured; no invented EPC or bill saving permitted | None (new) | Owner confirms the field; then one assertion of Not measured when no evidence exists |

Building applicability: the screen lists every building item without showing each item's `case_ids` or `package_ids` (G5). The domain advice asks that affected home or package scope, or unknown applicability, be shown; that display is not observed.

## Field status after the qualification

Vocabulary: local-observed, implemented-unverified, blocked, unknown. Statuses are those of the original matrix; none is upgraded.

| Field | Side | Status | Role observed | Exact remaining action |
| --- | --- | --- | --- | --- |
| Dependencies, holds, works, costs | building | local-observed | Finance only | Non-finance rendering check (G3) and amount assertions over HTTP (G4) |
| Shared systems | building | implemented-unverified | None | Assert SYS-1 in the building region and not the home region (G1) |
| Evidence documents | home | implemented-unverified | None | Own-home document assertion on two homes (G2) |
| Decision | home | local-observed | Finance only | None for the finance role |
| Cost allocation | home | local-observed | Finance only | Non-finance restricted rendering (G3) |
| Outcome (stage) | home | implemented-unverified for value; token only | Finance only | Owner definition accepted; stage value assertion |
| Outcome (quality, handover, performance) | home | unknown | None | Owner definition and G2 slice |
| No same-building transfer | both | local-observed (criterion 3, preserved) | Finance only | None |
| Real customer, human, AT, live and SQL Server acceptance | all | blocked | None | Outside this local evidence; requires separate approved work |

## Suggestion for Root

No tick or closure of criterion 2 is suggested. The literal criterion is not fully evidenced: shared systems, own-home documents and the outcome tuple are not asserted, only the finance role was observed, and "outcome" lacks an approved owner definition. Root decides after independent exact-head assessment. Ranked proof slices: first G1, G2 and G3 assertions (smallest, no new data model), then owner confirmation of the outcome fields and G5 display, then manual keyboard and screen-reader review and SQL Server durable-store acceptance.
