---
title: Stock fabric link 168 plan critique
description: Single independent assessment of the final candidate implementation plan
ms.date: 2026-10-15
---

## Metadata

* Task ID: 168 / stock-fabric-link-168
* Critique date: 2026-10-15
* Plan: .copilot-tracking/plans/2026-10-15/stock-fabric-link-168-plan.md
* Phase details: .copilot-tracking/details/2026-10-15/stock-fabric-link-168-phase-details.md
* Critique execution status: Complete
* Assessment count: One. No second critique was performed or is requested.
* Workspace: /home/azureuser/source/ama-wt/issue-168
* Branch: feat/src-stock-fabric-link-168
* Source baseline: a48d502c94125e7787250f90ea66abfb46a758d9

## Inputs and Criterion Boundary

* Read the supplied plan, phase details and research in full. Inspected bounded
  source evidence identified by research C1-C9: the retained fabric, builder,
  EPC and manifest modules; core output/provenance helpers; generated-dataset
  tests; project configuration and commands; SN-01 and the existing synthesis.
* Read project context in docs/case_study_48_original.md,
  docs/case_study_48_addendum.md (purpose and approved exercise baseline),
  docs/reference/README.md and docs/reference/memory.md. Inspected the layout
  decisions in docs/adrs/0006-src-layout-and-cutover.md and the migration
  placement context in docs/architecture/mvp-to-src-parity-matrix.md.
* Read issue #168 through gh: OPEN, all three acceptance criteria unchecked.
  They require case resolution or an explicit unlinked result, reproducible
  synthetic-labelled attributes, and assumption-labelled distributions.
  No open PR was returned for the named branch.
* Caller requirements govern: full RPI delivery; all new code/tests in src;
  reuse the merged generator; private data through ZF_DATA; pip only; no
  mvp, .env, .vscode or issue-cache edits; local suites, ruff, mypy, application
  smoke and a Docker attempt before CI; PR Refs #168; original acceptance
  remains unchecked where unavailable evidence or owner decisions are needed.
* The locked test allocation is one new semantic module,
  src/core/tests/test_stock_fabric.py, extensions to
  src/core/tests/test_generated_dataset.py, no test removals, and at most one
  additional test in an existing cross-project file if genuinely necessary.
* Boundary: credibility of the bounded migration and fictional-evidence slice,
  not implementation acceptance. Private geography, actual 980-case private
  output, unit identity, reconciliation and owner ratification were neither
  supplied nor inferred. No private corpus was inspected.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| ADR 0006; C1/C2; P01-T01 | Partial | Core destination and move-not-copy are sound, but support imports-only scope conflicts with required behavioral changes; PC-001. |
| Issue #168 case resolution; C3/C4; P01-T01 | Partial | Counted identities and explicit reasons are planned; report vocabulary and exact invalid-input behavior need closure; PC-002/PC-004. |
| Shared geography versus unit identity | Partial | Correct non-unit intent and owner deferral; legacy note/counter interpretation can still misstate it; PC-002. |
| Issue #168 seeded, synthetic-labelled fabric; P01-T02 | Covered | Seed/version preservation, golden payload, changed-seed variation and per-row labels are planned. Golden evidence must cover representative draw branches. |
| Issue #168 assumption distributions; P02-T01 | Covered | Declared weights and summary labels are explicit; no company-fact claim is authorized. |
| Exact 60,000/980 evidence; C5; P01-T02 | Partial | Separate scale and builder tests do not establish one connected fixture; PC-003. |
| Provenance; C6/C9; P01-T01/P01-T02 | Partial | Moved source fingerprinting is required, but dependency and regression evidence is underspecified; PC-005. |
| ZF_DATA and output safety; C6/C8; P01-T01/P01-T02 | Covered | Input-first validation, nonempty/repository/symlink refusal and no raw stdout are explicit requirements, not properties already supplied by the helpers. |
| SQLite restart; P01-T02 | Partial | Existing restart assertions concern queues, not new stock metadata; PC-006. |
| Typed code/tests; P02-T02 | Partial | Existing generated integration test is exempt from lint/type enforcement; PC-007. |
| SN-01; original acceptance; P02-T01/P02-T03 | Covered | Bounded iteration authorization is not full inventory approval or private-output acceptance. Keep original checkboxes unchecked and use Refs #168. |
| Local suites/app/Docker then CI; P02-T02/P02-T03 | Covered | Existing project commands and CI provide a credible path; invocation, failure, skip and remote check results must be recorded separately. |
| Full RPI and locked tests; P02-T03 | Covered | One implementation review is planned, with persistent artifacts and no test removal. Revisions below fit existing ownership without another critique. |

