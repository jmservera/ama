---
title: Issue 153 stale-stage plan critique
ms.date: 2026-11-12
task_id: 153-blocked-copy-readiness-1112
---

## Execution

One independent critique by a rubber-duck sub-agent of the final candidate plan; not repeated. Verdict: one blocking issue and two non-blocking issues; original API regression design judged sound (fails before change). No old-message consumers found in `src` or `docs`.

## Findings and direct dispositions

| Finding | Disposition |
| --- | --- |
| Blocking: "refresh and check history" is unsafe: reload may drop drafts, and the history panel labels an advance event "Returned" | Accepted. Wording becomes: "Copy any unsaved notes, then reload the case and check its current stage before taking further action." The history wording is not used. |
| Wording implies the case moved later and "Owner" may imply responsibility for the action | Accepted. "It may have changed since you opened it." and "Case owner: <name>." (the existing displayed Case owner). Add an earlier-stage test. |
| Content test is `src/api/tests/test_content_standard.py`; paths wrong; `/tmp` browser script not reproducible | Accepted. Run that test from `src/api`. Browser evidence remains the `/tmp` script output (recorded as non-repository evidence, a limitation); the committed regression is the API test. A browser unsaved-draft test of the recovery was not added: the client path is unchanged, so draft retention is untouched, and the wording asks the user to copy notes rather than relying on retention. |

No finding conflicts with a confirmed user decision. Plan amended in place: see the changes record.
