# Issue #98 research (2026-11-14)

* Validation: `form_review._report` counted any Accepted/Corrected field as confirmed, trusting stored state without checking reviewer history.
* Pack: `form_export.draft_export` carried schema/template and input version at pack level only; fields and attachments had no explicit template_version/input_version.
* Planning readiness: Ready. Approved Finance rules (FD-01 to FD-14) stay held; this change claims no approval.
