---
title: Issue 531 derive retry counts review
ms.date: 2026-11-03
---

* Review execution: executed once, self-review of the diff against plan and criteria; no independent reviewer.
* Outcome: Conformant for the scoped slice; not a closure of the issue.
* Checked: expected counts still equal 4 today (one load plus three delays), so behaviour of the check is unchanged; a future change to `SCRIPT_RETRY_DELAYS` now moves the check with it. No product code, approval boundary or consent behaviour changed.
* Criteria: 1 to 6 evidenced by merged work; criterion 7 (live verification on the employee site) remains UNMET and owner-run. Use Refs #531.
* Routed follow-ups: owner live run via `checks/employee_live_acceptance.py` after redeploy; human screen-reader and voice-control acceptance; independent review of this PR.
