---
title: Issue 350 live critique (2026-11-23)
---

Executed once on the final candidate plan. Verdict: proceed.

* Risk: counting a 403 or redirect as a pass. Disposition: applied; the note marks those unproven.
* Risk: reading `digests_checked` 0 as a defect. Disposition: applied; the job log and code path show the API checks local digests while the job checks blobs; recorded as design, not a gap.
* Risk: secrets or personal data in raw files. Disposition: applied; GUIDs and emails masked and files scanned.
* Risk: ticking issue boxes. Disposition: applied; none ticked.

No conflict with confirmed decisions.
