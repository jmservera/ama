<!-- markdownlint-disable-file -->

# Phase Details: issue-119-map-options-correction

Plan: .copilot-tracking/plans/2026-10-23/issue-119-map-options-correction-plan.md
Evidence: .copilot-tracking/research/2026-10-23/issue-119-map-options-correction-research.md (C1 to C7)

## P01 MAP-002 evidence-status labels

* P01-T01: After the Status and boundary paragraph add a legend. "Re-read 2026-10-20" covers only the OSM tile policy (W1) and the Azure Maps pricing page free allowance and blank paid rate (W2) plus the code reads. "Draft, unverified" covers claims retained from the pre-RPI draft and not re-read in recovery. "Secondary, unverified" is a search summary. State that the existing "read 2026-10-20" column dates the draft read, not a recovery re-read, and that no claim is a verified vendor term.
* P01-T02: In rows A to E, label each claim by status. Row A: policy terms re-read; ODbL and copyright page draft, unverified. Row B: pricing free allowance re-read, paid rate blank; Learn transaction rule, Gen1 retirement, geography, ARM regions, secondary processor claim draft, unverified. Row C: all OS docs, attribution, rate limit, authentication, terms status draft, unverified; plans secondary. Row D: all draft, unverified. Row E: all draft, unverified. Evidence: C4, C7.
* P01-T03: Apply the same labels in the Option B, C and D bullets, the Entra premise sentence (premise draft, unverified; the inference stays an inference), the OS proxy advice, the cost method Learn sentence and the unverified list intro. No new retrieval.
* P01-T04: In the ADR 0002 map delta add "draft, unverified" to the Azure geography and Entra statements and to the Ordnance Survey summary, pointing to the options review legend. Evidence: C6.
* P01-T05 (PC-001, PC-002): before editing, build a claim inventory in the changes record listing each location (table rows A to E, Read column, Option A, B, C, D, E bullets, Entra premise, cost method, unverified list, ADR delta) with its evidence status. Row A also labels the OSMF privacy statement and the no-DPA statement. Row B separates the re-read free allowance and blank paid rate from the Learn rule, the derived 75,000 figure (calculated from a draft rule) and the secondary 4.50 figure. The Read column heading note says dates are draft-read dates. After editing, grep the document for each vendor name and Learn, docs.os.uk, maptiler, ODbL, Protomaps and Geofabrik to confirm every hit carries a label.
* Done when: AC1 holds by the inventory and the grep.

## P02 MAP-001 cost paragraph

* P02-T01: Rewrite the budget part of the cost paragraph. State: the USD 500 October total, its expiry basis and the coordinator-supplied provisional resource-group-only USD 535.41 (reported 2026-10-21, no in-repository source, not live) are dated history on the superseded basis; current owner decision is the USD 700 all-in forecast ceiling for the month, authorization expiry unchanged at 2026-10-25T16:02Z, current all-in forecast and headroom Unknown, the 535.41 not a current liability or fresh forecast and not to be added to or subtracted from anything; no paid execution without verified all-in headroom and a finite separate owner approval; no resource retirement authority. Link ../../../case_study_48_addendum.md#revised-owner-budget-decision-2026-10-22 and cite its refresh gate (no tranche before a refreshed post-change forecast). Also reword Row E's "existing monthly budget" and the unverified list so no sentence implies a current cap. After editing, grep the document for USD500, USD 500 and 535.41 and confirm each hit is framed as dated history. Evidence: C1 to C3.
* Done when: AC2 holds.

## P03 Index, log and tracking

* P03-T01: Update the index paragraph in docs/reference/README.md to say vendor claims are labelled by evidence status and the budget wording follows the addendum; set ms.date to 2026-10-23 on the options doc, README and ADR 0002 (frontmatter only, ADR 0002 because its delta is edited) and add the correction date to the Status paragraph.
* P03-T02: Append a log entry dated 2026-10-23 (correction) stating both findings, what changed, that it supersedes only the budget and verification wording of the earlier 2026-10-20 entries, which are retained, and that nothing is selected, bought or accepted.
* P03-T03: Create the changes record and a new state file for this cycle recording phase order, the acknowledgement that the recovery PC-001 and AC1 completion statements were not borne out (MAP-002), the owner extra-correction decision, and residuals. Original artifacts, including all 2026-10-20 and 2026-10-21 tracking files, are untouched; the acknowledgement lives only in the new 2026-10-23 changes record and state file.
* P04 stop rule (PC-006): if the single Review returns a Medium or higher finding, record it as a residual and follow-up, commit nothing further, and stop; no further correction or second Review.

## P04 Validate, Review, commit

* P04-T01: git diff --check; ASCII scan of added lines; relative link existence check for changed Markdown; `python3 -m unittest tests.test_accessibility_baseline` from src/api as a static check, not accessibility acceptance. No full gate, Docker or Azure.
* P04-T02: one rpi-review of the working diff, recorded under reviews/logs/2026-10-23; findings route to follow-up, no second Review.
* P04-T03: resolve gh api user identity, repository-local email, Conventional Commit and Copilot trailer. No push.
