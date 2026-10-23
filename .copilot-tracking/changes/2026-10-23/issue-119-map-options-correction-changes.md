<!-- markdownlint-disable-file -->

# Release Changes: issue-119-map-options-correction

Plan: .copilot-tracking/plans/2026-10-23/issue-119-map-options-correction-plan.md
Details: .copilot-tracking/details/2026-10-23/issue-119-map-options-correction-phase-details.md
Date: 2026-10-23. Session: 07e1e254-42ed-44c3-9761-d5f76a7248c3. Starting head 0e7c9f9a5a9bc7d56d6b6a01a68ec015929ae39e on main 140d8f494482c78e84d15f3d46b9223d3c487af0.

## Phase order (genuine)

1. rpi-research: correction research (2026-10-23).
2. rpi-plan: plan and details, then one critique by a fresh worker (verdict Revise, 6 planner-direct findings applied; no second critique).
3. rpi-implement: this record.
4. rpi-review: single Review, recorded under reviews/logs/2026-10-23.

Owner authorization: "Authorize one additional ordered correction cycle", exactly one extra correction after P04 and P06; no waiver of review, local validation, receipt currency or human gates.

## Honest acknowledgement (MAP-002)

The recovery plan (2026-10-20) AC1 required every draft vendor claim not re-read
to be labelled draft-unverified, and its PC-001 disposition recorded the labels
as applied. The committed options review at 0e7c9f9a did not carry them: the
recovery implementation added only the secondary OS-rate caveat. That earlier
completion claim was not borne out. This cycle corrects the document. The
original recovery plan, details, critique, Review, changes, state and all failed
or historical receipts are unchanged; no earlier artifact is renumbered or edited.
The earlier Review passed that head without catching it, which is preserved as
history.

## Claim inventory (P01-T05)

| Location in map-tile-provider-options.md | Status label applied |
| --- | --- |
| Status legend (new) | defines re-read, draft unverified, secondary unverified; Read column is the draft read date |
| Row A policy terms | re-read (W1); ODbL copyright, community-edited coverage, OSMF privacy and no-DPA statements draft, unverified |
| Row B pricing page free allowance and blank paid rate | re-read (W2) |
| Row B terms, UK detail, Gen2/Gen1, 15-tile rule, 75,000 figure (derived), geography, ARM regions, processor | draft, unverified or secondary, unverified |
| Row C all OS pages, attribution, rate limit, authentication, plans | draft, unverified or secondary, unverified |
| Row D all MapTiler statements | draft, unverified |
| Row E ODbL, Protomaps, Geofabrik, privacy and "not now" position | draft, unverified; budget wording now refers to the all-in ceiling |
| Options B, C, D bullets, Entra premise, proxy advice | labelled; Entra premise draft, unverified, inference stays an inference |
| Cost method Learn sentence and unverified list intro | labelled |
| ADR 0002 map delta | labelled and linked to the legend |

## P01 MAP-002 labels (complete)

* docs/reference/research/ux/map-tile-provider-options.md: legend, row and bullet labels as above; ms.date 2026-10-23.
* docs/adrs/0002-pilot-readiness-architecture.md: map delta labelled; ms.date 2026-10-23.

## P02 MAP-001 cost paragraph (complete)

* The cost paragraph now separates the Learn-rule sentence (draft, unverified), the current budget position (USD 700 all-in ceiling, expiry 2026-10-25T16:02Z unchanged, headroom Unknown, refresh gate, verified headroom and finite separate approval needed, no retirement authority, link to the addendum) and the superseded history (USD500, USD 535.41 dated, not current).
* Grep for USD500, USD 500 and 535.41 shows hits only inside the history paragraph.

## P03 Index, log, tracking (complete)

* docs/reference/README.md: index paragraph and ms.date updated.
* docs/reference/log.md: appended 2026-10-23 correction entry; zero deleted log lines.
* This record and .copilot-tracking/rpi-sessions/2026-10-23/issue-119-map-options-correction-state.json.

## P04 Validation (this implement phase)

* git diff --check: pass. Non-ASCII scan of added lines: none. Deleted lines: 52, none in log.md.
* Relative links and the addendum anchor revised-owner-budget-decision-2026-10-22 verified to exist.
* Label grep of Learn, docs.os.uk, maptiler, ODbL, Protomaps, Geofabrik, eu.atlas: every hit is labelled.
* src/api tests.test_accessibility_baseline (7 tests) pass: a static check, not accessibility or screen-reader acceptance.
* Not run: the full gate, Docker, Azure, any web retrieval. Prior receipts for 0e7c9f9a are historical after this change; the coordinator runs a fresh exact-head gate.

## Residuals and boundaries

* Both issue criteria unmet; screen reader NOT RUN; no provider selected; rates, terms, DPA, licence and processor positions unverified; the USD500 and USD 535.41 figures are history; current all-in forecast and headroom Unknown under the USD 700 ceiling expiring 2026-10-25T16:02Z; no paid execution; no closing keyword.
