---
title: "Final-candidate plan critique: synthetic-dictionary-175"
description: "Bounded offline credibility assessment for issue 175."
ms.date: "2026-10-16"
---

## Metadata

* Task ID: issue-175 / synthetic-dictionary-175.
* Critique date: 2026-10-16.
* Plan: .copilot-tracking/plans/2026-10-16/synthetic-dictionary-175-plan.md.
* Phase details: .copilot-tracking/details/2026-10-16/synthetic-dictionary-175-phase-details.md.
* Critique execution status: Complete.
* Severity summary: 1 High, 2 Medium, 0 Critical, 0 Low.

## Inputs and Criterion Boundary

* Assessed the supplied plan, phase details and .copilot-tracking/research/2026-10-16/synthetic-dictionary-175-research.md against the caller's offline, bounded-build, no-private-data, no-legacy-edit and no-setup-entra.py-edit constraints.
* Read only specific referenced source files to establish existing labels, manifests, public exemptions and test behavior: src/core/tests/test_synthetic_provenance.py; src/core/src/zava_forward/core/synthetic/scale_fixture.py; src/core/src/zava_forward/core/synthetic/sensor_backfill.py; src/agents/tests/chat_fixture.py; src/agents/evals/registry.json; docs/reference/research/retrofit-synthetic-data/provenance-register.json; and the opening portions of src/agents/evals/chat_golden.json, src/agents/evals/ai_priority_golden.json, src/core/evals/document_control_fixtures.json and src/importer/evals/document_form_fixtures.json.
* Assessed AC1 through AC4, P01-T01 through P02-T02, locked test ownership, generator-byte preservation, public-fixture exemptions, actual checker/CLI mutations, private-dependency removal, documentation and acceptance audit.
* AC2 is intentionally unmet: the three missing historical retrieval dates and provisional licence terms cannot be invented or resolved through offline implementation. A nonzero source audit and explicit unmet acceptance result are required, not critique defects.
* This is a planning assessment, not implementation, execution evidence, legal approval or a claim that all acceptance criteria are achievable in this scope.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Offline work and excluded files | Covered | No remote research, private datasets, environment/identity files, legacy edits or identity setup edits are needed by the proposed validator. |
| AC1; C1, C5-C7, C9; P01-T03 | Covered | Dictionary/register changes cover scale/fabric, sensor, generated chat, runtime content, document controls and current eval families. |
| AC2; C4, C8; P01-T01, P01-T03, P02-T02 | Covered as intentionally unmet | Null dates and provisional terms remain visible; strict audit rejects them and delivery reports AC2 unmet. |
| Public-fixture exemptions; P01-T01, P01-T02 | Partial | Existing unlabelled eval containers and the registered CSV exemption need explicit validation contracts; PC-001. |
| AC3; P01-T01, P01-T02 | Partial | Production-checker mutation intent exists, but independent scanner, label and hash failure evidence is not specified; PC-002. |
| AC4; C3; P01-T02 | Covered | Replace private-reading tests; generate small fixtures and check ignored locations without reading private content. |
| Generator-byte preservation; C5-C7; locked test ownership | Covered | Reuse existing generators and labels; existing determinism and fixture suites retain behavioral ownership. PC-001 must not be resolved by editing fixture payloads. |
| Fixture isolation; P01-T02, P02-T01 | Partial | Fresh synthetic fixtures are required, but their permitted project-local location and inherited runtime configuration are unspecified; PC-003. |
| README/index/log; P01-T03 | Covered | Canonical documentation, relevant project guides, knowledge-base index and append-only log are explicitly included. |
| P02-T01, P02-T02 | Covered as planned, not executed | Targeted tests, static checks, local CLI/API smoke, one Review and honest acceptance audit precede delivery. No implementation validation was run in this critique. |

## Verdict

