# Details: phase 1

Scan `src/*/src` and `infra` text files (py, js, html, md, bicep) for `production[- ](ready|grade|resilien...)` and "ready for production". A hit passes only when its line contains a negation or gating word. Self-test feeds the scanner a positive claim (must flag) and a negated one (must pass). Test-only change; no `src` runtime code changes.
