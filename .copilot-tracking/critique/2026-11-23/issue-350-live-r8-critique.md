# Issue 350 r8 critique (2026-11-23)

Executed once. Verdict: proceed.

* Applying an `/api` Easy Auth exemption would be unsafe (spoofable principal header, SPA needs platform principal); rejected.
* A static guard test on both Easy Auth modules is small, deterministic and protects the criterion 1 condition. Accepted.
* Must not claim criterion 1 proven; live probe still fails.