* Verdict: Revise.
* The implementation direction is credible and the accepted AC2 limitation is honest. Three planner-owned clarifications are needed to prevent incompatible public-label enforcement, misleading mutation evidence and accidental use of forbidden scratch locations or existing runtime configuration. None requires a new user decision or another critique pass.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Specify narrow public-fixture label exemptions before enforcing row labels

* Related IDs: AC1, AC3, P01-T01, P01-T02; public-fixture preservation requirement.
* Evidence: The plan requires missing labels to fail and public/eval coverage. Phase details specify generated-family labels but no public eval record boundaries or exemption policy. The register explicitly exempts evidence-gap-register.csv from row labels. src/agents/evals/chat_golden.json and src/agents/evals/ai_priority_golden.json contain constructed scenarios and nested cases without is_synthetic row fields; src/core/evals/document_control_fixtures.json instead labels case records, not every nested upload object. The existing provenance test scans eval JSON for patterns without requiring per-object labels.
* Concern: A generic recursive row-label rule would reject legitimate committed public fixtures; a blanket eval exemption would silently weaken label coverage for fixtures that do carry labels. Neither outcome is authorized.
* Impact: The public CLI baseline can fail, or implementation can change public fixture bytes or bypass meaningful label checks merely to obtain a pass.
* Smallest useful change: Add an explicit public contract table to P01-T01/P01-T02: registered file or family, record collection, required label if applicable, and existing narrowly justified exemption. Preserve the CSV exemption and constructed/metadata-only eval exemptions without excluding their contents from pattern scanning. Do not add labels to existing payloads.
* Action owner: Planning parent.
* Exact resolving evidence: Revised phase details identify the exempt public families and labeled record boundaries; planned regressions require unchanged committed public fixtures to pass, missing/false labels in a label-bearing public fixture to fail, and an injected personal-data pattern inside an exempt fixture to fail through the production checker.
* Decision route: Direct planner correction. The caller already requires preservation of public-fixture exemptions and generator bytes.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Separate scanner and label rejection from manifest-integrity rejection in mutation evidence

* Related IDs: AC3, P01-T01, P01-T02, P02-T01.
* Evidence: Phase details require manifest hash checks and mutated positive fixtures, but do not state how mutations preserve unrelated validity or which diagnostic proves each rejection. src/core/src/zava_forward/core/synthetic/scale_fixture.py writes per-file hashes; src/agents/tests/chat_fixture.py writes an aggregate hash rather than file_sha256. The existing provenance test checks only a local scan helper against standalone strings.
* Concern: Mutating a hash-bound payload without updating its legitimate manifest hashes can yield nonzero status entirely because of integrity failure. That does not demonstrate that production scanning or label enforcement ran. A similarly combined source audit could fail for the already-known AC2 gap and mask an inert data scanner.
* Impact: AC3 could be reported met while the real checker accepts prohibited values or labels whenever integrity and source metadata are otherwise valid.
* Smallest useful change: Specify an isolated mutation matrix for email, UK telephone, NI number, postcode, missing/false labels and invalid manifest label/integrity. Start each case from a passing tiny fixture. For scanner/row-label cases, refresh applicable hashes without altering the generators; assert the intended production-checker reason and nonzero real CLI status with source audit disabled or independently valid. Keep stale-hash and source-readiness failures as separate cases. Include a clean CLI zero-status control and sanitized diagnostic assertions.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T02/P02-T01 require these independent tests in the existing permitted core test module and at most one agents module. The matrix distinguishes clean, pattern, label, integrity and source-audit outcomes and covers all nine generated chat payloads through the same checker.
* Decision route: Direct planner correction. No additional implementation scope or user decision is needed.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Bind generated fixtures and smoke runtime state to permitted project-local scratch paths