## Verdict

* Verdict: Revise
* Severity summary: Critical 0; High 3; Medium 4; Low 0.
* Rationale: The selected approach is credible, but scope contradictions and
  evidence gaps could yield either non-src behavior changes or overstated
  linkage/scale validation. Seven directly applicable planner corrections
  resolve the concerns without inventing private data or deciding unit identity.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Imports-only support wiring cannot deliver the promised builder behavior

* Related IDs: ADR 0006; C1/C3/C4; P01-T01.
* Evidence: The plan limits support changes to migration import/provenance
  wiring. Phase details explicitly say to update existing consumers' imports
  only. However,
  support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py:277-294
  uses a last-row-wins stock dictionary, enriches before producing link_report,
  and never attaches a per-case resolution. Import replacement alone cannot
  change those operations.
* Concern: The plan simultaneously requires unique-register-only enrichment,
  per-case metadata and no new behavior outside src, without assigning a
  permissible implementation seam.
* Impact: Implementation must violate the scope promise or leave the key
  ambiguity fix incomplete.
* Smallest useful change: Assign validation, resolution and case-enrichment
  assembly to the new core module. Explicitly permit minimal support call-site
  replacement invoking that core operation, in addition to import/provenance
  wiring. Keep EPC generation in its retained consumer; pass only validated
  unique row selections. Do not move the entire builder or copy its algorithm.
* Action owner: Planning parent, then implementer.
* Exact resolving evidence: Revised P01-T01 names the core-owned operation and
  bounded call-site substitutions. Implementation diff shows no new resolution
  algorithm in support; existing generated tests demonstrate ambiguous rows
  receive no fabricated stock fabric/EPC.
* Decision route: Direct planner correction. Current user direction already
  establishes src-only new behavior; no significant/divergent owner decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Preserving the legacy report without a semantic migration retains a false unit claim

* Related IDs: Issue #168 first acceptance criterion; C3/C4; P01-T01/P01-T02.
* Evidence: The retained fabric module's link_report describes resolution to
  exactly one stock home, returns distinct_stock_homes and
  stock_homes_shared_by_cases, and states that distinct homes are fewer than
  cases because flats share anchors. The builder's stock_link_kind instead
  explicitly says geography row, not unique stock-unit linkage. Phase details
  require preserving legacy counters and adding warnings, but do not explicitly
  correct the inherited note or specify how consumers distinguish these facts.
* Concern: A single matching register row establishes a source-reference match,
  not one dwelling. Likewise, multiple cases sharing a reference are not proof
  of shared dwelling identity. New warnings must not coexist with an
  authoritative-looking contradictory report.
* Impact: Downstream projection/sensor consumers can interpret a geography
  count or case-attached fabric/EPC assumption as verified unit evidence.
* Smallest useful change: Specify per-case reference status and non-unit scope;
  retain legacy numeric keys only with explicit anchor-count definitions.
  Replace the false legacy note, distinguish unique-register-match from
  shared-by-cases, and label attached fabric/EPC as source-anchor assumptions.
  Preserve legacy home.built/type and all consent/history fields unchanged.
* Action owner: Planning parent, then implementer.
* Exact resolving evidence: Tests for two distinct cases sharing one unique
  register row assert both reference matches, one distinct anchor, one shared
  anchor, explicit non-unit scope and no contradictory home-count explanation.
  Another test proves duplicate register rows are ambiguous instead. Generated
  integration assertions verify these labels survive case attachment.
* Decision route: Direct planner correction. Creating or asserting unit-level
  identity would require a significant owner decision and remains out of scope.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Independent 60,000-row and 980-case tests do not prove the stated linked-scale slice

* Related IDs: Research brief/C5; local acceptance; P01-T02.
* Evidence: Phase details prescribe a 60,000-row fictional fabric test and an
  extension of the existing retained 980-case builder test.
  src/core/tests/test_generated_dataset.py:24-44 supplies 6,000 register rows,
  not 60,000. No planned assertion requires the builder's 980 resolutions to
  reference the exact register whose 60,000 fabric rows were verified.
* Concern: Both independent tests can pass while full-scale register linkage,
  enrichment or summary reconciliation fails.
* Impact: The delivery could report exact 60k/980 evidence without having
  exercised the connection requested by issue #168.
* Smallest useful change: Add one connected fictional run within the locked
  existing generated test owner, using a builder-compatible 60,000-row register.
  Reuse that exact register for fabric and case resolution; retain smaller
  semantic cases in the one new core test module.
