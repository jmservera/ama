# Critique: #148 current-source local image and dry-run proof (2026-11-10)

Single same-agent critique of the final candidate plan and details, performed once before implementation. It is not independent. Verdict: Proceed with changes. No finding conflicts with a confirmed decision, so none needed a user decision.

## Findings and dispositions

* F1 Medium, claim strength. `--no-cache` plus an in-image `apt-get upgrade` means image IDs are not derivable from source alone and bit-identical rebuild is untested. Applied: the handoff reports image IDs as observations of this run. Local Docker inspect later showed populated `RepoDigests`; these are local metadata and not registry resolution, publication or deployment evidence. Reproducibility was not assessed. (Corrected 2026-11-10; the original F1 text said no `RepoDigests` and that IDs were not reproducible.)
* F2 Medium, isolation. The maintained smoke starts containers on the default Docker network and cannot take `--network none` without editing it. Applied: record "no outbound call is made by the smoke code, but container network egress was not technically blocked" as a residual; do not claim a network-isolated runtime.
* F3 Low, container ID capture. A `docker events` watcher can miss a container if it starts late. Applied: the watcher starts before the smoke and a post-check by `ancestor=` image lists leftovers; a missing ID is reported as unobserved, not guessed.
* F4 Low, dry-run proof strength. Static reading of `main()` is not proof. Applied: the run uses `env -i`, an empty `PATH` directory (no `az`), an empty `HOME`, and `unshare -rn`; if the namespace is unavailable the isolation file says so and the claim is reduced to "no az on PATH, no credentials in environment".
* F5 Low, worktree cleanliness. pip may write build output in the source tree. Applied: install from a `git archive` copy, and check `git status` for `src/` and `infra/` before and after.
* F6 Low, capacity. About 2 GiB memory was available at inspection. Applied: sequential execution under `nice` and CPU pinning; an out-of-memory or daemon failure is classified as environmental with the first failure preserved, no retry.
* F7 Info, scope. A dry-run with a zero-GUID subscription and a synthetic registry name proves the offline plan path only, not tenant correctness. Applied: stated in details "Not covered".

## Verdict

Proceed with changes; all seven applied to the plan, details and handoff wording (F1 to F7 are reflected in the Not covered and residual statements). Critique is not repeated for this task.
