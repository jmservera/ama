# Critique: issue 2313 plan (single pass)

Verdict: accept with direct dispositions.

* Risk: `pull_request` workflows run PR-authored code. Disposition: the job has no credentials, no secrets, read-only token and no push, so it is the same exposure as `src-ci.yml`. Accepted.
* Risk: duplicating `src-ci.yml` image builds. Disposition: that job tags `:ci` and is gated by changed-images; this job adds the versioned tag and a container startup check; the cost is acceptable for the demo and path filtered. Accepted.
* Risk: editing `infra-plan.yml` breaks the pinned hash. Disposition: not edited. Accepted.
* Gap: a "what-if only on infra PRs" criterion already met by the `changes` job; recorded as proven by inspection, not live, because `INFRA_PLAN_ENABLED` is unset and OIDC is an owner action (no demo authority to create it).
