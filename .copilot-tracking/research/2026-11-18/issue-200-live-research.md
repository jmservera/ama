# Issue 200 live research (2026-11-18)

Disposition: executed. Planning Readiness: Ready.
Unticked criteria: 2 (workflow paths/Docker/requirements to src) and 3 (src image behaviour, deployed and verified).
Findings: criterion 2 already satisfied on main (src-ci.yml, src-deploy.yml use src context and src/api/requirements.txt; legacy file names kept deliberately; prototype workflow retired in #295). Criterion 3: local build and src/check-container.py pass; live revision --0000031 healthy on a zava-forward-api digest with no command override; historical revisions keep tags. A fresh push needs an ACR public window, out of demo authorisation.
Full evidence: docs/reference/research/src-repoint-live-audit-200-2026-11-18.md
