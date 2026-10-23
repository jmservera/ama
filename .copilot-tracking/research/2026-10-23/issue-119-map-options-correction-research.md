<!-- markdownlint-disable-file -->

# Task Research: issue-119-map-options-correction

| Field | Value |
| --- | --- |
| Date | 2026-10-23 |
| Researcher / agent | rpi-research (actual skill invocation, session 07e1e254-42ed-44c3-9761-d5f76a7248c3) |
| Status | Complete |
| Research disposition | executed (internal evidence only; no live web retrieval, by owner scope) |
| Artifact path | .copilot-tracking/research/2026-10-23/issue-119-map-options-correction-research.md |

## Process disclosure

This is the extra correction cycle for #119 (earlier: P04 on 2026-10-20 and P06
on 2026-10-21, plus the distinct security regression P05). The owner answered
"Authorize one additional ordered correction cycle" on 2026-10-23. It grants
exactly one extra correction and waives no review, local validation, receipt
currency or human gate. The phase order in this cycle is research, plan (with one
critique), implement, review, each from an actual skill invocation. Earlier
artifacts, the original Review, the recovery critique and the failed and
historical receipts are preserved unchanged. The earlier claim that the recovery
plan's AC1 and PC-001 were satisfied was not borne out by the committed options
review (finding MAP-002); this cycle corrects the document and records that
honestly.

## Research Brief

* What to research: two independent-review findings on head 0e7c9f9a:
  MAP-001 (stale USD500 and USD535.41 budget wording) and MAP-002 (missing
  draft-unverified labels).
* Scope: documentation only. Non-goals: provider selection, any licence, cost,
  processor or DPA decision, new web retrieval, source feature change,
  accessibility acceptance. Both original issue criteria stay unmet and the
  screen reader remains NOT RUN.
* Output mode: analysis. Prepares planning: yes.
* Posture: focused (two named findings, named files); provenance: default.
* Edits allowed during research: this file only.

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instruction | repository AMA instructions (knowledge base index and log, dated regulatory and budget claims, Markdown style) | selected |
| Skill | web-design-guidelines and design skills | skipped: no web file is edited |
| Specialist | RPI Researcher | skipped: two small inline lanes |

## User Participation

No interaction needed: the owner authorization and coordinator brief fix scope.

## Prior Knowledge Gate

* Independent review: review.md of session b9cc4727 (MAP-001, MAP-002; the reviewer did not verify the receipt).
* Issue blocker comment 6370090787 on #119 (coordinator-confirmed findings).
* Recovery research (2026-10-20) evidence log and its statement that the draft claims about OS Maps API docs, MapTiler and Azure geography/auth pages were not re-read.

## Research Cycle Log

### Cycle 1

Wider: listed every place the options review, ADR 0002 delta, index and log
state budget or vendor facts, and every vendor claim in the options table and
the bullets after it.

Deeper: read the cost paragraph and the addendum budget synthesis, and mapped
each vendor claim to the evidence the recovery research actually re-read.

Contrarian: checked whether the recovery implementation commits added any label
beyond the OS-rate caveat (they did not; C5), and whether the USD535.41 figure
has an in-repository source or current status (it is a 2026-10-21
coordinator-supplied provisional forecast, treated by the addendum as
2026-10-20 history on the USD500 basis, with no post-change forecast yet).

Parent synthesis: accepted both findings as confirmed. Rejected new web
retrieval (out of scope) and any rewording of history as current. Deferred all
vendor verification to the owner or procurement. No further cycle: remaining
gaps need vendor pages or human decisions, not more repository reading.

## Evidence Log

