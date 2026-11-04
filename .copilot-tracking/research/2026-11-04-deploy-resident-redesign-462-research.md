# Research: deploy resident redesign (2026-11-04)

* Disposition: reused. Procedure from infra/README.md (live deploy sections): local docker build, short ACR window, bare-IP rule removal. `az acr build` fails in the window (hosted agents 403).
* Live before: demo API `--0000024` (4d56cf609), resident `--0000009`, `ZF_DEMO_EXPIRES_AT=2027-01-31T23:59:00Z`; demo API has no expiry env. Policy maximum 2028-01-01T00:00:00Z in resident-demo.json.
* Planning Readiness: Ready.
