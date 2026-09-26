<!-- markdownlint-disable-file -->
# RPI Changes: Integrate the Proper North Homes sector archetype research into the knowledge base

## Metadata

* Task ID: RPI-2026-09-25-proper-north-homes-sector-archetype
* Related plan: [.copilot-tracking/plans/2026-09-25/proper-north-homes-sector-archetype-plan.md](../../plans/2026-09-25/proper-north-homes-sector-archetype-plan.md)
* Implementation date: 2026-09-25

## Execution Status

* Status: Complete
* Declared invocation scope: full plan
* Completed scope markers: P01 (P01-T01 to P01-T04), P02 (P02-T01 to P02-T03), P03 (P03-T01), P04 (P04-T01 to P04-T03)
* All remaining active-plan markers: none
* Status basis: every task's Requirements hold, each has a completed-work entry, and the P04-T03 checks passed

## Execution Summary

The sector archetype research is now filed in the knowledge base. The primer holds the sector evidence: scale, archetypes, the full tenure picture, lease responsibility rules for retrofit, national resident-needs rates and board capital patterns, with every source classified and dated. The company profile research holds one labelled Modelled Customer Profile, aligned comparators, gaps, sources and limitations, and a corrected SRS MEES line. The addendum cross-references the profile without copying figures, and the index and log record the change. Nothing is committed, and the changes sit uncommitted on branch `docs/typesafe-open-decision-review` for the user to move.

## Completed Work

### The primer explains sector concentration, stock-transfer history and housing association archetypes

* Related phase or task: P01-T01
* Files:
  * [docs/reference/research/sector/housing-association-primer.md](../../../docs/reference/research/sector/housing-association-primer.md)
* Behavior or functionality changed: `## Sector Scale and Context` now adds official RSH size counts (1,353 providers; 8 over 50,000 and 72 at 10,001 to 50,000 units; 10 groups at 50,000+ and 32 at 30,000+) and dated stock-transfer history, next to the unchanged portal rows and ranking caveat. The new `## Common Housing Association Archetypes` holds the eight-row archetype table with northern relevance and sources, states that the archetypes are an analytical grouping, and links to the modelled archetype in company research. No comparator groups are named.
* Validation: covered by P04-T03 (passed)

### The primer covers the full tenure picture and who is responsible for retrofit in lease-based homes

* Related phase or task: P01-T02
* Files:
  * [docs/reference/research/sector/housing-association-primer.md](../../../docs/reference/research/sector/housing-association-primer.md)
* Behavior or functionality changed: `## Tenure Types` gains supported housing, housing for older people and non-social leasehold rows (about 95,900 homes, up 91% since 2015), followed by the England provider mix from RSH Table 1.1. The new `## Retrofit Responsibility in Shared Ownership and Leasehold Homes` separates shared ownership from right to buy and preserved right to buy leasehold. It cites GOV.UK guidance, Housing Act 1985 Schedule 6 paragraphs 16B and 16C, SI 2003/1987 regulations 4 and 6, the local SRS MEES snapshot `## Leasehold` section and the GMCA WH:SHF Wave 3 copy, and classifies each. The section labels the allocation as internal interpretation subject to legal review, names the unchecked preserved right to buy provisions and the GMCA-only verification, and points to the sources table for snapshot status and change likelihood.
* Validation: covered by P04-T03 (passed)

### The primer gives national resident-needs rates and the sector pattern for board capital prioritisation

* Related phase or task: P01-T03
* Files:
  * [docs/reference/research/sector/housing-association-primer.md](../../../docs/reference/research/sector/housing-association-primer.md)
* Behavior or functionality changed: The new `## Residents and Vulnerability Data` gives the EHS and DESNZ rates with survey years (61%, 28%, 50%, 63%, 11.6% LILEE 2024), says they include council tenants, names 10.0% as the superseded LIHC figure, and states the vulnerability data-completeness position with the Housing Ombudsman May 2023 finding and links to the Awaab's Law Phase 1 and Phase 2 snapshots. The new `## How Boards Prioritise Capital` presents the four-step order as a sector-informed hypothesis with RSH Sector Risk Profile paragraphs, the VfM 2025 capital split, northern medians and the SRS MEES snapshot. It separates the GBP 7,500 grant cap from the GBP 10,000 spend exemption and sets the 91% interest cover figure against the 87% baseline figure without editing the baseline research. `## Funding Model` now points to the new board section.
* Validation: covered by P04-T03 (passed)

### The primer's sources, open questions, implications and limitations reflect the new evidence

* Related phase or task: P01-T04
* Files:
  * [docs/reference/research/sector/housing-association-primer.md](../../../docs/reference/research/sector/housing-association-primer.md)
