<!-- markdownlint-disable-file -->
# Details: issue 120 slice 1

## Phase 1: code

* `src/api/src/zava_forward/api/timecapture.py`: `status()` computes `notice = bool(ZF_TIME_NOTICE_APPROVED) and ZF_TIME_NOTICE_VERSION.strip() == NOTICE_VERSION`. A missing reference keeps its existing reason; a reference with a wrong or missing version gets a reason naming `ZF_TIME_NOTICE_VERSION`. `notice_approved` in the status payload uses the combined value, so request, activation, acknowledgement, recording, listing and reports all refuse through the existing `_ready_to_enable` and `_require` paths. No schema or DDL change.

## Phase 2: tests

* `src/api/tests/test_timecapture.py`: existing env fixtures now set the version. New `test_approval_must_cover_the_current_notice_version` (missing, blank, old, near-miss versions refuse request, activation and recording; trimmed match enables; a changed version disables and restoring it re-enables the existing record). The notice-version bump test now proves capture is off until the version is re-confirmed, then the acknowledgement requirement applies.

## Phase 3: docs

* `src/api/README.md`: time capture paragraph and environment table list `ZF_TIME_NOTICE_VERSION`.
