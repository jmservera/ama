---
title: Resident PRD draft quality evidence and disposition
date: 2026-10-23
status: draft-blocked
---

## Review result

One `hve-core-all:prd-quality-reviewer` invocation returned both contracts:

* `reviewer-findings.yaml`: `PRD_STANDARD_FINDINGS_V1`, assessment
  `requirements-quality-PRD-2026-AMA48-001-20261023T172745Z`.
* `reviewer-report.yaml`: `PRD_QUALITY_REPORT_V1`, report
  `PRD-2026-AMA48-001-quality-20261023T172745Z`.

The persisted YAML preserves the returned values; flow-list formatting does
not change their meaning. It is not a new author-issued passing report.
As returned: **RISK**, two HIGH risks and three MEDIUM cautions,
overall **FAIL**, Validate **BLOCKED**, Finalize **NOT_EVALUATED**.
No waivers/signatures/approval have been supplied. No authoring/ADR/company
role agents were launched; this one read-only quality reviewer is the
required lifecycle check.

## Evidence limitation, not concealed as approval

The reviewer could read the amendment/patch but could not execute the
in-memory validator or independently access the pinned base. It reported
seeing a v0.17.0 checkout rather than v0.18.0. The author never used that
checkout as source: pinned `git show` bytes and exact candidate hashes are
verified in `validation.json`. The review's counts/category/goal scores are
therefore declared/inspection-based, not independent exact-byte coverage.
Its line locations are approximate and should not be used as validated
candidate line references.

The reviewer was provided the pre-final-whitespace candidate hash
`cae0e01ebe07e5a561acea47ef427343fcc3c27e178246e39807e206afb3e8b4`
and patch hash
`6cd106407a02cbb24be2e8dcb51de36a6c2b0389bfa159ff2fbdf9cf3e42d57e`.
After review the author removed one newly introduced duplicate blank line
after the OQ table, added exact original context to context-free replacement
hunks for portable patch application and corrected derived hunk counts/offsets. No requirement,
criterion, numerical assumption, authority, allocation or approval changed.
Final exact hashes are in `validation.json`; these are not represented as
fresh independently reviewed bytes.

The payload files are retained as returned review evidence, not a signed
strictly certified schema release. YAML parsing/contract discriminants and
counts may be checked statically; independent source access and feasibility
remain unverified by this reviewer. Do not turn its “all categories present”
or historical GOAL-001 to GOAL-004 PASS values into a current feasibility or
upstream approval claim.

## Findings and author disposition

| Reviewer ID | Type | Disposition |
| --- | --- | --- |
| req-qual-001 | Review capability limitation / HIGH | Exact base/hunks/candidate/IDs are author-verified read-only in memory, not reviewer-verified. Parent needs fresh integrated-byte independent review for any gate exit; no new agent invocation is used to mask this limit. |
| req-qual-002 | Inherited unsigned upstream / HIGH | Agreed. BRD Define remains BLOCKED/Govern NOT_EVALUATED; PRD unsigned draft delivery and ADR comparison are allowed but not lifecycle approval. |
| req-qual-003 | New GOAL-005 SMART/feasibility / MEDIUM | Retain deferred status. Six-script target and proposed bounded workload are concrete assumptions, but date/capacity acceptance and feasibility are not invented. OQ-031 carries this gap; original T0 and historical four goals remain unchanged. |
| req-qual-004 | Upstream FR-044/AC-084 contradiction / MEDIUM | Surfaced to parent. Per-message review/default OFF retained; reconciliation plus OD-53/policy/release evidence required before exception activation. An ADR cannot overrule requirements. |
| req-qual-005 | Review constraint-access limit / MEDIUM | Author separately read pinned CON-001 to CON-009 and mechanically proved every original definition byte-preserved. Rows name categories, imposing sources and authority/scope boundaries; no new constraint is invented. This is not a substitute for the reviewer's independent inspection. |

Author constraint check: CON-001 non-production data/authority; CON-002
authoritative systems; CON-003 human decision rights; CON-004 production
appraisal; CON-005 unverified estate; CON-006 independent hazard response;
CON-007 approval separation; CON-008 scenario reporting; CON-009 actual
Azure/SQL/real-AI accepted-build direction. Each remains imposed upstream or
owner scope, not a newly selected technology/quality target. CON-005 explicitly
distinguishes the document-store fallback as a design choice. No inherited
constraint classification rewrite was made.

## Static findings and Markdown limitations

The exact candidate passes patch syntax, in-memory exact hunk reconstruction,
original definition preservation, unique new allocation, all FR-to-AC links
matching requirement rows and all FR-to-goal definition checks. Every new
criterion remains Not run. Formula recomputation matches the supplied
low/base/high model without testing adoption or benefit.

One inherited goal-matrix overlink is also preserved: PRD FR-059's definition
links only GOAL-004, while its existing matrix range also links GOAL-002.
All new rows match exactly. Structural whole-document linkage remains
71/71, but this is not a claim that every inherited reciprocal link is exact.
The validator exposes the difference rather than repairing unrelated scope.

Static Markdown checking uses the already present upstream
`markdownlint-cli@0.45.0`, no install/cache writes. The recorded profile allows
long table rows, H2 top-level headings and existing `br` elements.
The pinned base has three MD056 warnings: PRD AC-104/105/106 are two-cell
definitions in a five-cell staff requirements table. They remain unchanged
at candidate lines 828 to 830; this task does not “fix” inherited unrelated
rows. The final candidate has **no new Markdown diagnostics**, but the full
candidate does not pass that unmodified profile. The package Markdown
documents pass it. The separately labelled package inheritance-tolerant profile
with MD056 disabled passes, but is not a default-rules or repaired-document claim.

This does not convert an inherited malformed table into valid product
acceptance. Parent may scope a separate editorial repair if required by its
integration gate. Keep the exact baseline diagnostic comparison.

## Decision

Deliver the **unsigned draft amendment and ADR handoff**, stopping at the
requested boundary. Validate remains BLOCKED; Finalize NOT_EVALUATED.
Upstream authority, GOAL-005 acceptance/feasibility, OD-52 to OD-55 and the
FR-044/AC-084 conflict remain explicit. No application suites, protected gate,
implementation, real resident service, deployment, paid call or signoff
was performed. Parent integrates through isolated native RPI and commissions
ADR next, without delaying independent staff landing/auth absent evidence.
