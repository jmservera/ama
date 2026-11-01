---
title: Dependabot alert triage research
ms.date: 2026-10-31
---

## Evidence

Source: `gh api repos/jmservera/ama/dependabot/alerts` (state open), retrieved 2026-10-31. 10 open alerts.

| Alerts | Package | Manifest | Patched | Locked before |
| --- | --- | --- | --- | --- |
| 24-26 (critical/high/low) | dompurify | tools/program-workbench-assets | 3.4.17 | nested 3.4.16 pinned by `overrides` |
| 40, 41 | nanoid | anc lock | 3.3.12 / 5.1.11 | 3.3.3 and 4.0.2 (exact pins in excalidraw packages) |
| 33-35 | lodash-es | anc lock | 4.17.23 / 4.18.0 | 4.17.21 (exact pins) |
| 43 | katex | anc lock | 0.18.2 | 0.16.47 |
| 23 | setuptools | src/build-requirements.txt | 84.1.0 | 84.1.0 (hash pinned by pip-compile) |

`npm audit` after the first pass showed newer nanoid advisories (GHSA-28wg-ghj8-5hjv, GHSA-2v37-7h3g-55p8) needing 3.3.18 and 5.1.16.

Planning Readiness: Ready. Research disposition: executed.