* Behavior or functionality changed: `## Source and Evidence Status` now lists every added source with classification, source date, retrieval or conversion date, and a new column for local snapshot status and change likelihood. All four open questions stay open, and each has a nested note linking to `#modelled-customer-profile` that says what is modelled, what is unknown, and that company details are not yet confirmed. `## Evidence Limitations` no longer relies only on the portal article and lists the remaining limits. The implication bullets link to the new sections and keep their internal-interpretation label. The frontmatter `description` covers the wider scope; `ms.date` stays `2026-09-25`.
* Validation: covered by P04-T03 (passed)

### The company profile research holds one labelled modelled profile of Proper North Homes

* Related phase or task: P02-T01
* Files:
  * [docs/reference/research/company/company-profile-research.md](../../../docs/reference/research/company/company-profile-research.md)
* Behavior or functionality changed: The new `## Modelled Customer Profile`, placed after `## Comparable Organisations`, opens with a section-level label: every value is a modelled estimate from sector medians or aggregates, maps to `Sector-informed hypothesis`, and company details are not yet confirmed. It records the D1 archetype with the viable national-group alternative and three rejected options, the scale position (top-ten group, larger than the largest northern-concentrated group at about 40,191 units, most plausibly a recent merger), the attributes table, the D2 tenure table matching the plan contract with D3 leaseholders shown as additional, the lease interests needing legal review (about 2,940 and 1,750), resident indicators on about 57,060 households (34,800, 16,000, 28,500, 35,900, 6,600), and the board prioritisation hypothesis. `### Retrofit Volume Versus Quality` keeps the Karbon-based 13,800 scenario and cross-references the separate 15,000 to 15,600 range. No W4 comparator groups are named.
* Validation: P04-T03 (passed). Derived counts recomputed: tenure rows sum to 60,000; 51,960 x GBP 101 x 52 is about GBP 273 million; per-unit ranges x 60,000 give GBP 291 million to 318 million and GBP 70 million to 83 million; resident rates x 57,060 round to the stated counts.

### The rest of the company profile research is consistent with the modelled profile

* Related phase or task: P02-T02
* Files:
  * [docs/reference/research/company/company-profile-research.md](../../../docs/reference/research/company/company-profile-research.md)
* Behavior or functionality changed: `## Comparable Organisations` notes that Karbon, Onward and Together are smaller than 60,000 homes, that Thirteen and Home Group sizes are not recorded, and links to the scale position. Gap items 1, 4, 6 and 7 each note that a modelled estimate exists and needs company confirmation; the other gaps are unchanged. `## Sources` gains `### Sector Statistics and Modelled Profile`. `## Evidence Limitations` adds the median, national-rate, alternative-archetype, lease-review, GMCA and preserved right to buy limits. `## Purpose` keeps the 10 September statement and adds the 25 September note. `ms.date` is `2026-09-25`.
* Validation: P04-T03 (passed)

### The company profile Regulatory Baseline states the SRS MEES final policy position

* Related phase or task: P02-T03
* Files:
  * [docs/reference/research/company/company-profile-research.md](../../../docs/reference/research/company/company-profile-research.md)
* Behavior or functionality changed: The bullet that called EPC C "a policy objective or proposal" is replaced. The new text gives the 2026 government response as final policy, not by itself a commenced duty, with EPC C on one reformed-EPC metric by 1 April 2030, a second by 1 April 2039, and a GBP 10,000 per-property spend exemption per metric lasting 10 years. It cites the local snapshot sections, the 19 September 2026 conversion date and the register's `Medium` likelihood and monthly-then-quarterly cadence, and keeps the Decent Homes sentence. The recheck note records that this line was rechecked on 25 September 2026 against the local snapshot only.
* Validation: P04-T03 (passed); wording checked against the snapshot `### Compliance date and metrics` and `### MEES Specific Spend Exemptions` and the register row

### The addendum points readers to the modelled profile without copying it

* Related phase or task: P03-T01
* Files:
  * [docs/case_study_48_addendum.md](../../../docs/case_study_48_addendum.md)
* Behavior or functionality changed: `## Provisional Sector Baseline` gains a paragraph after the baseline research reference that links to `./reference/research/company/company-profile-research.md#modelled-customer-profile`, names what the profile covers, and says its values are modelled estimates with company details not yet confirmed. `### Additions Since the Original` gains one bullet. No modelled figures were copied, and `ms.date` is `2026-09-25`. The original case study is unchanged.
* Validation: P04-T03 (passed)

### The knowledge base index catalogues and routes to the new content

* Related phase or task: P04-T01
* Files:
  * [docs/reference/README.md](../../../docs/reference/README.md)
* Behavior or functionality changed: The primer and company profile catalogue summaries describe the new content (company profile now dated 2026-09-25), the addendum row is dated 2026-09-25, and `## Task Routing` has a new row sending tenure, leasehold, resident or financial-scale estimates to the Modelled Customer Profile, then the primer. No catalogue rows were added, and the index `ms.date` stays `2026-09-25`.
* Validation: P04-T03 (passed)

