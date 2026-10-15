# Plan: #120

1. Require `ZF_TIME_NOTICE_APPROVED` and an audited manager enabling record (`time_enabled`, void if references change).
2. `POST /api/time/enable` (manager only) writes audit `time_capture_enabled`.
3. `#/time` screen (status checklist, notice, record, own entries, manager report).
4. Tests, README, ADR 0002 row, KB log.

Critique: executed once; compatible findings applied (void activation on reference change; no PII in report).
