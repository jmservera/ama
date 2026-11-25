---
title: Issue 2303 critique, revision 0000069 (2026-11-25)
---

Executed once. Verdict: proceed. The image already holds the fix, so no source change is justified; fabricating one would break the Tier rule. Risk: the 105 to 126 s latency could be mistaken for a failure; it is recorded as a caveat, not a criterion. The `networkidle` tolerance in the copied probe is a harness change only.
