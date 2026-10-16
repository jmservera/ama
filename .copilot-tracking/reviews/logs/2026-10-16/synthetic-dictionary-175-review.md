# Review: issue-175 / synthetic-dictionary-175

## Execution and Boundary

Execution: Complete. One post-implementation review of the complete supplied
issue boundary, not a security audit or operational acceptance.
Direct review; no additional worker needed for the cohesive bounded diff.

Artifacts: .copilot-tracking/research/2026-10-16/synthetic-dictionary-175-research.md;
.copilot-tracking/plans/2026-10-16/synthetic-dictionary-175-plan.md;
.copilot-tracking/details/2026-10-16/synthetic-dictionary-175-phase-details.md;
.copilot-tracking/plans/2026-10-16/synthetic-dictionary-175-critique.md;
.copilot-tracking/changes/2026-10-16/synthetic-dictionary-175-changes.md.

Source boundary: core privacy checker and provenance tests, agents generated-chat
tests, dictionary/register and the directly related README/index/log changes.

## Reconciliation

P01 tasks and P02-T01 have recorded evidence; P02-T02 is pending this review and
PR delivery. Critique PC-001/002/003 were directly dispositioned. The documented
outside-repository temporary directory exception preserves the actual stock
generator guard; it is not a source/schema change. No repeat critique planned.
AC2 remains a blocker and follow-up, not a completed approval.

## Validation Evidence

76 selected tests passed; core and agents full-project ruff/format/mypy passed.
Public CLI returned zero; source-audit CLI returns one for three known sources.
Isolated local app /healthz and landing returned 200. Added 21 Markdown links
and anchors resolve; diff whitespace check passed.
Sensor fixture tests emit pre-existing unclosed-file ResourceWarnings.
No private corpus, official-source currentness, actual model, Azure, SQL Server,
full application workflow or human/DPO acceptance is claimed.

## Findings and Outcome

Outcome: Residual work. Not a conformant/full issue acceptance outcome.
No functional defect identified for the current trusted register and supported
generated snapshots. No source edits or second Review performed in this phase.

### RV-001 (High): External provenance incomplete

AC2 is unmet: SRC-CENSUS-TS054, SRC-IMD-2025 and SRC-ONS-BOUNDARIES still
have null retrieval dates and provisional licence/attribution wording.
The actual source audit reports each missing/provisional field and returns 1.
This is preserved source evidence, not a failing unit-suite or silent success.
Route: distinct rpi-research follow-up to verify original retrieval evidence
and official licence/attribution terms with Juan Manuel Servera; no automatic
legal interpretation or operational reliance. The offline constraint prevents
resolving it in this delivery.

## Acceptance Matrix

| Criterion | Result | Evidence |
| --- | --- | --- |
| Dictionary coverage including sensor/chat | Met for known families | Updated dictionary/register includes stock EPC, scale/fabric, all public evals and generated/runtime chat; IDs/anchors and public-payload completeness checked |
| External licence/date/attribution | Unmet | RV-001, three explicitly rejected historic source entries |
| Automated pattern/label rejection | Met for bounded contract | Core production CLI mutations independently refresh hashes for all four patterns and row labels; agents mutate all nine chat payloads; inherited/exempt public text remains scanned |
| Public/private separation | Met locally | Fresh tiny fixtures, public-only scan, private-location reclassification rejection and ignored-path checks; original private-stock-reading tests removed |

The original issue stays open and its checkboxes remain unchanged. Existing
generator bytes are preserved by determinism/eval regressions; no real tenant
or map datasets are included in the diff. Runtime personal data, human/DPO
approvals, actual legal sources and operational deployment remain outside
the synthetic fixture guarantee.

## Recommended Destination

Deliver the bounded offline PR with Refs #175 and explicit RV-001/AC2 disclosure.
Do not claim the entire issue complete. The only ranked evidence-backed
follow-up is source-provenance verification (rank 1: direct acceptance blocker).