* Action owner: Planning parent, then implementer.
* Exact resolving evidence: One recorded test/run establishes 60,000 unique
  fictional register IDs and fabric rows; 980 unique retained-builder case IDs;
  exactly one resolution per case; linked plus explicitly unlinked equals 980;
  every linked anchor and attached fabric comes from that same register; and
  each categorical distribution sums to 60,000. Record seed/date/revision.
  Do not assert the private historical 825-anchor count for fictional data.
* Decision route: Direct planner correction; no owner decision or private
  register regeneration is needed.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Identity validation lacks an explicit bulk-generation and CLI contract

* Related IDs: C3; P01-T01/P01-T02; input-first output safety.
* Evidence: The plan rejects invalid/duplicate case IDs and ambiguous case
  references, but only generally mentions invalid stock identities. The
  retained fabric_rows simply maps fabric across every row; empty or duplicate
  synthetic_home_id values can therefore produce repeated/invalid output
  identities even if link_report correctly marks case references ambiguous.
* Concern: Resolver ambiguity handling and permission to generate a valid stock
  fabric snapshot are different policies. The plan does not distinguish them
  or define identifier type/whitespace behavior.
* Impact: A standalone CLI can emit a nominally successful labelled snapshot
  with unusable identities, or normalization can silently change stable IDs.
* Smallest useful change: Define accepted identity types and blank handling;
  preserve valid IDs verbatim and prohibit coercion/fuzzy repair. Explicitly
  distinguish diagnostic resolution of malformed registers from bulk fabric
  generation: reject invalid/nonunique snapshot IDs before output creation,
  while the diagnostic resolver can report ambiguous references.
* Action owner: Planning parent, then implementer.
* Exact resolving evidence: Locked core tests cover absent, empty,
  whitespace-only, non-string and duplicate identities; valid opaque IDs remain
  unchanged. CLI invalid-register/case tests assert nonzero exit, no success
  summary and no created snapshot. A duplicate-register resolver test still
  produces explicit ambiguity without choosing a row.
* Decision route: Direct planner correction under the existing safety and
  stable-identifier requirements, not an owner mapping decision.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Revision shape and determinism tests alone cannot verify migration provenance

* Related IDs: C6/C9; P01-T01/P01-T02.
* Evidence: zf_manifest.generator_revision hashes only support-folder Python
  files and returns 16 hexadecimal digits. Core provenance.source_revision
  fingerprints explicitly supplied sources and returns 64 digits with framed
  hashing. Existing generated tests assert the legacy 16-digit shape. The plan
  correctly requires adding the moved dependency, but names no dependency
  closure, revision-format boundary or change-sensitivity regression.
* Concern: A missed core source can leave builder/EPC provenance unchanged
  when fabric behavior changes; a deliberate format change can also break
  existing consumers/tests. Byte equality on unchanged sources proves neither.
* Impact: Generated snapshots can have incomplete reproducibility metadata or
  migration-induced compatibility failures.
* Smallest useful change: State the revision inputs for the installed core CLI
  and retained support manifests, including core helpers that affect output.
  Declare whether legacy support revision shape is retained or intentionally
  migrated, and update only directly affected assertions/documentation.
* Action owner: Planning parent, then implementer.
* Exact resolving evidence: Tests in the locked owners demonstrate a changed
  moved-fabric dependency changes builder/EPC revisions, identical source
  bytes under another root do not, and declared payload hashes match bytes.
  A pre-move golden payload records unchanged seeded attribute values
  independently of intentionally changed metadata, covering A/B/C locality
  and mapped versus fallback dwelling draws.
* Decision route: Direct planner correction; revision metadata need not remain
  numerically identical after a source move.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Existing restart coverage does not assert persistence of the new linkage evidence

* Related IDs: Local 980-case acceptance; P01-T02/P02-T02.
* Evidence: src/core/tests/test_generated_dataset.py:257-273 opens SQLite,
  opens another store while the first remains open, and compares visits,
  procurement and as_of. It does not compare stock anchors, per-case
  resolution, stock fabric/EPC or top-level link summary.
* Concern: Invoking the existing test cannot substantiate the new linkage
  metadata's persistence, and concurrent reopening is weaker evidence than a
  closed-store restart.
* Impact: Metadata loss or mutation across persistence can escape the claimed
  SQLite restart evidence.
* Smallest useful change: Extend that existing test, without schema changes or
  another test module, to capture the relevant metadata, close the first store,
  then reopen against the existing database and compare all 980 cases.
* Action owner: Planning parent, then implementer.
* Exact resolving evidence: Exact per-case equality of anchor, resolution and
  present fabric/EPC fields before/after a closed-store reopen; explicit
  accounting for any top-level report retained or intentionally seed-only.
  History, resident consent and approval-state assertions remain intact.
