# Critique 2026-11-23, issue 116 live r9

Executed once on the final candidate plan. Verdict: proceed.

* Behaviour risk: counting string bytes of system plus user is stricter than the later body-length check only by JSON escaping, which makes the body longer, so no request accepted before is refused except those the later check refused anyway. Compatible; keep the later check as defence in depth.
* Evidence honesty: the change proves ordering at the shared boundary offline. Live payload contents stay unobservable; the box is not ticked by this change.
* Tier: src change, so FULL tier is required; the coordinator runs gates and `rpi-checks.py --all` is not run here.
