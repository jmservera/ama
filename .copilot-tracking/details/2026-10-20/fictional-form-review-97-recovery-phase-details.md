<!-- markdownlint-disable-file -->
# RPI Phase Details: Fictional Finance form/template review pack (#97), recovery

## Metadata

* Task ID: 97-recovery
* Task slug: fictional-form-review-97-recovery
* Related plan: .copilot-tracking/plans/2026-10-20/fictional-form-review-97-recovery-plan.md
* Evidence sources: .copilot-tracking/research/2026-10-20/fictional-form-review-97-recovery-research.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|---|---|---|---|
| P01 | Reconcile pack, test and registration | ready | P01, P01-T01, P01-T02 |
| P02 | Knowledge base integration | ready | P02, P02-T01, P02-T02 |
| P03 | Validation and evidence | ready | P03, P03-T01 |

Locked test ownership: one file, src/core/tests/test_form_review_pack.py, owns introduced fixture behavior (registration compatibility on both stores, reviewer-substitution refusal, reference integrity, stale map exactness, null decisions, role separation, registry and privacy). Existing test_synthetic_provenance and test_form_staging are regression only. Removals: none. Maximum additions: the one test file and one JSON fixture. Canonical targets: the JSON fixture and provenance register; generated targets: none. Validation evidence: unittest output, ruff, ruff format, mypy.

<!-- rpi:phase id=P01 -->
## P01: Reconcile pack, test and registration

### Context

An uncommitted draft exists from a pre-RPI pass (unverified). Research C1-C8 and C12 define what it must satisfy.

### Intent

Make the draft an implementation-owned, verified artifact.

### Boundaries

* Included: the pack JSON, its test, its register entry.
* Excluded: forms.py or any runtime change; generator fixture.

### Likely Targets

* src/core/evals/fictional_form_review_pack.json: reconcile content.
* src/core/tests/test_form_review_pack.py: reconcile test.
* docs/reference/research/retrofit-synthetic-data/provenance-register.json: registration.

### Dependencies

* None

### Validation Expectations

* Focused tests, provenance and staging tests, core ruff and mypy pass.

### Completion Evidence

* Command outputs in the changes record.

### Unresolved Items

* None

<!-- rpi:task id=P01-T01 -->
### P01-T01: Verify and correct the pack fixture

#### Context

Draft has root not-approved labels, template FICT-FUND-FORM v1 with effective_from null, 16 fields (three human-only), calculations, field_review freshness, lineage expectations, roles, four stale triggers and FD-01..FD-14 null decisions.

#### Intent

Confirm every required element from the owner direction is present and every authority value is unresolved; correct gaps found. Critique-driven corrections (PC-001, PC-004, PC-005): add stale triggers for survey, design, funding-evidence, consent and source-age expiry (or align stale_on) so each field_review stale_on value maps to a trigger listing that field; add a statement that source ranks and evidence refs are fictional proposals pending FD-07 and FD-09.

Element to proof mapping (record in the changes record): field types, units, required, conditional (registration test); source authority and evidence (schema fields, fictional-proposal statement test); version and freshness (template block, field_review, age trigger test); parser/OCR lineage (lineage test); preparer/reviewer separation (roles test); stale propagation (trigger mapping test); unresolved Finance decisions (FD null test); labels (label test); registry and privacy (registry test).

#### Boundaries

* Included: content corrections, explicit no-submission and no-payment labels.
* Excluded: real terms, names, signatures, emails.

#### Likely Targets

* src/core/evals/fictional_form_review_pack.json

#### Dependencies

* None

#### Validation Expectations

* Test in P01-T02 passes; manual check that each requested element exists.

#### Completion Evidence

* Element checklist in changes record.

#### Unresolved Items

* None

<!-- rpi:task id=P01-T02 -->
### P01-T02: Verify the focused test and registration

#### Context

Draft test has six tests with two type-ignore comments for mypy.

#### Intent

Test only introduced behavior; keep registration `public` with a root_label contract. Critique-driven additions (PC-001, PC-002, PC-003, PC-005): assert every field stale_on maps to a trigger listing that field; assert NOT APPROVED, No submission, no payment and the fictional-proposal statement; assert stage_candidates refuses human-only fields on the registered pack schema and lineage keys match the contract (reuse test_form_staging helpers, no new harness).

#### Boundaries

* Included: test and register entry.
* Excluded: new harnesses or runtime.

#### Likely Targets

* src/core/tests/test_form_review_pack.py
* docs/reference/research/retrofit-synthetic-data/provenance-register.json

#### Dependencies

* P01-T01

