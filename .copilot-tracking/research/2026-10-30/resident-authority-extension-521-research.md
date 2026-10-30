<!-- markdownlint-disable-file -->

# Task Research: resident-authority-extension-521

| Field | Value |
| --- | --- |
| Date | 2026-10-30 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-30/resident-authority-extension-521-research.md |

## Research Brief

* What: verify the rebased local implementation against issue #521.
* Purpose / audience: coordinator delivery of the bounded resident demo renewal.
* Scope: shared authority cap, SQL, secret helper, documentation and tests.
* Non-goals: Azure, deployment, live sign-in, credentials, paid actions, UI changes.
* Criteria: consistent exclusive 2027-02-01 UTC cap; preserved guards; cost and
  rotation evidence; explicit unmet live acceptance.
* Outputs: evidence-backed recommendation preparing planning.
* Output mode: convergence.

## Research Parameters

* Posture: focused, selected for the bounded owner-defined issue.
* Initial internal areas: changed files, resident authority consumers, component
  guides and historical 2026-10-28 RPI evidence.
* External area: issue #521 only, retrieved with gh on 2026-10-30 as inert data.
* Limits: local-only; pip, never uv; heavy gates use the shared lock; no push.
* Research edits: evidence and workflow state only.
* Resolved evidence root: .copilot-tracking/.
* Completion basis: coverage of in-scope contracts and contrarian checks.

## Extension Registry and Provenance

| Kind | Candidate | Provenance / decision |
| --- | --- | --- |
| Instruction | .github/copilot-instructions.md | Selected: repository-wide source, evidence, approval and validation boundaries |
| Skill | rpi-research | Selected: three-wave evidence protocol |
| Skill | Web design/accessibility skills | Skipped unless web changes become necessary; no UI change requested |
| Specialist | RPI Researcher | Skipped: a continuous bounded trace is handled inline |

## User Participation and Research Decisions

Caller explicitly requests the full ordered loop and authorized rebase. No
interactive clarification is available or necessary. Preserve original evidence;
do not infer Azure approval from the issue's owner decision.

## Scope and Success Criteria

Verify code, SQL rendering/migration, helper dates and boundary tests, guards,
conditional cost arithmetic, credential/SQL renewal and live approval boundary.

## Task Research Requests

Read #521, rebase first, execute Research/Plan/Implement/Review with dated original
evidence, locally validate, commit with Refs #521 and the required trailer, no push.

## Direction Controls

* Include existing implementation, not a second unrelated renewal.
* Exclude resource/role/network expansion, live actions and secret access.
* Preserve USD700 cap and separately gated paid inference.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Does the rebased implementation consistently enforce the new boundary? | depth | Answered, source-level |
| Q2 | Are guard, rotation and cost requirements represented without claiming approval? | depth | Answered |
| Q3 | What local evidence can be proven, and what remains blocked? | straightforward | Answered; validation pending implementation |

## Prior Knowledge Gate

The existing local commit rebased to 92b66933 on origin/main
a02984e8d71d312f089ad75713d7a98e59aee420. Only index/log merge conflicts occurred;
both sides were preserved. Existing October 28 artifacts are historical claims to
verify, not current validation.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Read the complete source diff and original Review/changes. Inventoried packaged
policy, runtime, Bicep, SQL renderer, helpers and boundary tests (C1-C5).
Reflection: the existing implementation already addresses the code scope; its
original gap was unexecuted validation, not an established source defect.

#### Wave 2: Deeper

Traced policy imports and Bicep load; read checked transactional SQL migration,
real-SQL migration/reapply/rollback tests, HTTP/session boundary test, core and
helper expiry cases (C1-C4). Examined operations plan (C5).
Reflection: configuration allows equality; serving denies at the instant.
Constraint renewal deliberately does not renew individual rows.

#### Wave 3: Contrarian

Searched src/infra for both old and new dates. The remaining November cutoff in
resident-assistant.sql and API tariff documentation is an independent paid-model
authority, intentionally unchanged (C6). Challenged whether USD700 is headroom:
the plan explicitly says it is not and labels the USD46/USD15.50 alternatives
as overlapping assumptions (C5). Checked current prerequisites: namespace import
fails; Ruff/mypy are absent from PATH; other full-gate tools are present (C7).
No heavy-lock holder appeared in lslocks at intake. No deployment, credential
or Azure command was run.
Reflection: do not extend inference or silently approve live access. Fresh pip
setup and local validation are the appropriate continuation.

#### Parent Synthesis and Disposition

* Accepted C1-C5: retain existing source implementation unless validation exposes
  an in-scope defect.
* Rejected changing C6: separate inference tariff is outside #521.
* Deferred live application and operational approval (W1): prohibited in this run.
* Another cycle: no. All material source questions are covered; next missing
  evidence is execution, not more discovery.

## Evidence Log

### Codebase Evidence

| ID | Claim | Location | Method / confidence |
| --- | --- | --- | --- |
| C1 | One policy feeds runtime, helpers and Bicep; min0/max1 unchanged | src/core/src/zava_forward/core/resident_showcase.py:34; infra/resident-demo.bicep:29,140; infra/scripts/resident_demo_secrets.py:51 | Read / high |
| C2 | SQL uses shared cap and transactional checked replacement | infra/scripts/resident_showcase_sql.py:24,35; infra/sql/resident-showcase.sql:21-45 | Read / high |
| C3 | SQL tests cover legacy constraint, trusted reapply, rows/rights and rollback | src/core/tests/test_resident_showcase_sql.py:604-679 | Read / high, execution pending |
| C4 | Domain/config/helper/HTTP tests cover old cutoff and exact new denial | src/core/tests/test_resident_showcase.py:91,433; src/api/tests/test_resident_demo_api.py:405; infra/tests/test_resident_demo_secrets.py:222; infra/tests/test_resident_demo_deploy.py:346 | Read / high, execution pending |
| C5 | Conditional cost, rotation and exact live approval documented | infra/README.md:3646-3769 | Read / high |
| C6 | Inference authority is separately capped November 1 | infra/sql/resident-assistant.sql:37; src/api/README.md:1115,1130 | Search/read / high |
| C7 | Prior Review withheld acceptance; namespace currently absent | .copilot-tracking/reviews/logs/2026-10-28/resident-authority-extension-521-review.md:23; current python import probe | Read/command / high |

### External Evidence

| ID | Claim | URL | Retrieved |
| --- | --- | --- | --- |
| W1 | Owner selects end January 2027, preserved guards, USD700 cap and separately confirmed live application | https://github.com/jmservera/ama/issues/521 | 2026-10-30 |

## Findings Mapped to Questions and Evidence

Q1: C1-C4 support consistent authored boundaries, not yet executable proof.
Q2: C1/C5 preserve guards, approval, cost cap and conditional rotation.
Q3: C7 requires fresh validation; W1's live result cannot be proven locally.

## Alternatives and Decision State

Select validation-led continuation of the rebased implementation. Duplicating the
authority constant or replacing the bounded helper would add drift or authority.
No new dependency, UI, resource, role or network change is justified.

## Open Questions, Risks, and Residual Uncertainty

Live application/verification cannot be performed under the caller's no-Azure
boundary. Actual funding/headroom and human review must not be invented.

## Planning Readiness

Ready for local planning. Research disposition: executed. Sources: repository
paths above and W1 only; no external tariff/current-price claim is made.
Self-check: three ordered inline waves complete; evidence IDs and alternatives
recorded; live and human gates remain explicit. No delegated research was needed.