* Decision route: Direct planner correction. No new runtime/schema requirement
  or SQL Server acceptance claim is implied.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Planned integration additions inherit existing lint/type exemptions

* Related IDs: Non-functional typed code/tests requirement; locked test
  ownership; P01-T02/P02-T02.
* Evidence: src/core/pyproject.toml excludes test_generated_dataset.py from
  formatting, ignores multiple lint rules for it, and sets ignore_errors for
  both module spellings. The plan requires typed new module/tests with no
  exemptions, but relies only on the ordinary project ruff/mypy commands.
* Concern: New assertions/helpers in this exempt file will not receive the
  advertised enforcement even when all normal commands pass.
* Impact: A clean validation table can misrepresent the quality boundary for
  the new test code.
* Smallest useful change: Keep semantic logic and typed helpers in the new,
  non-exempt stock test owner; bound integration edits to the existing file.
  Add explicit exemption-free checks for changed integration test code, or
  bring just that file under enforcement if feasible without unrelated cleanup.
  Do not widen exemptions or create a second semantic test module.
* Action owner: Planning parent, then implementer.
* Exact resolving evidence: Recorded commands/configuration show new module
  and tests are not ignored; any new integration helper/assertion path has
  explicit lint/type evidence rather than only a passing exempt suite.
  Existing unrelated migration debt is separately identified, not silently fixed.
* Decision route: Direct planner correction; no significant/divergent owner
  decision is needed.

## Strengths and Residual Risk

* Move-not-copy reuse, fixed seeded draw lineage and no compatibility shim
  preserve the merged generator rather than introduce another stock lineage.
* Explicit ZF_DATA destinations, nonempty refusal, repository/symlink
  containment, input-first validation and payload hashes are strong requirements.
  They still need implementation: output_dir only chooses a default and
  prepare_output only rejects a final symlink/nonempty folder. Resolve ancestor
  paths and test repository aliases, including a symlinked parent and invocation
  from a different working directory; do not assume the helpers enforce them.
* The original issue acceptance must remain unchecked where evidence is absent.
  Synthetic fixture tests can be reported as local slice evidence, never as
  validation of the actual retained private stock/case outputs.
* Owner follow-ups correctly retain private register regeneration/deferral,
  mapping, unit-level identity and home-field reconciliation. These are not
  silently approved by proceeding with the bounded implementation.
* Existing CI can supply image and SQL Server contract evidence, not live
  Azure/model/human acceptance. Local attempts and eventual CI outcomes must be
  distinguished; a pending or skipped job is not a passed check.
* Full RPI artifacts, privacy-safe commit identity, topic-only push, Refs #168
  and no merge are credible delivery boundaries.

## Questions or Blocking Evidence Gaps

* No user response is required to apply PC-001 through PC-007.
* Private corpus availability and owner decisions remain explicit follow-ups,
  not blockers to this fictional-evidence slice. Completing those acceptance
  claims would require new evidence/authority and is not recommended here.

## Limitations

* This was one read-only assessment of planning credibility, not a code review
  or test execution. No implementation, dependency install, application run,
  Docker build, private-data access or CI execution was performed.
* Historical PR 246 and merged M1-M6 claims were assessed through supplied
  research and present source/README evidence, not a fresh audit of every PR.
* The plan, phase details, research, session state and other repository files
  remain unchanged. Only this requested critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Reconcile the core-owned implementation seam and
  minimal support call-site scope, then apply the remaining six findings to the
  same plan/details before implementation.
* User response required: No for these corrections. Do not seek or infer
  approval of deferred private-data/unit-identity decisions.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/stock-fabric-link-168-plan.md](.copilot-tracking/plans/2026-10-15/stock-fabric-link-168-plan.md) | Assessed final candidate plan. |
| [.copilot-tracking/details/2026-10-15/stock-fabric-link-168-phase-details.md](.copilot-tracking/details/2026-10-15/stock-fabric-link-168-phase-details.md) | Assessed task and evidence details. |
| [.copilot-tracking/research/2026-10-15/stock-fabric-link-168-research.md](.copilot-tracking/research/2026-10-15/stock-fabric-link-168-research.md) | Supplied bounded research. |
| [.copilot-tracking/plans/2026-10-15/stock-fabric-link-168-critique.md](.copilot-tracking/plans/2026-10-15/stock-fabric-link-168-critique.md) | Complete single critique and resolving evidence. |

## Next Steps

The active planning parent should apply the seven direct corrections, record
their dispositions and finalize the plan without another critique. Continue
the authorized RPI loop only after that gate. No user action is required for
these corrections. This critique task stops here; it does not implement or
disposition the findings.
