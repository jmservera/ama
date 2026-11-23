---
title: Critique for issue 1274 live run 5
---

Executed once. Verdict: proceed.

* Risk: a text-scan test could be brittle. Mitigation: assert narrow, stable facts (installer invocation, version string, no `releases/download` in curl/wget lines of non-generated workflows).
* Generated `*.lock.yml` workflows are excluded; they follow the compiler route and are not hand-edited.
* No src change: focused tier.
