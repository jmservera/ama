# Plan: #430

* Add `retries: 3` to the Publish verdict github-script step (default exempt codes 400/401/403/404/422 are not retried; 5xx are).
* Recompile with `gh aw compile rubric-score` so the lock file matches.
* Validate: pytest .github/rubric/scripts (17 failures identical on base, pre-existing); lock YAML parses.
* Critique: executed once, verdict proceed; no conflicting findings.
