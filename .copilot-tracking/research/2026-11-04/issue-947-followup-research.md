<!-- markdownlint-disable-file -->
# Research: issue 947 null digest file raises TypeError

Disposition: executed. Planning Readiness: Ready.

## Prior delivery check

* Merged PR search for 947: only #777 mentions the number incidentally. Nothing delivered.

## Evidence

* `ledger.read_year_digests` returns whatever `json.load` yields, so a `year-*.json` containing `null`, a list or a scalar is passed on as-is. Only unparseable JSON became the fail-closed marker `{"unreadable": name}`.
* `ledger.verify_years` already tolerates non-dict entries (reports them in `bad_digests`), but `orchestrator.digest_blob.publish` ran `"year" not in d`, which raises TypeError for `None` and ints (reproduced before the fix) and would raise KeyError later for a list.
* The fail-closed contract is the existing one: an unreadable local year digest is reported and "never anchored".

## Smallest fix

* `read_year_digests`: treat any non-object JSON as unreadable (`{"unreadable": name}`).
* `publish`: guard with `isinstance(d, dict)` before reading keys.
* Not changed: `read_digests` (head digests, `digest-*.json`) has no tolerance for bad files; that is outside this issue's "year ledger digest file" wording.
* Focused tier. Touches audit-ledger integrity code but not auth, infrastructure, SQL or deployment; the gate is not run here and the coordinator decides.

## Acceptance criteria

* A null digest file fails closed, not TypeError: met for year digest files (read and publish paths).
* Regression test covers null and other non-object JSON: met.