### The log records the filed answer, contradictions and open questions

* Related phase or task: P04-T02
* Files:
  * [docs/reference/log.md](../../../docs/reference/log.md)
* Behavior or functionality changed: One entry, `## [2026-09-25] query | File back the sector archetype research`, is appended at the end. It lists the files touched, the 10.0% to 11.6% fuel poverty correction, the unreconciled 91% against 87% interest cover basis difference, the corrected EPC C line, the three open questions, the 2026-09-25 retrieval date and the modelled-estimate caveat. Earlier entries are byte-for-byte unchanged, with the diff showing 33 insertions and no deletions.
* Validation: P04-T03 (passed)

### Links, labels, figures, style and change boundary were checked across the changed files

* Related phase or task: P04-T03
* Files:
  * The five changed documents above
* Behavior or functionality changed: No content change. The review confirmed that the changed files are consistent, and results are recorded in the validation record below.
* Validation: passed; see the validation record below

## Implementation-Time Plan Updates

### Snapshot status and change likelihood consolidated into the primer's source table

* Affected plan area or markers: P01-T02, P01-T04
* What changed: Local judgement, no plan text change. P01-T02 asks for "no local snapshot" marking and change likelihood; P01-T04 asks for every source in `## Source and Evidence Status`. To avoid two source tables, the primer holds one table with an added `Local snapshot and change likelihood` column, and the lease section points to it.
* Why: A single source table avoids duplicate, divergent citations
* Triggering evidence: overlapping Requirements in P01-T02 and P01-T04
* User answer or decision: none
* Reconciliation performed: none needed in the plan
* Planning and critique state: not needed

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Relative links and heading anchors resolve | Five changed files | Passed | Temporary script (outside the repository, deleted afterwards) checked 127 relative links, including every `#modelled-customer-profile` and new primer anchor, with 0 problems |
| Modelled-estimate labels | Company profile, primer, addendum | Passed | All modelled Proper North Homes values sit under the `## Modelled Customer Profile` section-level label or its subsections; the primer and addendum carry links, not modelled values |
| Numeric fidelity | P02-T01 table contract, research Q2, Q3 and Q5 | Passed | Tenure rows sum to 60,000 (44,400 + 7,560 + 3,600 + 1,500 + 2,940); resident counts reproduce from 57,060 x the stated rates; rent roll, cost and works ranges reproduce from per-unit medians; 1,750 / 60,000 is about 2.9% |
| ASCII punctuation, no em or en dashes, `*` bullets, no bolded-prefix list items | 576 added lines | Passed | Script scan of `git diff -U0` added lines found no issues |
| Heading hierarchy and table style | Five changed files | Passed | New sections use the files' existing `##` and `###` levels and `\| --- \|` tables |
| Change boundary | `docs/` and `.github/` | Passed | `git --no-pager diff --stat` and `git status --short` show only the primer, company profile research, addendum, index and log modified, plus this task's untracked `.copilot-tracking/` artifacts. Original case study, baseline research, regulatory snapshots and agents unchanged |
| Line endings | Five changed files | Passed | After fixing mixed line endings introduced during editing, `git ls-files --eol` reports `w/crlf` for all five, and the log diff is 33 insertions with no deletions |
| Rendered Markdown preview | Five changed files | Skipped | No preview was run; structure was reviewed in source |

## Pre-Review Reconciliation

* Plan markers and task-local context: current; all `Pxx` and `Pxx-Txx` markers checked
* Completed-work entries and handoff prose: current; one entry per task
* Validation, blockers, remaining work, and follow-up items: current
* Review readiness: ready for review

## Blockers

* None

## Remaining Work

* None within the plan

## Follow-Up Items

* Canonical plan list: [.copilot-tracking/plans/2026-09-25/proper-north-homes-sector-archetype-plan.md](../../plans/2026-09-25/proper-north-homes-sector-archetype-plan.md), `## Follow-Up Items`
* Snapshot the web-only regulatory sources cited in the primer into `docs/reference/regulatory/` with register rows and change likelihood. Owner: user, through a later ingest task.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; P01 to P04 and all tasks checked; no remaining active-plan markers
* Validation coverage: links and anchors, labels, figures, style, boundary and line endings passed; rendered preview skipped
* Blockers: none
* Current plan updates: none to plan text; local judgement recorded for the single consolidated source table in the primer
* Planning and critique state: current; critique PCA-001 disposed during planning, no new critique needed
* Follow-up items: snapshot ingest of web-only regulatory sources (user); preserved right to buy check, national DESNZ WH:SHF check and lease sample review remain open questions in the documents
* Review readiness or no-handoff reason: ready for `/rpi-review`
* Continuation owner: user
