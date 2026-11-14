# Research: #233 same-home walk hardening (2026-11-14)

Disposition: reused (prior 0925 and tensions research) plus a targeted probe. Planning Readiness: Ready. Stacked on #1639 at `656bf1cf1`; `Refs #233`.

* The stage map already carries the exact `case` id on every link. Gaps: no explicit case badge on the selected-home panel, and a record whose id differs from the requested `case` would still render under that screen.
* The case API exposes no UPRN to the web client, so the badge uses the case reference only. No UPRN is invented.
* `resident_demo` untouched. Heading-hierarchy browser test fails 35 cases before and after this change (pre-existing, environment); not caused here.