* Related IDs: AC4, P01-T02, P02-T01; no-private-dependencies and file-operation constraints.
* Evidence: The plan repeatedly calls fixtures and snapshots temporary, and phase details require fresh synthetic API data, but neither specifies the scratch root or how ZF_DATA is isolated from inherited settings. scale_fixture.py and chat_fixture.py otherwise offer per-user output defaults. The current execution constraints prohibit /tmp, /var/tmp and other temporary-directory file operations.
* Concern: Default temporary-directory helpers or generator defaults can write outside the permitted project location. Merely constructing a fresh API seed does not establish that all runtime state uses it rather than an inherited private ZF_DATA location.
* Impact: The implementation or validation can violate the file-operation boundary or fail to establish a private-independent smoke result despite using synthetic inputs.
* Smallest useful change: Require disposable scratch directories beneath the working project with explicit generator output arguments and cleanup. Scope ZF_DATA and all applicable API/runtime storage settings to those fresh paths before startup; do not load .env, .vscode/properwarm.json or existing user data. Use project-rooted scratch allocation rather than default system temporary directories.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T02/P02-T01 state the project-local scratch convention, explicit output/configuration overrides and cleanup. Planned validation records the isolated synthetic paths and verifies a responsive local API without remote/model calls or private inputs.
* Decision route: Direct planner correction. Existing constraints already select the permitted behavior.

## Strengths and Residual Risk

* AC2 is not disguised as success: three source entries remain provisional, the strict audit is expected to return nonzero, and the PR must disclose the unmet criterion.
* Sensor source_type, chat boolean labels and scale manifest inheritance follow existing generator contracts rather than changing deterministic payloads.
* The fictional TE[0-8] 1ST postcode exception is field-specific, not a blanket exemption for generated content.
* Real map anchors and live user content remain outside public scans and synthetic guarantees. Pattern rejection is a bounded detector, not proof that a person is fictional or that data is universally free of personal information.
* Full-stock materialization, operational approvals and actual chat/DPO approval remain explicitly out of scope. The exercise owner's role does not create those approvals.
* One post-implementation Review and measured AC1/3/4 evidence remain necessary. Passing implementation checks will not resolve AC2.

## Questions or Blocking Evidence Gaps

* No user question is required to correct PC-001 through PC-003.
* Missing historical source evidence remains an accepted AC2 blocker, not a blocker to this bounded assessment. Do not fabricate it, fetch it remotely or demand its resolution before scoped implementation.

## Limitations

* Assessment used only the supplied artifacts and the specific referenced sources listed above. No remote sources, private datasets, excluded configuration files, unreferenced repository documentation or legacy implementation files were read.
* Source excerpts establish concrete label/manifest differences, not an exhaustive fresh inventory of every eval payload or generator branch.
* No implementation, tests, API startup, build, commit, push or PR operation was performed. Read-only Git status/branch inspection established the existing topic branch and pre-existing untracked planning artifacts; those artifacts were not changed.
* The unavailable rg command produced no search results; direct reads of the specific referenced public fixture files supplied the relevant evidence instead.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the public label/exemption contract, isolated mutation matrix and project-local runtime/fixture isolation requirements to the existing plan/details. Resolve the three findings directly, without another critique pass.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/synthetic-dictionary-175-plan.md](.copilot-tracking/plans/2026-10-16/synthetic-dictionary-175-plan.md) | Assessed final-candidate plan; unchanged. |
| [.copilot-tracking/details/2026-10-16/synthetic-dictionary-175-phase-details.md](.copilot-tracking/details/2026-10-16/synthetic-dictionary-175-phase-details.md) | Assessed phase details; unchanged. |
| [.copilot-tracking/research/2026-10-16/synthetic-dictionary-175-research.md](.copilot-tracking/research/2026-10-16/synthetic-dictionary-175-research.md) | Supplied evidence and accepted AC2 limitation; unchanged. |
| [.copilot-tracking/plans/2026-10-16/synthetic-dictionary-175-critique.md](.copilot-tracking/plans/2026-10-16/synthetic-dictionary-175-critique.md) | Complete actionable finding set. |

## Next Steps

Planning parent: directly resolve PC-001, PC-002 and PC-003, preserving AC2 as unmet with a nonzero source audit. No user action is required. This critique stops here; it does not implement, delegate or invoke another RPI stage.
