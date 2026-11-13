# Review: #521 API cutoff test proof (code-review, one pass)

Outcome: conformant with minor findings. Boundary: tracking-only changes; no `src/`, `infra/`, `docs/` edits.

Confirmed: assertions match the tests; 6 + 47 = 53 tests; no skips; proof limits honest; no secrets.

Findings routed to follow-up (not fixed in this task):

1. Compact `-v` log not retained, only its sha256; run cannot be re-verified from the repo. Also PYTHONDONTWRITEBYTECODE and egg-info cleanup not itemised (`git status --ignored` was clean). Mitigation: the two boundary tests' `-v` lines were observed `ok` during the run (changes file names them).
2. State/changes status wording mismatch is pre-review bookkeeping; state records Review as the next action and is finalised in `review-done`.
3. Follow-up: add 2027-12-31T23:59:59Z and +1s/+1ms assertions and rename the "february" test (needs a src-test change task).
