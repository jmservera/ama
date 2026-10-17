---
title: Issue 97 form schema and candidate staging research
description: Focused evidence and ordered research for FR-038 and FR-039
ms.date: 2026-10-17
---

## Research brief

Implement only #97: versioned field schemas with recorded source authority and evidence, and candidate staging retaining parser/OCR lineage. Audience: implementer and PR reviewer. Output mode: convergence. Posture: focused, from caller's exact issue boundary. No private datasets, live paid AI/Azure/SQL, new services, UI, automatic field acceptance, financial submission, or #98 workflow.

## Opening state and prior knowledge gate

Read original case study, reference index and memory. Inspect the addendum and approved PRD relevant provisions before implementation. Clean branch `feat/form-schema-staging-97` is at latest fetched `origin/main`, `abaca7881e2a4a77eacf865fe235d4af9196643f`; no open branch PR. Existing approval, domain/version and evidence mechanisms must be verified rather than recreated.

## Extension registry

| Extension | Disposition and scoped authority |
| --- | --- |
| Repository instructions | Selected; src-only code, external tests, private-data prohibition, component guides |
| rpi-research | Selected; ordered wider/deeper/contrarian evidence |
| github-backlog-manager agent | Selected by explicit caller request; bounded scope/refinement review, at most one refinement, no remote mutation |
| Web skills | Skipped; backend/schema slice only |

## Questions and direction controls

* Q1: What exactly do #97, parent #96, related #98 and FR-038/039 require?
* Q2: Which core/API/SQL schema, version, authority and evidence helpers already exist?
* Q3: Is the parent's AI task registry prerequisite present, and does offline staging require it?
* Q4: Can source authority and approval be recorded without manufacturing approval or implementing #98?
* Caller explicitly authorizes one complete automatic loop and stop after final pushed PR and Review. No routine phase prompts are needed.

## Cycle 1

### Wider

Exact hierarchy and PRD reviewed. FR-038/039 cover a versioned schema contract and candidate provenance; FR-040 onward belongs to #98. The addendum records owner acceptance of PRD v0.12.0 for exercise implementation planning on 2026-10-10. Current local PRD frontmatter `in-review` is a separate status fact and does not negate that dated acceptance or create a new approval prerequisite. Neither planning acceptance nor exercise assumptions approve a particular form version.

Reflection: implement the bounded engineering contract without claiming actual approved templates, live extraction or full AC-046/047/053 acceptance.

### Deeper

Verified Store document uploads already retain `content_sha256`, `version`, scan state and case membership. SqlStore persists case bodies with row versions and audit atomically, and shared checked documents through `DOCS` / `_proc_write`; MssqlStore inherits these hooks. Existing `ai_registry.digest` provides stable structured hashing; `ledger` provides audit hashing, not canonical/hash APIs. Domain schema is the existing Python case/body contract; there is no separate schema-file framework to introduce.

The AI registry exists in migrated src and #105 is closed. It covers five assistants and retained paths, denies live authority when unknown, and already has a proposal envelope. There is no registered form semantic-selection capability. Keep that actual prerequisite for any future AI selector, but deterministic/manual candidate staging makes no provider calls and does not require a new AI task.

Reflection: use a core form module and existing JSON/SQL stores, global versioned registry as a checked shared document and per-case append-only candidates. API exposes bounded registry and candidate operations only. Source hash/version and field-source policies are checked server-side; callers cannot assert authority.

### Contrarian

Challenged "parent dependency means #97 must wait": contradicted by exact #97 Dependencies None and present registry (#105). Challenged "approve fixtures to satisfy the story": rejected; no concrete approved form/template or delegated form authority exists in the inspected baseline. Mechanical schema registration must remain unapproved, and candidate staging is collection only, not assisted preparation. No approved form positive-path claim follows.

Challenged accepting caller-supplied source hash/authority: rejected. Source ID must belong to the current case, pass the existing scan and role checks, match stored and actual byte hashes, and carry source metadata copied by the server. Exact text spans/CSV cells can be verified by deterministic parsers; OCR imports must retain route/version/error/authority evidence and remain unverified candidates, never certify an OCR route. Unsupported input must return an owned manual-recovery result, without candidate invention.

