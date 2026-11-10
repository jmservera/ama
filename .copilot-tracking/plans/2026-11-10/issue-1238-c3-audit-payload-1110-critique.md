<!-- markdownlint-disable-file -->
# Critique: issue 1238 C3 audit payload provenance (1110)

Execution: one inline self-critique, 2026-11-10T01:00Z, before any test or
source edit. This cycle forbids nested agents, so no independent critique agent
ran; this is the author's critique, not an independent one. Not repeated.
Verdict: Proceed, with the dispositions below applied directly to the details.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Medium | The digest must also bind the exact reservation, or an approval could move between attempts of one request | Already in the payload (reservation id and attempt number) |
| PC-002 | Medium | The first-authorization detail is written after the handler returns; the completing detail must carry the digest too, or replay cannot be compared | Both returns use `_approval_detail` |
| PC-003 | Low | The digest uses the current binding, so a restamp is caught only if the old audit digest differs; same binding id and digest is by design identical | Accepted; restoration remains documented unsupported |
| PC-004 | Low | Evidence text must not enter the audit | Only its SHA-256 enters the payload; a test asserts the raw text is absent |