#### Validation Expectations

* Run: cd src/core && PYTHONPATH=tests /tmp/ama-97-venv/bin/python -m unittest test_form_review_pack test_synthetic_provenance test_form_staging (recreate the venv with python3.12 and pip install -e src/core[dev] if missing)

#### Completion Evidence

* Passing output.

#### Unresolved Items

* None

<!-- rpi:phase id=P02 -->
## P02: Knowledge base integration

### Context

Registry entry points at data-dictionary.md#document-and-form-data; index row for #97 is at docs/reference/README.md; log is append-only.

### Intent

Make the pack discoverable and clearly non-approved.

### Boundaries

* Included: data-dictionary.md subsection, new note form-review-pack-97.md, src/core/README.md pointer, docs/reference/README.md row, docs/reference/log.md append, ms.date updates, dated clarification appended to the preserved draft artifacts.
* Excluded: infra runbook, budget/benefits synthesis, map, cohort docs.

### Likely Targets

* docs/reference/research/retrofit-synthetic-data/data-dictionary.md
* docs/reference/research/retrofit-synthetic-data/form-review-pack-97.md
* src/core/README.md
* docs/reference/README.md
* docs/reference/log.md

### Dependencies

* P01

### Validation Expectations

* Relative links resolve; git diff shows only allowed files.

### Completion Evidence

* Diff and link check in changes record.

### Unresolved Items

* None

<!-- rpi:task id=P02-T01 -->
### P02-T01: Dictionary subsection and review note

#### Context

Pack's Finance decisions need a reviewer-facing explanation of what to decide and what the pack does not prove.

#### Intent

Short subsection plus note listing the decision fields, how to review, labelled proposals (stale propagation, separation), and unmet criterion 1.

#### Boundaries

* Included: Markdown with frontmatter for the new note; ASCII; `*` bullets.
* Excluded: legal conclusions, real terms.

#### Likely Targets

* docs/reference/research/retrofit-synthetic-data/data-dictionary.md
* docs/reference/research/retrofit-synthetic-data/form-review-pack-97.md

#### Dependencies

* P01-T01

#### Validation Expectations

* Link review; the data-dictionary.md#document-and-form-data anchor exists; new text contains fictional, not approved, criterion 1 unmet (PC-007).

#### Completion Evidence

* Files exist; links resolve.

#### Unresolved Items

* None

<!-- rpi:task id=P02-T02 -->
### P02-T02: README pointer, index row, log entry, disclosure clarifications

#### Context

KB conventions require index and append-only log; coordinator requires disclosure on preserved draft artifacts.

#### Intent

Mechanical pointer/index/log; append a dated clarification section to each of the four preserved hand-authored artifacts without altering existing text.

#### Boundaries

* Included: append-only edits.
* Excluded: rewriting earlier log entries or the draft body.

#### Likely Targets

* src/core/README.md
* docs/reference/README.md
* docs/reference/log.md
* .copilot-tracking/*/2026-10-20/fictional-form-review-97-* (draft artifacts, append only)

#### Dependencies

* P02-T01

#### Validation Expectations

* Record SHA-256 of each preserved draft artifact before appending; afterwards the original bytes remain an exact prefix; log diff is additions only (PC-006).

#### Completion Evidence

* Diff review.

#### Unresolved Items

* None

<!-- rpi:phase id=P03 -->
## P03: Validation and evidence

### Context

Gate and Review follow implementation outside this plan.

### Intent

Prove the change and record evidence.

### Boundaries

* Included: focused tests, lint, changes record.
* Excluded: full gate (run after Review at freeze).

### Likely Targets

* .copilot-tracking/changes/2026-10-20/fictional-form-review-97-recovery-changes.md

### Dependencies

* P01, P02

### Validation Expectations

* All focused checks exit 0.

### Completion Evidence

* Recorded outputs.

### Unresolved Items

* None

<!-- rpi:task id=P03-T01 -->
### P03-T01: Focused checks and changes record

#### Context

Core quality gates: ruff check, ruff format --check, mypy in src/core.

#### Intent

Run and record results; write the changes record.

#### Boundaries

* Included: smallest covering commands.
* Excluded: broad suites.

#### Likely Targets

* .copilot-tracking/changes/2026-10-20/fictional-form-review-97-recovery-changes.md

#### Dependencies

* P01, P02

#### Validation Expectations

* From src/core: ruff check . ; ruff format --check . ; mypy. git diff --stat and git status show no change under src/core/src and none to excluded docs (PC-006).

#### Completion Evidence

* Changes record.

#### Unresolved Items

* None
