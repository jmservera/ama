---
title: Details for issue 73 live run r2 (2026-11-19)
---

* Children and live GitHub state (read 2026-11-19): closed 74, 75, 77, 78, 135, 183; open 76 (1 unticked), 79 (2), 80 (1). Epic 73 has 3 unticked; #440 open with 2 unticked.
* Test checks: every child number appears in the note; closed children are marked CLOSED; open children record their unticked count and residual; epic rows 1 and 2 say "Not met" and "No."; no line says the epic is closed, accepted or approved without a negation.
* Test reads the note only; it never asserts live GitHub state.
* Live read: Azure CLI `az containerapp show` for `ca-cutover-test-demo-api` (revision, digest, no secrets).
