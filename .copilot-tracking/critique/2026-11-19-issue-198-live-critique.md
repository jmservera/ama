# Issue 198 live critique (2026-11-19)

* Executed once, final candidate. Verdict: proceed.
* Risk: a skip hides workflows that gain a trigger later; mitigated because the test is parametrised per event and only skips events the workflow does not declare, which cannot run on a tracking-only change.
* Risk: sample path must match a real trigger; use a `src/` path, since `src/**` is the live trigger.
* Not in scope: retiring `mvp-ci.yml`/`mvp-validation.yml` (workflow_dispatch only); that is a workflow change needing a separate classification.
