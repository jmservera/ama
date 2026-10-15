# Research: #106 suggestions, accept/reject, workflow-only fallback

Disposition: executed. Planning readiness: Ready.

* Existing in `mvp/zavaforward_mvp/ai_tasks.py`: citation resolution with Unverified marking, per-request workflow-only mode, comparison record with fallback reason, accept/edit/reject with reason, assistants runtime with source verification.
* Gaps: no distinct citation-resolved / source-verified / human-reviewed states on legacy AI records; review did not recheck the source; no hold; review evidence lacked versions and comparison.
* Accept already only sets status; the new test proves cases are unchanged (task or draft creation is a separate person action).
* Open items (owner/external): authorized competent human exercises, seeded-defect human detection and effort reports, UK/EU legal and privacy approval, live release. Not verifiable offline.
