<!-- markdownlint-disable-file -->
# Changes: C2 fingerprint-label correction (task 440-m2-c2-fingerprint)

Written 2026-11-10. Prospective record: `.copilot-tracking/plans/critiques/2026-11-10-m2-c2-fingerprint-440-prospective.md`. Documentation only.

## File changed

* `docs/architecture/cutover-evidence-pack.md`, Quality M2 section only: the H2 values paragraph now states the binding fingerprint `b4791e0c22b1f1be` (`binding_sha`) and the distinct task body fingerprint `cfc0f0a9922fd69f` (`task_body_sha`); an erratum bullet was added; "deferred" wording for the actual-model walkthrough, IoT Hub, Azure SQL and OS restart became "not run, admission pending, no owner-approved deferral".

## Unchanged by design

* The C1 review record (Conformant), the original research record (which carries the same mislabel, superseded by this erratum), earlier pack sections, README paragraph and log entry (neither repeats the mislabel), H0/H1/H2 observations.
* Equality result unchanged; no source, persistence or runtime defect inferred; both fingerprints are truncated 16-hex values, not byte identity.

## Validation (pure docs)

Diff confined to the pack file; ASCII scan of added lines clean; no new links; no src, infra, tools or .github diff. No runtime run.
