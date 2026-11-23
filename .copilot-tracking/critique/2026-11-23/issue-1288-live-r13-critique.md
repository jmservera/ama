---
title: Critique r13 for issue 1288 (executed once)
date: 2026-11-23
---

Verdict: compatible, proceed.

* Risk: changing snapshot shape. Mitigation: keys exist only for implausible rows; no VERSION bump needed, existing digests unchanged.
* Risk: scope creep into a current-capture downgrade. Decision: out of scope; stated as a limit.
* Risk: false positives. Limits are the same constants the UI health badge already uses, so UI and model agree.
* No conflict with confirmed owner decisions; no release record, Azure change or push involved.
