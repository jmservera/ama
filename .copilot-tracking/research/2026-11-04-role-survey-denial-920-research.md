# Research: expected denials for the other roles (Refs #920)

Disposition: reused (research 2026-11-04 admin-routes-denial-920) plus a Chromium probe. Planning readiness: Ready.

## Already delivered (merged PRs)

* #929, #1017, #1061, #1006, #1120: photo, law alerts, regulatory chat status, assistants, admin-only landing and 11 admin-only case-data routes, strict mypy. Criterion 1 ticked.
* Open follow-up from the 2026-11-04 review: survey the other roles for expected 403/503.

## Probe (synthetic loopback server, trusted-proxy provider, law store off, no photo token)

* Seven staff roles (Coordinator, Liaison, Safety Liaison, Grants, Quality Inspector, Programme Manager, Support Officer): every navigation route plus #/case/ZF-1 and #/assistants gave no 4xx and no console error.
* Contractor: navigation routes plus #/case/ZF-1 gave no 4xx and no console error.
* No defect found; no app change needed. The gap was that no committed browser test covered these roles.

## Environment note

* The editable installs resolve to the primary checkout, so probes need PYTHONPATH set to this worktree's src folders. Not a repository defect.
