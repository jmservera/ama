<!-- markdownlint-disable-file -->
# Research: issue 148 C1 clock-accuracy correction (documentation only)

Actual `date -u` at start of C1, quoted from tool output: `Tue Nov 10 01:31:50 UTC 2026`. Research disposition: `executed`. Planning Readiness: `Ready`.

Original adverse finding (coordinator): the original records carry "Readback" times that were not observed. Original records, unchanged and linked: [research](2026-11-10-issue-148-four-images-research.md), [plan](../plans/2026-11-10-issue-148-four-images-plan.md), [details](../details/2026-11-10-issue-148-four-images-details.md), [critique](../plans/critiques/2026-11-10-issue-148-four-images-critique.md), [changes](../changes/2026-11-10-issue-148-four-images-changes.md), [review](../reviews/2026-11-10-issue-148-four-images-review.md). Their original outcomes stand (review: `conformant locally; independent exact-head review still required`).

Actual Git provenance (author and committer equal): parent `c9fa753f31f4983142c88cc5875c1f9e04042090` 2026-11-10T01:22:25+00:00; implementation `d305d0f90512fe448caf99b8520811660c2305cb` 2026-11-10T01:23:47+00:00; base `26bf987ca` 01:02:16+00:00. `git merge-base --is-ancestor c9fa753f3 d305d0f90` returned success. Source commit therefore descends from the prospective records commit.

Claimed readbacks: research 01:21Z, plan 01:30Z, details 01:30Z, critique 01:33Z, changes 01:45Z, review 01:47Z. Plan, details, critique, changes and review values are later than or inconsistent with the commits that contain them (critique 01:33, changes 01:45, review 01:47 are after the 01:23:47 head and the 01:31:50 present). The research 01:21Z matches an earlier observed `date -u` but was typed afterwards, so it is not an observed phase time either.
