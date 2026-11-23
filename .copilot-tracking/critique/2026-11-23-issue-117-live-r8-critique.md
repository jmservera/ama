# Critique, issue 117, 2026-11-23 (executed once)

Verdict: proceed.

* Risk: tests that restate implementation. Mitigation: assert fail-closed outcomes (pending, unavailable, ValueError), which would fail if the reader or factory failed open.
* Risk: touching the live estate. Rejected; the brief forbids estate changes and the 2026-11-19 probe already showed network rules block it. Recorded as unproven.
* Risk: duplicating existing tests. The existing ones patch `tags`; the new ones drive the real `blob_tags` through a fake transport, which is not covered.
* Direct dispositions: keep to one test file, no source change, Focused tier.
