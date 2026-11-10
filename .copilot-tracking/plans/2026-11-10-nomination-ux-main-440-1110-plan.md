<!-- markdownlint-disable-file -->
# Plan: nomination and UX integration wave checkpoint (#440, 2026-11-10)

Task `440-nomination-ux-main-1110`. Research: [research](../research/2026-11-10-nomination-ux-main-440-1110-research.md). Details: [details](../details/2026-11-10-nomination-ux-main-440-1110-details.md). Critique: [critique](critiques/2026-11-10-nomination-ux-main-440-1110-plan-critique.md).

## Objective

Append one dated, scoped, draft, local-only record to the existing `docs/architecture/cutover-evidence-pack.md`, one index paragraph in `docs/reference/README.md` and one append-only entry in `docs/reference/log.md`, for the integration wave of PR 1381 and PR 1376 on `main` `65c2ab9d9`. Documentation and evidence tier only; no source change, no check re-run, no new issue.

## Phases

* [ ] Phase 1: Write the pack section: identities, scope, consumed evidence with its class, document-qualified traceability, source boundaries, findings and owners, deferred and blocked rows, recommendation and limits.
* [ ] Phase 2: Add the index paragraph and the log entry (append only, disjoint from any other record).
* [ ] Phase 3: Review the diff against the identities, the raw records and the conventions (ASCII, no em dashes, links resolve, heading anchor matches the index link), then commit and verify the witness.

## Decisions and constraints

* The record is source-qualified: the local predictions were tested before merge on trees that differ from the actual main trees only in the rubric score file; no command ran on `65c2ab9d9`, no GitHub preview or Azure observation exists.
* Classes used: local observed (Root runs on the predicted trees), historic-source-qualified, current-metadata-equivalence, Azure observed NONE, implemented-unverified, deferred, blocked, unknown.
* No approval of Draft, proposed, human or HVE items. No requirement relaxation, no extra 132 or 133 budget.
* The old CSV-learning record and the old C6 are not included and not republished; this record owns only its own dated section, index paragraph and log entry.
* Excluded: unmerged 136 and 175 Bicep, 89 aftercare parent and child 133, held 132 and contractor identities, the #1384 checker fix; #1384 and #1383 are stated as owners only.

## Amendments from the single critique (applied directly)

* A1: hosted success and mergeability are PR-head metadata only; the record says no run result exists for the exact main commit.
* A2: the #1384 diagnostic wording is attributed to Root, not reproduced here; the record does not call the whole workspace browser check green.
* A3: #1383 stays OPEN; recovery is unproven by a later overall SUCCESS alone and no closure is invented.
* A4: the 5-empty and 2-populated split is stated as not independently re-derived.
* A5: passing nomination output still shows law-store-unavailable, 503 and disconnect lines; no zero-server-error claim.
* A6: unique heading, index paragraph and log entry; the record neither includes nor republishes the old CSV-learning record; any later append-only conflict is resolved by Root preserving both entries.

## Validation (focused documentation tier)

* `git diff` read; link targets resolved by a path check; anchor generated from the heading matches the index link; trailing whitespace and non-ASCII scan of added lines; JSON validity of the state file.
* Not run, by assignment: full or `--changed` gate, runtime checks, browsers, SQL, images, models, cloud.