| ID | Evidence | Source |
| --- | --- | --- |
| C1 | Cost paragraph states USD500 as the owner budget, an expiry, and the provisional USD 535.41 RG-only projection as already exceeding it, with no in-repo source | docs/reference/research/ux/map-tile-provider-options.md:104-125 |
| C2 | Current owner decision: USD 700 replacement all-in forecast ceiling; authorization still expires 2026-10-25T16:02Z; the USD 500 total, its thresholds and the 535.41 projection are 2026-10-20 history; no post-change forecast exists; no resource retirement authorised | docs/case_study_48_addendum.md:330-345 |
| C3 | Refresh gate: a refreshed post-change forecast with fresh inventory and a complete post-change day is required before any tranche; unknown spend or an unapproved tranche blocks | docs/case_study_48_addendum.md:395-414 |
| C4 | Vendor table rows B, C and D and the bullets after them state OS Maps API, OS attribution, rate limits and authentication advice, MapTiler plans and privacy, Azure geography, ARM regions, Learn transaction rules, Gen1 retirement and the Entra requirement without an evidence-status label | docs/reference/research/ux/map-tile-provider-options.md:59-64, 78-98, 104-107 |
| C5 | The recovery implementation commits 92b55fa7 through 8509d007 added only the secondary OS-rate caveat, while the PC-001 line and AC1 claim labels were applied | .copilot-tracking/plans/2026-10-20/issue-119-map-options-recovery-plan.md:50, 70 |
| C6 | The ADR 0002 delta repeats the Azure geography ("not the uksouth pilot region") and the Entra inference without a draft label | docs/adrs/0002-pilot-readiness-architecture.md:688-700 |
| C7 | Recovery research confirms re-read only W1 (OSM tile policy) and W2 (Azure Maps pricing page: free 5,000 base-map transactions, paid rate blank); W3 and W4 are secondary; OS docs, MapTiler and Azure geography/auth pages were not re-read | .copilot-tracking/research/2026-10-20/issue-119-map-options-recovery-research.md:95-102 |

## Findings Mapped to Questions

* Q1 MAP-001: the cost paragraph treats the superseded USD500 cap and the 535.41 forecast as governing. The addendum (C2, C3) supersedes them. Correct wording: USD500 and 535.41 are dated history (2026-10-20 and 2026-10-21); the current owner decision is the USD 700 all-in ceiling expiring 2026-10-25T16:02Z; actual all-in forecast and headroom are Unknown; 535.41 is not a current liability or fresh forecast; paid execution needs verified all-in headroom and a finite separate approval; nothing authorises retiring a resource. Link the addendum subsection.
* Q2 MAP-002: claims with a confirmed re-read are limited to W1 and W2 (C7). Everything else the table and bullets state about Azure Learn pages (transaction rule, Gen1 retirement, geography, ARM regions), the OS Maps API, branding, rate limiting and authentication pages, the OS Data Hub terms status and MapTiler pricing, terms and privacy is retained pre-RPI draft material: draft, unverified for this proposal. The ODbL and OSM copyright statements and the Protomaps and Geofabrik pointers are likewise not re-read.
* Q3 Scope of repeats: the table rows, the Option B, C and D bullets, the Entra implementation inference (labelled inference, but its Azure Maps premise is a draft claim), the cost method sentence citing Learn, the unverified list intro, and the ADR 0002 delta.
* Q4 Index and log: the index row and a new append-only log entry must describe the correction precisely without rewriting earlier entries.

## Alternatives and Decision State

* Add a single footnote: rejected, because the claims are stated as established in many places and MAP-002 requires consistent correction.
* New web retrieval to verify: rejected by owner scope for this cycle.
* Chosen direction: add an evidence-status legend, label each vendor row and bullet claim, restate the cost paragraph as dated history plus the current addendum position, and append dated corrections to the changes, plan and state records. No provider selected.

## Open Questions, Risks, Residual Uncertainty

* All vendor rates, terms, attribution wording and DPA positions remain unverified; screen-reader run NOT RUN; both issue criteria unmet.
* Current all-in forecast and headroom are Unknown; no paid execution.
* Risk: over-labelling could read as a downgrade of W1 and W2; keep those labelled re-read 2026-10-20.

## Potential Next Research

Owner or procurement verification of vendor pages; human screen-reader run; refreshed post-change forecast.

## Planning Readiness

Ready for a docs-only correction plan with one critique.

## Self-check

Brief, parameters, evidence IDs, three waves, disposition and readiness are
recorded. No source file edited, no web retrieval, no secret used.

## Linked artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-23/issue-119-map-options-correction-research.md](.copilot-tracking/research/2026-10-23/issue-119-map-options-correction-research.md) | This correction research |
| [.copilot-tracking/research/2026-10-20/issue-119-map-options-recovery-research.md](.copilot-tracking/research/2026-10-20/issue-119-map-options-recovery-research.md) | Original recovery research, preserved |

## Next Steps

Active parent action: invoke rpi-plan for the correction plan and its single critique.
