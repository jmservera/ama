# Review: remove the obsolete synthetic proof case (issue 360)

Date: 2026-10-25. Review executed once, by an independent code-review agent, after implementation. Outcome: PASS-WITH-FINDINGS. Assessed boundary: the executed guarded script, its outputs, the external report, the changes file and the two documentation edits (uncommitted tree before commit).

## Conclusions
The live operation matches the critique amendments and owner constraints: fixed-id, rowversion and body-hash selection; zero references scanned across audit, recommendations, meta, staff, chat tables and other cases; digests of the other 980 case ids and bodies equal before and after; single-row delete with rowcount assertions; chained `case_removed` audit entry on the captured head; head and `meta.seq` updates asserted. Result: 981 to 980 cases, 444 to 443 open, audit 17 to 18 with the chain intact. The dry run script differed from the live script only in its final line. Overclaims were not found (owner browser view, cost and authority are caveated).

## Findings and dispositions
| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Medium | Plan and changes stated 12:44Z and 12:45Z for the critique; file times show about 12:32Z, and 12:45Z is the commit | Fixed: times corrected to about 12:32Z, with the error disclosed in the plan |
| 2 | Low | Amendment 5 only partly asserted (chain verifies and count plus 1, no per-row comparison of the earlier 17 rows or an explicit `prev` check); amendment 4 HTTP verification limited to 401 probes, map exclusion is an in-container projection | Accepted as a limitation: report now says the earlier-rows statement is inferred from the verified chain; map exclusion is described as a projection, not an HTTP or UI check |
| 3 | Low | "Restarted at 12:45:28Z" was the pre-restart snapshot time | Fixed: restart window stated as between 12:45:28Z and 12:46:58Z |
| 4 | Low | Runbook bullet said `cases` is the only table that holds a case | Fixed: reworded to case content |

## Residual items (routed to later work, not repeated in this task)
* A reviewed helper with cache eviction for external deletes would remove the restart requirement.
* The owner browser check of the map after the reload remains open.

## Correction record (documentation only, appended after the original review, which is unchanged above)
Trigger: coordinator comment 6398225740. The original finding 2 said the earlier audit rows were not compared per row; the changes artifact, knowledge-base log and plan amendment 5 stated preservation or full application more strongly. Reconciled: wording now says prior-row preservation is inferred from chain integrity and the append-only ledger, amendment 5 is recorded as partly applied, and the superseded draft details are marked as not a runbook. No runtime validation was run or backfilled; no Azure, SQL or OSM request was made.
Current verdict for this documentation set: PASS-WITH-FINDINGS stands. Remaining limits: no direct audit-row comparison, owner browser view of the map unverified, no whole-issue acceptance, no provider approval. The external live report `/tmp/ama-360-remove-example-live.md` already carries the inferred-from-chain qualification.

### Review of this correction (one independent code-review run, diff and files only)
Outcome: PASS-WITH-FINDINGS. All listed checks passed (inferred-not-proven wording, amendment 5 partly applied, superseded details banner, original review unchanged, log additions only with 0 deletions against main, README and log keep both PR 458 and PR 459 content, no overclaims, phase order disclosed). Findings: (1) low, the earlier log entry still carries the stronger wording; left as is because the log is append-only and the later entry corrects it. (2) low, the banner time placeholder; fixed to about 14:25Z. The reviewer did not check external reports or the live database.

## Ledger-history correction cycle (2026-10-28, PR 459)

Trigger: Copilot review threads
[research schema](https://github.com/jmservera/ama/pull/459#discussion_r4398540360)
and [runbook retention boundary](https://github.com/jmservera/ama/pull/459#discussion_r4398540422).
This updates the existing review record, not a new full RPI loop or a repeat
of the original post-implementation Review. Original outcomes and finding 4's
inadequate "case content" disposition above are preserved, not reclassified.

Correction: the live `cases` table is an updatable ledger table. A `DELETE`
removes the current row but retains its old body in system-managed ledger
history. The `audit` ledger separately records `case_removed`; its
`INSTEAD OF UPDATE, DELETE` trigger is a non-ledger alternative, not extra
live-ledger protection. Evidence: [ledger-safe research E3-E6](../../research/2026-10-24/ledger-safe-migration-360-research.md#evidence)
and `MssqlStore._create_schema_serialized` in
`src/core/src/zava_forward/core/mssqlstore.py`.

Dispositions: the runbook now explicitly describes active-case removal and
history retention, not erasure or sole-table case-content storage. The original
research is unchanged except for its dated correction note. Related plan and
changes evidence qualify current-row counts and the non-history reference
scan; the knowledge-base index and append-only log carry the same boundary.
The superseded draft details remain historical, not a current runbook.

Validation boundary: documentation/link and diff checks only for the correction;
no live schema/history query, SQL mutation, Azure/OSM request, restart or browser
check was performed. No erasure, fresh live verification, whole-issue acceptance
or new conformant Review outcome is claimed. Original residual items and
publication/human/hosted gates remain separate.

Local correction checks: `git diff --check` passed; all ten added local
Markdown links and heading anchors resolved; original tracking text and earlier
log entries remained byte-for-byte prefixes of the corrected files. A wider
index-link probe found a pre-existing locally absent presentation delivery
file; it is unrelated and unchanged. Final committed-candidate publication
checks and thread dispositions are not implied by these documentation checks.
