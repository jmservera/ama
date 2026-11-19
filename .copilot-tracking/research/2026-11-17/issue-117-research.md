# Research: issue 117 scan, retention, legal hold design

Disposition: executed. Planning Readiness: Ready.

## Measured baseline (2026-11-17, base eb51af5c)

* `docs/design/` does not exist; no single design describes scan, retention and hold behaviour. Behaviour is in the `doc_controls.py` docstring, ADR 0002 decision 2 and PRD DH-003.
* Code facts (`src/core/src/zava_forward/core/doc_controls.py`): scan statuses clean/infected/mismatch/pending; only clean is available; bad verdicts delete the blob; `rescan_pending` is a job entry point with no scheduler; ZF_SCANNER local (default) or defender; Defender tag `Malware Scanning scan result`, clean value `No threats found`, bad `Malicious`; retention years EPC 6, Survey 6, Design 6, Consent 3, Funding evidence 7, Photo 3, Other 1 (synthetic placeholders); hold is case-level, placed and released by the programme manager role; retention_due lists only, approval deletes one document and is blocked by an active hold.
* `infra/modules/storage.bicep`: blob versioning on and 30-day soft delete, so an approved retention deletion leaves bytes recoverable for up to 30 days (and in versions); no Defender for Storage resource; `governance.bicep` Defender plans default off.
* Gaps for design: no pending timeout or alert, no scheduler cadence, hold placed and released by one role (no segregation), no hold on a single document, erasure versus soft delete/versioning unresolved, Defender tag race and tag-write permissions.

## Constraints
Docs only; no live resources; PR-003 periods stay placeholders; DPO/Legal/record owners approve; no scope in #1818/#1641 (core mssqlstore, chat grounding).