Reflection: retain competing candidates, reject authority-bearing fields, append rather than replace; no selection/review/pack/staleness capability. Approved-schema preparation remains an explicitly unmet integration boundary rather than a fabricated approval mechanism.

### Parent synthesis and disposition

* Accepted: source-linked immutable registry, unapproved schema versions, candidate-only staging, existing store/ledger/version mechanisms (C1-C6).
* Rejected: extra UI/services; duplicate AI registry; automatic approvals, extraction, field acceptance or submission (W1-W3, C2-C3).
* Deferred: actual approved form authority, funding preparation/binding, OCR route approval, optional semantic selection and all #98 workflow.
* Another cycle: not needed. Named requirements and implementation contracts are covered; further live authority discovery would exceed the explicit offline boundary.

## Backlog scope/refinement review

Executed the requested `hve-core-all:github-backlog-manager` once, read-only, with one refined interpretation and no issue mutation. It confirmed hierarchy is not ordering, registry is conditional on enabled AI, and #98 owns review/validation/packs/staleness. The agent returned a stale `proper-warm-...` filename and incorrect line numbers and reported unavailable issue retrieval; those citations are rejected. Parent independently retrieved exact issues and uses actual local PRD path/lines below. No second refinement was run.

## Evidence log

| ID | Evidence | Finding |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/97 retrieved 2026-10-17 | Two criteria; Dependencies None; parent #96 is hierarchy |
| W2 | https://github.com/jmservera/ama/issues/96 retrieved 2026-10-17 | Parent requires AI task registry for assisted extraction; raw value, source ID/hash/locator required |
| W3 | https://github.com/jmservera/ama/issues/98 retrieved 2026-10-17 | Downstream review, validation, pack and staleness are excluded |
| W4 | https://github.com/jmservera/ama/issues/105 retrieved 2026-10-17 | Closed 2026-10-15, task registry and proposal envelope delivered; real authority still gated |
| C1 | docs/prds/zava-forward-retrofit-programme-demonstrator.md:873-874,1492-1499 | Exact FR-038/039 and AC-046/047/053; PRD status in-review at line 8 |
| C2 | docs/case_study_48_addendum.md:112-130 | Approved exercise assumptions distinguish source authority, funding fixture and real inference |
| C3 | src/core/src/zava_forward/core/ai_registry.py:1-15,29-49,100-157 | Existing registry, digest and unapproved envelope; no form-selection task |
| C4 | src/core/src/zava_forward/core/store.py:575-609,631-650 | Actual upload hash/version, scan, role and document access |
| C5 | src/core/src/zava_forward/core/sqlstore.py:419-455,526-639 | Sync, row versions, atomic body/audit writes and checked shared documents |
| C6 | src/core/src/zava_forward/core/mssqlstore.py:1-21; src/core/src/zava_forward/core/ledger.py:1 | Shared SQL dialect/transaction contract and existing canonical audit hashes |
| C7 | src/core/src/zava_forward/core/projection.py:36-73; src/api/src/zava_forward/api/server.py:100-125,760-866 | Existing role policy and authenticated case/API boundary |

## Alternatives and decisions

1. Reuse existing stores and add a bounded registry/staging contract: selected, least new machinery and no provider activation.
2. Build extraction, approval or review workspace: rejected, exceeds #97 and invents authority or parallel #98 capability.
3. Stop all engineering until real templates exist: rejected; safe unapproved collection is independently useful and explicitly permitted by caller. Real approved-template acceptance remains unmet.

## Risks and acceptance limits

No actual approved schema, delegation or current funding route was supplied. Neither fixture data nor authenticated exercise staff establish actual form authority. Registry output must say unapproved and never expose an endpoint that manufactures approval. New code must not accept body `approved`, `authority` or reviewer identity overrides. Unit/HTTP fixtures demonstrate mechanics only.

Source authority in schemas describes allowed kind/precedence/evidence policy; staging never upgrades a source to authoritative or picks a winner. OCR provenance is a retained supplied assertion, not a trusted extractor result; unsupported parsing has a visible manual path.

## Readiness

Research disposition: executed. Planning Readiness: Ready for bounded registry and candidate-only engineering. Approved-template preparation and full PRD acceptance remain unmet; no human approval invented.
